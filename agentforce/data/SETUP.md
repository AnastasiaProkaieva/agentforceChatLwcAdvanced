# Setup Guide: FAQ Data Generation

Follow these steps to get started with generating synthetic banking FAQs.

## ⚡ Quick Setup (5 minutes)

### Step 1: Install Python Dependencies

```bash
cd agentforce/data
pip install -r requirements.txt
```

If you don't have pip, install it first:
```bash
# macOS/Linux
python3 -m ensurepip --upgrade

# Windows
py -m ensurepip --upgrade
```

### Step 2: Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### Step 3: Create `.env` File

```bash
# Copy the example file
cp .env.example .env

# Open .env in your editor
nano .env
# or
code .env
# or
open -a TextEdit .env
```

Add your API key:
```bash
GEMINI_API_KEY=your_actual_api_key_here
```

Save and close the file.

### Step 4: Test the Setup

Generate a small test dataset:

```bash
python3 generators/quick_generator.py --count 10
```

If successful, you'll see:
```
✅ Generated 10 FAQs
💾 Saved to: output/banking_faqs_quick.json
```

## 🎯 What's Next?

### Generate Full Dataset

From project root:
```bash
npm run data:generate
```

Or directly:
```bash
python3 agentforce/data/generators/generate_faqs.py
```

### Validate Generated Data

```bash
npm run data:validate
```

### Import to Salesforce (Optional)

First, add Salesforce credentials to `.env`:
```bash
SF_USERNAME=your_username@company.com
SF_PASSWORD=your_password
SF_SECURITY_TOKEN=your_security_token
SF_INSTANCE_URL=https://yourinstance.salesforce.com
```

Then import:
```bash
npm run data:import
```

## 🔧 Troubleshooting

### "Module not found" Error

```bash
pip install google-generativeai python-dotenv --upgrade
```

### "GEMINI_API_KEY not found" Error

Make sure:
1. You created the `.env` file (not `.env.example`)
2. The `.env` file is in `agentforce/data/` directory
3. The API key has no spaces or quotes around it

### Rate Limit Errors

Use the batch generator with delays:
```bash
python3 generators/batch_generator.py
```

Or adjust settings in `.env`:
```bash
DEFAULT_BATCH_SIZE=5
RATE_LIMIT_DELAY=3
```

### Salesforce Connection Issues

Check:
1. Credentials are correct in `.env`
2. Security token is appended to password if required
3. IP restrictions allow API access
4. User has API enabled permission

## 📚 Additional Resources

- **Full Documentation**: See `README.md` in this directory
- **Agentforce Guide**: See `../docs/GUIDE.md`
- **Project README**: See `../../README.md`

## ✅ Verification Checklist

Before generating production data:

- [ ] Python 3.8+ installed (`python3 --version`)
- [ ] Dependencies installed (`pip list | grep google-generativeai`)
- [ ] `.env` file created with valid API key
- [ ] Test generation successful (quick_generator with --count 5)
- [ ] Output directory exists and is writable
- [ ] (Optional) Salesforce credentials configured
- [ ] (Optional) Custom object FAQ__c exists in Salesforce

## 🎉 You're Ready!

Run the full generator:
```bash
npm run data:generate
```

This will create 300+ high-quality FAQs for your Agentforce agent!

---

Need help? Check the troubleshooting section or open an issue on GitHub.
