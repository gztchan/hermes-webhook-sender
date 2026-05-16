import importlib
import sys
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parent.parent / "src"


@pytest.fixture
def request_module(monkeypatch):
    monkeypatch.setenv("HERMES_WEBHOOK_URL", "https://example.com/webhook")
    monkeypatch.setenv("HERMES_SECRET", "test-secret")
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))
    import request

    importlib.reload(request)
    return request
