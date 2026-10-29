import sys
import subprocess

def main():
    if len(sys.argv) < 2:
        print("=== nexus__wolfX-__-Xsabyter Command Center ===")
        print("Usage:")
        print("  python3 src/nexus.py status           - Run workspace diagnostic check")
        print("  python3 src/nexus.py env              - Validate environment configuration")
        print("  python3 src/nexus.py log \"<note>\"      - Quickly log an idea")
        print("  python3 src/nexus.py log -c <cat> \"\"  - Log with custom category")
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
    else:
        print(f"[-] Unknown command: '{cmd}'. Run without arguments to see usage.")

if __name__ == "__main__":
    main()
