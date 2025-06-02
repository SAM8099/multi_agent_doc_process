from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from FlowBit.utils.parsers import extract_json
import os

groq_api_key = os.getenv("GROQ_API_KEY")

def classify_input(input_data: bytes) -> dict:
    llm = ChatGroq(
        temperature=0,
        model_name="llama3-70b-8192",
        api_key=groq_api_key
    )
    prompt = ChatPromptTemplate.from_template(
        """Return valid JSON ONLY. Classify input:
        {{
            "format": "JSON|Email|PDF",
            "intent": "RFQ|Complaint|Invoice|Regulation|Fraud Risk"
        }}

        Examples:
        {{
            "input": "Urgent: Missing shipment details",
            "output": {{"format": "Email", "intent": "Complaint"}}
        }}
        {{
            "input": "Invoice No. INV-2024 with total amount $1500",
            "output": {{"format": "PDF", "intent": "Invoice"}}
        }}
        {{
            "input": "Company policy document regarding GDPR compliance",
            "output": {{"format": "PDF", "intent": "Regulation"}}
        }}
        {{
            "input": "Risk assessment report highlighting potential fraud cases",
            "output": {{"format": "PDF", "intent": "Fraud Risk"}}
        }}
        {{
            "input": "FDA compliance certificate for medical devices",
            "output": {{"format": "PDF", "intent": "Regulation"}}
        }}
        {{
            "input": "Annual compliance audit summary for 2024",
            "output": {{"format": "PDF", "intent": "Regulation"}}
        }}
        {{
            "input": "Invoice issued to Acme Corp for consulting services",
            "output": {{"format": "PDF", "intent": "Invoice"}}
        }}
        {{
            "input": "Subject: Request for quotation\\nBody: Could you send a quote for 500 units of Widget X?",
            "output": {{"format": "Email", "intent": "RFQ"}}
        }}
        {{
            "input": "Subject: Invoice attached\\nBody: Please find attached the invoice for your recent purchase.",
            "output": {{"format": "Email", "intent": "Invoice"}}
        }}
        {{
            "input": "Subject: Policy update\\nBody: We have updated our data privacy policy as per GDPR.",
            "output": {{"format": "Email", "intent": "Regulation"}}
        }}
        {{
            "input": "Subject: Suspicious activity detected\\nBody: There has been a potential fraud risk flagged on your account.",
            "output": {{"format": "Email", "intent": "Fraud Risk"}}
        }}
        {{
            "input": "Subject: Complaint about damaged goods\\nBody: The items received were damaged, please resolve this issue.",
            "output": {{"format": "Email", "intent": "Complaint"}}
        }}
        {{
            "input": "{{\\"product\\": \\"Widget\\", \\"quantity\\": 500}}",
            "output": {{"format": "JSON", "intent": "RFQ"}}
        }}
        {{
            "input": "{{\\"complaint\\": \\"Damaged goods\\", \\"order_id\\": 789}}",
            "output": {{"format": "JSON", "intent": "Complaint"}}
        }}
        {{
            "input": "{{\\"invoice_number\\": \\"INV-987\\", \\"total\\": 1500}}",
            "output": {{"format": "JSON", "intent": "Invoice"}}
        }}
        {{
            "input": "{{\\"regulation\\": \\"GDPR\\", \\"compliance_status\\": true}}",
            "output": {{"format": "JSON", "intent": "Regulation"}}
        }}
        {{
            "input": "{{\\"risk_type\\": \\"Fraud\\", \\"severity\\": \\"High\\"}}",
            "output": {{"format": "JSON", "intent": "Fraud Risk"}}
        }}
        {{
            "input": "{{\\"purchase_order\\": \\"PO-2024\\", \\"items\\": [\\"Item1\\"]}}",
            "output": {{"format": "JSON", "intent": "RFQ"}}
        }}

        Input: {input}
        Output:"""
    )
    try:
        text_content = input_data.decode('utf-8', errors='replace')
    except Exception:
        text_content = str(input_data)
    chain = prompt | llm
    raw_output = chain.invoke({"input": text_content}).content
    return extract_json(raw_output)
