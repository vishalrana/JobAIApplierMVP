/**
 * JobAI Applier Frontend - Vanilla JavaScript
 *
 * This script handles the job search form submission and communicates
 * with the FastAPI backend to fetch AI-generated job listings.
 *
 * Backend Connection:
 * - Uses fetch API to make POST requests to the /search_jobs endpoint
 * - Sends form data as JSON with Content-Type: application/json
 * - Backend URL is configurable (currently set to port 8001)
 * - Handles both success and error responses from the API
 */

// DOM elements (cached for performance)
const jobSearchForm = document.getElementById('jobSearchForm');
const loadingElement = document.getElementById('loading');
const errorElement = document.getElementById('error');
const jobsTableBody = document.getElementById('jobsTableBody');


// Backend API configuration
const API_CONFIG = {
    // Update this URL to match your backend server (CORS-enabled server)
    BASE_URL: 'http://127.0.0.1:8000',
    ENDPOINT: '/search_jobs',
    TIMEOUT: 30000 // 30 seconds for AI API calls
};

/**
 * Initialize the application when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 JobAI Frontend initialized');

    // Add event listener to the form
    if (jobSearchForm) {
        jobSearchForm.addEventListener('submit', handleFormSubmit);
    }


    // Optional: Add real-time form validation
    addFormValidation();

    console.log('🎯 Frontend setup complete');
});

/**
 * Handle form submission
 * @param {Event} event - Form submit event
 */
async function handleFormSubmit(event) {
    event.preventDefault(); // Prevent default form submission

    // Get form data
    const formData = getFormData();

    // Validate required fields
    if (!validateFormData(formData)) {
        showError('Please fill in all required fields (Job Title and Location)');
        return;
    }

    // Clear previous results and errors
    clearResults();
    hideError();

    // Show loading state
    showLoading();

    try {
        // Make API call to backend
        const jobs = await searchJobs(formData);

        // Display results
        displayJobResults(jobs);

    } catch (error) {
        console.error('❌ Search error:', error);
        console.error('Error details:', {
            message: error.message,
            stack: error.stack,
            name: error.name
        });
        showError(getErrorMessage(error));
    } finally {
        hideLoading();
    }
}

/**
 * Extract data from form fields
 * @returns {Object} Form data object
 */
function getFormData() {
    return {
        title: document.getElementById('jobTitle').value.trim(),
        location: document.getElementById('location').value.trim(),
        ctc: document.getElementById('ctc').value.trim() || undefined // Optional field
    };
}

/**
 * Validate form data
 * @param {Object} formData - Form data to validate
 * @returns {boolean} True if valid
 */
function validateFormData(formData) {
    return formData.title && formData.location;
}

/**
 * Search for jobs using the backend API
 * @param {Object} searchData - Search criteria
 * @returns {Promise<Array>} Array of job objects
 */
async function searchJobs(searchData) {
    const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINT}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // Add other headers if needed (e.g., Authorization)
        },
        body: JSON.stringify(searchData),
        // Note: fetch doesn't support timeout directly, using AbortController
    });

    // Handle HTTP errors
    if (!response.ok) {
        let errorMessage = `HTTP ${response.status}: ${response.statusText}`;

        try {
            const errorData = await response.json();
            if (errorData.detail) {
                errorMessage = errorData.detail;
            }
        } catch (parseError) {
            // If we can't parse error response, use status text
            console.warn('Could not parse error response:', parseError);
        }

        throw new Error(errorMessage);
    }

    // Parse and return JSON response
    const jobs = await response.json();
    return jobs;
}

/**
 * Display job results in the table
 * @param {Array} jobs - Array of job objects
 */
function displayJobResults(jobs) {
    // Clear existing rows
    jobsTableBody.innerHTML = '';

    if (!jobs || jobs.length === 0) {
        showNoResults();
        return;
    }

    // Create table rows for each job
    jobs.forEach((job, index) => {
        const row = createJobRow(job, index);
        jobsTableBody.appendChild(row);
    });

    console.log(`✅ Displayed ${jobs.length} job results`);
}

/**
 * Create a table row for a job
 * @param {Object} job - Job object
 * @param {number} index - Job index for styling
 * @returns {HTMLElement} Table row element
 */
function createJobRow(job, index) {
    const row = document.createElement('tr');

    // Add alternating row styling
    if (index % 2 === 1) {
        row.classList.add('alternate-row');
    }

    // Create button with proper event handling
    const sendButton = document.createElement('button');
    sendButton.className = 'send-btn';
    sendButton.textContent = '📧 Send';
    sendButton.onclick = function() {
        sendJobApplication(job.title, job.company, job.emails, this);
    };

    row.innerHTML = `
        <td>${escapeHtml(job.company)}</td>
        <td>${escapeHtml(job.title)}</td>
        <td>${escapeHtml(job.description)}</td>
        <td>${escapeHtml(job.emails)}</td>
        <td>${escapeHtml(job.phone)}</td>
        <td></td>
    `;

    // Add the button to the last cell
    row.lastElementChild.appendChild(sendButton);

    return row;
}

/**
 * Send job application using files from uploads/ folder
 */
async function sendJobApplication(jobTitle, company, toEmails, button) {
    let originalButtonText = '📧 Send';

    try {
        // Disable the button to prevent multiple clicks
        if (button) {
            originalButtonText = button.textContent;
            button.disabled = true;
            button.textContent = '⏳ Sending...';
        }

        console.log(`🚀 Starting job application process for ${jobTitle} at ${company}`);

        // Fetch resume text from backend
        console.log('📄 Fetching resume text...');
        const resumeResponse = await fetch(`${API_CONFIG.BASE_URL}/get_file_text?filename=resume.pdf`);
        if (!resumeResponse.ok) {
            throw new Error(`Resume fetch failed: ${resumeResponse.statusText}`);
        }
        const resumeData = await resumeResponse.json();
        const resumeText = resumeData.text;

        // Fetch cover letter text from backend
        console.log('📄 Fetching cover letter text...');
        const coverResponse = await fetch(`${API_CONFIG.BASE_URL}/get_file_text?filename=cover_template.docx`);
        if (!coverResponse.ok) {
            throw new Error(`Cover letter fetch failed: ${coverResponse.statusText}`);
        }
        const coverData = await coverResponse.json();
        const coverText = coverData.text;

        // Generate AI email subject based on job and cover letter content
        console.log('📧 Generating email subject...');
        const subjectResponse = await fetch(`${API_CONFIG.BASE_URL}/generate_subject`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                job_title: jobTitle,
                company: company,
                cover_letter_content: coverText,
                job_description: `Looking for ${jobTitle} position at ${company}`
            })
        });

        if (!subjectResponse.ok) {
            throw new Error(`Subject generation failed: ${subjectResponse.statusText}`);
        }

        const subjectData = await subjectResponse.json();
        const emailSubject = subjectData.subject;
        console.log(`✅ Email subject generated: ${emailSubject}`);

        // Send email with cover letter content and resume from uploads/
        console.log('📧 Sending email...');

        const emailResponse = await fetch(`${API_CONFIG.BASE_URL}/send_email`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                to_emails: toEmails.split(',').map(email => email.trim()),
                subject: emailSubject,
                body: coverText,
                resume_file: 'uploads/resume.pdf' // Path to resume in uploads/
            })
        });

        const emailData = await emailResponse.json();
        console.log('📧 Email response received:', emailData);

        // Check response structure and show appropriate feedback
        if (emailResponse.ok && emailData.success) {
            // Success - check if real or demo mode
            const modeText = emailData.demo_mode ? ' (Demo Mode)' : '';
            const statusText = emailData.demo_mode ? 'prepared' : 'sent';

            alert(`✅ Application ${statusText} successfully${modeText}!\n\n📧 To: ${toEmails}\n📧 Subject: ${emailData.subject}\n📄 Resume: Attached as ${emailData.attachment}\n📄 Cover Letter: Used from uploads/cover_template.docx\n\n${emailData.demo_mode ? 'Note: Configure Gmail credentials in .env to enable real email sending.' : ''}`);
            console.log('✅ Job application completed:', emailData);
        } else {
            // Handle error responses
            const errorDetail = emailData.detail || emailData.message || 'Unknown error occurred';

            if (errorDetail.includes('authentication failed')) {
                alert(`❌ Gmail Authentication Failed!\n\n${errorDetail}\n\n📧 Please check your Gmail credentials in .env file.`);
            } else {
                alert(`❌ Email sending failed: ${errorDetail}`);
            }

            throw new Error(`Email sending failed: ${errorDetail}`);
        }

    } catch (error) {
        console.error('❌ Send application error:', error);

        let errorMessage = 'Failed to send job application. ';
        if (error.message.includes('Resume')) {
            errorMessage += 'Could not fetch resume.';
        } else if (error.message.includes('Cover')) {
            errorMessage += 'Could not fetch cover letter.';
        } else if (error.message.includes('Subject')) {
            errorMessage += 'Could not generate email subject.';
        } else if (error.message.includes('Email')) {
            errorMessage += 'Could not send email.';
        } else if (error.message.includes('fetch')) {
            errorMessage += 'Network error. Please check if the backend server is running.';
        } else {
            errorMessage += error.message;
        }

        alert(`❌ ${errorMessage}`);
    } finally {
        // Re-enable the button
        if (button) {
            button.disabled = false;
            button.textContent = originalButtonText;
        }
    }
}

/**
 * Show "no results" message
 */
function showNoResults() {
    jobsTableBody.innerHTML = `
        <tr>
            <td colspan="6" class="no-results">
                No jobs found. Try adjusting your search criteria.
            </td>
        </tr>
    `;
}

/**
 * Clear previous search results
 */
function clearResults() {
    jobsTableBody.innerHTML = '';
}

/**
 * Show loading indicator
 */
function showLoading() {
    loadingElement.style.display = 'block';
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    loadingElement.style.display = 'none';
}

/**
 * Show error message
 * @param {string} message - Error message to display
 */
function showError(message) {
    errorElement.textContent = message;
    errorElement.style.display = 'block';
}

/**
 * Hide error message
 */
function hideError() {
    errorElement.style.display = 'none';
}

/**
 * Get user-friendly error message
 * @param {Error} error - Error object
 * @returns {string} User-friendly message
 */
function getErrorMessage(error) {
    const message = error.message || 'An unexpected error occurred. Please try again.';

    // Network/CORS errors
    if (message.includes('Failed to fetch') || message.includes('NetworkError') || message.includes('CORS')) {
        return 'Cannot connect to the backend server. Make sure the server is running on ' + API_CONFIG.BASE_URL;
    }

    // Timeout errors
    if (message.includes('timeout')) {
        return 'Request timed out. The AI is taking longer than expected to generate jobs.';
    }

    // Validation errors (422)
    if (message.includes('422') || message.includes('Unprocessable')) {
        return 'Please check your input data. Job title and location are required fields.';
    }

    // API key errors (500)
    if (message.includes('500') || message.includes('API key')) {
        return 'Backend configuration issue. Please check if the Gemini API key is properly configured.';
    }

    // Return the original error message if it's already user-friendly
    return message;
}

/**
 * Escape HTML to prevent XSS attacks
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Add real-time form validation (optional enhancement)
 */
function addFormValidation() {
    const requiredFields = ['jobTitle', 'location'];

    requiredFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        field.addEventListener('blur', function() {
            if (this.value.trim() === '') {
                this.style.borderColor = '#dc3545';
            } else {
                this.style.borderColor = '#28a745';
            }
        });

        field.addEventListener('focus', function() {
            this.style.borderColor = '#007bff';
        });
    });
}

/**
 * Utility function to test backend connection
 * Call this from browser console: testBackendConnection()
 */
window.testBackendConnection = async function() {
    try {
        const response = await fetch(`${API_CONFIG.BASE_URL}/health`);
        const data = await response.json();
        console.log('✅ Backend connected:', data);
        return true;
    } catch (error) {
        console.error('❌ Backend connection failed:', error);
        return false;
    }
};













