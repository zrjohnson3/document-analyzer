import openai

openai.api_key = "sk-your-openai-key"

async def analyze_document(text):
    prompt = f"""Extract important details for animal emergency planning from the following text:

    {text}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
