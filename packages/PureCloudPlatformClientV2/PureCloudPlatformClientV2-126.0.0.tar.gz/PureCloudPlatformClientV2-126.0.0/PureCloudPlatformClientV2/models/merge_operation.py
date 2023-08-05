# coding: utf-8

"""
Copyright 2016 SmartBear Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Ref: https://github.com/swagger-api/swagger-codegen
"""

from pprint import pformat
from six import iteritems
import re
import json

from ..utils import sanitize_for_serialization

class MergeOperation(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        MergeOperation - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'source_contact': 'AddressableEntityRef',
            'target_contact': 'AddressableEntityRef',
            'resulting_contact': 'AddressableEntityRef'
        }

        self.attribute_map = {
            'source_contact': 'sourceContact',
            'target_contact': 'targetContact',
            'resulting_contact': 'resultingContact'
        }

        self._source_contact = None
        self._target_contact = None
        self._resulting_contact = None

    @property
    def source_contact(self):
        """
        Gets the source_contact of this MergeOperation.
        The source contact for the merge operation

        :return: The source_contact of this MergeOperation.
        :rtype: AddressableEntityRef
        """
        return self._source_contact

    @source_contact.setter
    def source_contact(self, source_contact):
        """
        Sets the source_contact of this MergeOperation.
        The source contact for the merge operation

        :param source_contact: The source_contact of this MergeOperation.
        :type: AddressableEntityRef
        """
        
        self._source_contact = source_contact

    @property
    def target_contact(self):
        """
        Gets the target_contact of this MergeOperation.
        The target contact for the merge operation

        :return: The target_contact of this MergeOperation.
        :rtype: AddressableEntityRef
        """
        return self._target_contact

    @target_contact.setter
    def target_contact(self, target_contact):
        """
        Sets the target_contact of this MergeOperation.
        The target contact for the merge operation

        :param target_contact: The target_contact of this MergeOperation.
        :type: AddressableEntityRef
        """
        
        self._target_contact = target_contact

    @property
    def resulting_contact(self):
        """
        Gets the resulting_contact of this MergeOperation.
        The contact created as a result of the merge operation

        :return: The resulting_contact of this MergeOperation.
        :rtype: AddressableEntityRef
        """
        return self._resulting_contact

    @resulting_contact.setter
    def resulting_contact(self, resulting_contact):
        """
        Sets the resulting_contact of this MergeOperation.
        The contact created as a result of the merge operation

        :param resulting_contact: The resulting_contact of this MergeOperation.
        :type: AddressableEntityRef
        """
        
        self._resulting_contact = resulting_contact

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

    def to_json(self):
        """
        Returns the model as raw JSON
        """
        return json.dumps(sanitize_for_serialization(self.to_dict()))

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

