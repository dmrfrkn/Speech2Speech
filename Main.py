import os
os.environ["PATH"] += os.pathsep + r"C:\Users\CumFur\Downloads\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin"

import re
from pydub import AudioSegment
import whisper
from elevenlabs import generate, set_api_key, save
from num2words import num2words  

# FFmpeg PATH
AudioSegment.converter = "C:/Users/CumFur/Downloads/ffmpeg-7.1.1-essentials_build/ffmpeg-7.1.1-essentials_build/bin/ffmpeg.exe"

# Whisper ve ElevenLabs Settings
WHISPER_MODEL = "base"
ELEVENLABS_API_KEY = "API_KEY"
VOICE_ID = "VOICE_ID"  

INPUT_AUDIO = "C:/Users/CumFur/Desktop/Furkan/VS Code/Seyma2.mp4"
WORKING_WAV = "working_audio.wav"
TRANSCRIPT = "transcript.txt"
OUTPUT_AUDIO = "output_new_sentences.wav"

# Model and API start
model = whisper.load_model(WHISPER_MODEL)
set_api_key(ELEVENLABS_API_KEY)

def save_audio_to_wav(input_path: str, output_path: str):
    audio = AudioSegment.from_file(input_path)
    audio.export(output_path, format="wav")
    print(f"[1] WAV olarak kaydedildi: {output_path}")

def transcribe_audio(input_wav: str, transcript_path: str) -> str:
    print(f"[2] Transkripsiyon başlatılıyor: {input_wav}")
    result = model.transcribe(input_wav)
    text = result["text"].strip()
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[2] Transkript dosyaya kaydedildi: {transcript_path}")
    return text

def append_to_transcript(transcript_path: str, new_text: str):
    with open(transcript_path, "a", encoding="utf-8") as f:
        f.write("\n" + new_text.strip())
    print(f"[3] Yeni metin eklendi: {new_text!r}")

def convert_numbers_to_words(text: str) -> str:
    # Rakamları Türkçe yazıya çevir
    def replacer(match):
        return num2words(int(match.group()), lang='tr')
    return re.sub(r'\b\d+\b', replacer, text)

def synthesize_speech(text: str, output_audio_path: str):
    print(f"[4] Voice synthesis is start. ({len(text)} karakter)")
    audio_data = generate(
        text=text,
        voice=VOICE_ID,
        model="eleven_multilingual_v2"
    )
    save(audio_data, output_audio_path)
    print(f"[4] Yeni ses dosyası kaydedildi: {output_audio_path}")

def main():
    # 1) Convert voice file to Wav 
    save_audio_to_wav(INPUT_AUDIO, WORKING_WAV)

    # 2) transcribe audio to text
    original_text = transcribe_audio(WORKING_WAV, TRANSCRIPT)
    print("Transkript (ham):\n", original_text)

    # 3) Numbers to words
    processed_text = convert_numbers_to_words(original_text)
    print("İşlenmiş Transkript:\n", processed_text)

    # 4) Speech synthesis
    synthesize_speech(processed_text, OUTPUT_AUDIO)

if __name__ == "__main__":
    main()
