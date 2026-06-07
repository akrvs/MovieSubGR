from __future__ import annotations

import shutil
import subprocess
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Protocol

CommandRunner = Callable[[Sequence[str]], None]


class FfmpegError(RuntimeError):
    pass


class _Runner(Protocol):
    def __call__(self, command: Sequence[str]) -> None: ...


def _default_runner(command: Sequence[str]) -> None:
    subprocess.run(list(command), check=True, capture_output=True)


def _escape_subtitle_path(path: Path) -> str:
    return str(path).replace("\\", "\\\\").replace(":", r"\:").replace("'", r"\'")


class FfmpegMedia:
    def __init__(
        self,
        sample_rate: int = 16000,
        font_size: int = 24,
        normalize: bool = True,
        binary: str = "ffmpeg",
        runner: _Runner = _default_runner,
    ) -> None:
        self._sample_rate = sample_rate
        self._font_size = font_size
        self._normalize = normalize
        self._binary = binary
        self._runner = runner

    def ensure_available(self) -> None:
        if shutil.which(self._binary) is None:
            raise FfmpegError(f"'{self._binary}' was not found on PATH")

    def extract_audio(self, video: Path) -> Path:
        video = Path(video)
        audio_path = video.with_suffix(".wav")
        command = [self._binary, "-y", "-i", str(video), "-vn"]
        if self._normalize:
            command += ["-af", "loudnorm"]
        command += [
            "-acodec",
            "pcm_s16le",
            "-ar",
            str(self._sample_rate),
            "-ac",
            "1",
            str(audio_path),
        ]
        self._runner(command)
        return audio_path

    def burn_subtitles(self, video: Path, subtitles: Path, output: Path) -> Path:
        video, subtitles, output = Path(video), Path(subtitles), Path(output)
        escaped = _escape_subtitle_path(subtitles)
        style = f"subtitles={escaped}:force_style='Fontsize={self._font_size}'"
        command = [
            self._binary,
            "-y",
            "-i",
            str(video),
            "-vf",
            style,
            "-c:a",
            "copy",
            str(output),
        ]
        self._runner(command)
        return output
