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

class ConversationBasic(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ConversationBasic - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'external_tag': 'str',
            'start_time': 'datetime',
            'end_time': 'datetime',
            'divisions': 'list[ConversationDivisionMembership]',
            'self_uri': 'str',
            'participants': 'list[ParticipantBasic]'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'external_tag': 'externalTag',
            'start_time': 'startTime',
            'end_time': 'endTime',
            'divisions': 'divisions',
            'self_uri': 'selfUri',
            'participants': 'participants'
        }

        self._id = None
        self._name = None
        self._external_tag = None
        self._start_time = None
        self._end_time = None
        self._divisions = None
        self._self_uri = None
        self._participants = None

    @property
    def id(self):
        """
        Gets the id of this ConversationBasic.
        The globally unique identifier for the object.

        :return: The id of this ConversationBasic.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ConversationBasic.
        The globally unique identifier for the object.

        :param id: The id of this ConversationBasic.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this ConversationBasic.


        :return: The name of this ConversationBasic.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ConversationBasic.


        :param name: The name of this ConversationBasic.
        :type: str
        """
        
        self._name = name

    @property
    def external_tag(self):
        """
        Gets the external_tag of this ConversationBasic.
        The external tag associated with the conversation.

        :return: The external_tag of this ConversationBasic.
        :rtype: str
        """
        return self._external_tag

    @external_tag.setter
    def external_tag(self, external_tag):
        """
        Sets the external_tag of this ConversationBasic.
        The external tag associated with the conversation.

        :param external_tag: The external_tag of this ConversationBasic.
        :type: str
        """
        
        self._external_tag = external_tag

    @property
    def start_time(self):
        """
        Gets the start_time of this ConversationBasic.
        The time when the conversation started. This will be the time when the first participant joined the conversation. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The start_time of this ConversationBasic.
        :rtype: datetime
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """
        Sets the start_time of this ConversationBasic.
        The time when the conversation started. This will be the time when the first participant joined the conversation. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param start_time: The start_time of this ConversationBasic.
        :type: datetime
        """
        
        self._start_time = start_time

    @property
    def end_time(self):
        """
        Gets the end_time of this ConversationBasic.
        The time when the conversation ended. This will be the time when the last participant left the conversation, or null when the conversation is still active. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The end_time of this ConversationBasic.
        :rtype: datetime
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """
        Sets the end_time of this ConversationBasic.
        The time when the conversation ended. This will be the time when the last participant left the conversation, or null when the conversation is still active. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param end_time: The end_time of this ConversationBasic.
        :type: datetime
        """
        
        self._end_time = end_time

    @property
    def divisions(self):
        """
        Gets the divisions of this ConversationBasic.
        Identifiers of divisions associated with this conversation

        :return: The divisions of this ConversationBasic.
        :rtype: list[ConversationDivisionMembership]
        """
        return self._divisions

    @divisions.setter
    def divisions(self, divisions):
        """
        Sets the divisions of this ConversationBasic.
        Identifiers of divisions associated with this conversation

        :param divisions: The divisions of this ConversationBasic.
        :type: list[ConversationDivisionMembership]
        """
        
        self._divisions = divisions

    @property
    def self_uri(self):
        """
        Gets the self_uri of this ConversationBasic.
        The URI for this object

        :return: The self_uri of this ConversationBasic.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this ConversationBasic.
        The URI for this object

        :param self_uri: The self_uri of this ConversationBasic.
        :type: str
        """
        
        self._self_uri = self_uri

    @property
    def participants(self):
        """
        Gets the participants of this ConversationBasic.


        :return: The participants of this ConversationBasic.
        :rtype: list[ParticipantBasic]
        """
        return self._participants

    @participants.setter
    def participants(self, participants):
        """
        Sets the participants of this ConversationBasic.


        :param participants: The participants of this ConversationBasic.
        :type: list[ParticipantBasic]
        """
        
        self._participants = participants

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

