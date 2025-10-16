import os
import logging
from github import Github, GithubException

logger = logging.getLogger("GITHUB_UTILS")
logging.basicConfig(level=logging.INFO, format="%(asctime)s | GITHUB_UTILS | %(levelname)s | %(message)s")

def create_repo_with_code(task_id: str, brief: str, code: str):
    """Create a new repo and add the generated code file."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return None, None, None

    g = Github(token)
    user = g.get_user()
    logger.info(f"✅ Authenticated as: {user.login}")

    try:
        repo = user.create_repo(
            name=task_id,
            description=brief,
            private=False,
            auto_init=False
        )
        logger.info(f"📦 Created new repo: {repo.html_url}")
    except GithubException as e:
        if e.status == 422 and "name already exists" in str(e):
            logger.warning(f"⚠️ Repo {task_id} already exists. Using existing one.")
            repo = user.get_repo(task_id)
        else:
            logger.error(f"❌ Repo creation failed: {e}")
            raise

    # Try creating or updating file
    try:
        repo.create_file("app_generated.py", "Initial commit", code)
        logger.info("📄 Created app_generated.py")
    except GithubException as e:
        if e.status == 422 and "already exists" in str(e):
            contents = repo.get_contents("app_generated.py")
            repo.update_file(contents.path, "Updated file", code, contents.sha)
            logger.info("♻️ Updated existing app_generated.py")
        else:
            logger.error(f"❌ File creation failed: {e}")
            raise

    pages_url = f"https://{user.login}.github.io/{task_id}/"
    logger.info(f"✅ Repo ready: {repo.html_url}")

    return repo.html_url, repo.get_commits()[0].sha, pages_url


def update_repo(task_id: str, content: str):
    """Update app_generated.py or create if missing."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("❌ Missing GITHUB_TOKEN environment variable.")

    g = Github(token)
    user = g.get_user()
    try:
        repo = user.get_repo(task_id)
    except GithubException as e:
        if e.status == 404:
            logger.warning(f"⚠️ Repo {task_id} not found, creating new one...")
            repo = user.create_repo(task_id, private=False)
        else:
            raise

    try:
        contents = repo.get_contents("app_generated.py")
        repo.update_file(contents.path, "Updated by round", content, contents.sha)
        logger.info("♻️ Updated existing app_generated.py")
    except GithubException as e:
        if e.status == 404:
            logger.warning("⚠️ app_generated.py not found, creating new file.")
            repo.create_file("app_generated.py", "Initial commit", content)
        else:
            logger.error(f"❌ Update failed: {e}")
            raise

    logger.info(f"✅ Repo update complete: {repo.html_url}")
    return repo.get_commits()[0].sha
