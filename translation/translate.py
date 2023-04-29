import requests, uuid, json

# Add your key and endpoint
key = "9dd019873db7486ab6a66d1cd94cfe94"
endpoint = "https://api.cognitive.microsofttranslator.com"

# location, also known as region.
# required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.
location = "global"

path = '/translate'
constructed_url = endpoint + path


headers = {
    'Ocp-Apim-Subscription-Key': key,
    # location required if you're using a multi-service or regional (not global) resource.
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}


def query_translate(text, source_language='es', dest_language='en'):
    params = {
    'api-version': '3.0',
    # 'from': 'en',
    'to': dest_language
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        # location required if you're using a multi-service or regional (not global) resource.
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    # You can pass more than one object in body.
    body = [{
        'text': text
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))
    return {"detected_language": response[0]['detectedLanguage']['language'],
            "text_en": response[0]["translations"][0]["text"]}

# text = "Hoy renové el baño, pinté la cocina y le lave los pies al cliente"
# text_en = query_translate(text)
# print("text_en: ", text_en[0]["translations"][0]["text"])
# print("language: ", text_en[0]['detectedLanguage']['language'])

