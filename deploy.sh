#!/bin/bash
# AgentForge Deploy Script
# One-command deployment for your AI agents

set -e

AGENT_NAME="${1:-}"
ENV_FILE=".env"

if [ -z "$AGENT_NAME" ]; then
    echo "Usage: ./deploy.sh <agent-name>"
    echo "Example: ./deploy.sh my-chatbot"
    exit 1
fi

if [ ! -d "$AGENT_NAME" ]; then
    echo "❌ Agent '$AGENT_NAME' not found. Create it first with: agent-forge create $AGENT_NAME"
    exit 1
fi

echo "🚀 Deploying agent: $AGENT_NAME"

# Check for .env
if [ ! -f "$AGENT_NAME/$ENV_FILE" ]; then
    echo "⚠️  No .env file found. Copying example..."
    cp "$AGENT_NAME/.env.example" "$AGENT_NAME/$ENV_FILE"
    echo "   ⚠️  EDIT $AGENT_NAME/$ENV_FILE WITH YOUR API KEYS!"
fi

# Deploy with docker-compose
cd "$AGENT_NAME"
docker-compose down 2>/dev/null || true
docker-compose up --build -d

echo ""
echo "✅ Agent '$AGENT_NAME' deployed!"
echo "   Health check: curl http://localhost:8000/health"
echo "   Logs: docker logs $AGENT_NAME -f"
