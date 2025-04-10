from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from services.document_parser import save_upload_file, extract_text_from_file, get_documents_list
from utils.file_storage import delete_file, list_uploaded_files
from typing import List
import os

router = APIRouter()

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    """Upload a single file"""
    try:
        save_path = await save_upload_file(file)
        return {"message": "File uploaded successfully", "path": save_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.post("/multiple")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    """Upload multiple files at once"""
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    results = []
    for file in files:
        try:
            save_path = await save_upload_file(file)
            results.append({"filename": file.filename, "path": save_path, "status": "success"})
        except Exception as e:
            results.append({"filename": file.filename, "error": str(e), "status": "failed"})
    
    return {"message": f"Processed {len(files)} files", "results": results}

@router.get("/files")
async def list_files():
    """List all uploaded files"""
    try:
        files = await get_documents_list()
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list files: {str(e)}")

@router.delete("/files/{filename}")
async def delete_uploaded_file(filename: str):
    """Delete an uploaded file"""
    from services.document_parser import UPLOAD_DIR
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File {filename} not found")
    
    try:
        deleted = delete_file(file_path)
        if deleted:
            return {"message": f"File {filename} deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail=f"Failed to delete {filename}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")

@router.get("/preview/{filename}")
async def preview_file(filename: str, max_chars: int = Query(5000, description="Maximum number of characters to return")):
    """Preview the contents of an uploaded file"""
    from services.document_parser import UPLOAD_DIR
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File {filename} not found")
    
    try:
        text = extract_text_from_file(file_path)
        preview = text[:max_chars]
        has_more = len(text) > max_chars
        
        return {
            "filename": filename,
            "preview": preview,
            "has_more": has_more,
            "total_length": len(text)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error previewing file: {str(e)}")
