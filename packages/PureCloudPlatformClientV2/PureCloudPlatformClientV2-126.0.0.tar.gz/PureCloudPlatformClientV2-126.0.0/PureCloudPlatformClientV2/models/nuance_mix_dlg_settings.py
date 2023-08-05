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

class NuanceMixDlgSettings(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        NuanceMixDlgSettings - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'channel_id': 'str',
            'input_parameters': 'dict(str, object)'
        }

        self.attribute_map = {
            'channel_id': 'channelId',
            'input_parameters': 'inputParameters'
        }

        self._channel_id = None
        self._input_parameters = None

    @property
    def channel_id(self):
        """
        Gets the channel_id of this NuanceMixDlgSettings.
        The Nuance channel ID to use when launching the Nuance bot, which must one of the code names of the bot's registered input channels.

        :return: The channel_id of this NuanceMixDlgSettings.
        :rtype: str
        """
        return self._channel_id

    @channel_id.setter
    def channel_id(self, channel_id):
        """
        Sets the channel_id of this NuanceMixDlgSettings.
        The Nuance channel ID to use when launching the Nuance bot, which must one of the code names of the bot's registered input channels.

        :param channel_id: The channel_id of this NuanceMixDlgSettings.
        :type: str
        """
        
        self._channel_id = channel_id

    @property
    def input_parameters(self):
        """
        Gets the input_parameters of this NuanceMixDlgSettings.
        Name/value pairs of input variables to be sent to the Nuance bot. The values must be in the appropriate format for the variable's type (see https://docs.mix.nuance.com/dialog-grpc/v1/#simple-variable-types for help)

        :return: The input_parameters of this NuanceMixDlgSettings.
        :rtype: dict(str, object)
        """
        return self._input_parameters

    @input_parameters.setter
    def input_parameters(self, input_parameters):
        """
        Sets the input_parameters of this NuanceMixDlgSettings.
        Name/value pairs of input variables to be sent to the Nuance bot. The values must be in the appropriate format for the variable's type (see https://docs.mix.nuance.com/dialog-grpc/v1/#simple-variable-types for help)

        :param input_parameters: The input_parameters of this NuanceMixDlgSettings.
        :type: dict(str, object)
        """
        
        self._input_parameters = input_parameters

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

