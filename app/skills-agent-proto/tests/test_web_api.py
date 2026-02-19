"""Web API tests for FastAPI + SSE bridge."""

from __future__ import annotations

import json
from typing import Iterator

from fastapi.testclient import TestClient

from langchain_skills.web_api import _parse_cors_origins, create_app


class FakeAgent:
    """Deterministic test double for API tests."""

    def get_discovered_skills(self):
        return [
            {
                "name": "news-extractor",
                "description": "Extract article content from news links",
                "path": "/tmp/skills/news-extractor",
            }
        ]

    def get_system_prompt(self) -> str:
        return "You are a test agent."

    def stream_events(self, message: str, thread_id: str = "default") -> Iterator[dict]:
        if message == "explode":
            raise RuntimeError("boom")

        yield {"type": "thinking", "content": "Thinking...", "id": 0}
        yield {"type": "tool_call", "name": "load_skill", "args": {"skill_name": "news-extractor"}, "id": "tool-1"}
        yield {"type": "tool_result", "name": "load_skill", "content": "[OK]\n\nloaded", "success": True}
        yield {"type": "text", "content": "Done."}
        yield {"type": "done", "response": "Done."}


def _read_sse_text(client: TestClient, url: str) -> str:
    with client.stream("GET", url) as response:
        assert response.status_code == 200
        chunks = [chunk for chunk in response.iter_text() if chunk]
    return "".join(chunks)


def test_health_endpoint():
    app = create_app(agent_provider=FakeAgent)
    client = TestClient(app)

    response = client.get("/api/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert "api_credentials_configured" in payload


def test_skills_endpoint():
    app = create_app(agent_provider=FakeAgent)
    client = TestClient(app)

    response = client.get("/api/skills")
    assert response.status_code == 200
    payload = response.json()
    assert "skills" in payload
    assert payload["skills"][0]["name"] == "news-extractor"


def test_prompt_endpoint():
    app = create_app(agent_provider=FakeAgent)
    client = TestClient(app)

    response = client.get("/api/prompt")
    assert response.status_code == 200
    payload = response.json()
    assert payload["prompt"] == "You are a test agent."


def test_chat_stream_endpoint_emits_sse_frames():
    app = create_app(agent_provider=FakeAgent)
    client = TestClient(app)

    text = _read_sse_text(client, "/api/chat/stream?message=hello&thread_id=t-1")

    assert "event: thinking" in text
    assert "event: tool_call" in text
    assert "event: tool_result" in text
    assert "event: text" in text
    assert "event: done" in text
    assert '"skill_name": "news-extractor"' in text


def test_chat_stream_endpoint_wraps_errors_as_error_event():
    app = create_app(agent_provider=FakeAgent)
    client = TestClient(app)

    text = _read_sse_text(client, "/api/chat/stream?message=explode&thread_id=t-1")

    assert "event: agent_error" in text
    assert "boom" in text


def test_chat_stream_requires_message():
    app = create_app(agent_provider=FakeAgent)
    client = TestClient(app)

    response = client.get("/api/chat/stream")
    assert response.status_code == 422


def test_chat_stream_frame_payload_is_valid_json():
    app = create_app(agent_provider=FakeAgent)
    client = TestClient(app)

    text = _read_sse_text(client, "/api/chat/stream?message=hello&thread_id=t-1")

    lines = [line for line in text.splitlines() if line.startswith("data: ")]
    assert lines, "expected at least one data line"

    for line in lines:
        json.loads(line.replace("data: ", "", 1))


# --- _parse_cors_origins tests ---


def test_parse_cors_origins_returns_defaults_when_none():
    result = _parse_cors_origins(None)
    assert "http://localhost:5173" in result
    assert "http://127.0.0.1:5173" in result


def test_parse_cors_origins_returns_defaults_when_empty_string():
    result = _parse_cors_origins("")
    assert "http://localhost:5173" in result


def test_parse_cors_origins_parses_custom_origins():
    result = _parse_cors_origins("https://example.com,https://app.test")
    assert result == ["https://example.com", "https://app.test"]


def test_parse_cors_origins_strips_whitespace():
    result = _parse_cors_origins("  https://a.com , https://b.com  ")
    assert result == ["https://a.com", "https://b.com"]


def test_parse_cors_origins_skips_empty_entries():
    result = _parse_cors_origins(",,,https://a.com,,,")
    assert result == ["https://a.com"]


def test_parse_cors_origins_falls_back_on_all_whitespace():
    result = _parse_cors_origins("  ,  ,  ")
    assert "http://localhost:5173" in result
