# Quick Reference: FAQ Data Generation

One-page reference for common operations.

## 🚀 Setup (First Time Only)

```bash
cd agentforce/data
pip install -r requirements.txt
cp .env.example .env
# Add your GEMINI_API_KEY to .env
```

## 📝 Common Commands

### Generate Data

```bash
# From project root
npm run data:generate              # Full generation (300+ FAQs)
npm run data:generate:quick        # Quick test (50 FAQs)

# From agentforce/data/
python3 generators/generate_faqs.py
python3 generators/quick_generator.py --count 20
python3 generators/batch_generator.py
```

### Validate Data

```bash
npm run data:validate
# or
python3 validators/validate_data.py output/banking_faqs.json
```

### Import to Salesforce

```bash
npm run data:import
# or
python3 importers/salesforce_import.py output/banking_faqs.json --method bulk
```

## 📊 Output Files

All files are created in `agentforce/data/output/`:

| File | Description | Use Case |
|------|-------------|----------|
| `banking_faqs.csv` | CSV format | Salesforce Data Loader |
| `banking_faqs.json` | Structured JSON | Data analysis, backup |
| `banking_faqs_vectorsearch.jsonl` | JSONL format | Vector Search import |
| `generation_report.json` | Statistics | Quality metrics |

## 🎯 FAQ Structure

```json
{
  "question": "How do I...?",
  "answer": "Detailed answer here (200-400 words)",
  "keywords": ["keyword1", "keyword2"],
  "difficulty": "basic|intermediate|advanced",
  "segment": "retail|business|wealth_management",
  "category": "Main Category",
  "subcategory": "Specific Subcategory"
}
```

## 🔑 Environment Variables

### Required
```bash
GEMINI_API_KEY=your_key_here
```

### Optional (for Salesforce import)
```bash
SF_USERNAME=username@company.com
SF_PASSWORD=password
SF_SECURITY_TOKEN=token
SF_INSTANCE_URL=https://instance.salesforce.com
```

### Optional (rate limiting)
```bash
DEFAULT_BATCH_SIZE=10
RATE_LIMIT_DELAY=2
```

## 📚 Categories (300+ Total FAQs)

- Account Management (15)
- Credit Cards (15)
- Loans and Mortgages (20)
- Investment Products (20)
- Retirement Planning (20)
- Wealth Management (25)
- Online Banking Security (15)
- Wire Transfers (15)
- Foreign Exchange (12)
- Tax Planning (18)
- Estate Planning (15)
- Insurance Products (12)
- Small Business Banking (15)
- Corporate Banking (12)
- Regulatory Compliance (10)
- Financial Planning (18)
- Portfolio Management (15)
- Trust Services (10)
- Private Banking (12)
- Asset Protection (10)

## 🛠️ Customization

### Generate Custom Category

```python
from generators.generate_faqs import BankingFAQGenerator

gen = BankingFAQGenerator()
faqs = gen.generate_category_faqs("Crypto Banking", count=25)
gen.export_to_json(faqs, "crypto_faqs.json")
```

### Modify Existing Categories

Edit `generators/generate_faqs.py`:
```python
CATEGORIES = {
    "Your Category": 30,  # Number of FAQs
}
```

## 🔍 Validation Thresholds

Default quality requirements:

- Question: 10-500 characters
- Answer: 100-2000 characters
- Keywords: 1-10 per FAQ
- Must end with "?"

Adjust in `validators/validate_data.py`

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| `GEMINI_API_KEY not found` | Check `.env` file exists in `agentforce/data/` |
| Rate limit error | Use `batch_generator.py` with delays |
| JSON parse error | Try `quick_generator.py` instead |
| Salesforce import fails | Verify credentials and object exists |
| Module not found | Run `pip install -r requirements.txt` |

## 📞 Get Help

- Setup Guide: `SETUP.md`
- Full Documentation: `README.md`
- Agent Docs: `../docs/GUIDE.md`
- Project README: `../../README.md`

## ⚡ Quick Test

```bash
# Test everything works
python3 generators/quick_generator.py --count 5
python3 validators/validate_data.py output/banking_faqs_quick.json
```

Expected output:
```
✅ Generated 5 FAQs
✅ PASSED: All FAQs are valid
```

---

**Ready to generate? Run:** `npm run data:generate`
