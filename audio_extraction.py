import subprocess
import os

def extract_audio(video_path, output_format="wav"):
    """
    Extracts audio from a video file using FFmpeg.
    :param video_path: Path to the input video file.
    :param output_format: Desired audio format (default is mp3).
    :return: Path to the extracted audio file.
    """
    base_name = os.path.splitext(video_path)[0]
    audio_path = f"{base_name}.{output_format}"
    command = ["ffmpeg", "-i", video_path, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", audio_path]
    subprocess.run(command, check=True)

    return audio_path
