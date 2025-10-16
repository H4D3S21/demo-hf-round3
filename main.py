from fastapi import FastAPI, Request
from hf_generator import generate_app_code
from github_utils import create_repo_with_code, update_repo
import logging
import os

app = FastAPI()

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

@app.get("/")
def root():
    return {"message": "🚀 LLM Deployment Server is Live on Render!"}


@app.post("/task")
async def handle_task(request: Request):
    data = await request.json()
    task_id = data.get("task_id", "demo-hf-round1")
    brief = data.get("brief", "AI code generation task")
    email = data.get("email", "student@example.com")

    logging.info(f"🧠 Round | Task {task_id} | Email {email}")
    logging.info("🧠 Sending prompt to HuggingFace server...")

    code = generate_app_code(brief)

    try:
        repo, sha, repo_url = create_repo_with_code(task_id, brief, code)
    except Exception as e:
        logging.error(f"⚠️ Repo creation failed: {e}")
        try:
            sha = update_repo(task_id, code)
            repo_url = f"https://github.com/H4D3S21/{task_id}"
        except Exception as e2:
            return {"error": str(e2)}

    logging.info(f"✅ Repo ready: {repo_url}")
    return {
        "task_id": task_id,
        "commit_sha": sha,
        "repo_url": repo_url,
        "status": "success",
        "message": f"✅ Successfully completed round for {task_id}"
    }
