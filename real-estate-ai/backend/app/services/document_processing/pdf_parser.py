import pypdf
from typing import Optional
from fastapi import HTTPException

class PDFProcessor:
    @staticmethod
    async def extract_text_from_pdf(file_path: str) -> str:
        try:
            text = ""
            with open(file_path, "rb") as file:
                reader = pypdf.PdfReader(file)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            if not text.strip():
                raise ValueError("PDF is empty or contains only images (OCR might be needed).")
                
            return text
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")