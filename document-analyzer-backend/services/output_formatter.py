from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os
from pathlib import Path
import time
from datetime import datetime
from dotenv import load_dotenv

# For PDF conversion
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import tempfile

# Load environment variables
load_dotenv()

# Get configuration from environment variables
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "storage/outputs")

def create_docx(extracted_text, filename, document_type="emergency_plan"):
    """
    Create a well-formatted DOCX file from extracted text
    
    Args:
        extracted_text: The analyzed text content
        filename: Base filename for the output
        document_type: Type of document (for styling)
    
    Returns:
        Path to the saved DOCX file
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    doc = Document()
    
    # Set document properties
    core_properties = doc.core_properties
    core_properties.author = "Document Analyzer"
    core_properties.title = filename.replace('_', ' ').title()
    core_properties.created = datetime.now()
    
    # Add styles
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(11)
    
    # Title page
    doc.add_heading(document_type.replace('_', ' ').upper(), 0)
    date_paragraph = doc.add_paragraph()
    date_paragraph.add_run(f"Generated: {datetime.now().strftime('%B %d, %Y')}")
    date_paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    
    doc.add_page_break()
    
    # Table of contents placeholder
    doc.add_heading("Table of Contents", 1)
    doc.add_paragraph("(Generated on export)")
    
    doc.add_page_break()
    
    # Process the extracted text - this is a simple implementation
    # For more complex parsing, you'd want to use a proper markdown parser
    sections = extracted_text.split('\n# ')
    
    # Handle the first section (or intro text)
    if sections and not sections[0].startswith('# '):
        intro_text = sections[0]
        doc.add_paragraph(intro_text)
        sections.pop(0)
    
    # Process remaining sections
    for section in sections:
        if section.strip():
            # Split into title and content
            lines = section.split('\n', 1)
            
            if len(lines) > 0:
                heading_text = lines[0].strip().replace('#', '').strip()
                doc.add_heading(heading_text, 1)
                
                if len(lines) > 1:
                    content = lines[1]
                    
                    # Process subsections
                    subsections = content.split('\n## ')
                    
                    # Handle first subsection or content
                    if subsections:
                        first_part = subsections[0]
                        if not first_part.startswith('## '):
                            paragraphs = first_part.split('\n\n')
                            for para in paragraphs:
                                if para.strip():
                                    # Check if it's a bullet point list
                                    if '\n- ' in para or para.startswith('- '):
                                        bullet_items = para.split('\n- ')
                                        for i, item in enumerate(bullet_items):
                                            if i == 0 and not item.startswith('- '):
                                                doc.add_paragraph(item)
                                            else:
                                                bullet_text = item.replace('- ', '', 1) if item.startswith('- ') else item
                                                doc.add_paragraph(bullet_text, style='List Bullet')
                                    else:
                                        doc.add_paragraph(para)
                    
                    # Process subsections
                    for i, subsection in enumerate(subsections):
                        if i == 0 and not subsection.startswith('## '):
                            continue  # Skip the first part that was already processed
                        
                        sub_lines = subsection.split('\n', 1)
                        if len(sub_lines) > 0:
                            sub_heading = sub_lines[0].strip().replace('##', '').strip()
                            doc.add_heading(sub_heading, 2)
                            
                            if len(sub_lines) > 1:
                                sub_content = sub_lines[1]
                                sub_paras = sub_content.split('\n\n')
                                for para in sub_paras:
                                    if para.strip():
                                        if '\n- ' in para or para.startswith('- '):
                                            bullet_items = para.split('\n- ')
                                            for j, item in enumerate(bullet_items):
                                                if j == 0 and not item.startswith('- '):
                                                    doc.add_paragraph(item)
                                                else:
                                                    bullet_text = item.replace('- ', '', 1) if item.startswith('- ') else item
                                                    doc.add_paragraph(bullet_text, style='List Bullet')
                                        else:
                                            doc.add_paragraph(para)
    
    # Save document
    timestamp = int(time.time())
    filename_safe = Path(filename).stem.replace(" ", "_")
    save_path = f"{OUTPUT_DIR}/{filename_safe}_{timestamp}.docx"
    doc.save(save_path)
    return save_path

def create_pdf_from_docx(docx_path):
    """
    Convert a DOCX file to PDF using WeasyPrint
    
    Args:
        docx_path: Path to the DOCX file
        
    Returns:
        Path to the generated PDF file
    """
    # This is a simplified implementation
    # For production, a more robust approach would be to use a dedicated conversion service
    # or to use docx2pdf library (which requires MS Word on Windows or LibreOffice on Linux)
    
    # Create a temporary HTML file from the document content
    pdf_path = docx_path.replace('.docx', '.pdf')
    
    # We'll create a simple HTML representation of the document
    # This is a very simplified approach - a production solution would use
    # a proper DOCX to HTML converter
    doc = Document(docx_path)
    html_content = "<html><head><style>body{font-family:Calibri;}</style></head><body>"
    
    for para in doc.paragraphs:
        if para.style.name.startswith('Heading'):
            level = para.style.name.replace('Heading', '')
            html_content += f"<h{level}>{para.text}</h{level}>"
        else:
            html_content += f"<p>{para.text}</p>"
    
    html_content += "</body></html>"
    
    # Use WeasyPrint to convert HTML to PDF
    font_config = FontConfiguration()
    html = HTML(string=html_content)
    css = CSS(string="@page { size: A4; margin: 1cm }")
    html.write_pdf(pdf_path, font_config=font_config, stylesheets=[css])
    
    return pdf_path

def generate_output_files(extracted_text, filename, formats=None):
    """
    Generate output files in the requested formats
    
    Args:
        extracted_text: Analyzed text content
        filename: Base filename
        formats: List of formats to generate (default: ["docx", "pdf"])
        
    Returns:
        Dictionary with paths to the generated files
    """
    if formats is None:
        formats = ["docx", "pdf"]
    
    output_files = {}
    
    if "docx" in formats:
        docx_path = create_docx(extracted_text, filename)
        output_files["docx"] = docx_path
    
    if "pdf" in formats and "docx" in output_files:
        # Generate PDF from the DOCX
        pdf_path = create_pdf_from_docx(output_files["docx"])
        output_files["pdf"] = pdf_path
    
    return output_files
