import logging

from pydantic import BaseModel

from helpers.api.wiremock_api import WiremockApi
from helpers.http_helper import HTTPHelper

log = logging.getLogger(__name__)


# Параметры запроса, по которому wiremock будет подбирать подходящую заглушку
class Request(BaseModel):
    urlPath: str = None
    method: str = HTTPHelper.POST
    headers: dict = None
    urlPattern: str = None  # f".*{url}.*",
    queryParameters: dict = (
        None  # {"param_name": {"matches": f".*{param_value_pattern}.*"}}
    )
    bodyPatterns: list = None  # [{"matches": f".*{mapping.body_matcher}.*"}]


# Заглушка, которую должен вернуть wiremock
class Response(BaseModel):
    body: str = None  # f"{json.dumps(mapping.response_data)}"
    jsonBody: dict = None
    status: int = 200
    headers: dict = {"Content-Type": "application/json"}
    transformers: list = None  # ["response-template"]


# Маппинг - объект, который хранит взаимосвязь входящего запроса и соответствующего ему ответа от wiremock
class Mapping(BaseModel):
    name: str
    request: Request
    response: Response


class Mocker:
    def __init__(self):
        self.api = WiremockApi()

    def create_mapping(self, mapping: Mapping):
        log.info(f"Creating mapping with name '{mapping.name}'")
        if mapping.response.body:
            mapping.response.body = f'"{mapping.response.body}"'
        mapping_id = self.api.post_mapping(content=mapping.model_dump())
        log.info(f"Mapping '{mapping.name}' was created: ID={mapping_id}")
        return mapping_id
