import re
from collections import defaultdict, namedtuple
from functools import lru_cache
from functools import partial
from typing import Dict, Callable, List, Tuple, DefaultDict, Set

from pulp import *
from pulp import LpProblem, LpMinimize, LpStatusOptimal, LpStatus

from mungo.common import vparse
from mungo.repositorydata import get_repository_data, merge_repository_data, RepositoryData

from time import time

Version = namedtuple("Version", "version build")


def equal_compare(y):
    p = re.compile(y.replace(".*", "*").replace("*", "(\D.*)??\Z"))
    return lambda x: bool(p.match(x.version))


# 3.*
# 3a
# 3*
# 3.0a

operator_function: Dict[str, Callable[[Version, Version], bool]] = {
    ">=": lambda x, y: vparse(x.version) >= vparse(y.version),
    ">": lambda x, y: vparse(x.version) > vparse(y.version),
    "<=": lambda x, y: vparse(x.version) <= vparse(y.version),
    "<": lambda x, y: vparse(x.version) < vparse(y.version),
    "!=": lambda x, y: ~(vparse(x.version) == vparse(y.version))
                       and (vparse(x.version) < vparse(y.version, ".99999999999999")),
    "==": lambda x, y: vparse(x.version) == vparse(y.version),
    #    "=": lambda x, y: (vparse(x.version) >= vparse(y.version))
    #                      and (vparse(x.version) < vparse(y.version, ".99999999999999")),
}


def build_comp(x: Version, constraint: Version) -> bool:
    xb, yb = x.build, constraint.build
    return xb == yb \
           or yb.endswith("*") and xb.startswith(yb.rstrip("*")) \
           or yb == "*"


class Node:
    def __init__(self, name: str, version, p):
        self.name = name
        self.version = version
        self.distance_root = -1
        self._in_nodes = []
        self._out_nodes = defaultdict(list)
        self._x = None
        self.p = p
        self._mass_low = None
        self._mass_high = None
        self.invalid = False

    def add_in_node(self, n: 'Node'):
        self._in_nodes.append(n)

    def remove_in_node(self, n: 'Node'):
        self._in_nodes.remove(n)

    def add_out_node(self, n: 'Node'):
        self._out_nodes[n.name].append(n)

    def remove_out_node(self, n: 'Node'):
        self._out_nodes[n.name].remove(n)

    @property
    def channel_name(self) -> str:
        if self.p is None or "channel" not in self.p:
            return ""
        return self.p['channel'].split('/')[-2]

    @property
    def installed(self) -> bool:
        if self.p is None:
            return False
        # print(self.name, self.version, "installed" in self.p)
        return "installed" in self.p and self.p["installed"]

    @property
    def in_nodes(self) -> List['Node']:
        return self._in_nodes

    @property
    def out_nodes(self) -> List['Node']:
        for nodes in self._out_nodes.values():
            for n in nodes:
                yield n

    @property
    def x(self) -> LpVariable:
        # create LP variable, if not exist
        if self._x is None:
            self._x = LpVariable("{name}-{version}".format(name=self.name, version=self.version), 0, 1, LpInteger)
        return self._x

    def delete(self):
        for n in self.in_nodes:
            n.remove_out_node(self)
        for n in self.out_nodes:
            n.remove_in_node(self)


NodeDict = DefaultDict[str, Dict[str, Node]]


@lru_cache()
def valid_packages(ls: list, repodata: dict):
    # print(ls)
    all_valids = []
    for s in ls:
        name, is_valid = _valid_packages_function(s)
        all_valids.append(is_valid)

    # all_valid = lambda x: reduce((lambda a, b: a(x) and b(x)), all_valids)
    all_valid = lambda x: any([f(x) for f in all_valids])  # TODO: any or all?
    ret = [(name, x) for x in repodata.d[name] if all_valid(Version(*x))]
    return ret


def split_package_constraint(s: str) -> Tuple[str, List[List[List[str]]]]:
    or_split = s.split("|")
    ret = []
    name = None

    for o in or_split:
        term = []
        for x in o.split(","):
            res = re.split('(==|!=|>=|<=|=|<|>| )', x)
            res = [y for y in res if y != " " and len(y) > 0]
            if name is None:
                name = res.pop(0)
            term.append(res)
        ret.append(term)
    return name, ret  # foo, [[]]


# print(split_package_constain("pysocks 4 rc3"))
# print(split_package_constain("pysocks >=1.5.6,<2.0,!=1.5.7"))
# print(split_package_constain("pysocks>=   1.5.6,  <  2.0,!= 1.5.7"))
# print(split_package_constain("pysocks 1=4"))
# f()

def _valid_packages_function(s: str) -> Tuple[str, Callable[[Version], bool]]:
    name, or_constraints = split_package_constraint(s)

    and_valids = []

    for constraints in or_constraints:
        is_valids = []  # lambda x: True

        for c in constraints:
            len_c = len(c)
            if len_c == 0:
                # no version constraint
                pass
            elif len_c == 1:
                # version constraint without operator (equals ==)
                version = c[0]
                is_valids.append(equal_compare(y=version))
            elif len_c == 2:
                # version constraint
                operator, v = c
                version = Version(v, "*")
                if operator == "=":
                    is_valids.append(equal_compare(y=v))
                elif operator in [">=", ">", "<=", "<", "!=", "=="]:
                    is_valids.append(partial(operator_function[operator], y=version))
                else:
                    # version build constraint with no operator
                    version = Version(*c)
                    if version.version != "*":
                        is_valids.append(equal_compare(y=version.version))
                    is_valids.append(partial(build_comp, constraint=version))
            elif len_c == 3:
                # operator version build
                operator, v, b = c
                version = Version(v, b)
                if operator == "=":
                    is_valids.append(equal_compare(y=v))
                elif operator in [">=", ">", "<=", "<", "!=", "=="]:
                    is_valids.append(partial(operator_function[operator], y=version))
                is_valids.append(partial(build_comp, constraint=version))
            else:
                raise Exception("invalid version constraint", s)

        def all_valids(x, is_valids=is_valids):
            return all([f(x) for f in is_valids])

        and_valids.append(all_valids)
    or_valid = lambda x: any([f(x) for f in and_valids])
    return name, or_valid


def create_node(name: str,
                version: str,
                repodata: RepositoryData,
                sender: Node = None,
                all_nodes: NodeDict = defaultdict(dict),
                override_dependencies: List[str] = None,
                debug: bool = False):
    if version in all_nodes[name]:
        node = all_nodes[name][version]
        node.add_in_node(sender)  # add the parent to in-nodes
        return node

    # create new node
    if version in repodata.d[name]:
        p = repodata.d[name][version]
    else:
        p = None

    new_node = Node(name, version, p)

    if sender is not None:
        new_node.add_in_node(sender)

    all_nodes[name][version] = new_node

    # get package information from repodata
    if override_dependencies is not None:
        dependencies = override_dependencies
    else:
        dependencies = p["depends"]

    # multiple constraints may refer the same package
    # group them

    grouped_dependencies = defaultdict(list)
    for dependency in dependencies:
        name = split_package_constraint(dependency)[0]
        grouped_dependencies[name].append(dependency)
    # print("python >=3.7,<3.8.0a0", valid_packages(("python >=3.7,<3.8.0a0", ), repodata))
    # exit()

    # print("openssl 1.0.1", list(valid_packages(["openssl 1.0.1"], repodata)))
    # print("valid_packages", valid_packages(("jpeg 9b",), repodata))
    # exit()

    # print("valid_packages", valid_packages(("zlib 1.2.*",), repodata))
    # exit()

    # print("valid_packages", valid_packages(("blas 1.1 openblas",), repodata))
    # exit()

    # print("valid_packages", valid_packages(("openmpi",), repodata))
    # exit()

    # print(name, version, grouped_dependencies)

    for dependency in grouped_dependencies.values():
        d_node = None
        # make sure s is list like if string
        if isinstance(dependency, str):
            dependency = (dependency,)
        for d_name, d_version in valid_packages(tuple(dependency), repodata):
            d_node = create_node(d_name, d_version, repodata, new_node, all_nodes, debug=debug)
            new_node.add_out_node(d_node)

        if d_node is None:  # no versions were found for a dependency
            print_missing_package(dependency, debug=debug)
            new_node.invalid = True
            # raise Exception("no packages found for", *dependency)

    return new_node


def reduce_dag(all_nodes: NodeDict, channels: List[str]):
    # reduce DAG

    # for name, versions in all_nodes.items():
    #    for current_node in versions.values():
    #        print(current_node.name, current_node.version)

    channel_order = dict()
    for priority, channel in enumerate(reversed(channels)):
        if channel == "defaults":
            channel_order['main'] = priority
            channel_order['free'] = priority
            channel_order['pro'] = priority
            channel_order['r'] = priority
        else:
            channel_order[channel] = priority
        channel_order[""] = priority + 1  # highest priority for local installed packages

    nodes_to_remove = set()

    for name, versions in all_nodes.items():
        if name == "root":
            continue
        seen_keys = set()

        # if name == "ca-certificates":
        #     print(list(sorted(versions.keys(), key=lambda v: (channel_order[versions[v].channel_name] + versions[v].is_installed * (priority + 1), vparse(v)), reverse=True)))
        #     exit()

        # TODO the following line is also used in "base" and should be some kind of function import
        for v in sorted(versions.keys(),
                        key=lambda x: (channel_order[versions[x].channel_name]
                                       + versions[x].installed * (priority + 1), vparse(x[0])),
                        reverse=True):
            current_node = versions[v]
            in_node_key = tuple(sorted([(n.name, n.version) for n in current_node.in_nodes]))
            out_node_key = tuple(sorted([(n.name, n.version) for n in current_node.out_nodes]))
            key = (in_node_key, out_node_key)

            # if current_node.version[0] == "3.6.8":
            # print(current_node.channel_name, current_node.is_installed, current_node.name, current_node.version, key in seen_keys)

            if key in seen_keys:
                # the in-node out-node combination exist in a higher version of the same package
                # thus the higher version is ALWAYS preferable and this version can be removed
                nodes_to_remove.add(current_node)
            else:
                seen_keys.add(key)

    # remove the identified nodes
    for n in nodes_to_remove:
        n.delete()
        del (all_nodes[n.name][n.version])


def distances_dag(root: Node):
    q = [root]
    root.distance_root = 0

    while len(q) > 0:
        current_node = q.pop(0)
        for child in current_node.out_nodes:
            if child.distance_root == -1:
                child.distance_root = current_node.distance_root + 1
                q.append(child)


def tprint(msg):
    print(msg, "...")
    return time()


def create_dag(channels: List[str],
               packages: Set[str],
               local_repodata: List[RepositoryData],
               njobs: int = 8,
               offline: bool = False,
               force_download: bool = False,
               debug: bool = False) -> Tuple[NodeDict, Node]:

    start = tprint("Retrieving repository data ...")
    repodata_chunks = get_repository_data(channels, njobs, offline, force_download)
    print(f"Done ({time() - start:0.2f}s)")

    start = tprint("Merging repository data ...")
    repodata = merge_repository_data(local_repodata + repodata_chunks)
    print(f"Done ({time() - start:0.2f}s)")

    # add installed packages to the repodata

    # create dag
    start = tprint("Creating dag ...")
    default_packages = set()
    # default_packages = {"sqlite", "wheel", "pip"}
    all_nodes = defaultdict(dict)
    root = create_node("root", ("0", "0"), repodata, all_nodes=all_nodes,
                       override_dependencies=list(packages | default_packages), debug=debug)
    print(f"Done ({time() - start:0.2f}s)")

    # reduce DAG
    start = tprint("Reduce dag ...")
    reduce_dag(all_nodes, channels)
    print(f"Done ({time() - start:0.2f}s)")

    distances_dag(root)
    return all_nodes, root


def nodes_to_install(all_nodes: NodeDict, root: Node, channels: List[str]) -> List[Node]:
    channel_order = dict()
    for priority, channel in enumerate(reversed(channels)):
        if channel == "defaults":
            channel_order['main'] = priority
            channel_order['free'] = priority
            channel_order['pro'] = priority
            channel_order['r'] = priority
        else:
            channel_order[channel] = priority
        channel_order[""] = priority + 1  # highest priority for local installed packages

    # create ILP problem
    prob = LpProblem("DependencySolve", LpMinimize)

    # build LP on the reduced DAG
    objective = []
    prob += root.x == 1

    # n.p['channel'].split('/')[-2]

    # create brother information
    for name, versions in all_nodes.items():
        big_brother = None
        # small hack to make local always be the highest

        for v in sorted(versions.keys(),
                        key=lambda v: (
                                channel_order[versions[v].channel_name] + versions[v].installed * (priority + 1),
                                vparse(v[0])),
                        reverse=True):
            n = versions[v]
            n.big_brother = big_brother
            big_brother = n


    def mass(n: Node):
        if n is None:
            return 0, 0

#        if n.name == "attrs" and n.version == ('15.2.0', 'py36'):
#            for children in n._out_nodes.values():
#                print([(c.name, c.version) for c in children])
#        print("\tmass", n.name, n.version)

        if n._mass_low is None:
            # n._mass_low = 0  # temporarily set mass to 0 for loops in "DAG"
            # n._mass_high = 0  # temporarily set mass to 0 for loops in "DAG"
            n._mass_low = 1
            n._mass_high = 1
            m_low = 0
            m_high = 0
            # print(n.name, n.distance_root)
            for children in n._out_nodes.values():
                children_masses = [mass(c) for c in children if c.distance_root > n.distance_root]
                if len(children_masses) > 0:
                    m_low += min([c for c, _ in children_masses])
                    m_high += max([c for _, c in children_masses])
                else:
                    m_low = 0
                    m_high = 1
            # n._mass_low = m_low + 1 + mass(n.big_brother)[1]
            # n._mass_high = m_high + 1 + mass(n.big_brother)[1]
            n._mass_high = m_high - m_low + 1 + mass(n.big_brother)[1]
            n._mass_low = 1 + mass(n.big_brother)[1]
        return n._mass_low, n._mass_high

    # for name, versions in all_nodes.items():
    #     for version, n in versions.items():
    #         print(name, version, mass(n))

    #breadth first search
    seen = [root]
    current_index = 0
    while current_index < len(seen):
        e = seen[current_index]
        for c in e.out_nodes:
            if c not in seen:
                seen.append(c)
        current_index += 1

#    for n in reversed(seen):
#        print(n.name, n.version)
#        mass(n)
#    exit()

    # create ILP
    constraints = []
    for name, versions in all_nodes.items():
        # constraint: install at most one version of a package
        constraints.append(pulp.lpSum(n.x for n in versions.values()) <= 1)
        # exclude invalid node
        # constraint: if a parent is installed, one version of each dependency must be installed too
        for current_node in versions.values():
            #            print(current_node.name, current_node.version)

            if current_node.invalid:  # exlude invalid nodes
                constraints.append(current_node.x == 0)
                continue

            for out_group in current_node._out_nodes.values():
                constraints.append(pulp.lpSum([n.x for n in out_group]) >= current_node.x)

        # storing the objectives
        objective.extend([mass(n)[0] * n.x for n in versions.values()])
        # print([(n.name, n.normalized_version, n.factor) for n in versions.values()])

        if current_node is root:  # no no_install for root  # FIXME current_node might be uninitialized
            continue

    prob.setObjective(pulp.lpSum(objective))
    prob.extend(constraints)
    # prob.writeLP("WhiskasModel.lp")
    prob.solve()

    if prob.status != LpStatusOptimal:
        print(f"ERROR: Solution is not optimal (status: {LpStatus[prob.status]}).\nAborting.", file=sys.stderr)
        exit(1)

    # for v in prob.variables():
    #     print(v.name, v.varValue)

    # collect all install nodes
    install_nodes = []
    for _, versions in sorted(all_nodes.items()):
        for n in versions.values():
            # print(n.name, n.version, n.x.varValue, "installed" in n.p)
            if n.p is None:  # skip root
                continue
            x = n.x
            if x.varValue == 1.0:
                install_nodes.append(n)

    return install_nodes


missing_dependencies = set()


def print_missing_package(dependency: list, debug=False):
    if not debug:
        return
    # print missing package information for a dependency constraint
    # only print once by remembering
    dependency = tuple(dependency)
    if dependency not in missing_dependencies:
        print("WARNING:", "no packages found for", *dependency, file=sys.stderr)
        missing_dependencies.add(dependency)
