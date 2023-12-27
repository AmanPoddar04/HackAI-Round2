from enum import Enum
from typing import List, Optional

from uagents import Model


class UAgentResponseType(Enum):
    ERROR = "error"
    RESPONSE = "response"


class UAgentResponse(Model):
    type: UAgentResponseType
    agent_address: Optional[str]
    response: Optional[str]
    request_id: Optional[str]


class Query(Model):
    question: str
    context: Optional[str]
    answer: Optional[str]
    previous_response: Optional[str]
