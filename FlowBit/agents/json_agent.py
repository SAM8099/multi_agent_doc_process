from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

def validate_json(json_text: str, schema: list) -> dict:
    llm = ChatGroq(
        temperature=0,
        model_name="llama3-70b-8192",
        api_key=groq_api_key
    )
    prompt = ChatPromptTemplate.from_template(
        """Validate the following JSON against the required fields: {required_fields}.
        Flag any missing fields or type errors.
        Input: {json_data}
        Return anomalies and validation result as JSON."""
    )
    chain = prompt | llm
    raw_output = chain.invoke({
        "json_data": json_text,
        "required_fields": ", ".join(schema)
    }).content
    from FlowBit.utils.parsers import extract_json
    return extract_json(raw_output)
