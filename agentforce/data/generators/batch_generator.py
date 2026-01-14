#!/usr/bin/env python3
"""
Batch FAQ Generator with Rate Limiting
Generates FAQs in batches to avoid API rate limits
"""

import os
import json
import time
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from tqdm import tqdm

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')


class BatchFAQGenerator:
    """Generate FAQs in controlled batches with rate limiting"""
    
    def __init__(self, api_key=None, batch_size=10, delay=2):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("❌ GEMINI_API_KEY not found")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        
        self.batch_size = int(os.getenv('DEFAULT_BATCH_SIZE', batch_size))
        self.delay = int(os.getenv('RATE_LIMIT_DELAY', delay))
        
        self.output_dir = Path(__file__).parent.parent / 'output'
        self.output_dir.mkdir(exist_ok=True)
        
        print(f"⚙️  Batch Generator Config:")
        print(f"   Batch size: {self.batch_size}")
        print(f"   Delay: {self.delay}s between batches")
    
    def generate_batch(self, category, batch_num, total_batches):
        """Generate a single batch of FAQs"""
        
        prompt = f"""
Generate {self.batch_size} unique FAQs for "{category}" in banking/wealth management.

This is batch {batch_num} of {total_batches}, so ensure variety and avoid repetition.

Return JSON array:
[
  {{
    "question": "question text",
    "answer": "detailed answer (200-300 words)",
    "keywords": ["keyword1", "keyword2"],
    "difficulty": "basic|intermediate|advanced",
    "segment": "retail|business|wealth_management"
  }}
]

Only return valid JSON, no markdown.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return self._parse_response(response.text, category)
        except Exception as e:
            print(f"    ⚠️  Error in batch {batch_num}: {e}")
            return []
    
    def _parse_response(self, text, category):
        """Parse and clean API response"""
        text = text.strip()
        
        if '```' in text:
            text = text.split('```')[1]
            if text.startswith('json'):
                text = text[4:]
        text = text.strip()
        
        try:
            faqs = json.loads(text)
            if isinstance(faqs, dict):
                faqs = [faqs]
            
            # Add category to each FAQ
            for faq in faqs:
                faq['category'] = category
            
            return faqs
        except:
            return []
    
    def generate_category_batched(self, category, total_count):
        """Generate FAQs for a category in batches"""
        num_batches = (total_count + self.batch_size - 1) // self.batch_size
        
        print(f"\n🔄 {category}: {total_count} FAQs in {num_batches} batches")
        
        all_faqs = []
        
        for batch_num in range(1, num_batches + 1):
            print(f"   Batch {batch_num}/{num_batches}...", end=' ')
            
            faqs = self.generate_batch(category, batch_num, num_batches)
            all_faqs.extend(faqs)
            
            print(f"✅ {len(faqs)} FAQs")
            
            # Rate limiting (except for last batch)
            if batch_num < num_batches:
                time.sleep(self.delay)
        
        print(f"   ✅ Total for {category}: {len(all_faqs)} FAQs")
        return all_faqs
    
    def generate_all_batched(self, categories):
        """Generate FAQs for all categories with batching"""
        print("=" * 60)
        print("📦 Batch FAQ Generation")
        print("=" * 60)
        
        all_faqs = []
        
        for category, count in categories.items():
            faqs = self.generate_category_batched(category, count)
            all_faqs.extend(faqs)
            
            # Small delay between categories
            time.sleep(1)
        
        return all_faqs
    
    def save_results(self, faqs, filename="banking_faqs_batched.json"):
        """Save generated FAQs"""
        filepath = self.output_dir / filename
        
        output = {
            'metadata': {
                'total_faqs': len(faqs),
                'generated_date': datetime.now().isoformat(),
                'method': 'batch_generator',
                'batch_size': self.batch_size
            },
            'faqs': faqs
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Saved to: {filepath}")
        return filepath


def main():
    """Main execution"""
    
    # Define categories
    categories = {
        "Account Management": 20,
        "Investment Products": 25,
        "Wealth Management": 25,
        "Loans and Mortgages": 20,
        "Retirement Planning": 20,
        "Online Banking": 15,
    }
    
    try:
        generator = BatchFAQGenerator()
        faqs = generator.generate_all_batched(categories)
        
        print(f"\n🎉 Generated {len(faqs)} total FAQs")
        
        generator.save_results(faqs)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
