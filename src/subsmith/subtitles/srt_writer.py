from __future__ import annotations

from datetime import timedelta
from pathlib import Path

import srt

from subsmith.models import Segment


def segments_to_srt(segments: list[Segment]) -> str:
    entries = [
        srt.Subtitle(
            index=index,
            start=timedelta(seconds=segment.start),
            end=timedelta(seconds=segment.end),
            content=segment.display_text,
        )
        for index, segment in enumerate(segments, start=1)
    ]
    return srt.compose(entries)


def write_srt(segments: list[Segment], output: Path) -> Path:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(segments_to_srt(segments), encoding="utf-8")
    return output
