from typing import Dict
from smolagents.tools import Tool
import re
import json
from datetime import datetime

class GenerateCoverLetterTool(Tool):
    name = "generate_cover_letter"
    description = "Generates a professional cover letter by combining resume summary and job details."
    inputs = {
        'resume_summary': {
            'type': 'string',
            'description': 'The summarized resume information'
        },
        'job_details': {
            'type': 'string',
            'description': 'The job posting details and requirements'
        }
    }
    output_type = "string"
    
    def forward(self, resume_summary: str, job_details: str) -> str:
        """Generates a cover letter."""
        if not resume_summary or resume_summary == "None":
            return "Error: Resume summary is missing or invalid."
        if not job_details or job_details == "Job description not found":
            return "Error: Job details are missing or invalid."
        
        try:
            resume_data = json.loads(resume_summary)
        except json.JSONDecodeError:
            resume_data = {
                'personal_info': self._extract_personal_info(resume_summary),
                'experience': self._extract_experience(resume_summary),
                'skills': self._extract_skills(resume_summary),
                'key_achievements': self._extract_achievements(resume_summary)
            }
        
        cover_letter = (
            f"{self._format_header(resume_data)}\n\n"
            f"{self._format_date()}\n\n"
            f"{self._format_recipient(job_details)}\n\n"
            f"Subject: {self._extract_position(job_details)} position\n\n"
            f"Dear {self._extract_hiring_manager(job_details)},\n\n"
            f"{self._generate_opener(job_details, resume_data)}\n\n"
            f"{self._format_qualifications(resume_data, job_details)}\n\n"
            f"{self._format_achievements(resume_data, job_details)}\n\n"
            f"{self._format_culture_fit(job_details)}\n\n"
            f"I look forward to the opportunity to discuss how my skills and experience align "
            f"with {self._extract_company(job_details)}'s needs in more detail.\n\n"
            f"Thank you for considering my application.\n\n"
            f"Sincerely,\n"
            f"{resume_data.get('personal_info', {}).get('name', '[Your Name]')}"
        )
        return cover_letter
    
    # Helper methods would be implemented here...
    def _extract_personal_info(self, text: str) -> dict:
        email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        phone_pattern = r'\+?[\d\s-]{10,}'
        email = re.search(email_pattern, text)
        phone = re.search(phone_pattern, text)
        return {
            'name': text.split('\n')[0] if text else '[Your Name]',
            'email': email.group(0) if email else '[Your Email]',
            'phone': phone.group(0) if phone else '[Your Phone]',
            'address': '[Your Address]'
        }
    
    def _format_header(self, resume_data: dict) -> str:
        personal_info = resume_data.get('personal_info', {})
        return (
            f"{personal_info.get('name', '[Your Name]')}\n"
            f"{personal_info.get('email', '[Your Email]')}\n"
            f"{personal_info.get('phone', '[Your Phone]')}\n"
            f"{personal_info.get('address', '[Your Address]')}"
        )
    
    def _format_date(self) -> str:
        return datetime.now().strftime("%B %d, %Y")
    
    # Additional helper methods would be implemented here...
    def _format_recipient(self, job_details: str) -> str:
        company = self._extract_company(job_details)
        manager = self._extract_hiring_manager(job_details)
        return f"{company}\nAttn: {manager}\n[Company Address]"
    
    def _extract_position(self, job_details: str) -> str:
        # Implementation would go here
        return "Position" 
    
    def _extract_hiring_manager(self, job_details: str) -> str:
        # Implementation would go here
        return "Hiring Manager"
    
    def _generate_opener(self, job_details: str, resume_data: dict) -> str:
        # Implementation would go here
        return "I am writing to express my interest in the position."
    
    def _format_qualifications(self, resume_data: dict, job_details: str) -> str:
        # Implementation would go here
        return "My qualifications include..."
    
    def _format_achievements(self, resume_data: dict, job_details: str) -> str:
        # Implementation would go here
        return "Throughout my career, I have achieved..."
    
    def _format_culture_fit(self, job_details: str) -> str:
        # Implementation would go here
        return "I am particularly drawn to your company because..."
    
    def _extract_company(self, job_details: str) -> str:
        # Implementation would go here
        return "Company"
    
    def _extract_experience(self, text: str) -> str:
        # Implementation would go here
        return ""
    
    def _extract_skills(self, text: str) -> list:
        # Implementation would go here
        return []
    
    def _extract_achievements(self, text: str) -> list:
        # Implementation would go here
        return []