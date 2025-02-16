import logging
import requests
from bs4 import BeautifulSoup
from smolagents.tools import Tool

class VisitWebpageTool(Tool):
    name = "visit_webpage"
    description = "Visits a webpage and extracts its content. Especially useful for extracting job posting details."
    inputs = {
        'url': {
            'type': 'string',
            'description': 'The URL of the webpage to visit'
        }
    }
    output_type = "string"

    def forward(self, url: str) -> str:
        try:
            logging.info(f"Fetching content from URL: {url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Lever.co specific selectors
            if 'lever.co' in url:
                job_info = self._extract_lever_content(soup)
                if job_info:
                    return job_info
            
            # Try other common job board selectors
            selectors = [
                ('div', {'class': ['description', 'job-description', 'posting-description']}),
                ('div', {'class': 'posting-details'}),
                ('div', {'data-qa': 'job-description'}),
                ('section', {'class': ['job-description', 'description']}),
                ('article', {'class': ['job-details', 'description']}),
                ('main', {}),
                ('body', {})
            ]
            
            for tag, attrs in selectors:
                content = soup.find(tag, attrs)
                if content:
                    text = content.get_text(separator='\n', strip=True)
                    if text:
                        return text

            return "Job description not found"
            
        except Exception as e:
            logging.error(f"Error processing webpage: {str(e)}")
            return f"Error processing webpage: {str(e)}"

    def _extract_lever_content(self, soup: BeautifulSoup) -> str:
        try:
            content_parts = []
            
            # Get job title
            title = soup.find('div', {'class': 'posting-headline'})
            if title:
                content_parts.append(f"Position: {title.h2.get_text(strip=True)}")
            
            # Get company info
            company = soup.find('a', {'class': 'main-header-logo'})
            if company:
                content_parts.append(f"Company: {company.get('aria-label', '').strip()}")
            
            # Get job description
            description = soup.find('div', {'class': 'content-wrapper'})
            if description:
                sections = description.find_all(['div', 'h3'])
                for section in sections:
                    if section.name == 'h3':
                        content_parts.append(f"\n{section.get_text(strip=True)}:")
                    elif 'section-wrapper' in section.get('class', []):
                        content_parts.append(section.get_text(strip=True))

            if content_parts:
                return "\n\n".join(content_parts)
            return None

        except Exception as e:
            logging.error(f"Error extracting Lever.co content: {str(e)}")
            return None