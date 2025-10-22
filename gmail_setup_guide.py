#!/usr/bin/env python3
"""
Gmail Setup Guide for JobAI Applier MVP
Run this script to get step-by-step instructions for setting up Gmail
"""

def show_gmail_setup_guide():
    """Display comprehensive Gmail setup instructions"""

    print("Gmail Setup Guide for JobAI Applier MVP")
    print("=" * 50)
    print()

    print("PROBLEM: Your Gmail credentials are incorrect.")
    print("SOLUTION: Follow these steps to set up Gmail App Passwords")
    print()

    print("STEP 1: Enable 2-Factor Authentication")
    print("-" * 40)
    print("1. Go to https://myaccount.google.com")
    print("2. Navigate to 'Security'")
    print("3. Enable '2-Step Verification'")
    print("4. Follow the setup process")
    print()

    print("STEP 2: Generate App Password")
    print("-" * 40)
    print("1. Go to https://myaccount.google.com/apppasswords")
    print("2. Sign in with your Gmail account")
    print("3. Select 'Mail' as the app")
    print("4. Select 'Other (custom name)' as the device")
    print("5. Enter 'JobAI Applier MVP' as the custom name")
    print("6. Click 'Generate'")
    print("7. Copy the 16-character password (e.g., 'abcd-efgh-ijkl-mnop')")
    print()

    print("STEP 3: Update .env File")
    print("-" * 40)
    print("Update these values in your .env file:")
    print()
    print("GMAIL_USER=your-email@gmail.com")
    print("GMAIL_APP_PASSWORD=your-16-character-app-password")
    print()
    print("IMPORTANT:")
    print("- Use your full Gmail address (including @gmail.com)")
    print("- Use the App Password, NOT your regular password")
    print("- Make sure there are no spaces in the App Password")
    print("- Do NOT include quotes around the password")
    print()

    print("STEP 4: Test Configuration")
    print("-" * 40)
    print("Run this command to test your Gmail setup:")
    print("python test_gmail.py")
    print()

    print("STEP 5: Common Issues & Solutions")
    print("-" * 40)
    print("❌ 'Username and Password not accepted'")
    print("   → Make sure you're using an App Password, not regular password")
    print()
    print("❌ 'Please log in via your web browser'")
    print("   → Enable 2FA first, then generate App Password")
    print()
    print("❌ 'Application-specific password required'")
    print("   → Generate a new App Password for 'JobAI Applier MVP'")
    print()

    print("Current .env file status:")
    print("-" * 40)

    try:
        with open('.env', 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines, 1):
                if 'GMAIL' in line:
                    print(f"Line {i}: {line.strip()}")
    except FileNotFoundError:
        print("❌ .env file not found")

    print()
    print("Need help? Check the Gmail App Password documentation:")
    print("https://support.google.com/accounts/answer/185833")

if __name__ == "__main__":
    show_gmail_setup_guide()