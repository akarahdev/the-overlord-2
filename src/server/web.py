from flask import Flask, request
import code_ast
import llm
import json
from dataclasses import asdict
from typing import Any

app = Flask(__name__)

class PlotData:
    players: list[str] = []
    chat_logs: list[Any] = []

    def __str__(self) -> str:
        return f"""
        Data of the plot is below.

        Online Players: {self.players}
        Previous chat messages: {self.chat_logs}
        """

plot_data = PlotData()

@app.post("/update_data")
def update_data():
    global plot_data
    plot_data = PlotData()
    plot_data.__dict__.update(request.json)
    print(plot_data)
    return ""


@app.post("/simple_prompt")
def simple_prompt():
    global plot_data
    llm_response = llm.ai_client.responses.parse(
        model=llm.model,
        reasoning={"effort": "none"},
        input=[
            {
                "role": "developer",
                "content": llm.system_prompt
            },
            {
                "role": "developer",
                "content": str(plot_data)
            },
            {
                "role": "user",
                "content": str(request.get_data())
            }
        ],
        text_format=code_ast.Program
    )
    program = llm_response.output_parsed
    if program is None:
        program = code_ast.Program(actions=[code_ast.SayMessage(message="The request failed, please try again.")])
    json_data = json.dumps(asdict(program))
    return f"{json_data}"