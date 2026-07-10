llama-server -hf ggml-org/gemma-4-E4B-it-GGUF:Q4_K_M -np 10
ngrok tcp 5000
python ./src/server/main.py