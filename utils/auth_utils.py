import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from pathlib import Path

def initialize_authentication():
    """Initialize the authentication system using streamlit_authenticator 0.4.2"""
    
    # Load configuration
    config_path = Path("config.yaml")
    
    with open(config_path) as file:
        config = yaml.load(file, Loader=SafeLoader)
    
    # Create authenticator object
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
    
    return authenticator
