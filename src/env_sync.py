import os
from pathlib import Path

def validate_environment():
    print("[*] Validating Environment Configuration...")
    env_path = Path(".env")
    example_path = Path("config/.env.example")
    
    if not env_path.exists():
        print("[-] Error: Active .env file missing.")
        return
        
    if not example_path.exists():
        print("[-] Warning: config/.env.example template not found.")
        return

    # Simple key parser
    def get_keys(file_path):
        keys = set()
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    keys.add(line.split("=")[0].strip())
        return keys

    active_keys = get_keys(env_path)
    example_keys = get_keys(example_path)

    missing_keys = example_keys - active_keys
    if missing_keys:
        print(f"[!] Warning: Missing keys in active .env compared to template: {missing_keys}")
    else:
        print("[+] Active .env contains all template keys.")

if __name__ == "__main__":
    print("=== nexus__wolfX-__-Xsabyter Env Validator ===")
    validate_environment()
    print("=============================================")
