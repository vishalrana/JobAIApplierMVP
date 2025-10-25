# JobAI Applier MVP

AI-powered job application automation tool with FastAPI and Gemini AI integration.

## Features

- 🚀 FastAPI backend with async support
- 🤖 Gemini AI integration for job search and email subject generation
- 📝 Pydantic models for request/response validation
- 🔧 Environment-based configuration
- 📚 Auto-generated API documentation
- 📄 Document upload and text extraction (PDF, DOC, DOCX, TXT)
- 📧 AI-powered email subject generation
- 📨 Automated job application emails with custom content

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   # Copy and update .env file
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```

3. **Run the server:**
   ```bash
   cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access the API:**
   - API Docs: http://127.0.0.1:8000/docs
   - Health Check: http://127.0.0.1:8000/health

## API Endpoints

### GET /health
Health check endpoint that returns the application status.

**Response:**
```json
{"status": "MVP ready"}
```

### POST /search_jobs
Generate AI-powered job listings based on search criteria.

**Request Body:**
```json
{
  "title": "Product Manager",
  "location": "Bangalore",
  "ctc": "10-15 LPA"
}
```

**Response:**
```json
[
  {
    "company": "Tech Solutions Ltd",
    "title": "Senior Product Manager",
    "description": "We are looking for an experienced Product Manager to lead our product strategy and drive growth initiatives.",
    "emails": "hr@techsolutions.com",
    "phone": "+91-80-1234-5678"
  }
]
```

### POST /generate_cover
Generate AI-powered cover letters based on job requirements and resume content.

**Request Body:**
```json
{
  "job_title": "Product Manager",
  "company": "Tech Solutions Ltd",
  "resume_text": "Experienced Product Manager with 5+ years..."
}
```

**Response:**
```json
{
  "cover_letter": "Dear Hiring Manager,\n\nI am writing to express..."
}
```

### POST /extract_text
Extract text content from uploaded files (PDF, DOC, DOCX, TXT).

**Request Body:** Form data with file upload
```
file: [uploaded_file]
```

**Response:**
```json
{
  "text": "Extracted text content...",
  "filename": "resume.pdf",
  "file_size": 1024,
  "content_type": "application/pdf"
}
```

### POST /generate_subject
Generate AI-powered email subject lines for job applications.

**Request Body:**
```json
{
  "job_title": "Product Manager",
  "company": "Tech Solutions Ltd",
  "cover_letter_content": "Dear Hiring Manager...",
  "job_description": "Looking for experienced PM..."
}
```

**Response:**
```json
{
  "subject": "Experienced SaaS Product Manager - Tech Solutions Ltd",
  "job_title": "Product Manager",
  "company": "Tech Solutions Ltd"
}
```

### POST /send_email
Send job application emails with attachments.

**Request Body:**
```json
{
  "to_emails": ["hr@company.com"],
  "subject": "Product Manager Application",
  "body": "Cover letter content...",
  "resume_file": "path/to/resume.pdf"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Email sent successfully!",
  "status": "success",
  "attachment": "Resume.pdf"
}
```

## Gemini AI Integration

The application uses Google's Gemini 2.5 Flash model to generate realistic job postings based on:

- **Job Title**: The position you're looking for
- **Location**: City/location for the job
- **CTC**: Cost to Company (salary range) in LPA format

### AI Prompt Strategy

The system generates 3-5 realistic job postings with:
- Authentic company names
- Detailed job descriptions
- Contact information (email/phone)
- Location-specific details

### Error Handling

- **API Key Missing**: Returns 500 error if `GEMINI_API_KEY` not configured
- **Quota Exceeded**: Returns 500 error if API quota exceeded
- **Parsing Errors**: Falls back to template response if AI response parsing fails

## Project Structure

```
JobAIApplierMVP/
├── backend/
│   └── main.py          # FastAPI application with Gemini integration
├── frontend/
│   ├── index.html       # Frontend interface with file upload
│   └── script.js        # JavaScript for file handling and API calls
├── uploads/             # Directory for uploaded documents
├── .env                 # Environment variables (API keys)
├── requirements.txt     # Python dependencies
├── test_endpoint.py     # Test script for API endpoints
├── test_complete_workflow.py # Complete workflow testing
└── README.md           # This file
```

## Development

### Testing the API

Run the test script to verify endpoints:
```bash
python test_endpoint.py
```

### Adding New Features

The current structure supports easy expansion:
- Add new Pydantic models for additional endpoints
- Extend Gemini integration for more AI features
- Add database integration when needed
- Implement authentication/authorization

## Next Steps

- [x] ~~Create frontend interface~~ - ✅ Completed with file upload functionality
- [x] ~~Add email integration for applications~~ - ✅ Completed with Gmail SMTP
- [x] ~~Implement resume tailoring with AI~~ - ✅ Completed with text extraction
- [ ] Add user authentication and user management
- [ ] Implement job application tracking database
- [ ] Add resume parsing and keyword optimization
- [ ] Create job application analytics dashboard
- [ ] Add multiple resume templates and customization

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **Gemini AI**: Google's generative AI for job content creation
- **Pydantic**: Data validation and settings management
- **Python-dotenv**: Environment variable management
- **Uvicorn**: ASGI web server implementation for production