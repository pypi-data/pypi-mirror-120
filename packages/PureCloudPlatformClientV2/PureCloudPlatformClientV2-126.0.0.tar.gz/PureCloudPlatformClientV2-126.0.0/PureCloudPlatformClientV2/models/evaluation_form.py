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

class EvaluationForm(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        EvaluationForm - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'modified_date': 'datetime',
            'published': 'bool',
            'context_id': 'str',
            'question_groups': 'list[EvaluationQuestionGroup]',
            'published_versions': 'DomainEntityListingEvaluationForm',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'modified_date': 'modifiedDate',
            'published': 'published',
            'context_id': 'contextId',
            'question_groups': 'questionGroups',
            'published_versions': 'publishedVersions',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._modified_date = None
        self._published = None
        self._context_id = None
        self._question_groups = None
        self._published_versions = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this EvaluationForm.
        The globally unique identifier for the object.

        :return: The id of this EvaluationForm.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this EvaluationForm.
        The globally unique identifier for the object.

        :param id: The id of this EvaluationForm.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this EvaluationForm.
        The evaluation form name

        :return: The name of this EvaluationForm.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this EvaluationForm.
        The evaluation form name

        :param name: The name of this EvaluationForm.
        :type: str
        """
        
        self._name = name

    @property
    def modified_date(self):
        """
        Gets the modified_date of this EvaluationForm.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The modified_date of this EvaluationForm.
        :rtype: datetime
        """
        return self._modified_date

    @modified_date.setter
    def modified_date(self, modified_date):
        """
        Sets the modified_date of this EvaluationForm.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param modified_date: The modified_date of this EvaluationForm.
        :type: datetime
        """
        
        self._modified_date = modified_date

    @property
    def published(self):
        """
        Gets the published of this EvaluationForm.


        :return: The published of this EvaluationForm.
        :rtype: bool
        """
        return self._published

    @published.setter
    def published(self, published):
        """
        Sets the published of this EvaluationForm.


        :param published: The published of this EvaluationForm.
        :type: bool
        """
        
        self._published = published

    @property
    def context_id(self):
        """
        Gets the context_id of this EvaluationForm.


        :return: The context_id of this EvaluationForm.
        :rtype: str
        """
        return self._context_id

    @context_id.setter
    def context_id(self, context_id):
        """
        Sets the context_id of this EvaluationForm.


        :param context_id: The context_id of this EvaluationForm.
        :type: str
        """
        
        self._context_id = context_id

    @property
    def question_groups(self):
        """
        Gets the question_groups of this EvaluationForm.
        A list of question groups

        :return: The question_groups of this EvaluationForm.
        :rtype: list[EvaluationQuestionGroup]
        """
        return self._question_groups

    @question_groups.setter
    def question_groups(self, question_groups):
        """
        Sets the question_groups of this EvaluationForm.
        A list of question groups

        :param question_groups: The question_groups of this EvaluationForm.
        :type: list[EvaluationQuestionGroup]
        """
        
        self._question_groups = question_groups

    @property
    def published_versions(self):
        """
        Gets the published_versions of this EvaluationForm.


        :return: The published_versions of this EvaluationForm.
        :rtype: DomainEntityListingEvaluationForm
        """
        return self._published_versions

    @published_versions.setter
    def published_versions(self, published_versions):
        """
        Sets the published_versions of this EvaluationForm.


        :param published_versions: The published_versions of this EvaluationForm.
        :type: DomainEntityListingEvaluationForm
        """
        
        self._published_versions = published_versions

    @property
    def self_uri(self):
        """
        Gets the self_uri of this EvaluationForm.
        The URI for this object

        :return: The self_uri of this EvaluationForm.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this EvaluationForm.
        The URI for this object

        :param self_uri: The self_uri of this EvaluationForm.
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

