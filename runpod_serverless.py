import runpod
import jzuluaga_accent_classifier

def handler(event):
    url = event.get("input", {}).get("url")
    if not url:
        return {"error": "Missing 'url' in input"}

    try:
        path = jzuluaga_accent_classifier.download_audio(url)
        result = jzuluaga_accent_classifier.classify_accent(path)
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

runpod.serverless.start({"handler": handler})
