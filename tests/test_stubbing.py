import json
import logging

from assertpy import assert_that
from pytest_cases import case, parametrize_with_cases

from helpers.http_helper import HTTPHelper
from helpers.mocker import Mapping, Mocker, Request, Response
from tests.conftest import log_info_blue, log_info_magenta

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class StubbingCases:
    @case(id="StubbingCases [stub] string body")
    def case_stubbing__string_body_stub(self):
        # Создаем стаб
        mapping = Mapping(
            name="[stub] string body",
            request=Request(method="GET", urlPath="/my-first-string-mapping"),
            response=Response(
                body="Your first mapping is awesome!",
                headers={"Content-Type": "text/plain; charset=utf-8"},
            ),
        )
        check_request = dict(method=HTTPHelper.GET, rel_url="/my-first-string-mapping")
        expected_response = "Your first mapping is awesome!"
        return mapping, check_request, expected_response

    @case(id="StubbingCases [stub] json body")
    def case_stubbing__json_body_stub(self):
        # Создаем стаб
        mapping = Mapping(
            name="[stub] json body",
            request=Request(method="GET", urlPath="/my-first-json-mapping"),
            response=Response(
                jsonBody={"Your first mapping": "is awesome!"},
                headers={"Content-Type": "application/json"},
            ),
        )
        check_request = dict(method=HTTPHelper.GET, rel_url="/my-first-json-mapping")
        expected_response = {"Your first mapping": "is awesome!"}
        return mapping, check_request, expected_response


class RequestMatchingCases:
    @case(id="RequestMatchingCases [matching] url with params")
    def case_matching_url_with_params(self):
        mapping = Mapping(
            name="[mapping] url with params",
            request=Request(
                method="GET",
                urlPath="/url-equalty",
                queryParameters={"limit": {"equalTo": "1"}},
            ),
            response=Response(
                body="URL with params matching successfully checked!",
                headers={"Content-Type": "text/plain"},
            ),
        )
        check_request = dict(method=HTTPHelper.GET, rel_url="/url-equalty?limit=1")
        expected_response = "URL with params matching successfully checked!"
        return mapping, check_request, expected_response

    @case(id="RequestMatchingCases [matching] url with regex")
    def case_matching_url_with_regex(self):
        mapping = Mapping(
            name="[mapping] url with regex",
            request=Request(method="GET", urlPattern="/url-equalty/[a-z]*"),
            response=Response(
                body="URL with regex matching successfully checked!",
                headers={"Content-Type": "text/plain"},
            ),
        )
        check_request = dict(method=HTTPHelper.GET, rel_url="/url-equalty/mytestregex")
        expected_response = "URL with regex matching successfully checked!"
        return mapping, check_request, expected_response

    @case(id="RequestMatchingCases [matching] headers")
    def case_matching_headers(self):
        mapping = Mapping(
            name="[mapping] headers",
            request=Request(
                method="GET",
                urlPath="/headers-matching-check",
                headers={"Content-Type": {"equalTo": "application/json"}},
            ),
            response=Response(
                body="Content-Type is application/json",
                headers={"Content-Type": "text/plain"},
            ),
        )
        check_request = dict(
            method=HTTPHelper.GET,
            rel_url="/headers-matching-check",
            headers={"Content-Type": "application/json"},
        )
        expected_response = "Content-Type is application/json"
        return mapping, check_request, expected_response

    @case(id="RequestMatchingCases [matching] cookies")
    def case_matching_cookies(self):
        mapping = Mapping(
            name="[mapping] cookies",
            request=Request(
                method="GET",
                urlPath="/cookies-matching-check",
                headers={"Cookie": {"contains": "my_profile=ivanivanov@example.com"}},
            ),
            response=Response(
                body="Cookies for Ivan Ivanov are present",
                headers={"Content-Type": "text/plain; charset=utf-8"},
            ),
        )
        check_request = dict(
            method=HTTPHelper.GET,
            rel_url="/cookies-matching-check",
            headers={"Cookie": "my_profile=ivanivanov@example.com"},
        )
        expected_response = "Cookies for Ivan Ivanov are present"
        return mapping, check_request, expected_response


class ResponseTemplatingCases:
    @case(id="ResponseTemplatingCases [stub] request model")
    def case_request_model(self):
        mapping = Mapping(
            name="[stub] request model",
            request=Request(
                method="POST",
                url="/response/templating",
                queryParameters={"my_param": {"equalTo": "my_value"}},
            ),
            response=Response(
                status=200,
                headers={"Content-Type": "application/json"},
                transformers=["response-template"],
                jsonBody={
                    "request.url": "{{request.url}}",
                    "request.path": "{{request.path}}",
                    "request.pathSegments.[1]": "{{request.pathSegments.[1]}}",
                    "request.query.my_param": "{{request.query.my_param}}",
                    "request.method": "{{request.method}}",
                    "request.baseUrl": "{{request.baseUrl}}",
                    "request.headers.my_header": "{{request.headers.my_header}}",
                    "request.body": "{{request.body}}",
                },
            ),
        )
        check_request = dict(
            method="POST",
            rel_url="/response/templating?my_param=my_value",
            headers={"my_header": "my_header_value"},
            data="my_body",
        )
        expected_response = {
            "request.url": "/response/templating?my_param=my_value",
            "request.path": "/response/templating",
            "request.pathSegments.[1]": "templating",
            "request.query.my_param": "my_value",
            "request.method": "POST",
            "request.baseUrl": "http://localhost:8080",
            "request.headers.my_header": "my_header_value",
            "request.body": "my_body",
        }
        return mapping, check_request, expected_response

    @case(id="ResponseTemplatingCases [stub] helpers math & vars")
    def case_helpers_math_vars(self):
        mapping = Mapping(
            name="[stub] helpers math & vars",
            request=Request(
                method="POST", url="/response/templating/helpers-conditions"
            ),
            response=Response(
                status=200,
                headers={"Content-Type": "application/json"},
                transformers=["response-template"],
                jsonBody={
                    "create_var_for_body_example": "{{val request.body assign='my_var'}}my_var={{my_var}}",
                    "sum_with_10_example": "{{val (math my_var '+' 10) assign='my_sum'}}my_sum={{my_sum}}",
                    "create_var_for_array_example": "{{val (array 1 2 3) assign='my_var_for_array'}}my_var_for_array={{my_var_for_array}}",
                },
            ),
        )
        check_request = dict(
            method="POST", rel_url="/response/templating/helpers-conditions", data="4"
        )
        expected_response_start = {
            "create_var_for_body_example": "my_var=4",
            "sum_with_10_example": "my_sum=14",
            "create_var_for_array_example": "my_var_for_array=[1, 2, 3]",
        }
        return mapping, check_request, expected_response_start

    @case(id="ResponseTemplatingCases [stub] helpers strings")
    def case_helpers_strings(self):
        mapping = Mapping(
            name="[stub] helpers strings",
            request=Request(
                method="POST", urlPath="/response/templating/helpers-strings"
            ),
            response=Response(
                status=200,
                headers={"Content-Type": "application/json"},
                transformers=["response-template"],
                jsonBody={
                    "capitalize_example": "{{capitalize request.body}}",
                    "contains_example": "{{contains request.body 'body'}}",
                    "abbreviate_example": "{{abbreviate request.body 10}}",
                    "replace_example": "{{replace request.body 'body' 'replacement'}}",
                    "cut_example": "{{cut request.body ' my %s'}}",
                    "string_format_example": "{{stringFormat request.body 'cool'}}",
                    "default_if_empty_example": "{{defaultIfEmpty request.body 'this is default response' }}",
                },
            ),
        )
        check_request = dict(
            method="POST",
            rel_url="/response/templating/helpers-strings",
            data="this is my %s body",
        )
        expected_response = {
            "capitalize_example": "This Is My %s Body",
            "contains_example": "true",
            "abbreviate_example": "this is...",
            "replace_example": "this is my %s replacement",
            "cut_example": "this is body",
            "string_format_example": "this is my cool body",
            "default_if_empty_example": "this is my %s body",
        }
        return mapping, check_request, expected_response

    @case(id="ResponseTemplatingCases [stub] helpers conditions")
    def case_helpers_conditions(self):
        mapping = Mapping(
            name="[stub] helpers conditions",
            request=Request(
                method="POST", url="/response/templating/helpers-conditions"
            ),
            response=Response(
                status=200,
                headers={"Content-Type": "application/json"},
                transformers=["response-template"],
                jsonBody={
                    "if_else_example": "{{#if request.body}}Body is NOT empty!{{else}}Body is empty!{{/if}}",
                    "contains_example": "{{#if}}{{#contains (array 'apple' 'orange' 'banana') request.body}}Item is on the list!{{/contains}}{{/if}}",
                    "matches_example": "{{#if (matches request.body 'ap.*le')}}Regex was matched!{{/if}}",
                    "equal_example": "{{eq request.body 'apple' yes='Yes! :)' no='No! :('}}",
                    "equal_with_else_example": "{{#eq request.body 'apple'}}Body equals 'apple'{{else}}Body does not equal 'apple'{{/eq}}",
                },
            ),
        )
        check_request = dict(
            method="POST",
            rel_url="/response/templating/helpers-conditions",
            data="apple",
        )
        expected_response = {
            "if_else_example": "Body is NOT empty!",
            "contains_example": "Item is on the list!",
            "matches_example": "Regex was matched!",
            "equal_example": "Yes! :)",
            "equal_with_else_example": "Body equals 'apple'",
        }
        return mapping, check_request, expected_response


class TestMocking:
    @parametrize_with_cases(
        "case", cases=[StubbingCases, RequestMatchingCases, ResponseTemplatingCases]
    )
    def test_mocking(self, mocker: Mocker, http: HTTPHelper, case, current_cases):
        mapping, check_request, expected_response = case
        log_info_magenta(f"Test title: {current_cases['case'].id}")

        log_info_blue("1. Create stub")
        log.info(f"\nMapping: {mapping.model_dump_json(indent=2, exclude_none=True)}")
        mocker.create_mapping(mapping)

        log_info_blue("2. Check stub")
        log.info(f"\nRequest: {json.dumps(check_request, indent=2, allow_nan=False)}")
        log.info(f"\nExpected response: {expected_response}")
        data = http.requester(**check_request)
        assert_that(data).is_equal_to(expected_response)
