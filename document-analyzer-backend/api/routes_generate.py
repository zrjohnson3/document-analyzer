from fastapi import APIRouter, HTTPException, Body, Query
from fastapi.responses import FileResponse
from services.ai_processor import analyze_document, analyze_multiple_documents
from services.document_parser import extract_text_from_file
from services.output_formatter import generate_output_files
from utils.file_storage import list_output_files, delete_file
import os
from typing import List, Optional
import time

router = APIRouter()

@router.post("/analyze")
async def analyze_single_document(
    file_path: str = Body(..., description="Path to the uploaded file to analyze"),
    document_type: str = Body("general", description="Type of document (animal_boarding, shelter_plan, general)")
):
    """Analyze a single document and return the extracted information"""
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
    
    try:
        # Extract text from the document
        text = extract_text_from_file(file_path)
        if not text or text.startswith("Error processing"):
            raise HTTPException(status_code=422, detail=f"Could not extract text from file: {text}")
        
        # Analyze the text
        analysis = await analyze_document(text, document_type)
        return {
            "file": os.path.basename(file_path),
            "document_type": document_type,
            "analysis": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing document: {str(e)}")

@router.post("/generate")
async def generate_document(
    file_paths: List[str] = Body(..., description="Paths to the uploaded files to analyze"),
    output_type: str = Body("animal_boarding", description="Type of output document to generate"),
    output_filename: str = Body("master_document", description="Base filename for output"),
    formats: List[str] = Body(["docx", "pdf"], description="Output formats")
):
    """Generate a master document from multiple input documents"""
    if not file_paths:
        raise HTTPException(status_code=400, detail="No files provided for analysis")
    
    # Validate file paths
    for path in file_paths:
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail=f"File not found: {path}")
    
    try:
        # Extract text from all documents
        documents_text = []
        for path in file_paths:
            text = extract_text_from_file(path)
            if text and not text.startswith("Error processing"):
                documents_text.append(text)
        
        if not documents_text:
            raise HTTPException(status_code=422, detail="Could not extract text from any of the provided files")
        
        # Analyze and merge documents
        merged_analysis = await analyze_multiple_documents(documents_text, output_type)
        
        # Generate output files
        output_files = generate_output_files(merged_analysis, output_filename, formats)
        
        return {
            "message": "Document generated successfully",
            "files": output_files
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating document: {str(e)}")

@router.get("/outputs")
async def list_generated_files():
    """List all generated output files"""
    try:
        files = list_output_files()
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list output files: {str(e)}")

@router.get("/download/{filename}")
async def download_file(filename: str):
    """Download a generated file"""
    from services.output_formatter import OUTPUT_DIR
    file_path = os.path.join(OUTPUT_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File {filename} not found")
    
    try:
        return FileResponse(file_path, filename=filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading file: {str(e)}")

@router.delete("/outputs/{filename}")
async def delete_output_file(filename: str):
    """Delete a generated output file"""
    from services.output_formatter import OUTPUT_DIR
    file_path = os.path.join(OUTPUT_DIR, filename)
    
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
