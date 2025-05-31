from core.groq_client import groq_completion
from typing import Union, Dict, Any
import json


import logging

logger = logging.getLogger(__name__)

def classify_agent(input_data: Union[str, bytes]) -> dict:
    """Classifier Agent - Determines format and intent"""
    # Check for PDF magic number
    if isinstance(input_data, bytes) and input_data.startswith(b'%PDF'):
        return {"format": "PDF", "intent": "Unknown"}
    
    # Convert bytes to string if needed
    if isinstance(input_data, bytes):
        try:
            content = input_data.decode('utf-8')[:2000]
        except UnicodeDecodeError:
            content = str(input_data)[:2000]
    else:
        content = str(input_data)[:2000]

    system_prompt = (
        "Classify input into format (PDF, JSON, Email) and intent "
        "(Invoice, RFQ, Complaint, Regulation, Other). Output JSON with keys: 'format', 'intent'."
    )
    prompt = f"Input:\n{content}\n\nAnalysis:"
    try:
        raw = groq_completion(prompt, system_prompt, response_format="json")
        result = json.loads(raw)
        return result
    except Exception as e:
        logger.error(f"Classification error: {e}")
        return {"format": "Email", "intent": "Other"}