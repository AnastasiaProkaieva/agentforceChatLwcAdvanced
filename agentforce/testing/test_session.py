#!/usr/bin/env python3
"""
Test Agentforce Session Creation
Tests if you can create a session with your agent
"""

import os
import sys
from pathlib import Path
import requests
import uuid
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Get configuration from .env
INSTANCE_URL = os.getenv('INSTANCE_URL', '').strip().strip('"')
CONSUMER_KEY = os.getenv('CONSUMER_KEY', '').strip().strip('"')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET', '').strip().strip('"')
AGENT_ID = os.getenv('AGENT_ID', '').strip().strip('"')

def get_access_token():
    """Get OAuth access token"""
    token_url = f"{INSTANCE_URL}/services/oauth2/token"
    
    payload = {
        'grant_type': 'client_credentials',
        'client_id': CONSUMER_KEY,
        'client_secret': CONSUMER_SECRET
    }
    
    try:
        response = requests.post(token_url, data=payload, timeout=30)
        if response.status_code == 200:
            return response.json().get('access_token')
        return None
    except:
        return None

def test_session_creation():
    """Test creating an agent session"""
    print("=" * 60)
    print("🤖 Testing Agent Session Creation")
    print("=" * 60)
    
    # Validate configuration
    if not AGENT_ID:
        print("❌ ERROR: AGENT_ID not found in .env")
        return False
    
    # Step 1: Get access token
    print("\n1️⃣ Getting access token...")
    access_token = get_access_token()
    
    if not access_token:
        print("❌ Failed to get access token")
        print("   Run test_oauth.py first to verify authentication")
        return False
    
    print("✅ Got access token")
    print(f"   Token: {access_token[:50]}...")
    
    # Step 2: Create session
    print("\n2️⃣ Creating agent session...")
    print(f"   Agent ID: {AGENT_ID}")
    print(f"   Instance: {INSTANCE_URL}")
    
    session_url = f"https://api.salesforce.com/einstein/ai-agent/v1/agents/{AGENT_ID}/sessions"
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    
    # Try without bypassUser first (agent may require user context)
    payload = {
        'externalSessionKey': str(uuid.uuid4()),
        'instanceConfig': {
            'endpoint': INSTANCE_URL
        },
        'streamingCapabilities': {
            'chunkTypes': ['Text']
        }
    }
    
    print(f"   API Endpoint: {session_url}")
    
    try:
        response = requests.post(
            session_url,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"\n📊 Response:")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code in [200, 201]:
            data = response.json()
            session_id = data.get('sessionId')
            print(f"\n✅ SUCCESS! Session created")
            print(f"   Session ID: {session_id}")
            return session_id
        else:
            print(f"\n❌ FAILED! Could not create session")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:500]}")
            
            # Parse error for helpful message
            try:
                error_data = response.json()
                if 'message' in error_data:
                    print(f"\n   Error Message: {error_data['message']}")
            except:
                pass
            
            return None
            
    except requests.exceptions.ConnectionError as e:
        print(f"❌ CONNECTION ERROR: Cannot reach api.salesforce.com")
        print(f"   This might be a Remote Site Settings issue in Salesforce")
        return None
    except requests.exceptions.Timeout:
        print(f"❌ TIMEOUT ERROR: Request took too long")
        return None
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None

if __name__ == "__main__":
    print("\n🧪 Agentforce Session Creation Test")
    print("Using credentials from: .env\n")
    
    session_id = test_session_creation()
    
    if session_id:
        print("\n" + "=" * 60)
        print("🎉 Agent Session Test PASSED")
        print("=" * 60)
        print("\n✅ Your agent is configured correctly!")
        print("✅ Session creation is working")
        print(f"✅ Session ID: {session_id}")
        print("\nNext step: Run test_full_flow.py to test sending messages")
        print("=" * 60)
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("💥 Agent Session Test FAILED")
        print("=" * 60)
        print("\n📋 Common Issues:")
        print("1. Agent not activated in Salesforce")
        print("2. Agent not linked to Connected App (Connections tab)")
        print("3. Wrong Agent ID")
        print("4. Missing Remote Site Settings in Salesforce:")
        print("   - Setup → Remote Site Settings")
        print("   - Add: https://api.salesforce.com")
        print("5. Missing API connection in agent")
        print("=" * 60)
        sys.exit(1)
