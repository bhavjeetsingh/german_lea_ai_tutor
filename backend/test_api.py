"""
Simple test script to verify the API is working.
Run this after starting the server with: python main.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"


def test_health_check():
    """Test health check endpoint."""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def test_create_profile():
    """Test creating a student profile."""
    print("Testing profile creation...")
    data = {
        "name": "Test Student",
        "email": "test@example.com",
        "current_level": "A2",
        "goals": ["Learn German", "Pass B1 exam"],
        "target_exam": "Goethe B1",
        "career_interest": "Engineering"
    }
    
    response = requests.post(f"{BASE_URL}/api/students/profile", json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        profile = response.json()
        print(f"Profile created: {json.dumps(profile, indent=2)}\n")
        return profile["student_id"]
    else:
        print(f"Error: {response.text}\n")
        return None


def test_chat(student_id):
    """Test sending a chat message."""
    if not student_id:
        print("Skipping chat test - no student ID\n")
        return
    
    print("Testing chat message...")
    data = {
        "student_id": student_id,
        "message": "Hallo Lea! How do I use German articles?",
        "teaching_mode": "grammar_practice"
    }
    
    response = requests.post(f"{BASE_URL}/api/chat/message", json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        chat_response = response.json()
        print(f"Chat response:\n{json.dumps(chat_response, indent=2)}\n")
        return chat_response["session_id"]
    else:
        print(f"Error: {response.text}\n")
        return None


def test_get_profile(student_id):
    """Test retrieving a profile."""
    if not student_id:
        print("Skipping profile retrieval test - no student ID\n")
        return
    
    print("Testing profile retrieval...")
    response = requests.get(f"{BASE_URL}/api/students/profile/{student_id}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        profile = response.json()
        print(f"Profile: {json.dumps(profile, indent=2)}\n")
    else:
        print(f"Error: {response.text}\n")


def main():
    print("=" * 60)
    print("GermanLeap Lea API Test Suite")
    print("=" * 60 + "\n")
    
    try:
        # Test 1: Health check
        test_health_check()
        
        # Test 2: Create profile
        student_id = test_create_profile()
        
        # Test 3: Get profile
        test_get_profile(student_id)
        
        # Test 4: Chat (requires API key)
        print("⚠️  Chat test requires a valid API key in .env")
        user_input = input("Run chat test? (y/n): ")
        if user_input.lower() == 'y':
            test_chat(student_id)
        
        print("=" * 60)
        print("Tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to the server.")
        print("Make sure the server is running with: python main.py")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
