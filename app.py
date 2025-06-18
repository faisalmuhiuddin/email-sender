import streamlit as st
import yaml
from yaml.loader import SafeLoader
import os
import pandas as pd
from pathlib import Path
import streamlit_authenticator as stauth

# Import utility modules
from utils.auth_utils import initialize_authentication
from utils.data_utils import load_poc_data, validate_contacts_file
from utils.email_utils import send_emails
from utils.template_utils import render_email_template

# Page configuration
st.set_page_config(
    page_title="Secure Email Sender",
    page_icon="📧",
    layout="wide"
)

# Application title and description
def show_header():
    st.title("📧 Secure Email Sender")
    st.markdown("Send personalized emails using templates and contact lists")

# Initialize session state variables
def initialize_session_state():
    if "authentication_status" not in st.session_state:
        st.session_state["authentication_status"] = None
    if "poc_data" not in st.session_state:
        st.session_state["poc_data"] = None
    if "selected_poc" not in st.session_state:
        st.session_state["selected_poc"] = None
    if "template_type" not in st.session_state:
        st.session_state["template_type"] = "Analytics"
    if "email_results" not in st.session_state:
        st.session_state["email_results"] = {"success": [], "failed": []}

# Login page
def show_login_page(authenticator):
    st.subheader("Login")
    
    try:
        name, authentication_status, username = authenticator.login('Login', 'main')
        
        if authentication_status == False:
            st.error("Invalid username or password")
        elif authentication_status is None:
            st.warning("Please enter your credentials")
            
    except Exception as e:
        st.error(f"Authentication Error: {e}")
        
    return authentication_status

# Main application page
def show_main_page():
    st.subheader("Email Configuration")
    
    # 1. POC Selection
    poc_data = load_poc_data("data/poc_details.xlsx")
    poc_names = poc_data["POC_name"].tolist()
    
    selected_poc_name = st.selectbox(
        "Select Point of Contact (POC)",
        options=poc_names
    )
    
    # Get selected POC details
    selected_poc = poc_data[poc_data["POC_name"] == selected_poc_name].iloc[0]
    st.session_state["selected_poc"] = selected_poc
    
    # Show POC details
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Name:** {selected_poc['POC_name']}")
        st.info(f"**Designation:** {selected_poc['POC_designation']}")
    with col2:
        st.info(f"**Contact:** {selected_poc['POC_contact']}")
    
    # 2. Template Selection
    template_type = st.radio(
        "Select Email Template",
        options=["Analytics", "Fin"],
        horizontal=True
    )
    st.session_state["template_type"] = template_type
    
    # 3. Upload Contacts
    st.subheader("Upload Contact List")
    contacts_file = st.file_uploader(
        "Upload Excel file with contacts (must contain email, name, company columns)",
        type=["xlsx", "xls"]
    )
    
    # 4. Email Preview and Sending
    if contacts_file is not None:
        # Validate the contacts file
        try:
            contacts_df = validate_contacts_file(contacts_file)
            st.success(f"Successfully loaded {len(contacts_df)} contacts")
            
            # Preview section
            with st.expander("Preview Email Template"):
                # Get sample data for preview
                sample_contact = contacts_df.iloc[0]
                sample_data = {
                    "name": sample_contact["name"],
                    "company": sample_contact["company"],
                    "poc_name": selected_poc["POC_name"],
                    "poc_designation": selected_poc["POC_designation"],
                    "poc_contact": selected_poc["POC_contact"]
                }
                
                # Render the template with sample data
                sample_html = render_email_template(
                    template_type,
                    sample_data
                )
                st.markdown("### Email Preview")
                st.markdown(f"**Subject:** {template_type} Opportunity")
                st.components.v1.html(sample_html, height=400)
            
            # Send emails button
            if st.button("Send Emails", type="primary"):
                with st.spinner("Sending emails..."):
                    results = send_emails(
                        contacts_df,
                        selected_poc,
                        template_type
                    )
                    
                    st.session_state["email_results"] = results
                    
                    # Show results
                    st.success(f"✅ Successfully sent emails to {len(results['success'])} recipients")
                    if len(results['failed']) > 0:
                        st.error(f"❌ Failed to send emails to {len(results['failed'])} recipients")
                        
                    # Detailed results
                    with st.expander("View Detailed Results"):
                        if len(results['success']) > 0:
                            st.write("### Successfully Sent")
                            for email in results['success']:
                                st.write(f"- {email}")
                        
                        if len(results['failed']) > 0:
                            st.write("### Failed to Send")
                            for email, error in results['failed']:
                                st.write(f"- {email} - Error: {error}")
        
        except Exception as e:
            st.error(f"Error processing contact file: {e}")

# Main application
def main():
    show_header()
    initialize_session_state()
    
    # Load and initialize authentication
    authenticator = initialize_authentication()
    
    # Handle authentication status
    if st.session_state["authentication_status"] is not True:
        authentication_status = show_login_page(authenticator)
        st.session_state["authentication_status"] = authentication_status
    else:
        # Show logout button
        authenticator.logout('Logout', 'main')
        
        # Display main application
        show_main_page()

if __name__ == "__main__":
    main()
