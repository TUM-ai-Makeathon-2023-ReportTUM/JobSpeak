import requests
import sys
sys.path.append("..")
from env import *
try:
    import whisper
    from .utils import get_mel_spectogram
    enable_local = True
except:
    enable_local = False
    print("whisper not available locally")

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v2"
headers = {"Authorization": "Bearer {}".format(HF_KEY)}

def query_hf(filename):
    '''
    filename: path to the audio file
    return: json response from the Whisper API
    '''
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

class Voice2Text:
    def __init__(self):
        print("loading model...")
        self.whisper_model = whisper.load_model("small")
    #     pass
    def query(self, filename):
        '''
        filename: path to the audio file
        return: original transcript, english transcript
        '''

        print("Detected audio file, transcribing...")
        print("filename: ", filename)
        mel = get_mel_spectogram(filename).to(self.whisper_model.device)

        # Detect language and translate if different from english
        _, probs = self.whisper_model.detect_language(mel)
        language = max(probs, key=probs.get)
        print(f"Detected language: {language}")

        orig_result = self.whisper_model.transcribe(
            filename, without_timestamps=False, language=language
        )
        kwargs = {}
        if language != "en":
            kwargs["language"] = language
            kwargs["task"] = "translate"
            # Get transcript in english
            eng_result = self.whisper_model.transcribe(
                filename, without_timestamps=False, **kwargs
            )
        else:
            eng_result = orig_result

        return orig_result["text"], eng_result["text"]