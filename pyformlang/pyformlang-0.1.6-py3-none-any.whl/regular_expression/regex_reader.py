import re

from pyformlang.regular_expression.regex_objects import CONCATENATION_SYMBOLS, UNION_SYMBOLS, KLEENE_STAR_SYMBOLS, \
    EPSILON_SYMBOLS, to_node, Operator, Symbol, Concatenation, Union, KleeneStar, MisformedRegexError

MISFORMED_MESSAGE = "The regex is misformed here."

WRONG_PARENTHESIS_MESSAGE = "Wrong parenthesis regex"


class RegexReader(object):
    def __init__(self, regex: str):
        self._current_node = None
        self._end_current_group: int = 0
        regex = pre_process_regex(regex)
        self._regex = regex
        self._components = get_regex_componants(regex)
        self._pre_process_input_regex_componants()
        self._setup_sons()
        self._setup_from_regex_componants()

    def _remove_useless_extreme_parenthesis_from_components(self):
        if self._begins_with_parenthesis_components():
            self._remove_useless_extreme_parenthesis_from_componants_when_starting_with_parenthesis()

    def _pre_process_input_regex_componants(self):
        self._remove_useless_extreme_parenthesis_from_components()
        self._compute_precedence()
        self._remove_useless_extreme_parenthesis_from_components()

    def _remove_useless_extreme_parenthesis_from_componants_when_starting_with_parenthesis(self):
        if self._is_surrounded_by_parenthesis():
            self._components = self._components[1:-1]
            self._remove_useless_extreme_parenthesis_from_components()

    def _is_surrounded_by_parenthesis(self):
        parenthesis_depths = self._get_parenthesis_depths()
        first_complete_closing = _find_first_complete_closing_if_possible(parenthesis_depths)
        return first_complete_closing == len(self._components) - 1

    def _get_parenthesis_depths(self):
        depths = [0]
        for component in self._components:
            depths.append(depths[-1] + _get_parenthesis_value(component))
        return depths[1:]

    def _begins_with_parenthesis_components(self):
        return self._components[0] == "("

    def _setup_precedence_when_not_trivial(self):
        self._set_end_first_group_in_components()
        if self._end_current_group == len(self._components):
            self._current_node = None
        else:
            self._current_node = to_node(self._components[self._end_current_group])

    def _setup_precedence(self):
        if len(self._components) <= 1:
            self._current_node = None
        else:
            self._setup_precedence_when_not_trivial()

    def _found_no_union(self, next_node):
        return self._end_current_group < len(self._components) and not isinstance(next_node, Union)

    def _add_parenthesis_around_part_of_componants(self, index_opening, index_closing):
        self._components.insert(index_opening, "(")
        # Add 1 as something was added before
        self._components.insert(index_closing + 1, ")")

    def _compute_precedent_when_not_kleene_nor_union(self):
        while self._found_no_union(self._current_node):
            self._set_next_end_group_and_node()
        if isinstance(self._current_node, Union):
            self._add_parenthesis_around_part_of_componants(0, self._end_current_group)

    def _compute_precedence(self):
        """ Add parenthesis for the first group in indicate precedence """
        self._setup_precedence()
        if isinstance(self._current_node, KleeneStar):
            self._add_parenthesis_around_part_of_componants(0, self._end_current_group + 1)
            self._compute_precedence()
        elif not isinstance(self._current_node, Union):
            self._compute_precedent_when_not_kleene_nor_union()

    def _set_next_end_group_and_node(self):
        if isinstance(self._current_node, Operator):
            self._end_current_group += 1
        self._set_end_first_group_in_components(self._end_current_group)
        if self._end_current_group < len(self._components):
            self._current_node = to_node(self._components[self._end_current_group])

    def _set_end_first_group_in_components(self, idx_from=0):
        """ Gives the end of the first group """
        if idx_from >= len(self._components):
            self._end_current_group = idx_from
        elif self._components[idx_from] == ")":
            raise MisformedRegexError(WRONG_PARENTHESIS_MESSAGE, " ".join(self._components))
        elif self._components[idx_from] == "(":
            parenthesis_depths = self._get_parenthesis_depths()
            first_complete_closing = _find_first_complete_closing_if_possible(parenthesis_depths, idx_from)
            if first_complete_closing > 0:
                self._end_current_group = first_complete_closing + 1 + idx_from
            else:
                raise MisformedRegexError(WRONG_PARENTHESIS_MESSAGE, " ".join(self._components))
        else:
            self._end_current_group = 1 + idx_from

    def _setup_non_trivial_regex(self):
        self._set_end_first_group_in_components()
        next_node = to_node(self._components[self._end_current_group])
        if isinstance(next_node, KleeneStar):
            self.head = next_node
            self.sons.append(self._process_sub_regex(0, self._end_current_group))
        else:
            begin_second_group = self._end_current_group
            if isinstance(next_node, Symbol):
                self.head = Concatenation()
            else:
                self.head = next_node
                begin_second_group += 1
            self.sons.append(self._process_sub_regex(0, self._end_current_group))
            self.sons.append(self._process_sub_regex(begin_second_group, len(self._components)))

    def _setup_empty_regex(self):
        self.head = to_node("")

    def _setup_one_symbol_regex(self):
        first_symbol = to_node(self._components[0])
        self._check_is_valid_single_first_symbol(first_symbol)
        self.head = first_symbol

    def _setup_from_regex_componants(self):
        if not self._components:
            self._setup_empty_regex()
        elif len(self._components) == 1:
            self._setup_one_symbol_regex()
        else:
            self._setup_non_trivial_regex()

    def _process_sub_regex(self, idx_from, idx_to):
        sub_regex = " ".join(self._components[idx_from:idx_to])
        return self.from_string(sub_regex)

    def _check_is_valid_single_first_symbol(self, first_symbol):
        if not isinstance(first_symbol, Symbol):
            raise MisformedRegexError(MISFORMED_MESSAGE, self._regex)

    def _setup_sons(self):
        self.sons = []

    def from_string(self, sub_regex):
        return RegexReader(sub_regex)


def _find_first_complete_closing_if_possible(parenthesis_depths, index_from=0):
    try:
        first_complete_closing = parenthesis_depths.index(0, index_from)
    except ValueError:
        first_complete_closing = -2
    return first_complete_closing


def _get_parenthesis_value(component):
    if component == "(":
        return 1
    elif component == ")":
        return -1
    else:
        return 0


def pre_process_regex(regex: str) -> str:
    regex = re.sub(r"\s+", " ", regex.strip())
    res = []
    pos = 0
    for current_c in regex:
        if (current_c in CONCATENATION_SYMBOLS
            or current_c in UNION_SYMBOLS
            or current_c in KLEENE_STAR_SYMBOLS
            or current_c in EPSILON_SYMBOLS
            or current_c in [")", "("]) and \
                pos != 0 and res[-1] != " ":
            res.append(" ")
        res.append(current_c)
        if (current_c in CONCATENATION_SYMBOLS
            or current_c in UNION_SYMBOLS
            or current_c in KLEENE_STAR_SYMBOLS
            or current_c in EPSILON_SYMBOLS
            or current_c in [")", "("]) and \
                pos != len(regex) - 1 and regex[pos + 1] != " ":
            res.append(" ")
        pos += 1
    return "".join(res)


def get_regex_componants(regex):
    return regex.split(" ")
