from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from .security import get_current_user, create_access_token
from fastapi import Depends
import os
from typing import List
import logging

app = FastAPI()
security = HTTPBearer()

class Query(BaseModel):
    question: str

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add file type validation
ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.doc', '.txt'}

def validate_file_extension(filename: str):
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {ALLOWED_EXTENSIONS}"
        )
    return ext

@app.post("/upload")
async def upload_document(
    file: UploadFile,
    current_user: User = Depends(get_current_user)
):
    try:
        # Validate file extension
        validate_file_extension(file.filename)
        
        # Process and store document
        content = await file.read()
        processor = DocumentProcessor()
        version_info = await processor.process_and_store_document(
            content,
            file.filename,
            current_user.username
        )
        
        return {
            "message": "Document processed successfully",
            "version_info": version_info
        }
    except Exception as e:
        logging.error(f"Error processing document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query_documents(
    query: Query,
    current_user: User = Depends(get_current_user)
):
    try:
        engine = QueryEngine()
        response = await engine.process_query(query.question, current_user.username)
        return {"answer": response}
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/document/versions/{filename}")
async def get_document_versions(
    filename: str,
    current_user: User = Depends(get_current_user)
):
    processor = DocumentProcessor()
    versions = processor.version_collection.query(
        query_texts=[filename],
        where={"filename": filename}
    )
    return {"versions": versions['documents']} 