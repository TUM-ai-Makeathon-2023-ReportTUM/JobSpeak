import requests

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v2"
headers = {"Authorization": "Bearer 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"}

def query(filename):
    '''
    filename: path to the audio file
    return: json response from the Whisper API
    '''
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

output = query("prueba.mp4")
print(output)


