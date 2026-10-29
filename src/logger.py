import argparse
from datetime import datetime
from pathlib import Path

def log_entry(category, content):
    logs_dir = Path("docs/logs")
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.now().strftime("%H:%M:%S")
    log_file = logs_dir / f"{today_str}.md"
    
    # Initialize file with header if it doesn't exist
    if not log_file.exists():
        log_file.write_text(f"# Daily Log: {today_str}\n\n")
        
    entry = f"- **[{time_str}] ({category.upper()})**: {content}\n"
    
    with open(log_file, "a") as f:
        f.write(entry)
        
    print(f"[+] Logged successfully to {log_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nexus Quick Idea & Task Logger")
    parser.add_argument("-c", "--category", default="idea", help="Category (e.g., idea, task, note, milestone)")
    parser.add_argument("content", type=str, help="The content or note to log")
    
    args = parser.parse_args()
    log_entry(args.category, args.content)
