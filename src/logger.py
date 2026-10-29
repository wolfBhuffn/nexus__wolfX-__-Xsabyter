import os
import sys
import json
import base64
import argparse
from datetime import datetime
import requests

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_NAME = os.environ.get("GITHUB_REPOSITORY", "wolfBhuffn/nexus__wolfX-__-Xsabyter")
LOG_PATH = "data/nexus_logs.json"

def log_entry(category, content):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = {
        "timestamp": timestamp,
        "category": category.upper(),
        "content": content
    }

    # If running in the cloud with a GitHub token, sync directly to GitHub repo
    if GITHUB_TOKEN:
        push_to_github(new_entry)
    else:
        # Local fallback saving to disk
        local_save(new_entry)
        
    print(f"[{timestamp}] [{category.upper()}] {content}")

def push_to_github(entry):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    api_url = f"https://api.github.com/repos/{REPO_NAME}/contents/{LOG_PATH}"

    # 1. Fetch existing log file to get its SHA (required by GitHub API for updates)
    response = requests.get(api_url, headers=headers)
    logs = []
    sha = None

    if response.status_code == 200:
        file_data = response.json()
        sha = file_data["sha"]
        decoded_content = base64.b64decode(file_data["content"]).decode("utf-8")
        try:
            logs = json.loads(decoded_content)
        except json.JSONDecodeError:
            logs = []

    # 2. Append new entry
    logs.append(entry)
    updated_content_str = json.dumps(logs, indent=2)
    encoded_content = base64.b64encode(updated_content_str.encode("utf-8")).decode("utf-8")

    # 3. Commit/Push update back to GitHub
    payload = {
        "message": f"NEXUS Log: [{entry['category']}] {entry['content'][:30]}...",
        "content": encoded_content,
        "branch": "main"
    }
    if sha:
        payload["sha"] = sha

    put_response = requests.put(api_url, headers=headers, json=payload)
    if put_response.status_code not in [200, 201]:
        print(f"Error syncing log to GitHub: {put_response.text}", file=sys.stderr)

def local_save(entry):
    os.makedirs("data", exist_ok=True)
    logs = []
    if os.path.exists(LOG_PATH):
        try:
            with open(LOG_PATH, "r") as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = []
    logs.append(entry)
    with open(LOG_PATH, "w") as f:
        json.dump(logs, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NEXUS Logger")
    parser.add_argument("-c", "--category", default="idea", help="Log category")
    parser.add_argument("content", help="Log content")
    args = parser.parse_args()
    log_entry(args.category, args.content)
