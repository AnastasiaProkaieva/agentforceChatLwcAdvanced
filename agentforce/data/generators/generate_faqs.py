#!/usr/bin/env python3
"""
Banking FAQ Generator - Main Script
Generates synthetic FAQ data for Bank Services and Wealth Management
Optimized for Salesforce Vector Search
Uses centralized configuration from config.yaml
"""

import os
import json
import csv
import sys
from pathlib import Path
from datetime import datetime
import google.generativeai as genai
from tqdm import tqdm

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from utils.config_loader import load_config


class BankingFAQGenerator:
    """Generate realistic banking and wealth management FAQs"""
    
    def __init__(self, api_key=None, output_dir=None, env='dev'):
        """Initialize the generator with config-driven settings"""
        
        # Load configuration
        self.config = load_config(env)
        
        # Get API key
        self.api_key = api_key or self.config.get('secrets.gemini_api_key')
        if not self.api_key:
            raise ValueError("❌ GEMINI_API_KEY not found. Please set it in .env file")
        
        # Get model configuration
        model_config = self.config.get_model_config()
        model_name = model_config.get('name', 'gemini-1.5-pro')
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)
        
        # Get categories from config
        self.CATEGORIES = self.config.get_categories()
        
        # Get generation settings
        self.generation_settings = self.config.get_generation_settings()
        
        # Set output directory
        self.output_dir = Path(output_dir) if output_dir else Path(__file__).parent.parent / 'output'
        self.output_dir.mkdir(exist_ok=True)
        
        print(f"✅ Initialized Banking FAQ Generator")
        print(f"🤖 Model: {model_name}")
        print(f"🌍 Environment: {env}")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"📊 Categories: {len(self.CATEGORIES)}")
    
    def generate_category_faqs(self, category, count=15):
        """Generate FAQs for a specific category using config prompt"""
        
        # Get prompt from config
        prompt = self.config.get_prompt('generate_faqs', count=count, category=category)
        
        try:
            response = self.model.generate_content(prompt)
            return self._parse_response(response.text, category)
        except Exception as e:
            print(f"❌ Error generating FAQs for {category}: {e}")
            return []
    
    def _parse_response(self, text, category):
        """Parse Gemini API response and extract JSON"""
        try:
            # Clean the response
            text = text.strip()
            
            # Remove markdown code blocks if present
            if '```' in text:
                parts = text.split('```')
                for part in parts:
                    part = part.strip()
                    if part.startswith('json'):
                        text = part[4:].strip()
                        break
                    elif part.startswith('[') or part.startswith('{'):
                        text = part
                        break
            
            # Parse JSON
            faqs = json.loads(text)
            
            # Ensure it's a list
            if isinstance(faqs, dict):
                faqs = [faqs]
            
            # Validate and clean each FAQ
            cleaned_faqs = []
            for faq in faqs:
                if 'question' in faq and 'answer' in faq:
                    # Ensure category is set
                    faq['category'] = category
                    
                    # Set defaults for missing fields
                    faq.setdefault('keywords', [])
                    faq.setdefault('difficulty', 'basic')
                    faq.setdefault('segment', 'retail')
                    faq.setdefault('subcategory', category)
                    
                    cleaned_faqs.append(faq)
            
            return cleaned_faqs
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            print(f"Response preview: {text[:200]}...")
            return []
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return []
    
    def generate_all_faqs(self):
        """Generate FAQs for all categories"""
        print(f"\n📝 Generating FAQs for {len(self.CATEGORIES)} categories...")
        print("=" * 60)
        
        all_faqs = []
        
        for category, count in tqdm(self.CATEGORIES.items(), desc="Categories"):
            print(f"\n🔄 {category}: Generating {count} FAQs...")
            
            faqs = self.generate_category_faqs(category, count)
            all_faqs.extend(faqs)
            
            print(f"   ✅ Generated {len(faqs)} FAQs")
        
        print(f"\n🎉 Total FAQs generated: {len(all_faqs)}")
        return all_faqs
    
    def export_to_csv(self, faqs, filename="banking_faqs.csv"):
        """Export FAQs to CSV format (Salesforce-compatible)"""
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'id', 'question', 'answer', 'keywords', 'difficulty',
                'segment', 'category', 'subcategory', 'created_date'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            for idx, faq in enumerate(faqs, 1):
                writer.writerow({
                    'id': f"FAQ_{idx:04d}",
                    'question': faq['question'],
                    'answer': faq['answer'],
                    'keywords': ', '.join(faq.get('keywords', [])),
                    'difficulty': faq.get('difficulty', 'basic'),
                    'segment': faq.get('segment', 'retail'),
                    'category': faq.get('category', 'General'),
                    'subcategory': faq.get('subcategory', 'General'),
                    'created_date': datetime.now().strftime('%Y-%m-%d')
                })
        
        print(f"✅ CSV exported: {filepath}")
        return filepath
    
    def export_to_json(self, faqs, filename="banking_faqs.json"):
        """Export FAQs to JSON format"""
        filepath = self.output_dir / filename
        
        output = {
            'metadata': {
                'total_faqs': len(faqs),
                'generated_date': datetime.now().isoformat(),
                'categories': list(set(faq.get('category', 'General') for faq in faqs)),
                'generator': 'BankingFAQGenerator v1.0'
            },
            'faqs': faqs
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"✅ JSON exported: {filepath}")
        return filepath
    
    def export_for_vector_search(self, faqs, filename="banking_faqs_vectorsearch.jsonl"):
        """Export in JSONL format optimized for Vector Search"""
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for idx, faq in enumerate(faqs, 1):
                # Create combined text for embedding
                combined_text = f"Question: {faq['question']}\n\nAnswer: {faq['answer']}"
                
                # Add keywords to text for better search
                if faq.get('keywords'):
                    keywords_text = ', '.join(faq['keywords'])
                    combined_text += f"\n\nKeywords: {keywords_text}"
                
                record = {
                    'id': f"FAQ_{idx:04d}",
                    'text': combined_text,
                    'question': faq['question'],
                    'answer': faq['answer'],
                    'metadata': {
                        'category': faq.get('category', 'General'),
                        'subcategory': faq.get('subcategory', 'General'),
                        'difficulty': faq.get('difficulty', 'basic'),
                        'segment': faq.get('segment', 'retail'),
                        'keywords': faq.get('keywords', []),
                        'created_date': datetime.now().isoformat()
                    }
                }
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
        
        print(f"✅ Vector Search JSONL exported: {filepath}")
        return filepath
    
    def generate_summary_report(self, faqs):
        """Generate a summary report of the generated FAQs"""
        from collections import Counter
        
        report = {
            'total_faqs': len(faqs),
            'by_category': Counter(faq.get('category', 'Unknown') for faq in faqs),
            'by_difficulty': Counter(faq.get('difficulty', 'Unknown') for faq in faqs),
            'by_segment': Counter(faq.get('segment', 'Unknown') for faq in faqs),
            'avg_question_length': sum(len(faq['question']) for faq in faqs) / len(faqs),
            'avg_answer_length': sum(len(faq['answer']) for faq in faqs) / len(faqs),
        }
        
        filepath = self.output_dir / 'generation_report.json'
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 Summary Report:")
        print(f"   Total FAQs: {report['total_faqs']}")
        print(f"   Categories: {len(report['by_category'])}")
        print(f"   Avg Question Length: {report['avg_question_length']:.0f} chars")
        print(f"   Avg Answer Length: {report['avg_answer_length']:.0f} chars")
        print(f"✅ Report saved: {filepath}")
        
        return report


def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Banking FAQ Generator')
    parser.add_argument('--env', type=str, default='dev',
                       choices=['dev', 'staging', 'prod'],
                       help='Environment (dev/staging/prod)')
    parser.add_argument('--output', type=str, help='Output directory')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🏦 Banking & Wealth Management FAQ Generator")
    print("=" * 60)
    
    try:
        # Initialize generator with environment
        generator = BankingFAQGenerator(output_dir=args.output, env=args.env)
        
        # Generate FAQs
        faqs = generator.generate_all_faqs()
        
        if not faqs:
            print("❌ No FAQs generated. Please check your API key and connection.")
            sys.exit(1)
        
        # Export in multiple formats
        print(f"\n💾 Exporting data...")
        print("-" * 60)
        
        generator.export_to_csv(faqs)
        generator.export_to_json(faqs)
        generator.export_for_vector_search(faqs)
        
        # Generate report
        generator.generate_summary_report(faqs)
        
        print("\n" + "=" * 60)
        print("🎉 FAQ Generation Complete!")
        print("=" * 60)
        print("\n📁 Files created in:", generator.output_dir)
        print("   - banking_faqs.csv (Salesforce import)")
        print("   - banking_faqs.json (structured data)")
        print("   - banking_faqs_vectorsearch.jsonl (Vector Search)")
        print("   - generation_report.json (statistics)")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
