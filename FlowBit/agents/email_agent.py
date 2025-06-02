from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

def process_email(email_text: str) -> dict:
    llm = ChatGroq(
        temperature=0,
        model_name="llama3-70b-8192",
        api_key=groq_api_key
    )
    prompt = ChatPromptTemplate.from_template(
        """Extract the following fields from the email:
        - Sender
        - Urgency (High/Medium/Low)
        - Main Issue or Request
        - Tone (Angry/Polite/Neutral)

        Email: {email}
        Return as JSON."""
    )
    chain = prompt | llm
    raw_output = chain.invoke({"email": email_text}).content
    from FlowBit.utils.parsers import extract_json
    return extract_json(raw_output)
