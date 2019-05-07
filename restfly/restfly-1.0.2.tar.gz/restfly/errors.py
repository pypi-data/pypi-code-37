'''
Errors
======

.. autoclass:: RestflyException
.. autoclass:: UnexpectedValueError
.. autoclass:: APIError
.. autoclass:: BadRequestError
.. autoclass:: UnauthorizedError
.. autoclass:: ForbiddenError
.. autoclass:: NotFoundError
.. autoclass:: InvalidMethodError
.. autoclass:: NotAcceptableError
.. autoclass:: ProxyAuthenticationError
.. autoclass:: RequestTimeoutError
.. autoclass:: RequestConflictError
.. autoclass:: NoLongerExistsError
.. autoclass:: LengthRequiredError
.. autoclass:: PreconditionFailedError
.. autoclass:: PayloadTooLargeError
.. autoclass:: URITooLongError
.. autoclass:: UnsupportedMediaTypeError
.. autoclass:: RangeNotSatisfiableError
.. autoclass:: ExpectationFailedError
.. autoclass:: TeapotResponseError
.. autoclass:: MisdirectRequestError
.. autoclass:: TooEarlyError
.. autoclass:: UpgradeRequiredError
.. autoclass:: PreconditionRequiredError
.. autoclass:: TooManyRequestsError
.. autoclass:: RequestHeaderFieldsTooLargeError
.. autoclass:: UnavailableForLegalReasonsError
.. autoclass:: ServerError
.. autoclass:: MethodNotImplementedError
.. autoclass:: BadGatewayError
.. autoclass:: ServiceUnavailableError
.. autoclass:: GatewayTimeoutError
.. autoclass:: NotExtendedError
.. autoclass:: NetworkAuthenticationRequiredError
'''
import logging

class RestflyException(Exception):
    '''
    Base exception class that sets up logging and handles some basic scaffolding
    for all other exception classes.  This exception should never be directly
    seen.
    '''
    def __init__(self, msg):
        self._log = logging.getLogger('{}.{}'.format(
            self.__module__, self.__class__.__name__))
        self.msg = str(msg)
        self._log.error(self.msg)

    def __str__(self):
        return self.msg

    def __repr__(self):
        return repr(self.__str__())


class UnexpectedValueError(RestflyException):
    '''
    An unexpected value error is thrown whenever the value specified for a
    parameter is outside the bounds of what is expected.  For example, if the
    parameter **a** is expected to have a value of 1, 2, or 3, and it is instead
    passed a value of 0, then it is an unexpected value, and this Exception
    should be thrown by the package.
    '''
    pass


# The following Exception codes have been written using the following link as
# a baseline (and the ):
# https://en.wikipedia.org/wiki/List_of_HTTP_status_codes


class APIError(RestflyException):
    '''
    The APIError Exception is a generic Exception for handling responses from
    the API that aren't whats expected.  The APIError Exception itself attempts
    to provide the developer with enough information around the response to
    ascertain what went wrong.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    retryable = False
    retries = None

    def __init__(self, r, retries=None):
        self.response = r
        self.code = r.status_code
        self.retries = retries
        RestflyException.__init__(self, '{} {} >> {}'.format(
            self.response.request.method,
            self.response.request.url,
            self.__str__()))

    def __str__(self):
        return '{}: {} {}'.format(
            str(self.code),
            str(self.response.request.method),
            str(self.response.request.url))


class BadRequestError(APIError):  # 400 Response
    '''
    The server cannot or will not process the request due to an apparent client
    error (e.g., malformed request syntax, size too large, invalid request
    message framing, or deceptive request routing).

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    pass


class UnauthorizedError(APIError):  # 401 Response
    '''
    Similar to 403 Forbidden, but specifically for use when authentication is
    required and has failed or has not yet been provided. The response must
    include a WWW-Authenticate header field containing a challenge applicable
    to the requested resource. See Basic access authentication and Digest access
    authentication. 401 semantically means "unauthenticated", i.e. the user
    does not have the necessary credentials.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''


class ForbiddenError(APIError):  # 403 Response
    '''
    The request was valid, but the server is refusing action. The user might
    not have the necessary permissions for a resource, or may need an account
    of some sort.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    pass


class NotFoundError(APIError):  # 404 Response
    '''
    The requested resource could not be found but may be available in the
    future. Subsequent requests by the client are permissible.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    pass


class InvalidMethodError(APIError):  # 405 Response
    '''
    A request method is not supported for the requested resource; for example,
    a GET request on a form that requires data to be presented via POST, or a
    PUT request on a read-only resource.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    pass


class NotAcceptableError(APIError):  # 406 Response
    '''
    The requested resource is only capable of generating content not
    acceptable according to the Accept headers sent in the request.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    pass


class ProxyAuthenticationError(APIError):  # 407 Response
    '''
    The client must first authenticate itself with the proxy.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    pass


class RequestTimeoutError(APIError):  # 408 Response
    '''
    The client did not produce a request within the time that the server was
    prepared to wait. The client MAY repeat the request without modifications
    at any later time.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    pass


class RequestConflictError(APIError):  # 409 Response
    '''
    Indicates that the request could not be processed because of conflict in
    the current state of the resource, such as an edit conflict between
    multiple simultaneous updates.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    pass


class NoLongerExistsError(APIError):  # 410 Response
    '''
    Indicates that the resource requested is no longer available and will not
    be available again. This should be used when a resource has been
    intentionally removed and the resource should be purged. Upon receiving a
    410 status code, the client should not request the resource in the future.
    Clients such as search engines should remove the resource from their
    indices. Most use cases do not require clients and search engines to purge
    the resource, and a "404 Not Found" may be used instead.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    pass


class LengthRequiredError(APIError):  # 411 Response
    '''
    The request did not specify the length of its content, which is required by
    the requested resource.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    pass


class PreconditionFailedError(APIError):  # 412 Response
    '''
    The server does not meet one of the preconditions that the requester put
    on the request.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    pass


class PayloadTooLargeError(APIError):  # 413 Response
    '''
    The request is larger than the server is willing or able to process.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    pass


class URITooLongError(APIError):  # 414 Response
    '''
    The URI provided was too long for the server to process. Often the result
    of too much data being encoded as a query-string of a GET request, in which
    case it should be converted to a POST request.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    pass


class UnsupportedMediaTypeError(APIError): # 415 Response
    '''
    The request entity has a media type which the server or resource does not
    support. For example, the client uploads an image as image/svg+xml, but the
    server requires that images use a different format.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    pass


class RangeNotSatisfiableError(APIError):  # 416 Response
    '''
    The client has asked for a portion of the file (byte serving), but the
    server cannot supply that portion. For example, if the client asked for a
    part of the file that lies beyond the end of the file.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    pass


class ExpectationFailedError(APIError):  # 417 Response
    '''
    The server cannot meet the requirements of the Expect request-header field.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    pass


class TeapotResponseError(APIError):  # 418 Response
    '''
    This code was defined in 1998 as one of the traditional IETF April Fools'
    jokes, in RFC 2324, Hyper Text Coffee Pot Control Protocol, and is not
    expected to be implemented by actual HTTP servers. The RFC specifies this
    code should be returned by teapots requested to brew coffee.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    pass


class MisdirectRequestError(APIError):  # 421 Response
    '''
    The request was directed at a server that is not able to produce a response

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    pass


    '''
    The request failed because it depended on another request and that request
    failed.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    pass


class TooEarlyError(APIError):  # 425 Response
    '''
    Indicates that the server is unwilling to risk processing a request that
    might be replayed.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    pass


class UpgradeRequiredError(APIError):  # 426 Response
    '''
    The client should switch to a different protocol such as TLS/1.0, given in
    the Upgrade header field.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    pass


class PreconditionRequiredError(APIError):  # 428 Response
    '''
    The origin server requires the request to be conditional. Intended to
    prevent the 'lost update' problem, where a client GETs a resource's state,
    modifies it, and PUTs it back to the server, when meanwhile a third party
    has modified the state on the server, leading to a conflict.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    pass


class TooManyRequestsError(APIError):  # 420 & 429 Response
    '''
    The user has sent too many requests in a given amount of time. Intended for
    use with rate-limiting schemes.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    retryable = True


class RequestHeaderFieldsTooLargeError(APIError):  # 431 Response
    '''
    The server is unwilling to process the request because either an individual
    header field, or all the header fields collectively, are too large.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    pass


class UnavailableForLegalReasonsError(APIError):  # 451 Response
    '''
    A server operator has received a legal demand to deny access to a resource
    or to a set of resources that includes the requested resource.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    pass


class ServerError(APIError):  # 500 Response
    '''
    A generic error message, given when an unexpected condition was encountered
    and no more specific message is suitable.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    pass


class MethodNotImplementedError(APIError):  # 501 Response
    '''
    The server either does not recognize the request method, or it lacks the
    ability to fulfil the request. Usually this implies future availability.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    retryable = True


class BadGatewayError(APIError):  # 502 Response
    '''
    The server was acting as a gateway or proxy and received an invalid
    response from the upstream server.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    retryable = True


class ServiceUnavailableError(APIError):  # 503 Response
    '''
    The server cannot handle the request (because it is overloaded or down for
    maintenance). Generally, this is a temporary state.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    retryable = True


class GatewayTimeoutError(APIError):  # 504 Response
    '''
    The server was acting as a gateway or proxy and did not receive a timely
    response from the upstream server.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    retryable = True


class NotExtendedError(APIError):  # 510 Response
    '''
    Further extensions to the request are required for the server to fulfil it.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    pass


class NetworkAuthenticationRequiredError(APIError):  # 511 Response
    '''
    The client needs to authenticate to gain network access. Intended for use
    by intercepting proxies used to control access to the network

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    '''
    pass