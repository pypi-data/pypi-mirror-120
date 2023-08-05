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

class TranscriptionTopicTranscriptWord(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        TranscriptionTopicTranscriptWord - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'confidence': 'float',
            'start_time_ms': 'int',
            'offset_ms': 'int',
            'duration_ms': 'int',
            'word': 'str'
        }

        self.attribute_map = {
            'confidence': 'confidence',
            'start_time_ms': 'startTimeMs',
            'offset_ms': 'offsetMs',
            'duration_ms': 'durationMs',
            'word': 'word'
        }

        self._confidence = None
        self._start_time_ms = None
        self._offset_ms = None
        self._duration_ms = None
        self._word = None

    @property
    def confidence(self):
        """
        Gets the confidence of this TranscriptionTopicTranscriptWord.


        :return: The confidence of this TranscriptionTopicTranscriptWord.
        :rtype: float
        """
        return self._confidence

    @confidence.setter
    def confidence(self, confidence):
        """
        Sets the confidence of this TranscriptionTopicTranscriptWord.


        :param confidence: The confidence of this TranscriptionTopicTranscriptWord.
        :type: float
        """
        
        self._confidence = confidence

    @property
    def start_time_ms(self):
        """
        Gets the start_time_ms of this TranscriptionTopicTranscriptWord.


        :return: The start_time_ms of this TranscriptionTopicTranscriptWord.
        :rtype: int
        """
        return self._start_time_ms

    @start_time_ms.setter
    def start_time_ms(self, start_time_ms):
        """
        Sets the start_time_ms of this TranscriptionTopicTranscriptWord.


        :param start_time_ms: The start_time_ms of this TranscriptionTopicTranscriptWord.
        :type: int
        """
        
        self._start_time_ms = start_time_ms

    @property
    def offset_ms(self):
        """
        Gets the offset_ms of this TranscriptionTopicTranscriptWord.


        :return: The offset_ms of this TranscriptionTopicTranscriptWord.
        :rtype: int
        """
        return self._offset_ms

    @offset_ms.setter
    def offset_ms(self, offset_ms):
        """
        Sets the offset_ms of this TranscriptionTopicTranscriptWord.


        :param offset_ms: The offset_ms of this TranscriptionTopicTranscriptWord.
        :type: int
        """
        
        self._offset_ms = offset_ms

    @property
    def duration_ms(self):
        """
        Gets the duration_ms of this TranscriptionTopicTranscriptWord.


        :return: The duration_ms of this TranscriptionTopicTranscriptWord.
        :rtype: int
        """
        return self._duration_ms

    @duration_ms.setter
    def duration_ms(self, duration_ms):
        """
        Sets the duration_ms of this TranscriptionTopicTranscriptWord.


        :param duration_ms: The duration_ms of this TranscriptionTopicTranscriptWord.
        :type: int
        """
        
        self._duration_ms = duration_ms

    @property
    def word(self):
        """
        Gets the word of this TranscriptionTopicTranscriptWord.


        :return: The word of this TranscriptionTopicTranscriptWord.
        :rtype: str
        """
        return self._word

    @word.setter
    def word(self, word):
        """
        Sets the word of this TranscriptionTopicTranscriptWord.


        :param word: The word of this TranscriptionTopicTranscriptWord.
        :type: str
        """
        
        self._word = word

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

