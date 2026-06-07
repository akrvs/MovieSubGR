from __future__ import annotations

import pytest

from subsmith.pipeline import SubtitlePipeline
from tests.conftest import FakeMedia, FakeTranscriber, FakeTranslator


def _video(tmp_path):
    path = tmp_path / "movie.mkv"
    path.write_bytes(b"fake")
    return path


def test_run_produces_translated_subtitles_and_video(tmp_path, segments):
    media = FakeMedia()
    translator = FakeTranslator({"Hello": "Geia", "World": "Kosme"})
    pipeline = SubtitlePipeline(FakeTranscriber(segments), translator, media)

    result = pipeline.run(_video(tmp_path))

    assert [s.translation for s in result.segments] == ["Geia", "Kosme"]
    assert result.subtitles_path.exists()
    assert "Geia" in result.subtitles_path.read_text(encoding="utf-8")
    assert result.output_video.name == "movie_subtitled.mp4"
    assert media.burned[0][2] == result.output_video


def test_run_invokes_stages_in_order(tmp_path, segments):
    media = FakeMedia()
    transcriber = FakeTranscriber(segments)
    pipeline = SubtitlePipeline(transcriber, FakeTranslator(), media, source_language="en")

    pipeline.run(_video(tmp_path))

    assert transcriber.calls[0][1] == "en"
    assert media.extracted and media.burned


def test_run_missing_video_raises(tmp_path):
    pipeline = SubtitlePipeline(FakeTranscriber([]), FakeTranslator(), FakeMedia())
    with pytest.raises(FileNotFoundError):
        pipeline.run(tmp_path / "missing.mp4")


def test_run_empty_transcription_raises(tmp_path):
    pipeline = SubtitlePipeline(FakeTranscriber([]), FakeTranslator(), FakeMedia())
    with pytest.raises(ValueError):
        pipeline.run(_video(tmp_path))


def test_custom_output_paths(tmp_path, segments):
    media = FakeMedia()
    pipeline = SubtitlePipeline(FakeTranscriber(segments), FakeTranslator(), media)
    out = tmp_path / "final.mp4"
    srt_path = tmp_path / "subs.srt"

    result = pipeline.run(_video(tmp_path), output=out, subtitles_path=srt_path)

    assert result.output_video == out
    assert result.subtitles_path == srt_path
