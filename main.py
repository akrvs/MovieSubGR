from audio_extraction import extract_audio
from STT import transcribe_audio
from noise_reduction import reduce_noise
from translator import translate_to_greek
from subtitles_generation import generate_srt
from subtitles_emb import embed_subtitles

video_file = "/Users/akrvs/Downloads/Silicon Valley.mkv"
audio_file = extract_audio(video_file, "wav")
cleaned_audio_file = reduce_noise(audio_file)

# Use the cleaned audio file instead of the original
transcriptions = transcribe_audio(cleaned_audio_file)

# Add error checking
if not transcriptions:
    print("No transcriptions generated. Cannot create subtitles.")
else:
    translations = [translate_to_greek(text) for _, _, text in transcriptions]
    generate_srt(transcriptions, translations, "greek_subtitles.srt")
    print(f"Created subtitles with {len(transcriptions)} entries")

embed_subtitles(video_file, "greek_subtitles.srt", "final_video.mp4")
