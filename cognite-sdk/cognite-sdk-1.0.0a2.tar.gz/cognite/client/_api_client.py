import gzip
import json as _json
import logging
import os
import re
from typing import Any, Dict, List, Union

import requests.utils
from requests import Response, Session
from requests.adapters import HTTPAdapter
from requests.structures import CaseInsensitiveDict
from urllib3 import Retry

from cognite.client._base import CogniteResource, CogniteUpdate
from cognite.client.exceptions import CogniteAPIError
from cognite.client.utils import _utils as utils

log = logging.getLogger("cognite-sdk")

BACKOFF_MAX = 30
DEFAULT_MAX_POOL_SIZE = 50
DEFAULT_MAX_RETRIES = 5
HTTP_STATUS_CODES_TO_RETRY = [429, 500, 502, 503]


class RetryWithMaxBackoff(Retry):
    def get_backoff_time(self):
        return min(BACKOFF_MAX, super().get_backoff_time())


def _init_requests_session():
    session = Session()
    num_of_retries = int(os.getenv("COGNITE_MAX_RETRIES", DEFAULT_MAX_RETRIES))
    max_pool_size = int(os.getenv("COGNITE_MAX_CONNECTION_POOL_SIZE", DEFAULT_MAX_POOL_SIZE))
    adapter = HTTPAdapter(
        max_retries=RetryWithMaxBackoff(
            total=num_of_retries, connect=num_of_retries, read=0, status=0, backoff_factor=0.5, raise_on_status=False
        ),
        pool_maxsize=max_pool_size,
    )
    adapter_with_retry = HTTPAdapter(
        max_retries=RetryWithMaxBackoff(
            total=num_of_retries,
            backoff_factor=0.5,
            status_forcelist=HTTP_STATUS_CODES_TO_RETRY,
            method_whitelist=False,
            raise_on_status=False,
        ),
        pool_maxsize=max_pool_size,
    )
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    # TODO: mount adapter_with_retry on all retryable paths. This list of paths should be generated from openapi spec.
    return session


_REQUESTS_SESSION = _init_requests_session()


class APIClient:
    _RESOURCE_PATH = None
    _LIST_CLASS = None

    def __init__(
        self,
        version: str = None,
        project: str = None,
        api_key: str = None,
        base_url: str = None,
        max_workers: int = None,
        headers: Dict = None,
        timeout: int = None,
        cognite_client=None,
    ):
        self._request_session = _REQUESTS_SESSION
        self._project = project
        self._api_key = api_key
        __base_path = "/api/{}/projects/{}".format(version, project) if version else ""
        self._base_url = base_url + __base_path
        self._max_workers = max_workers
        self._headers = self._configure_headers(headers)
        self._timeout = timeout
        self._cognite_client = cognite_client

        self._CREATE_LIMIT = 1000
        self._LIST_LIMIT = 1000
        self._RETRIEVE_LIMIT = 1000
        self._DELETE_LIMIT = 1000
        self._UPDATE_LIMIT = 1000

    def _delete(self, url_path: str, params: Dict[str, Any] = None, headers: Dict[str, Any] = None):
        return self._do_request("DELETE", url_path, params=params, headers=headers, timeout=self._timeout)

    def _get(self, url_path: str, params: Dict[str, Any] = None, headers: Dict[str, Any] = None):
        return self._do_request("GET", url_path, params=params, headers=headers, timeout=self._timeout)

    def _post(self, url_path: str, json: Dict[str, Any], params: Dict[str, Any] = None, headers: Dict[str, Any] = None):
        return self._do_request("POST", url_path, json=json, headers=headers, params=params, timeout=self._timeout)

    def _put(self, url_path: str, json: Dict[str, Any] = None, headers: Dict[str, Any] = None):
        return self._do_request("PUT", url_path, json=json, headers=headers, timeout=self._timeout)

    def _do_request(self, method: str, url_path: str, **kwargs):
        full_url = self._resolve_url(url_path)

        json_payload = kwargs.get("json")
        headers = self._headers.copy()
        headers.update(kwargs.get("headers") or {})

        if json_payload:
            data = _json.dumps(json_payload, default=utils.json_dump_default)
            kwargs["data"] = data
            if method in ["PUT", "POST"] and not os.getenv("COGNITE_DISABLE_GZIP", False):
                kwargs["data"] = gzip.compress(data.encode())
                headers["Content-Encoding"] = "gzip"

        kwargs["headers"] = headers

        res = self._request_session.request(method=method, url=full_url, **kwargs)

        if not self._status_is_valid(res.status_code):
            self._raise_API_error(res, payload=json_payload)
        self._log_request(res, payload=json_payload)
        return res

    def _configure_headers(self, additional_headers):
        headers = CaseInsensitiveDict()
        headers.update(requests.utils.default_headers())
        headers["api-key"] = self._api_key
        headers["content-type"] = "application/json"
        headers["accept"] = "application/json"
        headers["x-cdp-sdk"] = "CognitePythonSDK:{}".format(utils.get_current_sdk_version())
        if "User-Agent" in headers:
            headers["User-Agent"] += " " + utils.get_user_agent()
        else:
            headers["User-Agent"] = utils.get_user_agent()
        headers.update(additional_headers)
        return headers

    def _resolve_url(self, url_path: str):
        if not url_path.startswith("/"):
            raise ValueError("URL path must start with '/'")
        full_url = self._base_url + url_path
        # Hack to allow running model hosting requests against local emulator
        full_url = self._apply_model_hosting_emulator_url_filter(full_url)
        return full_url

    def _retrieve(
        self, id: Union[int, str], cls=None, resource_path: str = None, params: Dict = None, headers: Dict = None
    ):
        cls = cls or self._LIST_CLASS._RESOURCE
        resource_path = resource_path or self._RESOURCE_PATH
        return cls._load(
            self._get(
                url_path=utils.interpolate_and_url_encode(resource_path + "/{}", str(id)),
                params=params,
                headers=headers,
            ).json(),
            cognite_client=self._cognite_client,
        )

    def _retrieve_multiple(
        self,
        wrap_ids: bool,
        cls=None,
        resource_path: str = None,
        ids: Union[List[int], int] = None,
        external_ids: Union[List[str], str] = None,
        headers: Dict = None,
    ):
        cls = cls or self._LIST_CLASS
        resource_path = resource_path or self._RESOURCE_PATH
        all_ids = self._process_ids(ids, external_ids, wrap_ids=wrap_ids)
        id_chunks = utils.split_into_chunks(all_ids, self._RETRIEVE_LIMIT)

        tasks = [
            {"url_path": resource_path + "/byids", "json": {"items": id_chunk}, "headers": headers}
            for id_chunk in id_chunks
        ]
        res_list = utils.execute_tasks_concurrently(self._post, tasks, max_workers=self._max_workers)
        retrieved_items = []
        for res in res_list:
            retrieved_items.extend(res.json()["items"])

        if self._is_single_identifier(ids, external_ids):
            return cls._RESOURCE._load(retrieved_items[0], cognite_client=self._cognite_client)
        return cls._load(retrieved_items, cognite_client=self._cognite_client)

    def _list_generator(
        self,
        method: str,
        cls=None,
        resource_path: str = None,
        limit: int = None,
        chunk_size: int = None,
        filter: Dict = None,
        headers: Dict = None,
    ):
        cls = cls or self._LIST_CLASS
        resource_path = resource_path or self._RESOURCE_PATH
        total_items_retrieved = 0
        current_limit = self._LIST_LIMIT
        if chunk_size and chunk_size <= self._LIST_LIMIT:
            current_limit = chunk_size
        next_cursor = None
        filter = filter or {}
        current_items = []
        while True:
            if limit:
                num_of_remaining_items = limit - total_items_retrieved
                if num_of_remaining_items < self._LIST_LIMIT:
                    current_limit = num_of_remaining_items

            if method == "GET":
                params = filter.copy()
                params["limit"] = current_limit
                params["cursor"] = next_cursor
                res = self._get(url_path=resource_path, params=params, headers=headers)
            elif method == "POST":
                body = {"filter": filter, "limit": current_limit, "cursor": next_cursor}
                res = self._post(url_path=resource_path + "/list", json=body, headers=headers)
            else:
                raise ValueError("_list_generator parameter `method` must be GET or POST, not %s", method)
            last_received_items = res.json()["items"]
            current_items.extend(last_received_items)

            if not chunk_size:
                for item in current_items:
                    yield cls._RESOURCE._load(item, cognite_client=self._cognite_client)
                total_items_retrieved += len(current_items)
                current_items = []
            elif len(current_items) >= chunk_size or len(last_received_items) < self._LIST_LIMIT:
                items_to_yield = current_items[:chunk_size]
                yield cls._load(items_to_yield, cognite_client=self._cognite_client)
                total_items_retrieved += len(items_to_yield)
                current_items = current_items[chunk_size:]

            next_cursor = res.json().get("nextCursor")
            if total_items_retrieved == limit or next_cursor is None:
                break

    def _list(
        self,
        method: str,
        cls=None,
        resource_path: str = None,
        limit: int = None,
        filter: Dict = None,
        headers: Dict = None,
    ):
        cls = cls or self._LIST_CLASS
        resource_path = resource_path or self._RESOURCE_PATH
        items = []
        for resource_list in self._list_generator(
            cls=cls,
            resource_path=resource_path,
            method=method,
            limit=limit,
            chunk_size=self._LIST_LIMIT,
            filter=filter,
            headers=headers,
        ):
            items.extend(resource_list.data)
        return cls(items, cognite_client=self._cognite_client)

    def _create_multiple(
        self,
        items: Union[List[Any], Any],
        cls: Any = None,
        resource_path: str = None,
        params: Dict = None,
        headers: Dict = None,
        limit=None,
    ):
        cls = cls or self._LIST_CLASS
        resource_path = resource_path or self._RESOURCE_PATH
        limit = limit or self._CREATE_LIMIT
        single_item = not isinstance(items, list)
        if single_item:
            items = [items]

        items_split = []
        for i in range(0, len(items), limit):
            if isinstance(items[i], CogniteResource):
                items_chunk = [item.dump(camel_case=True) for item in items[i : i + limit]]
            else:
                items_chunk = [item for item in items[i : i + limit]]
            items_split.append({"items": items_chunk})

        tasks = [(resource_path, task_items, params, headers) for task_items in items_split]
        results = utils.execute_tasks_concurrently(self._post, tasks, max_workers=self._max_workers)

        created_resources = []
        for res in results:
            created_resources.extend(res.json()["items"])

        if single_item:
            return cls._RESOURCE._load(created_resources[0], cognite_client=self._cognite_client)
        return cls._load(created_resources, cognite_client=self._cognite_client)

    def _delete_multiple(
        self,
        wrap_ids: bool,
        resource_path: str = None,
        ids: Union[List[int], int] = None,
        external_ids: Union[List[str], str] = None,
        params: Dict = None,
        headers: Dict = None,
    ):
        resource_path = resource_path or self._RESOURCE_PATH
        all_ids = self._process_ids(ids, external_ids, wrap_ids)
        id_chunks = utils.split_into_chunks(all_ids, self._DELETE_LIMIT)
        tasks = [
            {"url_path": resource_path + "/delete", "json": {"items": chunk}, "params": params, "headers": headers}
            for chunk in id_chunks
        ]
        utils.execute_tasks_concurrently(self._post, tasks, max_workers=self._max_workers)

    def _update_multiple(
        self,
        items: Union[List[Any], Any],
        cls: Any = None,
        resource_path: str = None,
        params: Dict = None,
        headers: Dict = None,
    ):
        cls = cls or self._LIST_CLASS
        resource_path = resource_path or self._RESOURCE_PATH
        patch_objects = []
        single_item = not isinstance(items, list)
        if single_item:
            items = [items]

        for item in items:
            if isinstance(item, CogniteResource):
                patch_objects.append(self._convert_resource_to_patch_object(item, cls._UPDATE._get_update_properties()))
            elif isinstance(item, CogniteUpdate):
                patch_objects.append(item.dump())
            else:
                raise ValueError("update item must be of type CogniteResource or CogniteUpdate")
        patch_object_chunks = utils.split_into_chunks(patch_objects, self._UPDATE_LIMIT)

        tasks = [
            {"url_path": resource_path + "/update", "json": {"items": chunk}, "params": params, "headers": headers}
            for chunk in patch_object_chunks
        ]
        res_list = utils.execute_tasks_concurrently(self._post, tasks, max_workers=self._max_workers)

        updated_items = []
        for res in res_list:
            updated_items.extend(res.json()["items"])

        if single_item:
            return cls._RESOURCE._load(updated_items[0], cognite_client=self._cognite_client)
        return cls._load(updated_items, cognite_client=self._cognite_client)

    def _search(
        self, json: Dict, cls: Any = None, resource_path: str = None, params: Dict = None, headers: Dict = None
    ):
        cls = cls or self._LIST_CLASS
        resource_path = resource_path or self._RESOURCE_PATH
        res = self._post(url_path=resource_path + "/search", json=json, params=params, headers=headers)
        return cls._load(res.json()["items"], cognite_client=self._cognite_client)

    @staticmethod
    def _convert_resource_to_patch_object(resource, update_attributes):
        dumped_resource = resource.dump(camel_case=True)
        has_id = "id" in dumped_resource
        has_external_id = "externalId" in dumped_resource
        utils.assert_exactly_one_of_id_or_external_id(dumped_resource.get("id"), dumped_resource.get("externalId"))

        patch_object = {"update": {}}
        if has_id:
            patch_object["id"] = dumped_resource.pop("id")
        elif has_external_id:
            patch_object["externalId"] = dumped_resource.pop("externalId")

        for key, value in dumped_resource.items():
            if key in update_attributes:
                patch_object["update"][key] = {"set": value}
        return patch_object

    @staticmethod
    def _process_ids(
        ids: Union[List[int], int, None], external_ids: Union[List[str], str, None], wrap_ids: bool
    ) -> List:
        if external_ids is None and ids is None:
            raise ValueError("No ids specified")
        if external_ids and not wrap_ids:
            raise ValueError("externalIds must be wrapped")

        if isinstance(ids, int):
            ids = [ids]
        elif isinstance(ids, list) or ids is None:
            ids = ids or []
        else:
            raise TypeError("ids must be int or list of int")

        if isinstance(external_ids, str):
            external_ids = [external_ids]
        elif isinstance(external_ids, list) or external_ids is None:
            external_ids = external_ids or []
        else:
            raise TypeError("external_ids must be str or list of str")

        if wrap_ids:
            ids = [{"id": id} for id in ids]
            external_ids = [{"externalId": external_id} for external_id in external_ids]

        all_ids = ids + external_ids

        return all_ids

    @staticmethod
    def _is_single_identifier(ids, external_ids):
        single_id = isinstance(ids, int) and external_ids is None
        single_external_id = isinstance(external_ids, str) and ids is None
        return single_id or single_external_id

    @staticmethod
    def _status_is_valid(status_code: int):
        return status_code < 400

    @staticmethod
    def _raise_API_error(res: Response, payload: Dict):
        x_request_id = res.headers.get("X-Request-Id")
        code = res.status_code
        extra = {}
        try:
            error = res.json()["error"]
            if isinstance(error, str):
                msg = error
            elif isinstance(error, Dict):
                msg = error["message"]
                extra = error.get("extra", {})
                for key in set(error.keys()) - {"code", "message", "extra"}:
                    extra[key] = error[key]
            else:
                msg = res.content
        except:
            msg = res.content

        error_details = {"X-Request-ID": x_request_id}
        if payload:
            error_details["payload"] = payload
        if extra:
            error_details["extra"] = extra

        log.error("HTTP Error %s %s %s: %s", code, res.request.method, res.request.url, msg, extra=error_details)
        raise CogniteAPIError(msg, code, x_request_id, extra=extra)

    @staticmethod
    def _log_request(res: Response, **kwargs):
        method = res.request.method
        url = res.request.url
        status_code = res.status_code

        extra = kwargs.copy()
        extra["headers"] = res.request.headers.copy()
        if "api-key" in extra.get("headers", {}):
            extra["headers"]["api-key"] = None
        if extra["payload"] is None:
            del extra["payload"]

        http_protocol_version = ".".join(list(str(res.raw.version)))

        log.info("HTTP/{} {} {} {}".format(http_protocol_version, method, url, status_code), extra=extra)

    def _apply_model_hosting_emulator_url_filter(self, full_url):
        mlh_emul_url = os.getenv("MODEL_HOSTING_EMULATOR_URL")
        if mlh_emul_url is not None:
            pattern = "{}/analytics/models(.*)".format(self._base_url)
            res = re.match(pattern, full_url)
            if res is not None:
                path = res.group(1)
                return "{}/projects/{}/models{}".format(mlh_emul_url, self._project, path)
        return full_url
