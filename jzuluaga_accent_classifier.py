import os
import subprocess
import torchaudio
import requests
from speechbrain.pretrained.interfaces import foreign_class

# Windows fix for SpeechBrain local file caching
os.environ["SPEECHBRAIN_LOCAL_FILE_STRATEGY"] = "copy"

def download_audio(url, output_path="audio.wav"):
    try:
        # Attempt to extract audio using yt-dlp
        command = [
            "yt-dlp", "--extract-audio", "--audio-format", "wav",
            "--audio-quality", "0", "-o", "temp.%(ext)s", url
        ]
        subprocess.run(command, check=True)

        # Find the downloaded audio
        for ext in ["wav", "mp3", "webm", "m4a"]:
            file = f"temp.{ext}"
            if os.path.exists(file):
                waveform, sr = torchaudio.load(file)
                os.remove(file)
                break
        else:
            raise FileNotFoundError("No audio downloaded with yt-dlp.")
    except subprocess.CalledProcessError:
        # Fallback: direct download
        if url.endswith((".wav", ".mp4", ".mp3", ".m4a")):
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
