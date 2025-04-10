import openai
import os
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

async def analyze_document(text, document_type="general"):
    """
    Analyze document text using OpenAI's GPT models.
    
    Args:
        text: The extracted text from the document
        document_type: The type of document being analyzed (animal_boarding, shelter_plan, etc.)
    
    Returns:
        Structured analysis from the AI
    """
    # Check if API key is set
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    
    # Select prompt based on document type
    if document_type == "animal_boarding":
        system_prompt = "You are an expert in emergency animal boarding programs. Extract critical information including operational procedures, agreements, contact information, and legal requirements."
    elif document_type == "shelter_plan":
        system_prompt = "You are an expert in multi-community shelter planning. Extract critical information including facility details, resource allocation, staff requirements, and coordination procedures."
    else:
        system_prompt = "You are an emergency management documents expert. Extract operational procedures, agreements, checklists, contact info, animal shelter plans, and legal requirements."
    
    user_prompt = f"""Analyze this emergency management document and extract ALL critical, actionable information.
    Focus on:
    1. Key operational procedures and protocols
    2. Contact information and responsible parties
    3. Resource requirements and logistics
    4. Legal and compliance requirements
    5. Timeline and scheduling information
    
    Structure your response in clear sections with appropriate headings and bullet points where relevant.
    
    DOCUMENT CONTENT:
    {text[:8000]}  # Limiting to first 8000 chars - for larger docs, implement chunking
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,  # Lower temperature for more consistent results
            max_tokens=4000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return f"Error analyzing document: {str(e)}"

async def analyze_multiple_documents(documents_text, output_type="animal_boarding"):
    """
    Analyze multiple documents and merge the information into a cohesive output
    
    Args:
        documents_text: List of document text contents
        output_type: Type of output document to generate
    
    Returns:
        Merged analysis from the AI
    """
    if not documents_text:
        return "No documents provided for analysis"
    
    # First analyze each document individually
    individual_analyses = []
    for doc_text in documents_text:
        analysis = await analyze_document(doc_text, document_type=output_type)
        individual_analyses.append(analysis)
    
    # Create a summary prompt that merges the individual analyses
    merge_prompt = f"""You are creating a comprehensive emergency management plan.
    
    You've analyzed multiple documents and extracted the following information:
    
    {json.dumps(individual_analyses)}
    
    Create a unified document that merges all this information without repetition.
    Focus on creating a practical, actionable document structured with clear sections.
    Resolve any conflicting information by selecting the most comprehensive option.
    
    The output should be formatted as a professional {output_type.replace('_', ' ')} document.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in creating consolidated emergency management plans from multiple sources."},
                {"role": "user", "content": merge_prompt}
            ],
            temperature=0.3,
            max_tokens=4000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API for document merge: {e}")
        return f"Error merging documents: {str(e)}"
