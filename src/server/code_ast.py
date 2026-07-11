from typing import Literal, Union
from pydantic import BaseModel
from dataclasses import dataclass

@dataclass
class AllPlayers(BaseModel):
    type: Literal["players/all"] = "players/all"

@dataclass
class PlayerByName(BaseModel):
    type: Literal["players/by_name"] = "players/by_name"
    name: str

PlayerSelectionType = Union[AllPlayers, PlayerByName]

@dataclass
class AllEntities(BaseModel):
    type: Literal["entities/all"] = "entities/all"

EntitySelectionType = AllEntities

GenericSelectionType = Union[PlayerSelectionType, EntitySelectionType]

@dataclass
class Location(BaseModel):
    type: Literal["location"] = "location"
    x: float
    y: float
    z: float
    pitch: float
    yaw: float

@dataclass
class SelectionLocation(BaseModel):
    type: Literal["selection/location"] = "selection/location"
    selection: GenericSelectionType

LocationType = Union[Location, SelectionLocation]

@dataclass
class SayMessage(BaseModel):
    type: Literal["say_message"] = "say_message"
    message: str

@dataclass
class Teleport(BaseModel):
    type: Literal["teleport"] = "teleport"
    selection: GenericSelectionType
    location: LocationType

@dataclass
class ApplyDamage(BaseModel):
    type: Literal["selection/damage"] = "selection/damage"
    selection: GenericSelectionType
    amount: float

@dataclass
class SetBlock(BaseModel):
    type: Literal["world/set_block"] = "world/set_block"
    location: LocationType
    block_id: str

Actions = Union[SayMessage, Teleport, ApplyDamage, SetBlock]

@dataclass
class Program(BaseModel):
    actions: list[Actions]

functions = [
    {
        "function": "say_message",
        "description": "Sends a message to the chat."
    },
    {
        "function": "teleport",
        "description": "Teleports a selection to a location."
    },
    {
        "function": "players/all",
        "description": "Selects all online players." 
    },
    {
        "function": "players/by_name",
        "description": "Selects a player by name." 
    },
    {
        "function": "location",
        "description": "Generate a location from numeric coordinates." 
    },
    {
        "function": "selection/location",
        "description": "Get the location of entities or players in a selection." 
    },
    {
        "function": "selection/damage",
        "description": "Apply damage to a selection." 
    },
    {
        "function": "set_block",
        "description": "Set a block in the world at a location." 
    }
]