# Agentforce Agent Management

This directory contains everything needed to programmatically manage your Agentforce agents.

## 📁 Directory Structure

```
agentforce/
├── agent-spec.yaml          # Agent configuration
├── requirements.txt         # Python dependencies  
├── README.md               # This file
├── scripts/                # Agent management scripts
│   ├── deploy.sh          # Deployment script
│   └── manage.py          # Python management tool
├── data/                   # FAQ data generation (NEW!)
│   ├── generators/        # FAQ generators
│   ├── validators/        # Data validation
│   ├── importers/         # Salesforce import
│   ├── templates/         # Sample data
│   ├── output/            # Generated files
│   ├── README.md          # Data generation guide
│   └── SETUP.md           # Quick setup guide
└── docs/                   # Documentation
    ├── GUIDE.md           # Comprehensive guide
    └── QUICK_START.md     # Quick start guide
```

## 🚀 Quick Start

### 1. Install Prerequisites

```bash
# Install Salesforce CLI plugin
sf plugins install @salesforce/plugin-agent

# Install Python dependencies (optional, for Python script)
pip install -r agentforce/requirements.txt
```

### 2. Configure Your Agent

Edit `agent-spec.yaml` to customize your agent's behavior, topics, and instructions.

### 3. Deploy

```bash
# Using npm script (from project root)
npm run agent:create

# Or using bash script directly
./agentforce/scripts/deploy.sh [org-alias]

# Or using Python
python3 agentforce/scripts/manage.py create --org [org-alias]
```

## 📝 Common Commands

### Deploy Agent
```bash
npm run agent:create
# or
./agentforce/scripts/deploy.sh
```

### List Agents
```bash
npm run agent:list
# or
python3 agentforce/scripts/manage.py list
```

### Test Agent
```bash
python3 agentforce/scripts/manage.py test --agent-id <ID> --message "Hello"
```

### Activate Agent
```bash
python3 agentforce/scripts/manage.py activate --agent-id <ID>
```

## 🎯 Synthetic Data Generation

Need training data for your agent? Generate high-quality banking FAQs:

```bash
# From project root
npm run data:generate

# Or directly
cd data
python3 generators/generate_faqs.py
```

See `data/SETUP.md` for complete setup instructions.

**Features**:
- Generates 300+ realistic FAQs
- 20+ banking categories
- Optimized for Vector Search
- Multiple export formats
- Quality validation included

## 🔧 Configuration

### agent-spec.yaml

This is your agent's configuration file. Edit it to:

- Change agent name and description
- Add/modify topics
- Update instructions
- Configure model settings
- Set security options

Example:
```yaml
agent:
  name: "My Custom Agent"
  description: "Agent for customer support"
  
topics:
  - name: "Product Help"
    instructions: |
      Help customers with product questions.
      Be friendly and professional.
```

## 📚 Documentation

- **Quick Start**: See `docs/QUICK_START.md` for a 3-step guide
- **Full Guide**: See `docs/GUIDE.md` for comprehensive documentation
- **Project README**: See `../README.md` for overall project documentation

## 🔄 Workflow

1. Edit `agent-spec.yaml`
2. Run `npm run agent:create`
3. Copy the Agent ID from output
4. Update your LWC component config
5. Test on your site

## 💡 Tips

- **Version Control**: Commit `agent-spec.yaml` to track changes
- **Multiple Environments**: Create separate spec files for dev/staging/prod
- **Testing**: Always test in a sandbox before deploying to production
- **Automation**: Use the provided scripts in CI/CD pipelines

## 🆘 Troubleshooting

### Plugin not installed?
```bash
sf plugins install @salesforce/plugin-agent --force
```

### Authentication issues?
```bash
sf org login web --alias my-org --set-default
```

### Spec file errors?
```bash
# Validate YAML syntax
python3 -c "import yaml; yaml.safe_load(open('agentforce/agent-spec.yaml'))"
```

## 🔗 Resources

- [Salesforce CLI Plugin](https://github.com/salesforcecli/plugin-agent)
- [Agentforce Documentation](https://developer.salesforce.com/docs/agentforce)
- [Python SDK Blog Post](https://developer.salesforce.com/blogs/2025/09/build-and-manage-agents-with-agentforce-python-sdk)

---

**Need help?** Check the docs or open an issue on GitHub.
