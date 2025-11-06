import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv
import re
import requests

from core.db import save_message, get_recent_messages, count_messages, clear_user_history
from core.tools import get_time, get_weather, calculate, get_aqi

load_dotenv()
logger = logging.getLogger(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.0-flash-lite"
SHORT_TERM_LIMIT = 10
SUMMARIZE_THRESHOLD = 20

genai.configure(api_key=API_KEY)


def extract_city_from_message(message: str):
    """Extract city name from a user message."""
    match = re.search(r"in ([A-Za-z\s]+)", message, re.IGNORECASE)
    if match:
        city = match.group(1).strip().rstrip("?.,")
        return city
    return None


def get_city_from_ip():
    """
    Detect city from user's public IP address using ipapi.co.
    Returns 'Bengaluru' if detection fails.
    """
    try:
        ip_resp = requests.get("https://ipapi.co/json/", timeout=3)
        if ip_resp.status_code == 200:
            data = ip_resp.json()
            city = data.get("city")
            if city:
                return city
    except Exception as e:
        logger.warning("IP-based city detection failed: %s", e)
    return "Bengaluru"  # default fallback


def generate_agent_reply(user_id: str, user_message: str):
    """Core reasoning logic of the Agent AI assistant."""
    lower_msg = user_message.lower().strip()

    # --- WEATHER ---
    if "weather" in lower_msg:
        city = extract_city_from_message(user_message) or get_city_from_ip()
        reply = get_weather(city)
        save_message(user_id, "assistant", reply)
        return reply

    # --- AQI ---
    if "aqi" in lower_msg or "air quality" in lower_msg:
        city = extract_city_from_message(user_message) or get_city_from_ip()
        reply = get_aqi(city)
        save_message(user_id, "assistant", reply)
        return reply

    # --- TIME ---
    if "time" in lower_msg or "date" in lower_msg:
        reply = get_time()
        save_message(user_id, "assistant", reply)
        return reply

    # --- CALCULATOR ---
    if any(op in lower_msg for op in ["+", "-", "*", "/", "sqrt"]):
        reply = calculate(user_message)
        save_message(user_id, "assistant", reply)
        return reply

    # --- GEMINI FALLBACK ---
    model = genai.GenerativeModel(MODEL_NAME)
    history = get_recent_messages(user_id, limit=SHORT_TERM_LIMIT)

    # Format conversation more naturally
    conversation = ""
    for role, content in history:
        if role in ["user", "assistant"]:
            conversation += f"{role.capitalize()}: {content}\n"

    # Summarize if message count exceeds threshold
    total = count_messages(user_id)
    if total > SUMMARIZE_THRESHOLD:
        summary_prompt = f"Summarize the key facts from this conversation:\n\n{conversation}"
        try:
            resp = model.generate_content(summary_prompt)
            summary_text = resp.text.strip()
            clear_user_history(user_id)
            save_message(user_id, "system", f"Summary so far: {summary_text}")
            conversation = f"System: Summary so far: {summary_text}\n"
        except Exception as e:
            logger.warning("Summarization failed: %s", e)

    # Build prompt for Gemini
    prompt = f"""
You are a friendly AI assistant having a casual, helpful chat with the user.
Here’s the recent conversation:

{conversation}
User: {user_message}
Assistant:"""

    # Generate response
    try:
        resp = model.generate_content(prompt)
        reply = resp.text.strip() if resp and resp.text else "I'm here, but I couldn’t generate a proper reply right now."
    except Exception as e:
        logger.exception("Gemini error: %s", e)
        reply = "There was an issue generating my response. Please try again."

    # Save messages to DB
    save_message(user_id, "user", user_message)
    save_message(user_id, "assistant", reply)

    return reply
