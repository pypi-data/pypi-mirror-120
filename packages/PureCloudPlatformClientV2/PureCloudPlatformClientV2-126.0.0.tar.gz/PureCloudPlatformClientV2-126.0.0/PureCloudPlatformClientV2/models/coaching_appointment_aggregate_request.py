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

class CoachingAppointmentAggregateRequest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        CoachingAppointmentAggregateRequest - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'interval': 'str',
            'metrics': 'list[str]',
            'group_by': 'list[str]',
            'filter': 'QueryRequestFilter'
        }

        self.attribute_map = {
            'interval': 'interval',
            'metrics': 'metrics',
            'group_by': 'groupBy',
            'filter': 'filter'
        }

        self._interval = None
        self._metrics = None
        self._group_by = None
        self._filter = None

    @property
    def interval(self):
        """
        Gets the interval of this CoachingAppointmentAggregateRequest.
        Interval to aggregate across. End date is not inclusive. Intervals are represented as an ISO-8601 string. For example: YYYY-MM-DDThh:mm:ss/YYYY-MM-DDThh:mm:ss

        :return: The interval of this CoachingAppointmentAggregateRequest.
        :rtype: str
        """
        return self._interval

    @interval.setter
    def interval(self, interval):
        """
        Sets the interval of this CoachingAppointmentAggregateRequest.
        Interval to aggregate across. End date is not inclusive. Intervals are represented as an ISO-8601 string. For example: YYYY-MM-DDThh:mm:ss/YYYY-MM-DDThh:mm:ss

        :param interval: The interval of this CoachingAppointmentAggregateRequest.
        :type: str
        """
        
        self._interval = interval

    @property
    def metrics(self):
        """
        Gets the metrics of this CoachingAppointmentAggregateRequest.
        A list of metrics to aggregate.  If omitted, all metrics are returned.

        :return: The metrics of this CoachingAppointmentAggregateRequest.
        :rtype: list[str]
        """
        return self._metrics

    @metrics.setter
    def metrics(self, metrics):
        """
        Sets the metrics of this CoachingAppointmentAggregateRequest.
        A list of metrics to aggregate.  If omitted, all metrics are returned.

        :param metrics: The metrics of this CoachingAppointmentAggregateRequest.
        :type: list[str]
        """
        
        self._metrics = metrics

    @property
    def group_by(self):
        """
        Gets the group_by of this CoachingAppointmentAggregateRequest.
        An optional list of items by which to group the result data.

        :return: The group_by of this CoachingAppointmentAggregateRequest.
        :rtype: list[str]
        """
        return self._group_by

    @group_by.setter
    def group_by(self, group_by):
        """
        Sets the group_by of this CoachingAppointmentAggregateRequest.
        An optional list of items by which to group the result data.

        :param group_by: The group_by of this CoachingAppointmentAggregateRequest.
        :type: list[str]
        """
        
        self._group_by = group_by

    @property
    def filter(self):
        """
        Gets the filter of this CoachingAppointmentAggregateRequest.
        The filter applied to the data

        :return: The filter of this CoachingAppointmentAggregateRequest.
        :rtype: QueryRequestFilter
        """
        return self._filter

    @filter.setter
    def filter(self, filter):
        """
        Sets the filter of this CoachingAppointmentAggregateRequest.
        The filter applied to the data

        :param filter: The filter of this CoachingAppointmentAggregateRequest.
        :type: QueryRequestFilter
        """
        
        self._filter = filter

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

