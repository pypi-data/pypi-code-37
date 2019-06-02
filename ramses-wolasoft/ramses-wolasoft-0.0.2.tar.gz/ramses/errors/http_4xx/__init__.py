"""Http 4XX erors package"""

from .bad_request_error import BadRequestError
from .forbidden import ForbiddenError
from .not_found_error import NotFoundError
from .http_4xx_errors_mapper import http400, http401, http403, http404
