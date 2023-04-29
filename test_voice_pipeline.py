from voice2text.whisper_voice2text import query_hf, Voice2Text
import nlp.use_llm as llm

IS_LOCAL = False
if IS_LOCAL:
    voice2text = Voice2Text()
    orig_result, output = voice2text.query("voice2text/prueba3.mp4")
    print("orig_result:", orig_result)
    print("eng_result:", output)
else:
    output = query_hf("voice2text/prueba3.mp4")["text"]
    print(output)

date = "29.04.2023"

results_a = llm.process_case_A(output, date)
print("results_a: ", results_a)

