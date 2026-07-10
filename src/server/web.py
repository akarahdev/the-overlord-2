from flask import Flask, request
import code_ast
import llm
import json
import plot_data
from dataclasses import asdict

app = Flask(__name__)


@app.post("/update_data")
def update_data():
    plot_data.data.__dict__.update(request.json)
    print(plot_data.data)
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
                "content": str(plot_data.data)
            },
            {
                "role": "user",
                "content": str(request.get_data())
            }
        ],
        text_format=code_ast.Program
    )
    print(str(plot_data.data))
    program = llm_response.output_parsed
    if program is None:
        program = code_ast.Program(actions=[code_ast.SayMessage(message="The request failed, please try again.")])
    json_data = json.dumps(asdict(program))
    return f"{json_data}"