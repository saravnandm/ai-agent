import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY missing in .env")

genai.configure(api_key=api_key)

def run_agent(user_input: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-2.0-flash-lite")
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print("🤖 Gemini AI Agent Started!")
    message = "Hello, who are you?"
    result = run_agent(message)
    print("User:", message)
    print("Agent:", result)