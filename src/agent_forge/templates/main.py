"""{{ name }} - AI Agent"""

from agent import {{ name.title().replace('_', '') }}Agent
import uvicorn

def main():
    """Run the agent"""
    agent = {{ name.title().replace('_', '') }}Agent()
    uvicorn.run(agent.app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
