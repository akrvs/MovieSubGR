from __future__ import annotations

from subsmith.translation.concurrent import ConcurrentTranslator


def build_google_translator(
    source_language: str | None,
    target_language: str,
    workers: int = 8,
    max_retries: int = 3,
) -> ConcurrentTranslator:
    from deep_translator import GoogleTranslator

    source = source_language or "auto"

    def translate_one(text: str) -> str:
        return GoogleTranslator(source=source, target=target_language).translate(text)

    return ConcurrentTranslator(translate_one, workers=workers, max_retries=max_retries)
