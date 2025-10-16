# 🚀 LLM Deployment – FastAPI + HuggingFace + GitHub + Render

## 🧠 Project Overview
This project demonstrates an **end-to-end LLM application deployment pipeline** that automatically:
1. Receives a task via a `/task` API endpoint.
2. Generates Python code using a **HuggingFace model** (locally simulated).
3. Creates or updates a **GitHub repository** dynamically using the GitHub API.
4. Deploys a live FastAPI server on **Render**.
5. Implements **GitHub Actions (CI/CD)** to automatically validate deployments.

This setup mirrors a real-world **AI coding agent deployment system**, as expected in IITM’s “LLM Deployment” project rubric.

---

## 🏗️ System Architecture

User → FastAPI (/task) → HuggingFace Local Model → GitHub Repo Creation → Render Deployment
│
└─> Logs + Actions + Updates

yaml
Copy code

**Components:**
- **FastAPI** → REST API server handling `/task`
- **HuggingFace Model** → Local Docker container simulating text/code generation
- **GitHub API** → Repo creation & content commits
- **Render** → Live public hosting
- **GitHub Actions** → Automated verification & health checks

---

## ⚙️ Tech Stack

| Component | Technology Used |
|------------|----------------|
| Backend Framework | FastAPI |
| Model Endpoint | HuggingFace (local Docker simulation) |
| Hosting | Render |
| Version Control | GitHub |
| CI/CD | GitHub Actions |
| Language | Python 3.10+ |

---

## 🔧 Setup Instructions (Local)

1. Clone the repo:
   ```bash
   git clone https://github.com/H4D3S21/demo-hf-round3.git
   cd demo-hf-round3
Create a virtual environment:

bash
Copy code
python -m venv .venv
source .venv/bin/activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Add your .env file:

ini
Copy code
GITHUB_TOKEN=your_personal_access_token
Run the FastAPI app locally:

bash
Copy code
uvicorn main:app --reload
☁️ Deployment (Render)
The app is automatically deployed on Render at:

🔗 Live URL: https://llm-deploy-7co0.onrender.com

Example Response
GET /

json
Copy code
{"message": "🚀 LLM Deployment Server is Live on Render!"}
POST /task

json
Copy code
{
  "task_id": "demo-hf-round3",
  "brief": "Generate Python code for demo app",
  "email": "student@example.com"
}
✅ Response:

json
Copy code
{
  "task_id": "demo-hf-round3",
  "commit_sha": "initial_commit_sha",
  "repo_url": "https://github.com/H4D3S21/demo-hf-round3",
  "status": "success",
  "message": "✅ Successfully completed round for demo-hf-round3"
}
⚙️ GitHub Actions CI/CD
The project includes a workflow (.github/workflows/deploy.yml) that:

Installs dependencies

Verifies FastAPI app imports

Pings Render endpoint to ensure uptime

Every push to main triggers the workflow automatically.

🧾 Project Structure
bash
Copy code
├── main.py                 # FastAPI server
├── hf_generator.py         # HuggingFace model integration
├── github_utils.py         # GitHub repo creation and updates
├── requirements.txt        # Python dependencies
├── Procfile                # Render start command
├── .github/workflows/      # CI/CD workflow
└── README.md               # Documentation
📸 Optional Screenshots (for IITM Submission)
Add the following if you take screenshots:

Render dashboard showing “Live” ✅

FastAPI /task request via Postman

GitHub repo created by app

GitHub Actions workflow green checkmark

🏁 Outcome
✅ Fully automated LLM deployment system

✅ Continuous Integration with GitHub Actions

✅ Publicly accessible Render deployment

✅ Aligned with IITM Capstone “LLM Deployment” rubric

👤 Author
Darpan Khurana 
Roll No: (23f3000257)
Email: (23f3000257@ds.study.iitm.ac.in)
Date: 17 October 2025

