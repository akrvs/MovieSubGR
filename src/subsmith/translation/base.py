from __future__ import annotations

from typing import Protocol


class Translator(Protocol):
    def translate_batch(self, texts: list[str]) -> list[str]: ...
