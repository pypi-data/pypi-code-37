# coding: utf-8

"""
    Call Recorder API

    Call Recorder API   # noqa: E501

    OpenAPI spec version: 1.0.0
    
"""

import pprint
import re  # noqa: F401

import six


class GetFilesRequest(object):
    """NOTE: 

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'api_key': 'str',
        'page': 'str',
        'folder_id': 'int',
        'source': 'str',
        '_pass': 'str',
        'reminder': 'bool',
        'q': 'str',
        'id': 'int',
        'op': 'str'
    }

    attribute_map = {
        'api_key': 'api_key',
        'page': 'page',
        'folder_id': 'folder_id',
        'source': 'source',
        '_pass': 'pass',
        'reminder': 'reminder',
        'q': 'q',
        'id': 'id',
        'op': 'op'
    }

    def __init__(self, api_key=None, page=None, folder_id=None, source=None, _pass=None, reminder=None, q=None, id=None, op=None):  # noqa: E501
        """GetFilesRequest - a model defined in spec"""  # noqa: E501
        self._api_key = None
        self._page = None
        self._folder_id = None
        self._source = None
        self.__pass = None
        self._reminder = None
        self._q = None
        self._id = None
        self._op = None
        self.discriminator = None
        self.api_key = api_key
        if page is not None:
            self.page = page
        if folder_id is not None:
            self.folder_id = folder_id
        if source is not None:
            self.source = source
        if _pass is not None:
            self._pass = _pass
        if reminder is not None:
            self.reminder = reminder
        if q is not None:
            self.q = q
        if id is not None:
            self.id = id
        if op is not None:
            self.op = op

    @property
    def api_key(self):
        """Gets the api_key of this GetFilesRequest.  # noqa: E501


        :return: The api_key of this GetFilesRequest.  # noqa: E501
        :rtype: str
        """
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        """Sets the api_key of this GetFilesRequest.


        :param api_key: The api_key of this GetFilesRequest.  # noqa: E501
        :type: str
        """
        if api_key is None:
            raise ValueError("Invalid value for `api_key`, must not be `None`")  # noqa: E501

        self._api_key = api_key

    @property
    def page(self):
        """Gets the page of this GetFilesRequest.  # noqa: E501


        :return: The page of this GetFilesRequest.  # noqa: E501
        :rtype: str
        """
        return self._page

    @page.setter
    def page(self, page):
        """Sets the page of this GetFilesRequest.


        :param page: The page of this GetFilesRequest.  # noqa: E501
        :type: str
        """

        self._page = page

    @property
    def folder_id(self):
        """Gets the folder_id of this GetFilesRequest.  # noqa: E501


        :return: The folder_id of this GetFilesRequest.  # noqa: E501
        :rtype: int
        """
        return self._folder_id

    @folder_id.setter
    def folder_id(self, folder_id):
        """Sets the folder_id of this GetFilesRequest.


        :param folder_id: The folder_id of this GetFilesRequest.  # noqa: E501
        :type: int
        """

        self._folder_id = folder_id

    @property
    def source(self):
        """Gets the source of this GetFilesRequest.  # noqa: E501


        :return: The source of this GetFilesRequest.  # noqa: E501
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this GetFilesRequest.


        :param source: The source of this GetFilesRequest.  # noqa: E501
        :type: str
        """
        allowed_values = ["all", "app2"]  # noqa: E501
        if source not in allowed_values:
            raise ValueError(
                "Invalid value for `source` ({0}), must be one of {1}"  # noqa: E501
                .format(source, allowed_values)
            )

        self._source = source

    @property
    def _pass(self):
        """Gets the _pass of this GetFilesRequest.  # noqa: E501


        :return: The _pass of this GetFilesRequest.  # noqa: E501
        :rtype: str
        """
        return self.__pass

    @_pass.setter
    def _pass(self, _pass):
        """Sets the _pass of this GetFilesRequest.


        :param _pass: The _pass of this GetFilesRequest.  # noqa: E501
        :type: str
        """

        self.__pass = _pass

    @property
    def reminder(self):
        """Gets the reminder of this GetFilesRequest.  # noqa: E501


        :return: The reminder of this GetFilesRequest.  # noqa: E501
        :rtype: bool
        """
        return self._reminder

    @reminder.setter
    def reminder(self, reminder):
        """Sets the reminder of this GetFilesRequest.


        :param reminder: The reminder of this GetFilesRequest.  # noqa: E501
        :type: bool
        """

        self._reminder = reminder

    @property
    def q(self):
        """Gets the q of this GetFilesRequest.  # noqa: E501


        :return: The q of this GetFilesRequest.  # noqa: E501
        :rtype: str
        """
        return self._q

    @q.setter
    def q(self, q):
        """Sets the q of this GetFilesRequest.


        :param q: The q of this GetFilesRequest.  # noqa: E501
        :type: str
        """

        self._q = q

    @property
    def id(self):
        """Gets the id of this GetFilesRequest.  # noqa: E501


        :return: The id of this GetFilesRequest.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this GetFilesRequest.


        :param id: The id of this GetFilesRequest.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def op(self):
        """Gets the op of this GetFilesRequest.  # noqa: E501


        :return: The op of this GetFilesRequest.  # noqa: E501
        :rtype: str
        """
        return self._op

    @op.setter
    def op(self, op):
        """Sets the op of this GetFilesRequest.


        :param op: The op of this GetFilesRequest.  # noqa: E501
        :type: str
        """
        allowed_values = ["less", "greater"]  # noqa: E501
        if op not in allowed_values:
            raise ValueError(
                "Invalid value for `op` ({0}), must be one of {1}"  # noqa: E501
                .format(op, allowed_values)
            )

        self._op = op

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(GetFilesRequest, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, GetFilesRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
