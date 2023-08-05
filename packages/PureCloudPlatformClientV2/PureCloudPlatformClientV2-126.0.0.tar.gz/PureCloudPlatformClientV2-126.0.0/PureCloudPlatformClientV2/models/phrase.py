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

class Phrase(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        Phrase - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'text': 'str',
            'strictness': 'str',
            'sentiment': 'str'
        }

        self.attribute_map = {
            'text': 'text',
            'strictness': 'strictness',
            'sentiment': 'sentiment'
        }

        self._text = None
        self._strictness = None
        self._sentiment = None

    @property
    def text(self):
        """
        Gets the text of this Phrase.
        The phrase text

        :return: The text of this Phrase.
        :rtype: str
        """
        return self._text

    @text.setter
    def text(self, text):
        """
        Sets the text of this Phrase.
        The phrase text

        :param text: The text of this Phrase.
        :type: str
        """
        
        self._text = text

    @property
    def strictness(self):
        """
        Gets the strictness of this Phrase.
        The phrase strictness, default value is null

        :return: The strictness of this Phrase.
        :rtype: str
        """
        return self._strictness

    @strictness.setter
    def strictness(self, strictness):
        """
        Sets the strictness of this Phrase.
        The phrase strictness, default value is null

        :param strictness: The strictness of this Phrase.
        :type: str
        """
        allowed_values = ["1", "55", "65", "72", "85", "90"]
        if strictness.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for strictness -> " + strictness)
            self._strictness = "outdated_sdk_version"
        else:
            self._strictness = strictness

    @property
    def sentiment(self):
        """
        Gets the sentiment of this Phrase.
        The phrase sentiment, default value is Unspecified

        :return: The sentiment of this Phrase.
        :rtype: str
        """
        return self._sentiment

    @sentiment.setter
    def sentiment(self, sentiment):
        """
        Sets the sentiment of this Phrase.
        The phrase sentiment, default value is Unspecified

        :param sentiment: The sentiment of this Phrase.
        :type: str
        """
        allowed_values = ["Unspecified", "Positive", "Neutral", "Negative"]
        if sentiment.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for sentiment -> " + sentiment)
            self._sentiment = "outdated_sdk_version"
        else:
            self._sentiment = sentiment

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

