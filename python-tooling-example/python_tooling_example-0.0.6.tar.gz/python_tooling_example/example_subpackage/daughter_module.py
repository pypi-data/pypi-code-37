"""Another example module, this time inside of a subpackage."""


def concat_2(a):
    """Concatenate the string "2" to to the end of an existing string object.

    Parameters
    ----------
    a : string
        The string to be concatenated to.

    Returns
    -------
    a+"2" : string
        The resulting string.

    Notes
    -----
    Uses the built-in ``+`` operator.
    """
    return a + "2"
