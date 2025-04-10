from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Union
from enum import Enum
from datetime import datetime

class DocumentType(str, Enum):
    ANIMAL_BOARDING = "animal_boarding"
    SHELTER_PLAN = "shelter_plan"
    GENERAL = "general"

class OutputFormat(str, Enum):
    DOCX = "docx"
    PDF = "pdf"

class FileInfo(BaseModel):
    name: str
    path: str
    size: int
    type: Optional[str] = None
    uploaded_at: Optional[datetime] = None

class AnalyzeRequest(BaseModel):
    file_path: str
    document_type: DocumentType = DocumentType.GENERAL

class GenerateRequest(BaseModel):
    file_paths: List[str]
    output_type: DocumentType = DocumentType.ANIMAL_BOARDING
    output_filename: str = "master_document"
    formats: List[OutputFormat] = [OutputFormat.DOCX, OutputFormat.PDF]

class AnalysisResult(BaseModel):
    file: str
    document_type: DocumentType
    analysis: str

class GenerateResult(BaseModel):
    message: str
    files: Dict[str, str]

class FilesList(BaseModel):
    files: List[FileInfo]

class UploadResult(BaseModel):
    message: str
    path: str

class MultiUploadResult(BaseModel):
    message: str
    results: List[Dict[str, str]]

class PreviewResult(BaseModel):
    filename: str
    preview: str
    has_more: bool
    total_length: int

class ErrorResponse(BaseModel):
    detail: str
