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

class TokenInfo(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        TokenInfo - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'organization': 'NamedEntity',
            'home_organization': 'NamedEntity',
            'authorized_scope': 'list[str]',
            'cloned_user': 'TokenInfoClonedUser',
            'o_auth_client': 'OrgOAuthClient'
        }

        self.attribute_map = {
            'organization': 'organization',
            'home_organization': 'homeOrganization',
            'authorized_scope': 'authorizedScope',
            'cloned_user': 'clonedUser',
            'o_auth_client': 'OAuthClient'
        }

        self._organization = None
        self._home_organization = None
        self._authorized_scope = None
        self._cloned_user = None
        self._o_auth_client = None

    @property
    def organization(self):
        """
        Gets the organization of this TokenInfo.
        The current organization

        :return: The organization of this TokenInfo.
        :rtype: NamedEntity
        """
        return self._organization

    @organization.setter
    def organization(self, organization):
        """
        Sets the organization of this TokenInfo.
        The current organization

        :param organization: The organization of this TokenInfo.
        :type: NamedEntity
        """
        
        self._organization = organization

    @property
    def home_organization(self):
        """
        Gets the home_organization of this TokenInfo.
        The token's home organization

        :return: The home_organization of this TokenInfo.
        :rtype: NamedEntity
        """
        return self._home_organization

    @home_organization.setter
    def home_organization(self, home_organization):
        """
        Sets the home_organization of this TokenInfo.
        The token's home organization

        :param home_organization: The home_organization of this TokenInfo.
        :type: NamedEntity
        """
        
        self._home_organization = home_organization

    @property
    def authorized_scope(self):
        """
        Gets the authorized_scope of this TokenInfo.
        The list of scopes authorized for the OAuth client

        :return: The authorized_scope of this TokenInfo.
        :rtype: list[str]
        """
        return self._authorized_scope

    @authorized_scope.setter
    def authorized_scope(self, authorized_scope):
        """
        Sets the authorized_scope of this TokenInfo.
        The list of scopes authorized for the OAuth client

        :param authorized_scope: The authorized_scope of this TokenInfo.
        :type: list[str]
        """
        
        self._authorized_scope = authorized_scope

    @property
    def cloned_user(self):
        """
        Gets the cloned_user of this TokenInfo.
        Only present when a user is a clone of trustee user in the trustor org.

        :return: The cloned_user of this TokenInfo.
        :rtype: TokenInfoClonedUser
        """
        return self._cloned_user

    @cloned_user.setter
    def cloned_user(self, cloned_user):
        """
        Sets the cloned_user of this TokenInfo.
        Only present when a user is a clone of trustee user in the trustor org.

        :param cloned_user: The cloned_user of this TokenInfo.
        :type: TokenInfoClonedUser
        """
        
        self._cloned_user = cloned_user

    @property
    def o_auth_client(self):
        """
        Gets the o_auth_client of this TokenInfo.


        :return: The o_auth_client of this TokenInfo.
        :rtype: OrgOAuthClient
        """
        return self._o_auth_client

    @o_auth_client.setter
    def o_auth_client(self, o_auth_client):
        """
        Sets the o_auth_client of this TokenInfo.


        :param o_auth_client: The o_auth_client of this TokenInfo.
        :type: OrgOAuthClient
        """
        
        self._o_auth_client = o_auth_client

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

