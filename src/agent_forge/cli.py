#!/usr/bin/env python3
"""
AgentForge CLI - Spawn AI agents in seconds, not hours.
"""
import sys
import os
from pathlib import Path
from datetime import datetime

import click
from jinja2 import Environment, FileSystemLoader

@click.group()
def main():
    """AgentForge - AI Agent Scaffolding CLI"""
    pass

@main.command()
@click.argument("name")
@click.option("--provider", default="openai", type=click.Choice(["openai", "anthropic", "gemini"]))
@click.option("--type", "agent_type", default="chat", type=click.Choice(["chat", "tool", "agent"]))
@click.option("--docker/--no-docker", default=True)
def create(name: str, provider: str, agent_type: str, docker: bool):
    """Create a new AI agent scaffold"""
    
    target_dir = Path(name)
    if target_dir.exists():
        click.echo(f"❌ Directory '{name}' already exists!")
        sys.exit(1)
    
    target_dir.mkdir(parents=True)
    click.echo(f"🚀 Forging agent '{name}'...")
    
    # Setup templates
    template_dir = Path(__file__).parent / "templates"
    env = Environment(loader=FileSystemLoader(str(template_dir)))
    
    # Generate files
    files = [
        ("__init__.py", "__init__.py"),
        ("main.py", "main.py"),
        ("agent.py", "agent.py"),
        ("requirements.txt", "requirements.txt"),
        (".env.example", ".env.example"),
    ]
    
    if docker:
        files.append(("Dockerfile", "Dockerfile"))
        files.append(("docker-compose.yml", "docker-compose.yml"))
    
    context = {
        "name": name,
        "provider": provider,
        "agent_type": agent_type,
        "timestamp": datetime.now().isoformat(),
    }
    
    for filename, template_name in files:
        template = env.get_template(template_name)
        content = template.render(**context)
        
        filepath = target_dir / filename
        filepath.write_text(content)
        
        # Make scripts executable
        if filename in ["main.py"]:
            filepath.chmod(0o755)
    
    # Create tests directory
    (target_dir / "tests").mkdir(exist_ok=True)
    (target_dir / "tests" / "__init__.py").touch()
    test_template = env.get_template("test_agent.py")
    (target_dir / "tests" / "test_agent.py").write_text(test_template.render(**context))
    
    click.echo(f"✅ Agent '{name}' forged at {target_dir}")
    click.echo(f"   cd {name}")
    click.echo(f"   cp .env.example .env")
    click.echo(f"   python main.py")
    click.echo(f"   docker-compose up --build (if using Docker)")

@main.command()
@click.argument("name")
def deploy(name: str):
    """Deploy agent to production (via docker-compose)"""
    target_dir = Path(name)
    if not target_dir.exists():
        click.echo(f"❌ Agent '{name}' not found!")
        sys.exit(1)
    
    click.echo(f"🚀 Deploying '{name}'...")
    os.system(f"cd {target_dir} && docker-compose up --build -d")
    click.echo(f"✅ Agent '{name}' deployed!")

@main.command()
@click.argument("name")
def stop(name: str):
    """Stop deployed agent"""
    target_dir = Path(name)
    if not target_dir.exists():
        click.echo(f"❌ Agent '{name}' not found!")
        sys.exit(1)
    
    click.echo(f"🛑 Stopping '{name}'...")
    os.system(f"cd {target_dir} && docker-compose down")
    click.echo(f"✅ Agent '{name}' stopped!")

@main.command()
def list():
    """List all forged agents"""
    mvps_dir = Path(__file__).parent.parent.parent
    agents = [d for d in mvps_dir.iterdir() if d.is_dir() and (d / "main.py").exists()]
    
    if not agents:
        click.echo("No agents forged yet. Run: agent-forge create <name>")
        return
    
    click.echo("🛠️ Forged Agents:")
    for agent in agents:
        click.echo(f"   - {agent.name}")

if __name__ == "__main__":
    main()
