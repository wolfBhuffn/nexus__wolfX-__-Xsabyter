import json
import random
from datetime import datetime

THEMES = [
    {"theme": "Unshakeable Focus", "hook": "While they chase noise, build in silence.", "angle": "High-Value Discipline & Mental Toughness"},
    {"theme": "Spiritual Resilience", "hook": "Your tests are just proof of your potential.", "angle": "Spiritual Grounding & Self-Mastery"},
    {"theme": "Execution Over Emotion", "hook": "Do what needs to be done, regardless of how you feel.", "angle": "Monetizable Mindset & E-Commerce Drive"}
]

def generate_daily_content():
    selected = random.choice(THEMES)
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    content_payload = {
        "date": today_str,
        "persona": "Wolf SaByter",
        "theme": selected["theme"],
        "carousel_slides": [
            f"Slide 1 (Hook): {selected['hook']}",
            "Slide 2: Most people quit at 90%. The real rewards live in the final 10%.",
            "Slide 3: Control your inputs. Guard your focus. Protect your energy.",
            f"Slide 4 (CTA): Tap the link in bio / TikTok Shop to gear up and stay locked in."
        ],
        "tiktok_shop_pitch": f"🔥 Quick reminder: Motivation is temporary, but structure is permanent. Grab our top productivity & focus gear linked below while stock lasts.",
        "caption": f"🐺 {selected['theme']} // {selected['hook']}\n\nStay relentless. Master the craft.\n#WolfSaByter #Mindset #Discipline #FuturesTrading #DailyWisdom",
        "status": "STAGED_FOR_REVIEW"
    }
    
    return content_payload

if __name__ == "__main__":
    print(json.dumps(generate_daily_content(), indent=2))
