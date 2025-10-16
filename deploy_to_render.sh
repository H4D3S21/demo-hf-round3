#!/bin/bash

# ==============================================================
# 🚀 Render Auto Deployment Script for ai-code-deploy Project
# Author: Aarav (H4D3S21)
# ==============================================================

echo "🔧 Preparing Render deployment..."

# Step 1: Log in (you only need to do this once manually on Render)
# Go to: https://render.com
# → Click “New Web Service” → “Connect your GitHub account”
# → Choose your repo (e.g. demo-hf-round3)
# → Then set the following fields:

# Name: demo-hf-round3
# Environment: Python 3
# Build Command: pip install -r requirements.txt
# Start Command: uvicorn main:app --host 0.0.0.0 --port 10000
# Port: 10000
# Auto Deploy: Yes
# Branch: main

echo "✅ Connected GitHub repo to Render."

# Step 2: Create a Procfile (Render reads this automatically)
echo "web: uvicorn main:app --host 0.0.0.0 --port 10000" > Procfile

# Step 3: Create a runtime file (ensures Python version consistency)
echo "python-3.10.13" > runtime.txt

# Step 4: Push new deployment configs
git add Procfile runtime.txt
git commit -m "Added Render deployment files"
git push origin main

echo "🚀 Deployment files pushed. Go to Render Dashboard and click 'Deploy Now'."
echo "Once live, you’ll get your public app URL like:"
echo "🌐 https://demo-hf-round3.onrender.com"
