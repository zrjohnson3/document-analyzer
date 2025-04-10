from docx import Document
import os

OUTPUT_DIR = "storage/outputs"

def create_docx(extracted_text, filename):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    doc = Document()
    doc.add_heading("Emergency Animal Boarding Program", 0)
    doc.add_paragraph(extracted_text)
    save_path = f"{OUTPUT_DIR}/{filename}.docx"
    doc.save(save_path)
    return save_path
