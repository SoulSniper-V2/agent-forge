# 🔨 AgentForge

**Scaffold, deploy, and manage AI agents with one command.**

> Because waiting weeks to ship an AI agent is for corporate roadmaps, not chaos coders.

## ⚡ Quick Start

```bash
# Install
pip install agent-forge

# Forge an agent
agent-forge create my-chatbot --provider openai --type chat

# Deploy it
cd my-chatbot
cp .env.example .env
# Edit .env with your API keys
agent-forge deploy my-chatbot

# Stop it
agent-forge stop my-chatbot
```

## 🚀 Features

- **One-command scaffolding** - Generate complete agent projects in seconds
- **Multi-provider support** - OpenAI, Anthropic, Gemini out of the box
- **Docker deployment** - Production-ready containers with one command
- **FastAPI powered** - Built-in REST API for your agents
- **Developer-grade** - Proper architecture, tests, docs included

## 📦 Installation

```bash
# From source
git clone https://github.com/yourusername/agent-forge.git
cd agent-forge
pip install -e .
```

## 🎯 Usage

### Create an Agent

```bash
# Basic chat agent with OpenAI
agent-forge create translator --provider openai --type chat

# Tool-using agent with Anthropic
agent-forge create research-bot --provider anthropic --type tool

# Full agent with Gemini
agent-forge create assistant --provider gemini --type agent
```

### Deploy

```bash
# Docker deployment
agent-forge deploy my-agent

# Check logs
docker logs my-agent

# Stop
agent-forge stop my-agent
```

### List All Agents

```bash
agent-forge list
```

## 🏗️ Generated Structure

```
my-agent/
├── agent.py          # Core agent logic (FastAPI)
├── main.py           # Entry point
├── requirements.txt  # Dependencies
├── .env.example      # Environment template
├── Dockerfile        # Container config
├── docker-compose.yml
└── tests/
    └── test_agent.py
```

## 🔧 Configuration

Edit `.env` with your API keys:

```env
OPENAI_API_KEY=your-key-here
# Or
ANTHROPIC_API_KEY=your-key-here
# Or
GEMINI_API_KEY=your-key-here
```

## 🐳 Docker Commands

```bash
# Build
docker-compose build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Restart
docker-compose restart
```

## 🧪 Testing

```bash
pytest tests/ -v
```

## 📝 License

MIT - Build something cool.
