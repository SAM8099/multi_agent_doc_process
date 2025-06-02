def make_json_serializable(obj):
    # If it's a list, process each item
    if isinstance(obj, list):
        return [make_json_serializable(item) for item in obj]
    # If it's an AIMessage or similar, extract .content
    if hasattr(obj, "content"):
        return obj.content
    # If it's a dict, process its values
    if isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    # If it's a primitive, return as is
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    # Fallback: convert to string
    return str(obj)