from agents.classifier_agent import classify_agent
from agents.email_agent import email_agent
from agents.json_agent import json_agent
from agents.pdf_agent import pdf_agent
from core.shared_memory import shared_memory
import json, time, hashlib
from typing import Any
import logging

from io import BytesIO
from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)

def is_pdf_empty(pdf_bytes: bytes) -> bool:
    try:
        reader = PdfReader(BytesIO(pdf_bytes))
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text.strip() == ""
    except Exception as e:
        logger.warning(f"PDF text extraction failed: {e}")
        return True

def process_input(input_data: Any, conversation_id: str = None, clear_memory: bool = False) -> dict:
    

    if not conversation_id:
        conversation_id = hashlib.md5(str(time.time()).encode()).hexdigest()[:12]

    if clear_memory:
        shared_memory.clear_conversation(conversation_id)

    try:
        # Step 1: Classify input
        classification = classify_agent(input_data)
        fmt = classification.get("format", "Email")
        intent = classification.get("intent", "Other")

        # Step 2: Validate empty inputs before agent processing
        if fmt == "PDF":
            pdf_bytes = input_data if isinstance(input_data, bytes) else input_data.encode()
            if len(pdf_bytes) < 10 or is_pdf_empty(pdf_bytes):
                logger.warning("Empty or invalid PDF content received.")
                return {
                    "conversation_id": conversation_id,
                    "classification": classification,
                    "result": {"error": "Please provide a valid PDF file."}
                }
            result = pdf_agent(pdf_bytes, conversation_id)

        elif fmt == "JSON":
            try:
                payload = json.loads(input_data) if isinstance(input_data, str) else input_data
                # Check if JSON is empty dict or empty list
                if not payload:
                    logger.warning("Empty JSON payload received.")
                    return {
                        "conversation_id": conversation_id,
                        "classification": classification,
                        "result": {"error": "Please provide a valid file."}
                    }
            except (TypeError, json.JSONDecodeError):
                logger.warning("Invalid JSON received.")
                return {
                    "conversation_id": conversation_id,
                    "classification": classification,
                    "result": {"error": "Please provide a valid file."}
                }
            result = json_agent(payload, conversation_id, intent)

        else:  # Email or fallback
            content = input_data.decode() if isinstance(input_data, bytes) else str(input_data)
            if content.strip() == "":
                logger.warning("Empty Email content received.")
                return {
                    "conversation_id": conversation_id,
                    "classification": classification,
                    "result": {"error": "Please provide a valid file."}
                }
            result = email_agent(content, conversation_id, intent)

       
        shared_memory.log(conversation_id, {
            "source": "user_input",
            "type": fmt,
            "intent": intent,
            "extracted_values": result
        })

        return {
            "conversation_id": conversation_id,
            "classification": classification,
            "result": result
        }

    except Exception as e:
        logger.exception(f"Processing failed: {e}")
        return {"error": str(e)}
