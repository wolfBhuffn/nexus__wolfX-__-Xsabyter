import os
import subprocess
from pathlib import Path

def check_git_status():
    print("[*] Checking Git Status...")
    try:
        result = subprocess.run(["git", "status", "-s"], capture_output=True, text=True, check=True)
        if result.stdout.strip():
            print("[!] Uncommitted changes detected:")
            print(result.stdout)
        else:
            print("[+] Working tree is clean.")
    except Exception as e:
        print(f"[-] Error checking git status: {e}")

def check_environment():
    print("\n[*] Checking Environment Configuration...")
    env_path = Path(".env")
    if env_path.exists():
        print("[+] Local .env file found.")
    else:
        print("[!] Warning: Local .env file not found (check config/.env.example).")

if __name__ == "__main__":
    print("=== nexus__wolfX-__-Xsabyter Status Control ===")
    check_git_status()
    check_environment()
    print("===============================================")
