from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import pytesseract
from pdf2image import convert_from_path
from transformers import pipeline
import tempfile
import os
import re

app = FastAPI(title="DocVerification API v1.0")

try:
    nlp_model = pipeline("ner",
                         model="sberbank-ai/rubert-base-cased",
                         aggregation_strategy="simple")
except Exception:
    print("⚠️  Модель не загружена. Используется симуляция.")
    nlp_model = None

class VerificationResult(BaseModel):
    filename: str
    errors: list
    status: str = "processed"

VALID_CABLE_TYPES = ['КВВГ', 'ВВГнг', 'АВБбШв', 'NYM', 'КВВГнг']
SIGNAL_RANGE = (4, 20)

@app.post("/verify-document/", response_model=VerificationResult)
async def verify_document(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        images = convert_from_path(tmp_path, dpi=200)
        extracted_text = "\n".join([
            pytesseract.image_to_string(img, lang='rus+eng') for img in images
        ])
        entities = nlp_model(extracted_text[:2000]) if nlp_model else []
        errors = []
        for e in entities:
            word = e.get('word', '').strip()
            entity_group = e.get('entity_group', '')
            if entity_group == 'CABLE_TYPE' or re.match(r'[А-Я]{2,6}[а-я]*', word):
                if word not in VALID_CABLE_TYPES and len(word) >= 3:
                    errors.append(f"Тип кабеля: '{word}' — не в списке разрешённых")
            if entity_group == 'SIGNAL_MA':
                try:
                    val = float(word)
                    if not (SIGNAL_RANGE[0] <= val <= SIGNAL_RANGE[1]):
                        errors.append(f"Сигнал {val} мА вне диапазона 4–20 мА")
                except ValueError:
                    pass
        return VerificationResult(filename=file.filename, errors=errors)
    except Exception as e:
        return VerificationResult(filename=file.filename, errors=[str(e)], status="error")
    finally:
        os.unlink(tmp_path)