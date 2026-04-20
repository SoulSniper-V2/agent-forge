"""{{ name }} - AI Agent"""

from agent import {{ class_name }}Agent
import uvicorn

def main():
    """Run the agent"""
    agent = {{ class_name }}Agent()
    uvicorn.run(agent.app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
