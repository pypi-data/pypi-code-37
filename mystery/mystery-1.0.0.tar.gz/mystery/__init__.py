
# I'd like not to affect the current imported modules (besides 'mystery' of course).
# Using a function's scope to contain the imports makes it less of a headache during cleanup.
def _import_guard():
    """
    Attempt to import the chosen package and add it to sys.modules.
    """
    try:
        import awscli
    except ImportError as error:
        print('Internal error:', error)
        print("The mystery module wasn't playing nice. Sorry!")
        return
    import sys
    sys.modules['mystery'] = awscli
_import_guard()
del _import_guard
