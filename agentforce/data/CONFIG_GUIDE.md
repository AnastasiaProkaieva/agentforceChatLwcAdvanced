# Configuration Guide

This guide explains the configuration architecture and how to use it.

## 📋 Configuration Architecture

We use a **hybrid approach** following DevOps best practices:

```
┌─────────────────────────────────────────┐
│ .env (Secrets - NOT in version control) │
│  - API Keys                              │
│  - Passwords                             │
│  - Tokens                                │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ config.yaml (Base config - versioned)   │
│  - Model settings                        │
│  - Prompts                               │
│  - Categories                            │
│  - Quality thresholds                    │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ config/{ENV}.yaml (Environment specific)│
│  - dev: Fast model, small datasets      │
│  - staging: Testing configuration        │
│  - prod: Best quality, full datasets    │
└─────────────────────────────────────────┘
```

## 🔑 Why This Approach?

### YAML for Application Config ✅
- **Version controlled** - track changes over time
- **Structured** - supports complex nested data
- **Multi-line text** - perfect for prompts
- **Environment-specific** - different configs per environment
- **Readable** - easy for humans to read and edit

### .env for Secrets ✅
- **NOT version controlled** - keeps secrets safe
- **Simple key-value** - perfect for API keys
- **Standard practice** - works with all deployment tools
- **Environment-specific** - each env has its own .env

## 📁 File Structure

```
agentforce/data/
├── .env                    # Secrets (in .gitignore)
├── .env.example            # Template (in git)
├── config.yaml             # Base configuration
├── config/
│   ├── config.dev.yaml    # Development overrides
│   ├── config.staging.yaml # Staging overrides
│   └── config.prod.yaml   # Production overrides
└── utils/
    └── config_loader.py   # Configuration loader
```

## 🚀 Quick Start

### 1. Set Up Secrets

```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 2. Choose Environment

In `.env`:
```bash
ENV=dev  # or staging, or prod
```

### 3. Use in Code

```python
from utils.config_loader import load_config

# Load configuration
config = load_config()  # Uses ENV from .env

# Get values
model_name = config.get('model.name')
api_key = config.get('secrets.gemini_api_key')

# Get formatted prompts
prompt = config.get_prompt('generate_faqs', count=10, category='Banking')
```

## 📝 Configuration Files

### config.yaml (Base Config)

This is your main configuration file (version controlled):

```yaml
# Model settings
model:
  name: "gemini-1.5-pro"
  temperature: 0.7
  max_tokens: 8192

# Prompts (multi-line)
prompts:
  generate_faqs: |
    Generate {count} FAQs for {category}...
    
# Categories
categories:
  "Account Management": 15
  "Investment Products": 20

# Quality thresholds
quality:
  min_answer_length: 100
  max_answer_length: 2000
```

### config/config.dev.yaml (Development)

Overrides for local development:

```yaml
model:
  name: "gemini-1.5-flash"  # Faster model

categories:
  "Account Management": 5  # Fewer FAQs for testing
```

### config/config.prod.yaml (Production)

Overrides for production:

```yaml
model:
  name: "gemini-1.5-pro"  # Best quality

generation:
  retry_attempts: 5  # More retries

quality:
  min_answer_length: 150  # Stricter requirements
```

## 🎯 Common Use Cases

### Change Model

Edit `config.yaml`:
```yaml
model:
  name: "gemini-1.5-flash"  # or gemini-1.5-pro
```

### Update Prompts

Edit `config.yaml`:
```yaml
prompts:
  generate_faqs: |
    Your new prompt here...
    Can use {variables}
```

### Add New Category

Edit `config.yaml`:
```yaml
categories:
  "New Category": 20
```

### Environment-Specific Settings

Create `config/config.{env}.yaml`:
```yaml
# Only override what's different
model:
  temperature: 0.9
```

### Use Different Environment

```bash
# In terminal
export ENV=prod
python3 generators/generate_faqs.py

# Or pass as argument
python3 generators/generate_faqs.py --env prod
```

## 🔧 Configuration Loader API

```python
from utils.config_loader import load_config

config = load_config(env='dev')

# Get nested values with dot notation
value = config.get('model.name')
value = config.get('quality.min_answer_length', default=100)

# Get model configuration
model_config = config.get_model_config()
# Returns: {'name': 'gemini-1.5-pro', 'temperature': 0.7, ...}

# Get formatted prompt
prompt = config.get_prompt('generate_faqs', count=10, category='Banking')

# Get categories
categories = config.get_categories()
# Returns: {'Account Management': 15, ...}

# Get settings
gen_settings = config.get_generation_settings()
quality_settings = config.get_quality_thresholds()
export_settings = config.get_export_settings()
```

## 🌍 Environments

### Development (dev)
- **Purpose**: Local testing
- **Model**: Fast (gemini-1.5-flash)
- **Datasets**: Small (5-10 FAQs per category)
- **Quality**: Lenient thresholds

### Staging (staging)
- **Purpose**: Pre-production testing
- **Model**: Medium quality
- **Datasets**: Medium size
- **Quality**: Production-like thresholds

### Production (prod)
- **Purpose**: Production deployment
- **Model**: Best quality (gemini-1.5-pro)
- **Datasets**: Full size (300+ FAQs)
- **Quality**: Strict thresholds

## 🔒 Security Best Practices

### ✅ DO:
- Keep secrets in `.env` (never commit)
- Use YAML for application config (commit)
- Have different `.env` files per environment
- Use environment variables in CI/CD
- Rotate API keys regularly

### ❌ DON'T:
- Put API keys in YAML files
- Commit `.env` to version control
- Hardcode secrets in code
- Share `.env` files
- Use production secrets in dev

## 📊 Configuration Priority

Settings are merged in this order (later overrides earlier):

1. **Base config** (config.yaml)
2. **Environment config** (config/{ENV}.yaml)
3. **Environment variables** (secrets from .env)

Example:
```yaml
# config.yaml
model:
  name: "gemini-1.5-pro"
  temperature: 0.7

# config/config.dev.yaml  
model:
  name: "gemini-1.5-flash"  # Overrides base

# Final result in dev:
# model:
#   name: "gemini-1.5-flash"  # From dev config
#   temperature: 0.7          # From base config
```

## 🧪 Testing Configuration

Test your configuration:

```bash
python3 utils/config_loader.py
```

Output:
```
📝 Development Environment:
   Model: gemini-1.5-flash
   Batch Size: 5
   Categories: 4

🚀 Production Environment:
   Model: gemini-1.5-pro
   Batch Size: 10
   Categories: 20

✅ Configuration loaded successfully!
```

## 🛠️ Troubleshooting

### "GEMINI_API_KEY not found"
- Check `.env` file exists in `agentforce/data/`
- Verify key is set: `GEMINI_API_KEY=abc123...`
- No quotes needed around the value

### "Prompt not found"
- Check prompt name matches exactly
- Verify prompt exists in `config.yaml`
- Check YAML indentation

### "Config file not found"
- Verify file exists: `config/config.{env}.yaml`
- Check ENV variable in `.env`
- Default is 'dev' if not set

### Changes Not Applied
- Restart your script after editing config
- Check you're using correct environment
- Verify YAML syntax is valid

## 📚 Examples

### Example 1: Quick Test with Dev Config

```bash
ENV=dev python3 generators/quick_generator.py --count 5
```

### Example 2: Production Generation

```bash
ENV=prod python3 generators/generate_faqs.py
```

### Example 3: Custom Environment

Create `config/config.custom.yaml`:
```yaml
model:
  name: "gemini-1.5-flash"
  temperature: 0.9

categories:
  "Test Category": 3
```

Use it:
```bash
ENV=custom python3 generators/generate_faqs.py
```

### Example 4: Override in Code

```python
from utils.config_loader import load_config

# Load specific environment
config = load_config(env='prod')

# Use configuration
model_name = config.get('model.name')
print(f"Using model: {model_name}")
```

## 🎓 Best Practices

1. **Keep secrets separate** - Never mix secrets with app config
2. **Version control YAML** - Track prompt and config changes
3. **Use environments** - Different settings for dev/staging/prod
4. **Document changes** - Add comments in YAML files
5. **Test locally** - Use dev config before prod
6. **Review prompts** - Version control helps track prompt evolution
7. **Validate config** - Run test script after changes

## 🔗 Related Documentation

- **Setup Guide**: `SETUP.md` - Initial setup
- **Main README**: `README.md` - Full documentation
- **Quick Reference**: `QUICK_REFERENCE.md` - Command cheat sheet

---

**Questions?** Open an issue or check the main documentation!
