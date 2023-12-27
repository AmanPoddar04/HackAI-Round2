import os
import requests
from dotenv import load_dotenv
from uagents import Agent, Context, Protocol
from uagents.setup import fund_agent_if_low
from messages import UAgentResponse, UAgentResponseType, Query
from utils.initiate import init_palm
import google.generativeai as palm

load_dotenv()

# Get the ANSWERER_SEED from environment or use a default value
ANSWERER_SEED = os.getenv("ANSWERER_SEED", "answerer service secret phrase")

# Initialize an Agent with a name and seed
agent = Agent(name="answerer_agent", seed=ANSWERER_SEED)

# Fund the agent's wallet if it's low on funds
fund_agent_if_low(agent.wallet.address())

# Define a custom protocol for defining handlers
answerer_protocol = Protocol("Answerer")

palm_model = None


@agent.on_event("startup")
async def start(ctx: Context):
    palm_model = await init_palm()


@answerer_protocol.on_message(model=Query, replies=Query)
async def answer(ctx: Context, sender: str, msg: Query):
    # ctx.logger.info(msg.question)
    # ctx.logger.info(msg.context)
    palm_model = await init_palm()
    # print(palm_model)
    answer = palm.generate_text(
        model=palm_model,
        prompt=f"Expand this answer based on the question with a proper sentence. question: {msg.question} answer: {msg.context}. Give a proper statement with the answer. Also provide more information regarding the question and write a short paragraph for the answer.",
        temperature=0,
        max_output_tokens=800,
    )
    print(answer.result)
    text = f"""
    Question: {msg.question}
    Answer: {answer.result}
    """
    print("What else can I help you with?")
    ques = input()
    await ctx.send(
        sender,
        Query(
            question=ques,
            context=msg.context,
            answer=answer.result,
            previous_response=text,
        ),
    )


# Include the answerer protocol in the agent
agent.include(answerer_protocol)
