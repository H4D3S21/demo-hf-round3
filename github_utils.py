import os
from github import Github
import logging

def get_github_user():
    """Authenticate to GitHub using a Personal Access Token (PAT)."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise EnvironmentError("❌ Missing GITHUB_TOKEN environment variable.")
    g = Github(token)
    user = g.get_user()
    logging.info(f"✅ Authenticated as: {user.login}")
    return user


def create_repo_with_code(task_id, brief, code):
    """Create a new repo and upload generated code."""
    user = get_github_user()
    logging.info(f"📦 Creating new repo: {task_id}")

    repo = user.create_repo(
        name=task_id,
        description=brief,
        private=False,
        auto_init=False
    )
    repo.create_file(
        "app_generated.py",
        f"Initial commit for {task_id}",
        code
    )

    repo_url = repo.html_url
    logging.info(f"✅ Repo ready: {repo_url}")
    return repo, "initial_commit_sha", repo_url


def update_repo(task_id, content):
    """Update an existing repo with new generated content."""
    user = get_github_user()
    try:
        repo = user.get_repo(task_id)
    except Exception:
        raise RuntimeError(f"❌ Repository for task {task_id} not found!")

    contents = repo.get_contents("app_generated.py")
    repo.update_file(
        contents.path,
        f"Updated code for {task_id}",
        content,
        contents.sha
    )
    logging.info(f"✅ Updated repo: {repo.html_url}")
    return contents.sha
