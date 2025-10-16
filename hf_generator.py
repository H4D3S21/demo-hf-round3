import os
import requests
import json
import logging

logger = logging.getLogger("HF_GENERATOR")

HF_SERVER = os.getenv("HF_SERVER", "http://127.0.0.1:8010/generate")

def generate_app_code(brief, attachments=None):
    """
    Ask the local HuggingFace Flask server to generate multi-file project code.
    Returns a dictionary with filenames as keys and code as values.
    """
    logger.info("🧠 Sending prompt to HuggingFace server...")

    prompt = (
        f"Generate a small Flask web app with the following description:\n"
        f"{brief}\n\n"
        "Output must include 3 files:\n"
        "1. app.py (Flask backend serving index.html)\n"
        "2. templates/index.html (main HTML page)\n"
        "3. static/style.css (basic styling)\n"
        "Provide them as JSON object {{'app.py': code1, 'templates/index.html': code2, 'static/style.css': code3}}."
    )

    payload = {"prompt": prompt}
    try:
        resp = requests.post(HF_SERVER, json=payload, timeout=120)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error contacting HF server: {e}")
        raise RuntimeError(f"Failed to connect to HuggingFace server at {HF_SERVER}") from e

    try:
        data = resp.json()
    except json.JSONDecodeError:
        logger.error("❌ Invalid JSON from HF server.")
        raise

    if "text" not in data:
        raise RuntimeError(f"Unexpected HF server response: {data}")

    try:
        # Attempt to parse generated JSON dictionary
        parsed = json.loads(data["text"])
        logger.info("✅ Multi-file code generation successful.")
        return parsed
    except Exception as e:
        logger.warning("⚠️ HF output not valid JSON, returning as single file.")
        return {"app_generated.py": data["text"]}
