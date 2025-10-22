#!/usr/bin/env python3
"""
Debug script to compare credentials between test_gmail.py and backend
"""

from dotenv import load_dotenv
import os

def debug_credentials():
    """Compare credentials loaded in different contexts"""

    print("Debugging Credential Loading")
    print("=" * 50)

    # Test loading in standalone script context
    print("\n1. Standalone script context:")
    load_dotenv()
    user1 = os.getenv("GMAIL_USER")
    password1 = os.getenv("GMAIL_APP_PASSWORD")

    print(f"   GMAIL_USER: {user1}")
    print(f"   GMAIL_APP_PASSWORD: {password1[:10]}...{password1[-4:] if password1 and len(password1) > 10 else password1}")

    # Check for .env file
    print(f"\n2. .env file exists: {os.path.exists('.env')}")

    if os.path.exists('.env'):
        print("   .env file contents:")
        with open('.env', 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines, 1):
                if 'GMAIL' in line:
                    print(f"   Line {i}: {line.strip()}")

    # Test loading again (simulating FastAPI context)
    print("\n3. Reloading in same context:")
    load_dotenv()
    user2 = os.getenv("GMAIL_USER")
    password2 = os.getenv("GMAIL_APP_PASSWORD")

    print(f"   GMAIL_USER: {user2}")
    print(f"   GMAIL_APP_PASSWORD: {password2[:10]}...{password2[-4:] if password2 and len(password2) > 10 else password2}")

    # Check if credentials match
    print("\n4. Credential comparison:")
    print(f"   Users match: {user1 == user2}")
    print(f"   Passwords match: {password1 == password2}")
    print(f"   Password1 length: {len(password1) if password1 else 'None'}")
    print(f"   Password2 length: {len(password2) if password2 else 'None'}")

    if password1 and password2:
        print(f"   Passwords identical: {password1 == password2}")
        print(f"   Password1 type: {type(password1)}")
        print(f"   Password2 type: {type(password2)}")

    print("\n5. Validation:")
    if password1 and len(password1) != 16:
        print(f"   WARNING: Password1 length {len(password1)} != 16")
    if password2 and len(password2) != 16:
        print(f"   WARNING: Password2 length {len(password2)} != 16")

if __name__ == "__main__":
    debug_credentials()