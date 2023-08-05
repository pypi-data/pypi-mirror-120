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

class RoutingConversationAttributesResponse(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        RoutingConversationAttributesResponse - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'priority': 'int',
            'skills': 'list[RoutingSkill]',
            'language': 'Language'
        }

        self.attribute_map = {
            'priority': 'priority',
            'skills': 'skills',
            'language': 'language'
        }

        self._priority = None
        self._skills = None
        self._language = None

    @property
    def priority(self):
        """
        Gets the priority of this RoutingConversationAttributesResponse.
        Current priority value on in-queue conversation. Range:[-25000000, 25000000]

        :return: The priority of this RoutingConversationAttributesResponse.
        :rtype: int
        """
        return self._priority

    @priority.setter
    def priority(self, priority):
        """
        Sets the priority of this RoutingConversationAttributesResponse.
        Current priority value on in-queue conversation. Range:[-25000000, 25000000]

        :param priority: The priority of this RoutingConversationAttributesResponse.
        :type: int
        """
        
        self._priority = priority

    @property
    def skills(self):
        """
        Gets the skills of this RoutingConversationAttributesResponse.
        Current routing skills on in-queue conversation

        :return: The skills of this RoutingConversationAttributesResponse.
        :rtype: list[RoutingSkill]
        """
        return self._skills

    @skills.setter
    def skills(self, skills):
        """
        Sets the skills of this RoutingConversationAttributesResponse.
        Current routing skills on in-queue conversation

        :param skills: The skills of this RoutingConversationAttributesResponse.
        :type: list[RoutingSkill]
        """
        
        self._skills = skills

    @property
    def language(self):
        """
        Gets the language of this RoutingConversationAttributesResponse.
        Current language on in-queue conversation

        :return: The language of this RoutingConversationAttributesResponse.
        :rtype: Language
        """
        return self._language

    @language.setter
    def language(self, language):
        """
        Sets the language of this RoutingConversationAttributesResponse.
        Current language on in-queue conversation

        :param language: The language of this RoutingConversationAttributesResponse.
        :type: Language
        """
        
        self._language = language

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

