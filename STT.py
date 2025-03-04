import whisper

def transcribe_audio(audio_file, model_size="small"):
    """
    Transcribes an audio file and extracts timestamps.
    :param audio_file: Path to the extracted audio file.
    :param model_size: Whisper model size (default: "small").
    :return: List of (start_time, end_time, text) tuples.
    """
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_file)

    transcriptions = []
    for segment in result.get("segments", []):  # Ensure segments exist
        start_time = segment.get("start")
        end_time = segment.get("end")
        text = segment.get("text")

        if start_time is not None and end_time is not None and text:  # Avoid None values
            transcriptions.append((start_time, end_time, text))

    if not transcriptions:
        print("⚠️ Warning: No transcriptions were generated!")

    return transcriptions
