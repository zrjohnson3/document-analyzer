# Document Analyzer Backend

A Python-based backend for analyzing emergency management documents and generating consolidated reports.

## Features

- Upload PDF and DOCX documents
- Extract text content from documents
- Analyze documents using OpenAI's GPT models
- Merge information from multiple documents
- Generate well-formatted DOCX and PDF output files
- RESTful API for frontend integration

## Prerequisites

- Python 3.8+
- OpenAI API key

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Running the Application

Start the application with:

```
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

Interactive API documentation: http://localhost:8000/docs

## API Endpoints

### Document Upload

- `POST /api/upload/`: Upload a single file
- `POST /api/upload/multiple`: Upload multiple files
- `GET /api/upload/files`: List all uploaded files
- `GET /api/upload/preview/{filename}`: Preview text content of a file
- `DELETE /api/upload/files/{filename}`: Delete an uploaded file

### Document Generation

- `POST /api/generate/analyze`: Analyze a single document
- `POST /api/generate/generate`: Generate a consolidated document from multiple files
- `GET /api/generate/outputs`: List all generated output files
- `GET /api/generate/download/{filename}`: Download a generated file
- `DELETE /api/generate/outputs/{filename}`: Delete a generated file

## Usage Example

1. Upload documents using the `/api/upload/` endpoint
2. List files with `/api/upload/files` to get file paths
3. Generate a consolidated document with `/api/generate/generate`
4. Download the generated files with `/api/generate/download/{filename}`

## API Request Examples

### Upload a Document

```
POST /api/upload/
```

Form data:

- `file`: PDF or DOCX file

### Generate a Consolidated Document

```
POST /api/generate/generate
```

Request body:

```json
{
  "file_paths": [
    "storage/uploads/document1.pdf",
    "storage/uploads/document2.docx"
  ],
  "output_type": "animal_boarding",
  "output_filename": "consolidated_plan",
  "formats": ["docx", "pdf"]
}
```

## Integrating with Frontend

This backend provides all necessary APIs to integrate with a frontend application. Here's a typical flow:

1. Frontend provides document upload functionality
2. Backend extracts and analyzes text
3. Frontend displays analysis results
4. User selects documents to merge
5. Backend generates final document
6. Frontend provides download links

## Project Structure

- `main.py`: Application entry point
- `api/`: API route definitions
- `services/`: Core functionality
  - `document_parser.py`: Document text extraction
  - `ai_processor.py`: OpenAI integration for analysis
  - `output_formatter.py`: DOCX and PDF generation
- `models/`: Data models
- `utils/`: Utility functions
- `storage/`: Document storage (created at runtime)
  - `uploads/`: Uploaded files
  - `outputs/`: Generated files
