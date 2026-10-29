import os
import sys
from datetime import datetime

# Load .env quietly if present locally
try:
    from dotenv import load_dotenv
    load_dotenv(verbose=False)
except ImportError:
    pass

def get_status():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    github_status = "CONFIGURED (Cloud API)" if os.environ.get("GITHUB_TOKEN") else "LOCAL ONLY (Fallback)"
    
    status_output = [
        f"=== NEXUS SYSTEM DIAGNOSTICS ===",
        f"Timestamp: {timestamp}",
        f"Environment: {'Render Cloud' if os.environ.get('RENDER') else 'Local Machine'}",
        f"GitHub Sync: {github_status}",
        f"Repository: {os.environ.get('GITHUB_REPOSITORY', 'wolfBhuffn/nexus__wolfX-__-Xsabyter')}",
        f"System State: ONLINE & OPERATIONAL"
    ]
    return "\n".join(status_output)

if __name__ == "__main__":
    print(get_status())
