#!/usr/bin/env python3
"""
Test script to verify Gmail SMTP credentials and sending capability
Run this independently to test if Gmail credentials work before integrating into the main app
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

def test_gmail_credentials():
    """Test Gmail SMTP authentication and sending"""

    # Load environment variables
    load_dotenv()

    GMAIL_USER = os.getenv("GMAIL_USER")
    GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        print("ERROR: Gmail credentials not found in .env file")
        return False

    print(f"Testing Gmail credentials for: {GMAIL_USER}")
    print("=" * 50)

    try:
        # Create a simple test email
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = GMAIL_USER  # Send to self for testing
        msg['Subject'] = "JobAI Applier MVP - Test Email"

        body = "This is a test email from JobAI Applier MVP to verify Gmail SMTP functionality."
        msg.attach(MIMEText(body, 'plain'))

        print("Connecting to Gmail SMTP...")
        server = smtplib.SMTP('smtp.gmail.com', 587)

        print("Starting TLS encryption...")
        server.starttls()

        print("Authenticating...")
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)

        print("Sending test email...")
        text = msg.as_string()
        result = server.sendmail(GMAIL_USER, [GMAIL_USER], text)

        print("Closing connection...")
        server.quit()

        print(f"SUCCESS: Email sent successfully! Server response: {result}")
        print(f"Test email sent from {GMAIL_USER} to {GMAIL_USER}")
        return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"ERROR: Authentication failed: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you're using an App Password, not your regular Gmail password")
        print("2. Enable 2-factor authentication on your Google account")
        print("3. Generate an App Password: https://myaccount.google.com/apppasswords")
        print("4. Make sure the App Password is exactly 16 characters")
        return False

    except smtplib.SMTPRecipientsRefused as e:
        print(f"ERROR: Recipients refused: {e}")
        return False

    except smtplib.SMTPServerDisconnected as e:
        print(f"ERROR: Server disconnected: {e}")
        return False

    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        return False

def test_gmail_without_sending():
    """Test Gmail connection without actually sending an email"""

    load_dotenv()

    GMAIL_USER = os.getenv("GMAIL_USER")
    GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        print("ERROR: Gmail credentials not found in .env file")
        return False

    print(f"Testing Gmail connection for: {GMAIL_USER}")
    print("=" * 50)

    try:
        print("Connecting to Gmail SMTP...")
        server = smtplib.SMTP('smtp.gmail.com', 587)

        print("Starting TLS...")
        server.starttls()

        print("Testing authentication...")
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)

        print("SUCCESS: Authentication successful!")
        print("Closing connection...")
        server.quit()

        print("SUCCESS: Gmail connection test passed!")
        return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"ERROR: Authentication failed: {e}")
        print("\nCommon issues and solutions:")
        print("1. Wrong password type - Use App Password, not regular password")
        print("2. 2FA not enabled - Enable 2-factor authentication first")
        print("3. Wrong App Password - Regenerate at https://myaccount.google.com/apppasswords")
        return False

    except Exception as e:
        print(f"ERROR: Connection error: {e}")
        return False

if __name__ == "__main__":
    print("Gmail SMTP Test for JobAI Applier MVP")
    print("=" * 50)

    # First test connection only
    print("\n1. Testing Gmail connection (no email sending)...")
    connection_ok = test_gmail_without_sending()

    if connection_ok:
        print("\n2. Testing actual email sending...")
        test_gmail_credentials()
    else:
        print("\nERROR: Cannot proceed with email sending test until connection works")