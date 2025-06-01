from core.shared_memory import shared_memory
from core.groq_client import groq_completion
import re
import json
import logging
logger = logging.getLogger(__name__)



URGENCY_KEYWORDS = ["urgent", "immediate", "asap", "as soon as possible", "priority", "important", "critical"]

def detect_urgency(text: str) -> str:
    text_lower = text.lower()
    for keyword in URGENCY_KEYWORDS:
        if keyword in text_lower:
            return "High"
    return "Normal"

def email_agent(content: str, conversation_id: str, intent: str) -> dict:
    cleaned_content = re.sub(r'\s+', ' ', content)[:5000]
    context = shared_memory.get_last_extraction(conversation_id)
    
    system_prompt = (
        "You are an email processing expert. Extract key information. "
        f"Current intent: {intent}. Detect urgency based on keywords like: urgent, immediate, asap, priority. "
        "Output JSON with: sender, intent, urgency, topics, summary."
    )
    
    prompt = (
        f"Previous Context: {json.dumps(context, indent=2)[:1000]}\n\n"
        f"Email Content:\n{cleaned_content}\n\n"
        "Output JSON with keys: sender, intent, urgency, topics, summary."
    )
    
    try:
        raw = groq_completion(
            prompt, 
            system_prompt, 
            model="llama3-70b-8192",
            response_format="json"
        )
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            logger.warning("Email agent returned invalid JSON, using fallback urgency detection.")
            data = {"sender": None, "intent": intent, "urgency": detect_urgency(cleaned_content), "topics": [], "summary": ""}
        
        if "urgency" not in data or data.get("urgency", "").lower() in ["normal", "none", ""]:
            data["urgency"] = detect_urgency(cleaned_content)
        
        shared_memory.log(conversation_id, {
            "event_type": "agent_output",
            "agent": "Email_Agent",
            "input_intent": intent,
            "output": data
        })
        
        return data
    except Exception as e:
        logger.error(f"Email agent error: {e}")
        return {"error": str(e)}
