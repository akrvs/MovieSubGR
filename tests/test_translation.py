from __future__ import annotations

import threading

import pytest

from subsmith.translation.concurrent import ConcurrentTranslator


def test_preserves_order():
    translator = ConcurrentTranslator(lambda text: text.upper(), workers=4)
    assert translator.translate_batch(["a", "b", "c"]) == ["A", "B", "C"]


def test_deduplicates_repeated_texts():
    calls: list[str] = []
    lock = threading.Lock()

    def translate_one(text: str) -> str:
        with lock:
            calls.append(text)
        return text.upper()

    translator = ConcurrentTranslator(translate_one, workers=4)
    result = translator.translate_batch(["a", "a", "b", "a"])

    assert result == ["A", "A", "B", "A"]
    assert sorted(calls) == ["a", "b"]


def test_retries_transient_failures():
    attempts = {"count": 0}

    def flaky(text: str) -> str:
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise RuntimeError("transient")
        return text.upper()

    translator = ConcurrentTranslator(flaky, workers=1, max_retries=3)
    assert translator.translate_batch(["a"]) == ["A"]
    assert attempts["count"] == 3


def test_raises_after_exhausting_retries():
    def always_fails(text: str) -> str:
        raise RuntimeError("permanent")

    translator = ConcurrentTranslator(always_fails, workers=1, max_retries=1)
    with pytest.raises(RuntimeError):
        translator.translate_batch(["a"])


def test_blank_text_is_passed_through():
    translator = ConcurrentTranslator(lambda text: text.upper(), workers=2)
    assert translator.translate_batch(["", "  "]) == ["", "  "]
