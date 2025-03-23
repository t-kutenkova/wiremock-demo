import logging
from copy import deepcopy
from typing import Iterable, Union

import requests
import urllib3
from requests import ConnectionError, HTTPError, Timeout, TooManyRedirects
from requests.auth import HTTPBasicAuth

from helpers.dot_proxy import DotProxy

log = logging.getLogger(__name__)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class HTTPHelper:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

    HTTP_PORT = 80
    HTTPS_PORT = 443

    HTTP = "http"
    HTTPS = "https"

    HEADERS = {"Accept": "application/json;charset=UTF-8"}

    def __init__(
        self,
        host,
        protocol=HTTPS,
        port=None,
        headers=None,
        header_sanitizers=None,
        username=None,
        password=None,
        s_cert=False,
        c_cert=None,
        c_key=None,
    ):
        self.base_url = f"{protocol}://{host}:{port}"
        if not port:
            self.base_url = f"{protocol}://{host}"
        self.headers = headers or self.HEADERS
        self.header_sanitizers = header_sanitizers  # Ex: ['Authorization']
        if username and password:
            self.auth = HTTPBasicAuth(username, password)
        else:
            self.auth = None
        self.verify = s_cert
        if c_cert and c_key:
            self.cert = (c_cert, c_key)
        else:
            self.cert = None

    def requester(
        self,
        method: str,
        rel_url: str,
        headers: dict = None,
        data: dict = None,
        params: dict = None,
        json: dict = None,
        files: dict = None,
        expected_error=None,
    ):
        url = f"{self.base_url}{rel_url}"
        log.debug(
            "-------------------- HTTP_REQUEST_BEGIN_SESSION --------------------"
        )
        log.debug(f"URL: {url}")
        log.debug(f"METHOD: {method}")
        if params:
            log.debug(f"PARAMS: {params}")
        if data:
            log.debug(f"DATA: {data}")
        if json:
            log.debug(f"JSON: {json}")
        response = requests.request(
            method,
            url,
            headers=headers or self.headers,
            data=data,
            json=json,
            params=params,
            cert=self.cert,
            verify=self.verify,
            auth=self.auth,
            files=files,
        )
        if self.header_sanitizers:
            sanitized_headers = self._sanitize_data_by_keys(
                dict(response.request.headers), sensitive_keys=self.header_sanitizers
            )
            response_copy = deepcopy(response)
            response_copy.request.headers.update(sanitized_headers)
            headers = sanitized_headers

        log.debug(f"HEADERS: {headers}")
        log.debug(f"RESPONSE CODE: {response.status_code}")
        try:
            response.raise_for_status()
        except (Timeout, ConnectionError, TooManyRedirects, HTTPError) as e:
            log.error(response.text)
            if expected_error and expected_error in str(e):
                log.warning(f"Expected error: {e}")
                return
            else:
                raise e
        return self._parse(response)

    def get(self, url: str, **kwargs):
        return self.requester(self.GET, url, **kwargs)

    def post(self, url: str, **kwargs):
        return self.requester(self.POST, url, **kwargs)

    def put(self, url: str, **kwargs):
        return self.requester(self.PUT, url, **kwargs)

    def delete(self, url: str, **kwargs):
        return self.requester(self.DELETE, url, **kwargs)

    def _parse(self, response):
        content = response.content
        if response.headers.get("Content-Type") in [
            "application/json",
            "application/json;charset=UTF-8",
            "text/plain; charset=utf-8",
        ] or "application/json" in str(response.request.headers):
            try:
                content = response.json()
                log.debug(f"RESPONSE DATA: {content}")
            except requests.JSONDecodeError:
                # We don't log non-json response since it could be not readable and large (if it's a file content for example)
                pass
        log.debug("-------------------- HTTP_REQUEST_END_SESSION --------------------")
        return content

    # Modified autotest_client.helper.sanitizers.sanitize_data_by_keys() due to cfg var existence
    @staticmethod
    def _sanitize_data_by_keys(
        value_to_sanitize: Union[dict, Iterable],
        sensitive_keys: Iterable,
        raise_on_miss: bool = False,
    ) -> Union[dict, Iterable]:
        value = deepcopy(value_to_sanitize)
        data_proxy = DotProxy(value, strict=raise_on_miss)

        for sensitive_key in sensitive_keys:
            try:
                value = data_proxy[sensitive_key]
            except KeyError:
                if raise_on_miss:
                    raise
                continue
            if not value:
                continue
            data_proxy[sensitive_key] = "****"

        return data_proxy.data
