#!/usr/bin/env python3
"""
Complete Agentforce Flow Test
Tests authentication, session creation, and sending a message
"""

import os
import sys
from pathlib import Path
import requests
import uuid
import time
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Get configuration from .env
INSTANCE_URL = os.getenv('INSTANCE_URL', '').strip().strip('"')
CONSUMER_KEY = os.getenv('CONSUMER_KEY', '').strip().strip('"')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET', '').strip().strip('"')
AGENT_ID = os.getenv('AGENT_ID', '').strip().strip('"')

class AgentforceTester:
    def __init__(self):
        self.instance_url = INSTANCE_URL
        self.consumer_key = CONSUMER_KEY
        self.consumer_secret = CONSUMER_SECRET
        self.agent_id = AGENT_ID
        self.access_token = None
        self.session_id = None
        self.sequence_id = 1
    
    def print_step(self, step_name):
        """Print test step header"""
        print(f"\n{'='*60}")
        print(f"🧪 {step_name}")
        print(f"{'='*60}")
    
    def get_access_token(self):
        """Step 1: Get OAuth token"""
        self.print_step("Step 1: Get OAuth Access Token")
        
        token_url = f"{self.instance_url}/services/oauth2/token"
        
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.consumer_key,
            'client_secret': self.consumer_secret
        }
        
        print(f"   Endpoint: {token_url}")
        
        try:
            response = requests.post(token_url, data=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access_token')
                print(f"✅ SUCCESS")
                print(f"   Token: {self.access_token[:50]}...")
                return True
            else:
                print(f"❌ FAILED: {response.status_code}")
                print(f"   Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return False
    
    def create_session(self):
        """Step 2: Create agent session"""
        self.print_step("Step 2: Create Agent Session")
        
        if not self.access_token:
            print("❌ No access token")
            return False
        
        session_url = f"https://api.salesforce.com/einstein/ai-agent/v1/agents/{self.agent_id}/sessions"
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        
        # Try without bypassUser (agent may require user context)
        payload = {
            'externalSessionKey': str(uuid.uuid4()),
            'instanceConfig': {'endpoint': self.instance_url},
            'streamingCapabilities': {'chunkTypes': ['Text']}
        }
        
        print(f"   Endpoint: {session_url}")
        print(f"   Agent ID: {self.agent_id}")
        
        try:
            response = requests.post(session_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code in [200, 201]:
                data = response.json()
                self.session_id = data.get('sessionId')
                print(f"✅ SUCCESS")
                print(f"   Session ID: {self.session_id}")
                return True
            else:
                print(f"❌ FAILED: {response.status_code}")
                print(f"   Error: {response.text[:300]}")
                return False
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return False
    
    def send_message(self, message):
        """Step 3: Send message to agent"""
        self.print_step(f"Step 3: Send Message")
        
        if not self.session_id:
            print("❌ No session ID")
            return False
        
        print(f"   Message: \"{message}\"")
        
        message_url = f"https://api.salesforce.com/einstein/ai-agent/v1/sessions/{self.session_id}/messages"
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        
        payload = {
            'message': {
                'sequenceId': self.sequence_id,
                'type': 'Text',
                'text': message
            },
            'variables': []
        }
        
        print(f"   Endpoint: {message_url}")
        
        try:
            response = requests.post(message_url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                messages = data.get('messages', [])
                
                print(f"✅ SUCCESS")
                print(f"   Status: {response.status_code}")
                print(f"   Messages received: {len(messages)}")
                
                if messages:
                    print(f"\n   🤖 Agent Response:")
                    for i, msg in enumerate(messages, 1):
                        response_text = msg.get('message', 'No message')
                        # Truncate long responses
                        if len(response_text) > 200:
                            response_text = response_text[:200] + "..."
                        print(f"      [{i}] {response_text}")
                else:
                    print(f"   ⚠️  No messages in response")
                
                self.sequence_id += 1
                return True
            else:
                print(f"❌ FAILED: {response.status_code}")
                print(f"   Error: {response.text[:300]}")
                return False
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return False
    
    def run_full_test(self):
        """Run complete test flow"""
        print("\n" + "="*60)
        print("🚀 AGENTFORCE COMPLETE FLOW TEST")
        print("="*60)
        print(f"\n📋 Configuration:")
        print(f"   Instance: {self.instance_url}")
        print(f"   Agent ID: {self.agent_id}")
        print(f"   Consumer Key: {self.consumer_key[:20]}...")
        
        # Test 1: OAuth
        if not self.get_access_token():
            print("\n💥 Test stopped: OAuth authentication failed")
            return False
        
        time.sleep(1)
        
        # Test 2: Session
        if not self.create_session():
            print("\n💥 Test stopped: Session creation failed")
            return False
        
        time.sleep(1)
        
        # Test 3: Message
        if not self.send_message("Hello, what can you help me with?"):
            print("\n💥 Test stopped: Message sending failed")
            return False
        
        print("\n" + "="*60)
        print("🎉 ALL TESTS PASSED!")
        print("="*60)
        print("\n✅ OAuth authentication: WORKING")
        print("✅ Agent session creation: WORKING")
        print("✅ Message sending: WORKING")
        print("✅ Agent responses: WORKING")
        print("\n🎊 Your Agentforce setup is fully functional!")
        print("="*60)
        return True

if __name__ == "__main__":
    print("\n🧪 Agentforce Complete Flow Test")
    print("Using credentials from: .env\n")
    
    tester = AgentforceTester()
    success = tester.run_full_test()
    
    if not success:
        print("\n" + "="*60)
        print("📋 TROUBLESHOOTING CHECKLIST:")
        print("="*60)
        print("1. ☐ Remote Site Settings exist in Salesforce")
        print("      Setup → Remote Site Settings")
        print("      Add: https://api.salesforce.com")
        print("      Add: https://login.salesforce.com")
        print("")
        print("2. ☐ Consumer Key/Secret are correct")
        print("      Check .env file for typos")
        print("")
        print("3. ☐ Agent is ACTIVATED")
        print("      Setup → Agents → Your Agent → Status")
        print("")
        print("4. ☐ Agent linked to Connected App")
        print("      Setup → Agents → Your Agent → Connections tab")
        print("      Should have API connection")
        print("")
        print("5. ☐ Connected App has correct OAuth scopes")
        print("      - chatbot_api")
        print("      - sfap_api")
        print("      - api")
        print("      - refresh_token, offline_access")
        print("="*60)
        sys.exit(1)
    else:
        sys.exit(0)
