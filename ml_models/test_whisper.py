from whisper_voice2text import query_hf, Voice2Text

IS_LOCAL = False
if IS_LOCAL:
    voice2text = Voice2Text()
    orig_result, eng_result = voice2text.query("prueba3.mp4")
    print("orig_result:", orig_result)
    print("eng_result:", eng_result)
else:
    output = query_hf("prueba3.mp4")["text"]
    print(output)


