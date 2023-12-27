import os
import requests
from dotenv import load_dotenv
from uagents import Agent, Context, Protocol
from uagents.setup import fund_agent_if_low
from messages import UAgentResponse, UAgentResponseType, Query
from utils.initiate import init_pipeline, init_palm
import google.generativeai as palm
from agents.answerer.answerer import agent as answerer_agent

load_dotenv()

# Get the GENERATOR_SEED from environment or use a default value
GENERATOR_SEED = os.getenv("GENERATOR_SEED", "generator service secret phrase")

# Initialize an Agent with a name and seed
agent = Agent(name="generator_agent", seed=GENERATOR_SEED)

# Fund the agent's wallet if it's low on funds
fund_agent_if_low(agent.wallet.address())


def get_project_root() -> str:
    """Returns the absolute path of the project's root directory."""
    current_file = os.path.abspath(__file__)  # Absolute path of the current script
    return os.path.dirname(
        os.path.dirname(current_file)
    )  # Parent directory (project root)


def get_document(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return "File not found or path is incorrect."
    except Exception as e:
        return f"Error occurred: {str(e)}"


parts = get_project_root().rsplit("\\", 1)
if len(parts) > 1:
    file_path = parts[0]
else:
    file_path = get_project_root()

file_path = f"{file_path}\document.txt"


def get_document(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return "File not found or path is incorrect."
    except Exception as e:
        return f"Error occurred: {str(e)}"


def update_document(text):
    try:
        with open(file_path, "a") as file:
            file.write(text + "\n")
            return "Document updated successfully."
    except Exception as e:
        return f"Error occurred: {str(e)}"


# Define a custom protocol for defining handlers
generator_protocol = Protocol("Generator")

nlp = None

answerer_agent_address = answerer_agent.address


@agent.on_event("startup")
async def start(ctx: Context):
    nlp = await init_pipeline()
    print("Welcome to Hitachi Customer Support")
    print("This enchanted helpdesk will help you with any queries you might have regarding our platform.")
    print("What magical aid do you require today?")
    query = input()
    document = get_document(file_path=file_path)
    palm_model = await init_palm()
    potential_answers = palm.generate_text(
        model=palm_model,
        prompt=f"I have a question regarding a company's customer service. The question is {query}. What can be the potential answers to this questioin?",
        temperature=0,
        max_output_tokens=800,
    )
    potential_answers = potential_answers.result
    # print(potential_answers)
    query = f"""{query}
    Potential answers: {potential_answers}
    """
    # print(query)
    answer = nlp(question=query, context=document, max_length=1024)
    answer = answer["answer"]
    # print(answer)
    await ctx.send(answerer_agent_address, Query(question=query, context=answer))


@generator_protocol.on_message(model=Query, replies=Query)
async def generate(ctx: Context, sender: str, msg: Query):
    # ctx.logger.info(msg.question)
    update_document(msg.previous_response)
    nlp = await init_pipeline()
    document = get_document(file_path=file_path)
    # print(document)
    query = msg.question
    answer = nlp(question=query, context=document, max_length=1024)
    answer = answer["answer"]
    # print(answer)
    await ctx.send(sender, Query(question=msg.question, context=answer))


# Include the generator protocol in the agent
agent.include(generator_protocol)
