from __future__ import annotations

from pathlib import Path

from subsmith.media.ffmpeg import FfmpegMedia
from tests.conftest import RecordingRunner


def test_extract_audio_builds_mono_pcm_command():
    runner = RecordingRunner()
    media = FfmpegMedia(sample_rate=16000, runner=runner)

    audio = media.extract_audio(Path("/videos/clip.mkv"))

    assert audio == Path("/videos/clip.wav")
    command = runner.commands[0]
    assert "-ac" in command and command[command.index("-ac") + 1] == "1"
    assert command[command.index("-ar") + 1] == "16000"
    assert "loudnorm" in command


def test_extract_audio_can_disable_normalization():
    runner = RecordingRunner()
    media = FfmpegMedia(normalize=False, runner=runner)
    media.extract_audio(Path("clip.mp4"))
    assert "loudnorm" not in runner.commands[0]


def test_burn_subtitles_builds_filter_command():
    runner = RecordingRunner()
    media = FfmpegMedia(font_size=28, runner=runner)

    output = media.burn_subtitles(Path("clip.mp4"), Path("subs.srt"), Path("out.mp4"))

    assert output == Path("out.mp4")
    command = runner.commands[0]
    vf = command[command.index("-vf") + 1]
    assert "subtitles=" in vf
    assert "Fontsize=28" in vf
