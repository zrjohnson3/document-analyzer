from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from api import routes_upload, routes_generate
import os
from utils.file_storage import ensure_storage_dirs
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("document-analyzer")

# Create storage directories
ensure_storage_dirs()

# Initialize FastAPI app
app = FastAPI(
    title="Document Analyzer API",
    description="API for analyzing and consolidating emergency management documents",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routes
app.include_router(routes_upload.router, prefix="/api/upload", tags=["Document Upload"])
app.include_router(routes_generate.router, prefix="/api/generate", tags=["Document Generation"])

# Serve static files (outputs for download)
os.makedirs("storage/outputs", exist_ok=True)
app.mount("/outputs", StaticFiles(directory="storage/outputs"), name="outputs")

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

# Root endpoint
@app.get("/", tags=["Health Check"])
async def root():
    return {
        "message": "Document Analyzer API is running",
        "status": "online",
        "version": "1.0.0"
    }

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Document Analyzer API",
        version="1.0.0",
        description="API for analyzing emergency management documents and generating consolidated reports",
        routes=app.routes,
    )
    
    # Add custom info if needed
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Run the application - for development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
