# MovieSubGR

A Python application that automatically transcribes videos, translates the transcriptions to Greek, and embeds the subtitles back into the video.

## Features

- Extract audio from video files using FFmpeg
- Apply noise reduction to improve audio quality
- Transcribe audio to text using OpenAI's Whisper model
- Translate transcriptions from English to Greek using Google Translate
- Generate SRT subtitle files
- Embed subtitles into the original video

## Prerequisites

- Python 3.9
- FFmpeg installed on your system

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/SubtitlesProject.git
   cd SubtitlesProject
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install openai-whisper pydub deep_translator srt
   ```

## Usage

1. Update the `video_file` path in `main.py` to point to your video file:
   ```python
   video_file = "/path/to/your/video.mp4"
   ```

2. Run the application:
   ```
   python main.py
   ```

3. The script will:
   - Extract audio from the video file
   - Reduce noise in the audio
   - Transcribe the audio to text
   - Translate the text to Greek
   - Generate an SRT subtitle file
   - Embed the subtitles into the original video

4. The final video with embedded subtitles will be saved as `final_video.mp4`

## Module Overview

- `audio_extraction.py`: Extracts audio from video files using FFmpeg
- `noise_reduction.py`: Applies noise normalization to improve audio quality
- `STT.py`: Transcribes audio using OpenAI's Whisper model
- `translator.py`: Translates text from English to Greek using Google Translate
- `subtitles_generation.py`: Generates SRT subtitle files
- `subtitles_emb.py`: Embeds subtitles into videos
- `main.py`: Orchestrates the entire process

## Customization

- To use a different Whisper model size, modify the `model_size` parameter in the `transcribe_audio` function call in `main.py`.
- To translate to a language other than Greek, modify the target language in `translator.py`.
- To customize subtitle appearance, adjust the `force_style` parameter in `subtitles_emb.py`.

## Acknowledgements

- [OpenAI Whisper](https://github.com/openai/whisper) for speech-to-text transcription
- [Deep Translator](https://github.com/nidhaloff/deep-translator) for translation capabilities
- [FFmpeg](https://ffmpeg.org/) for audio extraction and subtitle embedding
