#!/usr/bin/env python
"""
Test script to add sample leads to the Lead Capture Agent database
"""
import requests
import json

BASE_URL = "http://localhost:8000"

# Sample leads
sample_leads = [
    {
        "phone": "+92300123456",
        "message": "I want to buy your product, can you tell me more about pricing?",
        "channel": "whatsapp",
        "sender_name": "Ahmed Khan"
    },
    {
        "email": "sarah@example.com",
        "message": "Can you help me with product features?",
        "channel": "website",
        "sender_name": "Sarah Ali"
    },
    {
        "phone": "+92333999888",
        "message": "Your service is terrible, where is customer support?",
        "channel": "whatsapp",
        "sender_name": "Hassan"
    },
    {
        "email": "john@business.com",
        "message": "We are looking for enterprise solutions for our company",
        "channel": "email",
        "sender_name": "John Business"
    }
]

print("=" * 60)
print("LEAD CAPTURE AGENT - TEST DATA LOADER")
print("=" * 60)

# Add test leads
added_count = 0
for i, lead in enumerate(sample_leads, 1):
    try:
        response = requests.post(
            f"{BASE_URL}/api/webhook",
            json=lead,
            timeout=5
        )
        if response.status_code == 200:
            print(f"✓ Test Lead {i} ({lead['sender_name']}) - Added successfully")
            added_count += 1
        else:
            print(f"✗ Test Lead {i} - Error: Status {response.status_code}")
    except Exception as e:
        print(f"✗ Test Lead {i} - Connection Error: {e}")

print("\n" + "=" * 60)
print(f"Total Leads Added: {added_count}/{len(sample_leads)}")
print("=" * 60)
print("\n📊 DASHBOARD LINK:")
print("http://localhost:8000/static/dashboard.html")
print("\n📈 API ENDPOINTS:")
print("  - Get All Leads: http://localhost:8000/api/webhook/leads")
print("  - Get Stats: http://localhost:8000/api/webhook/stats")
print("\n" + "=" * 60)
