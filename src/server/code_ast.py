from typing import Literal
from pydantic import BaseModel
from dataclasses import dataclass

@dataclass
class SayMessage(BaseModel):
    type: Literal["say_message"] = "say_message"
    message: str

Actions = SayMessage

@dataclass
class Program(BaseModel):
    actions: list[Actions]

functions = [
    {
        "function": "say_message",
        "description": "Sends a message to the chat."
    }
]