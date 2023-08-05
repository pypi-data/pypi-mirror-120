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

class QuickReply(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        QuickReply - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'text': 'str',
            'payload': 'str',
            'url': 'str',
            'action': 'str',
            'is_selected': 'bool'
        }

        self.attribute_map = {
            'text': 'text',
            'payload': 'payload',
            'url': 'url',
            'action': 'action',
            'is_selected': 'isSelected'
        }

        self._text = None
        self._payload = None
        self._url = None
        self._action = None
        self._is_selected = None

    @property
    def text(self):
        """
        Gets the text of this QuickReply.
        Text to show inside the quick reply. This is also used as the response text after clicking on the quick reply.

        :return: The text of this QuickReply.
        :rtype: str
        """
        return self._text

    @text.setter
    def text(self, text):
        """
        Sets the text of this QuickReply.
        Text to show inside the quick reply. This is also used as the response text after clicking on the quick reply.

        :param text: The text of this QuickReply.
        :type: str
        """
        
        self._text = text

    @property
    def payload(self):
        """
        Gets the payload of this QuickReply.
        Content of the textback payload after clicking a quick reply

        :return: The payload of this QuickReply.
        :rtype: str
        """
        return self._payload

    @payload.setter
    def payload(self, payload):
        """
        Sets the payload of this QuickReply.
        Content of the textback payload after clicking a quick reply

        :param payload: The payload of this QuickReply.
        :type: str
        """
        
        self._payload = payload

    @property
    def url(self):
        """
        Gets the url of this QuickReply.
        The location of the image file associated with quick reply

        :return: The url of this QuickReply.
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """
        Sets the url of this QuickReply.
        The location of the image file associated with quick reply

        :param url: The url of this QuickReply.
        :type: str
        """
        
        self._url = url

    @property
    def action(self):
        """
        Gets the action of this QuickReply.
        Specifies the type of action that is triggered upon clicking the quick reply. Currently, the only supported action is \"Message\" which sends a message using the quick reply text.

        :return: The action of this QuickReply.
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """
        Sets the action of this QuickReply.
        Specifies the type of action that is triggered upon clicking the quick reply. Currently, the only supported action is \"Message\" which sends a message using the quick reply text.

        :param action: The action of this QuickReply.
        :type: str
        """
        allowed_values = ["Message"]
        if action.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for action -> " + action)
            self._action = "outdated_sdk_version"
        else:
            self._action = action

    @property
    def is_selected(self):
        """
        Gets the is_selected of this QuickReply.
        Indicates if the quick reply option is selected by end customer

        :return: The is_selected of this QuickReply.
        :rtype: bool
        """
        return self._is_selected

    @is_selected.setter
    def is_selected(self, is_selected):
        """
        Sets the is_selected of this QuickReply.
        Indicates if the quick reply option is selected by end customer

        :param is_selected: The is_selected of this QuickReply.
        :type: bool
        """
        
        self._is_selected = is_selected

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

