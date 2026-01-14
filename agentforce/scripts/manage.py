#!/usr/bin/env python3
"""
Agentforce Agent Management Script
Provides programmatic control over Agentforce agents
"""

import json
import subprocess
import sys
import yaml
from pathlib import Path

class AgentManager:
    """Manage Agentforce agents programmatically"""
    
    def __init__(self, org_alias=None):
        self.org_alias = org_alias or self._get_default_org()
        self.script_dir = Path(__file__).parent
        self.agentforce_dir = self.script_dir.parent
        self.project_root = self.agentforce_dir.parent
        self.agent_spec_path = self.agentforce_dir / "agent-spec.yaml"
    
    def _get_default_org(self):
        """Get the default target org from SF CLI"""
        try:
            result = subprocess.run(
                ["sf", "config", "get", "target-org", "--json"],
                capture_output=True,
                text=True,
                check=True
            )
            data = json.loads(result.stdout)
            return data.get("result", [{}])[0].get("value")
        except Exception as e:
            print(f"❌ Error getting default org: {e}")
            return None
    
    def load_agent_spec(self):
        """Load agent specification from YAML file"""
        try:
            with open(self.agent_spec_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"❌ Agent spec file not found: {self.agent_spec_path}")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"❌ Error parsing agent spec: {e}")
            sys.exit(1)
    
    def create_agent(self):
        """Create or update an agent using the CLI"""
        print("🤖 Creating/Updating Agentforce Agent...")
        
        if not self.org_alias:
            print("❌ No target org specified")
            sys.exit(1)
        
        spec = self.load_agent_spec()
        agent_name = spec.get("agent", {}).get("name", "Agentforce Chat Agent")
        api_name = agent_name.replace(" ", "_")
        
        try:
            result = subprocess.run(
                [
                    "sf", "agent", "create",
                    "--name", agent_name,
                    "--api-name", api_name,
                    "--spec", str(self.agent_spec_path),
                    "--target-org", self.org_alias
                ],
                capture_output=True,
                text=True,
                check=True
            )
            print("✅ Agent created successfully!")
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating agent: {e}")
            print(e.stderr if e.stderr else e.stdout)
            return False
    
    def list_agents(self):
        """List all agents in the org"""
        print("📋 Listing agents...")
        
        try:
            result = subprocess.run(
                ["sf", "agent", "list", "--target-org", self.org_alias, "--json"],
                capture_output=True,
                text=True,
                check=True
            )
            data = json.loads(result.stdout)
            agents = data.get("result", [])
            
            if not agents:
                print("No agents found in the org.")
                return []
            
            print(f"\n{'Name':<30} {'API Name':<30} {'ID':<20}")
            print("-" * 80)
            for agent in agents:
                print(f"{agent.get('label', 'N/A'):<30} {agent.get('apiName', 'N/A'):<30} {agent.get('id', 'N/A'):<20}")
            
            return agents
        except subprocess.CalledProcessError as e:
            print(f"❌ Error listing agents: {e}")
            return []
    
    def activate_agent(self, agent_id):
        """Activate an agent"""
        print(f"🚀 Activating agent {agent_id}...")
        
        try:
            result = subprocess.run(
                ["sf", "agent", "activate", "--agent-id", agent_id, "--target-org", self.org_alias],
                capture_output=True,
                text=True,
                check=True
            )
            print("✅ Agent activated successfully!")
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error activating agent: {e}")
            print(e.stderr if e.stderr else e.stdout)
            return False
    
    def update_agent_spec(self, updates):
        """Update the agent specification file"""
        spec = self.load_agent_spec()
        
        # Deep merge updates into spec
        def deep_merge(base, updates):
            for key, value in updates.items():
                if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                    deep_merge(base[key], value)
                else:
                    base[key] = value
        
        deep_merge(spec, updates)
        
        # Write back to file
        with open(self.agent_spec_path, 'w') as f:
            yaml.dump(spec, f, default_flow_style=False, sort_keys=False)
        
        print(f"✅ Agent spec updated: {self.agent_spec_path}")
        return spec
    
    def test_agent(self, agent_id, message):
        """Test an agent with a message"""
        print(f"🧪 Testing agent {agent_id}...")
        
        try:
            result = subprocess.run(
                [
                    "sf", "agent", "test",
                    "--agent-id", agent_id,
                    "--message", message,
                    "--target-org", self.org_alias,
                    "--json"
                ],
                capture_output=True,
                text=True,
                check=True
            )
            data = json.loads(result.stdout)
            response = data.get("result", {}).get("response", "No response")
            print(f"\n📨 Agent Response:\n{response}\n")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error testing agent: {e}")
            return False


def main():
    """Main CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage Agentforce agents programmatically")
    parser.add_argument("--org", help="Target org alias")
    parser.add_argument("command", choices=["create", "list", "activate", "update", "test"], 
                       help="Command to execute")
    parser.add_argument("--agent-id", help="Agent ID (for activate/test commands)")
    parser.add_argument("--message", help="Test message (for test command)")
    parser.add_argument("--updates", help="JSON string with updates (for update command)")
    
    args = parser.parse_args()
    
    manager = AgentManager(org_alias=args.org)
    
    if args.command == "create":
        manager.create_agent()
    elif args.command == "list":
        manager.list_agents()
    elif args.command == "activate":
        if not args.agent_id:
            print("❌ --agent-id is required for activate command")
            sys.exit(1)
        manager.activate_agent(args.agent_id)
    elif args.command == "test":
        if not args.agent_id or not args.message:
            print("❌ --agent-id and --message are required for test command")
            sys.exit(1)
        manager.test_agent(args.agent_id, args.message)
    elif args.command == "update":
        if not args.updates:
            print("❌ --updates is required for update command")
            sys.exit(1)
        try:
            updates = json.loads(args.updates)
            manager.update_agent_spec(updates)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
