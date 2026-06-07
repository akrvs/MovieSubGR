from __future__ import annotations

from pathlib import Path

import typer

from subsmith.config import get_settings
from subsmith.logging import configure_logging

app = typer.Typer(help="Subsmith subtitle generation pipeline", no_args_is_help=True)


@app.command()
def run(
    video: Path,
    output: Path | None = typer.Option(None, help="Output video path"),
    subtitles: Path | None = typer.Option(None, help="Output .srt path"),
    target: str | None = typer.Option(None, help="Target language code"),
    model: str | None = typer.Option(None, help="Whisper model size"),
) -> None:
    settings = get_settings()
    if target:
        settings = settings.model_copy(update={"target_language": target})
    if model:
        settings = settings.model_copy(update={"whisper_model": model})
    configure_logging(settings.log_level)

    from subsmith.factory import build_pipeline

    pipeline = build_pipeline(settings)
    result = pipeline.run(video, output=output, subtitles_path=subtitles)
    typer.echo(f"Subtitles: {result.subtitles_path}")
    typer.echo(f"Video: {result.output_video}")


@app.command()
def transcribe(
    video: Path,
    subtitles: Path | None = typer.Option(None, help="Output .srt path"),
    model: str | None = typer.Option(None, help="Whisper model size"),
) -> None:
    settings = get_settings()
    if model:
        settings = settings.model_copy(update={"whisper_model": model})
    configure_logging(settings.log_level)

    from subsmith.media.ffmpeg import FfmpegMedia
    from subsmith.subtitles.srt_writer import write_srt
    from subsmith.transcription.whisper_transcriber import WhisperTranscriber

    media = FfmpegMedia(sample_rate=settings.audio_sample_rate)
    media.ensure_available()
    audio = media.extract_audio(video)
    transcriber = WhisperTranscriber(
        model_size=settings.whisper_model,
        device=settings.device,
        compute_type=settings.compute_type,
    )
    segments = transcriber.transcribe(audio, language=settings.source_language)
    output = subtitles or video.with_suffix(".srt")
    write_srt(segments, output)
    typer.echo(f"Subtitles: {output}")


if __name__ == "__main__":
    app()
