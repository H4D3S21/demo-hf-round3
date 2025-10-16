from fastapi import FastAPI, Request
from github_utils import create_repo_with_code, update_repo
from hf_generator import generate_code
from utils import send_callback
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

# ✅ Home route (for Render homepage)
@app.get("/")
def home():
    return {"message": "🚀 LLM Deployment Server is Live on Render!"}


# ✅ Task route (main app logic)
@app.post("/task")
async def handle_task(request: Request):
    data = await request.json()
    task_id = data.get("task_id", "demo-hf-round")
    email = data.get("email", "student@example.com")
    round_num = data.get("round", "1")
    brief = data.get("brief", "No brief provided")
    nonce = data.get("nonce", "no-nonce")

    logging.info(f"Round {round_num} | Task {task_id} | Email {email}")

    # --- Step 1: Generate code from Hugging Face server
    hf_server = "http://127.0.0.1:8010/generate"
    logging.info(f"🧠 Sending prompt to HuggingFace server...")
    code = generate_code(hf_server, brief)

    # --- Step 2: Push to GitHub repo
    try:
        logging.info("✅ Authenticated with GitHub")
        try:
            sha = update_repo(task_id, code)
        except RuntimeError:
            logging.warning(f"⚠️ Repo {task_id} not found. Creating new one...")
            repo, sha, pages_url = create_repo_with_code(task_id, brief, code)
            logging.info(f"✅ Created repo: {pages_url}")
        else:
            repo = f"https://github.com/H4D3S21/{task_id}"
            logging.info(f"✅ Updated existing repo: {repo}")

        commit_sha = sha
        repo_url = f"https://github.com/H4D3S21/{task_id}"

    except Exception as e:
        logging.error(f"❌ GitHub error: {e}")
        commit_sha = None
        repo_url = None

    # --- Step 3: Send callback
    send_callback(task_id, round_num, email, nonce, commit_sha)

    return {
        "status": "ok",
        "round": round_num,
        "repo_url": repo_url,
        "commit_sha": commit_sha
    }
