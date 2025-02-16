from typing import Dict
from smolagents.tools import Tool
from PyPDF2 import PdfReader
import os

class ExtractTextFromPdfTool(Tool):
    name = "extract_text_from_pdf"
    description = "Extracts text content from a PDF file"
    inputs = {
        'pdf_path': {
            'type': 'string',
            'description': 'The path to the PDF file'
        }
    }
    output_type = "string"
    
    def forward(self, pdf_path: str) -> str:
        """Extract all text from a PDF file."""
        if not os.path.exists(pdf_path):
            return f"Error: PDF file not found at path: {pdf_path}"
        
        try:
            reader = PdfReader(pdf_path)
            text = ""
            
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
            
            if not text:
                return "The PDF appears to be empty or contains no extractable text."
            
            return text.strip()
        except Exception as e:
            return f"Error extracting text from PDF: {str(e)}"