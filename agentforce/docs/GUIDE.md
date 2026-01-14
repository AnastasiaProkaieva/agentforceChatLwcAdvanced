# Agentforce Agent Management Guide

This guide explains how to programmatically create and update Agentforce agents instead of doing it manually through the Salesforce UI.

## 🎯 Why Use Programmatic Agent Management?

- **Version Control**: Track agent configurations in Git
- **Automation**: Deploy agents as part of CI/CD pipelines
- **Consistency**: Ensure all environments use the same agent configuration
- **Speed**: Update multiple agents across orgs quickly
- **Documentation**: Agent specs serve as documentation

## 🛠️ Available Tools

### 1. Salesforce CLI Plugin (Easiest to Get Started)

The official Salesforce CLI plugin provides commands to manage agents.

**Installation:**
```bash
sf plugins install @salesforce/plugin-agent
```

**Common Commands:**
```bash
# Create/update an agent from a spec file
sf agent create --name "My Agent" --spec config/agent-spec.yaml --target-org my-org

# List all agents
sf agent list --target-org my-org

# Activate an agent
sf agent activate --agent-id <ID> --target-org my-org

# Test an agent
sf agent test --agent-id <ID> --message "Hello" --target-org my-org
```

### 2. NPM Scripts (Convenient Shortcuts)

We've added npm scripts for common operations:

```bash
# Create/update agent
npm run agent:create

# List all agents in default org
npm run agent:list

# Deploy LWC and create agent in one command
npm run agent:deploy
```

### 3. Bash Script (Automated Deployment)

The `scripts/deploy-agent.sh` script automates agent deployment:

```bash
# Make it executable (first time only)
chmod +x scripts/deploy-agent.sh

# Deploy to default org
./scripts/deploy-agent.sh

# Deploy to specific org
./scripts/deploy-agent.sh my-org-alias
```

### 4. Python Script (Advanced Automation)

For complex workflows, use the Python script:

```bash
# Create agent
python3 scripts/manage-agent.py create --org my-org

# List agents
python3 scripts/manage-agent.py list --org my-org

# Activate an agent
python3 scripts/manage-agent.py activate --agent-id <ID> --org my-org

# Update agent spec programmatically
python3 scripts/manage-agent.py update --updates '{"agent":{"name":"New Name"}}'
```

**Requirements:**
```bash
pip install pyyaml
```

## 📝 Agent Specification File

The agent configuration is defined in `config/agent-spec.yaml`:

```yaml
agent:
  name: "Agentforce Chat Agent"
  description: "AI agent for customer support"
  
topics:
  - name: "General Support"
    instructions: |
      Your instructions here...
    actions:
      - name: "HTML_Stylize"
        type: "prompt"
        required: true

global_instructions: |
  You are a helpful AI assistant...

model:
  name: "gpt-4"
  temperature: 0.7
  max_tokens: 2000
```

## 🔄 Typical Workflow

### 1. Modify Agent Configuration

Edit `config/agent-spec.yaml` to change your agent's behavior:

```yaml
topics:
  - name: "Product Questions"
    instructions: |
      Answer questions about our products.
      Always be helpful and accurate.
```

### 2. Deploy the Agent

```bash
npm run agent:create
```

### 3. Get the Agent ID

The command will output the Agent ID. Copy it.

### 4. Update Your LWC Configuration

Update the `agentId` property in your Experience Builder component settings.

### 5. Test

Visit your Experience Cloud site and test the updated agent.

## 🚀 Advanced Use Cases

### CI/CD Pipeline Integration

Add to your `.github/workflows/deploy.yml`:

```yaml
- name: Deploy Agent
  run: |
    sf plugins install @salesforce/plugin-agent
    sf agent create --name "My Agent" --spec config/agent-spec.yaml --target-org prod
```

### Multi-Environment Management

Create separate spec files for each environment:

```
config/
  agent-spec-dev.yaml
  agent-spec-staging.yaml
  agent-spec-prod.yaml
```

Deploy with:
```bash
sf agent create --spec config/agent-spec-prod.yaml --target-org prod
```

### Automated Testing

Test agent responses programmatically:

```bash
sf agent test \
  --agent-id <ID> \
  --message "What is your return policy?" \
  --target-org my-org
```

### Bulk Updates

Update multiple agents across orgs:

```bash
#!/bin/bash
ORGS=("dev" "staging" "prod")

for org in "${ORGS[@]}"; do
  echo "Deploying to $org..."
  sf agent create --spec config/agent-spec.yaml --target-org "$org"
done
```

## 🐍 Python SDK (Coming Soon)

Salesforce is developing an official Python SDK for more advanced agent management:

```python
from agentforce import Agent, Topic, Action

# Define agent programmatically
agent = Agent(
    name="Customer Support Agent",
    topics=[
        Topic(
            name="Product Questions",
            instructions="Answer product questions",
            actions=[Action(name="HTML_Stylize")]
        )
    ]
)

# Deploy
agent.deploy(org_alias="prod")

# Update
agent.update_topic("Product Questions", instructions="New instructions")
```

**Resources:**
- [Agentforce Python SDK Blog Post](https://developer.salesforce.com/blogs/2025/09/build-and-manage-agents-with-agentforce-python-sdk)

## 📊 Metadata API Approach

You can also manage agents as Salesforce metadata:

1. Retrieve agent metadata:
```bash
sf project retrieve start --metadata Bot:My_Agent
```

2. Edit the XML files in `force-app/main/default/bots/`

3. Deploy:
```bash
sf project deploy start --source-path force-app/main/default/bots
```

## 🔍 Troubleshooting

### Plugin Not Found
```bash
# Reinstall the plugin
sf plugins install @salesforce/plugin-agent --force
```

### Authentication Errors
```bash
# Reconnect to your org
sf org login web --alias my-org --set-default
```

### Spec File Validation Errors

Make sure your YAML is properly formatted:
```bash
# Validate YAML syntax
python3 -c "import yaml; yaml.safe_load(open('config/agent-spec.yaml'))"
```

### Agent Not Updating

Clear the agent cache:
```bash
sf agent delete --agent-id <OLD_ID> --target-org my-org
npm run agent:create
```

## 📚 Additional Resources

- [Salesforce CLI Plugin GitHub](https://github.com/salesforcecli/plugin-agent)
- [Agentforce Developer Guide](https://developer.salesforce.com/docs/agentforce)
- [Agent Script Documentation](https://www.salesforce.com/agentforce/script/)
- [Metadata API Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/)

## 💡 Best Practices

1. **Version Control**: Always commit your `agent-spec.yaml` to Git
2. **Environment-Specific Configs**: Use separate specs for dev/staging/prod
3. **Test First**: Test agent changes in a sandbox before deploying to production
4. **Document Changes**: Add comments to your spec file explaining configuration choices
5. **Automate**: Integrate agent deployment into your CI/CD pipeline
6. **Monitor**: Use Salesforce Event Monitoring to track agent performance

## 🤝 Contributing

If you have suggestions for improving agent management workflows, please:
1. Open an issue on GitHub
2. Submit a pull request with your changes
3. Share your automation scripts with the community

---

**Need Help?** Open an issue on GitHub or check the Salesforce Developer Forums.
