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

class SchedulingSettingsRequest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        SchedulingSettingsRequest - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'max_occupancy_percent_for_deferred_work': 'int',
            'default_shrinkage_percent': 'float',
            'shrinkage_overrides': 'ShrinkageOverrides',
            'planning_period': 'ValueWrapperPlanningPeriodSettings',
            'start_day_of_weekend': 'str'
        }

        self.attribute_map = {
            'max_occupancy_percent_for_deferred_work': 'maxOccupancyPercentForDeferredWork',
            'default_shrinkage_percent': 'defaultShrinkagePercent',
            'shrinkage_overrides': 'shrinkageOverrides',
            'planning_period': 'planningPeriod',
            'start_day_of_weekend': 'startDayOfWeekend'
        }

        self._max_occupancy_percent_for_deferred_work = None
        self._default_shrinkage_percent = None
        self._shrinkage_overrides = None
        self._planning_period = None
        self._start_day_of_weekend = None

    @property
    def max_occupancy_percent_for_deferred_work(self):
        """
        Gets the max_occupancy_percent_for_deferred_work of this SchedulingSettingsRequest.
        Max occupancy percent for deferred work

        :return: The max_occupancy_percent_for_deferred_work of this SchedulingSettingsRequest.
        :rtype: int
        """
        return self._max_occupancy_percent_for_deferred_work

    @max_occupancy_percent_for_deferred_work.setter
    def max_occupancy_percent_for_deferred_work(self, max_occupancy_percent_for_deferred_work):
        """
        Sets the max_occupancy_percent_for_deferred_work of this SchedulingSettingsRequest.
        Max occupancy percent for deferred work

        :param max_occupancy_percent_for_deferred_work: The max_occupancy_percent_for_deferred_work of this SchedulingSettingsRequest.
        :type: int
        """
        
        self._max_occupancy_percent_for_deferred_work = max_occupancy_percent_for_deferred_work

    @property
    def default_shrinkage_percent(self):
        """
        Gets the default_shrinkage_percent of this SchedulingSettingsRequest.
        Default shrinkage percent for scheduling

        :return: The default_shrinkage_percent of this SchedulingSettingsRequest.
        :rtype: float
        """
        return self._default_shrinkage_percent

    @default_shrinkage_percent.setter
    def default_shrinkage_percent(self, default_shrinkage_percent):
        """
        Sets the default_shrinkage_percent of this SchedulingSettingsRequest.
        Default shrinkage percent for scheduling

        :param default_shrinkage_percent: The default_shrinkage_percent of this SchedulingSettingsRequest.
        :type: float
        """
        
        self._default_shrinkage_percent = default_shrinkage_percent

    @property
    def shrinkage_overrides(self):
        """
        Gets the shrinkage_overrides of this SchedulingSettingsRequest.
        Shrinkage overrides for scheduling

        :return: The shrinkage_overrides of this SchedulingSettingsRequest.
        :rtype: ShrinkageOverrides
        """
        return self._shrinkage_overrides

    @shrinkage_overrides.setter
    def shrinkage_overrides(self, shrinkage_overrides):
        """
        Sets the shrinkage_overrides of this SchedulingSettingsRequest.
        Shrinkage overrides for scheduling

        :param shrinkage_overrides: The shrinkage_overrides of this SchedulingSettingsRequest.
        :type: ShrinkageOverrides
        """
        
        self._shrinkage_overrides = shrinkage_overrides

    @property
    def planning_period(self):
        """
        Gets the planning_period of this SchedulingSettingsRequest.
        Planning period settings for scheduling

        :return: The planning_period of this SchedulingSettingsRequest.
        :rtype: ValueWrapperPlanningPeriodSettings
        """
        return self._planning_period

    @planning_period.setter
    def planning_period(self, planning_period):
        """
        Sets the planning_period of this SchedulingSettingsRequest.
        Planning period settings for scheduling

        :param planning_period: The planning_period of this SchedulingSettingsRequest.
        :type: ValueWrapperPlanningPeriodSettings
        """
        
        self._planning_period = planning_period

    @property
    def start_day_of_weekend(self):
        """
        Gets the start_day_of_weekend of this SchedulingSettingsRequest.
        Start day of weekend for scheduling

        :return: The start_day_of_weekend of this SchedulingSettingsRequest.
        :rtype: str
        """
        return self._start_day_of_weekend

    @start_day_of_weekend.setter
    def start_day_of_weekend(self, start_day_of_weekend):
        """
        Sets the start_day_of_weekend of this SchedulingSettingsRequest.
        Start day of weekend for scheduling

        :param start_day_of_weekend: The start_day_of_weekend of this SchedulingSettingsRequest.
        :type: str
        """
        allowed_values = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        if start_day_of_weekend.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for start_day_of_weekend -> " + start_day_of_weekend)
            self._start_day_of_weekend = "outdated_sdk_version"
        else:
            self._start_day_of_weekend = start_day_of_weekend

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

