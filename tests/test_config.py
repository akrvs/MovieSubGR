from __future__ import annotations

from subsmith.config import Settings


def test_defaults_target_greek():
    settings = Settings()
    assert settings.target_language == "el"
    assert settings.whisper_model == "small"


def test_env_overrides(monkeypatch):
    monkeypatch.setenv("SUBSMITH_TARGET_LANGUAGE", "fr")
    monkeypatch.setenv("SUBSMITH_WHISPER_MODEL", "medium")
    monkeypatch.setenv("SUBSMITH_TRANSLATION_WORKERS", "16")
    settings = Settings()
    assert settings.target_language == "fr"
    assert settings.whisper_model == "medium"
    assert settings.translation_workers == 16
