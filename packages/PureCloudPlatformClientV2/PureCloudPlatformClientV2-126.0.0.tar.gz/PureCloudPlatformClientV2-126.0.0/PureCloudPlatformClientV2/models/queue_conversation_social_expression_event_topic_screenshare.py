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

class QueueConversationSocialExpressionEventTopicScreenshare(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        QueueConversationSocialExpressionEventTopicScreenshare - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'state': 'str',
            'pcSelf': 'QueueConversationSocialExpressionEventTopicAddress',
            'id': 'str',
            'context': 'str',
            'sharing': 'bool',
            'provider': 'str',
            'script_id': 'str',
            'peer_id': 'str',
            'disconnect_type': 'str',
            'connected_time': 'datetime',
            'disconnected_time': 'datetime',
            'wrapup': 'QueueConversationSocialExpressionEventTopicWrapup',
            'after_call_work': 'QueueConversationSocialExpressionEventTopicAfterCallWork',
            'after_call_work_required': 'bool',
            'additional_properties': 'object'
        }

        self.attribute_map = {
            'state': 'state',
            'pcSelf': 'self',
            'id': 'id',
            'context': 'context',
            'sharing': 'sharing',
            'provider': 'provider',
            'script_id': 'scriptId',
            'peer_id': 'peerId',
            'disconnect_type': 'disconnectType',
            'connected_time': 'connectedTime',
            'disconnected_time': 'disconnectedTime',
            'wrapup': 'wrapup',
            'after_call_work': 'afterCallWork',
            'after_call_work_required': 'afterCallWorkRequired',
            'additional_properties': 'additionalProperties'
        }

        self._state = None
        self._pcSelf = None
        self._id = None
        self._context = None
        self._sharing = None
        self._provider = None
        self._script_id = None
        self._peer_id = None
        self._disconnect_type = None
        self._connected_time = None
        self._disconnected_time = None
        self._wrapup = None
        self._after_call_work = None
        self._after_call_work_required = None
        self._additional_properties = None

    @property
    def state(self):
        """
        Gets the state of this QueueConversationSocialExpressionEventTopicScreenshare.


        :return: The state of this QueueConversationSocialExpressionEventTopicScreenshare.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this QueueConversationSocialExpressionEventTopicScreenshare.


        :param state: The state of this QueueConversationSocialExpressionEventTopicScreenshare.
        :type: str
        """
        allowed_values = ["ALERTING", "DIALING", "CONTACTING", "OFFERING", "CONNECTED", "DISCONNECTED", "TERMINATED", "NONE"]
        if state.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for state -> " + state)
            self._state = "outdated_sdk_version"
        else:
            self._state = state

    @property
    def pcSelf(self):
        """
        Gets the pcSelf of this QueueConversationSocialExpressionEventTopicScreenshare.


        :return: The pcSelf of this QueueConversationSocialExpressionEventTopicScreenshare.
        :rtype: QueueConversationSocialExpressionEventTopicAddress
        """
        return self._pcSelf

    @pcSelf.setter
    def pcSelf(self, pcSelf):
        """
        Sets the pcSelf of this QueueConversationSocialExpressionEventTopicScreenshare.


        :param pcSelf: The pcSelf of this QueueConversationSocialExpressionEventTopicScreenshare.
        :type: QueueConversationSocialExpressionEventTopicAddress
        """
        
        self._pcSelf = pcSelf

    @property
    def id(self):
        """
        Gets the id of this QueueConversationSocialExpressionEventTopicScreenshare.


        :return: The id of this QueueConversationSocialExpressionEventTopicScreenshare.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this QueueConversationSocialExpressionEventTopicScreenshare.


        :param id: The id of this QueueConversationSocialExpressionEventTopicScreenshare.
        :type: str
        """
        
        self._id = id

    @property
    def context(self):
        """
        Gets the context of this QueueConversationSocialExpressionEventTopicScreenshare.


        :return: The context of this QueueConversationSocialExpressionEventTopicScreenshare.
        :rtype: str
        """
        return self._context

    @context.setter
    def context(self, context):
        """
        Sets the context of this QueueConversationSocialExpressionEventTopicScreenshare.


        :param context: The context of this QueueConversationSocialExpressionEventTopicScreenshare.
        :type: str
        """
        
        self._context = context

    @property
    def sharing(self):
        """
        Gets the sharing of this QueueConversationSocialExpressionEventTopicScreenshare.


        :return: The sharing of this QueueConversationSocialExpressionEventTopicScreenshare.
        :rtype: bool
        """
        return self._sharing

    @sharing.setter
    def sharing(self, sharing):
        """
        Sets the sharing of this QueueConversationSocialExpressionEventTopicScreenshare.


        :param sharing: The sharing of this QueueConversationSocialExpressionEventTopicScreenshare.
        :type: bool
        """
        
        self._sharing = sharing

    @property
    def provider(self):
        """
        Gets the provider of this QueueConversationSocialExpressionEventTopicScreenshare.


        :return: The provider of this QueueConversationSocialExpressionEventTopicScreenshare.
        :rtype: str
        """
        return self._provider

    @provider.setter
    def provider(self, provider):
        """
        Sets the provider of this QueueConversationSocialExpressionEventTopicScreenshare.


        :param provider: The provider of this QueueConversationSocialExpressionEventTopicScreenshare.
        :type: str
        """
        
        self._provider = provider

    @property
    def script_id(self):
        """
        Gets the script_id of this QueueConversationSocialExpressionEventTopicScreenshare.


        :return: The script_id of this QueueConversationSocialExpressionEventTopicScreenshare.
        :rtype: str
        """
        return self._script_id

    @script_id.setter
    def script_id(self, script_id):
        """
        Sets the script_id of this QueueConversationSocialExpressionEventTopicScreenshare.


        :param script_id: The script_id of this QueueConversationSocialExpressionEventTopicScreenshare.
        :type: str
        """
        
        self._script_id = script_id

    @property
    def peer_id(self):
        """
        Gets the peer_id of this QueueConversationSocialExpressionEventTopicScreenshare.


        :return: The peer_id of this QueueConversationSocialExpressionEventTopicScreenshare.
        :rtype: str
        """
        return self._peer_id

    @peer_id.setter
    def peer_id(self, peer_id):
        """
        Sets the peer_id of this QueueConversationSocialExpressionEventTopicScreenshare.


        :param peer_id: The peer_id of this QueueConversationSocialExpressionEventTopicScreenshare.
        :type: str
        """
        
        self._peer_id = peer_id

    @property
    def disconnect_type(self):
        """
        Gets the disconnect_type of this QueueConversationSocialExpressionEventTopicScreenshare.


        :return: The disconnect_type of this QueueConversationSocialExpressionEventTopicScreenshare.
        :rtype: str
        """
        return self._disconnect_type

    @disconnect_type.setter
    def disconnect_type(self, disconnect_type):
        """
        Sets the disconnect_type of this QueueConversationSocialExpressionEventTopicScreenshare.


        :param disconnect_type: The disconnect_type of this QueueConversationSocialExpressionEventTopicScreenshare.
        :type: str
        """
        allowed_values = ["ENDPOINT", "CLIENT", "SYSTEM", "TIMEOUT", "TRANSFER", "TRANSFER_CONFERENCE", "TRANSFER_CONSULT", "TRANSFER_FORWARD", "TRANSFER_NOANSWER", "TRANSFER_NOTAVAILABLE", "TRANSPORT_FAILURE", "ERROR", "PEER", "OTHER", "SPAM", "UNCALLABLE"]
        if disconnect_type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for disconnect_type -> " + disconnect_type)
            self._disconnect_type = "outdated_sdk_version"
        else:
            self._disconnect_type = disconnect_type

    @property
    def connected_time(self):
        """
        Gets the connected_time of this QueueConversationSocialExpressionEventTopicScreenshare.


        :return: The connected_time of this QueueConversationSocialExpressionEventTopicScreenshare.
        :rtype: datetime
        """
        return self._connected_time

    @connected_time.setter
    def connected_time(self, connected_time):
        """
        Sets the connected_time of this QueueConversationSocialExpressionEventTopicScreenshare.


        :param connected_time: The connected_time of this QueueConversationSocialExpressionEventTopicScreenshare.
        :type: datetime
        """
        
        self._connected_time = connected_time

    @property
    def disconnected_time(self):
        """
        Gets the disconnected_time of this QueueConversationSocialExpressionEventTopicScreenshare.


        :return: The disconnected_time of this QueueConversationSocialExpressionEventTopicScreenshare.
        :rtype: datetime
        """
        return self._disconnected_time

    @disconnected_time.setter
    def disconnected_time(self, disconnected_time):
        """
        Sets the disconnected_time of this QueueConversationSocialExpressionEventTopicScreenshare.


        :param disconnected_time: The disconnected_time of this QueueConversationSocialExpressionEventTopicScreenshare.
        :type: datetime
        """
        
        self._disconnected_time = disconnected_time

    @property
    def wrapup(self):
        """
        Gets the wrapup of this QueueConversationSocialExpressionEventTopicScreenshare.


        :return: The wrapup of this QueueConversationSocialExpressionEventTopicScreenshare.
        :rtype: QueueConversationSocialExpressionEventTopicWrapup
        """
        return self._wrapup

    @wrapup.setter
    def wrapup(self, wrapup):
        """
        Sets the wrapup of this QueueConversationSocialExpressionEventTopicScreenshare.


        :param wrapup: The wrapup of this QueueConversationSocialExpressionEventTopicScreenshare.
        :type: QueueConversationSocialExpressionEventTopicWrapup
        """
        
        self._wrapup = wrapup

    @property
    def after_call_work(self):
        """
        Gets the after_call_work of this QueueConversationSocialExpressionEventTopicScreenshare.


        :return: The after_call_work of this QueueConversationSocialExpressionEventTopicScreenshare.
        :rtype: QueueConversationSocialExpressionEventTopicAfterCallWork
        """
        return self._after_call_work

    @after_call_work.setter
    def after_call_work(self, after_call_work):
        """
        Sets the after_call_work of this QueueConversationSocialExpressionEventTopicScreenshare.


        :param after_call_work: The after_call_work of this QueueConversationSocialExpressionEventTopicScreenshare.
        :type: QueueConversationSocialExpressionEventTopicAfterCallWork
        """
        
        self._after_call_work = after_call_work

    @property
    def after_call_work_required(self):
        """
        Gets the after_call_work_required of this QueueConversationSocialExpressionEventTopicScreenshare.


        :return: The after_call_work_required of this QueueConversationSocialExpressionEventTopicScreenshare.
        :rtype: bool
        """
        return self._after_call_work_required

    @after_call_work_required.setter
    def after_call_work_required(self, after_call_work_required):
        """
        Sets the after_call_work_required of this QueueConversationSocialExpressionEventTopicScreenshare.


        :param after_call_work_required: The after_call_work_required of this QueueConversationSocialExpressionEventTopicScreenshare.
        :type: bool
        """
        
        self._after_call_work_required = after_call_work_required

    @property
    def additional_properties(self):
        """
        Gets the additional_properties of this QueueConversationSocialExpressionEventTopicScreenshare.


        :return: The additional_properties of this QueueConversationSocialExpressionEventTopicScreenshare.
        :rtype: object
        """
        return self._additional_properties

    @additional_properties.setter
    def additional_properties(self, additional_properties):
        """
        Sets the additional_properties of this QueueConversationSocialExpressionEventTopicScreenshare.


        :param additional_properties: The additional_properties of this QueueConversationSocialExpressionEventTopicScreenshare.
        :type: object
        """
        
        self._additional_properties = additional_properties

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

