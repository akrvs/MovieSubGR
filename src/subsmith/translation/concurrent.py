from __future__ import annotations

from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor

from tenacity import retry, stop_after_attempt, wait_exponential

TranslateOne = Callable[[str], str]


class ConcurrentTranslator:
    def __init__(
        self,
        translate_one: TranslateOne,
        workers: int = 8,
        max_retries: int = 3,
    ) -> None:
        self._workers = workers

        @retry(
            stop=stop_after_attempt(max_retries + 1),
            wait=wait_exponential(multiplier=0.5, max=8),
            reraise=True,
        )
        def _resilient(text: str) -> str:
            return translate_one(text)

        self._translate_one = _resilient

    def translate_batch(self, texts: list[str]) -> list[str]:
        unique_texts = list(dict.fromkeys(text for text in texts if text.strip()))
        if not unique_texts:
            return list(texts)

        with ThreadPoolExecutor(max_workers=self._workers) as executor:
            translations = list(executor.map(self._translate_one, unique_texts))

        mapping = dict(zip(unique_texts, translations, strict=True))
        return [mapping.get(text, text) for text in texts]
