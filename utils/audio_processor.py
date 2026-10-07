import os
from pydub import AudioSegment
import yt_dlp

# Automatically downloads/adds ffmpeg and ffprobe to PATH for this process


DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_youtube_audio(url: str) -> str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "ios", "web"]
            }
        },
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        raw_filename = ydl.prepare_filename(info)
        wav_filename = os.path.splitext(raw_filename)[0] + ".wav"

    return wav_filename





def convert_to_wav(input_path:str)->str:
    """convert any video/audio to WAV format using pydub"""
    output_path= os.path.splitext(input_path)[0]+ "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio= audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")
    return output_path



def chunk_audio(wav_path:str, chunk_minutes:int=10)->list:
    audio= AudioSegment.from_wav(wav_path)
    chunk_ms= chunk_minutes*60*1000

    chunks=[]

    for i, start in enumerate(range(0,len(audio),chunk_ms)):
        chunk= audio[start:start+chunk_ms]
        chunk_path= f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")

        chunks.append(chunk_path)
    return chunks

def process_input(source:str)->list:
    if source.startswith("http://") or source.startswith("https://"):
        print("detected yt URL. downloading audio...")
        wav_path= download_youtube_audio(source)
    else:
        print("detected local file. converting to WAV...")
        wav_path= convert_to_wav(source)
    print("chunking audio..")
    chunks= chunk_audio(wav_path)
    print(f"Audio ready- {len(chunks)} chunks created.")
    return chunks