# agents/classify_agent.py

from core.groq_client import groq_completion
from typing import Union, Dict, Any
import json
import logging
from io import BytesIO
from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)

def is_json(content: str) -> bool:

    try:
        data = json.loads(content)
        return isinstance(data, dict)
    except json.JSONDecodeError:
        return False

def extract_text_from_pdf_bytes(pdf_bytes: bytes, max_chars: int = 2000) -> str:

    try:
        reader = PdfReader(BytesIO(pdf_bytes))
        all_text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                all_text.append(page_text)
        joined = "\n".join(all_text).strip()
        # Truncate in case the PDF is huge
        return joined[:max_chars]
    except Exception as e:
        logger.warning(f"[classify_agent] PDF text extraction error: {e}")
        return ""

def classify_agent(input_data: Union[str, bytes]) -> Dict[str, str]:


    if isinstance(input_data, bytes):
        
        raw = input_data.lstrip(b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09"
                                b"\x0A\x0B\x0C\x0D\x0E\x0F\x10\x11\x12"
                                b"\x13\x14\x15\x16\x17\x18\x19\x1A\x1B"
                                b"\x1C\x1D\x1E\x1F\x20")
        if raw.startswith(b"%PDF-"):
            # Extract text → call LLM for intent
            pdf_text = extract_text_from_pdf_bytes(input_data, max_chars=2000)
            if not pdf_text:
                # If extraction failed or was empty, return a default
                return {"format": "PDF", "intent": "Other"}

            system_prompt = (
                "Identify the intent of this PDF. "
                "Possible intents: Invoice, RFQ, Complaint, Regulation, Other. "
                "Return output strictly as JSON with a single key 'intent'."
            )
            prompt = f"PDF Text (truncated):\n{pdf_text}\n\nAnalysis:"

            try:
                raw_response = groq_completion(
                    prompt,
                    system_prompt,
                    response_format="json"
                )
                intent_obj = json.loads(raw_response)
                intent = intent_obj.get("intent", "Other")
            except Exception as e:
                logger.error(f"[classify_agent] LLM PDF intent classification failed: {e}")
                intent = "Other"

            return {"format": "PDF", "intent": intent}

    # --- STEP 2: If we reach here, it’s not a PDF (or PDF check failed) ---
    if isinstance(input_data, bytes):
        try:
            content = input_data.decode("utf-8")
        except UnicodeDecodeError:
            content = repr(input_data)
    else:
        content = input_data

    content_strip = content.strip()

    # --- STEP 3: Detect JSON vs. Email vs. Unknown ---
    if is_json(content_strip):
        fmt = "JSON"
    elif any(header in content_strip for header in ["From:", "Subject:", "Dear", "Regards", "To:"]):
        fmt = "Email"
    else:
        fmt = "Unknown"

    # --- STEP 4: For JSON/Email/Unknown, ask LLM for intent ---
    system_prompt = (
        "Identify the intent of this input. "
        "Possible intents: Invoice, RFQ, Complaint, Regulation, Other. "
        "Return output strictly as JSON with a single key 'intent'."
    )
    truncated = content_strip[:2000]
    prompt = f"Input:\n{truncated}\n\nAnalysis:"

    try:
        raw_response = groq_completion(
            prompt,
            system_prompt,
            response_format="json"
        )
        intent_obj = json.loads(raw_response)
        intent = intent_obj.get("intent", "Other")
    except Exception as e:
        logger.error(f"[classify_agent] LLM classification failed: {e}")
        intent = "Other"

    return {"format": fmt, "intent": intent}
