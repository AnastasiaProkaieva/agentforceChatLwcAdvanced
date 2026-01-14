#!/usr/bin/env python3
"""
FAQ Data Validator
Validates generated FAQ data for quality, completeness, and format
"""

import json
import sys
from pathlib import Path
from collections import Counter
import re


class FAQValidator:
    """Validate FAQ data quality and format"""
    
    REQUIRED_FIELDS = ['question', 'answer', 'category']
    OPTIONAL_FIELDS = ['keywords', 'difficulty', 'segment', 'subcategory']
    
    VALID_DIFFICULTIES = ['basic', 'intermediate', 'advanced']
    VALID_SEGMENTS = ['retail', 'business', 'wealth_management']
    
    # Quality thresholds
    MIN_QUESTION_LENGTH = 10
    MAX_QUESTION_LENGTH = 500
    MIN_ANSWER_LENGTH = 100
    MAX_ANSWER_LENGTH = 2000
    MIN_KEYWORDS = 1
    MAX_KEYWORDS = 10
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.stats = {
            'total': 0,
            'valid': 0,
            'invalid': 0,
            'warnings': 0
        }
    
    def validate_file(self, filepath):
        """Validate a JSON file containing FAQs"""
        print(f"🔍 Validating: {filepath}")
        print("=" * 60)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different JSON structures
            if isinstance(data, dict) and 'faqs' in data:
                faqs = data['faqs']
            elif isinstance(data, list):
                faqs = data
            else:
                raise ValueError("Invalid JSON structure. Expected list or dict with 'faqs' key")
            
            return self.validate_faqs(faqs)
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON Parse Error: {e}")
            return False
        except FileNotFoundError:
            print(f"❌ File not found: {filepath}")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def validate_faqs(self, faqs):
        """Validate a list of FAQs"""
        self.stats['total'] = len(faqs)
        
        print(f"📊 Validating {len(faqs)} FAQs...\n")
        
        for idx, faq in enumerate(faqs, 1):
            is_valid = self.validate_single_faq(faq, idx)
            
            if is_valid:
                self.stats['valid'] += 1
            else:
                self.stats['invalid'] += 1
        
        # Print results
        self._print_results()
        
        # Return overall validity
        return self.stats['invalid'] == 0
    
    def validate_single_faq(self, faq, idx):
        """Validate a single FAQ entry"""
        is_valid = True
        
        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field not in faq or not faq[field]:
                self.errors.append(f"FAQ #{idx}: Missing required field '{field}'")
                is_valid = False
        
        if not is_valid:
            return False
        
        # Validate question
        question = faq['question'].strip()
        if len(question) < self.MIN_QUESTION_LENGTH:
            self.warnings.append(f"FAQ #{idx}: Question too short ({len(question)} chars)")
            self.stats['warnings'] += 1
        elif len(question) > self.MAX_QUESTION_LENGTH:
            self.warnings.append(f"FAQ #{idx}: Question too long ({len(question)} chars)")
            self.stats['warnings'] += 1
        
        # Check for question mark
        if not question.endswith('?'):
            self.warnings.append(f"FAQ #{idx}: Question doesn't end with '?'")
            self.stats['warnings'] += 1
        
        # Validate answer
        answer = faq['answer'].strip()
        if len(answer) < self.MIN_ANSWER_LENGTH:
            self.warnings.append(f"FAQ #{idx}: Answer too short ({len(answer)} chars)")
            self.stats['warnings'] += 1
        elif len(answer) > self.MAX_ANSWER_LENGTH:
            self.warnings.append(f"FAQ #{idx}: Answer too long ({len(answer)} chars)")
            self.stats['warnings'] += 1
        
        # Validate keywords
        if 'keywords' in faq:
            keywords = faq['keywords']
            if not isinstance(keywords, list):
                self.errors.append(f"FAQ #{idx}: Keywords must be a list")
                is_valid = False
            elif len(keywords) < self.MIN_KEYWORDS:
                self.warnings.append(f"FAQ #{idx}: Too few keywords ({len(keywords)})")
                self.stats['warnings'] += 1
            elif len(keywords) > self.MAX_KEYWORDS:
                self.warnings.append(f"FAQ #{idx}: Too many keywords ({len(keywords)})")
                self.stats['warnings'] += 1
        
        # Validate difficulty
        if 'difficulty' in faq:
            if faq['difficulty'] not in self.VALID_DIFFICULTIES:
                self.errors.append(f"FAQ #{idx}: Invalid difficulty '{faq['difficulty']}'")
                is_valid = False
        
        # Validate segment
        if 'segment' in faq:
            if faq['segment'] not in self.VALID_SEGMENTS:
                self.errors.append(f"FAQ #{idx}: Invalid segment '{faq['segment']}'")
                is_valid = False
        
        # Check for duplicates in answer (copy-paste detection)
        if self._has_repetitive_content(answer):
            self.warnings.append(f"FAQ #{idx}: Answer may have repetitive content")
            self.stats['warnings'] += 1
        
        return is_valid
    
    def _has_repetitive_content(self, text, threshold=0.3):
        """Detect repetitive content in text"""
        sentences = re.split(r'[.!?]+', text)
        if len(sentences) < 3:
            return False
        
        # Check for duplicate sentences
        sentence_counts = Counter(s.strip().lower() for s in sentences if s.strip())
        max_count = max(sentence_counts.values()) if sentence_counts else 0
        
        return max_count / len(sentences) > threshold
    
    def _print_results(self):
        """Print validation results"""
        print("\n" + "=" * 60)
        print("📋 Validation Results")
        print("=" * 60)
        
        print(f"Total FAQs: {self.stats['total']}")
        print(f"✅ Valid: {self.stats['valid']}")
        print(f"❌ Invalid: {self.stats['invalid']}")
        print(f"⚠️  Warnings: {self.stats['warnings']}")
        
        # Print errors
        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors[:10]:  # Show first 10
                print(f"   - {error}")
            if len(self.errors) > 10:
                print(f"   ... and {len(self.errors) - 10} more")
        
        # Print warnings
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings[:10]:  # Show first 10
                print(f"   - {warning}")
            if len(self.warnings) > 10:
                print(f"   ... and {len(self.warnings) - 10} more")
        
        # Overall result
        print("\n" + "=" * 60)
        if self.stats['invalid'] == 0:
            if self.stats['warnings'] == 0:
                print("🎉 PASSED: All FAQs are valid with no warnings!")
            else:
                print("✅ PASSED: All FAQs are valid (with warnings)")
        else:
            print("❌ FAILED: Some FAQs have errors")
        print("=" * 60)
    
    def generate_quality_report(self, faqs, output_path=None):
        """Generate detailed quality report"""
        report = {
            'summary': self.stats,
            'category_distribution': Counter(faq.get('category', 'Unknown') for faq in faqs),
            'difficulty_distribution': Counter(faq.get('difficulty', 'Unknown') for faq in faqs),
            'segment_distribution': Counter(faq.get('segment', 'Unknown') for faq in faqs),
            'avg_question_length': sum(len(faq['question']) for faq in faqs) / len(faqs),
            'avg_answer_length': sum(len(faq['answer']) for faq in faqs) / len(faqs),
            'avg_keywords': sum(len(faq.get('keywords', [])) for faq in faqs) / len(faqs),
        }
        
        if output_path:
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\n📊 Quality report saved: {output_path}")
        
        return report


def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate FAQ data')
    parser.add_argument('file', help='JSON file to validate')
    parser.add_argument('--report', help='Output path for quality report')
    
    args = parser.parse_args()
    
    validator = FAQValidator()
    is_valid = validator.validate_file(args.file)
    
    if args.report:
        with open(args.file, 'r') as f:
            data = json.load(f)
        faqs = data['faqs'] if isinstance(data, dict) else data
        validator.generate_quality_report(faqs, args.report)
    
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
