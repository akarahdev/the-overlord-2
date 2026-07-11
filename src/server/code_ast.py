from inspect import cleandoc
from typing import Literal, TypeVar, get_args, get_origin
from pydantic import BaseModel

functions: list[dict[str, str]] = []
AstNode = TypeVar("AstNode", bound=BaseModel)


def register_function(cls: type[AstNode]) -> type[AstNode]:
    """Register an AST node using its literal type and class docstring."""
    type_annotation: object | None = cls.__annotations__.get("type")
    if get_origin(type_annotation) is not Literal:
        raise TypeError(f"{cls.__name__} must define its type field as a Literal")

    type_arguments: tuple[object, ...] = get_args(type_annotation)
    if len(type_arguments) != 1 or not isinstance(type_arguments[0], str):
        raise TypeError(f"{cls.__name__}'s type Literal must contain one string")

    function = type_arguments[0]
    description = cleandoc(cls.__doc__ or "")
    if not description:
        raise ValueError(f"{cls.__name__} must have a docstring")

    functions.append({"function": function, "description": description})
    return cls

type PlayerSelectionType = AllPlayers | PlayerByName

type EntitySelectionType = AllEntities

type GenericSelectionType = PlayerSelectionType | EntitySelectionType

type Vec3Type = Vec3Literal | SelectionPosition | SelectionDirection | ShiftLocation

type AnyAction = SayMessage | Teleport | ApplyDamage | SetBlock | GiveItem

@register_function
class AllPlayers(BaseModel):
    """Returns a list of all players."""
    type: Literal["players/all"] = "players/all"

@register_function
class PlayerByName(BaseModel):
    """Returns a player by name."""
    type: Literal["players/by_name"] = "players/by_name"
    name: str

@register_function
class AllEntities(BaseModel):
    """Returns a list of all entities."""
    type: Literal["entities/all"] = "entities/all"

@register_function
class Vec3Literal(BaseModel):
    """Returns a new Vec3."""
    type: Literal["vec3"] = "vec3"
    x: float
    y: float
    z: float

@register_function
class SelectionPosition(BaseModel):
    """Returns the position of the provided selection."""
    type: Literal["selection/position"] = "selection/position"
    selection: GenericSelectionType

@register_function
class SelectionDirection(BaseModel):
    """Returns the facing direction of the provided selection. The direction is guaranteed to be a unit vector (1 block of distance)."""
    type: Literal["selection/direction"] = "selection/direction"
    selection: GenericSelectionType

@register_function
class ShiftLocation(BaseModel):
    """Returns a shifted version of the given Vec3 by the provided offset."""
    type: Literal["vec3/shifted"] = "vec3/shifted"
    base: Vec3Type
    shift_by: Vec3Type

@register_function
class ScaleLocation(BaseModel):
    """Returns a scaled version of the given Vec3 by the provided size as a multiplier."""
    type: Literal["vec3/scaled"] = "vec3/scaled"
    base: Vec3Type
    scale_by: float

@register_function
class SayMessage(BaseModel):
    """Broadcasts a message across the plot."""
    type: Literal["say_message"] = "say_message"
    message: str

@register_function
class Teleport(BaseModel):
    """Teleports the selection to the given location."""
    type: Literal["selection/teleport"] = "selection/teleport"
    selection: GenericSelectionType
    location: Vec3Type

@register_function
class ApplyDamage(BaseModel):
    """Damages the given selection by the specified amount."""
    type: Literal["selection/damage"] = "selection/damage"
    selection: GenericSelectionType
    amount: float

@register_function
class SetBlock(BaseModel):
    """Sets the block in the world at the specified position."""
    type: Literal["world/set_block"] = "world/set_block"
    location: Vec3Type
    block_id: str

@register_function
class GiveItem(BaseModel):
    """Gives an item to the player."""
    type: Literal["selection/give_item"] = "selection/give_item"
    selection: PlayerSelectionType
    item_id: str
    on_right_click: list[AnyAction]

class Program(BaseModel):
    actions: list[AnyAction]
