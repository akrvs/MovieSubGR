```
   ███████╗██╗   ██╗██████╗ ███████╗███╗   ███╗██╗████████╗██╗  ██╗
   ██╔════╝██║   ██║██╔══██╗██╔════╝████╗ ████║██║╚══██╔══╝██║  ██║
   ███████╗██║   ██║██████╔╝███████╗██╔████╔██║██║   ██║   ███████║
   ╚════██║██║   ██║██╔══██╗╚════██║██║╚██╔╝██║██║   ██║   ██╔══██║
   ███████║╚██████╔╝██████╔╝███████║██║ ╚═╝ ██║██║   ██║   ██║  ██║
   ╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝
            s u b t i t l e   p i p e l i n e
```

> Feed it a raw video. The pipeline rips the audio, makes a model confess every spoken line with timestamps, rewrites each line in the target language under concurrent fire, and burns the track back into the frame. One command in, a subtitled cut out.

![status](https://img.shields.io/badge/status-ACTIVE-brightgreen)
![category](https://img.shields.io/badge/category-AI%20%2F%20Audio-9cf)
![difficulty](https://img.shields.io/badge/difficulty-Medium-orange)
![python](https://img.shields.io/badge/python-3.10%2B-blue)
![license](https://img.shields.io/badge/license-MIT-green)

```
┌─[ MACHINE ]────────────────────────────────────────────────┐
│ codename    : Subsmith                                      │
│ category    : AI / Audio / Media                            │
│ difficulty  : Medium                                        │
│ stack       : faster-whisper · deep-translator · ffmpeg     │
│ interfaces  : Typer CLI                                     │
│ flags       : user [transcribe]   root [translate + burn]   │
│ status      : OWNED - JFK sample transcribed verbatim       │
└─────────────────────────────────────────────────────────────┘
```

## [ Briefing ]

Subsmith turns any video into a subtitled video in one command. It extracts and loudness-normalizes the audio, transcribes speech with Whisper, translates each line into the target language, and burns clean subtitles back into the video. Default language is Greek, but the target is a single flag away.

## [ Recon ] - reading the target

Generating translated subtitles is a multi-stage media problem: demux audio, run speech-to-text with accurate timestamps, translate hundreds of short lines, serialize valid SRT timing, and re-encode the video with a burned-in track. The naive build breaks in predictable ways:

```
[!] one blocking network call per line     -> a feature film takes forever
[!] zero retry logic                        -> first transient error kills the run
[!] one hard-coded path, one flat script    -> not reusable, not testable
[!] "noise reduction" that only normalizes  -> a dependency that no longer builds
```

Subsmith treats the workflow as a real pipeline of isolated, swappable stages.

## [ Attack Path ] - video in, subtitles out

```
   video
     │
     v
 [ ffmpeg extract + loudnorm ] ── audio (16k mono, EBU R128)
     │
     v
 [ faster-whisper STT ] ──────── timed segments
     │
     v
 [ concurrent translator ] ───── translated segments
     │                            (dedup · thread pool · retry)
     v
 [ SRT writer ] ──────────────── .srt
     │
     v
 [ ffmpeg burn-in ] ──────────── subtitled video
```

Each stage hides behind a small interface (`Transcriber`, `Translator`, `Media`), and `SubtitlePipeline` wires them together. Decoupled stages mean every backend is swappable and the orchestration is testable with no ffmpeg, no model weights, and no network.

## [ Tradecraft ] - why it is built this way

- `[*]` **Concurrent, resilient translation.** The legacy build fired one blocking call per subtitle line. Subsmith deduplicates repeated lines, fans the unique set across a thread pool, wraps each call in exponential-backoff retries, and reassembles in original order. Fewer calls, faster runs, survives flaky APIs.
- `[*]` **faster-whisper over openai-whisper.** The CTranslate2 backend is several times faster on CPU at equal model size and exposes word-accurate timestamps that map straight onto SRT cues.
- `[*]` **Honest audio.** The old "noise reduction" only normalized levels with pydub, which no longer builds on modern Python. Subsmith runs EBU R128 loudness normalization through ffmpeg's `loudnorm` during extraction - one fewer dependency, named for what it does.
- `[*]` **Pluggable translation.** Google Translate (no API key) is the default so it runs out of the box, but `Translator` is an interface; a DeepL or LLM backend drops in without touching the pipeline.
- `[*]` **Config as environment.** Pydantic settings (`SUBSMITH_*`) control model size, languages, concurrency, and styling with no code edits.

## [ Arsenal ]

```
stt         : faster-whisper (ctranslate2)
translate   : deep-translator (pluggable backend) · tenacity retries
media       : ffmpeg (loudnorm extract + subtitle burn-in)
subtitles   : srt
service     : pydantic v2 · typer
quality     : pytest · ruff · mypy
ship        : docker · github actions
```

## [ Deploy ] - spawn the box

ffmpeg must be on `PATH`. The first run pulls the selected Whisper model once.

```bash
$ pip install -e ".[transcription]"
[+] stt + translation backends online

$ subsmith run movie.mkv
[*] extracting audio (loudnorm)
[*] transcribing  -> 412 segments
[*] translating   -> el (8 workers)
[*] burning subtitles
[+] movie_subtitled.mp4

$ subsmith run movie.mkv --target fr --model medium
$ subsmith transcribe movie.mkv --subtitles movie.srt
```

Containerized run (ffmpeg ships inside the image):

```bash
$ docker build -t subsmith .
$ docker run --rm -v "$PWD:/work" -w /work subsmith run movie.mkv
```

## [ Loadout ] - configuration

| Variable                          | Default | Action                                   |
| --------------------------------- | ------- | ---------------------------------------- |
| `SUBSMITH_WHISPER_MODEL`          | `small` | Whisper model size                       |
| `SUBSMITH_SOURCE_LANGUAGE`        | auto    | Force a source language, or autodetect   |
| `SUBSMITH_TARGET_LANGUAGE`        | `el`    | Translation target language code         |
| `SUBSMITH_TRANSLATION_WORKERS`    | `8`     | Concurrent translation workers           |
| `SUBSMITH_TRANSLATION_MAX_RETRIES`| `3`     | Retries per line on transient failure    |
| `SUBSMITH_SUBTITLE_FONT_SIZE`     | `24`    | Burned-in subtitle font size             |

## [ Layout ]

```
src/subsmith/
  config.py              pydantic settings
  models.py              Segment model with timing validation
  media/                 Media protocol + ffmpeg extraction and burn-in
  transcription/         Transcriber protocol + faster-whisper backend
  translation/           Translator protocol + concurrent, retrying backend
  subtitles/             SRT serialization
  pipeline.py            stage orchestration
  factory.py             default pipeline assembly from settings
  cli.py                 Typer command line
tests/                   unit tests with fakes (no ffmpeg or models required)
```

## [ Test Range ]

```bash
$ pip install -e ".[dev]"
$ make test
[+] 25 passed

$ make lint
[+] ruff clean · mypy clean
```

The pipeline, translation concurrency and retry logic, SRT serialization, ffmpeg command construction, the Segment model, and configuration are all driven by injected fakes, so the suite runs fast and offline. CI replays lint, type checking, and tests on Python 3.10 through 3.12.

## [ Skill Tree ] - next objectives

- `[ ]` Word-level karaoke-style subtitle timing
- `[ ]` Optional soft-subtitle muxing (mov_text) alongside burn-in
- `[ ]` Batch mode for directories and glob patterns
- `[ ]` Speaker diarization for multi-speaker labeling
- `[ ]` DeepL and LLM translation backends with glossary support
- `[ ]` Progress reporting and resumable runs for long videos

## [ Intel ]

MIT. Use it, fork it, build on it.
