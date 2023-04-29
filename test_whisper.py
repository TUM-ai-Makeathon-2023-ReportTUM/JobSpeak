from voice2text.whisper_voice2text import query_hf, Voice2Text

IS_LOCAL = False
if IS_LOCAL:
    voice2text = Voice2Text()
    orig_result, eng_result = voice2text.query("voice2text/prueba.mp4")
    print("orig_result:", orig_result)
    print("eng_result:", eng_result)
else:
    output = query_hf("voice2text/prueba.mp4")
    print(output)


