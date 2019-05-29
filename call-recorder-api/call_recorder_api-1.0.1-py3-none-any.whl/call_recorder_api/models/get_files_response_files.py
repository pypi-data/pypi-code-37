# coding: utf-8

"""
    Call Recorder API

    Call Recorder API   # noqa: E501

    OpenAPI spec version: 1.0.0
    
"""

import pprint
import re  # noqa: F401

import six


class GetFilesResponseFiles(object):
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
        'id': 'int',
        'access_number': 'str',
        'name': 'str',
        'f_name': 'str',
        'l_name': 'str',
        'email': 'str',
        'phone': 'str',
        'notes': 'str',
        'meta': 'str',
        'source': 'str',
        'url': 'str',
        'credits': 'str',
        'duration': 'str',
        'time': 'str',
        'share_url': 'str',
        'download_url': 'str'
    }

    attribute_map = {
        'id': 'id',
        'access_number': 'access_number',
        'name': 'name',
        'f_name': 'f_name',
        'l_name': 'l_name',
        'email': 'email',
        'phone': 'phone',
        'notes': 'notes',
        'meta': 'meta',
        'source': 'source',
        'url': 'url',
        'credits': 'credits',
        'duration': 'duration',
        'time': 'time',
        'share_url': 'share_url',
        'download_url': 'download_url'
    }

    def __init__(self, id=None, access_number=None, name=None, f_name=None, l_name=None, email=None, phone=None, notes=None, meta=None, source=None, url=None, credits=None, duration=None, time=None, share_url=None, download_url=None):  # noqa: E501
        """GetFilesResponseFiles - a model defined in spec"""  # noqa: E501
        self._id = None
        self._access_number = None
        self._name = None
        self._f_name = None
        self._l_name = None
        self._email = None
        self._phone = None
        self._notes = None
        self._meta = None
        self._source = None
        self._url = None
        self._credits = None
        self._duration = None
        self._time = None
        self._share_url = None
        self._download_url = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if access_number is not None:
            self.access_number = access_number
        if name is not None:
            self.name = name
        if f_name is not None:
            self.f_name = f_name
        if l_name is not None:
            self.l_name = l_name
        if email is not None:
            self.email = email
        if phone is not None:
            self.phone = phone
        if notes is not None:
            self.notes = notes
        if meta is not None:
            self.meta = meta
        if source is not None:
            self.source = source
        if url is not None:
            self.url = url
        if credits is not None:
            self.credits = credits
        if duration is not None:
            self.duration = duration
        if time is not None:
            self.time = time
        if share_url is not None:
            self.share_url = share_url
        if download_url is not None:
            self.download_url = download_url

    @property
    def id(self):
        """Gets the id of this GetFilesResponseFiles.  # noqa: E501


        :return: The id of this GetFilesResponseFiles.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this GetFilesResponseFiles.


        :param id: The id of this GetFilesResponseFiles.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def access_number(self):
        """Gets the access_number of this GetFilesResponseFiles.  # noqa: E501


        :return: The access_number of this GetFilesResponseFiles.  # noqa: E501
        :rtype: str
        """
        return self._access_number

    @access_number.setter
    def access_number(self, access_number):
        """Sets the access_number of this GetFilesResponseFiles.


        :param access_number: The access_number of this GetFilesResponseFiles.  # noqa: E501
        :type: str
        """

        self._access_number = access_number

    @property
    def name(self):
        """Gets the name of this GetFilesResponseFiles.  # noqa: E501


        :return: The name of this GetFilesResponseFiles.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this GetFilesResponseFiles.


        :param name: The name of this GetFilesResponseFiles.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def f_name(self):
        """Gets the f_name of this GetFilesResponseFiles.  # noqa: E501


        :return: The f_name of this GetFilesResponseFiles.  # noqa: E501
        :rtype: str
        """
        return self._f_name

    @f_name.setter
    def f_name(self, f_name):
        """Sets the f_name of this GetFilesResponseFiles.


        :param f_name: The f_name of this GetFilesResponseFiles.  # noqa: E501
        :type: str
        """

        self._f_name = f_name

    @property
    def l_name(self):
        """Gets the l_name of this GetFilesResponseFiles.  # noqa: E501


        :return: The l_name of this GetFilesResponseFiles.  # noqa: E501
        :rtype: str
        """
        return self._l_name

    @l_name.setter
    def l_name(self, l_name):
        """Sets the l_name of this GetFilesResponseFiles.


        :param l_name: The l_name of this GetFilesResponseFiles.  # noqa: E501
        :type: str
        """

        self._l_name = l_name

    @property
    def email(self):
        """Gets the email of this GetFilesResponseFiles.  # noqa: E501


        :return: The email of this GetFilesResponseFiles.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this GetFilesResponseFiles.


        :param email: The email of this GetFilesResponseFiles.  # noqa: E501
        :type: str
        """

        self._email = email

    @property
    def phone(self):
        """Gets the phone of this GetFilesResponseFiles.  # noqa: E501


        :return: The phone of this GetFilesResponseFiles.  # noqa: E501
        :rtype: str
        """
        return self._phone

    @phone.setter
    def phone(self, phone):
        """Sets the phone of this GetFilesResponseFiles.


        :param phone: The phone of this GetFilesResponseFiles.  # noqa: E501
        :type: str
        """

        self._phone = phone

    @property
    def notes(self):
        """Gets the notes of this GetFilesResponseFiles.  # noqa: E501


        :return: The notes of this GetFilesResponseFiles.  # noqa: E501
        :rtype: str
        """
        return self._notes

    @notes.setter
    def notes(self, notes):
        """Sets the notes of this GetFilesResponseFiles.


        :param notes: The notes of this GetFilesResponseFiles.  # noqa: E501
        :type: str
        """

        self._notes = notes

    @property
    def meta(self):
        """Gets the meta of this GetFilesResponseFiles.  # noqa: E501


        :return: The meta of this GetFilesResponseFiles.  # noqa: E501
        :rtype: str
        """
        return self._meta

    @meta.setter
    def meta(self, meta):
        """Sets the meta of this GetFilesResponseFiles.


        :param meta: The meta of this GetFilesResponseFiles.  # noqa: E501
        :type: str
        """

        self._meta = meta

    @property
    def source(self):
        """Gets the source of this GetFilesResponseFiles.  # noqa: E501


        :return: The source of this GetFilesResponseFiles.  # noqa: E501
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this GetFilesResponseFiles.


        :param source: The source of this GetFilesResponseFiles.  # noqa: E501
        :type: str
        """

        self._source = source

    @property
    def url(self):
        """Gets the url of this GetFilesResponseFiles.  # noqa: E501


        :return: The url of this GetFilesResponseFiles.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this GetFilesResponseFiles.


        :param url: The url of this GetFilesResponseFiles.  # noqa: E501
        :type: str
        """

        self._url = url

    @property
    def credits(self):
        """Gets the credits of this GetFilesResponseFiles.  # noqa: E501


        :return: The credits of this GetFilesResponseFiles.  # noqa: E501
        :rtype: str
        """
        return self._credits

    @credits.setter
    def credits(self, credits):
        """Sets the credits of this GetFilesResponseFiles.


        :param credits: The credits of this GetFilesResponseFiles.  # noqa: E501
        :type: str
        """

        self._credits = credits

    @property
    def duration(self):
        """Gets the duration of this GetFilesResponseFiles.  # noqa: E501


        :return: The duration of this GetFilesResponseFiles.  # noqa: E501
        :rtype: str
        """
        return self._duration

    @duration.setter
    def duration(self, duration):
        """Sets the duration of this GetFilesResponseFiles.


        :param duration: The duration of this GetFilesResponseFiles.  # noqa: E501
        :type: str
        """

        self._duration = duration

    @property
    def time(self):
        """Gets the time of this GetFilesResponseFiles.  # noqa: E501


        :return: The time of this GetFilesResponseFiles.  # noqa: E501
        :rtype: str
        """
        return self._time

    @time.setter
    def time(self, time):
        """Sets the time of this GetFilesResponseFiles.


        :param time: The time of this GetFilesResponseFiles.  # noqa: E501
        :type: str
        """

        self._time = time

    @property
    def share_url(self):
        """Gets the share_url of this GetFilesResponseFiles.  # noqa: E501


        :return: The share_url of this GetFilesResponseFiles.  # noqa: E501
        :rtype: str
        """
        return self._share_url

    @share_url.setter
    def share_url(self, share_url):
        """Sets the share_url of this GetFilesResponseFiles.


        :param share_url: The share_url of this GetFilesResponseFiles.  # noqa: E501
        :type: str
        """

        self._share_url = share_url

    @property
    def download_url(self):
        """Gets the download_url of this GetFilesResponseFiles.  # noqa: E501


        :return: The download_url of this GetFilesResponseFiles.  # noqa: E501
        :rtype: str
        """
        return self._download_url

    @download_url.setter
    def download_url(self, download_url):
        """Sets the download_url of this GetFilesResponseFiles.


        :param download_url: The download_url of this GetFilesResponseFiles.  # noqa: E501
        :type: str
        """

        self._download_url = download_url

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
        if issubclass(GetFilesResponseFiles, dict):
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
        if not isinstance(other, GetFilesResponseFiles):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
