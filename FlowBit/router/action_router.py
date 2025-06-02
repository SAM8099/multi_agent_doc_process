from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import httpx
import os
import logging
from FlowBit.core.schemas import ActionRequest

router = APIRouter()
BASE_URL = os.getenv("ACTION_ROUTER_BASE_URL", "http://localhost:8000")

@router.post("/trigger-action")
async def trigger_action(request: ActionRequest):
    async def forward_and_return_redirect(post_endpoint: str, redirect_path: str, payload: dict):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{BASE_URL}{post_endpoint}", json=payload)
            if response.status_code in [200, 201]:
                return JSONResponse(status_code=200, content={"redirect_url": redirect_path})
            else:
                try:
                    content = response.json()
                except Exception:
                    content = {
                        "error": "Non-JSON response received",
                        "raw": response.text[:300]
                    }
                return JSONResponse(status_code=response.status_code, content=content)
        except Exception as e:
            logging.error(f"Forwarding failed: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={"error": str(e), "redirect_url": "/routine"}
            )

    if request.action_type == "create_ticket":
        return await forward_and_return_redirect("/routine", "/routine", request.payload)
    elif request.action_type == "crm_escalate":
        return await forward_and_return_redirect("/escalate", "/escalate", request.payload)
    elif request.action_type == "risk_alert":
        return await forward_and_return_redirect("/risk_alert", "/risk_alert", request.payload)
    elif request.action_type == "compliance_risk":
        # Just return the fallback redirect target
        return JSONResponse(status_code=200, content={"redirect_url": "/routine"})
    else:
        raise HTTPException(status_code=400, detail=f"Unknown action_type: {request.action_type}")
