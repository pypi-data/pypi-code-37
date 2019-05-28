from mungo.conda.models.version import VersionOrder

mungoversion = "0.5.4"


def vparse(x: str, add: str = "") -> VersionOrder:
    # TODO: remove strip?
    if x != "*":
        x = x.strip("*").strip(".")
    return VersionOrder(f"{x}{add}")


def print_dag(packages: list, all_nodes: list, to_install: list, installed: dict = None):
    from graphviz import Digraph
    dot = Digraph()
    # dot.attr("graph", splines="false")

    # ugly, but sufficient for the time being
    to_install2 = {node.p['name']: node.p for node in to_install}
    installed_keys = installed.keys() if installed is not None else {}
    changed = installed_keys & to_install2.keys()
    local_versions = {name: list(installed[name].values())[0] for name in changed}
    remote_versions = {name: data for name, data in to_install2.items() if name in changed}
    version_changes = {package: (local_versions[package], remote_versions[package]) for package in changed}
    upgrades = {package: (p_from, p_to)
                for (package, (p_from, p_to)) in version_changes.items()
                # if vparse(([p_from['version'], p_from['build']])) < vparse(([p_to['version'], p_to['build']]))
                if vparse(p_from['version']) < vparse(p_to['version'])
                }
    downgrades = {package: (p_from, p_to)
                  for (package, (p_from, p_to)) in version_changes.items()
                  if vparse(p_from['version']) > vparse(p_to['version'])
                  # if vparse(([p_from['version'], p_from['build']])) > vparse(([p_to['version'], p_to['build']]))}
                  }
    # nodes
    out_nodes = set()
    for v in to_install:
        # color = "white" if v.name not in changed else "red"
        requested = v.name in packages
        upgrade = v.name in upgrades
        downgrade = v.name in downgrades
        local = v.name in installed_keys
        kwargs = {
            # 'shape': "house" if upgrade else "invhouse" if downgrade else "folder" if local else "note",
            'shape': "folder" if local else "note",
            'fillcolor': "#C0E2E7" if requested else "#CFE7C0" if upgrade else "#E7C6C0" if downgrade else "white",
            'style': 'filled',
            'fontname': 'Fira Sans',
        }
        dot.node(f"{v.name}_{v.version}", f"{v.name}\n{v.version[0]} {v.version[1]}", **kwargs)
        out_nodes.add(v)

    # edges
    for v in to_install:
        for c in v.out_nodes:
            if c in out_nodes:
                for d in v.p["depends"]:
                    if d.startswith(c.name):  # finde dependency
                        kwargs = {
                            'fontname': 'Fira Sans',
                        }
                        dot.edge(f"{v.name}_{v.version}", f"{c.name}_{c.version}",
                                 label='\n'.join(d.split(' ')),
                                 weight=f"{v.distance_root}",
                                 **kwargs)
    dot.render('graph.tmp', view=True)
    print(dot.source)
