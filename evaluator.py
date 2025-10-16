import requests
import time

def send_evaluation_callback(evaluation_url, payload):
    for attempt in range(6):  # retries with exponential backoff
        resp = requests.post(evaluation_url, json=payload)
        if resp.status_code == 200:
            return True
        time.sleep(2 ** attempt)
    return False
