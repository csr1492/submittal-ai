from fastapi import FastAPI, UploadFile, File
import fitz
from app.ai import extract_spec_requirements, extract_cutsheet_data, run_compliance
from app.pdf_builder import generate_compliance_letter, merge_pdfs
import uuid
import os

app = FastAPI()

def extract_text_from_pdf(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


@app.post("/process/")
async def process_submittal(
    spec: UploadFile = File(...),
    cutsheet: UploadFile = File(...)
):

    spec_text = extract_text_from_pdf(await spec.read())
    cut_text = extract_text_from_pdf(await cutsheet.read())

    spec_json = extract_spec_requirements(spec_text)
    cut_json = extract_cutsheet_data(cut_text)

    compliance = run_compliance(spec_json, cut_json)

    deviations = [
        c for c in compliance
        if c["status"] in ["Non-Compliant", "Not Addressed"]
    ]

    letter_path = f"letter_{uuid.uuid4()}.pdf"
    generate_compliance_letter(letter_path, deviations)

    final_path = f"final_{uuid.uuid4()}.pdf"
    merge_pdfs(final_path, [letter_path])

    return {"message": "Submittal processed", "file": final_path}
