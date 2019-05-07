# coding: utf-8

"""
    Flywheel

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 8.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


## NOTE: This file is auto generated by the swagger code generator program.
## Do not edit the file manually.

import pprint
import re  # noqa: F401

import six

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.


class ConfigSiteConfigOutput(object):

    swagger_types = {
        'central_url': 'str',
        'ssl_cert': 'str',
        'api_url': 'str',
        'registered': 'bool',
        'id': 'str',
        'name': 'str'
    }

    attribute_map = {
        'central_url': 'central_url',
        'ssl_cert': 'ssl_cert',
        'api_url': 'api_url',
        'registered': 'registered',
        'id': 'id',
        'name': 'name'
    }

    rattribute_map = {
        'central_url': 'central_url',
        'ssl_cert': 'ssl_cert',
        'api_url': 'api_url',
        'registered': 'registered',
        'id': 'id',
        'name': 'name'
    }

    def __init__(self, central_url=None, ssl_cert=None, api_url=None, registered=None, id=None, name=None):  # noqa: E501
        """ConfigSiteConfigOutput - a model defined in Swagger"""
        super(ConfigSiteConfigOutput, self).__init__()

        self._central_url = None
        self._ssl_cert = None
        self._api_url = None
        self._registered = None
        self._id = None
        self._name = None
        self.discriminator = None
        self.alt_discriminator = None

        self.central_url = central_url
        if ssl_cert is not None:
            self.ssl_cert = ssl_cert
        self.api_url = api_url
        self.registered = registered
        self.id = id
        self.name = name

    @property
    def central_url(self):
        """Gets the central_url of this ConfigSiteConfigOutput.


        :return: The central_url of this ConfigSiteConfigOutput.
        :rtype: str
        """
        return self._central_url

    @central_url.setter
    def central_url(self, central_url):
        """Sets the central_url of this ConfigSiteConfigOutput.


        :param central_url: The central_url of this ConfigSiteConfigOutput.  # noqa: E501
        :type: str
        """

        self._central_url = central_url

    @property
    def ssl_cert(self):
        """Gets the ssl_cert of this ConfigSiteConfigOutput.


        :return: The ssl_cert of this ConfigSiteConfigOutput.
        :rtype: str
        """
        return self._ssl_cert

    @ssl_cert.setter
    def ssl_cert(self, ssl_cert):
        """Sets the ssl_cert of this ConfigSiteConfigOutput.


        :param ssl_cert: The ssl_cert of this ConfigSiteConfigOutput.  # noqa: E501
        :type: str
        """

        self._ssl_cert = ssl_cert

    @property
    def api_url(self):
        """Gets the api_url of this ConfigSiteConfigOutput.


        :return: The api_url of this ConfigSiteConfigOutput.
        :rtype: str
        """
        return self._api_url

    @api_url.setter
    def api_url(self, api_url):
        """Sets the api_url of this ConfigSiteConfigOutput.


        :param api_url: The api_url of this ConfigSiteConfigOutput.  # noqa: E501
        :type: str
        """

        self._api_url = api_url

    @property
    def registered(self):
        """Gets the registered of this ConfigSiteConfigOutput.


        :return: The registered of this ConfigSiteConfigOutput.
        :rtype: bool
        """
        return self._registered

    @registered.setter
    def registered(self, registered):
        """Sets the registered of this ConfigSiteConfigOutput.


        :param registered: The registered of this ConfigSiteConfigOutput.  # noqa: E501
        :type: bool
        """

        self._registered = registered

    @property
    def id(self):
        """Gets the id of this ConfigSiteConfigOutput.


        :return: The id of this ConfigSiteConfigOutput.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ConfigSiteConfigOutput.


        :param id: The id of this ConfigSiteConfigOutput.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this ConfigSiteConfigOutput.


        :return: The name of this ConfigSiteConfigOutput.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ConfigSiteConfigOutput.


        :param name: The name of this ConfigSiteConfigOutput.  # noqa: E501
        :type: str
        """

        self._name = name


    @staticmethod
    def positional_to_model(value):
        """Converts a positional argument to a model value"""
        return value

    def return_value(self):
        """Unwraps return value from model"""
        return self

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

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ConfigSiteConfigOutput):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

    # Container emulation
    def __getitem__(self, key):
        """Returns the value of key"""
        key = self._map_key(key)
        return getattr(self, key)

    def __setitem__(self, key, value):
        """Sets the value of key"""
        key = self._map_key(key)
        setattr(self, key, value)

    def __contains__(self, key):
        """Checks if the given value is a key in this object"""
        key = self._map_key(key, raise_on_error=False)
        return key is not None

    def keys(self):
        """Returns the list of json properties in the object"""
        return self.__class__.rattribute_map.keys()

    def values(self):
        """Returns the list of values in the object"""
        for key in self.__class__.attribute_map.keys():
            yield getattr(self, key)

    def items(self):
        """Returns the list of json property to value mapping"""
        for key, prop in self.__class__.rattribute_map.items():
            yield key, getattr(self, prop)

    def get(self, key, default=None):
        """Get the value of the provided json property, or default"""
        key = self._map_key(key, raise_on_error=False)
        if key:
            return getattr(self, key, default)
        return default

    def _map_key(self, key, raise_on_error=True):
        result = self.__class__.rattribute_map.get(key)
        if result is None:
            if raise_on_error:
                raise AttributeError('Invalid attribute name: {}'.format(key))
            return None
        return '_' + result
