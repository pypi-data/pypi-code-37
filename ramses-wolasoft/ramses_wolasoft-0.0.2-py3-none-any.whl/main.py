"""Server module"""

import json

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_log_request_id import RequestID, current_request_id

from ramses.status_codes import HTTPStatus
from .errors.http_4xx import BadRequestError, NotFoundError, http400, http401, http403, http404
from .errors.http_5xx import InternalServerError, http500


class Server:
    """Server class"""

    def __init__(self, name, simple_logger, request_logger, config):
        """
        Constructor

        :param name: Server name
        :param simple_logger: Simple logger
        :param request_logger: Request logger (print id for every http request)
        :param config: Application configuration
        :type name: str
        :type simple_logger: logging.logger
        :type request_logger: logging.logger
        :type config: dict
        """
        self.simple_logger = simple_logger
        self.request_logger = request_logger
        self.config = config
        self._app = Flask(name)
        self._errors = []
        RequestID(self.app)

    @property
    def app(self):
        """
        Return flask app instance
        :rtype: Flask
        """
        return self._app

    @app.setter
    def app(self, value):
        """
        Set flask app instance
        :param value: Flask app instance
        :type value: Flask
        """
        self._app = value

    @property
    def errors(self):
        """
        Return app custom errors
        :rtype: list
        """
        return self._errors

    @errors.setter
    def errors(self, values):
        """
        Set app customs errors
        :param values: App custom errors
        :type values: list
        :return: None
        """
        self._errors = values

    def initialize(self, env_config=None):
        """
        Initialize ramses
        :param env_config: Running environment
        :type env_config: str
        :return: None
        """
        if env_config is not None:
            self.app.config.from_object(env_config)

        # Set cross domain
        self.set_cors()
        # bind errors
        self.load_error()
        # Prepare http request
        self.before_request()
        # Prepare http response
        self.after_request()

    def register_blueprint(self, blueprint):
        """
        Register flask blueprint
        :param blueprint: Flask blueprint
        :type blueprint: flask.Blueprint
        :return: None
        """
        self.app.register_blueprint(blueprint)

    def register_error(self, exception):
        """
        Transform custom error to json http response
        :param exception: Exception to transform
        :type exception: Exception
        :return: None
        """
        @self.app.errorhandler(exception)
        def handle_error(error):  # pylint: disable=unused-variable
            # pylint: disable=unidiomatic-typecheck
            if type(error) in self.errors:
                response = jsonify(error.to_json())
                response.status_code = error.statusCode
            else:
                response = jsonify(InternalServerError().to_json())
                response.status_code = InternalServerError.statusCode

            return response

    def set_cors(self):
        """Configure http CORS"""
        if self.config['headers'] is not None:
            CORS(self.app, resources={r'/api/*': self.config['headers']})
        else:
            CORS(self.app)

    def before_request(self):
        """
        Prepare incoming request
        :return: None
        """
        this = self

        @self.app.before_request
        def log_entry():  # pylint: disable=unused-variable
            details = {
                'details':  {
                    'host': request.remote_addr,
                    'url': request.path,
                    'method': request.method,
                    'body': request.json
                }
            }
            this.request_logger.info('Route called', extra=details)

    def after_request(self):
        """
        Prepare request response
        :return: None
        """
        @self.app.after_request
        def append_request_id(response):  # pylint: disable=unused-variable
            response.headers.add('X-REQUEST-ID', current_request_id())
            data = json.loads(response.data)
            details = {'details': data}
            self.request_logger.info('Request completed', extra=details)
            return response

    def start(self):
        """Start ramses"""
        self.app.run(host=self.config['hostname'], port=self.config['port'])

    def load_error(self):
        """Register ramses error"""
        for error in self.errors:
            self.register_error(error)
        self.register_error(BadRequestError)
        self.register_error(NotFoundError)
        self.register_error(InternalServerError)
        self.app.register_error_handler(HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR, http500)
        self.app.register_error_handler(HTTPStatus.HTTP_400_BAD_REQUEST, http400)
        self.app.register_error_handler(HTTPStatus.HTTP_401_UNAUTHORIZED, http401)
        self.app.register_error_handler(HTTPStatus.HTTP_403_FORBIDDEN, http403)
        self.app.register_error_handler(HTTPStatus.HTTP_404_NOT_FOUND, http404)
        self.register_error(Exception)
