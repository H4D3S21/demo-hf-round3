from fastapi import FastAPI, Request
from github_utils import create_or_update_repo
from hf_generator import generate_app_code
import logging

app = FastAPI()
logger = logging.getLogger("HF_GENERATOR")
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

@app.post("/task")
async def handle_task(request: Request):
    data = await request.json()
    email = data.get("email")
    secret = data.get("secret")
    task = data.get("task")
    brief = data.get("brief")
    round_ = data.get("round")
    nonce = data.get("nonce", f"local-{task}")

    logger.info(f"Round {round_} | Task {task} | Email {email}")
    logger.info("🧠 Sending prompt to HuggingFace server...")

    # Generate code
    code = generate_app_code(brief)

    # Create or update GitHub repo
    repo = create_or_update_repo(task, brief, code)
    pages_url = f"https://github.com/H4D3S21/{repo.name}"

    logger.info(f"✅ Repo ready: {pages_url}")

    # Optional callback data
    callback_data = {"task": task, "repo_url": pages_url}

    return {"status": "success", "round": round_, "repo": repo.name, "url": pages_url}
