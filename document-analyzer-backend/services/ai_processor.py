import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

async def analyze_document(text):
    # Check if API key is set
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
        
    prompt = f"""Extract important details for animal emergency planning from the following text:

    {text}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
