import os
from github import Github, GithubException

def create_or_update_repo(task_id, brief, files_dict):
    """
    Creates or updates a GitHub repo and uploads multiple files.
    files_dict = {filename: content}
    """
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("❌ GITHUB_TOKEN not found in environment variables.")

    g = Github(token)
    user = g.get_user()
    print(f"✅ Authenticated as: {user.login}")

    # Check or create repo
    try:
        repo = user.get_repo(task_id)
        print(f"⚙️ Updating existing repo: {repo.name}")
    except GithubException:
        print(f"📦 Creating new repo: {task_id}")
        repo = user.create_repo(
            name=task_id,
            description=brief or "AI-generated Flask project",
            private=False,
            auto_init=False,
        )

    # Commit files
    for path, content in files_dict.items():
        commit_message = f"🤖 Auto-update: {path}"
        try:
            # Try updating existing file
            existing = repo.get_contents(path)
            repo.update_file(existing.path, commit_message, content, existing.sha)
            print(f"🌀 Updated {path}")
        except GithubException as e:
            if e.status == 404:
                repo.create_file(path, commit_message, content)
                print(f"📄 Created {path}")
            else:
                raise

    # Auto-generate README.md
    readme_content = f"# {task_id}\n\nGenerated automatically by AI code generator.\n\n## Brief\n{brief}"
    try:
        existing = repo.get_contents("README.md")
        repo.update_file("README.md", "📘 Auto-update README", readme_content, existing.sha)
    except GithubException:
        repo.create_file("README.md", "📘 Add README", readme_content)

    print(f"✅ Repo ready: https://github.com/{user.login}/{repo.name}")
    return repo
