import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("GEMINI_KEY")
if not api_key:
    raise ValueError("GEMINI_KEY environment variable not set")

# Configure the client
genai.configure(api_key=api_key)

# Use the model
model = genai.GenerativeModel('gemini-3.5-flash')
response = model.generate_content("Explain how AI works in a few words")
print(response.text)
