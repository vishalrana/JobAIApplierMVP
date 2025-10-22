"""
Main FastAPI application for JobAI Applier MVP.

This module sets up the core FastAPI application with basic configuration
and endpoints for the AI-powered job application tool.

Key Features:
- FastAPI web framework for building APIs
- Environment variable loading via python-dotenv
- Health check endpoint for monitoring
- Minimal setup ready for AI and job application features
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import google.generativeai as genai
from pydantic import BaseModel
from typing import List, Optional

# Load environment variables from .env file
load_dotenv()

# Configure Gemini AI with API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Email configuration from environment
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
RESUME_FILE_PATH = os.getenv("RESUME_FILE_PATH")

# Pydantic models for request/response
class JobSearchRequest(BaseModel):
    """Request model for job search endpoint."""
    title: str
    location: str
    ctc: Optional[str] = None  # CTC = Cost to Company (salary range) - now optional

class JobPosting(BaseModel):
    """Response model for individual job posting."""
    company: str
    title: str
    description: str
    emails: str
    phone: str

class CoverLetterRequest(BaseModel):
    """Request model for cover letter generation."""
    job_title: str
    company: str
    resume_text: str

class EmailRequest(BaseModel):
    """Request model for sending job application emails."""
    to_emails: List[str]
    subject: str
    body: str
    resume_file: Optional[str] = None  # Optional for MVP

# Create FastAPI application instance
app = FastAPI(
    title="JobAI Applier MVP",
    description="AI-powered job application automation tool",
    version="1.0.0"
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080", "http://localhost:8081", "http://127.0.0.1:8081"],  # Frontend servers
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.

    Returns:
        dict: Status message indicating the MVP is ready

    This endpoint serves as a simple monitoring check and confirms
    that the FastAPI application is running properly.
    """
    return {"status": "MVP ready"}

# Gemini AI job search functionality
async def generate_jobs_with_gemini(title: str, location: str, ctc: Optional[str] = None) -> List[JobPosting]:
    """
    Generate realistic job postings using Gemini AI.

    Args:
        title: Job title (e.g., "Product Manager")
        location: Job location (e.g., "Bangalore")
        ctc: Salary range (e.g., "10-15 LPA")

    Returns:
        List of job postings in the specified format

    Raises:
        HTTPException: If Gemini API key is not configured or API call fails
    """
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Gemini API key not configured. Please add GEMINI_API_KEY to .env file."
        )

    try:
        # Initialize Gemini model (using gemini-2.5-flash as requested)
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Create detailed prompt for realistic job generation
        ctc_text = f" at {ctc} salary range" if ctc else ""
        prompt = f"""
        Generate 3 realistic job postings for {title} position in {location}{ctc_text}.
        Each job should include:
        - Company name (realistic tech/IT company)
        - Exact job title
        - Brief description snippet (2-3 sentences)
        - HR contact email (if none exists, suggest hr@company.com format)
        - Phone number (Bangalore format: +91-80-XXXX-XXXX)

        Output as a JSON array of objects with this exact structure:
        [
            {{
                "company": "Company Name",
                "title": "Job Title",
                "description": "Brief description snippet",
                "emails": "hr@company.com",
                "phone": "+91-80-1234-5678"
            }}
        ]

        Make the jobs realistic for the Indian market and {location} specifically.
        """

        # Generate response from Gemini
        response = model.generate_content(prompt)

        # Parse JSON response
        try:
            # Extract JSON from response text
            response_text = response.text.strip()
            # Find JSON array in response (in case of extra text)
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON array found in response")

            json_str = response_text[start_idx:end_idx]
            jobs_data = json.loads(json_str)

            # Convert to JobPosting objects
            jobs = []
            for job_data in jobs_data:
                jobs.append(JobPosting(**job_data))

            return jobs

        except (json.JSONDecodeError, ValueError, KeyError) as e:
            # If JSON parsing fails, create a fallback response
            print(f"Failed to parse Gemini response: {e}")
            return [
                JobPosting(
                    company="Tech Solutions Ltd",
                    title=f"{title}",
                    description=f"We are looking for a skilled {title} to join our team in {location}. Competitive salary package offered.",
                    emails="hr@techsolutions.com",
                    phone="+91-80-1234-5678"
                )
            ]

    except Exception as e:
        print(f"Gemini API error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate job listings. Please check your API quota and try again."
        )

@app.post("/search_jobs", response_model=List[JobPosting])
async def search_jobs(request: JobSearchRequest):
    """
    Search for jobs using AI-generated mock data.

    This endpoint uses Gemini AI to generate realistic job postings
    based on the provided title, location, and CTC (Cost to Company).

    Request Body:
        - title: Job title (e.g., "Product Manager")
        - location: Job location (e.g., "Bangalore")
        - ctc: Salary range (e.g., "10-15 LPA")

    Returns:
        List of job postings with company, title, description, emails, and phone
    """
    jobs = await generate_jobs_with_gemini(request.title, request.location, request.ctc)
    return jobs

@app.post("/generate_cover")
async def generate_cover_letter(request: CoverLetterRequest):
    """
    Generate a professional cover letter using Gemini AI.

    This endpoint creates a personalized cover letter based on the job title,
    company, and resume text provided.

    Request Body:
        - job_title: Target job title (e.g., "Product Manager")
        - company: Target company name (e.g., "TechCorp Solutions")
        - resume_text: Resume content/skills to highlight

    Returns:
        dict: Contains the generated cover letter text
    """
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Gemini API key not configured. Please add GEMINI_API_KEY to .env file."
        )

    try:
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Create cover letter prompt
        prompt = f"""
        Write a 150-word professional cover letter for {request.job_title} position at {request.company}.
        Highlight relevant skills and experiences from this resume: {request.resume_text}.

        The cover letter should:
        - Be professional and concise (around 150 words)
        - Show enthusiasm for the role and company
        - Connect resume skills to job requirements
        - Include a strong opening and closing
        - Be ready to copy-paste into an email

        Format it as a proper business letter with:
        - Greeting (Dear Hiring Manager,)
        - 3-4 paragraphs
        - Professional closing (Best regards, [Name])
        """

        # Generate cover letter
        response = model.generate_content(prompt)
        cover_letter = response.text.strip()

        return {"cover_letter": cover_letter}

    except Exception as e:
        print(f"Cover letter generation error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate cover letter. Please try again."
        )

@app.post("/send_email")
async def send_job_application(request: EmailRequest):
    """
    Send job application email with cover letter and resume attachment.

    This endpoint sends an email with the cover letter as body and attaches
    the resume PDF file to the specified email addresses.

    Request Body:
        - to_emails: List of recipient email addresses
        - subject: Email subject line
        - body: Cover letter content
        - resume_file: Path to resume PDF file (optional)

    Returns:
        dict: Success message with confirmation details
    """
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        raise HTTPException(
            status_code=500,
            detail="Gmail credentials not configured. Please add GMAIL_USER and GMAIL_APP_PASSWORD to .env file."
        )

    # Create email message
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = ', '.join(request.to_emails)
    msg['Subject'] = request.subject

    # Add cover letter as email body
    msg.attach(MIMEText(request.body, 'plain'))

    # Attach resume PDF if file exists (optional for MVP)
    attachment_status = "No attachment"
    try:
        if request.resume_file and os.path.exists(request.resume_file):
            with open(request.resume_file, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment; filename=Resume.pdf")
                msg.attach(part)
            print(f"✅ Resume attached: {request.resume_file}")
            attachment_status = "Resume.pdf"
        else:
            print(f"ℹ️ No resume file attached (MVP mode)")
    except PermissionError as e:
        print(f"⚠️ Permission denied accessing resume file: {e}")
    except Exception as e:
        print(f"⚠️ Error attaching resume file: {e}")

    # Send email via Gmail SMTP (using a more compatible approach for FastAPI)
    email_sent = False
    error_details = ""

    try:
        print(f"📧 Attempting to send email to: {', '.join(request.to_emails)}")
        print(f"📧 Subject: {request.subject}")
        print(f"📧 Gmail User: {GMAIL_USER}")

        # Validate credentials before attempting connection
        if len(GMAIL_APP_PASSWORD) != 16:
            print(f"⚠️ App Password length issue: {len(GMAIL_APP_PASSWORD)} characters (expected 16)")
        if ' ' in GMAIL_APP_PASSWORD:
            print("⚠️ App Password contains spaces")

        # Create SMTP connection (use context manager for better cleanup)
        print("🔗 Connecting to Gmail SMTP...")
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            # Set timeout to prevent hanging
            server.timeout = 30

            print("🔒 Starting TLS...")
            server.starttls()

            print("🔑 Attempting login...")
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            print("✅ SMTP authentication successful")

            # Send email
            text = msg.as_string()
            print(f"📤 Sending email to {len(request.to_emails)} recipient(s)...")
            print(f"📤 Email content length: {len(text)} characters")

            result = server.sendmail(GMAIL_USER, request.to_emails, text)
            print(f"✅ Email sent successfully! Server response: {result}")
            email_sent = True

    except smtplib.SMTPAuthenticationError as e:
        error_details = f"Authentication failed: {e}"
        print(f"❌ Authentication error: {error_details}")

        # Provide detailed troubleshooting information
        raise HTTPException(
            status_code=500,
            detail="Gmail authentication failed. Please check your credentials and follow these steps:\n"
                   "1. Enable 2-factor authentication on your Google account\n"
                   "2. Generate an App Password: https://myaccount.google.com/apppasswords\n"
                   "3. Use the 16-character App Password (not your regular password)\n"
                   "4. Update GMAIL_USER and GMAIL_APP_PASSWORD in .env file\n"
                   f"Error details: {error_details}"
        )
    except smtplib.SMTPRecipientsRefused as e:
        error_details = f"Recipients refused: {e}"
        print(f"❌ Recipients refused: {error_details}")
        raise HTTPException(
            status_code=500,
            detail=f"Email recipients refused the message: {error_details}"
        )
    except smtplib.SMTPServerDisconnected as e:
        error_details = f"Server disconnected: {e}"
        print(f"❌ Server disconnected: {error_details}")
        raise HTTPException(
            status_code=500,
            detail=f"Email server disconnected: {error_details}"
        )
    except Exception as e:
        error_details = f"Unexpected error: {e}"
        print(f"❌ Unexpected email error: {error_details}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send email: {error_details}"
        )

    # Return success response (whether real or demo)
    status = "sent" if email_sent else "prepared"
    mode_indicator = " (Demo Mode)" if not email_sent else ""

    return {
        "success": True,
        "message": f"Email {status} successfully{mode_indicator}!",
        "status": "success",
        "to": request.to_emails,
        "subject": request.subject,
        "demo_mode": not email_sent,
        "attachment": attachment_status,
        "details": f"Email {status} to {len(request.to_emails)} recipient(s) with subject: '{request.subject}'"
    }