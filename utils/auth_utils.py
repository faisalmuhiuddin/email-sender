import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from pathlib import Path

def initialize_authentication():
    """Initialize the authentication system using streamlit_authenticator 0.4.2"""
    
    # Load configuration
    config_path = Path("config.yaml")
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file {config_path} not found. Please create it.")
    
    try:
        with open(config_path) as file:
            config = yaml.load(file, Loader=SafeLoader)
    except Exception as e:
        raise ValueError(f"Error loading configuration file: {e}")
    
    # Validate configuration structure
    required_keys = ['credentials', 'cookie']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required configuration key: {key}")
    
    # Create authenticator object
    try:
        authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days']
        )
        return authenticator
    except Exception as e:
        raise ValueError(f"Error creating authenticator: {e}")
