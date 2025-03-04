import srt
from datetime import timedelta

def generate_srt(transcriptions, translations, output_path="subtitles.srt"):
    """
    Generates an SRT subtitle file from Whisper timestamps and translations.
    :param transcriptions: List of (start_time, end_time, text) tuples.
    :param translations: List of translated Greek sentences.
    :param output_path: Path to save the .srt file.
    """
    subtitle_entries = []

    for i, ((start, end, _), greek_text) in enumerate(zip(transcriptions, translations), start=1):
        subtitle = srt.Subtitle(
            index=i,
            start=timedelta(seconds=start),
            end=timedelta(seconds=end),
            content=greek_text
        )
        subtitle_entries.append(subtitle)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(srt.compose(subtitle_entries))

    print(f"✅ Subtitles saved to {output_path}")

