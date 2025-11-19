from __future__ import annotations

import os

import uvicorn
from agent_framework import ChatClientProtocol
from azure.identity import DefaultAzureCredential
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework.openai import OpenAIChatClient
from agent_framework.ag_ui import add_agent_framework_fastapi_endpoint
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware

from agent import create_agent

load_dotenv()

def _build_chat_client() -> ChatClientProtocol:
    try:
        if bool(os.getenv("AZURE_OPENAI_ENDPOINT")):
            # Azure OpenAI setup - uses environment variables by default
            # Optionally can pass deployment_name explicitly
            deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "gpt-4o-mini")
            return AzureOpenAIChatClient(
                credential=DefaultAzureCredential(),
                deployment_name=deployment_name,
                endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            )

        if bool(os.getenv("OPENAI_API_KEY")):
            # OpenAI setup - requires explicit model_id and api_key
            return OpenAIChatClient(
                model_id=os.getenv("OPENAI_CHAT_MODEL_ID", "gpt-4o-mini"),
                api_key=os.getenv("OPENAI_API_KEY"),
            )

        raise ValueError("Either AZURE_OPENAI_ENDPOINT or OPENAI_API_KEY environment variable is required")

    except Exception as exc:  # pragma: no cover
        raise RuntimeError(
            "Unable to initialize the chat client. Double-check your API credentials as documented in README.md."
        ) from exc


chat_client = _build_chat_client()
my_agent = create_agent(chat_client)

app = FastAPI(title="CopilotKit + Microsoft Agent Framework (Python)")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REQUIRED_BEARER_TOKEN = os.getenv("AUTH_BEARER_TOKEN")

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    # Protect the AG-UI endpoint if a token is configured
    if REQUIRED_BEARER_TOKEN and request.url.path == "/":
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
        token = auth_header.split(" ", 1)[1].strip()
        if token != REQUIRED_BEARER_TOKEN:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return await call_next(request)

add_agent_framework_fastapi_endpoint(
    app=app,
    agent=my_agent,
    path="/",
)


if __name__ == "__main__":
    host = os.getenv("AGENT_HOST", "0.0.0.0")
    port = int(os.getenv("AGENT_PORT", "8000"))
    uvicorn.run("main:app", host=host, port=port, reload=True)
