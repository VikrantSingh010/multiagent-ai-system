from core.groq_client import groq_completion
from typing import Union, Dict, Any
import json
import logging

logger = logging.getLogger(__name__)

def is_json(content: str) -> bool:
    try:
        data = json.loads(content)
        return isinstance(data, dict)
    except json.JSONDecodeError:
        return False

def classify_agent(input_data: Union[str, bytes]) -> dict:


    if isinstance(input_data, bytes) and input_data.startswith(b'%PDF'):
        return {"format": "PDF", "intent": "Unknown"}
    
    if isinstance(input_data, bytes):
        try:
            content = input_data.decode('utf-8')
        except UnicodeDecodeError:
            content = str(input_data)
    else:
        content = str(input_data)


    if is_json(content):
        fmt = "JSON"
    elif "From:" in content or "Subject:" in content or "Dear" in content:
        fmt = "Email"
    else:
        fmt = "Unknown"

    system_prompt = (
        "Identify the intent of this input. "
        "Possible intents: Invoice, RFQ, Complaint, Regulation, Other. "
        "Output JSON with key: 'intent'"
    )
    prompt = f"Input:\n{content[:2000]}\n\nAnalysis:"

    try:
        raw = groq_completion(prompt, system_prompt, response_format="json")
        intent_result = json.loads(raw)
        return {
            "format": fmt,
            "intent": intent_result.get("intent", "Other")
        }
    except Exception as e:
        logger.error(f"Classification error: {e}")
        return {
            "format": fmt,
            "intent": "Other"
        }
