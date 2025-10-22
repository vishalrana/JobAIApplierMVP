#!/usr/bin/env python3
"""
Test script for the /search_jobs endpoint
Run this after restarting the server with updated code
"""

import requests
import json

def test_search_jobs():
    """Test the search_jobs endpoint with sample data"""

    # Test data
    test_payload = {
        "title": "Product Manager",
        "location": "Bangalore",
        "ctc": "10-15 LPA"
    }

    try:
        # Make request to the endpoint (CORS-enabled server with Gemini AI)
        response = requests.post(
            'http://127.0.0.1:8002/search_jobs',
            json=test_payload,
            timeout=30  # Increased timeout for AI API calls
        )

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            jobs = response.json()
            print(f"✅ Success! Found {len(jobs)} jobs:")
            print(json.dumps(jobs, indent=2))

            # Validate response structure
            for i, job in enumerate(jobs):
                required_fields = ['company', 'title', 'description', 'emails', 'phone']
                missing_fields = [field for field in required_fields if field not in job]
                if missing_fields:
                    print(f"⚠️  Job {i+1} missing fields: {missing_fields}")
                else:
                    print(f"✅ Job {i+1} has all required fields")

        else:
            print(f"❌ Error: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on http://127.0.0.1:8002")
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    print("Testing /search_jobs endpoint...")
    test_search_jobs()