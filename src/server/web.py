from flask import Flask, request
import llm

app = Flask(__name__)

@app.post("/simple_prompt")
def simple_prompt():
    llm_response = llm.ai_client.responses.create(
        model=llm.model,
        reasoning={"effort": "none"},
        input=[
            {
                "role": "developer",
                "content": llm.system_prompt
            },
            {
                "role": "user",
                "content": str(request.get_data())
            }
        ]
    )
    return f"{str(request.get_data())} -> {llm_response.output_text}"