from PyPDF2 import PdfReader
from io import BytesIO
from agents.classifier_agent import classify_agent
from agents.email_agent import email_agent
def pdf_agent(pdf_bytes: bytes, conversation_id: str) -> dict:
    """PDF Agent - Extracts text from PDF and processes it"""
    try:
        from PyPDF2 import PdfReader
        from io import BytesIO
        
        reader = PdfReader(BytesIO(pdf_bytes))
        text = ""
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"
            if len(text) > 10000:  # Limit extraction
                break
        
        # Classify content from text
        classification = classify_agent(text[:2000])
        intent = classification.get("intent", "Unknown")
        
        # Route to email agent for content extraction
        return email_agent(text, conversation_id, intent)
        
    except ImportError:
        logger.error("PyPDF2 required for PDF processing")
        return {"error": "PyPDF2 not installed"}
    except Exception as e:
        logger.exception("PDF processing failed")
        return {"error": str(e)}