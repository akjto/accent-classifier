import os
import subprocess
import torchaudio
import requests
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from speechbrain.pretrained.interfaces import foreign_class
from fastapi.responses import JSONResponse
from mangum import Mangum

# Windows fix
os.environ["SPEECHBRAIN_LOCAL_FILE_STRATEGY"] = "copy"

app = FastAPI()

class VideoURLRequest(BaseModel):
    url: str

def download_audio(url, output_path="audio.wav"):
    try:
        # Try yt-dlp first
        command = [
            "yt-dlp", "--extract-audio", "--audio-format", "wav",
            "--audio-quality", "0", "-o", "temp.%(ext)s", url
        ]
        subprocess.run(command, check=True)

        for ext in ["wav", "mp3", "webm", "m4a"]:
            file = f"temp.{ext}"
            if os.path.exists(file):
                waveform, sr = torchaudio.load(file)
                os.remove(file)
                break
        else:
            raise FileNotFoundError("No audio downloaded with yt-dlp.")
    except subprocess.CalledProcessError:
        # Fallback: direct file download
        if url.endswith(".wav") or url.endswith(".mp4"):
            try:
                response = requests.get(url, timeout=10)
                with open("temp.raw", "wb") as f:
                    f.write(response.content)
                waveform, sr = torchaudio.load("temp.raw")
                os.remove("temp.raw")
            except Exception:
                raise RuntimeError("Direct download failed or unsupported format.")
        else:
            raise RuntimeError("yt-dlp failed and URL is not a direct media file.")

    if sr != 16000:
        waveform = torchaudio.transforms.Resample(sr, 16000)(waveform)
    waveform = waveform.mean(dim=0, keepdim=True)
    torchaudio.save(output_path, waveform, 16000)
    return output_path

def classify_accent(audio_path):
    clf = foreign_class(
        source="Jzuluaga/accent-id-commonaccent_xlsr-en-english",
        pymodule_file="custom_interface.py",
        classname="CustomEncoderWav2vec2Classifier",
        run_opts={"device": "cpu"}
    )
    out_prob, score, idx, label = clf.classify_file(audio_path)
    return {
        "accent": label[0].title(),
        "confidence": f"{round(float(score[0]) * 100, 1)}%"
    }

@app.post("/classify-accent")
async def classify_endpoint(payload: VideoURLRequest, request: Request):
    try:
        wav_path = download_audio(payload.url)
        result = classify_accent(wav_path)
        return {"status": "success", "result": result}
    
    except subprocess.CalledProcessError as e:
        error_msg = f"Video processing failed. Possible bad or truncated URL. Details: {str(e)}"
        raise HTTPException(status_code=400, detail=error_msg)

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"Audio extraction failed: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
            "code": exc.status_code,
            "path": request.url.path
        },
    )

handler = Mangum(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("jzuluaga_accent_classifier:app", host="0.0.0.0", port=8000, reload=True)