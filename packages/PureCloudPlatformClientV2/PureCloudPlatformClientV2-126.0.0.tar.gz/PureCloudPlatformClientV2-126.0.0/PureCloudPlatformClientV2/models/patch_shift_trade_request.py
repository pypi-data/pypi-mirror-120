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

class PatchShiftTradeRequest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        PatchShiftTradeRequest - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'receiving_user_id': 'ValueWrapperString',
            'expiration': 'ValueWrapperDate',
            'acceptable_intervals': 'ListWrapperInterval',
            'metadata': 'WfmVersionedEntityMetadata'
        }

        self.attribute_map = {
            'receiving_user_id': 'receivingUserId',
            'expiration': 'expiration',
            'acceptable_intervals': 'acceptableIntervals',
            'metadata': 'metadata'
        }

        self._receiving_user_id = None
        self._expiration = None
        self._acceptable_intervals = None
        self._metadata = None

    @property
    def receiving_user_id(self):
        """
        Gets the receiving_user_id of this PatchShiftTradeRequest.
        Update the ID of the receiving user to direct the request at a specific user, or set the wrapped id to null to open up a trade to be matched by any user.

        :return: The receiving_user_id of this PatchShiftTradeRequest.
        :rtype: ValueWrapperString
        """
        return self._receiving_user_id

    @receiving_user_id.setter
    def receiving_user_id(self, receiving_user_id):
        """
        Sets the receiving_user_id of this PatchShiftTradeRequest.
        Update the ID of the receiving user to direct the request at a specific user, or set the wrapped id to null to open up a trade to be matched by any user.

        :param receiving_user_id: The receiving_user_id of this PatchShiftTradeRequest.
        :type: ValueWrapperString
        """
        
        self._receiving_user_id = receiving_user_id

    @property
    def expiration(self):
        """
        Gets the expiration of this PatchShiftTradeRequest.
        Update the expiration time for this shift trade.

        :return: The expiration of this PatchShiftTradeRequest.
        :rtype: ValueWrapperDate
        """
        return self._expiration

    @expiration.setter
    def expiration(self, expiration):
        """
        Sets the expiration of this PatchShiftTradeRequest.
        Update the expiration time for this shift trade.

        :param expiration: The expiration of this PatchShiftTradeRequest.
        :type: ValueWrapperDate
        """
        
        self._expiration = expiration

    @property
    def acceptable_intervals(self):
        """
        Gets the acceptable_intervals of this PatchShiftTradeRequest.
        Update the acceptable intervals the initiating user is willing to accept in trade. Setting the enclosed list to empty will make this a one sided trade request

        :return: The acceptable_intervals of this PatchShiftTradeRequest.
        :rtype: ListWrapperInterval
        """
        return self._acceptable_intervals

    @acceptable_intervals.setter
    def acceptable_intervals(self, acceptable_intervals):
        """
        Sets the acceptable_intervals of this PatchShiftTradeRequest.
        Update the acceptable intervals the initiating user is willing to accept in trade. Setting the enclosed list to empty will make this a one sided trade request

        :param acceptable_intervals: The acceptable_intervals of this PatchShiftTradeRequest.
        :type: ListWrapperInterval
        """
        
        self._acceptable_intervals = acceptable_intervals

    @property
    def metadata(self):
        """
        Gets the metadata of this PatchShiftTradeRequest.
        Version metadata

        :return: The metadata of this PatchShiftTradeRequest.
        :rtype: WfmVersionedEntityMetadata
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this PatchShiftTradeRequest.
        Version metadata

        :param metadata: The metadata of this PatchShiftTradeRequest.
        :type: WfmVersionedEntityMetadata
        """
        
        self._metadata = metadata

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

