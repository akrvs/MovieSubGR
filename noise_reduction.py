from pydub import AudioSegment
from pydub.effects import normalize

def reduce_noise(audio_path):
    audio = AudioSegment.from_file(audio_path)
    audio = normalize(audio)
    cleaned_path = audio_path.replace(".wav", "_clean.wav")
    audio.export(cleaned_path, format="wav")
    return cleaned_path
