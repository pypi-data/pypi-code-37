from .disaggregation import weighted_disaggregation as wd

DEFAULTS = ('exact', 'disaggregation')


def match_fields(data, correspondence, field, match_types=DEFAULTS,
                 split_function=wd, log_function=None):
    """Match fields in ``data`` to new labels in ``correspondence``. Returns an iterator.

    By default, handles exact (1-to-1) matches, and disaggregation (1-to-N) matches. Aggregation of similar records (for M-to-N or N-to-1 matches) should take place after this function is run.

    Only matches one field at a time, you should call this for each field to be mapped.

    Arguments:

        * ``data``: An iterable of dictionaries.
        * ``correspondence``: A dictionary in the prescribed form.
        * ``field``: A key in each element of ``data``.

    Returns an iterator of modified elements of ``data`` (or unmodified if no match can be made).

    """
    for row in data:
        if field not in row or row[field] not in correspondence:
            # No information to make changes
            yield row

        matches = [obj
                   for obj in correspondence[row[field]]
                   if obj['type'] in match_types]

        if len(matches) == 1:
            # No disaggregation needed
            row[field] = matches[0]['value']
            yield row
        else:
            for new_row, match in split_function(row, matches):
                new_row[field] = match['value']
                yield new_row
