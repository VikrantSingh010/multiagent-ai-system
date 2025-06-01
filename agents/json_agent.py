from core.shared_memory import shared_memory
from core.groq_client import groq_completion
import json
import logging

logger = logging.getLogger(__name__)


def json_agent(payload: dict, conversation_id: str, intent: str) -> dict:
    context = shared_memory.get_last_extraction(conversation_id)
    
    system_prompt = (
        "You are a JSON processing expert. Extract data to match the target schema. "
        f"Current intent: {intent}. Flag anomalies/errors in 'anomalies' array."
    )
    
    prompt = (
        f"Previous Context: {json.dumps(context, indent=2)[:1000]}\n\n"
        f"Target Schema:\n- Fields vary based on intent: {intent}\n\n"
        f"Input JSON Payload:\n{json.dumps(payload, indent=2)[:3000]}\n\n"
        "Output JSON with keys: 'extracted_data' and 'anomalies'."
    )

    try:
        raw = groq_completion(prompt, system_prompt, response_format="json")
        data = json.loads(raw)
        
        # Log agent activity
        shared_memory.log(conversation_id, {
            "agent": "JSON_Agent",
            "input_intent": intent,
            "output": data
        })
        
        return data
    except Exception as e:
        logger.error(f"JSON agent error: {e}")
        return {"extracted_data": {}, "anomalies": [str(e)]}
