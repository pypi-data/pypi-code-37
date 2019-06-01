class AllowsException(Exception):
    """
    Raised when invariants are violated while creating SideEffects (like multiple side
    effects specified)
    """
