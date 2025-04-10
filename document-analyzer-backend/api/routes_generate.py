from fastapi import APIRouter
from services.ai_processor import analyze_document
from services.output_formatter import create_docx
import os

router = APIRouter()

@router.get("/")
async def generate_document():
    extracted_text = await analyze_document("Example input text here from parsing!")
    output_path = create_docx(extracted_text, "final_output")
    return {"message": "Document Generated", "path": output_path}
