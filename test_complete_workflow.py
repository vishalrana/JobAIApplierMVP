#!/usr/bin/env python3
"""
Test script for the complete JobAI Applier MVP workflow
Tests: Job Search -> Cover Letter Generation -> Email Sending
"""

import requests
import json

def test_complete_workflow():
    """Test the complete workflow from job search to email sending"""

    base_url = 'http://127.0.0.1:8002'

    print("🚀 Testing Complete JobAI Applier MVP Workflow")
    print("=" * 50)

    try:
        # Step 1: Search for jobs
        print("\n1️⃣ Testing Job Search...")
        job_response = requests.post(
            f'{base_url}/search_jobs',
            json={
                'title': 'Product Manager',
                'location': 'Bangalore',
                'ctc': '15-25 LPA'
            },
            timeout=30
        )

        if job_response.status_code != 200:
            print(f"❌ Job search failed: {job_response.status_code}")
            print(f"Error: {job_response.text}")
            return

        jobs = job_response.json()
        print(f"✅ Found {len(jobs)} jobs")

        if not jobs:
            print("❌ No jobs returned")
            return

        # Step 2: Generate cover letter for first job
        print(f"\n2️⃣ Testing Cover Letter Generation...")
        first_job = jobs[0]

        cover_response = requests.post(
            f'{base_url}/generate_cover',
            json={
                'job_title': first_job['title'],
                'company': first_job['company'],
                'resume_text': 'Experienced Product Manager with 5+ years in SaaS, led cross-functional teams, launched successful products serving 100K+ users.'
            },
            timeout=30
        )

        if cover_response.status_code != 200:
            print(f"❌ Cover letter generation failed: {cover_response.status_code}")
            print(f"Error: {cover_response.text}")
            return

        cover_data = cover_response.json()
        cover_letter = cover_data['cover_letter']
        print(f"✅ Generated {len(cover_letter)} character cover letter")
        print(f"📄 Cover letter preview: {cover_letter[:100]}...")

        # Step 3: Send email (demo mode)
        print(f"\n3️⃣ Testing Email Sending (Demo Mode)...")
        email_response = requests.post(
            f'{base_url}/send_email',
            json={
                'to_emails': [first_job['emails']],
                'subject': f'Job Application: {first_job["title"]} at {first_job["company"]}',
                'body': cover_letter
                # No resume_file for demo
            },
            timeout=30
        )

        if email_response.status_code != 200:
            print(f"❌ Email sending failed: {email_response.status_code}")
            print(f"Error: {email_response.text}")
            return

        email_data = email_response.json()
        print(f"✅ Email demo completed: {email_data['message']}")
        print(f"📧 Would send to: {', '.join(email_data['to'])}")
        print(f"📧 Subject: {email_data['subject']}")
        print(f"📧 Demo mode: {email_data.get('demo_mode', 'False')}")

        # Success summary
        print("\n🎉 Complete Workflow Test: SUCCESS!")
        print("=" * 50)
        print("✅ Job Search: Working")
        print("✅ Cover Letter Generation: Working")
        print("✅ Email Sending (Demo): Working")
        print("\n🚀 Your JobAI Applier MVP is ready for frontend testing!")

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server")
        print(f"💡 Make sure the server is running on {base_url}")
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_complete_workflow()