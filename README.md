# Subsmith

Subsmith turns any video into a subtitled video in one command. It extracts and loudness-normalizes the audio, transcribes speech with Whisper, translates each line into the target language, and burns clean subtitles back into the video.

[![CI](https://github.com/akrvs/Subsmith/actions/workflows/ci.yml/badge.svg)](https://github.com/akrvs/Subsmith/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Problem

Generating translated subtitles is a multi-stage media problem: demux audio, run speech-to-text with accurate timestamps, translate hundreds of short lines, serialize valid SRT timing, and re-encode the video with a burned-in track. Doing this naively breaks in predictable ways. Translating one segment per blocking network call makes a feature-length film take many minutes and fall over on the first transient error. A single hard-coded path and a flat script make the tool impossible to reuse or test. Subsmith treats the workflow as a real pipeline with isolated, swappable stages.

## Approach

```
 video ──> [ffmpeg extract + loudnorm] ──> audio
                                             │
                                             v
                                     [Whisper STT] ──> timed segments
                                             │
                                             v
                            [concurrent translator] ──> translated segments
                                             │
                                             v
                                      [SRT writer] ──> .srt
                                             │
                                             v
                            [ffmpeg burn-in] ──> subtitled video
```

Each stage sits behind a small interface (`Transcriber`, `Translator`, `Media`), and `SubtitlePipeline` wires them together. Because the stages are decoupled, every backend can be swapped and the orchestration can be tested without ffmpeg, model weights, or a network.

## Design decisions

- **Concurrent, resilient translation.** The original approach issued one blocking call per subtitle line. Subsmith deduplicates repeated lines, fans the unique set out across a thread pool, and wraps each call in exponential-backoff retries, then reassembles results in the original order. Fewer calls, faster runs, and tolerance for transient API failures.
- **faster-whisper over openai-whisper.** The CTranslate2 backend is several times faster on CPU at equal model size and exposes word-accurate segment timestamps that map directly onto SRT cues.
- **Honest audio handling.** The legacy "noise reduction" step only normalized levels with pydub (a dependency that no longer builds on modern Python). Subsmith performs EBU R128 loudness normalization with ffmpeg's `loudnorm` filter during extraction, removing the extra dependency and naming the step for what it does.
- **Pluggable translation backend.** Google Translate (no API key) is the default so the tool runs out of the box, but `Translator` is an interface; a DeepL or LLM backend drops in without touching the pipeline.
- **Typed configuration.** Pydantic settings (`SUBSMITH_*`) control model size, languages, concurrency, and styling with no code edits.

## Quick start

```bash
pip install -e ".[transcription]"

subsmith run movie.mkv
subsmith run movie.mkv --target fr --model medium
subsmith transcribe movie.mkv --subtitles movie.srt
```

ffmpeg must be installed and on `PATH`. The first run downloads the selected Whisper model once.

### Docker

```bash
docker build -t subsmith .
docker run --rm -v "$PWD:/work" -w /work subsmith run movie.mkv
```

The image ships with ffmpeg preinstalled.

## Configuration

| Variable                          | Default | Description                              |
| --------------------------------- | ------- | ---------------------------------------- |
| `SUBSMITH_WHISPER_MODEL`          | `small` | Whisper model size                       |
| `SUBSMITH_SOURCE_LANGUAGE`        | auto    | Force a source language, or autodetect   |
| `SUBSMITH_TARGET_LANGUAGE`        | `el`    | Translation target language code         |
| `SUBSMITH_TRANSLATION_WORKERS`    | `8`     | Concurrent translation workers           |
| `SUBSMITH_TRANSLATION_MAX_RETRIES`| `3`     | Retries per line on transient failure    |
| `SUBSMITH_SUBTITLE_FONT_SIZE`     | `24`    | Burned-in subtitle font size             |

## Project layout

```
src/subsmith/
  config.py              Pydantic settings
  models.py              Segment model with timing validation
  media/                 Media protocol + ffmpeg extraction and burn-in
  transcription/         Transcriber protocol + faster-whisper backend
  translation/           Translator protocol + concurrent, retrying backend
  subtitles/             SRT serialization
  pipeline.py            Stage orchestration
  factory.py             Default pipeline assembly from settings
  cli.py                 Typer command line
tests/                   Unit tests with fakes (no ffmpeg or models required)
```

## Testing

```bash
pip install -e ".[dev]"
make test
make lint
```

The pipeline, translation concurrency and retry logic, SRT serialization, ffmpeg command construction, and configuration are tested with injected fakes, so the suite runs fast and offline. CI runs lint, type checking, and tests on Python 3.10 through 3.12.

## Roadmap

- Word-level karaoke-style subtitle timing
- Optional soft-subtitle muxing (mov_text) alongside burn-in
- Batch mode for directories and glob patterns
- Speaker diarization for multi-speaker labeling
- DeepL and LLM translation backends with glossary support
- Progress reporting and resumable runs for long videos

## License

MIT
