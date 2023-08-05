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

class DevelopmentActivityAggregateQueryResponseMetric(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        DevelopmentActivityAggregateQueryResponseMetric - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'metric': 'str',
            'stats': 'DevelopmentActivityAggregateQueryResponseStatistics'
        }

        self.attribute_map = {
            'metric': 'metric',
            'stats': 'stats'
        }

        self._metric = None
        self._stats = None

    @property
    def metric(self):
        """
        Gets the metric of this DevelopmentActivityAggregateQueryResponseMetric.
        The metric this applies to

        :return: The metric of this DevelopmentActivityAggregateQueryResponseMetric.
        :rtype: str
        """
        return self._metric

    @metric.setter
    def metric(self, metric):
        """
        Sets the metric of this DevelopmentActivityAggregateQueryResponseMetric.
        The metric this applies to

        :param metric: The metric of this DevelopmentActivityAggregateQueryResponseMetric.
        :type: str
        """
        allowed_values = ["nActivities", "nPlannedActivities", "nInProgressActivities", "nCompleteActivities", "nOverdueActivities", "nInvalidScheduleActivities", "nPassedActivities", "nFailedActivities", "oActivityScore"]
        if metric.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for metric -> " + metric)
            self._metric = "outdated_sdk_version"
        else:
            self._metric = metric

    @property
    def stats(self):
        """
        Gets the stats of this DevelopmentActivityAggregateQueryResponseMetric.
        The aggregated values for this metric

        :return: The stats of this DevelopmentActivityAggregateQueryResponseMetric.
        :rtype: DevelopmentActivityAggregateQueryResponseStatistics
        """
        return self._stats

    @stats.setter
    def stats(self, stats):
        """
        Sets the stats of this DevelopmentActivityAggregateQueryResponseMetric.
        The aggregated values for this metric

        :param stats: The stats of this DevelopmentActivityAggregateQueryResponseMetric.
        :type: DevelopmentActivityAggregateQueryResponseStatistics
        """
        
        self._stats = stats

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

