# coding: utf-8

"""
    Flywheel

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 8.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from flywheel.api_client import ApiClient
import flywheel.models

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.

class DevicesApi(object):
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create_device(self, body, **kwargs):  # noqa: E501
        """Create a new device.

        Will create a new device record together with an api key. Request must be an admin request. 
        This method makes a synchronous HTTP request by default.

        :param Device body: (required)
        :param bool async_: Perform the request asynchronously
        :return: object
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_'):
            return self.create_device_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.create_device_with_http_info(body, **kwargs)  # noqa: E501
            if data and hasattr(data, 'return_value'):
                return data.return_value()
            return data


    def create_device_with_http_info(self, body, **kwargs):  # noqa: E501
        """Create a new device.

        Will create a new device record together with an api key. Request must be an admin request. 
        This method makes a synchronous HTTP request by default.

        :param Device body: (required)
        :param bool async: Perform the request asynchronously
        :return: object
        """

        all_params = ['body']  # noqa: E501
        all_params.append('async_')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        all_params.append('_request_out')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_device" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_device`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = flywheel.models.Device.positional_to_model(params['body'])
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKey']  # noqa: E501

        return self.api_client.call_api(
            '/devices', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='object',  # noqa: E501
            auth_settings=auth_settings,
            async_=params.get('async_'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            _request_out=params.get('_request_out'),
            collection_formats=collection_formats)

    def get_all_devices(self, **kwargs):  # noqa: E501
        """List all devices.

        Requires login.
        This method makes a synchronous HTTP request by default.

        :param bool async_: Perform the request asynchronously
        :return: list[Device]
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_'):
            return self.get_all_devices_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_all_devices_with_http_info(**kwargs)  # noqa: E501
            if data and hasattr(data, 'return_value'):
                return data.return_value()
            return data


    def get_all_devices_with_http_info(self, **kwargs):  # noqa: E501
        """List all devices.

        Requires login.
        This method makes a synchronous HTTP request by default.

        :param bool async: Perform the request asynchronously
        :return: list[Device]
        """

        all_params = []  # noqa: E501
        all_params.append('async_')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        all_params.append('_request_out')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_all_devices" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKey']  # noqa: E501

        return self.api_client.call_api(
            '/devices', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[Device]',  # noqa: E501
            auth_settings=auth_settings,
            async_=params.get('async_'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            _request_out=params.get('_request_out'),
            collection_formats=collection_formats)

    def get_all_devices_status(self, **kwargs):  # noqa: E501
        """Get status for all known devices.

        ok - missing - error - unknown
        This method makes a synchronous HTTP request by default.

        :param bool async_: Perform the request asynchronously
        :return: DeviceStatus
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_'):
            return self.get_all_devices_status_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_all_devices_status_with_http_info(**kwargs)  # noqa: E501
            if data and hasattr(data, 'return_value'):
                return data.return_value()
            return data


    def get_all_devices_status_with_http_info(self, **kwargs):  # noqa: E501
        """Get status for all known devices.

        ok - missing - error - unknown
        This method makes a synchronous HTTP request by default.

        :param bool async: Perform the request asynchronously
        :return: DeviceStatus
        """

        all_params = []  # noqa: E501
        all_params.append('async_')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        all_params.append('_request_out')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_all_devices_status" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKey']  # noqa: E501

        return self.api_client.call_api(
            '/devices/status', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DeviceStatus',  # noqa: E501
            auth_settings=auth_settings,
            async_=params.get('async_'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            _request_out=params.get('_request_out'),
            collection_formats=collection_formats)

    def get_device(self, device_id, **kwargs):  # noqa: E501
        """Get device details

        This method makes a synchronous HTTP request by default.

        :param str device_id: (required)
        :param bool async_: Perform the request asynchronously
        :return: Device
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_'):
            return self.get_device_with_http_info(device_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_device_with_http_info(device_id, **kwargs)  # noqa: E501
            if data and hasattr(data, 'return_value'):
                return data.return_value()
            return data


    def get_device_with_http_info(self, device_id, **kwargs):  # noqa: E501
        """Get device details

        This method makes a synchronous HTTP request by default.

        :param str device_id: (required)
        :param bool async: Perform the request asynchronously
        :return: Device
        """

        all_params = ['device_id']  # noqa: E501
        all_params.append('async_')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        all_params.append('_request_out')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_device" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'device_id' is set
        if ('device_id' not in params or
                params['device_id'] is None):
            raise ValueError("Missing the required parameter `device_id` when calling `get_device`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'device_id' in params:
            path_params['DeviceId'] = params['device_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKey']  # noqa: E501

        return self.api_client.call_api(
            '/devices/{DeviceId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Device',  # noqa: E501
            auth_settings=auth_settings,
            async_=params.get('async_'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            _request_out=params.get('_request_out'),
            collection_formats=collection_formats)

    def modify_device(self, device_id, body, **kwargs):  # noqa: E501
        """Update a device

        This method makes a synchronous HTTP request by default.

        :param str device_id: (required)
        :param Device body: (required)
        :param bool async_: Perform the request asynchronously
        :return: None
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_'):
            return self.modify_device_with_http_info(device_id, body, **kwargs)  # noqa: E501
        else:
            (data) = self.modify_device_with_http_info(device_id, body, **kwargs)  # noqa: E501
            if data and hasattr(data, 'return_value'):
                return data.return_value()
            return data


    def modify_device_with_http_info(self, device_id, body, **kwargs):  # noqa: E501
        """Update a device

        This method makes a synchronous HTTP request by default.

        :param str device_id: (required)
        :param Device body: (required)
        :param bool async: Perform the request asynchronously
        :return: None
        """

        all_params = ['device_id', 'body']  # noqa: E501
        all_params.append('async_')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        all_params.append('_request_out')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method modify_device" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'device_id' is set
        if ('device_id' not in params or
                params['device_id'] is None):
            raise ValueError("Missing the required parameter `device_id` when calling `modify_device`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `modify_device`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'device_id' in params:
            path_params['DeviceId'] = params['device_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = flywheel.models.Device.positional_to_model(params['body'])
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKey']  # noqa: E501

        return self.api_client.call_api(
            '/devices/{DeviceId}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_=params.get('async_'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            _request_out=params.get('_request_out'),
            collection_formats=collection_formats)

    def regenerate_key(self, device_id, **kwargs):  # noqa: E501
        """Regenerate device API key

        This method makes a synchronous HTTP request by default.

        :param str device_id: (required)
        :param bool async_: Perform the request asynchronously
        :return: InlineResponse2001
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_'):
            return self.regenerate_key_with_http_info(device_id, **kwargs)  # noqa: E501
        else:
            (data) = self.regenerate_key_with_http_info(device_id, **kwargs)  # noqa: E501
            if data and hasattr(data, 'return_value'):
                return data.return_value()
            return data


    def regenerate_key_with_http_info(self, device_id, **kwargs):  # noqa: E501
        """Regenerate device API key

        This method makes a synchronous HTTP request by default.

        :param str device_id: (required)
        :param bool async: Perform the request asynchronously
        :return: InlineResponse2001
        """

        all_params = ['device_id']  # noqa: E501
        all_params.append('async_')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        all_params.append('_request_out')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method regenerate_key" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'device_id' is set
        if ('device_id' not in params or
                params['device_id'] is None):
            raise ValueError("Missing the required parameter `device_id` when calling `regenerate_key`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'device_id' in params:
            path_params['DeviceId'] = params['device_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKey']  # noqa: E501

        return self.api_client.call_api(
            '/devices/{DeviceId}/key', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse2001',  # noqa: E501
            auth_settings=auth_settings,
            async_=params.get('async_'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            _request_out=params.get('_request_out'),
            collection_formats=collection_formats)

    def update_device(self, body, **kwargs):  # noqa: E501
        """Modify a device&#39;s type, name, interval, info or set errors.

        Will modify the device record of the device making the request. Type may only be set once if not already specified at creation. Request must be a drone request. 
        This method makes a synchronous HTTP request by default.

        :param Device body: (required)
        :param bool async_: Perform the request asynchronously
        :return: Device
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_'):
            return self.update_device_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.update_device_with_http_info(body, **kwargs)  # noqa: E501
            if data and hasattr(data, 'return_value'):
                return data.return_value()
            return data


    def update_device_with_http_info(self, body, **kwargs):  # noqa: E501
        """Modify a device&#39;s type, name, interval, info or set errors.

        Will modify the device record of the device making the request. Type may only be set once if not already specified at creation. Request must be a drone request. 
        This method makes a synchronous HTTP request by default.

        :param Device body: (required)
        :param bool async: Perform the request asynchronously
        :return: Device
        """

        all_params = ['body']  # noqa: E501
        all_params.append('async_')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        all_params.append('_request_out')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_device" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `update_device`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = flywheel.models.Device.positional_to_model(params['body'])
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKey']  # noqa: E501

        return self.api_client.call_api(
            '/devices/self', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Device',  # noqa: E501
            auth_settings=auth_settings,
            async_=params.get('async_'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            _request_out=params.get('_request_out'),
            collection_formats=collection_formats)
