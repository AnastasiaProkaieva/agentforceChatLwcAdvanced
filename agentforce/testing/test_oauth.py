#!/usr/bin/env python3
"""
Test Salesforce OAuth Authentication
Tests if your Consumer Key/Secret can get an access token
"""

import os
import sys
from pathlib import Path
import requests
from dotenv import load_dotenv

# Load environment variables from parent directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Get configuration from .env
INSTANCE_URL = os.getenv('INSTANCE_URL', '').strip().strip('"')
CONSUMER_KEY = os.getenv('CONSUMER_KEY', '').strip().strip('"')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET', '').strip().strip('"')

def test_oauth():
    """Test OAuth token generation"""
    print("=" * 60)
    print("🔐 Testing OAuth Authentication")
    print("=" * 60)
    
    # Validate configuration
    if not INSTANCE_URL:
        print("❌ ERROR: INSTANCE_URL not found in .env")
        return None
    
    if not CONSUMER_KEY:
        print("❌ ERROR: CONSUMER_KEY not found in .env")
        return None
    
    if not CONSUMER_SECRET:
        print("❌ ERROR: CONSUMER_SECRET not found in .env")
        return None
    
    token_url = f"{INSTANCE_URL}/services/oauth2/token"
    
    payload = {
        'grant_type': 'client_credentials',
        'client_id': CONSUMER_KEY,
        'client_secret': CONSUMER_SECRET
    }
    
    print(f"\n📡 Configuration:")
    print(f"   Instance URL: {INSTANCE_URL}")
    print(f"   Consumer Key: {CONSUMER_KEY[:20]}...")
    print(f"   Consumer Secret: {CONSUMER_SECRET[:20]}...")
    print(f"\n📡 Requesting token from: {token_url}")
    
    try:
        response = requests.post(
            token_url,
            data=payload,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=30
        )
        
        print(f"\n📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS! Got access token")
            print(f"   Access Token: {data.get('access_token', 'N/A')[:50]}...")
            print(f"   Instance URL: {data.get('instance_url', 'N/A')}")
            print(f"   Token Type: {data.get('token_type', 'N/A')}")
            print(f"   Issued At: {data.get('issued_at', 'N/A')}")
            return data.get('access_token')
        else:
            print("❌ FAILED! Authentication error")
            print(f"   Status: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError as e:
        print(f"❌ CONNECTION ERROR: Cannot reach {INSTANCE_URL}")
        print(f"   Error: {e}")
        return None
    except requests.exceptions.Timeout:
        print(f"❌ TIMEOUT ERROR: Request took too long")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ REQUEST ERROR: {e}")
        return None
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")
        return None

if __name__ == "__main__":
    print("\n🧪 Agentforce OAuth Test")
    print("Using credentials from: .env\n")
    
    token = test_oauth()
    
    if token:
        print("\n" + "=" * 60)
        print("🎉 OAuth Test PASSED")
        print("=" * 60)
        print("\n✅ Your Consumer Key and Secret are correct!")
        print("✅ OAuth authentication is working")
        print("\nNext step: Run test_session.py to test agent session creation")
        print("=" * 60)
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("💥 OAuth Test FAILED")
        print("=" * 60)
        print("\n📋 Troubleshooting:")
        print("1. Check your Consumer Key and Secret in .env")
        print("2. Verify Connected App is configured correctly")
        print("3. Check Connected App policies (IP restrictions, etc.)")
        print("4. Ensure Client Credentials Flow is enabled")
        print("=" * 60)
        sys.exit(1)
