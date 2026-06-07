from __future__ import annotations

from subsmith.config import Settings
from subsmith.media.ffmpeg import FfmpegMedia
from subsmith.pipeline import SubtitlePipeline
from subsmith.translation.google import build_google_translator


def build_pipeline(settings: Settings) -> SubtitlePipeline:
    from subsmith.transcription.whisper_transcriber import WhisperTranscriber

    transcriber = WhisperTranscriber(
        model_size=settings.whisper_model,
        device=settings.device,
        compute_type=settings.compute_type,
    )
    translator = build_google_translator(
        source_language=settings.source_language,
        target_language=settings.target_language,
        workers=settings.translation_workers,
        max_retries=settings.translation_max_retries,
    )
    media = FfmpegMedia(
        sample_rate=settings.audio_sample_rate,
        font_size=settings.subtitle_font_size,
    )
    media.ensure_available()
    return SubtitlePipeline(transcriber, translator, media, settings.source_language)
