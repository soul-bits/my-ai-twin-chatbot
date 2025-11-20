import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import gradio as gr
import requests

# ---------------------------------------------------------
# Setup
# ---------------------------------------------------------
load_dotenv(override=True)
client = OpenAI()

NAME = os.getenv("NAME")

# ---------------------------------------------------------
# Load sources
# ---------------------------------------------------------
# Summary text
with open("me/summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()

# LinkedIn PDF text
pdf_reader = PdfReader("me/linkedin.pdf")
linkedin_text = "".join(page.extract_text() or "" for page in pdf_reader.pages)

# ---------------------------------------------------------
# System prompt
# ---------------------------------------------------------
SYSTEM_PROMPT = f"""
You are {NAME}. You are answering questions on {NAME}'s website,
specifically about {NAME}'s career, background, skills, and experience.
Use the summary and LinkedIn profile provided below to answer questions
accurately and professionally. If you don't know the answer, invoke the `record_unknown_question` tool.

IMPORTANT:
- Do not make up an answer. If you don't know the answer, invoke the `record_unknown_question` tool.
- Do not hallucinate. If you don't know the answer, invoke the `record_unknown_question` tool.

Summary:
{summary}

LinkedIn Profile:
{linkedin_text}

Always speak as {NAME}.
"""

# ---------------------------------------------------------
# Push notification helper
# ---------------------------------------------------------
PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")

def push_message(msg: str):
    print(f"Push: {msg}")
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "user": PUSHOVER_USER,
            "token": PUSHOVER_TOKEN,
            "message": msg
        }
    )

# ---------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------
def record_unknown_question(question):
    push_message(f"Recording {question} asked that I couldn't answer")
    return {"recorded": "ok"}

tools = [
    {
        "type": "function",
        "function": {
            "name": "record_unknown_question",
            "description": "Record an unknown question that you couldn't answer",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"}
                },
                "required": ["question"],
                "additionalProperties": False
            }
        }
    }
]

# ---------------------------------------------------------
# Tool call handler
# ---------------------------------------------------------
def handle_tool_calls(tool_calls):
    """Handle tool calls and return results."""
    results = []
    for call in tool_calls:
        # Parse arguments
        if isinstance(call.function.arguments, str):
            args = json.loads(call.function.arguments)
        else:
            args = call.function.arguments
        
        # Execute the tool function
        tool_name = call.function.name
        if tool_name == "record_unknown_question":
            result = record_unknown_question(**args)
        else:
            result = {"recorded": "ok"}
        
        # Add tool result to messages
        results.append({
            "role": "tool",
            "content": json.dumps(result),
            "tool_call_id": call.id
        })
    return results

# ---------------------------------------------------------
# Chat function for Gradio
# ---------------------------------------------------------
def chat(message, history):
    # Build messages list
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # Add history (Gradio format is list of dicts)
    for msg in history:
        if isinstance(msg, dict):
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if content:  # Only add non-empty messages
                messages.append({"role": role, "content": content})
    
    # Add current user message
    messages.append({"role": "user", "content": message})
    
    # Loop until we get a final response (not a tool call)
    while True:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        choice = response.choices[0]
        
        # If model wants to call a tool
        if choice.finish_reason == "tool_calls":
            tool_calls = choice.message.tool_calls
            print(f"🔧 Tool called: {[call.function.name for call in tool_calls]}")
            # Add assistant message with tool calls
            messages.append(choice.message)
            # Execute tools and add results
            messages.extend(handle_tool_calls(tool_calls))
            # Continue loop to get final response
        else:
            # Got final response, return it
            content = choice.message.content
            return content if content else "I apologize, but I couldn't generate a response."

# ---------------------------------------------------------
# Launch UI
# ---------------------------------------------------------
gr.ChatInterface(chat, type="messages").launch()
