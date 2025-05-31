from agents.classifier_agent import classify_agent
from agents.email_agent import email_agent
from agents.json_agent import json_agent
from agents.pdf_agent import pdf_agent
from core.shared_memory import shared_memory
import json, time, hashlib
from typing import Union, Dict, Any

import logging

logger = logging.getLogger(__name__)


def process_input(input_data: Any, conversation_id: str = None, clear_memory: bool = False) -> dict:
    """Main orchestrator function"""
    if not conversation_id:
        conversation_id = hashlib.md5(str(time.time()).encode()).hexdigest()[:12]
    
    if clear_memory:
        shared_memory.clear_conversation(conversation_id)
    
    try:
        # Step 1: Classify input
        classification = classify_agent(input_data)
        fmt = classification.get("format", "Email")
        intent = classification.get("intent", "Other")
        
        # Step 2: Route to appropriate agent
        if fmt == "JSON":
            try:
                payload = json.loads(input_data) if isinstance(input_data, str) else input_data
            except (TypeError, json.JSONDecodeError):
                payload = {"raw_data": str(input_data)[:1000]}
            result = json_agent(payload, conversation_id, intent)
        elif fmt == "PDF":
            if not isinstance(input_data, bytes):
                input_data = input_data.encode()
            result = pdf_agent(input_data, conversation_id)
        else:  # Email or fallback
            content = input_data.decode() if isinstance(input_data, bytes) else str(input_data)
            result = email_agent(content, conversation_id, intent)
        
        # Step 3: Log to shared memory
        shared_memory.log(conversation_id, {
            "source": "user_input",
            "type": fmt,
            "intent": intent,
            "extracted_values": result
        })
        
        # Return concise result
        return {
            "conversation_id": conversation_id,
            "classification": classification,
            "result": result
        }
        
    except Exception as e:
        logger.exception(f"Processing failed: {e}")
        return {"error": str(e)}

def get_conversation_history(conversation_id: str) -> list:
    """Get conversation history for a specific ID"""
    return shared_memory.get_context(conversation_id)

def print_result(result: dict, title: str = "RESULT"):
    """Pretty print results"""
    print(f"\n=== {title} ===")
    print(json.dumps(result, indent=2))
    print()
