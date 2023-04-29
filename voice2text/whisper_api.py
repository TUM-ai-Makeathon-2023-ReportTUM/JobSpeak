import requests
try:
    import whisper
    enable_local = True
except:
    enable_local = False
    print("whisper not available")

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v2"
headers = {"Authorization": "Bearer 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"}

def query_hf(filename):
    '''
    filename: path to the audio file
    return: json response from the Whisper API
    '''
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

class Voice2Text
    def __init__(self):
        pass
    def query(self, filename):



        if extension == "mp3" or extension == "wav":
            print("Detected audio file, transcribing...")
            whisper_model = whisper.load_model("medium")

            # Detect language and translate if different from english
            mel = get_mel_spectogram(config.INPUT_FILE).to(whisper_model.device)
            _, probs = whisper_model.detect_language(mel)
            language = max(probs, key=probs.get)
            print(f"Detected language: {language}")

            orig_result = whisper_model.transcribe(
                config.INPUT_FILE, without_timestamps=False, language=language
            )
            kwargs = {}
            if language != "en":
                kwargs["language"] = language
                kwargs["task"] = "translate"
                # Get transcript in english
                eng_result = whisper_model.transcribe(
                    config.INPUT_FILE, without_timestamps=False, **kwargs
                )
            else:
                eng_result = orig_result

            print(orig_result)

            pass

# output = query("prueba.mp4")
output = "empty"
print(output)