from ocr import query_ocr
from translate import query_translate

filename = "prueba.jpeg"
ocr_result, bboxes = query_ocr(filename)
print("ocr_result: ", ocr_result)

# Translate
response = query_translate(ocr_result)
print("translation: ", response)