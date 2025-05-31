import os, json, time, logging
from groq import Groq
from typing import Union, Dict, Any


logger = logging.getLogger(__name__)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

def groq_completion(
    prompt: str,
    system: str = "",
    model: str = "llama3-70b-8192",
    response_format: str = None,
    max_retries: int = 3,
    timeout: int = 30,
) -> Any:
    if client is None:
        logger.error("Groq client not initialized.")
        raise RuntimeError("Groq client not available.")

    if response_format == "json" and "json" not in prompt.lower():
        prompt += "\n\nPlease respond in JSON format."

    messages = ([{"role": "system", "content": system}] if system else []) + [
        {"role": "user", "content": prompt}
    ]

    for attempt in range(1, max_retries + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.3,
                response_format={"type": "json_object"} if response_format == "json" else None,
                timeout=timeout,
            )
            content = response.choices[0].message.content
            return content
        except Exception as e:
            logger.warning(f"Groq completion failed (attempt {attempt}): {e}")
            time.sleep(2 ** attempt)
    logger.error("Groq completion failed after retries.")
    raise RuntimeError("Groq completion failed.")