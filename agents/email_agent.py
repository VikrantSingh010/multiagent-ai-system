from core.shared_memory import shared_memory
from core.groq_client import groq_completion
import re
import json


def email_agent(content: str, conversation_id: str, intent: str) -> dict:
    """Email Agent - Processes email/text content"""
    # Clean and truncate email content
    cleaned_content = re.sub(r'\s+', ' ', content)[:5000]
    context = shared_memory.get_last_extraction(conversation_id)
    
    system_prompt = (
        "You are an email processing expert. Extract key information. "
        f"Current intent: {intent}. Output JSON with: sender, intent, urgency, topics, summary."
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
        data = json.loads(raw)
        
        # Log agent activity
        shared_memory.log(conversation_id, {
            "agent": "Email_Agent",
            "input_intent": intent,
            "output": data
        })
        
        return data
    except Exception as e:
        logger.error(f"Email agent error: {e}")
        return {"error": str(e)}