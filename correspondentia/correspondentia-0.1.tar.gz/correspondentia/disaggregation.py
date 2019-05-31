from copy import deepcopy


def equal_split(obj, matches, copy_func=deepcopy):
    allocation_factor = 1 / len(matches)
    for match in matches:
        child = copy_func(obj)
        child['correspondentia_allocation'] = allocation_factor
        yield child, match


def weighted_disaggregation(obj, matches, copy_func=deepcopy):
    total = sum([x.get('weight', 0) for x in matches])
    if not total:
        return equal_split(obj, matches, copy_func)

    for match in matches:
        child = copy_func(obj)
        child['correspondentia_allocation'] = match.get('weight', 0) / total
        yield child, match
