from openai import OpenAI
import os
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable is not set")

    # Select prompt based on document type
    if document_type == "animal_boarding":
        system_prompt = """You are an expert in emergency animal boarding programs. Your task is to analyze and structure the document content into a clear, well-organized format.

Format your response using markdown with the following structure:
# [Document Title]

## Executive Summary
[2-3 paragraph overview of key points]

## Key Information
- [Bullet points of critical information]

## Operational Procedures
### [Procedure Name]
- Step-by-step instructions
- Required resources
- Safety considerations

## Contact Information
### Primary Contacts
- [Name/Role]: [Contact details]
- [Name/Role]: [Contact details]

## Resource Requirements
### Equipment
- [List of required equipment]
### Supplies
- [List of required supplies]
### Staffing
- [Staff requirements and roles]

## Legal Requirements
- [List of legal requirements and compliance items]

## Timeline
- [Key dates and milestones]

Format all sections with clear headings (use # for main sections, ## for subsections)
Use bullet points (-) for lists
Use bold (**text**) for emphasis on critical information
Use italics (*text*) for supplementary information"""
    elif document_type == "shelter_plan":
        system_prompt = """You are an expert in multi-community shelter planning. Your task is to analyze and structure the document content into a clear, well-organized format.

Format your response using markdown with the following structure:
# [Document Title]

## Executive Summary
[2-3 paragraph overview of key points]

## Facility Details
### Location
- [Address and access information]
### Capacity
- [Number of people/animals]
- [Space requirements]

## Resource Allocation
### Staffing
- [Required staff and roles]
### Equipment
- [List of required equipment]
### Supplies
- [List of required supplies]

## Coordination Procedures
### Communication
- [Communication protocols]
### Transportation
- [Transportation arrangements]
### Security
- [Security measures]

## Emergency Protocols
- [Emergency response procedures]
- [Evacuation plans]

Format all sections with clear headings (use # for main sections, ## for subsections)
Use bullet points (-) for lists
Use bold (**text**) for emphasis on critical information
Use italics (*text*) for supplementary information"""
    else:
        system_prompt = """You are an emergency management documents expert. Your task is to analyze and structure the document content into a clear, well-organized format.

Format your response using markdown with the following structure:
# [Document Title]

## Executive Summary
[2-3 paragraph overview of key points]

## Key Components
- [Bullet points of critical information]

## Operational Procedures
### [Procedure Name]
- Step-by-step instructions
- Required resources
- Safety considerations

## Contact Information
- [List of key contacts and roles]

## Resource Requirements
- [List of required resources]

## Legal Requirements
- [List of legal requirements and compliance items]

## Timeline
- [Key dates and milestones]

Format all sections with clear headings (use # for main sections, ## for subsections)
Use bullet points (-) for lists
Use bold (**text**) for emphasis on critical information
Use italics (*text*) for supplementary information"""

    user_prompt = f"""Analyze this emergency management document and extract ALL critical, actionable information.
    Focus on:
    1. Key operational procedures and protocols
    2. Contact information and responsible parties
    3. Resource requirements and logistics
    4. Legal and compliance requirements
    5. Timeline and scheduling information
    
    Structure your response in clear sections with appropriate headings and bullet points where relevant.
    Use markdown formatting for better readability.
    
    DOCUMENT CONTENT:
    {text[:8000]}  # Limiting to first 8000 chars - for larger docs, implement chunking
    """

    try:
        response = client.chat.completions.create(model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,  # Lower temperature for more consistent results
        max_tokens=4000)
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
        response = client.chat.completions.create(model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in creating consolidated emergency management plans from multiple sources."},
            {"role": "user", "content": merge_prompt}
        ],
        temperature=0.3,
        max_tokens=4000)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API for document merge: {e}")
        return f"Error merging documents: {str(e)}"
