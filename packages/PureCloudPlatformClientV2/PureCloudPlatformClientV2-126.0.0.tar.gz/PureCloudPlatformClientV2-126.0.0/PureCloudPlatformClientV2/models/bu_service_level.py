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

class BuServiceLevel(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        BuServiceLevel - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'include': 'bool',
            'percent': 'int',
            'seconds': 'int'
        }

        self.attribute_map = {
            'include': 'include',
            'percent': 'percent',
            'seconds': 'seconds'
        }

        self._include = None
        self._percent = None
        self._seconds = None

    @property
    def include(self):
        """
        Gets the include of this BuServiceLevel.
        Whether to include service level targets in the associated configuration

        :return: The include of this BuServiceLevel.
        :rtype: bool
        """
        return self._include

    @include.setter
    def include(self, include):
        """
        Sets the include of this BuServiceLevel.
        Whether to include service level targets in the associated configuration

        :param include: The include of this BuServiceLevel.
        :type: bool
        """
        
        self._include = include

    @property
    def percent(self):
        """
        Gets the percent of this BuServiceLevel.
        Service level target percent answered. Required if include == true

        :return: The percent of this BuServiceLevel.
        :rtype: int
        """
        return self._percent

    @percent.setter
    def percent(self, percent):
        """
        Sets the percent of this BuServiceLevel.
        Service level target percent answered. Required if include == true

        :param percent: The percent of this BuServiceLevel.
        :type: int
        """
        
        self._percent = percent

    @property
    def seconds(self):
        """
        Gets the seconds of this BuServiceLevel.
        Service level target answer time. Required if include == true

        :return: The seconds of this BuServiceLevel.
        :rtype: int
        """
        return self._seconds

    @seconds.setter
    def seconds(self, seconds):
        """
        Sets the seconds of this BuServiceLevel.
        Service level target answer time. Required if include == true

        :param seconds: The seconds of this BuServiceLevel.
        :type: int
        """
        
        self._seconds = seconds

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

