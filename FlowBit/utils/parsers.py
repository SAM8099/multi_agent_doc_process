import json
import re

def extract_json(text: str) -> dict:
    text = text.strip()
    # Try to extract JSON object using regex
    match = re.search(r'\{[\s\S]*\}', text)
    if match:
        json_str = match.group(0)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON: {str(e)}"}
    else:
        return {"error": "No JSON object found in text"}

