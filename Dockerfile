FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code, templates, and sample data
COPY app.py .
COPY FlowBit ./FlowBit
COPY templates ./templates
COPY sample_data ./sample_data
COPY .env .env

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
