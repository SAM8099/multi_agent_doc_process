<h1 style="font-size: 32px;">Multi-Format Autonomous AI System with Contextual Decisioning & Chained Actions</h1>

<p>The is a modular, multi-agent backend system built with FastAPI that classifies and processes uploaded documents (Email, JSON, PDF), extracts structured information using LLMs, triggers business actions, and logs all interactions.</p>

<p>It exposes its endpoints as MCP tools, making it AI-agent friendly and ready for automation or integration with AI copilots.</p>

<h2 style="font-size: 28px;">The project structure is given below:</h2>



�   app.py
�   Dockerfile
�   memory.db
�   README.md
�   requirements.txt
�   tree.txt
�   
+---FlowBit
�   �   logger.py
�   �   __init__.py
�   �   
�   +---agents
�   �   �   classifier.py
�   �   �   email_agent.py
�   �   �   json_agent.py
�   �   �   pdf_agent.py
�   �   �   __init__.py
�   �   �   
�   �           
�   +---core
�   �   �   memory.py
�   �   �   schemas.py
�   �   �   __init__.py
�   �   �   
�   �           
�   +---mcp
�   �       mcp-server.json
�   �       __init__.py
�   �       
�   +---router
�   �   �   action_router.py
�   �   �   __init__.py
�   �           
�   +---utils
�   �   �   fake_samples.py
�   �   �   json_serialize.py
�   �   �   parsers.py
�   �   �   __init__.py
�   �        
+---sample_data
�       sample_complaint.eml
�       sample_invoice.pdf
�       sample_rfq.json
�       sample_risk.pdf
�       sodapdf-converted.pdf
�       webhook_sample.json
�       
+---templates
�       escalate.html
�       home.html
�       risk_alert.html
�       routine.html
�       

<h1 style="font-size: 32px;">Component Explanations:</h1>

<h2 style="font-size: 28px;">1. app.py (Main Application)</h2>
<p><b>Purpose:</b> Entry point for FastAPI; wires together all routes, agents, templates, memory, and MCP.</p>

<h3 style="font-size: 24px;">Key Responsibilities:</h3>
<ol>
  <li>Handles file uploads (/uploads/)</li>
  <li>Serves HTML pages (home, routine, escalate, risk alert)</li>
  <li>Initializes MCP (Model Context Protocol) for AI agent integration</li>
  <li>Orchestrates document classification, agent processing, action routing, and memory logging</li>
</ol>

<h2 style="font-size: 28px;">2. FlowBit/agents/</h2>

<h3 style="font-size: 24px;">1. classifier.py</h3>
<p><b>Purpose:</b> Classifies uploaded content (Email, PDF, JSON) and detects intent (RFQ, Complaint, Invoice, Regulation, Fraud Risk).</p>
<p><b>How:</b> Uses an LLM (e.g., Groq/Llama3) with a prompt and examples to output a structured classification.</p>

<h3 style="font-size: 24px;">2. email_agent.py</h3>
<p><b>Purpose:</b> Extracts structured fields from emails (sender, urgency, main issue, tone).</p>
<p><b>How:</b> Sends email text to LLM and parses the JSON response.</p>

<h3 style="font-size: 24px;">3. pdf_agent.py</h3>
<p><b>Purpose:</b> Extracts text from PDFs, then uses LLM to extract document type, entities, compliance flags, total amount, etc.</p>
<p><b>How:</b> Uses pypdf for text extraction, LLM for information extraction.</p>

<h3 style="font-size: 24px;">4. json_agent.py</h3>
<p><b>Purpose:</b> Validates and extracts fields from JSON documents, checks for anomalies or required fields.</p>
<p><b>How:</b> Uses LLM to validate against a schema and flag missing fields.</p>

<h2 style="font-size: 28px;">3. FlowBit/core/</h2>

<h3 style="font-size: 24px;">1. memory.py</h3>
<p><b>Purpose:</b> Stores all interactions (input, extracted fields, triggered actions, decision trace) in a SQLite database for auditability and analytics.</p>
<p><b>How:</b> Uses SQLAlchemy ORM for database operations.</p>

<h3 style="font-size: 24px;">2. schemas.py</h3>
<p><b>Purpose:</b> Defines Pydantic models for structured data exchange (e.g., ActionRequest).</p>

<h2 style="font-size: 28px;">4. FlowBit/router/</h2>

<h3 style="font-size: 24px;">1. action_router.py</h3>
<p><b>Purpose:</b> Receives action requests (e.g., escalate, create ticket, risk alert) and routes them to the correct FastAPI endpoint or simulates external system calls.</p>
<p><b>How:</b> Implements logic for forwarding requests and returning responses, including redirect URLs.</p>

<h2 style="font-size: 28px;">5. FlowBit/utils/</h2>

<h3 style="font-size: 24px;">1. parsers.py</h3>
<p><b>Purpose:</b> Robustly extracts JSON from LLM outputs, handling code blocks, extra text, and malformed responses.</p>

<h3 style="font-size: 24px;">2. json_serialize.py</h3>
<p><b>Purpose:</b> Utility to ensure complex agent results are JSON-serializable before storage.</p>

<h3 style="font-size: 24px;">3. fake_samples.py</h3>
<p><b>Purpose:</b> Uses Faker library to generate webhook data for json files.</p>

<h2 style="font-size: 28px;">6. templates/</h2>
<p><b>Purpose:</b> Contains Jinja2 HTML files for home, routine, escalate, and risk alert pages.</p>
<p><b>How:</b> Rendered by FastAPI endpoints for user-friendly web pages.</p>

<h2 style="font-size: 28px;">7. FlowBit/mcp/</h2>
<p><b>Purpose :</b> It contains the MCP (Model Context Protocol) proxy server. It is stored in JSON format.</p>

<h2 style="font-size: 28px;">8. sample_data/</h2>
<p><b>Purpose:</b> Stores example files (PDFs, JSONs, emails) for testing and demos.</p>

<h2 style="font-size: 28px;">9. FlowBit/logger.py</h2>
<p><b>Purpose:</b> It is responsible for logging all the events which are happening when the app is working.</p>

<h2 style="font-size: 28px;">10. Dockerfile, .env, requirements.txt</h2>
<p><b>Purpose:</b> Enable containerized deployment, environment variable management, and dependency installation.</p>

<h1 style="font-size: 32px;">Flow of the Project</h1>

<h2 style="font-size: 28px;">Step-by-Step Flow</h2>
<ol>
  <li>User Uploads a File</li>
  <li>User visits the home page and uploads a file (PDF, Email, JSON) via the web UI.</li>
  <li><code>/uploads/</code> Endpoint Receives the File</li>
  <li>The file is sent to the <code>/uploads/</code> FastAPI endpoint as a POST request.</li>
  <li>Classification</li>
  <li>The classifier agent determines the file format and intent using the LLM.</li>
  <li>Agent Processing</li>
  <li>Based on classification:
    <ul>
      <li>Email: Processed by email_agent</li>
      <li>PDF: Processed by pdf_agent</li>
      <li>JSON: Processed by json_agent</li>
    </ul>
  </li>
  <li>Each agent extracts structured fields relevant to the format and intent.</li>
  <li>Action Routing
    <ul>
      <li>The <code>determine_action_type</code> function decides which business action to trigger (routine, escalate, risk alert) based on extracted fields and classification.</li>
    </ul>
  </li>
  <li>An <code>ActionRequest</code> is created and sent to the <code>action_router</code>.</li>
  <li>Action Execution</li>
  <li>The <code>action_router</code> calls the appropriate FastAPI endpoint or simulates an external system (e.g., creates a ticket, escalates a case, triggers a risk alert).</li>
  <li>Returns a redirect URL or response.</li>
  <li>Memory Logging
    <ul>
      <li>The entire interaction (input, extracted fields, action, decision trace) is logged in the database for traceability.</li>
    </ul>
  </li>
  <li>User Feedback
    <ul>
      <li>The user is redirected to a result page (routine, escalate, risk alert) or shown the result in the web UI.</li>
    </ul>
  </li>
  <li>MCP Exposure
    <ul>
      <li>All relevant endpoints are exposed as MCP tools, allowing AI agents to discover and use them programmatically.</li>
    </ul>
  </li>
</ol>

<h2 style="font-size: 28px;">How MCP Fits In:</h2>
<ol>
  <li>All endpoints (like <code>/uploads/</code>, <code>/routine</code>, <code>/escalate</code>, <code>/risk_alert</code>) are also available as MCP tools.</li>
  <li>AI agents can discover, describe, and call these endpoints automatically, enabling automation, integration, and AI-driven workflows.</li>
</ol>

