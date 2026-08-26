import whisper
from pydub import AudioSegment
import requests
import os 

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")
SARVAM_PIECE_SECOND=25

_model= None

SARVAM_MODEL=os.getenv("SARVAM_API_KEY")
SARVAM_TRANSLATE_STT_URL="https://api.sarvam.ai/speech-to-text-translate"
SARVAM_MODEL_NAME=os.getenv("SARVAM_STT_MODEL", "saaras:v2.5")


def load_model():

    global _model

    if _model is None:
        print(f"loading whisper model:{WHISPER_MODEL}...")
        _model= whisper.load_model(WHISPER_MODEL)
        print("whisper model loaded successfully")

    return _model

def transcribe_chunk_whisper(chunk_path:str)->str:
    model= load_model()
    result= model.transcribe(chunk_path, task= "transcribe")
    return result['text']

def send_to_sarvam(chunk_path:str)->str:
    headers= {"api-subscription-key":SARVAM_MODEL}

    with open(chunk_path, "rb") as f:
        files= {"file":(os.path.basename(chunk_path), f, "audio/wav")}
        data= {"model": SARVAM_MODEL, "with diarization": "false"}
        response= requests.post(
            SARVAM_TRANSLATE_STT_URL, 
            headers= headers,
            files=files,
            data=data,
            timeout=120
        )

        if not response.ok:
           print(f"\n❌ Sarvam returned {response.status_code}")
           print(f"Response body: {response.text}\n")
        response.raise_for_status()

        return response.json().get("transcript", "")

def transcribe_chunk_sarvam(chunk_path:str)->str:
    if not SARVAM_MODEL:
        raise RuntimeError("sarvam api is not set in env.")

    audio= AudioSegment.from_wav(chunk_path)
    piece_ms=SARVAM_PIECE_SECOND * 1000
    full_text=""
    total_pieces= (len(audio)+piece_ms-1)

    for i,start in enumerate(range(0,len(audio), piece_ms)):
        piece=audio[start:start+piece_ms]
        piece_path=f"{chunk_path}_sv_{i}.wav"
        piece.export(piece_path, format="wav")

        try:
            print(f"  → Sarvam piece {i + 1}/{total_pieces} ...")
            full_text += send_to_sarvam(piece_path) + " "
        finally:
            if os.path.exists(piece_path):
                os.remove(piece_path)

    return full_text.strip()


def transcribe_chunk(chunk_path:str, language:str="english")->str:
    """route one chunk to whisper or sarvam depending on the language choice.
    -english -> Whisper(local moodel)
    -hinglish ->Sarvam(translates to english while transcribing)
    """
    if language.lower()=="hinglish":
        return transcribe_chunk_sarvam(chunk_path)
    return transcribe_chunk_whisper(chunk_path)


def transcribe_all(chunks:list,language:str="english")->str:
    full_transcript= ""

    engine= "Sarvam AI" if language.lower()=="hinglish" else "Whisper"
    print(f"using {engine} for transcribing.")

    for i,chunk in enumerate(chunks):
        print(f"trancribing chunks {i+1}/{len(chunks)}")
        text= transcribe_chunk(chunk, language=language)
        full_transcript+=text + " "

    print("transcription completed")

    return full_transcript.strip()

