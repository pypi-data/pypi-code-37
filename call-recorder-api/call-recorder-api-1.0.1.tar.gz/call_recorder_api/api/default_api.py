# coding: utf-8

"""
    Call Recorder API

    Call Recorder API   # noqa: E501

    OpenAPI spec version: 1.0.0
    
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six
import json

from call_recorder_api.api_client import ApiClient


class DefaultApi(object):
    """NOTE: 

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def buy_credits_post(self, api_key, amount, receipt, product_id, device_type, **kwargs):  # noqa: E501
        """buy_credits_post  # noqa: E501

        Buy Credits   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.buy_credits_post(api_key, amount, receipt, product_id, device_type, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param int amount: (required)
        :param str receipt: (required)
        :param int product_id: (required)
        :param DeviceType device_type: (required)
        :return: BuyCreditsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.buy_credits_post_with_http_info(api_key, amount, receipt, product_id, device_type, **kwargs)  # noqa: E501
        else:
            (data) = self.buy_credits_post_with_http_info(api_key, amount, receipt, product_id, device_type, **kwargs)  # noqa: E501
            return data

    def buy_credits_post_with_http_info(self, api_key, amount, receipt, product_id, device_type, **kwargs):  # noqa: E501
        """buy_credits_post  # noqa: E501

        Buy Credits   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.buy_credits_post_with_http_info(api_key, amount, receipt, product_id, device_type, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param int amount: (required)
        :param str receipt: (required)
        :param int product_id: (required)
        :param DeviceType device_type: (required)
        :return: BuyCreditsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key', 'amount', 'receipt', 'product_id', 'device_type']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method buy_credits_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `buy_credits_post`")  # noqa: E501
        # verify the required parameter 'amount' is set
        if ('amount' not in params or
                params['amount'] is None):
            raise ValueError("Missing the required parameter `amount` when calling `buy_credits_post`")  # noqa: E501
        # verify the required parameter 'receipt' is set
        if ('receipt' not in params or
                params['receipt'] is None):
            raise ValueError("Missing the required parameter `receipt` when calling `buy_credits_post`")  # noqa: E501
        # verify the required parameter 'product_id' is set
        if ('product_id' not in params or
                params['product_id'] is None):
            raise ValueError("Missing the required parameter `product_id` when calling `buy_credits_post`")  # noqa: E501
        # verify the required parameter 'device_type' is set
        if ('device_type' not in params or
                params['device_type'] is None):
            raise ValueError("Missing the required parameter `device_type` when calling `buy_credits_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501
        if 'amount' in params:
            form_params.append(('amount', params['amount']))  # noqa: E501
        if 'receipt' in params:
            form_params.append(('receipt', params['receipt']))  # noqa: E501
        if 'product_id' in params:
            form_params.append(('product_id', params['product_id']))  # noqa: E501
        if 'device_type' in params:
            form_params.append(('device_type', params['device_type']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/buy_credits', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='BuyCreditsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def clone_file_post(self, api_key, id, **kwargs):  # noqa: E501
        """clone_file_post  # noqa: E501

        Clone File   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.clone_file_post(api_key, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param int id: (required)
        :return: CloneFileResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.clone_file_post_with_http_info(api_key, id, **kwargs)  # noqa: E501
        else:
            (data) = self.clone_file_post_with_http_info(api_key, id, **kwargs)  # noqa: E501
            return data

    def clone_file_post_with_http_info(self, api_key, id, **kwargs):  # noqa: E501
        """clone_file_post  # noqa: E501

        Clone File   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.clone_file_post_with_http_info(api_key, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param int id: (required)
        :return: CloneFileResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key', 'id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method clone_file_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `clone_file_post`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `clone_file_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501
        if 'id' in params:
            form_params.append(('id', params['id']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/clone_file', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CloneFileResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_file_post(self, api_key, file, data, **kwargs):  # noqa: E501
        """create_file_post  # noqa: E501

        Create File   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_file_post(api_key, file, data, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param str file: (required)
        :param CreateFileData data: (required)
        :return: CreateFileResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_file_post_with_http_info(api_key, file, data, **kwargs)  # noqa: E501
        else:
            (data) = self.create_file_post_with_http_info(api_key, file, data, **kwargs)  # noqa: E501
            return data

    def create_file_post_with_http_info(self, api_key, file, data, **kwargs):  # noqa: E501
        """create_file_post  # noqa: E501

        Create File   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_file_post_with_http_info(api_key, file, data, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param str file: (required)
        :param CreateFileData data: (required)
        :return: CreateFileResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key', 'file', 'data']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_file_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `create_file_post`")  # noqa: E501
        # verify the required parameter 'file' is set
        if ('file' not in params or
                params['file'] is None):
            raise ValueError("Missing the required parameter `file` when calling `create_file_post`")  # noqa: E501
        # verify the required parameter 'data' is set
        if ('data' not in params or
                params['data'] is None):
            raise ValueError("Missing the required parameter `data` when calling `create_file_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501
        if 'file' in params:
            local_var_files['file'] = file
        if 'data' in params:
            create_file_data = params['data']
            json_create_file_data = {}
            if create_file_data.name:
                json_create_file_data['name'] = create_file_data.name
            if create_file_data.email:
                json_create_file_data['email'] = create_file_data.email
            if create_file_data.phone:
                json_create_file_data['phone'] = create_file_data.phone
            if create_file_data.l_name:
                json_create_file_data['l_name'] = create_file_data.l_name
            if create_file_data.f_name:
                json_create_file_data['f_name'] = create_file_data.f_name
            if create_file_data.notes:
                json_create_file_data['notes'] = create_file_data.notes
            if create_file_data.tags:
                json_create_file_data['tags'] = create_file_data.tags
            if create_file_data.meta:
                json_create_file_data['meta'] = create_file_data.meta
            if create_file_data.source:
                json_create_file_data['source'] = create_file_data.source
            if create_file_data.remind_days:
                json_create_file_data['remind_days'] = create_file_data.remind_days
            if create_file_data.remind_date:
                json_create_file_data['remind_date'] = create_file_data.remind_date.strftime('yyyy-MM-dd HH:mm:ss')
            form_params.append(('data', json.dumps(json_create_file_data)))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/create_file', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CreateFileResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_folder_post(self, api_key, name, _pass, **kwargs):  # noqa: E501
        """create_folder_post  # noqa: E501

        Create Folder   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_folder_post(api_key, name, _pass, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param str name: (required)
        :param str _pass: (required)
        :return: CreateFolderResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_folder_post_with_http_info(api_key, name, _pass, **kwargs)  # noqa: E501
        else:
            (data) = self.create_folder_post_with_http_info(api_key, name, _pass, **kwargs)  # noqa: E501
            return data

    def create_folder_post_with_http_info(self, api_key, name, _pass, **kwargs):  # noqa: E501
        """create_folder_post  # noqa: E501

        Create Folder   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_folder_post_with_http_info(api_key, name, _pass, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param str name: (required)
        :param str _pass: (required)
        :return: CreateFolderResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key', 'name', '_pass']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_folder_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `create_folder_post`")  # noqa: E501
        # verify the required parameter 'name' is set
        if ('name' not in params or
                params['name'] is None):
            raise ValueError("Missing the required parameter `name` when calling `create_folder_post`")  # noqa: E501
        # verify the required parameter '_pass' is set
        if ('_pass' not in params or
                params['_pass'] is None):
            raise ValueError("Missing the required parameter `_pass` when calling `create_folder_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501
        if 'name' in params:
            form_params.append(('name', params['name']))  # noqa: E501
        if '_pass' in params:
            form_params.append(('pass', params['_pass']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/create_folder', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CreateFolderResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_files_post(self, api_key, ids, action, **kwargs):  # noqa: E501
        """delete_files_post  # noqa: E501

        Delete Files   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_files_post(api_key, ids, action, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param list[int] ids: (required)
        :param str action: (required)
        :return: DeleteFilesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_files_post_with_http_info(api_key, ids, action, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_files_post_with_http_info(api_key, ids, action, **kwargs)  # noqa: E501
            return data

    def delete_files_post_with_http_info(self, api_key, ids, action, **kwargs):  # noqa: E501
        """delete_files_post  # noqa: E501

        Delete Files   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_files_post_with_http_info(api_key, ids, action, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param list[int] ids: (required)
        :param str action: (required)
        :return: DeleteFilesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key', 'ids', 'action']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_files_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `delete_files_post`")  # noqa: E501
        # verify the required parameter 'ids' is set
        if ('ids' not in params or
                params['ids'] is None):
            raise ValueError("Missing the required parameter `ids` when calling `delete_files_post`")  # noqa: E501
        # verify the required parameter 'action' is set
        if ('action' not in params or
                params['action'] is None):
            raise ValueError("Missing the required parameter `action` when calling `delete_files_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501
        if 'ids' in params:
            form_params.append(('ids', params['ids']))  # noqa: E501
            collection_formats['ids'] = 'multi'  # noqa: E501
        if 'action' in params:
            form_params.append(('action', params['action']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/delete_files', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DeleteFilesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_folder_post(self, api_key, id, move_to, **kwargs):  # noqa: E501
        """delete_folder_post  # noqa: E501

        Delete Folder   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_folder_post(api_key, id, move_to, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param int id: (required)
        :param int move_to: (required)
        :return: DeleteFolderResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_folder_post_with_http_info(api_key, id, move_to, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_folder_post_with_http_info(api_key, id, move_to, **kwargs)  # noqa: E501
            return data

    def delete_folder_post_with_http_info(self, api_key, id, move_to, **kwargs):  # noqa: E501
        """delete_folder_post  # noqa: E501

        Delete Folder   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_folder_post_with_http_info(api_key, id, move_to, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param int id: (required)
        :param int move_to: (required)
        :return: DeleteFolderResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key', 'id', 'move_to']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_folder_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `delete_folder_post`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `delete_folder_post`")  # noqa: E501
        # verify the required parameter 'move_to' is set
        if ('move_to' not in params or
                params['move_to'] is None):
            raise ValueError("Missing the required parameter `move_to` when calling `delete_folder_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501
        if 'id' in params:
            form_params.append(('id', params['id']))  # noqa: E501
        if 'move_to' in params:
            form_params.append(('move_to', params['move_to']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/delete_folder', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DeleteFolderResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_meta_files_post(self, api_key, ids, parent_id, **kwargs):  # noqa: E501
        """delete_meta_files_post  # noqa: E501

        Delete Meta Files   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_meta_files_post(api_key, ids, parent_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param list[int] ids: (required)
        :param int parent_id: (required)
        :return: DeleteMetaFilesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_meta_files_post_with_http_info(api_key, ids, parent_id, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_meta_files_post_with_http_info(api_key, ids, parent_id, **kwargs)  # noqa: E501
            return data

    def delete_meta_files_post_with_http_info(self, api_key, ids, parent_id, **kwargs):  # noqa: E501
        """delete_meta_files_post  # noqa: E501

        Delete Meta Files   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_meta_files_post_with_http_info(api_key, ids, parent_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param list[int] ids: (required)
        :param int parent_id: (required)
        :return: DeleteMetaFilesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key', 'ids', 'parent_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_meta_files_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `delete_meta_files_post`")  # noqa: E501
        # verify the required parameter 'ids' is set
        if ('ids' not in params or
                params['ids'] is None):
            raise ValueError("Missing the required parameter `ids` when calling `delete_meta_files_post`")  # noqa: E501
        # verify the required parameter 'parent_id' is set
        if ('parent_id' not in params or
                params['parent_id'] is None):
            raise ValueError("Missing the required parameter `parent_id` when calling `delete_meta_files_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501
        if 'ids' in params:
            form_params.append(('ids', params['ids']))  # noqa: E501
            collection_formats['ids'] = 'multi'  # noqa: E501
        if 'parent_id' in params:
            form_params.append(('parent_id', params['parent_id']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/delete_meta_files', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DeleteMetaFilesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_files_post(self, api_key, page, folder_id, source, _pass, reminder, q, id, op, **kwargs):  # noqa: E501
        """get_files_post  # noqa: E501

        Get Files   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_files_post(api_key, page, folder_id, source, _pass, reminder, q, id, op, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param str page: (required)
        :param int folder_id: (required)
        :param str source: (required)
        :param str _pass: (required)
        :param bool reminder: (required)
        :param str q: (required)
        :param int id: (required)
        :param str op: (required)
        :return: GetFilesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_files_post_with_http_info(api_key, page, folder_id, source, _pass, reminder, q, id, op, **kwargs)  # noqa: E501
        else:
            (data) = self.get_files_post_with_http_info(api_key, page, folder_id, source, _pass, reminder, q, id, op, **kwargs)  # noqa: E501
            return data

    def get_files_post_with_http_info(self, api_key, page, folder_id, source, _pass, reminder, q, id, op, **kwargs):  # noqa: E501
        """get_files_post  # noqa: E501

        Get Files   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_files_post_with_http_info(api_key, page, folder_id, source, _pass, reminder, q, id, op, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param str page: (required)
        :param int folder_id: (required)
        :param str source: (required)
        :param str _pass: (required)
        :param bool reminder: (required)
        :param str q: (required)
        :param int id: (required)
        :param str op: (required)
        :return: GetFilesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key', 'page', 'folder_id', 'source', '_pass', 'reminder', 'q', 'id', 'op']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_files_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `get_files_post`")  # noqa: E501
        # verify the required parameter 'page' is set
        if ('page' not in params or
                params['page'] is None):
            raise ValueError("Missing the required parameter `page` when calling `get_files_post`")  # noqa: E501
        # verify the required parameter 'folder_id' is set
        if ('folder_id' not in params or
                params['folder_id'] is None):
            raise ValueError("Missing the required parameter `folder_id` when calling `get_files_post`")  # noqa: E501
        # verify the required parameter 'source' is set
        if ('source' not in params or
                params['source'] is None):
            raise ValueError("Missing the required parameter `source` when calling `get_files_post`")  # noqa: E501
        # verify the required parameter '_pass' is set
        if ('_pass' not in params or
                params['_pass'] is None):
            raise ValueError("Missing the required parameter `_pass` when calling `get_files_post`")  # noqa: E501
        # verify the required parameter 'reminder' is set
        if ('reminder' not in params or
                params['reminder'] is None):
            raise ValueError("Missing the required parameter `reminder` when calling `get_files_post`")  # noqa: E501
        # verify the required parameter 'q' is set
        if ('q' not in params or
                params['q'] is None):
            raise ValueError("Missing the required parameter `q` when calling `get_files_post`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `get_files_post`")  # noqa: E501
        # verify the required parameter 'op' is set
        if ('op' not in params or
                params['op'] is None):
            raise ValueError("Missing the required parameter `op` when calling `get_files_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501
        if 'page' in params:
            form_params.append(('page', params['page']))  # noqa: E501
        if 'folder_id' in params:
            form_params.append(('folder_id', params['folder_id']))  # noqa: E501
        if 'source' in params:
            form_params.append(('source', params['source']))  # noqa: E501
        if '_pass' in params:
            form_params.append(('pass', params['_pass']))  # noqa: E501
        if 'reminder' in params:
            form_params.append(('reminder', params['reminder']))  # noqa: E501
        if 'q' in params:
            form_params.append(('q', params['q']))  # noqa: E501
        if 'id' in params:
            form_params.append(('id', params['id']))  # noqa: E501
        if 'op' in params:
            form_params.append(('op', params['op']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/get_files', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetFilesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_folders_post(self, api_key, **kwargs):  # noqa: E501
        """get_folders_post  # noqa: E501

        Get Folders   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_folders_post(api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :return: GetFoldersResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_folders_post_with_http_info(api_key, **kwargs)  # noqa: E501
        else:
            (data) = self.get_folders_post_with_http_info(api_key, **kwargs)  # noqa: E501
            return data

    def get_folders_post_with_http_info(self, api_key, **kwargs):  # noqa: E501
        """get_folders_post  # noqa: E501

        Get Folders   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_folders_post_with_http_info(api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :return: GetFoldersResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_folders_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `get_folders_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/get_folders', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetFoldersResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_languages_post(self, api_key, **kwargs):  # noqa: E501
        """get_languages_post  # noqa: E501

        Get Languages   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_languages_post(api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :return: GetLanguagesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_languages_post_with_http_info(api_key, **kwargs)  # noqa: E501
        else:
            (data) = self.get_languages_post_with_http_info(api_key, **kwargs)  # noqa: E501
            return data

    def get_languages_post_with_http_info(self, api_key, **kwargs):  # noqa: E501
        """get_languages_post  # noqa: E501

        Get Languages   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_languages_post_with_http_info(api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :return: GetLanguagesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_languages_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `get_languages_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/get_languages', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetLanguagesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_meta_files_post(self, api_key, parent_id, **kwargs):  # noqa: E501
        """get_meta_files_post  # noqa: E501

        Get Meta File   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_meta_files_post(api_key, parent_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param int parent_id: (required)
        :return: GetMetaFilesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_meta_files_post_with_http_info(api_key, parent_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_meta_files_post_with_http_info(api_key, parent_id, **kwargs)  # noqa: E501
            return data

    def get_meta_files_post_with_http_info(self, api_key, parent_id, **kwargs):  # noqa: E501
        """get_meta_files_post  # noqa: E501

        Get Meta File   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_meta_files_post_with_http_info(api_key, parent_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param int parent_id: (required)
        :return: GetMetaFilesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key', 'parent_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_meta_files_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `get_meta_files_post`")  # noqa: E501
        # verify the required parameter 'parent_id' is set
        if ('parent_id' not in params or
                params['parent_id'] is None):
            raise ValueError("Missing the required parameter `parent_id` when calling `get_meta_files_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501
        if 'parent_id' in params:
            form_params.append(('parent_id', params['parent_id']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/get_meta_files', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetMetaFilesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msgs_post(self, api_key, **kwargs):  # noqa: E501
        """get_msgs_post  # noqa: E501

        Get Messages   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msgs_post(api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :return: GetMessagesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msgs_post_with_http_info(api_key, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msgs_post_with_http_info(api_key, **kwargs)  # noqa: E501
            return data

    def get_msgs_post_with_http_info(self, api_key, **kwargs):  # noqa: E501
        """get_msgs_post  # noqa: E501

        Get Messages   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msgs_post_with_http_info(api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :return: GetMessagesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msgs_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `get_msgs_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/get_msgs', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetMessagesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_phones_post(self, api_key, **kwargs):  # noqa: E501
        """get_phones_post  # noqa: E501

        Get Phones   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_phones_post(api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :return: GetPhonesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_phones_post_with_http_info(api_key, **kwargs)  # noqa: E501
        else:
            (data) = self.get_phones_post_with_http_info(api_key, **kwargs)  # noqa: E501
            return data

    def get_phones_post_with_http_info(self, api_key, **kwargs):  # noqa: E501
        """get_phones_post  # noqa: E501

        Get Phones   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_phones_post_with_http_info(api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :return: GetPhonesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_phones_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `get_phones_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/get_phones', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetPhonesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_profile_post(self, api_key, **kwargs):  # noqa: E501
        """get_profile_post  # noqa: E501

        Get Profile   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_profile_post(api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :return: GetProfileResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_profile_post_with_http_info(api_key, **kwargs)  # noqa: E501
        else:
            (data) = self.get_profile_post_with_http_info(api_key, **kwargs)  # noqa: E501
            return data

    def get_profile_post_with_http_info(self, api_key, **kwargs):  # noqa: E501
        """get_profile_post  # noqa: E501

        Get Profile   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_profile_post_with_http_info(api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :return: GetProfileResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_profile_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `get_profile_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/get_profile', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetProfileResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_settings_post(self, api_key, **kwargs):  # noqa: E501
        """get_settings_post  # noqa: E501

        Get Settings   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_settings_post(api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :return: GetSettingsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_settings_post_with_http_info(api_key, **kwargs)  # noqa: E501
        else:
            (data) = self.get_settings_post_with_http_info(api_key, **kwargs)  # noqa: E501
            return data

    def get_settings_post_with_http_info(self, api_key, **kwargs):  # noqa: E501
        """get_settings_post  # noqa: E501

        Get Settings   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_settings_post_with_http_info(api_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :return: GetSettingsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_settings_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `get_settings_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/get_settings', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetSettingsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_translations_post(self, api_key, language, **kwargs):  # noqa: E501
        """get_translations_post  # noqa: E501

        Get Translations   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_translations_post(api_key, language, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param str language: (required)
        :return: GetTranslationsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_translations_post_with_http_info(api_key, language, **kwargs)  # noqa: E501
        else:
            (data) = self.get_translations_post_with_http_info(api_key, language, **kwargs)  # noqa: E501
            return data

    def get_translations_post_with_http_info(self, api_key, language, **kwargs):  # noqa: E501
        """get_translations_post  # noqa: E501

        Get Translations   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_translations_post_with_http_info(api_key, language, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param str language: (required)
        :return: GetTranslationsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key', 'language']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_translations_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `get_translations_post`")  # noqa: E501
        # verify the required parameter 'language' is set
        if ('language' not in params or
                params['language'] is None):
            raise ValueError("Missing the required parameter `language` when calling `get_translations_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501
        if 'language' in params:
            form_params.append(('language', params['language']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/get_translations', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetTranslationsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def notify_user_post(self, api_key, title, body, device_type, **kwargs):  # noqa: E501
        """notify_user_post  # noqa: E501

        Notify User   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.notify_user_post(api_key, title, body, device_type, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param str title: (required)
        :param str body: (required)
        :param DeviceType device_type: (required)
        :return: NotifyUserResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.notify_user_post_with_http_info(api_key, title, body, device_type, **kwargs)  # noqa: E501
        else:
            (data) = self.notify_user_post_with_http_info(api_key, title, body, device_type, **kwargs)  # noqa: E501
            return data

    def notify_user_post_with_http_info(self, api_key, title, body, device_type, **kwargs):  # noqa: E501
        """notify_user_post  # noqa: E501

        Notify User   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.notify_user_post_with_http_info(api_key, title, body, device_type, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param str title: (required)
        :param str body: (required)
        :param DeviceType device_type: (required)
        :return: NotifyUserResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key', 'title', 'body', 'device_type']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method notify_user_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `notify_user_post`")  # noqa: E501
        # verify the required parameter 'title' is set
        if ('title' not in params or
                params['title'] is None):
            raise ValueError("Missing the required parameter `title` when calling `notify_user_post`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `notify_user_post`")  # noqa: E501
        # verify the required parameter 'device_type' is set
        if ('device_type' not in params or
                params['device_type'] is None):
            raise ValueError("Missing the required parameter `device_type` when calling `notify_user_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501
        if 'title' in params:
            form_params.append(('title', params['title']))  # noqa: E501
        if 'body' in params:
            form_params.append(('body', params['body']))  # noqa: E501
        if 'device_type' in params:
            form_params.append(('device_type', params['device_type']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/notify_user_custom', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='NotifyUserResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def recover_file_post(self, api_key, id, folder_id, **kwargs):  # noqa: E501
        """recover_file_post  # noqa: E501

        Recover File   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.recover_file_post(api_key, id, folder_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param int id: (required)
        :param int folder_id: (required)
        :return: RecoverFileResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.recover_file_post_with_http_info(api_key, id, folder_id, **kwargs)  # noqa: E501
        else:
            (data) = self.recover_file_post_with_http_info(api_key, id, folder_id, **kwargs)  # noqa: E501
            return data

    def recover_file_post_with_http_info(self, api_key, id, folder_id, **kwargs):  # noqa: E501
        """recover_file_post  # noqa: E501

        Recover File   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.recover_file_post_with_http_info(api_key, id, folder_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param int id: (required)
        :param int folder_id: (required)
        :return: RecoverFileResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key', 'id', 'folder_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method recover_file_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `recover_file_post`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `recover_file_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501
        if 'id' in params:
            form_params.append(('id', params['id']))  # noqa: E501
        if 'folder_id' in params:
            form_params.append(('folder_id', params['folder_id']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/recover_file', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RecoverFileResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def register_phone_post(self, token, phone, **kwargs):  # noqa: E501
        """register_phone_post  # noqa: E501

        Register Phone, Send phone number to server to get verification code    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.register_phone_post(token, phone, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str token: (required)
        :param str phone: (required)
        :return: RegisterPhoneResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.register_phone_post_with_http_info(token, phone, **kwargs)  # noqa: E501
        else:
            (data) = self.register_phone_post_with_http_info(token, phone, **kwargs)  # noqa: E501
            return data

    def register_phone_post_with_http_info(self, token, phone, **kwargs):  # noqa: E501
        """register_phone_post  # noqa: E501

        Register Phone, Send phone number to server to get verification code    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.register_phone_post_with_http_info(token, phone, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str token: (required)
        :param str phone: (required)
        :return: RegisterPhoneResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['token', 'phone']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method register_phone_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'token' is set
        if ('token' not in params or
                params['token'] is None):
            raise ValueError("Missing the required parameter `token` when calling `register_phone_post`")  # noqa: E501
        # verify the required parameter 'phone' is set
        if ('phone' not in params or
                params['phone'] is None):
            raise ValueError("Missing the required parameter `phone` when calling `register_phone_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'token' in params:
            form_params.append(('token', params['token']))  # noqa: E501
        if 'phone' in params:
            form_params.append(('phone', params['phone']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/register_phone', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RegisterPhoneResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_device_token_post(self, api_key, device_token, device_type, **kwargs):  # noqa: E501
        """update_device_token_post  # noqa: E501

        Update Device Token   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_device_token_post(api_key, device_token, device_type, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param str device_token: (required)
        :param DeviceType device_type: (required)
        :return: UpdateDeviceTokenResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_device_token_post_with_http_info(api_key, device_token, device_type, **kwargs)  # noqa: E501
        else:
            (data) = self.update_device_token_post_with_http_info(api_key, device_token, device_type, **kwargs)  # noqa: E501
            return data

    def update_device_token_post_with_http_info(self, api_key, device_token, device_type, **kwargs):  # noqa: E501
        """update_device_token_post  # noqa: E501

        Update Device Token   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_device_token_post_with_http_info(api_key, device_token, device_type, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param str device_token: (required)
        :param DeviceType device_type: (required)
        :return: UpdateDeviceTokenResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key', 'device_token', 'device_type']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_device_token_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `update_device_token_post`")  # noqa: E501
        # verify the required parameter 'device_token' is set
        if ('device_token' not in params or
                params['device_token'] is None):
            raise ValueError("Missing the required parameter `device_token` when calling `update_device_token_post`")  # noqa: E501
        # verify the required parameter 'device_type' is set
        if ('device_type' not in params or
                params['device_type'] is None):
            raise ValueError("Missing the required parameter `device_type` when calling `update_device_token_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501
        if 'device_token' in params:
            form_params.append(('device_token', params['device_token']))  # noqa: E501
        if 'device_type' in params:
            form_params.append(('device_type', params['device_type']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/update_device_token', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UpdateDeviceTokenResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_file_post(self, api_key, id, f_name, l_name, notes, email, phone, tags, folder_id, name, remind_days, remind_date, **kwargs):  # noqa: E501
        """update_file_post  # noqa: E501

        Update File   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_file_post(api_key, id, f_name, l_name, notes, email, phone, tags, folder_id, name, remind_days, remind_date, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param int id: (required)
        :param str f_name: (required)
        :param str l_name: (required)
        :param str notes: (required)
        :param str email: (required)
        :param str phone: (required)
        :param str tags: (required)
        :param int folder_id: (required)
        :param str name: (required)
        :param str remind_days: (required)
        :param datetime remind_date: (required)
        :return: UpdateFileResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_file_post_with_http_info(api_key, id, f_name, l_name, notes, email, phone, tags, folder_id, name, remind_days, remind_date, **kwargs)  # noqa: E501
        else:
            (data) = self.update_file_post_with_http_info(api_key, id, f_name, l_name, notes, email, phone, tags, folder_id, name, remind_days, remind_date, **kwargs)  # noqa: E501
            return data

    def update_file_post_with_http_info(self, api_key, id, f_name, l_name, notes, email, phone, tags, folder_id, name, remind_days, remind_date, **kwargs):  # noqa: E501
        """update_file_post  # noqa: E501

        Update File   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_file_post_with_http_info(api_key, id, f_name, l_name, notes, email, phone, tags, folder_id, name, remind_days, remind_date, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param int id: (required)
        :param str f_name: (required)
        :param str l_name: (required)
        :param str notes: (required)
        :param str email: (required)
        :param str phone: (required)
        :param str tags: (required)
        :param int folder_id: (required)
        :param str name: (required)
        :param str remind_days: (required)
        :param datetime remind_date: (required)
        :return: UpdateFileResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key', 'id', 'f_name', 'l_name', 'notes', 'email', 'phone', 'tags', 'folder_id', 'name', 'remind_days', 'remind_date']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_file_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `update_file_post`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `update_file_post`")  # noqa: E501
        # verify the required parameter 'f_name' is set
        if ('f_name' not in params or
                params['f_name'] is None):
            raise ValueError("Missing the required parameter `f_name` when calling `update_file_post`")  # noqa: E501
        # verify the required parameter 'l_name' is set
        if ('l_name' not in params or
                params['l_name'] is None):
            raise ValueError("Missing the required parameter `l_name` when calling `update_file_post`")  # noqa: E501
        # verify the required parameter 'notes' is set
        if ('notes' not in params or
                params['notes'] is None):
            raise ValueError("Missing the required parameter `notes` when calling `update_file_post`")  # noqa: E501
        # verify the required parameter 'email' is set
        if ('email' not in params or
                params['email'] is None):
            raise ValueError("Missing the required parameter `email` when calling `update_file_post`")  # noqa: E501
        # verify the required parameter 'phone' is set
        if ('phone' not in params or
                params['phone'] is None):
            raise ValueError("Missing the required parameter `phone` when calling `update_file_post`")  # noqa: E501
        # verify the required parameter 'tags' is set
        if ('tags' not in params or
                params['tags'] is None):
            raise ValueError("Missing the required parameter `tags` when calling `update_file_post`")  # noqa: E501
        # verify the required parameter 'folder_id' is set
        if ('folder_id' not in params or
                params['folder_id'] is None):
            raise ValueError("Missing the required parameter `folder_id` when calling `update_file_post`")  # noqa: E501
        # verify the required parameter 'name' is set
        if ('name' not in params or
                params['name'] is None):
            raise ValueError("Missing the required parameter `name` when calling `update_file_post`")  # noqa: E501
        # verify the required parameter 'remind_days' is set
        if ('remind_days' not in params or
                params['remind_days'] is None):
            raise ValueError("Missing the required parameter `remind_days` when calling `update_file_post`")  # noqa: E501
        # verify the required parameter 'remind_date' is set
        if ('remind_date' not in params or
                params['remind_date'] is None):
            raise ValueError("Missing the required parameter `remind_date` when calling `update_file_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501
        if 'id' in params:
            form_params.append(('id', params['id']))  # noqa: E501
        if 'f_name' in params:
            form_params.append(('f_name', params['f_name']))  # noqa: E501
        if 'l_name' in params:
            form_params.append(('l_name', params['l_name']))  # noqa: E501
        if 'notes' in params:
            form_params.append(('notes', params['notes']))  # noqa: E501
        if 'email' in params:
            form_params.append(('email', params['email']))  # noqa: E501
        if 'phone' in params:
            form_params.append(('phone', params['phone']))  # noqa: E501
        if 'tags' in params:
            form_params.append(('tags', params['tags']))  # noqa: E501
        if 'folder_id' in params:
            form_params.append(('folder_id', params['folder_id']))  # noqa: E501
        if 'name' in params:
            form_params.append(('name', params['name']))  # noqa: E501
        if 'remind_days' in params:
            form_params.append(('remind_days', params['remind_days']))  # noqa: E501
        if 'remind_date' in params:
            form_params.append(('remind_date', params['remind_date']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/update_file', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UpdateFileResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_folder_post(self, api_key, id, name, _pass, is_private, **kwargs):  # noqa: E501
        """update_folder_post  # noqa: E501

        Update Folder   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_folder_post(api_key, id, name, _pass, is_private, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param int id: (required)
        :param str name: (required)
        :param str _pass: (required)
        :param bool is_private: (required)
        :return: UpdateFolderResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_folder_post_with_http_info(api_key, id, name, _pass, is_private, **kwargs)  # noqa: E501
        else:
            (data) = self.update_folder_post_with_http_info(api_key, id, name, _pass, is_private, **kwargs)  # noqa: E501
            return data

    def update_folder_post_with_http_info(self, api_key, id, name, _pass, is_private, **kwargs):  # noqa: E501
        """update_folder_post  # noqa: E501

        Update Folder   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_folder_post_with_http_info(api_key, id, name, _pass, is_private, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param int id: (required)
        :param str name: (required)
        :param str _pass: (required)
        :param bool is_private: (required)
        :return: UpdateFolderResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key', 'id', 'name', '_pass', 'is_private']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_folder_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `update_folder_post`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `update_folder_post`")  # noqa: E501
        # verify the required parameter 'name' is set
        if ('name' not in params or
                params['name'] is None):
            raise ValueError("Missing the required parameter `name` when calling `update_folder_post`")  # noqa: E501
        # verify the required parameter '_pass' is set
        if ('_pass' not in params or
                params['_pass'] is None):
            raise ValueError("Missing the required parameter `_pass` when calling `update_folder_post`")  # noqa: E501
        # verify the required parameter 'is_private' is set
        if ('is_private' not in params or
                params['is_private'] is None):
            raise ValueError("Missing the required parameter `is_private` when calling `update_folder_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501
        if 'id' in params:
            form_params.append(('id', params['id']))  # noqa: E501
        if 'name' in params:
            form_params.append(('name', params['name']))  # noqa: E501
        if '_pass' in params:
            form_params.append(('pass', params['_pass']))  # noqa: E501
        if 'is_private' in params:
            form_params.append(('is_private', params['is_private']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/update_folder', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UpdateFolderResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_order_post(self, api_key, folders, **kwargs):  # noqa: E501
        """update_order_post  # noqa: E501

        Update Order   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_order_post(api_key, folders, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param list[UpdateOrderRequestFolders] folders: (required)
        :return: UpdateOrderResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_order_post_with_http_info(api_key, folders, **kwargs)  # noqa: E501
        else:
            (data) = self.update_order_post_with_http_info(api_key, folders, **kwargs)  # noqa: E501
            return data

    def update_order_post_with_http_info(self, api_key, folders, **kwargs):  # noqa: E501
        """update_order_post  # noqa: E501

        Update Order   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_order_post_with_http_info(api_key, folders, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param list[UpdateOrderRequestFolders] folders: (required)
        :return: UpdateOrderResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key', 'folders']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_order_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `update_order_post`")  # noqa: E501
        # verify the required parameter 'folders' is set
        if ('folders' not in params or
                params['folders'] is None):
            raise ValueError("Missing the required parameter `folders` when calling `update_order_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501
        if 'folders' in params:
            form_params.append(('folders', params['folders']))  # noqa: E501
            collection_formats['folders'] = 'multi'  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/update_order', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UpdateOrderResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_profile_img_post(self, api_key, file, **kwargs):  # noqa: E501
        """update_profile_img_post  # noqa: E501

        Update Profile Img   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_profile_img_post(api_key, file, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param str file: (required)
        :return: UpdateProfileImgResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_profile_img_post_with_http_info(api_key, file, **kwargs)  # noqa: E501
        else:
            (data) = self.update_profile_img_post_with_http_info(api_key, file, **kwargs)  # noqa: E501
            return data

    def update_profile_img_post_with_http_info(self, api_key, file, **kwargs):  # noqa: E501
        """update_profile_img_post  # noqa: E501

        Update Profile Img   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_profile_img_post_with_http_info(api_key, file, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param str file: (required)
        :return: UpdateProfileImgResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key', 'file']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_profile_img_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `update_profile_img_post`")  # noqa: E501
        # verify the required parameter 'file' is set
        if ('file' not in params or
                params['file'] is None):
            raise ValueError("Missing the required parameter `file` when calling `update_profile_img_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501
        if 'file' in params:
            local_var_files['file'] = params['file']

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/upload/update_profile_img', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UpdateProfileImgResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_profile_post(self, api_key, data, **kwargs):  # noqa: E501
        """update_profile_post  # noqa: E501

        Update Profile   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_profile_post(api_key, data, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param UpdateProfileRequestData data: (required)
        :return: UpdateProfileResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_profile_post_with_http_info(api_key, data, **kwargs)  # noqa: E501
        else:
            (data) = self.update_profile_post_with_http_info(api_key, data, **kwargs)  # noqa: E501
            return data

    def update_profile_post_with_http_info(self, api_key, data, **kwargs):  # noqa: E501
        """update_profile_post  # noqa: E501

        Update Profile   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_profile_post_with_http_info(api_key, data, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param UpdateProfileRequestData data: (required)
        :return: UpdateProfileResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key', 'data']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_profile_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `update_profile_post`")  # noqa: E501
        # verify the required parameter 'data' is set
        if ('data' not in params or
                params['data'] is None):
            raise ValueError("Missing the required parameter `data` when calling `update_profile_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501
        if 'data' in params:
            if data.f_name:
                form_params.append(('data[f_name]', data.f_name))
            if data.l_name:
                form_params.append(('data[l_name]', data.l_name))
            if data.email:
                form_params.append(('data[email]', data.email))
            if data.is_public:
                form_params.append(('data[is_public]', data.is_public))
            if data.language:
                form_params.append(('data[language]', data.language))

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/update_profile', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UpdateProfileResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_settings_post(self, api_key, play_beep, files_permission, **kwargs):  # noqa: E501
        """update_settings_post  # noqa: E501

        Update Settings   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_settings_post(api_key, play_beep, files_permission, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param PlayBeep play_beep: (required)
        :param FilesPermission files_permission: (required)
        :return: UpdateSettingsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_settings_post_with_http_info(api_key, play_beep, files_permission, **kwargs)  # noqa: E501
        else:
            (data) = self.update_settings_post_with_http_info(api_key, play_beep, files_permission, **kwargs)  # noqa: E501
            return data

    def update_settings_post_with_http_info(self, api_key, play_beep, files_permission, **kwargs):  # noqa: E501
        """update_settings_post  # noqa: E501

        Update Settings   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_settings_post_with_http_info(api_key, play_beep, files_permission, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param PlayBeep play_beep: (required)
        :param FilesPermission files_permission: (required)
        :return: UpdateSettingsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key', 'play_beep', 'files_permission']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_settings_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `update_settings_post`")  # noqa: E501
        # verify the required parameter 'play_beep' is set
        if ('play_beep' not in params or
                params['play_beep'] is None):
            raise ValueError("Missing the required parameter `play_beep` when calling `update_settings_post`")  # noqa: E501
        # verify the required parameter 'files_permission' is set
        if ('files_permission' not in params or
                params['files_permission'] is None):
            raise ValueError("Missing the required parameter `files_permission` when calling `update_settings_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501
        if 'play_beep' in params:
            form_params.append(('play_beep', params['play_beep']))  # noqa: E501
        if 'files_permission' in params:
            form_params.append(('files_permission', params['files_permission']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/update_settings', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UpdateSettingsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_star_post(self, api_key, id, star, type, **kwargs):  # noqa: E501
        """update_star_post  # noqa: E501

        Update Star   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_star_post(api_key, id, star, type, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param int id: (required)
        :param int star: (required)
        :param str type: (required)
        :return: UpdateStarResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_star_post_with_http_info(api_key, id, star, type, **kwargs)  # noqa: E501
        else:
            (data) = self.update_star_post_with_http_info(api_key, id, star, type, **kwargs)  # noqa: E501
            return data

    def update_star_post_with_http_info(self, api_key, id, star, type, **kwargs):  # noqa: E501
        """update_star_post  # noqa: E501

        Update Star   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_star_post_with_http_info(api_key, id, star, type, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param int id: (required)
        :param int star: (required)
        :param str type: (required)
        :return: UpdateStarResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key', 'id', 'star', 'type']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_star_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `update_star_post`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `update_star_post`")  # noqa: E501
        # verify the required parameter 'star' is set
        if ('star' not in params or
                params['star'] is None):
            raise ValueError("Missing the required parameter `star` when calling `update_star_post`")  # noqa: E501
        # verify the required parameter 'type' is set
        if ('type' not in params or
                params['type'] is None):
            raise ValueError("Missing the required parameter `type` when calling `update_star_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501
        if 'id' in params:
            form_params.append(('id', params['id']))  # noqa: E501
        if 'star' in params:
            form_params.append(('star', params['star']))  # noqa: E501
        if 'type' in params:
            form_params.append(('type', params['type']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/update_star', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UpdateStarResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_user_post(self, api_key, app, timezone, **kwargs):  # noqa: E501
        """update_user_post  # noqa: E501

        Update User   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_user_post(api_key, app, timezone, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param App app: (required)
        :param str timezone: (required)
        :return: UpdateUserResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_user_post_with_http_info(api_key, app, timezone, **kwargs)  # noqa: E501
        else:
            (data) = self.update_user_post_with_http_info(api_key, app, timezone, **kwargs)  # noqa: E501
            return data

    def update_user_post_with_http_info(self, api_key, app, timezone, **kwargs):  # noqa: E501
        """update_user_post  # noqa: E501

        Update User   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_user_post_with_http_info(api_key, app, timezone, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param App app: (required)
        :param str timezone: (required)
        :return: UpdateUserResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key', 'app', 'timezone']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_user_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `update_user_post`")  # noqa: E501
        # verify the required parameter 'app' is set
        if ('app' not in params or
                params['app'] is None):
            raise ValueError("Missing the required parameter `app` when calling `update_user_post`")  # noqa: E501
        # verify the required parameter 'timezone' is set
        if ('timezone' not in params or
                params['timezone'] is None):
            raise ValueError("Missing the required parameter `timezone` when calling `update_user_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501
        if 'app' in params:
            form_params.append(('app', params['app']))  # noqa: E501
        if 'timezone' in params:
            form_params.append(('timezone', params['timezone']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/update_user', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UpdateUserResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def upload_meta_file_post(self, api_key, file, name, parent_id, id, **kwargs):  # noqa: E501
        """upload_meta_file_post  # noqa: E501

        Upload Meta File   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.upload_meta_file_post(api_key, file, name, parent_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param str file: (required)
        :param str name: (required)
        :param int parent_id: (required)
        :param int id: (required)
        :return: UploadMetaFileResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.upload_meta_file_post_with_http_info(api_key, file, name, parent_id, id, **kwargs)  # noqa: E501
        else:
            (data) = self.upload_meta_file_post_with_http_info(api_key, file, name, parent_id, id, **kwargs)  # noqa: E501
            return data

    def upload_meta_file_post_with_http_info(self, api_key, file, name, parent_id, id, **kwargs):  # noqa: E501
        """upload_meta_file_post  # noqa: E501

        Upload Meta File   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.upload_meta_file_post_with_http_info(api_key, file, name, parent_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param str file: (required)
        :param str name: (required)
        :param int parent_id: (required)
        :param int id: (required)
        :return: UploadMetaFileResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key', 'file', 'name', 'parent_id', 'id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method upload_meta_file_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `upload_meta_file_post`")  # noqa: E501
        # verify the required parameter 'file' is set
        if ('file' not in params or
                params['file'] is None):
            raise ValueError("Missing the required parameter `file` when calling `upload_meta_file_post`")  # noqa: E501
        # verify the required parameter 'name' is set
        if ('name' not in params or
                params['name'] is None):
            raise ValueError("Missing the required parameter `name` when calling `upload_meta_file_post`")  # noqa: E501
        # verify the required parameter 'parent_id' is set
        if ('parent_id' not in params or
                params['parent_id'] is None):
            raise ValueError("Missing the required parameter `parent_id` when calling `upload_meta_file_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501
        if 'file' in params:
            local_var_files['file'] = params['file']
        if 'name' in params:
            form_params.append(('name', params['name']))  # noqa: E501
        if 'parent_id' in params:
            form_params.append(('parent_id', params['parent_id']))  # noqa: E501
        if 'id' in params and params['id'] is not None:
            form_params.append(('id', params['id']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/upload_meta_file', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UploadMetaFileResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def verify_folder_pass_post(self, api_key, id, _pass, **kwargs):  # noqa: E501
        """verify_folder_pass_post  # noqa: E501

        Verify Folder Pass   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.verify_folder_pass_post(api_key, id, _pass, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param int id: (required)
        :param str _pass: (required)
        :return: VerifyFolderPassResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.verify_folder_pass_post_with_http_info(api_key, id, _pass, **kwargs)  # noqa: E501
        else:
            (data) = self.verify_folder_pass_post_with_http_info(api_key, id, _pass, **kwargs)  # noqa: E501
            return data

    def verify_folder_pass_post_with_http_info(self, api_key, id, _pass, **kwargs):  # noqa: E501
        """verify_folder_pass_post  # noqa: E501

        Verify Folder Pass   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.verify_folder_pass_post_with_http_info(api_key, id, _pass, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str api_key: (required)
        :param int id: (required)
        :param str _pass: (required)
        :return: VerifyFolderPassResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['api_key', 'id', '_pass']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method verify_folder_pass_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'api_key' is set
        if ('api_key' not in params or
                params['api_key'] is None):
            raise ValueError("Missing the required parameter `api_key` when calling `verify_folder_pass_post`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `verify_folder_pass_post`")  # noqa: E501
        # verify the required parameter '_pass' is set
        if ('_pass' not in params or
                params['_pass'] is None):
            raise ValueError("Missing the required parameter `_pass` when calling `verify_folder_pass_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'api_key' in params:
            form_params.append(('api_key', params['api_key']))  # noqa: E501
        if 'id' in params:
            form_params.append(('id', params['id']))  # noqa: E501
        if '_pass' in params:
            form_params.append(('pass', params['_pass']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/verify_folder_pass', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='VerifyFolderPassResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def verify_phone_post(self, token, phone, code, mcc, app, device_token, device_id, device_type, time_zone, **kwargs):  # noqa: E501
        """verify_phone_post  # noqa: E501

        Send phone number and verification code to get API Key   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.verify_phone_post(token, phone, code, mcc, app, device_token, device_id, device_type, time_zone, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str token: (required)
        :param str phone: (required)
        :param str code: (required)
        :param str mcc: (required)
        :param App app: (required)
        :param str device_token: (required)
        :param str device_id: (required)
        :param DeviceType device_type: (required)
        :param str time_zone: (required)
        :return: VerifyPhoneResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.verify_phone_post_with_http_info(token, phone, code, mcc, app, device_token, device_id, device_type, time_zone, **kwargs)  # noqa: E501
        else:
            (data) = self.verify_phone_post_with_http_info(token, phone, code, mcc, app, device_token, device_id, device_type, time_zone, **kwargs)  # noqa: E501
            return data

    def verify_phone_post_with_http_info(self, token, phone, code, mcc, app, device_token, device_id, device_type, time_zone, **kwargs):  # noqa: E501
        """verify_phone_post  # noqa: E501

        Send phone number and verification code to get API Key   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.verify_phone_post_with_http_info(token, phone, code, mcc, app, device_token, device_id, device_type, time_zone, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str token: (required)
        :param str phone: (required)
        :param str code: (required)
        :param str mcc: (required)
        :param App app: (required)
        :param str device_token: (required)
        :param str device_id: (required)
        :param DeviceType device_type: (required)
        :param str time_zone: (required)
        :return: VerifyPhoneResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['token', 'phone', 'code', 'mcc', 'app', 'device_token', 'device_id', 'device_type', 'time_zone']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method verify_phone_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'token' is set
        if ('token' not in params or
                params['token'] is None):
            raise ValueError("Missing the required parameter `token` when calling `verify_phone_post`")  # noqa: E501
        # verify the required parameter 'phone' is set
        if ('phone' not in params or
                params['phone'] is None):
            raise ValueError("Missing the required parameter `phone` when calling `verify_phone_post`")  # noqa: E501
        # verify the required parameter 'code' is set
        if ('code' not in params or
                params['code'] is None):
            raise ValueError("Missing the required parameter `code` when calling `verify_phone_post`")  # noqa: E501
        # verify the required parameter 'mcc' is set
        if ('mcc' not in params or
                params['mcc'] is None):
            raise ValueError("Missing the required parameter `mcc` when calling `verify_phone_post`")  # noqa: E501
        # verify the required parameter 'app' is set
        if ('app' not in params or
                params['app'] is None):
            raise ValueError("Missing the required parameter `app` when calling `verify_phone_post`")  # noqa: E501
        # verify the required parameter 'device_token' is set
        if ('device_token' not in params or
                params['device_token'] is None):
            raise ValueError("Missing the required parameter `device_token` when calling `verify_phone_post`")  # noqa: E501
        # verify the required parameter 'device_id' is set
        if ('device_id' not in params or
                params['device_id'] is None):
            raise ValueError("Missing the required parameter `device_id` when calling `verify_phone_post`")  # noqa: E501
        # verify the required parameter 'device_type' is set
        if ('device_type' not in params or
                params['device_type'] is None):
            raise ValueError("Missing the required parameter `device_type` when calling `verify_phone_post`")  # noqa: E501
        # verify the required parameter 'time_zone' is set
        if ('time_zone' not in params or
                params['time_zone'] is None):
            raise ValueError("Missing the required parameter `time_zone` when calling `verify_phone_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'token' in params:
            form_params.append(('token', params['token']))  # noqa: E501
        if 'phone' in params:
            form_params.append(('phone', params['phone']))  # noqa: E501
        if 'code' in params:
            form_params.append(('code', params['code']))  # noqa: E501
        if 'mcc' in params:
            form_params.append(('mcc', params['mcc']))  # noqa: E501
        if 'app' in params:
            form_params.append(('app', params['app']))  # noqa: E501
        if 'device_token' in params:
            form_params.append(('device_token', params['device_token']))  # noqa: E501
        if 'device_id' in params:
            form_params.append(('device_id', params['device_id']))  # noqa: E501
        if 'device_type' in params:
            form_params.append(('device_type', params['device_type']))  # noqa: E501
        if 'time_zone' in params:
            form_params.append(('time_zone', params['time_zone']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rapi/verify_phone', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='VerifyPhoneResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
