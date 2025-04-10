from fastapi import FastAPI
from api import routes_upload, routes_generate

app = FastAPI(title="Document Analyzer API")

# Register API Routes
app.include_router(routes_upload.router, prefix="/api/upload")
app.include_router(routes_generate.router, prefix="/api/generate")
