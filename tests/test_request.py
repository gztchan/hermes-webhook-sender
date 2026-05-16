import hashlib
import hmac
import json
from unittest.mock import MagicMock, patch

WEBHOOK_URL = "https://example.com/webhook"
SECRET = "test-secret"


def _expected_signature(payload: dict, secret: str) -> str:
    return hmac.new(
        key=secret.encode("utf-8"),
        msg=json.dumps(payload).encode("utf-8"),
        digestmod=hashlib.sha256,
    ).hexdigest()


@patch("request.requests.post")
def test_request_posts_to_configured_url(mock_post, request_module):
    payload = {"event": "ping", "id": 1}
    mock_post.return_value = MagicMock(json=MagicMock(return_value={"ok": True}))

    result = request_module.request(payload)

    mock_post.assert_called_once_with(
        WEBHOOK_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "X-Webhook-Signature": _expected_signature(payload, SECRET),
        },
    )
    assert result == {"ok": True}


@patch("request.requests.post")
def test_request_signature_matches_hmac_sha256(mock_post, request_module):
    payload = {"nested": {"a": 1}, "list": [1, 2]}
    mock_post.return_value = MagicMock(json=MagicMock(return_value={}))

    request_module.request(payload)

    signature = mock_post.call_args.kwargs["headers"]["X-Webhook-Signature"]
    assert signature == _expected_signature(payload, SECRET)
    assert len(signature) == 64


@patch("request.requests.post")
def test_request_returns_response_json(mock_post, request_module):
    payload = {"event": "done"}
    expected = {"status": "accepted", "delivery_id": "abc"}
    mock_post.return_value = MagicMock(json=MagicMock(return_value=expected))

    assert request_module.request(payload) == expected
