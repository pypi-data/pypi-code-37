import abc

from combcov.exact_cover import ExactCover


class CombCov():

    def __init__(self, root_object, max_elmnt_size):
        self.root_object = root_object
        self.max_elmnt_size = max_elmnt_size
        self._enumerate_all_elmnts_up_to_max_size()
        self._create_binary_strings_from_rules()

    def _enumerate_all_elmnts_up_to_max_size(self):
        elmnts = []
        self.enumeration = [None] * (self.max_elmnt_size + 1)
        for n in range(self.max_elmnt_size + 1):
            elmnts_of_length_n = self.root_object.get_elmnts(of_size=n)
            self.enumeration[n] = len(elmnts_of_length_n)
            elmnts.extend(elmnts_of_length_n)

        self.elmnts_dict = {
            string: nr for nr, string in enumerate(elmnts, start=0)
        }

    def _create_binary_strings_from_rules(self):
        self.rules_dict = {}
        self.rules = []
        for rule in self.root_object.get_subrules():
            rule_is_good = True
            binary_string = 0
            for elmnt_size in range(self.max_elmnt_size + 1):
                seen_elmnts = set()
                for elmnt in rule.get_elmnts(of_size=elmnt_size):
                    if elmnt not in self.elmnts_dict or elmnt in seen_elmnts:
                        rule_is_good = False
                        break
                    else:
                        seen_elmnts.add(elmnt)
                        binary_string += 2 ** (self.elmnts_dict[elmnt])

                if not rule_is_good:
                    break

            if rule_is_good:
                self.rules.append(rule)
                self.rules_dict[rule] = binary_string

    def solve(self):
        self.ec = ExactCover(list(self.rules_dict.values()),
                             len(self.elmnts_dict))
        self.solutions_indices = self.ec.exact_cover()

    def get_solutions(self):
        solutions = []
        for solution_indices in self.solutions_indices:
            solution = [self.rules[binary_string] for binary_string in
                        solution_indices]
            solutions.append(solution)

        return solutions


class Rule(abc.ABC):
    @abc.abstractmethod
    def get_elmnts(self, of_size):
        pass

    @abc.abstractmethod
    def get_subrules(self):
        pass

    @abc.abstractmethod
    def __hash__(self):
        pass

    @abc.abstractmethod
    def __str__(self):
        pass
