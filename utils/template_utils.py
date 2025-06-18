import os
from pathlib import Path
from jinja2 import Template, Environment, FileSystemLoader

def render_email_template(template_type, data):
    """Render an email template with the provided data"""
    
    templates_dir = Path("templates")
    env = Environment(loader=FileSystemLoader(templates_dir))
    
    # Select template based on type
    if template_type == "Analytics":
        template_file = "analytics.html"
    else:  # "Fin"
        template_file = "fin.html"
    
    try:
        # Load and render template
        template = env.get_template(template_file)
        rendered_html = template.render(**data)
        return rendered_html
        
    except Exception as e:
        raise ValueError(f"Error rendering email template: {e}")
