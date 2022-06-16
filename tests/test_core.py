from unittest.mock import Mock, call, patch

from parameterized import parameterized

from postpy2.core import PostRequest


@parameterized.expand(
    [
        (
            "graphql_and_empty_variables",
            {
                "name": "name",
                "url": {"raw": "raw_url"},
                "body": {
                    "mode": "graphql",
                    "graphql": {"query": "{\n  countries {\n    code \n    name\n  }\n}\n", "variables": ""},
                },
                "header": [{"key": "key", "value": "value"}],
                "method": "POST",
            },
            [call(url="raw_url", json={"query": "{\n  countries {\n    code \n    name\n  }\n}\n", "variables": "{}"}, headers={"key": "value"}, method="POST")],
        ),
        (
            "graphql_and_empty_variables_object",
            {
                "name": "name",
                "url": {"raw": "raw_url"},
                "body": {
                    "mode": "graphql",
                    "graphql": {"query": "{\n  countries {\n    code \n    name\n  }\n}\n", "variables": "{}"},
                },
                "header": [{"key": "key", "value": "value"}],
                "method": "POST",
            },
            [call(url="raw_url", json={"query": "{\n  countries {\n    code \n    name\n  }\n}\n", "variables": "{}"}, headers={"key": "value"}, method="POST")],
        ),
        (
            "graphql_with_variables",
            {
                "name": "name",
                "url": {"raw": "raw_url"},
                "body": {
                    "mode": "graphql",
                    "graphql": {"query": "{\n  countries {\n    code \n    name\n  }\n}\n", "variables": "{ 'myvar': 'value' }"},
                },
                "header": [{"key": "key", "value": "value"}],
                "method": "POST",
            },
            [call(url="raw_url", json={"query": "{\n  countries {\n    code \n    name\n  }\n}\n", "variables": "{ 'myvar': 'value' }"}, headers={"key": "value"}, method="POST")],
        ),
    ]
)
@patch("postpy2.core.requests.request")
def test_PostRequest(name, data, expected_request_call, request_mock: Mock):

    mock_post_python = Mock()
    mock_post_python.environments = {}
    mock_post_python.request_overrides = None
    post_request = PostRequest(mock_post_python, data)
    post_request()

    assert expected_request_call == request_mock.call_args_list


@parameterized.expand(
    [
        (
            "with_request_override",
            {"headers": {"RUNTIMEHEADER": "RUNTIMEVALUE"}},
            [call(headers={"myCollectionHeader": "MyCollectionHeaderValue", "RUNTIMEHEADER": "RUNTIMEVALUE"}, method="POST", url="raw_url")],
        ),
        ("no_request_override", None, [call(headers={"myCollectionHeader": "MyCollectionHeaderValue"}, method="POST", url="raw_url")]),
        ("with_existing_keys", {"headers": {"myCollectionHeader": "RUNTIMEVALUE"}}, [call(headers={"myCollectionHeader": "RUNTIMEVALUE"}, method="POST", url="raw_url")]),
    ]
)
@patch("postpy2.core.requests.request")
def test_request_overrides(name: str, request_overrides, expected_request, mock_requests: Mock):

    mock_post_python = Mock()
    mock_post_python.request_overrides = request_overrides
    mock_post_python.environments = {}

    data = {"name": "name", "url": {"raw": "raw_url"}, "method": "POST", "header": [{"key": "myCollectionHeader", "value": "MyCollectionHeaderValue"}]}
    post_request = PostRequest(mock_post_python, data)
    post_request()

    assert mock_requests.call_args_list == expected_request
