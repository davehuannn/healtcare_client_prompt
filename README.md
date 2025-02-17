# Healthcare Documentation Assistant

A powerful documentation management system designed specifically for healthcare systems, allowing easy access to specifications and technical documentation through natural language queries.

## 🌟 Features

- **Document Processing**
  - Support for PDF, DOCX, DOC, and TXT files
  - Automatic text extraction and chunking
  - Version control for all documents
  - Document metadata tracking

- **Intelligent Querying**
  - Natural language question answering
  - Context-aware responses
  - RAG (Retrieval Augmented Generation) implementation
  - Response caching for improved performance

- **Security**
  - JWT-based authentication
  - Role-based access control
  - Secure document storage
  - Audit logging

- **API Features**
  - Rate limiting
  - CORS support
  - Error handling
  - Request validation

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- FastAPI
- ChromaDB
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/healthcare-docs-assistant.git
cd healthcare-docs-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export SECRET_KEY="your-secret-key"
export OPENAI_API_KEY="your-openai-key"
```

4. Create necessary directories:
```bash
mkdir temp
mkdir logs
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

## 📁 Project Structure

```
healthcare-docs-assistant/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── document_processor.py # Document processing logic
│   ├── query_engine.py      # Query handling
│   └── security.py          # Authentication & authorization
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── data/
│   └── documents/
└── requirements.txt
```

## 🔧 Usage

### Document Upload

```bash
POST /upload
# Uploads and processes a new document
# Requires authentication
# Supports PDF, DOCX, DOC, TXT formats
```

### Query Documents

```bash
POST /query
# Query the document database
# Returns relevant answers based on document context
```

### View Document Versions

```bash
GET /document/versions/{filename}
# Retrieves version history for a specific document
```

## 🔒 Security

- All endpoints require authentication
- Documents are processed and stored securely
- Version history is maintained for audit purposes
- Rate limiting prevents API abuse
- All operations are logged for tracking

## 💡 Use Cases

1. **Technical Support**
   - Quick access to system specifications
   - Instant answers to common technical questions
   - Version tracking for documentation updates

2. **Training**
   - Easy onboarding for new staff
   - Quick reference for procedures and specifications
   - Consistent information access

3. **Documentation Management**
   - Centralized document storage
   - Version control
   - Easy updates and maintenance

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## 🙏 Acknowledgments

- OpenAI for providing the language model capabilities
- FastAPI for the web framework
- ChromaDB for vector storage
- LangChain for document processing
