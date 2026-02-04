"""{{ name }} - AI Agent Core"""

import os
from typing import List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
{% if provider == "openai" -%}
from openai import OpenAI
{% elif provider == "anthropic" -%}
from anthropic import Anthropic
{% elif provider == "gemini" -%}
import google.generativeai as genai
{% endif %}

# Agent Configuration
AGENT_NAME = os.getenv("AGENT_NAME", "{{ name }}")
{% if provider == "openai" -%}
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
{% elif provider == "anthropic" -%}
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
{% elif provider == "gemini" -%}
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
{% endif %}

# Pydantic Models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Message]] = []

class ChatResponse(BaseModel):
    response: str
    agent: str

class {{ name.title().replace('_', '') }}Agent:
    """AI Agent with {{ provider }} provider"""
    
    def __init__(self):
        self.app = FastAPI(
            title=f"{AGENT_NAME} API",
            description=f"AI Agent powered by {{ provider }}",
            version="0.1.0"
        )
        self.setup_routes()
        self.conversation_history: List[dict] = []
    
    def setup_routes(self):
        """Setup FastAPI routes"""
        
        @self.app.get("/")
        async def root():
            return {
                "agent": AGENT_NAME,
                "provider": "{{ provider }}",
                "type": "{{ agent_type }}",
                "status": "alive"
            }
        
        @self.app.get("/health")
        async def health():
            return {"status": "healthy"}
        
        @self.app.post("/chat", response_model=ChatResponse)
        async def chat(request: ChatRequest):
            """Chat with the agent"""
            try:
                response = self._generate_response(request.message, request.history)
                return ChatResponse(response=response, agent=AGENT_NAME)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/clear")
        async def clear_history():
            """Clear conversation history"""
            self.conversation_history = []
            return {"status": "cleared"}
    
    def _generate_response(self, message: str, history: List[Message]) -> str:
        """Generate AI response"""
        {% if provider == "openai" -%}
        messages = [{"role": msg.role, "content": msg.content} for msg in history]
        messages.append({"role": "user", "content": message})
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=1024
        )
        return response.choices[0].message.content
        {% elif provider == "anthropic" -%}
        prompt = "\n".join([f"{msg.role}: {msg.content}" for msg in history])
        prompt += f"\n\nHuman: {message}\n\nAssistant:"
        
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            prompt=prompt
        )
        return response.content[0].text
        {% elif provider == "gemini" -%}
        model = genai.GenerativeModel("gemini-pro")
        chat = model.start_chat(history=[])
        response = chat.send_message(message)
        return response.text
        {% endif %}
    
    def run(self):
        """Run the agent server"""
        import uvicorn
        uvicorn.run(self.app, host="0.0.0.0", port=8000)
