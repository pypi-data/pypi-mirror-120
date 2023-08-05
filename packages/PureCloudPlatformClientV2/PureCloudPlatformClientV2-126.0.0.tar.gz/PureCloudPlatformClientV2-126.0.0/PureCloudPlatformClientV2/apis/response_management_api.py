# coding: utf-8

"""
ResponseManagementApi.py
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
"""

from __future__ import absolute_import

import sys
import os
import re

# python 2 and python 3 compatibility library
from six import iteritems

from ..configuration import Configuration
from ..api_client import ApiClient


class ResponseManagementApi(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        config = Configuration()
        if api_client:
            self.api_client = api_client
        else:
            if not config.api_client:
                config.api_client = ApiClient()
            self.api_client = config.api_client

    def delete_responsemanagement_library(self, library_id, **kwargs):
        """
        Delete an existing response library.
        This will remove any responses associated with the library.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.delete_responsemanagement_library(library_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str library_id: Library ID (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['library_id']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_responsemanagement_library" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'library_id' is set
        if ('library_id' not in params) or (params['library_id'] is None):
            raise ValueError("Missing the required parameter `library_id` when calling `delete_responsemanagement_library`")


        resource_path = '/api/v2/responsemanagement/libraries/{libraryId}'.replace('{format}', 'json')
        path_params = {}
        if 'library_id' in params:
            path_params['libraryId'] = params['library_id']

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'DELETE',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type=None,
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def delete_responsemanagement_response(self, response_id, **kwargs):
        """
        Delete an existing response.
        This will remove the response from any libraries associated with it.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.delete_responsemanagement_response(response_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str response_id: Response ID (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['response_id']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_responsemanagement_response" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'response_id' is set
        if ('response_id' not in params) or (params['response_id'] is None):
            raise ValueError("Missing the required parameter `response_id` when calling `delete_responsemanagement_response`")


        resource_path = '/api/v2/responsemanagement/responses/{responseId}'.replace('{format}', 'json')
        path_params = {}
        if 'response_id' in params:
            path_params['responseId'] = params['response_id']

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'DELETE',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type=None,
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def get_responsemanagement_libraries(self, **kwargs):
        """
        Gets a list of existing response libraries.
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_responsemanagement_libraries(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param int page_number: Page number
        :param int page_size: Page size
        :param str messaging_template_filter: Returns a list of libraries that contain responses with at least one messaging template defined for a specific message channel
        :return: LibraryEntityListing
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['page_number', 'page_size', 'messaging_template_filter']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_responsemanagement_libraries" % key
                )
            params[key] = val
        del params['kwargs']



        resource_path = '/api/v2/responsemanagement/libraries'.replace('{format}', 'json')
        path_params = {}

        query_params = {}
        if 'page_number' in params:
            query_params['pageNumber'] = params['page_number']
        if 'page_size' in params:
            query_params['pageSize'] = params['page_size']
        if 'messaging_template_filter' in params:
            query_params['messagingTemplateFilter'] = params['messaging_template_filter']

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='LibraryEntityListing',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def get_responsemanagement_library(self, library_id, **kwargs):
        """
        Get details about an existing response library.
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_responsemanagement_library(library_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str library_id: Library ID (required)
        :return: Library
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['library_id']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_responsemanagement_library" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'library_id' is set
        if ('library_id' not in params) or (params['library_id'] is None):
            raise ValueError("Missing the required parameter `library_id` when calling `get_responsemanagement_library`")


        resource_path = '/api/v2/responsemanagement/libraries/{libraryId}'.replace('{format}', 'json')
        path_params = {}
        if 'library_id' in params:
            path_params['libraryId'] = params['library_id']

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='Library',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def get_responsemanagement_response(self, response_id, **kwargs):
        """
        Get details about an existing response.
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_responsemanagement_response(response_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str response_id: Response ID (required)
        :param str expand: Expand instructions for the return value.
        :return: Response
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['response_id', 'expand']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_responsemanagement_response" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'response_id' is set
        if ('response_id' not in params) or (params['response_id'] is None):
            raise ValueError("Missing the required parameter `response_id` when calling `get_responsemanagement_response`")


        resource_path = '/api/v2/responsemanagement/responses/{responseId}'.replace('{format}', 'json')
        path_params = {}
        if 'response_id' in params:
            path_params['responseId'] = params['response_id']

        query_params = {}
        if 'expand' in params:
            query_params['expand'] = params['expand']

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='Response',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def get_responsemanagement_responses(self, library_id, **kwargs):
        """
        Gets a list of existing responses.
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_responsemanagement_responses(library_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str library_id: Library ID (required)
        :param int page_number: Page number
        :param int page_size: Page size
        :param str expand: Expand instructions for the return value.
        :return: ResponseEntityListing
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['library_id', 'page_number', 'page_size', 'expand']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_responsemanagement_responses" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'library_id' is set
        if ('library_id' not in params) or (params['library_id'] is None):
            raise ValueError("Missing the required parameter `library_id` when calling `get_responsemanagement_responses`")


        resource_path = '/api/v2/responsemanagement/responses'.replace('{format}', 'json')
        path_params = {}

        query_params = {}
        if 'library_id' in params:
            query_params['libraryId'] = params['library_id']
        if 'page_number' in params:
            query_params['pageNumber'] = params['page_number']
        if 'page_size' in params:
            query_params['pageSize'] = params['page_size']
        if 'expand' in params:
            query_params['expand'] = params['expand']

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='ResponseEntityListing',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def post_responsemanagement_libraries(self, body, **kwargs):
        """
        Create a response library.
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.post_responsemanagement_libraries(body, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param Library body: Library (required)
        :return: Library
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_responsemanagement_libraries" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'body' is set
        if ('body' not in params) or (params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `post_responsemanagement_libraries`")


        resource_path = '/api/v2/responsemanagement/libraries'.replace('{format}', 'json')
        path_params = {}

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'POST',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='Library',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def post_responsemanagement_responses(self, body, **kwargs):
        """
        Create a response.
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.post_responsemanagement_responses(body, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param Response body: Response (required)
        :param str expand: Expand instructions for the return value.
        :return: Response
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'expand']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_responsemanagement_responses" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'body' is set
        if ('body' not in params) or (params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `post_responsemanagement_responses`")


        resource_path = '/api/v2/responsemanagement/responses'.replace('{format}', 'json')
        path_params = {}

        query_params = {}
        if 'expand' in params:
            query_params['expand'] = params['expand']

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'POST',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='Response',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def post_responsemanagement_responses_query(self, body, **kwargs):
        """
        Query responses
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.post_responsemanagement_responses_query(body, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param ResponseQueryRequest body: Response (required)
        :return: ResponseQueryResults
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_responsemanagement_responses_query" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'body' is set
        if ('body' not in params) or (params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `post_responsemanagement_responses_query`")


        resource_path = '/api/v2/responsemanagement/responses/query'.replace('{format}', 'json')
        path_params = {}

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'POST',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='ResponseQueryResults',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def put_responsemanagement_library(self, library_id, body, **kwargs):
        """
        Update an existing response library.
        Fields that can be updated: name. The most recent version is required for updates.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.put_responsemanagement_library(library_id, body, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str library_id: Library ID (required)
        :param Library body: Library (required)
        :return: Library
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['library_id', 'body']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method put_responsemanagement_library" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'library_id' is set
        if ('library_id' not in params) or (params['library_id'] is None):
            raise ValueError("Missing the required parameter `library_id` when calling `put_responsemanagement_library`")
        # verify the required parameter 'body' is set
        if ('body' not in params) or (params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `put_responsemanagement_library`")


        resource_path = '/api/v2/responsemanagement/libraries/{libraryId}'.replace('{format}', 'json')
        path_params = {}
        if 'library_id' in params:
            path_params['libraryId'] = params['library_id']

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'PUT',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='Library',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def put_responsemanagement_response(self, response_id, body, **kwargs):
        """
        Update an existing response.
        Fields that can be updated: name, libraries, and texts. The most recent version is required for updates.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.put_responsemanagement_response(response_id, body, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str response_id: Response ID (required)
        :param Response body: Response (required)
        :param str expand: Expand instructions for the return value.
        :return: Response
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['response_id', 'body', 'expand']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method put_responsemanagement_response" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'response_id' is set
        if ('response_id' not in params) or (params['response_id'] is None):
            raise ValueError("Missing the required parameter `response_id` when calling `put_responsemanagement_response`")
        # verify the required parameter 'body' is set
        if ('body' not in params) or (params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `put_responsemanagement_response`")


        resource_path = '/api/v2/responsemanagement/responses/{responseId}'.replace('{format}', 'json')
        path_params = {}
        if 'response_id' in params:
            path_params['responseId'] = params['response_id']

        query_params = {}
        if 'expand' in params:
            query_params['expand'] = params['expand']

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'PUT',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='Response',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response
