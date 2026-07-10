from typing import Any
import code_ast
import json


class PlotData:
    players: list[str] = []
    chat_logs: list[Any] = []
    item_types: list[str] = []
    entity_types: list[str] = []

    def __str__(self) -> str:
        return f"""
        Data of the plot is below.

        Available functions: {code_ast.functions}
        Online Players: {self.players}
        Previous chat messages: {self.chat_logs}
        """

data = PlotData()

with open("./src/data/entities.json") as f:
    data.entity_types = []
    json_data = json.load(f)
    for entity in json_data:
        data.entity_types.append(entity["name"])



with open("./src/data/items.json") as f:
    data.item_types = []
    json_data = json.load(f)
    for item in json_data:
        data.item_types.append(item["name"])