from __future__ import annotations

from pathlib import Path
from typing import Protocol

from subsmith.models import Segment


class Transcriber(Protocol):
    def transcribe(self, audio: Path, language: str | None = None) -> list[Segment]: ...
