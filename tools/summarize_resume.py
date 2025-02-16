from typing import Dict
from smolagents.tools import Tool
import re

class SummarizeResumeTool(Tool):
    name = "summarize_resume"
    description = "Summarizes the provided resume text to extract important keywords and highlights."
    inputs = {
        'resume_text': {
            'type': 'string',
            'description': 'The full text of the resume to be summarized'
        }
    }
    output_type = "string"
    
    def forward(self, resume_text: str) -> str:
        """
        Summarizes the provided resume text to extract important sections.
        """
        sections = {
            'contact_info': '',
            'summary': '',
            'experience': '',
            'education': '',
            'skills': '',
            'projects': ''
        }
        
        current_section = 'summary'  # Default starting section
        lines = resume_text.split('\n')
        
        for line in lines:
            line = line.strip()
            lower_line = line.lower()
            
            # Detect section headers
            if any(keyword in lower_line for keyword in ['experience', 'work history']):
                current_section = 'experience'
                continue
            elif any(keyword in lower_line for keyword in ['education', 'academic']):
                current_section = 'education'
                continue
            elif any(keyword in lower_line for keyword in ['skills', 'technologies']):
                current_section = 'skills'
                continue
            elif any(keyword in lower_line for keyword in ['projects', 'portfolio']):
                current_section = 'projects'
                continue
            elif re.match(r'^.*@.*\..*$', line):  # Email detection
                current_section = 'contact_info'
            
            # Add content to current section
            if line:
                sections[current_section] += line + '\n'
        
        # Build summary
        summary = "Resume Summary:\n\n"
        
        if sections['contact_info']:
            summary += "Contact Information:\n" + sections['contact_info'] + "\n"
        if sections['experience']:
            summary += "Professional Experience:\n" + sections['experience'] + "\n"
        if sections['skills']:
            summary += "Technical Skills:\n" + sections['skills'] + "\n"
        if sections['education']:
            summary += "Education:\n" + sections['education'] + "\n"
        if sections['projects']:
            summary += "Notable Projects:\n" + sections['projects'] + "\n"
        
        return summary.strip()