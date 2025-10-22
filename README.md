# JobAI Applier MVP

AI-powered job application automation tool with FastAPI and Gemini AI integration.

## Features

- 🚀 FastAPI backend with async support
- 🤖 Gemini AI integration for job search
- 📝 Pydantic models for request/response validation
- 🔧 Environment-based configuration
- 📚 Auto-generated API documentation

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
   python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Access the API:**
   - API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

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
├── .env                 # Environment variables (API keys)
├── requirements.txt     # Python dependencies
├── test_endpoint.py     # Test script for API endpoints
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

- [ ] Add user authentication
- [ ] Implement job application automation
- [ ] Add database for job tracking
- [ ] Create frontend interface
- [ ] Add email integration for applications
- [ ] Implement resume tailoring with AI

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **Gemini AI**: Google's generative AI for job content creation
- **Pydantic**: Data validation and settings management
- **Python-dotenv**: Environment variable management
- **Uvicorn**: ASGI web server implementation for production