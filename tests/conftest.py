from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import pytest

from subsmith.models import Segment


class FakeTranscriber:
    def __init__(self, segments: list[Segment]) -> None:
        self._segments = segments
        self.calls: list[tuple[Path, str | None]] = []

    def transcribe(self, audio: Path, language: str | None = None) -> list[Segment]:
        self.calls.append((audio, language))
        return list(self._segments)


class FakeTranslator:
    def __init__(self, mapping: dict[str, str] | None = None) -> None:
        self._mapping = mapping or {}
        self.batches: list[list[str]] = []

    def translate_batch(self, texts: list[str]) -> list[str]:
        self.batches.append(list(texts))
        return [self._mapping.get(text, f"[el] {text}") for text in texts]


class FakeMedia:
    def __init__(self) -> None:
        self.extracted: list[Path] = []
        self.burned: list[tuple[Path, Path, Path]] = []

    def extract_audio(self, video: Path) -> Path:
        self.extracted.append(video)
        return Path(video).with_suffix(".wav")

    def burn_subtitles(self, video: Path, subtitles: Path, output: Path) -> Path:
        self.burned.append((video, subtitles, output))
        return output


class RecordingRunner:
    def __init__(self) -> None:
        self.commands: list[list[str]] = []

    def __call__(self, command: Sequence[str]) -> None:
        self.commands.append(list(command))


@pytest.fixture
def segments() -> list[Segment]:
    return [
        Segment(start=0.0, end=1.5, text="Hello"),
        Segment(start=1.5, end=3.0, text="World"),
    ]
