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

class FlowDivisionView(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        FlowDivisionView - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'division': 'WritableDivision',
            'type': 'str',
            'input_schema': 'JsonSchemaDocument',
            'output_schema': 'JsonSchemaDocument',
            'published_version': 'FlowVersion',
            'debug_version': 'FlowVersion',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'division': 'division',
            'type': 'type',
            'input_schema': 'inputSchema',
            'output_schema': 'outputSchema',
            'published_version': 'publishedVersion',
            'debug_version': 'debugVersion',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._division = None
        self._type = None
        self._input_schema = None
        self._output_schema = None
        self._published_version = None
        self._debug_version = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this FlowDivisionView.
        The flow identifier

        :return: The id of this FlowDivisionView.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this FlowDivisionView.
        The flow identifier

        :param id: The id of this FlowDivisionView.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this FlowDivisionView.
        The flow name

        :return: The name of this FlowDivisionView.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this FlowDivisionView.
        The flow name

        :param name: The name of this FlowDivisionView.
        :type: str
        """
        
        self._name = name

    @property
    def division(self):
        """
        Gets the division of this FlowDivisionView.
        The division to which this entity belongs.

        :return: The division of this FlowDivisionView.
        :rtype: WritableDivision
        """
        return self._division

    @division.setter
    def division(self, division):
        """
        Sets the division of this FlowDivisionView.
        The division to which this entity belongs.

        :param division: The division of this FlowDivisionView.
        :type: WritableDivision
        """
        
        self._division = division

    @property
    def type(self):
        """
        Gets the type of this FlowDivisionView.


        :return: The type of this FlowDivisionView.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this FlowDivisionView.


        :param type: The type of this FlowDivisionView.
        :type: str
        """
        allowed_values = ["BOT", "COMMONMODULE", "INBOUNDCALL", "INBOUNDCHAT", "INBOUNDEMAIL", "INBOUNDSHORTMESSAGE", "INQUEUECALL", "INQUEUEEMAIL", "INQUEUESHORTMESSAGE", "OUTBOUNDCALL", "SECURECALL", "SPEECH", "SURVEYINVITE", "VOICEMAIL", "WORKFLOW", "WORKITEM"]
        if type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for type -> " + type)
            self._type = "outdated_sdk_version"
        else:
            self._type = type

    @property
    def input_schema(self):
        """
        Gets the input_schema of this FlowDivisionView.
        json schema describing the inputs for the flow

        :return: The input_schema of this FlowDivisionView.
        :rtype: JsonSchemaDocument
        """
        return self._input_schema

    @input_schema.setter
    def input_schema(self, input_schema):
        """
        Sets the input_schema of this FlowDivisionView.
        json schema describing the inputs for the flow

        :param input_schema: The input_schema of this FlowDivisionView.
        :type: JsonSchemaDocument
        """
        
        self._input_schema = input_schema

    @property
    def output_schema(self):
        """
        Gets the output_schema of this FlowDivisionView.
        json schema describing the outputs for the flow

        :return: The output_schema of this FlowDivisionView.
        :rtype: JsonSchemaDocument
        """
        return self._output_schema

    @output_schema.setter
    def output_schema(self, output_schema):
        """
        Sets the output_schema of this FlowDivisionView.
        json schema describing the outputs for the flow

        :param output_schema: The output_schema of this FlowDivisionView.
        :type: JsonSchemaDocument
        """
        
        self._output_schema = output_schema

    @property
    def published_version(self):
        """
        Gets the published_version of this FlowDivisionView.
        published version information if there is a published version

        :return: The published_version of this FlowDivisionView.
        :rtype: FlowVersion
        """
        return self._published_version

    @published_version.setter
    def published_version(self, published_version):
        """
        Sets the published_version of this FlowDivisionView.
        published version information if there is a published version

        :param published_version: The published_version of this FlowDivisionView.
        :type: FlowVersion
        """
        
        self._published_version = published_version

    @property
    def debug_version(self):
        """
        Gets the debug_version of this FlowDivisionView.
        debug version information if there is a debug version

        :return: The debug_version of this FlowDivisionView.
        :rtype: FlowVersion
        """
        return self._debug_version

    @debug_version.setter
    def debug_version(self, debug_version):
        """
        Sets the debug_version of this FlowDivisionView.
        debug version information if there is a debug version

        :param debug_version: The debug_version of this FlowDivisionView.
        :type: FlowVersion
        """
        
        self._debug_version = debug_version

    @property
    def self_uri(self):
        """
        Gets the self_uri of this FlowDivisionView.
        The URI for this object

        :return: The self_uri of this FlowDivisionView.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this FlowDivisionView.
        The URI for this object

        :param self_uri: The self_uri of this FlowDivisionView.
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

