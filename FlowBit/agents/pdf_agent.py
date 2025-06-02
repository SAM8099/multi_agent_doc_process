from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from PyPDF2 import PdfReader
from FlowBit.utils.parsers import extract_json
import io
import os
import logging
from dotenv import load_dotenv
load_dotenv()
import sys
groq_api_key = os.getenv("GROQ_API_KEY")

def extract_pdf_text(pdf_bytes: bytes) -> str:
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        if not text.strip():
            raise ValueError("PDF text extraction failed: Empty content")
        return text
    except Exception as e:
        logging.error(f"PDF extraction error: {str(e)}")
        return ""

def analyze_pdf_content(pdf_bytes: bytes) -> dict:
    llm = ChatGroq(
        temperature=0,
        model_name="llama3-70b-8192",
        api_key=groq_api_key
    )
    prompt = ChatPromptTemplate.from_template(
        """Extract the following from the PDF text:
        - Document Type (Invoice/Policy/Other)
        - Key Entities
        - Compliance Flags (e.g., GDPR, FDA)
        - Total Amount (if invoice)

        Content: {content}
        Return ONLY valid JSON, no explanation, no markdown, no extra text."""
    )
    text = extract_pdf_text(pdf_bytes)
    chain = prompt | llm
    raw_output = chain.invoke({"content": text}).content
    print(raw_output)

    return extract_json(raw_output)
