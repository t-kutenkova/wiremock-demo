import logging
import os
import sys

sys.path.append(f"{os.path.dirname(os.path.abspath(__file__))}/../..")

from helpers.http_helper import HTTPHelper

log = logging.getLogger(__name__)


class WiremockApi:
    DEFAULT_PORT = 8080

    def __init__(self, host: str = "localhost", port: str = DEFAULT_PORT):
        self._http = HTTPHelper(
            host=host, protocol=HTTPHelper.HTTP, port=port or self.DEFAULT_PORT
        )

    def get_mappings(self):
        return self._http.get(url="/__admin/mappings")

    def get_mapping(self, id: str):
        return self._http.get(url=f"/__admin/mappings/{id}")

    def put_mapping(self, id: str, content: dict):
        return self._http.put(url=f"/__admin/mappings/{id}", json=content)["id"]

    def post_mapping(self, content: dict):
        return self._http.post(url="/__admin/mappings", json=content)["id"]

    def delete_mapping(self, id: str):
        return self._http.delete(url=f"/__admin/mappings/{id}")

    def delete_all_mappings(self):
        return self._http.delete(url="/__admin/mappings")
