import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from utils.template_utils import render_email_template
import random

def send_emails(contacts_df, poc_data, template_type):
    """Send emails to all contacts using the selected template and POC data"""
    
    # Get email credentials from Streamlit secrets
    email_sender = st.secrets["email"]["sender"]
    email_password = st.secrets["email"]["password"]
    
    # Track results
    results = {
        "success": [],
        "failed": []
    }
    
    # Configure email server
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_sender, email_password)
        
        # Batch processing to avoid rate limits
        batch_size = 50
        total_contacts = len(contacts_df)
        
        # Process in batches with progress bar
        progress_bar = st.progress(0)
        
        for i, (_, contact) in enumerate(contacts_df.iterrows()):
            try:
                # Prepare email data
                #poc_name = poc_data["POC_name"]
                #poc_first_name = poc_name.split([0]) if poc_name.strip() else ""

                email_data = {
                    "name": contact["name"],
                    "company": contact["company"],
                    "poc_name": poc_data["POC_name"],
                    #"poc_first_name": poc_first_name,
                    "poc_designation": poc_data["POC_designation"],
                    "poc_contact": poc_data["POC_contact"]
                }
                
                # Create message
                msg = MIMEMultipart()
                msg["From"] = "IDDD Placement Strategks" #email_sender
                msg["To"] = contact["email"]
                msg["Subject"] = f"Invitation to {contact['company']} for IDDD recruitment"
                
                # Render HTML email body
                html_content = render_email_template(template_type, email_data)
                msg.attach(MIMEText(html_content, "html"))
                
                # Send email
                server.send_message(msg)
                
                # Add to success list
                results["success"].append(contact["email"])
                
                # Update progress
                progress_bar.progress((i + 1) / total_contacts)
                
                # Add delay to avoid rate limiting
                delay = random.uniform(0.5, 3)
                time.sleep(delay)
                # if (i + 1) % 20 == 0:
                #    time.sleep(1)
                    
            except Exception as e:
                # Add to failed list
                results["failed"].append((contact["email"], str(e)))
                
        # Close connection
        server.quit()
        progress_bar.empty()
        
        return results
        
    except Exception as e:
        st.error(f"Error connecting to email server: {e}")
        return {
            "success": [],
            "failed": [(contact["email"], "Failed to connect to email server") 
                      for _, contact in contacts_df.iterrows()]
        }
