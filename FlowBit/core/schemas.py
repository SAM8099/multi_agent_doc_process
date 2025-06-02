from pydantic import BaseModel
from typing import Optional, Dict, Any

class InputMetadata(BaseModel):
    source: str
    format: str
    intent: str
    timestamp: str

class ActionRequest(BaseModel):
    action_type: str
    payload: dict
    
