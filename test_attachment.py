#!/usr/bin/env python3
"""
Test script specifically for resume PDF attachment functionality
"""

import requests

def test_attachment_functionality():
    """Test that resume PDF attachment is working properly"""

    base_url = 'http://127.0.0.1:8000'

    print("Testing Resume PDF Attachment Functionality")
    print("=" * 50)

    # Test data
    test_payload = {
        "to_emails": ["test@example.com"],
        "subject": "Resume Attachment Test",
        "body": "This is a test email with resume attachment.",
        "resume_file": "G:\\My Drive\\Resume & Documents\\Resume\\Resume\\Product Management\\Resume.pdf"
    }

    try:
        print(f"Sending email with attachment to: {test_payload['to_emails']}")
        print(f"Resume file: {test_payload['resume_file']}")

        response = requests.post(
            f'{base_url}/send_email',
            json=test_payload,
            timeout=30
        )

        print(f"\nResponse Status: {response.status_code}")

        if response.status_code == 200:
            response_data = response.json()
            print("SUCCESS: Email sent successfully!")
            print(f"Subject: {response_data.get('subject')}")
            print(f"Attachment: {response_data.get('attachment')}")
            print(f"Email size: {response_data.get('details', 'N/A')}")

            if response_data.get('attachment') == 'Resume.pdf':
                print("\nSUCCESS: Resume PDF attachment is working correctly!")
                return True
            else:
                print(f"\nWARNING: Expected attachment 'Resume.pdf', got '{response_data.get('attachment')}'")
                return False
        else:
            print(f"ERROR: Email sending failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to backend server")
        print(f"Make sure the server is running on {base_url}")
        return False
    except requests.exceptions.Timeout:
        print("ERROR: Request timed out")
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_attachment_functionality()

    if success:
        print("\nResume attachment test PASSED!")
    else:
        print("\nResume attachment test FAILED!")