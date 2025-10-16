#!/bin/bash
echo "Starting lightweight HuggingFace Flask server..."
python3 - <<'PYCODE'
from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)
generator = pipeline("text-generation", model="distilgpt2")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(force=True)
    prompt = data.get("prompt", "")
    result = generator(prompt, max_new_tokens=150)
    return jsonify({"text": result[0]["generated_text"]})

if __name__ == "__main__":
    print("Running on port 8001 ...")
    app.run(host="0.0.0.0", port=8001)
PYCODE
