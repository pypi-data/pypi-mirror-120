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

class RecordingMessagingMessage(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        RecordingMessagingMessage - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'pcFrom': 'str',
            'from_user': 'User',
            'from_external_contact': 'ExternalContact',
            'to': 'str',
            'timestamp': 'datetime',
            'id': 'str',
            'message_text': 'str',
            'message_media_attachments': 'list[MessageMediaAttachment]',
            'message_sticker_attachments': 'list[MessageStickerAttachment]'
        }

        self.attribute_map = {
            'pcFrom': 'from',
            'from_user': 'fromUser',
            'from_external_contact': 'fromExternalContact',
            'to': 'to',
            'timestamp': 'timestamp',
            'id': 'id',
            'message_text': 'messageText',
            'message_media_attachments': 'messageMediaAttachments',
            'message_sticker_attachments': 'messageStickerAttachments'
        }

        self._pcFrom = None
        self._from_user = None
        self._from_external_contact = None
        self._to = None
        self._timestamp = None
        self._id = None
        self._message_text = None
        self._message_media_attachments = None
        self._message_sticker_attachments = None

    @property
    def pcFrom(self):
        """
        Gets the pcFrom of this RecordingMessagingMessage.


        :return: The pcFrom of this RecordingMessagingMessage.
        :rtype: str
        """
        return self._pcFrom

    @pcFrom.setter
    def pcFrom(self, pcFrom):
        """
        Sets the pcFrom of this RecordingMessagingMessage.


        :param pcFrom: The pcFrom of this RecordingMessagingMessage.
        :type: str
        """
        
        self._pcFrom = pcFrom

    @property
    def from_user(self):
        """
        Gets the from_user of this RecordingMessagingMessage.


        :return: The from_user of this RecordingMessagingMessage.
        :rtype: User
        """
        return self._from_user

    @from_user.setter
    def from_user(self, from_user):
        """
        Sets the from_user of this RecordingMessagingMessage.


        :param from_user: The from_user of this RecordingMessagingMessage.
        :type: User
        """
        
        self._from_user = from_user

    @property
    def from_external_contact(self):
        """
        Gets the from_external_contact of this RecordingMessagingMessage.


        :return: The from_external_contact of this RecordingMessagingMessage.
        :rtype: ExternalContact
        """
        return self._from_external_contact

    @from_external_contact.setter
    def from_external_contact(self, from_external_contact):
        """
        Sets the from_external_contact of this RecordingMessagingMessage.


        :param from_external_contact: The from_external_contact of this RecordingMessagingMessage.
        :type: ExternalContact
        """
        
        self._from_external_contact = from_external_contact

    @property
    def to(self):
        """
        Gets the to of this RecordingMessagingMessage.


        :return: The to of this RecordingMessagingMessage.
        :rtype: str
        """
        return self._to

    @to.setter
    def to(self, to):
        """
        Sets the to of this RecordingMessagingMessage.


        :param to: The to of this RecordingMessagingMessage.
        :type: str
        """
        
        self._to = to

    @property
    def timestamp(self):
        """
        Gets the timestamp of this RecordingMessagingMessage.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The timestamp of this RecordingMessagingMessage.
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """
        Sets the timestamp of this RecordingMessagingMessage.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param timestamp: The timestamp of this RecordingMessagingMessage.
        :type: datetime
        """
        
        self._timestamp = timestamp

    @property
    def id(self):
        """
        Gets the id of this RecordingMessagingMessage.


        :return: The id of this RecordingMessagingMessage.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this RecordingMessagingMessage.


        :param id: The id of this RecordingMessagingMessage.
        :type: str
        """
        
        self._id = id

    @property
    def message_text(self):
        """
        Gets the message_text of this RecordingMessagingMessage.


        :return: The message_text of this RecordingMessagingMessage.
        :rtype: str
        """
        return self._message_text

    @message_text.setter
    def message_text(self, message_text):
        """
        Sets the message_text of this RecordingMessagingMessage.


        :param message_text: The message_text of this RecordingMessagingMessage.
        :type: str
        """
        
        self._message_text = message_text

    @property
    def message_media_attachments(self):
        """
        Gets the message_media_attachments of this RecordingMessagingMessage.


        :return: The message_media_attachments of this RecordingMessagingMessage.
        :rtype: list[MessageMediaAttachment]
        """
        return self._message_media_attachments

    @message_media_attachments.setter
    def message_media_attachments(self, message_media_attachments):
        """
        Sets the message_media_attachments of this RecordingMessagingMessage.


        :param message_media_attachments: The message_media_attachments of this RecordingMessagingMessage.
        :type: list[MessageMediaAttachment]
        """
        
        self._message_media_attachments = message_media_attachments

    @property
    def message_sticker_attachments(self):
        """
        Gets the message_sticker_attachments of this RecordingMessagingMessage.


        :return: The message_sticker_attachments of this RecordingMessagingMessage.
        :rtype: list[MessageStickerAttachment]
        """
        return self._message_sticker_attachments

    @message_sticker_attachments.setter
    def message_sticker_attachments(self, message_sticker_attachments):
        """
        Sets the message_sticker_attachments of this RecordingMessagingMessage.


        :param message_sticker_attachments: The message_sticker_attachments of this RecordingMessagingMessage.
        :type: list[MessageStickerAttachment]
        """
        
        self._message_sticker_attachments = message_sticker_attachments

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

