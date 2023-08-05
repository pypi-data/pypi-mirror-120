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

class CreateAdminTimeOffRequest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        CreateAdminTimeOffRequest - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'status': 'str',
            'users': 'list[UserReference]',
            'activity_code_id': 'str',
            'notes': 'str',
            'full_day_management_unit_dates': 'list[str]',
            'partial_day_start_date_times': 'list[datetime]',
            'daily_duration_minutes': 'int'
        }

        self.attribute_map = {
            'status': 'status',
            'users': 'users',
            'activity_code_id': 'activityCodeId',
            'notes': 'notes',
            'full_day_management_unit_dates': 'fullDayManagementUnitDates',
            'partial_day_start_date_times': 'partialDayStartDateTimes',
            'daily_duration_minutes': 'dailyDurationMinutes'
        }

        self._status = None
        self._users = None
        self._activity_code_id = None
        self._notes = None
        self._full_day_management_unit_dates = None
        self._partial_day_start_date_times = None
        self._daily_duration_minutes = None

    @property
    def status(self):
        """
        Gets the status of this CreateAdminTimeOffRequest.
        The status of this time off request

        :return: The status of this CreateAdminTimeOffRequest.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this CreateAdminTimeOffRequest.
        The status of this time off request

        :param status: The status of this CreateAdminTimeOffRequest.
        :type: str
        """
        allowed_values = ["PENDING", "APPROVED"]
        if status.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for status -> " + status)
            self._status = "outdated_sdk_version"
        else:
            self._status = status

    @property
    def users(self):
        """
        Gets the users of this CreateAdminTimeOffRequest.
        A set of IDs for users to associate with this time off request

        :return: The users of this CreateAdminTimeOffRequest.
        :rtype: list[UserReference]
        """
        return self._users

    @users.setter
    def users(self, users):
        """
        Sets the users of this CreateAdminTimeOffRequest.
        A set of IDs for users to associate with this time off request

        :param users: The users of this CreateAdminTimeOffRequest.
        :type: list[UserReference]
        """
        
        self._users = users

    @property
    def activity_code_id(self):
        """
        Gets the activity_code_id of this CreateAdminTimeOffRequest.
        The ID of the activity code associated with this time off request. Activity code must be of the TimeOff category

        :return: The activity_code_id of this CreateAdminTimeOffRequest.
        :rtype: str
        """
        return self._activity_code_id

    @activity_code_id.setter
    def activity_code_id(self, activity_code_id):
        """
        Sets the activity_code_id of this CreateAdminTimeOffRequest.
        The ID of the activity code associated with this time off request. Activity code must be of the TimeOff category

        :param activity_code_id: The activity_code_id of this CreateAdminTimeOffRequest.
        :type: str
        """
        
        self._activity_code_id = activity_code_id

    @property
    def notes(self):
        """
        Gets the notes of this CreateAdminTimeOffRequest.
        Notes about the time off request

        :return: The notes of this CreateAdminTimeOffRequest.
        :rtype: str
        """
        return self._notes

    @notes.setter
    def notes(self, notes):
        """
        Sets the notes of this CreateAdminTimeOffRequest.
        Notes about the time off request

        :param notes: The notes of this CreateAdminTimeOffRequest.
        :type: str
        """
        
        self._notes = notes

    @property
    def full_day_management_unit_dates(self):
        """
        Gets the full_day_management_unit_dates of this CreateAdminTimeOffRequest.
        A set of dates in yyyy-MM-dd format.  Should be interpreted in the management unit's configured time zone.

        :return: The full_day_management_unit_dates of this CreateAdminTimeOffRequest.
        :rtype: list[str]
        """
        return self._full_day_management_unit_dates

    @full_day_management_unit_dates.setter
    def full_day_management_unit_dates(self, full_day_management_unit_dates):
        """
        Sets the full_day_management_unit_dates of this CreateAdminTimeOffRequest.
        A set of dates in yyyy-MM-dd format.  Should be interpreted in the management unit's configured time zone.

        :param full_day_management_unit_dates: The full_day_management_unit_dates of this CreateAdminTimeOffRequest.
        :type: list[str]
        """
        
        self._full_day_management_unit_dates = full_day_management_unit_dates

    @property
    def partial_day_start_date_times(self):
        """
        Gets the partial_day_start_date_times of this CreateAdminTimeOffRequest.
        A set of start date-times in ISO-8601 format for partial day requests.

        :return: The partial_day_start_date_times of this CreateAdminTimeOffRequest.
        :rtype: list[datetime]
        """
        return self._partial_day_start_date_times

    @partial_day_start_date_times.setter
    def partial_day_start_date_times(self, partial_day_start_date_times):
        """
        Sets the partial_day_start_date_times of this CreateAdminTimeOffRequest.
        A set of start date-times in ISO-8601 format for partial day requests.

        :param partial_day_start_date_times: The partial_day_start_date_times of this CreateAdminTimeOffRequest.
        :type: list[datetime]
        """
        
        self._partial_day_start_date_times = partial_day_start_date_times

    @property
    def daily_duration_minutes(self):
        """
        Gets the daily_duration_minutes of this CreateAdminTimeOffRequest.
        The daily duration of this time off request in minutes

        :return: The daily_duration_minutes of this CreateAdminTimeOffRequest.
        :rtype: int
        """
        return self._daily_duration_minutes

    @daily_duration_minutes.setter
    def daily_duration_minutes(self, daily_duration_minutes):
        """
        Sets the daily_duration_minutes of this CreateAdminTimeOffRequest.
        The daily duration of this time off request in minutes

        :param daily_duration_minutes: The daily_duration_minutes of this CreateAdminTimeOffRequest.
        :type: int
        """
        
        self._daily_duration_minutes = daily_duration_minutes

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

