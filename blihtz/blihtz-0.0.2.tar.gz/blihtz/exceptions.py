class BlihtzException(Exception):
    """A generic exception class."""

    message = 'An error occurred'

    def __init__(self, message: str = None):
        """The class constructor."""

        if message is not None:
            self.message = message

    def __str__(self):
        """Get the object string representation."""

        return self.message


class AuthenticationException(BlihtzException):
    """Failed to authenticate using the credentials provided."""

    message = 'Authentication failed'


class UnavailableException(BlihtzException):
    """The resource is not available."""

    message = 'Unavailable'


class NotFoundException(BlihtzException):
    """The resource was not found."""

    message = 'Not found'


class UnauthorizedException(BlihtzException):
    """The authorization was not granted."""

    message = 'Unauthorized'
