import sys
import subprocess

def main():
    if len(sys.argv) < 2:
        print("=== nexus__wolfX-__-Xsabyter Command Center ===")
        print("Usage:")
        print("  nexus status           - Run workspace diagnostic check")
        print("  nexus env              - Validate environment configuration")
        print("  nexus log \"<note>\"      - Quickly log an idea")
        print("  nexus serve            - Spin up mobile browser command server")
        print("===============================================")
        return

    cmd = sys.argv[1].lower()

    if cmd == "status":
        subprocess.run(["python3", "src/nexus_status.py"])
    elif cmd == "env":
        subprocess.run(["python3", "src/env_sync.py"])
    elif cmd == "log":
        log_args = ["python3", "src/logger.py"] + sys.argv[2:]
        subprocess.run(log_args)
    elif cmd == "serve":
        subprocess.run(["python3", "src/server.py"])
    else:
        print(f"[-] Unknown command: '{cmd}'. Run without arguments to see usage.")

if __name__ == "__main__":
    main()
