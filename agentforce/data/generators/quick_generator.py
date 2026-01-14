#!/usr/bin/env python3
"""
Quick FAQ Generator - Simple Version
For rapid prototyping and small datasets
Uses centralized configuration from config.yaml
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime
import google.generativeai as genai

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from utils.config_loader import load_config


def generate_quick_faqs(num_faqs=50, output_dir=None, env='dev'):
    """Quick generation of banking FAQs using centralized config"""
    
    # Load configuration
    config = load_config(env)
    
    # Get API key from config
    api_key = config.get('secrets.gemini_api_key')
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env file")
        sys.exit(1)
    
    # Get model configuration
    model_config = config.get_model_config()
    model_name = model_config.get('name', 'gemini-1.5-flash')
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    
    # Set output directory
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / 'output'
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    print(f"🚀 Quick FAQ Generator")
    print(f"📝 Generating {num_faqs} FAQs...")
    print(f"🤖 Using model: {model_name}")
    print(f"🌍 Environment: {env}")
    
    # Get prompt from config
    prompt = config.get_prompt('quick_generate', count=num_faqs)
    
    try:
        response = model.generate_content(prompt)
        
        # Parse response
        text = response.text.strip()
        if '```' in text:
            text = text.split('```')[1]
            if text.startswith('json'):
                text = text[4:]
        text = text.strip()
        
        faqs = json.loads(text)
        
        # Add metadata
        for idx, faq in enumerate(faqs, 1):
            faq['id'] = f"FAQ_{idx:04d}"
            faq['generated_date'] = datetime.now().isoformat()
        
        # Save to file
        output_file = output_dir / 'banking_faqs_quick.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': {
                    'total': len(faqs),
                    'generated': datetime.now().isoformat(),
                    'method': 'quick_generator'
                },
                'faqs': faqs
            }, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Generated {len(faqs)} FAQs")
        print(f"💾 Saved to: {output_file}")
        
        return faqs
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Quick FAQ Generator')
    parser.add_argument('--count', type=int, default=50, help='Number of FAQs to generate')
    parser.add_argument('--output', type=str, help='Output directory')
    parser.add_argument('--env', type=str, default='dev', 
                       choices=['dev', 'staging', 'prod'],
                       help='Environment (dev/staging/prod)')
    
    args = parser.parse_args()
    
    generate_quick_faqs(num_faqs=args.count, output_dir=args.output, env=args.env)
