import requests
import logging

HF_SERVER_URL = "http://127.0.0.1:8010/generate"  # local Docker HF endpoint

def generate_app_code(prompt: str):
    """Send prompt to HuggingFace generator and get code."""
    try:
        response = requests.post(HF_SERVER_URL, json={"prompt": prompt}, timeout=30)
        if response.status_code == 200:
            return response.text
        logging.warning(f"⚠️ HF returned {response.status_code}: {response.text}")
        return f"# HF server error: {response.text}"
    except Exception as e:
        logging.error(f"❌ HF request failed: {e}")
        return f"# HF connection error: {e}"
