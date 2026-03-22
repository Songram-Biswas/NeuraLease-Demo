import pypdf
from typing import Optional

class PDFProcessor:
    @staticmethod
    async def extract_text(file_path: str) -> str:
        text = ""
        with open(file_path, "rb") as file:
            reader = pypdf.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text