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

class SystemMessageSystemMessage(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        SystemMessageSystemMessage - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'channel_id': 'str',
            'system_topic_type': 'str',
            'correlation_id': 'str',
            'organization_id': 'str',
            'user_id': 'str',
            'oauth_client_id': 'str',
            'reason': 'str',
            'message': 'str',
            'data': 'object'
        }

        self.attribute_map = {
            'channel_id': 'channelId',
            'system_topic_type': 'systemTopicType',
            'correlation_id': 'correlationId',
            'organization_id': 'organizationId',
            'user_id': 'userId',
            'oauth_client_id': 'oauthClientId',
            'reason': 'reason',
            'message': 'message',
            'data': 'data'
        }

        self._channel_id = None
        self._system_topic_type = None
        self._correlation_id = None
        self._organization_id = None
        self._user_id = None
        self._oauth_client_id = None
        self._reason = None
        self._message = None
        self._data = None

    @property
    def channel_id(self):
        """
        Gets the channel_id of this SystemMessageSystemMessage.


        :return: The channel_id of this SystemMessageSystemMessage.
        :rtype: str
        """
        return self._channel_id

    @channel_id.setter
    def channel_id(self, channel_id):
        """
        Sets the channel_id of this SystemMessageSystemMessage.


        :param channel_id: The channel_id of this SystemMessageSystemMessage.
        :type: str
        """
        
        self._channel_id = channel_id

    @property
    def system_topic_type(self):
        """
        Gets the system_topic_type of this SystemMessageSystemMessage.


        :return: The system_topic_type of this SystemMessageSystemMessage.
        :rtype: str
        """
        return self._system_topic_type

    @system_topic_type.setter
    def system_topic_type(self, system_topic_type):
        """
        Sets the system_topic_type of this SystemMessageSystemMessage.


        :param system_topic_type: The system_topic_type of this SystemMessageSystemMessage.
        :type: str
        """
        allowed_values = ["no_longer_subscribed", "subscription_changed", "token_revoked"]
        if system_topic_type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for system_topic_type -> " + system_topic_type)
            self._system_topic_type = "outdated_sdk_version"
        else:
            self._system_topic_type = system_topic_type

    @property
    def correlation_id(self):
        """
        Gets the correlation_id of this SystemMessageSystemMessage.


        :return: The correlation_id of this SystemMessageSystemMessage.
        :rtype: str
        """
        return self._correlation_id

    @correlation_id.setter
    def correlation_id(self, correlation_id):
        """
        Sets the correlation_id of this SystemMessageSystemMessage.


        :param correlation_id: The correlation_id of this SystemMessageSystemMessage.
        :type: str
        """
        
        self._correlation_id = correlation_id

    @property
    def organization_id(self):
        """
        Gets the organization_id of this SystemMessageSystemMessage.


        :return: The organization_id of this SystemMessageSystemMessage.
        :rtype: str
        """
        return self._organization_id

    @organization_id.setter
    def organization_id(self, organization_id):
        """
        Sets the organization_id of this SystemMessageSystemMessage.


        :param organization_id: The organization_id of this SystemMessageSystemMessage.
        :type: str
        """
        
        self._organization_id = organization_id

    @property
    def user_id(self):
        """
        Gets the user_id of this SystemMessageSystemMessage.


        :return: The user_id of this SystemMessageSystemMessage.
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """
        Sets the user_id of this SystemMessageSystemMessage.


        :param user_id: The user_id of this SystemMessageSystemMessage.
        :type: str
        """
        
        self._user_id = user_id

    @property
    def oauth_client_id(self):
        """
        Gets the oauth_client_id of this SystemMessageSystemMessage.


        :return: The oauth_client_id of this SystemMessageSystemMessage.
        :rtype: str
        """
        return self._oauth_client_id

    @oauth_client_id.setter
    def oauth_client_id(self, oauth_client_id):
        """
        Sets the oauth_client_id of this SystemMessageSystemMessage.


        :param oauth_client_id: The oauth_client_id of this SystemMessageSystemMessage.
        :type: str
        """
        
        self._oauth_client_id = oauth_client_id

    @property
    def reason(self):
        """
        Gets the reason of this SystemMessageSystemMessage.


        :return: The reason of this SystemMessageSystemMessage.
        :rtype: str
        """
        return self._reason

    @reason.setter
    def reason(self, reason):
        """
        Sets the reason of this SystemMessageSystemMessage.


        :param reason: The reason of this SystemMessageSystemMessage.
        :type: str
        """
        allowed_values = ["another_channel_subscribed", "user_tokens_revoked"]
        if reason.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for reason -> " + reason)
            self._reason = "outdated_sdk_version"
        else:
            self._reason = reason

    @property
    def message(self):
        """
        Gets the message of this SystemMessageSystemMessage.


        :return: The message of this SystemMessageSystemMessage.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """
        Sets the message of this SystemMessageSystemMessage.


        :param message: The message of this SystemMessageSystemMessage.
        :type: str
        """
        
        self._message = message

    @property
    def data(self):
        """
        Gets the data of this SystemMessageSystemMessage.


        :return: The data of this SystemMessageSystemMessage.
        :rtype: object
        """
        return self._data

    @data.setter
    def data(self, data):
        """
        Sets the data of this SystemMessageSystemMessage.


        :param data: The data of this SystemMessageSystemMessage.
        :type: object
        """
        
        self._data = data

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

