from PyPDF2 import PdfReader
from io import BytesIO
from agents.classifier_agent import classify_agent
from agents.email_agent import email_agent
import logging
logger = logging.getLogger(__name__)
def pdf_agent(pdf_bytes: bytes, conversation_id: str) -> dict:
    try:
        from PyPDF2 import PdfReader
        from io import BytesIO
        
        reader = PdfReader(BytesIO(pdf_bytes))
        text = ""
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"
            if len(text) > 10000: 
                break
        
        
        classification = classify_agent(text[:2000])
        intent = classification.get("intent", "Unknown")
        
        return email_agent(text, conversation_id, intent)
        
    except ImportError:
        logger.error("PyPDF2 required for PDF processing")
        return {"error": "PyPDF2 not installed"}
    except Exception as e:
        logger.exception("PDF processing failed")
        return {"error": str(e)}