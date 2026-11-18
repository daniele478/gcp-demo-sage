"""Unit tests for the extra instructions read from Cloud Storage — no GCP calls."""

import pytest

from sage.config import get_app_config
from sage.domain.qa.generation import build_prompt
from sage.integrations.storage import instructions as instructions_module


class _FakeBlob:
    def __init__(self, text: str) -> None:
        self._text = text

    def download_as_text(self, encoding: str = "utf-8") -> str:
        return self._text


class _FakeBucket:
    def __init__(self, blobs: dict[str, str]) -> None:
        self._blobs = blobs

    def blob(self, name: str) -> _FakeBlob:
        return _FakeBlob(self._blobs[name])


class _FakeStorageClient:
    def __init__(self, blobs: dict[str, str]) -> None:
        self._blobs = blobs

    def bucket(self, name: str) -> _FakeBucket:
        return _FakeBucket(self._blobs)


def test_prompt_contains_the_extra_instructions() -> None:
    prompt = build_prompt("Domanda?", [], instructions="# Istruzioni aggiuntive\nSii solenne.")

    assert "# Istruzioni aggiuntive" in prompt
    assert "Sii solenne." in prompt
    assert "Nessuna istruzione aggiuntiva." not in prompt


def test_prompt_marks_missing_instructions() -> None:
    prompt = build_prompt("Domanda?", [])

    assert "Nessuna istruzione aggiuntiva." in prompt
    assert "Nessun documento disponibile" in prompt


def test_read_instructions_is_disabled_without_bucket(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(get_app_config(), "instructions_bucket_name", "")

    assert instructions_module.read_instructions() == ""


def test_read_instructions_returns_the_blob_text(monkeypatch: pytest.MonkeyPatch) -> None:
    config = get_app_config()
    monkeypatch.setattr(config, "instructions_bucket_name", "bucket-istruzioni")
    monkeypatch.setattr(config, "instructions_blob_name", "istruzioni.md")
    monkeypatch.setattr(
        instructions_module,
        "get_storage_client",
        lambda: _FakeStorageClient({"istruzioni.md": "  # Titolo\nTesto  \n"}),
    )

    assert instructions_module.read_instructions() == "# Titolo\nTesto"


def test_read_instructions_degrades_when_the_blob_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = get_app_config()
    monkeypatch.setattr(config, "instructions_bucket_name", "bucket-istruzioni")
    monkeypatch.setattr(config, "instructions_blob_name", "manca.md")
    monkeypatch.setattr(
        instructions_module,
        "get_storage_client",
        lambda: _FakeStorageClient({}),
    )

    assert instructions_module.read_instructions() == ""
