# Agentforce FAQ Data Generation

This directory contains tools for generating synthetic FAQ data for banking and wealth management services, specifically optimized for Salesforce Vector Search.

## ⚙️ Configuration Architecture

We use a **hybrid DevOps best practice**:
- **YAML files** for prompts, model settings, and application config (version controlled)
- **.env files** for API keys and secrets (NOT version controlled)

```
.env (secrets) + config.yaml (settings) + config/{env}.yaml (environment) = Complete Config
```

**Why?** Prompts are application logic that should be versioned. Secrets should never be in git.

See **[CONFIG_GUIDE.md](CONFIG_GUIDE.md)** for complete configuration documentation.

## 📁 Directory Structure

```
agentforce/data/
├── config.yaml                 # Base configuration (versioned)
├── config/
│   ├── config.dev.yaml        # Development config
│   ├── config.staging.yaml    # Staging config (optional)
│   └── config.prod.yaml       # Production config
├── utils/
│   ├── config_loader.py       # Configuration loader
│   └── __init__.py
├── generators/                 # FAQ generation scripts
│   ├── generate_faqs.py       # Main generator (comprehensive)
│   ├── quick_generator.py     # Quick generator (fast, smaller datasets)
│   └── batch_generator.py     # Batch generator (rate-limited)
├── validators/                 # Data validation tools
│   └── validate_data.py       # Validate FAQ quality and format
├── importers/                  # Salesforce import tools
│   └── salesforce_import.py   # Import to Salesforce
├── templates/                  # Sample data templates
│   └── faq_template.json      # Example FAQ structure
├── output/                     # Generated data files (gitignored)
├── .env                        # Secrets (NOT in git)
├── .env.example               # Template for .env
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── SETUP.md                   # Setup guide
├── QUICK_REFERENCE.md         # Quick reference
└── CONFIG_GUIDE.md            # Configuration guide (NEW!)
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd agentforce/data
pip install -r requirements.txt
```

### 2. Set Up Environment

Copy `.env.example` to `.env` and add your Gemini API key:

```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 3. Generate FAQs

**Option A: Full Generation (Recommended)**
```bash
python3 generators/generate_faqs.py
```
Generates 300+ comprehensive FAQs across 20+ categories.

**Option B: Quick Generation**
```bash
python3 generators/quick_generator.py --count 50
```
Generates 50 FAQs quickly for testing.

**Option C: Batch Generation (Rate-Limited)**
```bash
python3 generators/batch_generator.py
```
Generates FAQs in batches with delays to avoid API rate limits.

### 5. Validate Data

```bash
python3 validators/validate_data.py output/banking_faqs.json
```

### 6. Import to Salesforce (Optional)

```bash
# Set SF credentials in .env first
python3 importers/salesforce_import.py output/banking_faqs.json --method bulk
```

## 📊 Generated Files

After running a generator, you'll find these files in `output/`:

- **`banking_faqs.csv`** - CSV format for Salesforce Data Loader
- **`banking_faqs.json`** - Structured JSON with metadata
- **`banking_faqs_vectorsearch.jsonl`** - JSONL format optimized for Vector Search
- **`generation_report.json`** - Statistics and quality metrics

## 🎯 FAQ Categories

The generators create FAQs for:

- Account Management (15-20 FAQs)
- Credit Cards (15 FAQs)
- Loans and Mortgages (20 FAQs)
- Investment Products (20-25 FAQs)
- Retirement Planning (18-20 FAQs)
- Wealth Management Services (25 FAQs)
- Online Banking Security (15 FAQs)
- Wire Transfers and Payments (15 FAQs)
- Foreign Exchange (12 FAQs)
- Tax Planning (18 FAQs)
- Estate Planning (15 FAQs)
- Insurance Products (12 FAQs)
- Small Business Banking (15 FAQs)
- Corporate Banking (12 FAQs)
- Regulatory Compliance (10 FAQs)
- Financial Planning (18 FAQs)
- Portfolio Management (15 FAQs)
- Trust Services (10 FAQs)
- Private Banking (12 FAQs)
- Asset Protection (10 FAQs)

## 🔧 Advanced Usage

### Custom Category Generation

```python
from generators.generate_faqs import BankingFAQGenerator

generator = BankingFAQGenerator()
faqs = generator.generate_category_faqs("Cryptocurrency Banking", count=20)
generator.export_to_json(faqs, "crypto_faqs.json")
```

### Batch Processing with Custom Config

```python
from generators.batch_generator import BatchFAQGenerator

generator = BatchFAQGenerator(batch_size=5, delay=3)
categories = {"Investment Banking": 30, "Forex Trading": 25}
faqs = generator.generate_all_batched(categories)
```

### Data Validation with Report

```bash
python3 validators/validate_data.py output/banking_faqs.json --report output/quality_report.json
```

### Salesforce Import Options

```bash
# Import as Knowledge Articles
python3 importers/salesforce_import.py output/banking_faqs.json --knowledge

# Import as Custom Objects (single record at a time)
python3 importers/salesforce_import.py output/banking_faqs.json --method single --object FAQ__c

# Bulk import (recommended for large datasets)
python3 importers/salesforce_import.py output/banking_faqs.json --method bulk --object FAQ__c
```

## 📝 Data Format

Each FAQ includes:

```json
{
  "question": "Customer question text",
  "answer": "Detailed answer (200-400 words)",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "difficulty": "basic|intermediate|advanced",
  "segment": "retail|business|wealth_management",
  "category": "Main category",
  "subcategory": "Specific subcategory"
}
```

### Vector Search Format (JSONL)

```json
{
  "id": "FAQ_0001",
  "text": "Combined question and answer for embedding",
  "question": "Original question",
  "answer": "Original answer",
  "metadata": {
    "category": "Investment Products",
    "difficulty": "intermediate",
    "segment": "wealth_management",
    "keywords": ["diversification", "portfolio"]
  }
}
```

## 🔐 Environment Variables

Required for generation:
```bash
GEMINI_API_KEY=your_key_here
```

Required for Salesforce import:
```bash
SF_USERNAME=your_username
SF_PASSWORD=your_password
SF_SECURITY_TOKEN=your_token
SF_INSTANCE_URL=https://yourinstance.salesforce.com
```

Optional settings:
```bash
DEFAULT_BATCH_SIZE=10
RATE_LIMIT_DELAY=2
```

## 🎨 Customization

### Modify Categories

Edit `generators/generate_faqs.py`:

```python
CATEGORIES = {
    "Your Category": 20,  # Number of FAQs
    "Another Category": 15,
}
```

### Adjust Quality Thresholds

Edit `validators/validate_data.py`:

```python
MIN_ANSWER_LENGTH = 150  # Increase minimum answer length
MAX_KEYWORDS = 8         # Allow more keywords
```

### Change Output Format

Modify export methods in generators to customize CSV columns, JSON structure, or add new export formats.

## 🐛 Troubleshooting

### API Rate Limits

If you hit rate limits:
1. Use `batch_generator.py` with longer delays
2. Reduce batch size in `.env`: `DEFAULT_BATCH_SIZE=5`
3. Generate fewer FAQs per category

### JSON Parsing Errors

If the generator fails to parse responses:
1. Check your API key is valid
2. Increase delay between requests
3. Try `quick_generator.py` which uses simpler prompts

### Salesforce Import Failures

Common issues:
1. Check custom object/fields exist in Salesforce
2. Verify field API names match your schema
3. Ensure user has proper permissions
4. Check field length limits (adjust in importer)

### Validation Warnings

Common warnings and fixes:
- **Question too short**: Normal for some yes/no questions
- **Answer too long**: May be split into multiple FAQs
- **Missing keywords**: Add keyword generation to your prompt

## 📚 Best Practices

1. **Start Small**: Test with `quick_generator.py` before full generation
2. **Validate Always**: Run validator before importing to Salesforce
3. **Version Control**: Keep generated data in version control for reproducibility
4. **Backup Data**: Save generated files before importing
5. **Test in Sandbox**: Always test Salesforce imports in a sandbox first
6. **Monitor Quality**: Review sample FAQs manually before deployment
7. **Update Regularly**: Regenerate data as banking regulations change

## 🔗 Integration with Agentforce

These FAQs are designed to work with your Agentforce chat agent:

1. Import FAQs to Salesforce Knowledge or custom objects
2. Enable Vector Search on the FAQ object
3. Configure Agentforce agent to query Vector Search
4. Agent will use semantic search to find relevant FAQs
5. Responses will include context from FAQ answers

## 📈 Performance Tips

- Use bulk import for datasets > 100 records
- Generate in batches during off-peak hours
- Cache frequently accessed FAQs
- Index category and keyword fields in Salesforce
- Use JSONL format for vector embeddings

## 🆘 Need Help?

- Check the main project README: `../../README.md`
- Review Agentforce docs: `../docs/GUIDE.md`
- Open an issue on GitHub
- Check Gemini API documentation

---

**Happy Data Generating! 🎉**
