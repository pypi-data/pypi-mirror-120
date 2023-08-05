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

class FieldList(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        FieldList - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'custom_labels': 'bool',
            'instruction_text': 'str',
            'key': 'str',
            'label_keys': 'list[str]',
            'params': 'dict(str, object)',
            'repeatable': 'bool',
            'state': 'str',
            'type': 'str',
            'required': 'bool',
            'gdpr': 'bool'
        }

        self.attribute_map = {
            'custom_labels': 'customLabels',
            'instruction_text': 'instructionText',
            'key': 'key',
            'label_keys': 'labelKeys',
            'params': 'params',
            'repeatable': 'repeatable',
            'state': 'state',
            'type': 'type',
            'required': 'required',
            'gdpr': 'gdpr'
        }

        self._custom_labels = None
        self._instruction_text = None
        self._key = None
        self._label_keys = None
        self._params = None
        self._repeatable = None
        self._state = None
        self._type = None
        self._required = None
        self._gdpr = None

    @property
    def custom_labels(self):
        """
        Gets the custom_labels of this FieldList.


        :return: The custom_labels of this FieldList.
        :rtype: bool
        """
        return self._custom_labels

    @custom_labels.setter
    def custom_labels(self, custom_labels):
        """
        Sets the custom_labels of this FieldList.


        :param custom_labels: The custom_labels of this FieldList.
        :type: bool
        """
        
        self._custom_labels = custom_labels

    @property
    def instruction_text(self):
        """
        Gets the instruction_text of this FieldList.


        :return: The instruction_text of this FieldList.
        :rtype: str
        """
        return self._instruction_text

    @instruction_text.setter
    def instruction_text(self, instruction_text):
        """
        Sets the instruction_text of this FieldList.


        :param instruction_text: The instruction_text of this FieldList.
        :type: str
        """
        
        self._instruction_text = instruction_text

    @property
    def key(self):
        """
        Gets the key of this FieldList.


        :return: The key of this FieldList.
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """
        Sets the key of this FieldList.


        :param key: The key of this FieldList.
        :type: str
        """
        
        self._key = key

    @property
    def label_keys(self):
        """
        Gets the label_keys of this FieldList.


        :return: The label_keys of this FieldList.
        :rtype: list[str]
        """
        return self._label_keys

    @label_keys.setter
    def label_keys(self, label_keys):
        """
        Sets the label_keys of this FieldList.


        :param label_keys: The label_keys of this FieldList.
        :type: list[str]
        """
        
        self._label_keys = label_keys

    @property
    def params(self):
        """
        Gets the params of this FieldList.


        :return: The params of this FieldList.
        :rtype: dict(str, object)
        """
        return self._params

    @params.setter
    def params(self, params):
        """
        Sets the params of this FieldList.


        :param params: The params of this FieldList.
        :type: dict(str, object)
        """
        
        self._params = params

    @property
    def repeatable(self):
        """
        Gets the repeatable of this FieldList.


        :return: The repeatable of this FieldList.
        :rtype: bool
        """
        return self._repeatable

    @repeatable.setter
    def repeatable(self, repeatable):
        """
        Sets the repeatable of this FieldList.


        :param repeatable: The repeatable of this FieldList.
        :type: bool
        """
        
        self._repeatable = repeatable

    @property
    def state(self):
        """
        Gets the state of this FieldList.


        :return: The state of this FieldList.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this FieldList.


        :param state: The state of this FieldList.
        :type: str
        """
        
        self._state = state

    @property
    def type(self):
        """
        Gets the type of this FieldList.


        :return: The type of this FieldList.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this FieldList.


        :param type: The type of this FieldList.
        :type: str
        """
        
        self._type = type

    @property
    def required(self):
        """
        Gets the required of this FieldList.


        :return: The required of this FieldList.
        :rtype: bool
        """
        return self._required

    @required.setter
    def required(self, required):
        """
        Sets the required of this FieldList.


        :param required: The required of this FieldList.
        :type: bool
        """
        
        self._required = required

    @property
    def gdpr(self):
        """
        Gets the gdpr of this FieldList.


        :return: The gdpr of this FieldList.
        :rtype: bool
        """
        return self._gdpr

    @gdpr.setter
    def gdpr(self, gdpr):
        """
        Sets the gdpr of this FieldList.


        :param gdpr: The gdpr of this FieldList.
        :type: bool
        """
        
        self._gdpr = gdpr

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

