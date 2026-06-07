from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from subsmith.logging import get_logger
from subsmith.media.base import Media
from subsmith.models import Segment
from subsmith.subtitles.srt_writer import write_srt
from subsmith.transcription.base import Transcriber
from subsmith.translation.base import Translator

logger = get_logger(__name__)


@dataclass(slots=True)
class SubtitleResult:
    segments: list[Segment]
    subtitles_path: Path
    output_video: Path


class SubtitlePipeline:
    def __init__(
        self,
        transcriber: Transcriber,
        translator: Translator,
        media: Media,
        source_language: str | None = None,
    ) -> None:
        self._transcriber = transcriber
        self._translator = translator
        self._media = media
        self._source_language = source_language

    def run(
        self,
        video: Path,
        output: Path | None = None,
        subtitles_path: Path | None = None,
    ) -> SubtitleResult:
        video = Path(video)
        if not video.exists():
            raise FileNotFoundError(f"Video not found: {video}")

        output = output or video.with_name(f"{video.stem}_subtitled.mp4")
        subtitles_path = subtitles_path or video.with_suffix(".srt")

        logger.info("Extracting audio from %s", video.name)
        audio = self._media.extract_audio(video)

        logger.info("Transcribing audio")
        segments = self._transcriber.transcribe(audio, language=self._source_language)
        if not segments:
            raise ValueError("Transcription produced no segments")
        logger.info("Transcribed %d segments", len(segments))

        logger.info("Translating %d segments", len(segments))
        translations = self._translator.translate_batch([segment.text for segment in segments])
        translated = [
            segment.with_translation(translation)
            for segment, translation in zip(segments, translations, strict=True)
        ]

        logger.info("Writing subtitles to %s", subtitles_path.name)
        write_srt(translated, subtitles_path)

        logger.info("Burning subtitles into %s", output.name)
        self._media.burn_subtitles(video, subtitles_path, output)

        return SubtitleResult(
            segments=translated,
            subtitles_path=subtitles_path,
            output_video=output,
        )
