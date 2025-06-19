import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for Air Quality Monitor"""
    
    # Anthropic API Configuration
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    
    # Database Configuration
    CASSANDRA_HOSTS = os.getenv('CASSANDRA_HOSTS', '127.0.0.1').split(',')
    CASSANDRA_KEYSPACE = os.getenv('CASSANDRA_KEYSPACE', 'pollution_db')
    
    # Web Interface Configuration
    WEB_PORT = int(os.getenv('WEB_PORT', 7860))
    WEB_HOST = os.getenv('WEB_HOST', '0.0.0.0')
    
    @classmethod
    def validate_config(cls):
        """Validate that all required configuration is present"""
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY is required. Please set it in your .env file.")
        if cls.ANTHROPIC_API_KEY == 'your_anthropic_api_key_here':
            raise ValueError("Please replace 'your_anthropic_api_key_here' with your actual Anthropic API key in .env file.")
        
        print("✅ Configuration validated successfully!")
        return True
    
    @classmethod
    def display_config(cls):
        """Display current configuration (without sensitive data)"""
        print("📋 Current Configuration:")
        print(f"   API Key: {'✅ Set' if cls.ANTHROPIC_API_KEY else '❌ Missing'}")
        print(f"   Cassandra Hosts: {cls.CASSANDRA_HOSTS}")
        print(f"   Cassandra Keyspace: {cls.CASSANDRA_KEYSPACE}")
        print(f"   Web Port: {cls.WEB_PORT}")
        print(f"   Web Host: {cls.WEB_HOST}") 