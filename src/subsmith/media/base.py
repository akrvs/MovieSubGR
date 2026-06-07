from __future__ import annotations

from pathlib import Path
from typing import Protocol


class Media(Protocol):
    def extract_audio(self, video: Path) -> Path: ...

    def burn_subtitles(self, video: Path, subtitles: Path, output: Path) -> Path: ...
