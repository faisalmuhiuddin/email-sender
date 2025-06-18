import pandas as pd
import streamlit as st

def load_poc_data(file_path):
    """Load and validate POC data from Excel file"""
    try:
        df = pd.read_excel(file_path)
        
        # Validate required columns
        required_columns = ["POC_name", "POC_designation", "POC_contact"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
            
        return df
        
    except Exception as e:
        st.error(f"Error loading POC data: {e}")
        return pd.DataFrame(columns=["POC_name", "POC_designation", "POC_contact"])

def validate_contacts_file(file):
    """Validate uploaded contacts file and return DataFrame"""
    try:
        df = pd.read_excel(file)
        
        # Validate required columns
        required_columns = ["email", "name", "company"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
        
        # Validate email format
        invalid_emails = df[~df["email"].str.contains("@")]["email"].tolist()
        if invalid_emails:
            raise ValueError(f"Invalid email format for: {', '.join(invalid_emails[:5])}" + 
                            (f"... and {len(invalid_emails) - 5} more" if len(invalid_emails) > 5 else ""))
        
        return df
        
    except Exception as e:
        raise ValueError(f"Error validating contacts file: {e}")
