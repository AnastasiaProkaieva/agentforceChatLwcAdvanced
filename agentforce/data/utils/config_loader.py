#!/usr/bin/env python3
"""
Configuration Loader
Loads configuration from YAML files with environment overrides
"""

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv


class ConfigLoader:
    """Load and merge YAML configuration files"""
    
    def __init__(self, env=None):
        """
        Initialize config loader
        
        Args:
            env: Environment name (dev, staging, prod). 
                 If None, reads from ENV or defaults to 'dev'
        """
        self.base_dir = Path(__file__).parent.parent
        self.config_dir = self.base_dir / 'config'
        
        # Load .env file for secrets
        load_dotenv(self.base_dir / '.env')
        
        # Determine environment
        self.env = env or os.getenv('ENV', 'dev')
        
        # Load configurations
        self.config = self._load_config()
    
    def _load_config(self):
        """Load and merge configuration files"""
        # Load base config
        base_config_path = self.base_dir / 'config.yaml'
        config = self._load_yaml(base_config_path)
        
        # Load environment-specific config
        env_config_path = self.config_dir / f'config.{self.env}.yaml'
        if env_config_path.exists():
            env_config = self._load_yaml(env_config_path)
            config = self._deep_merge(config, env_config)
        
        # Add secrets from environment variables
        config['secrets'] = {
            'gemini_api_key': os.getenv('GEMINI_API_KEY'),
            'sf_username': os.getenv('SF_USERNAME'),
            'sf_password': os.getenv('SF_PASSWORD'),
            'sf_security_token': os.getenv('SF_SECURITY_TOKEN'),
            'sf_instance_url': os.getenv('SF_INSTANCE_URL'),
        }
        
        return config
    
    def _load_yaml(self, filepath):
        """Load YAML file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            return {}
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file {filepath}: {e}")
    
    def _deep_merge(self, base, override):
        """Deep merge two dictionaries"""
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def get(self, key_path, default=None):
        """
        Get configuration value using dot notation
        
        Examples:
            config.get('model.name')
            config.get('prompts.generate_faqs')
            config.get('secrets.gemini_api_key')
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def get_model_config(self):
        """Get model configuration"""
        return self.config.get('model', {})
    
    def get_prompt(self, prompt_name, **kwargs):
        """
        Get formatted prompt
        
        Args:
            prompt_name: Name of the prompt (e.g., 'generate_faqs')
            **kwargs: Variables to substitute in the prompt
        """
        prompt_template = self.get(f'prompts.{prompt_name}')
        
        if not prompt_template:
            raise ValueError(f"Prompt '{prompt_name}' not found in config")
        
        # Format the prompt with provided variables
        try:
            return prompt_template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing required variable for prompt: {e}")
    
    def get_categories(self):
        """Get FAQ categories"""
        return self.config.get('categories', {})
    
    def get_generation_settings(self):
        """Get generation settings"""
        return self.config.get('generation', {})
    
    def get_quality_thresholds(self):
        """Get quality thresholds"""
        return self.config.get('quality', {})
    
    def get_export_settings(self):
        """Get export settings"""
        return self.config.get('export', {})


# Convenience function
def load_config(env=None):
    """Load configuration (convenience function)"""
    return ConfigLoader(env=env)


if __name__ == "__main__":
    # Test configuration loading
    print("Testing Configuration Loader")
    print("=" * 60)
    
    # Test dev environment
    print("\n📝 Development Environment:")
    config_dev = load_config('dev')
    print(f"   Model: {config_dev.get('model.name')}")
    print(f"   Batch Size: {config_dev.get('generation.batch_size')}")
    print(f"   Categories: {len(config_dev.get_categories())}")
    
    # Test prod environment
    print("\n🚀 Production Environment:")
    config_prod = load_config('prod')
    print(f"   Model: {config_prod.get('model.name')}")
    print(f"   Batch Size: {config_prod.get('generation.batch_size')}")
    print(f"   Categories: {len(config_prod.get_categories())}")
    
    # Test prompt loading
    print("\n📄 Prompt Test:")
    prompt = config_dev.get_prompt('quick_generate', count=10)
    print(f"   Prompt length: {len(prompt)} chars")
    print(f"   First 100 chars: {prompt[:100]}...")
    
    print("\n✅ Configuration loaded successfully!")
