# coding: utf-8

"""
Copyright 2017 Square, Inc.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""


from pprint import pformat
from six import iteritems
import re


class BatchUpsertCatalogObjectsRequest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, idempotency_key=None, batches=None):
        """
        BatchUpsertCatalogObjectsRequest - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'idempotency_key': 'str',
            'batches': 'list[CatalogObjectBatch]'
        }

        self.attribute_map = {
            'idempotency_key': 'idempotency_key',
            'batches': 'batches'
        }

        self._idempotency_key = idempotency_key
        self._batches = batches

    @property
    def idempotency_key(self):
        """
        Gets the idempotency_key of this BatchUpsertCatalogObjectsRequest.
        A value you specify that uniquely identifies this request among all your requests. A common way to create a valid idempotency key is to use a Universally unique identifier (UUID).  If you're unsure whether a particular request was successful, you can reattempt it with the same idempotency key without worrying about creating duplicate objects.  See [Idempotency](/basics/api101/idempotency) for more information.

        :return: The idempotency_key of this BatchUpsertCatalogObjectsRequest.
        :rtype: str
        """
        return self._idempotency_key

    @idempotency_key.setter
    def idempotency_key(self, idempotency_key):
        """
        Sets the idempotency_key of this BatchUpsertCatalogObjectsRequest.
        A value you specify that uniquely identifies this request among all your requests. A common way to create a valid idempotency key is to use a Universally unique identifier (UUID).  If you're unsure whether a particular request was successful, you can reattempt it with the same idempotency key without worrying about creating duplicate objects.  See [Idempotency](/basics/api101/idempotency) for more information.

        :param idempotency_key: The idempotency_key of this BatchUpsertCatalogObjectsRequest.
        :type: str
        """

        if idempotency_key is None:
            raise ValueError("Invalid value for `idempotency_key`, must not be `None`")
        if len(idempotency_key) < 1:
            raise ValueError("Invalid value for `idempotency_key`, length must be greater than or equal to `1`")

        self._idempotency_key = idempotency_key

    @property
    def batches(self):
        """
        Gets the batches of this BatchUpsertCatalogObjectsRequest.
        A batch of [CatalogObject](#type-catalogobject)s to be inserted/updated atomically. The objects within a batch will be inserted in an all-or-nothing fashion, i.e., if an error occurs attempting to insert or update an object within a batch, the entire batch will be rejected. However, an error in one batch will not affect other batches within the same request.  For each object, its `updated_at` field is ignored and replaced with a current [timestamp](#workingwithdates), and its `is_deleted` field must not be set to `true`.  To modify an existing object, supply its ID. To create a new object, use an ID starting with `#`. These IDs may be used to create relationships between an object and attributes of other objects that reference it. For example, you can create a [CatalogItem](#type-catalogitem) with ID `#ABC` and a [CatalogItemVariation](#type-catalogitemvariation) with its `item_id` attribute set to `#ABC` in order to associate the [CatalogItemVariation](#type-catalogitemvariation) with its parent [CatalogItem](#type-catalogitem).  Any `#`-prefixed IDs are valid only within a single atomic batch, and will be replaced by server-generated IDs.  Each batch may contain up to 1,000 objects. The total number of objects across all batches for a single request may not exceed 10,000. If either of these limits is violated, an error will be returned and no objects will be inserted or updated.

        :return: The batches of this BatchUpsertCatalogObjectsRequest.
        :rtype: list[CatalogObjectBatch]
        """
        return self._batches

    @batches.setter
    def batches(self, batches):
        """
        Sets the batches of this BatchUpsertCatalogObjectsRequest.
        A batch of [CatalogObject](#type-catalogobject)s to be inserted/updated atomically. The objects within a batch will be inserted in an all-or-nothing fashion, i.e., if an error occurs attempting to insert or update an object within a batch, the entire batch will be rejected. However, an error in one batch will not affect other batches within the same request.  For each object, its `updated_at` field is ignored and replaced with a current [timestamp](#workingwithdates), and its `is_deleted` field must not be set to `true`.  To modify an existing object, supply its ID. To create a new object, use an ID starting with `#`. These IDs may be used to create relationships between an object and attributes of other objects that reference it. For example, you can create a [CatalogItem](#type-catalogitem) with ID `#ABC` and a [CatalogItemVariation](#type-catalogitemvariation) with its `item_id` attribute set to `#ABC` in order to associate the [CatalogItemVariation](#type-catalogitemvariation) with its parent [CatalogItem](#type-catalogitem).  Any `#`-prefixed IDs are valid only within a single atomic batch, and will be replaced by server-generated IDs.  Each batch may contain up to 1,000 objects. The total number of objects across all batches for a single request may not exceed 10,000. If either of these limits is violated, an error will be returned and no objects will be inserted or updated.

        :param batches: The batches of this BatchUpsertCatalogObjectsRequest.
        :type: list[CatalogObjectBatch]
        """

        self._batches = batches

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
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
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
