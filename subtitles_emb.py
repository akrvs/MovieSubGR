import subprocess

def embed_subtitles(video_file, subtitle_file, output_file="output_video.mp4"):
    """
    Embeds the given subtitle file into the video using FFmpeg.
    :param video_file: Path to the input video file.
    :param subtitle_file: Path to the .srt subtitle file.
    :param output_file: Path to save the output video.
    """
    command = [
        "ffmpeg", "-i", video_file,
        "-vf", f"subtitles={subtitle_file}:force_style='Fontsize=24'",
        "-c:a", "copy", output_file
    ]

    subprocess.run(command, check=True)
    print(f"✅ Subtitled video saved as {output_file}")
