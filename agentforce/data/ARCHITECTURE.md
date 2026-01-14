# Configuration Architecture

Visual overview of the configuration system.

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User / Developer                         │
└────────────┬────────────────────────────────────────────────┘
             │
             ├─► Edit .env (secrets only)
             │   - GEMINI_API_KEY
             │   - SF_USERNAME, SF_PASSWORD
             │   - ENV=dev|staging|prod
             │
             ├─► Edit config.yaml (application config)
             │   - Model settings
             │   - Prompts
             │   - Categories
             │   - Quality thresholds
             │
             └─► Edit config/{env}.yaml (environment overrides)
                 - Different settings per environment
                 
┌─────────────────────────────────────────────────────────────┐
│                   Configuration Loader                       │
│  (utils/config_loader.py)                                   │
│                                                               │
│  1. Load .env → Extract secrets                             │
│  2. Load config.yaml → Base config                          │
│  3. Load config/{ENV}.yaml → Merge overrides               │
│  4. Provide unified API                                      │
└────────────┬────────────────────────────────────────────────┘
             │
             ├─► generators/generate_faqs.py
             │   - Uses config.get('model.name')
             │   - Uses config.get_prompt('generate_faqs')
             │   - Uses config.get_categories()
             │
             ├─► generators/quick_generator.py
             │   - Uses config.get_model_config()
             │   - Uses config.get_prompt('quick_generate')
             │
             └─► validators/validate_data.py
                 - Uses config.get_quality_thresholds()
```

## 📊 Configuration Flow

```
Developer Changes          File Changed              Who Sees It
─────────────────────────────────────────────────────────────────
Change model              config.yaml               Everyone (versioned)
Update prompt             config.yaml               Everyone (versioned)
Add category              config.yaml               Everyone (versioned)
Set API key               .env                      Only local (not versioned)
Dev-specific setting      config/config.dev.yaml    Everyone (versioned)
```

## 🔄 Configuration Merge Process

```
Step 1: Base Config (config.yaml)
─────────────────────────────────────
model:
  name: "gemini-1.5-pro"
  temperature: 0.7
  max_tokens: 8192

categories:
  "Account Management": 15
  "Investment Products": 20
  
         ↓ MERGE ↓

Step 2: Environment Override (config/config.dev.yaml)
──────────────────────────────────────────────────────
model:
  name: "gemini-1.5-flash"  # Override

categories:
  "Account Management": 5    # Override
  
         ↓ RESULT ↓

Step 3: Final Configuration
─────────────────────────────
model:
  name: "gemini-1.5-flash"   # From dev config
  temperature: 0.7            # From base config
  max_tokens: 8192            # From base config

categories:
  "Account Management": 5     # From dev config
  "Investment Products": 20   # From base config
```

## 🔐 Security Model

```
┌────────────────────────┐
│   Version Control      │
│   (Git Repository)     │
│                        │
│  ✅ config.yaml        │
│  ✅ config/*.yaml      │
│  ✅ Code               │
│  ❌ .env (gitignored)  │
└────────────────────────┘

┌────────────────────────┐
│   Local / Deployment   │
│   Environment          │
│                        │
│  ✅ .env file          │
│  ✅ Environment vars   │
│  ❌ Committed to git   │
└────────────────────────┘
```

## 🎯 Use Cases

### Use Case 1: Change Model Globally

```yaml
# Edit config.yaml
model:
  name: "gemini-1.5-flash"  # Change here

# All environments use this unless overridden
```

### Use Case 2: Dev Uses Fast Model, Prod Uses Best

```yaml
# config.yaml (base)
model:
  name: "gemini-1.5-pro"

# config/config.dev.yaml (override)
model:
  name: "gemini-1.5-flash"

# Result:
# - Dev: Uses gemini-1.5-flash
# - Prod: Uses gemini-1.5-pro
```

### Use Case 3: Update Prompt for Everyone

```yaml
# Edit config.yaml
prompts:
  generate_faqs: |
    New improved prompt...

# Commit to git
# Everyone gets the new prompt
```

### Use Case 4: Team Member Setup

```bash
# 1. Clone repo (gets config.yaml)
git clone repo

# 2. Create .env (secrets stay local)
cp .env.example .env
# Add API key

# 3. Ready to go!
python3 generators/generate_faqs.py
```

## 🔄 CI/CD Integration

```yaml
# GitHub Actions / GitLab CI
name: Generate FAQs

on: push

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      # Config files are in repo (automatic)
      
      # Secrets from CI/CD secrets
      - name: Create .env
        run: |
          echo "GEMINI_API_KEY=${{ secrets.GEMINI_API_KEY }}" > .env
          echo "ENV=prod" >> .env
      
      # Run generation
      - name: Generate
        run: python3 generators/generate_faqs.py --env prod
```

## 📈 Benefits

| Aspect | YAML Config | .env Secrets |
|--------|-------------|--------------|
| **Version Control** | ✅ Yes | ❌ No |
| **Team Sharing** | ✅ Yes | ❌ No (everyone has own) |
| **CI/CD** | ✅ Automatic | ✅ Via secrets |
| **Security** | ✅ Safe to share | ⚠️ Must protect |
| **Multi-line** | ✅ Perfect | ❌ Difficult |
| **Structure** | ✅ Nested data | ❌ Flat key-value |
| **Environment-specific** | ✅ config/{env}.yaml | ✅ Different .env |

## 🎓 Best Practices

1. **Secrets in .env** - API keys, passwords
2. **Config in YAML** - Everything else
3. **Version control YAML** - Track changes
4. **Never commit .env** - Keep secrets safe
5. **Use environments** - dev/staging/prod
6. **Document changes** - Comments in YAML
7. **Test locally first** - Use dev config

## 📚 Related Documentation

- **[CONFIG_GUIDE.md](CONFIG_GUIDE.md)** - Detailed configuration guide
- **[SETUP.md](SETUP.md)** - Initial setup instructions
- **[README.md](README.md)** - Main documentation

---

**Architecture Questions?** See CONFIG_GUIDE.md or open an issue!
