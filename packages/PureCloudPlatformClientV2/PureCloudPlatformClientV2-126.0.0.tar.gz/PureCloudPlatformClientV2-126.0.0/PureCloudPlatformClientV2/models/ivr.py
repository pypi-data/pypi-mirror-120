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

class IVR(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        IVR - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'description': 'str',
            'version': 'int',
            'date_created': 'datetime',
            'date_modified': 'datetime',
            'modified_by': 'str',
            'created_by': 'str',
            'state': 'str',
            'modified_by_app': 'str',
            'created_by_app': 'str',
            'dnis': 'list[str]',
            'open_hours_flow': 'DomainEntityRef',
            'closed_hours_flow': 'DomainEntityRef',
            'holiday_hours_flow': 'DomainEntityRef',
            'schedule_group': 'DomainEntityRef',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'description': 'description',
            'version': 'version',
            'date_created': 'dateCreated',
            'date_modified': 'dateModified',
            'modified_by': 'modifiedBy',
            'created_by': 'createdBy',
            'state': 'state',
            'modified_by_app': 'modifiedByApp',
            'created_by_app': 'createdByApp',
            'dnis': 'dnis',
            'open_hours_flow': 'openHoursFlow',
            'closed_hours_flow': 'closedHoursFlow',
            'holiday_hours_flow': 'holidayHoursFlow',
            'schedule_group': 'scheduleGroup',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._description = None
        self._version = None
        self._date_created = None
        self._date_modified = None
        self._modified_by = None
        self._created_by = None
        self._state = None
        self._modified_by_app = None
        self._created_by_app = None
        self._dnis = None
        self._open_hours_flow = None
        self._closed_hours_flow = None
        self._holiday_hours_flow = None
        self._schedule_group = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this IVR.
        The globally unique identifier for the object.

        :return: The id of this IVR.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this IVR.
        The globally unique identifier for the object.

        :param id: The id of this IVR.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this IVR.
        The name of the entity.

        :return: The name of this IVR.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this IVR.
        The name of the entity.

        :param name: The name of this IVR.
        :type: str
        """
        
        self._name = name

    @property
    def description(self):
        """
        Gets the description of this IVR.
        The resource's description.

        :return: The description of this IVR.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this IVR.
        The resource's description.

        :param description: The description of this IVR.
        :type: str
        """
        
        self._description = description

    @property
    def version(self):
        """
        Gets the version of this IVR.
        The current version of the resource.

        :return: The version of this IVR.
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this IVR.
        The current version of the resource.

        :param version: The version of this IVR.
        :type: int
        """
        
        self._version = version

    @property
    def date_created(self):
        """
        Gets the date_created of this IVR.
        The date the resource was created. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The date_created of this IVR.
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """
        Sets the date_created of this IVR.
        The date the resource was created. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param date_created: The date_created of this IVR.
        :type: datetime
        """
        
        self._date_created = date_created

    @property
    def date_modified(self):
        """
        Gets the date_modified of this IVR.
        The date of the last modification to the resource. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The date_modified of this IVR.
        :rtype: datetime
        """
        return self._date_modified

    @date_modified.setter
    def date_modified(self, date_modified):
        """
        Sets the date_modified of this IVR.
        The date of the last modification to the resource. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param date_modified: The date_modified of this IVR.
        :type: datetime
        """
        
        self._date_modified = date_modified

    @property
    def modified_by(self):
        """
        Gets the modified_by of this IVR.
        The ID of the user that last modified the resource.

        :return: The modified_by of this IVR.
        :rtype: str
        """
        return self._modified_by

    @modified_by.setter
    def modified_by(self, modified_by):
        """
        Sets the modified_by of this IVR.
        The ID of the user that last modified the resource.

        :param modified_by: The modified_by of this IVR.
        :type: str
        """
        
        self._modified_by = modified_by

    @property
    def created_by(self):
        """
        Gets the created_by of this IVR.
        The ID of the user that created the resource.

        :return: The created_by of this IVR.
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """
        Sets the created_by of this IVR.
        The ID of the user that created the resource.

        :param created_by: The created_by of this IVR.
        :type: str
        """
        
        self._created_by = created_by

    @property
    def state(self):
        """
        Gets the state of this IVR.
        Indicates if the resource is active, inactive, or deleted.

        :return: The state of this IVR.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this IVR.
        Indicates if the resource is active, inactive, or deleted.

        :param state: The state of this IVR.
        :type: str
        """
        allowed_values = ["active", "inactive", "deleted"]
        if state.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for state -> " + state)
            self._state = "outdated_sdk_version"
        else:
            self._state = state

    @property
    def modified_by_app(self):
        """
        Gets the modified_by_app of this IVR.
        The application that last modified the resource.

        :return: The modified_by_app of this IVR.
        :rtype: str
        """
        return self._modified_by_app

    @modified_by_app.setter
    def modified_by_app(self, modified_by_app):
        """
        Sets the modified_by_app of this IVR.
        The application that last modified the resource.

        :param modified_by_app: The modified_by_app of this IVR.
        :type: str
        """
        
        self._modified_by_app = modified_by_app

    @property
    def created_by_app(self):
        """
        Gets the created_by_app of this IVR.
        The application that created the resource.

        :return: The created_by_app of this IVR.
        :rtype: str
        """
        return self._created_by_app

    @created_by_app.setter
    def created_by_app(self, created_by_app):
        """
        Sets the created_by_app of this IVR.
        The application that created the resource.

        :param created_by_app: The created_by_app of this IVR.
        :type: str
        """
        
        self._created_by_app = created_by_app

    @property
    def dnis(self):
        """
        Gets the dnis of this IVR.
        The phone number(s) to contact the IVR by.  Each phone number must be unique and not in use by another resource.  For example, a user and an iVR cannot have the same phone number.

        :return: The dnis of this IVR.
        :rtype: list[str]
        """
        return self._dnis

    @dnis.setter
    def dnis(self, dnis):
        """
        Sets the dnis of this IVR.
        The phone number(s) to contact the IVR by.  Each phone number must be unique and not in use by another resource.  For example, a user and an iVR cannot have the same phone number.

        :param dnis: The dnis of this IVR.
        :type: list[str]
        """
        
        self._dnis = dnis

    @property
    def open_hours_flow(self):
        """
        Gets the open_hours_flow of this IVR.
        The Architect flow to execute during the hours an organization is open.

        :return: The open_hours_flow of this IVR.
        :rtype: DomainEntityRef
        """
        return self._open_hours_flow

    @open_hours_flow.setter
    def open_hours_flow(self, open_hours_flow):
        """
        Sets the open_hours_flow of this IVR.
        The Architect flow to execute during the hours an organization is open.

        :param open_hours_flow: The open_hours_flow of this IVR.
        :type: DomainEntityRef
        """
        
        self._open_hours_flow = open_hours_flow

    @property
    def closed_hours_flow(self):
        """
        Gets the closed_hours_flow of this IVR.
        The Architect flow to execute during the hours an organization is closed.

        :return: The closed_hours_flow of this IVR.
        :rtype: DomainEntityRef
        """
        return self._closed_hours_flow

    @closed_hours_flow.setter
    def closed_hours_flow(self, closed_hours_flow):
        """
        Sets the closed_hours_flow of this IVR.
        The Architect flow to execute during the hours an organization is closed.

        :param closed_hours_flow: The closed_hours_flow of this IVR.
        :type: DomainEntityRef
        """
        
        self._closed_hours_flow = closed_hours_flow

    @property
    def holiday_hours_flow(self):
        """
        Gets the holiday_hours_flow of this IVR.
        The Architect flow to execute during an organization's holiday hours.

        :return: The holiday_hours_flow of this IVR.
        :rtype: DomainEntityRef
        """
        return self._holiday_hours_flow

    @holiday_hours_flow.setter
    def holiday_hours_flow(self, holiday_hours_flow):
        """
        Sets the holiday_hours_flow of this IVR.
        The Architect flow to execute during an organization's holiday hours.

        :param holiday_hours_flow: The holiday_hours_flow of this IVR.
        :type: DomainEntityRef
        """
        
        self._holiday_hours_flow = holiday_hours_flow

    @property
    def schedule_group(self):
        """
        Gets the schedule_group of this IVR.
        The schedule group defining the open and closed hours for an organization.  If this is provided, an open flow and a closed flow must be specified as well.

        :return: The schedule_group of this IVR.
        :rtype: DomainEntityRef
        """
        return self._schedule_group

    @schedule_group.setter
    def schedule_group(self, schedule_group):
        """
        Sets the schedule_group of this IVR.
        The schedule group defining the open and closed hours for an organization.  If this is provided, an open flow and a closed flow must be specified as well.

        :param schedule_group: The schedule_group of this IVR.
        :type: DomainEntityRef
        """
        
        self._schedule_group = schedule_group

    @property
    def self_uri(self):
        """
        Gets the self_uri of this IVR.
        The URI for this object

        :return: The self_uri of this IVR.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this IVR.
        The URI for this object

        :param self_uri: The self_uri of this IVR.
        :type: str
        """
        
        self._self_uri = self_uri

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

