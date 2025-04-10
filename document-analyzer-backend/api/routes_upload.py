from fastapi import APIRouter, UploadFile, File
from services.document_parser import save_upload_file
import os

router = APIRouter()

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    save_path = await save_upload_file(file)
    return {"message": "File uploaded successfully", "path": save_path}
