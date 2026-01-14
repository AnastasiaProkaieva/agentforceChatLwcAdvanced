# 🚀 Quick Start: Programmatic Agent Management

Stop making manual changes! Here's how to manage your Agentforce agents with code.

## ⚡ 3-Step Quick Start

### 1️⃣ Install the CLI Plugin

```bash
sf plugins install @salesforce/plugin-agent
```

### 2️⃣ Edit Your Agent Configuration

Open `config/agent-spec.yaml` and modify it:

```yaml
agent:
  name: "My Awesome Agent"
  
topics:
  - name: "Customer Support"
    instructions: |
      Help customers with their questions.
      Be friendly and professional.
```

### 3️⃣ Deploy Your Agent

```bash
npm run agent:create
```

That's it! Your agent is now deployed. 🎉

---

## 📋 Common Commands

```bash
# Create/update agent
npm run agent:create

# List all agents
npm run agent:list

# Deploy everything (LWC + Agent)
npm run agent:deploy

# Use the bash script directly
./scripts/deploy-agent.sh your-org-alias

# Use Python for advanced operations
python3 scripts/manage-agent.py create --org your-org
```

---

## 🔄 Typical Workflow

1. **Make changes** to `config/agent-spec.yaml`
2. **Run** `npm run agent:create`
3. **Copy** the Agent ID from the output
4. **Update** your LWC component config in Experience Builder
5. **Test** on your site

---

## 📁 What Changed in Your Project?

We added these files:

```
📦 Your Project
├── config/
│   └── agent-spec.yaml          # ← Agent configuration
├── scripts/
│   ├── deploy-agent.sh          # ← Bash deployment script
│   └── manage-agent.py          # ← Python management tool
├── .github/workflows/
│   └── deploy-agent.yml         # ← CI/CD workflow
├── requirements.txt             # ← Python dependencies
├── AGENT_MANAGEMENT_GUIDE.md    # ← Full documentation
└── QUICK_START_AGENT_MANAGEMENT.md  # ← This file
```

---

## 💡 Pro Tips

### Version Control Everything
```bash
git add config/agent-spec.yaml
git commit -m "Update agent instructions"
git push
```

### Multiple Environments
```bash
# Create environment-specific configs
cp config/agent-spec.yaml config/agent-spec-dev.yaml
cp config/agent-spec.yaml config/agent-spec-prod.yaml

# Deploy to specific env
sf agent create --spec config/agent-spec-prod.yaml --target-org prod
```

### Test Changes Locally First
```bash
# Test in sandbox
sf agent create --spec config/agent-spec.yaml --target-org sandbox

# Get the agent ID
sf agent list --target-org sandbox

# Test it
sf agent test --agent-id <ID> --message "Hello" --target-org sandbox
```

---

## 🐛 Troubleshooting

### "Agent not found" error?
```bash
# List your agents
sf agent list
```

### Plugin not installed?
```bash
sf plugins install @salesforce/plugin-agent --force
```

### Authentication issues?
```bash
sf org login web --alias my-org --set-default
```

---

## 🎯 What You Can Do Now

- ✅ Create agents from code
- ✅ Update agents without clicking through the UI
- ✅ Version control your agent configurations
- ✅ Deploy agents across multiple orgs easily
- ✅ Automate agent deployment in CI/CD
- ✅ Test agent changes programmatically

---

## 📚 Learn More

- **Full Guide**: See `AGENT_MANAGEMENT_GUIDE.md` for detailed documentation
- **CLI Plugin**: https://github.com/salesforcecli/plugin-agent
- **Python SDK**: https://developer.salesforce.com/blogs/2025/09/build-and-manage-agents-with-agentforce-python-sdk

---

## 🆘 Need Help?

1. Check `AGENT_MANAGEMENT_GUIDE.md` for detailed instructions
2. Open an issue on GitHub
3. Join the Salesforce Developer community

**Happy Coding! 🎉**
