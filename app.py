from fastapi import FastAPI, UploadFile
from fastapi_mcp import FastApiMCP
from FlowBit.agents.classifier import classify_input
from FlowBit.agents.email_agent import process_email
from FlowBit.agents.json_agent import validate_json
from FlowBit.agents.pdf_agent import analyze_pdf_content
from FlowBit.core.memory import MemoryManager
from FlowBit.core.schemas import ActionRequest
from FlowBit.utils.json_serialize import make_json_serializable
from FlowBit.router.action_router import router as action_router, trigger_action
from fastapi.templating import Jinja2Templates
import logging
import os
from fastapi import Request
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

app = FastAPI()
app.include_router(action_router)
templates = Jinja2Templates(directory="templates")

mcp = FastApiMCP(
    app,
    include_operations=['process_input']  # Exposes only this endpoint as a tool
)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./memory.db")
memory = MemoryManager(db_url=DATABASE_URL)

def determine_action_type(classification: dict, result: dict) -> str:
    format_ = classification.get('format')
    intent = classification.get('intent')

    # Escalate: Complaint (with angry + urgent email)
    if format_ == 'Email':
        if intent == 'Complaint':
            if result.get('urgency', '').lower() == 'high' and result.get('tone', '').lower() == 'angry':
                return "crm_escalate"
            else:
                return "create_ticket"  # Routine for other complaints
        elif intent in ['Fraud Risk', 'Risk']:
            return "risk_alert"
        elif intent in ['RFQ', 'Invoice']:
            return "create_ticket"  # Routine
        else:
            return "create_ticket"

    elif format_ == 'PDF':
        if intent == 'Invoice':
            if result.get('total_amount') and float(result['total_amount']) > 10000:
                return "crm_escalate"
            return "create_ticket"  # Routine
        elif intent == 'RFQ':
            if result.get('product') and result.get('quantity'):
                return "create_ticket"  # Routine
            return "risk_alert"
        elif intent in ['Fraud Risk', 'Risk']:
            if result.get('anomalies') or any(flag.lower() in ['fraud', 'risk'] for flag in result.get('Compliance Flags', [])):
                return "risk_alert"
            return "create_ticket"
        elif intent == 'Complaint':
            # Escalate if angry and urgent even in PDF (rare, but for completeness)
            if result.get('urgency', '').lower() == 'high' and result.get('tone', '').lower() == 'angry':
                return "crm_escalate"
            return "create_ticket"
        else:
            return "create_ticket"

    elif format_ == 'JSON':
        if intent == 'Invoice':
            if result.get('total_amount') and float(result['total_amount']) > 10000:
                return "crm_escalate"
            return "create_ticket"  # Routine
        elif intent == 'RFQ':
            if result.get('product') and result.get('quantity'):
                return "create_ticket"  # Routine
            return "risk_alert"
        elif intent in ['Fraud Risk', 'Risk']:
            if result.get('anomalies') or any(flag.lower() in ['fraud', 'risk'] for flag in result.get('Compliance Flags', [])):
                return "risk_alert"
            return "create_ticket"
        elif intent == 'Complaint':
            if result.get('urgency', '').lower() == 'high' and result.get('tone', '').lower() == 'angry':
                return "crm_escalate"
            return "create_ticket"
        elif result.get('anomalies'):
            return "risk_alert"
        else:
            return "create_ticket"

    return "create_ticket"


@app.get("/", operation_id="index")
async def index(request: Request):
    logging.info("Welcome to FlowBit MCP API")
    return templates.TemplateResponse("home.html", {"request": request})

# Corrected page endpoints (changed to GET)
@app.get("/routine")
async def create_ticket_page(request: Request):
    return templates.TemplateResponse("routine.html", {"request": request})

@app.get("/escalate")
async def escalate_ticket_page(request: Request):
    return templates.TemplateResponse("escalate.html", {"request": request})

@app.get("/risk_alert")
async def risk_alert_page(request: Request):
    return templates.TemplateResponse("risk_alert.html", {"request": request})

@app.post("/uploads/", operation_id="process_input")
async def process_input(file: UploadFile):
    content = await file.read()
    classification = classify_input(content)
    logging.info(f"Raw content: {content[:100]}")
    logging.info(f"Classification: {classification}")
    try:
        if classification['format'] == 'Email':
            result = process_email(content.decode('utf-8', errors='replace'))
        elif classification['format'] == 'PDF':
            result = analyze_pdf_content(content)
        elif classification['format'] == 'JSON':
            decoded_content = content.decode('utf-8', errors='replace')
            if not decoded_content.strip():
                raise ValueError("Uploaded JSON file is empty.")
            try:
                result = validate_json(decoded_content, ["product", "quantity"])
            except Exception as e:
                raise ValueError(f"Invalid JSON format: {str(e)}")
        else:
            result = {}
        action_type = determine_action_type(classification, result)
        action_request = ActionRequest(
            action_type=action_type,
            payload={
                "classification": classification,
                "result": result
            }
        )
        action_response = await trigger_action(action_request)
        
        memory.log_interaction({
            "input_metadata": classification,
            "extracted_fields": make_json_serializable(result),
            "actions_triggered": make_json_serializable(action_response),
            "decision_trace": {"agent_flow": classification['format']}
        })
        return {
            "classification": classification,
            "result": result,
            "redirect_url": action_response.get("redirect_url") if isinstance(action_response, dict) else "/routine"
        }

    except Exception as e:
        logging.error(f"Processing error: {str(e)}")
        return {"error": str(e)}

@app.post("/routine")
async def create_ticket(request: Request, payload: dict):
    return templates.TemplateResponse(
        "routine.html",
        {"request": request, "payload": payload}  # Add request to context
    )

@app.post("/escalate")
async def escalate_ticket(request: Request, payload: dict):
    return templates.TemplateResponse(
        "escalate.html",
        {"request": request, "payload": payload}
    )

@app.post("/risk_alert")
async def risk_alert(request: Request, payload: dict):
    return templates.TemplateResponse(
        "risk_alert.html",
        {"request": request, "payload": payload}
    )

@app.post("/routine")
async def create_ticket(request: Request, payload: Optional[dict] = None):
    return templates.TemplateResponse("routine.html", {"request": request, "payload": payload})
mcp.mount(app)
