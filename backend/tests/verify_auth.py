import requests
import json

BASE_URL = 'http://localhost:5000/api'

def test_signup_login():
    # 1. Signup with email
    username = "testuser_new_auth"
    password = "password123"
    display_name = "Test User"
    email = "testuser@example.com"
    
    print(f"Attempting signup for {username}...")
    signup_payload = {
        "username": username,
        "password": password,
        "display_name": display_name,
        "email": email
    }
    
    try:
        response = requests.post(f"{BASE_URL}/signup", json=signup_payload)
        if response.status_code == 201:
            print("Signup successful!")
            user_data = response.json()
            print(f"User created: {user_data}")
        elif response.status_code == 409:
            print("User already exists (expected if running multiple times).")
        else:
            print(f"Signup failed: {response.status_code} - {response.text}")
            return

        # 2. Login with correct password
        print(f"Attempting login for {username}...")
        login_payload = {
            "username": username,
            "password": password
        }
        response = requests.post(f"{BASE_URL}/login", json=login_payload)
        
        if response.status_code == 200:
            print("Login successful!")
            user_data = response.json()
            print(f"Logged in user: {user_data}")
        else:
            print(f"Login failed: {response.status_code} - {response.text}")
            
        # 3. Login with WRONG password
        print(f"Attempting login with WRONG password...")
        wrong_login_payload = {
            "username": username,
            "password": "wrongpassword"
        }
        response = requests.post(f"{BASE_URL}/login", json=wrong_login_payload)
        
        if response.status_code == 401:
            print("Login with wrong password failed as expected.")
        else:
            print(f"Unexpected result for wrong password: {response.status_code} - {response.text}")

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure the backend is running.")

if __name__ == "__main__":
    test_signup_login()
