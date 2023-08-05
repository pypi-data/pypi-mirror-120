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

class CreateCallbackCommand(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        CreateCallbackCommand - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'script_id': 'str',
            'queue_id': 'str',
            'routing_data': 'RoutingData',
            'callback_user_name': 'str',
            'callback_numbers': 'list[str]',
            'callback_scheduled_time': 'datetime',
            'country_code': 'str',
            'validate_callback_numbers': 'bool',
            'data': 'dict(str, str)',
            'caller_id': 'str',
            'caller_id_name': 'str'
        }

        self.attribute_map = {
            'script_id': 'scriptId',
            'queue_id': 'queueId',
            'routing_data': 'routingData',
            'callback_user_name': 'callbackUserName',
            'callback_numbers': 'callbackNumbers',
            'callback_scheduled_time': 'callbackScheduledTime',
            'country_code': 'countryCode',
            'validate_callback_numbers': 'validateCallbackNumbers',
            'data': 'data',
            'caller_id': 'callerId',
            'caller_id_name': 'callerIdName'
        }

        self._script_id = None
        self._queue_id = None
        self._routing_data = None
        self._callback_user_name = None
        self._callback_numbers = None
        self._callback_scheduled_time = None
        self._country_code = None
        self._validate_callback_numbers = None
        self._data = None
        self._caller_id = None
        self._caller_id_name = None

    @property
    def script_id(self):
        """
        Gets the script_id of this CreateCallbackCommand.
        The identifier of the script to be used for the callback

        :return: The script_id of this CreateCallbackCommand.
        :rtype: str
        """
        return self._script_id

    @script_id.setter
    def script_id(self, script_id):
        """
        Sets the script_id of this CreateCallbackCommand.
        The identifier of the script to be used for the callback

        :param script_id: The script_id of this CreateCallbackCommand.
        :type: str
        """
        
        self._script_id = script_id

    @property
    def queue_id(self):
        """
        Gets the queue_id of this CreateCallbackCommand.
        The identifier of the queue to be used for the callback. Either queueId or routingData is required.

        :return: The queue_id of this CreateCallbackCommand.
        :rtype: str
        """
        return self._queue_id

    @queue_id.setter
    def queue_id(self, queue_id):
        """
        Sets the queue_id of this CreateCallbackCommand.
        The identifier of the queue to be used for the callback. Either queueId or routingData is required.

        :param queue_id: The queue_id of this CreateCallbackCommand.
        :type: str
        """
        
        self._queue_id = queue_id

    @property
    def routing_data(self):
        """
        Gets the routing_data of this CreateCallbackCommand.
        The routing data to be used for the callback. Either queueId or routingData is required.

        :return: The routing_data of this CreateCallbackCommand.
        :rtype: RoutingData
        """
        return self._routing_data

    @routing_data.setter
    def routing_data(self, routing_data):
        """
        Sets the routing_data of this CreateCallbackCommand.
        The routing data to be used for the callback. Either queueId or routingData is required.

        :param routing_data: The routing_data of this CreateCallbackCommand.
        :type: RoutingData
        """
        
        self._routing_data = routing_data

    @property
    def callback_user_name(self):
        """
        Gets the callback_user_name of this CreateCallbackCommand.
        The name of the party to be called back.

        :return: The callback_user_name of this CreateCallbackCommand.
        :rtype: str
        """
        return self._callback_user_name

    @callback_user_name.setter
    def callback_user_name(self, callback_user_name):
        """
        Sets the callback_user_name of this CreateCallbackCommand.
        The name of the party to be called back.

        :param callback_user_name: The callback_user_name of this CreateCallbackCommand.
        :type: str
        """
        
        self._callback_user_name = callback_user_name

    @property
    def callback_numbers(self):
        """
        Gets the callback_numbers of this CreateCallbackCommand.
        A list of phone numbers for the callback.

        :return: The callback_numbers of this CreateCallbackCommand.
        :rtype: list[str]
        """
        return self._callback_numbers

    @callback_numbers.setter
    def callback_numbers(self, callback_numbers):
        """
        Sets the callback_numbers of this CreateCallbackCommand.
        A list of phone numbers for the callback.

        :param callback_numbers: The callback_numbers of this CreateCallbackCommand.
        :type: list[str]
        """
        
        self._callback_numbers = callback_numbers

    @property
    def callback_scheduled_time(self):
        """
        Gets the callback_scheduled_time of this CreateCallbackCommand.
        The scheduled date-time for the callback as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The callback_scheduled_time of this CreateCallbackCommand.
        :rtype: datetime
        """
        return self._callback_scheduled_time

    @callback_scheduled_time.setter
    def callback_scheduled_time(self, callback_scheduled_time):
        """
        Sets the callback_scheduled_time of this CreateCallbackCommand.
        The scheduled date-time for the callback as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param callback_scheduled_time: The callback_scheduled_time of this CreateCallbackCommand.
        :type: datetime
        """
        
        self._callback_scheduled_time = callback_scheduled_time

    @property
    def country_code(self):
        """
        Gets the country_code of this CreateCallbackCommand.
        The country code to be associated with the callback numbers.

        :return: The country_code of this CreateCallbackCommand.
        :rtype: str
        """
        return self._country_code

    @country_code.setter
    def country_code(self, country_code):
        """
        Sets the country_code of this CreateCallbackCommand.
        The country code to be associated with the callback numbers.

        :param country_code: The country_code of this CreateCallbackCommand.
        :type: str
        """
        
        self._country_code = country_code

    @property
    def validate_callback_numbers(self):
        """
        Gets the validate_callback_numbers of this CreateCallbackCommand.
        Whether or not to validate the callback numbers for phone number format.

        :return: The validate_callback_numbers of this CreateCallbackCommand.
        :rtype: bool
        """
        return self._validate_callback_numbers

    @validate_callback_numbers.setter
    def validate_callback_numbers(self, validate_callback_numbers):
        """
        Sets the validate_callback_numbers of this CreateCallbackCommand.
        Whether or not to validate the callback numbers for phone number format.

        :param validate_callback_numbers: The validate_callback_numbers of this CreateCallbackCommand.
        :type: bool
        """
        
        self._validate_callback_numbers = validate_callback_numbers

    @property
    def data(self):
        """
        Gets the data of this CreateCallbackCommand.
        A map of key-value pairs containing additional data that can be associated to the callback. These values will appear in the attributes property on the conversation participant. Example: { \"notes\": \"ready to close the deal!\", \"customerPreferredName\": \"Doc\" }

        :return: The data of this CreateCallbackCommand.
        :rtype: dict(str, str)
        """
        return self._data

    @data.setter
    def data(self, data):
        """
        Sets the data of this CreateCallbackCommand.
        A map of key-value pairs containing additional data that can be associated to the callback. These values will appear in the attributes property on the conversation participant. Example: { \"notes\": \"ready to close the deal!\", \"customerPreferredName\": \"Doc\" }

        :param data: The data of this CreateCallbackCommand.
        :type: dict(str, str)
        """
        
        self._data = data

    @property
    def caller_id(self):
        """
        Gets the caller_id of this CreateCallbackCommand.
        The phone number displayed to recipients when a phone call is placed as part of the callback. Must conform to the E.164 format. May be overridden by other settings in the system such as external trunk settings. Telco support for \"callerId\" varies.

        :return: The caller_id of this CreateCallbackCommand.
        :rtype: str
        """
        return self._caller_id

    @caller_id.setter
    def caller_id(self, caller_id):
        """
        Sets the caller_id of this CreateCallbackCommand.
        The phone number displayed to recipients when a phone call is placed as part of the callback. Must conform to the E.164 format. May be overridden by other settings in the system such as external trunk settings. Telco support for \"callerId\" varies.

        :param caller_id: The caller_id of this CreateCallbackCommand.
        :type: str
        """
        
        self._caller_id = caller_id

    @property
    def caller_id_name(self):
        """
        Gets the caller_id_name of this CreateCallbackCommand.
        The name displayed to recipients when a phone call is placed as part of the callback. May be overridden by other settings in the system such as external trunk settings. Telco support for \"callerIdName\" varies.

        :return: The caller_id_name of this CreateCallbackCommand.
        :rtype: str
        """
        return self._caller_id_name

    @caller_id_name.setter
    def caller_id_name(self, caller_id_name):
        """
        Sets the caller_id_name of this CreateCallbackCommand.
        The name displayed to recipients when a phone call is placed as part of the callback. May be overridden by other settings in the system such as external trunk settings. Telco support for \"callerIdName\" varies.

        :param caller_id_name: The caller_id_name of this CreateCallbackCommand.
        :type: str
        """
        
        self._caller_id_name = caller_id_name

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

