#!/usr/bin/env python3
"""
Salesforce Vector Search Importer
Import FAQ data into Salesforce for Vector Search
"""

import os
import json
import sys
from pathlib import Path
from dotenv import load_dotenv
from simple_salesforce import Salesforce
from tqdm import tqdm

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')


class SalesforceVectorImporter:
    """Import FAQs into Salesforce for Vector Search"""
    
    def __init__(self):
        """Initialize Salesforce connection"""
        self.username = os.getenv('SF_USERNAME')
        self.password = os.getenv('SF_PASSWORD')
        self.security_token = os.getenv('SF_SECURITY_TOKEN')
        self.instance_url = os.getenv('SF_INSTANCE_URL')
        
        if not all([self.username, self.password, self.security_token]):
            raise ValueError(
                "❌ Missing Salesforce credentials. "
                "Please set SF_USERNAME, SF_PASSWORD, and SF_SECURITY_TOKEN in .env"
            )
        
        print("🔐 Connecting to Salesforce...")
        try:
            self.sf = Salesforce(
                username=self.username,
                password=self.password,
                security_token=self.security_token,
                instance_url=self.instance_url
            )
            print(f"✅ Connected to Salesforce")
            print(f"   Instance: {self.sf.sf_instance}")
            print(f"   Version: {self.sf.sf_version}")
        except Exception as e:
            raise ConnectionError(f"❌ Failed to connect to Salesforce: {e}")
    
    def create_knowledge_articles(self, faqs, article_type='FAQ__kav'):
        """
        Create Knowledge Articles from FAQs
        
        Args:
            faqs: List of FAQ dictionaries
            article_type: Salesforce Knowledge Article Type API name
        """
        print(f"\n📝 Creating {len(faqs)} Knowledge Articles...")
        print("=" * 60)
        
        created = 0
        failed = 0
        errors = []
        
        for idx, faq in enumerate(tqdm(faqs, desc="Importing"), 1):
            try:
                # Prepare article data
                article_data = {
                    'Title': faq['question'][:255],  # Salesforce title limit
                    'Question__c': faq['question'],
                    'Answer__c': faq['answer'],
                    'UrlName': self._generate_url_name(faq['question'], idx),
                    'Language': 'en_US',
                    'ValidationStatus': 'Draft'
                }
                
                # Add optional fields if they exist
                if 'category' in faq:
                    article_data['Category__c'] = faq['category']
                
                if 'difficulty' in faq:
                    article_data['Difficulty__c'] = faq['difficulty'].capitalize()
                
                if 'segment' in faq:
                    article_data['Segment__c'] = faq['segment'].replace('_', ' ').title()
                
                if 'keywords' in faq:
                    keywords = ', '.join(faq['keywords'][:5])  # Limit keywords
                    article_data['Keywords__c'] = keywords[:255]  # Field limit
                
                # Create the article
                result = self.sf.__getattr__(article_type).create(article_data)
                
                if result['success']:
                    created += 1
                else:
                    failed += 1
                    errors.append(f"FAQ #{idx}: {result}")
                
            except Exception as e:
                failed += 1
                errors.append(f"FAQ #{idx}: {str(e)}")
        
        # Print results
        print("\n" + "=" * 60)
        print("📊 Import Results")
        print("=" * 60)
        print(f"✅ Created: {created}")
        print(f"❌ Failed: {failed}")
        
        if errors and len(errors) <= 10:
            print("\n❌ Errors:")
            for error in errors:
                print(f"   {error}")
        elif errors:
            print(f"\n❌ {len(errors)} errors occurred (showing first 5):")
            for error in errors[:5]:
                print(f"   {error}")
        
        return {'created': created, 'failed': failed, 'errors': errors}
    
    def create_custom_objects(self, faqs, object_name='FAQ__c'):
        """
        Create custom objects for FAQs
        
        Args:
            faqs: List of FAQ dictionaries
            object_name: Custom object API name
        """
        print(f"\n📝 Creating {len(faqs)} Custom Objects ({object_name})...")
        print("=" * 60)
        
        created = 0
        failed = 0
        errors = []
        
        for idx, faq in enumerate(tqdm(faqs, desc="Importing"), 1):
            try:
                # Prepare custom object data
                obj_data = {
                    'Name': faq['question'][:80],  # Name field limit
                    'Question__c': faq['question'],
                    'Answer__c': faq['answer'],
                    'Category__c': faq.get('category', 'General'),
                    'Difficulty__c': faq.get('difficulty', 'basic').capitalize(),
                    'Segment__c': faq.get('segment', 'retail').replace('_', ' ').title(),
                }
                
                # Add keywords if present
                if 'keywords' in faq and faq['keywords']:
                    obj_data['Keywords__c'] = ', '.join(faq['keywords'][:5])
                
                # Create the record
                result = self.sf.__getattr__(object_name).create(obj_data)
                
                if result['success']:
                    created += 1
                else:
                    failed += 1
                    errors.append(f"FAQ #{idx}: {result}")
                
            except Exception as e:
                failed += 1
                errors.append(f"FAQ #{idx}: {str(e)}")
        
        # Print results
        print("\n" + "=" * 60)
        print("📊 Import Results")
        print("=" * 60)
        print(f"✅ Created: {created}")
        print(f"❌ Failed: {failed}")
        
        if errors and len(errors) <= 10:
            print("\n❌ Errors:")
            for error in errors:
                print(f"   {error}")
        
        return {'created': created, 'failed': failed, 'errors': errors}
    
    def bulk_import(self, faqs, object_name='FAQ__c', batch_size=200):
        """
        Bulk import FAQs using Salesforce Bulk API
        
        Args:
            faqs: List of FAQ dictionaries
            object_name: Object API name
            batch_size: Number of records per batch
        """
        print(f"\n⚡ Bulk importing {len(faqs)} records...")
        print(f"   Object: {object_name}")
        print(f"   Batch size: {batch_size}")
        print("=" * 60)
        
        # Prepare data for bulk import
        records = []
        for idx, faq in enumerate(faqs, 1):
            record = {
                'Name': faq['question'][:80],
                'Question__c': faq['question'],
                'Answer__c': faq['answer'],
                'Category__c': faq.get('category', 'General'),
                'Difficulty__c': faq.get('difficulty', 'basic').capitalize(),
                'Segment__c': faq.get('segment', 'retail').replace('_', ' ').title(),
            }
            
            if 'keywords' in faq and faq['keywords']:
                record['Keywords__c'] = ', '.join(faq['keywords'][:5])
            
            records.append(record)
        
        try:
            # Use bulk API
            results = self.sf.bulk.__getattr__(object_name).insert(records, batch_size=batch_size)
            
            # Count successes and failures
            created = sum(1 for r in results if r['success'])
            failed = sum(1 for r in results if not r['success'])
            
            print(f"\n✅ Successfully imported: {created}")
            print(f"❌ Failed: {failed}")
            
            # Show sample errors
            errors = [r for r in results if not r['success']]
            if errors:
                print(f"\nSample errors (showing first 5):")
                for error in errors[:5]:
                    print(f"   {error}")
            
            return {'created': created, 'failed': failed, 'results': results}
            
        except Exception as e:
            print(f"❌ Bulk import failed: {e}")
            return {'created': 0, 'failed': len(records), 'error': str(e)}
    
    def _generate_url_name(self, question, idx):
        """Generate URL-safe name for Knowledge Article"""
        import re
        
        # Take first 50 chars of question
        name = question[:50].lower()
        
        # Replace special chars with hyphens
        name = re.sub(r'[^a-z0-9]+', '-', name)
        
        # Remove leading/trailing hyphens
        name = name.strip('-')
        
        # Add index for uniqueness
        name = f"{name}-{idx}"
        
        return name


def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Import FAQs to Salesforce')
    parser.add_argument('file', help='JSON file with FAQs')
    parser.add_argument('--object', default='FAQ__c', help='Salesforce object name')
    parser.add_argument('--method', choices=['single', 'bulk'], default='bulk',
                       help='Import method (single or bulk)')
    parser.add_argument('--knowledge', action='store_true',
                       help='Import as Knowledge Articles')
    
    args = parser.parse_args()
    
    # Load FAQs
    print(f"📂 Loading FAQs from: {args.file}")
    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        faqs = data['faqs'] if isinstance(data, dict) else data
        print(f"✅ Loaded {len(faqs)} FAQs")
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        sys.exit(1)
    
    # Initialize importer
    try:
        importer = SalesforceVectorImporter()
    except Exception as e:
        print(f"❌ {e}")
        sys.exit(1)
    
    # Import based on method
    if args.knowledge:
        results = importer.create_knowledge_articles(faqs)
    elif args.method == 'bulk':
        results = importer.bulk_import(faqs, args.object)
    else:
        results = importer.create_custom_objects(faqs, args.object)
    
    print("\n🎉 Import complete!")
    
    if results['failed'] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
