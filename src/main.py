from uagents import Bureau
from agents.answerer.answerer import agent as answerer_agent
from agents.generator.generator import agent as generator_agent

if __name__ == "__main__":
    # Create a Bureau instance with the specified endpoint and port
    bureau = Bureau(endpoint="http://127.0.0.1:8000/submit", port=8000)

    # Add the user agent to the bureau
    print(f"Adding answerer agent to bureau: {answerer_agent.address}")
    bureau.add(answerer_agent)

    # Add the user agent to the bureau
    print(f"Adding generator agent to bureau: {generator_agent.address}")
    bureau.add(generator_agent)

    # Run the bureau, which will manage the agents
    bureau.run()
