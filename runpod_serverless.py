import runpod
import jzuluaga_accent_classifier

def handler(event):
    url = event.get("input", {}).get("url")
    if not url:
        return {"status": "error", "message": "Missing 'url' in input"}

    try:
        path = jzuluaga_accent_classifier.download_audio(url)
        result = jzuluaga_accent_classifier.classify_accent(path)
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

<<<<<<< HEAD
# Start the RunPod serverless worker
=======
>>>>>>> 180cf1797a47a38f709d9e494140dd8087839849
runpod.serverless.start({"handler": handler})
