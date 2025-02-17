from typing import List
import fitz  # PyMuPDF for PDF processing
from docx import Document
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from datetime import datetime
import hashlib
import logging

# Set up logging
logging.basicConfig(
    filename='document_operations.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        self.embeddings = OpenAIEmbeddings()
        self.db = chromadb.Client()
        self.collection = self.db.create_collection("healthcare_docs")
        self.version_collection = self.db.create_collection("document_versions")

    def process_pdf(self, file_path: str) -> List[str]:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return self.text_splitter.split_text(text)

    def process_docx(self, file_path: str) -> List[str]:
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return self.text_splitter.split_text(text)

    def store_documents(self, chunks: List[str], metadata: dict):
        # Store chunks in ChromaDB with metadata
        embeddings = self.embeddings.embed_documents(chunks)
        self.collection.add(
            embeddings=embeddings,
            documents=chunks,
            metadata=[metadata] * len(chunks)
        )

    def calculate_document_hash(self, content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()

    async def process_and_store_document(self, file_content: bytes, filename: str, user: str):
        # Calculate document hash
        doc_hash = self.calculate_document_hash(file_content)
        
        # Check if this is a new version
        version = 1
        existing_versions = self.version_collection.query(
            query_texts=[filename],
            where={"filename": filename}
        )
        
        if existing_versions['documents']:
            version = len(existing_versions['documents']) + 1
        
        # Store version metadata
        version_metadata = {
            "filename": filename,
            "version": version,
            "hash": doc_hash,
            "uploaded_by": user,
            "upload_date": datetime.utcnow().isoformat(),
        }
        
        # Process document
        chunks = []
        if filename.endswith('.pdf'):
            chunks = self.process_pdf(filename)
        elif filename.endswith('.docx'):
            chunks = self.process_docx(filename)
        
        # Store document with version info
        self.store_documents(chunks, {
            **version_metadata,
            "chunk_index": list(range(len(chunks)))
        })
        
        # Log the operation
        logging.info(
            f"Document processed: {filename}, Version: {version}, "
            f"User: {user}, Hash: {doc_hash}"
        )
        
        return version_metadata 