from __future__ import annotations

import srt

from subsmith.models import Segment
from subsmith.subtitles.srt_writer import segments_to_srt, write_srt


def test_srt_contains_translated_text():
    segments = [Segment(start=0, end=1, text="hello").with_translation("geia")]
    output = segments_to_srt(segments)
    assert "geia" in output
    assert "hello" not in output


def test_srt_is_parseable_and_indexed():
    segments = [
        Segment(start=0.0, end=1.0, text="a"),
        Segment(start=1.0, end=2.0, text="b"),
    ]
    parsed = list(srt.parse(segments_to_srt(segments)))
    assert [entry.index for entry in parsed] == [1, 2]
    assert parsed[0].content == "a"


def test_srt_timing_is_formatted():
    segments = [Segment(start=3661.0, end=3662.5, text="x")]
    output = segments_to_srt(segments)
    assert "01:01:01,000 --> 01:01:02,500" in output


def test_write_srt_creates_file(tmp_path):
    segments = [Segment(start=0, end=1, text="hello")]
    path = write_srt(segments, tmp_path / "nested" / "out.srt")
    assert path.exists()
    assert "hello" in path.read_text(encoding="utf-8")
