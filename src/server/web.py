from flask import Flask, request
import code_ast
import llm
import json
import plot_data

app = Flask(__name__)


@app.post("/update_data")
def update_data():
    try:
        plot_data.data.players = request.json["players"]
        plot_data.data.chat_logs = request.json["chat_logs"]
        print(plot_data.data)
    except Exception:
        print(f"An error occured when updating data.")
    return ""


@app.post("/simple_prompt")
def simple_prompt():
    global plot_data

    inputs = request.get_json()
    print(f"inputs: {inputs}")

    llm_response = llm.ai_client.responses.parse(
        model=inputs["model"],
        reasoning={"effort": inputs["reasoning_effort"]},
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
                "content": str(inputs["user_request"])
            }
        ],
        text_format=code_ast.Program
    )
    print(str(plot_data.data))
    program = llm_response.output_parsed
    if program is None:
        program = code_ast.Program(actions=[code_ast.SayMessage(message="The request failed, please try again.")])
    program_data = program.model_dump(mode="json")
    json_data = json.dumps(program_data)
    pretty_json = json.dumps(program_data, indent=4)
    print(pretty_json)
    return f"{json_data}"

@app.errorhandler(400)
def handle_bad_request(e): # type: ignore
    # Print the exact parsing description from Flask/Werkzeug
    print(f"--- 400 Error Description: {e.description} ---") # type: ignore
    
    # Inspect query parameters (?key=value)
    print(f"URL Args: {request.args}")
    
    # Inspect form data
    print(f"Form Data: {request.form}")
    
    # Inspect raw data strings safely
    raw_data = request.get_data(as_text=True)
    print(f"Raw Request Body: {raw_data}")

    return "400 occurred, check console :("
