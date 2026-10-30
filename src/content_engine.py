import json
import random
from datetime import datetime

THEMES = [
    {
        "theme": "Unshakeable Focus",
        "core_message": "While they chase noise, build in silence.",
        "pillar": "High-Value Discipline & Mental Toughness"
    },
    {
        "theme": "Spiritual Resilience",
        "core_message": "Your tests are just proof of your potential.",
        "pillar": "Spiritual Grounding & Self-Mastery"
    },
    {
        "theme": "Execution Over Emotion",
        "core_message": "Do what needs to be done, regardless of how you feel.",
        "pillar": "Monetizable Mindset & E-Commerce Drive"
    }
]

def generate_daily_content():
    selected = random.choice(THEMES)
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    content_payload = {
        "date": today_str,
        "persona": "Wolf SaByter",
        "theme": selected["theme"],
        "pillar": selected["pillar"],
        "platforms": {
            "instagram": {
                "carousel_slides": [
                    f"Slide 1 (Hook): {selected['core_message']}",
                    "Slide 2: Most people quit at 90%. The real compounding lives in the final 10%.",
                    "Slide 3: Guard your inputs. Silence the noise. Execute your daily routine.",
                    "Slide 4 (CTA): Save this for when focus slips. Link in bio for full command toolkits."
                ],
                "caption": f"🐺 {selected['theme']} // {selected['core_message']}\n\nMaster the inner dialogue before taking the outer field.\n\n#WolfSaByter #Mindset #Discipline #Execution #DailyWisdom"
            },
            "youtube_shorts": {
                "hook_spoken": f"Stop letting your feelings run your agenda. {selected['core_message']}",
                "visual_cues": "Dark background, high-contrast bold typography, rapid transition visuals.",
                "pinned_comment": "🔥 Access the Wolf SaByter productivity & focus engine kit in the description link."
            },
            "x_twitter": {
                "thread": [
                    f"1/ {selected['core_message']} Here is how to maintain deep focus in a hyper-distracted world:",
                    "2/ Audit your daily inputs. If it doesn't build your wealth, spiritual strength, or mental acuity, reduce it.",
                    "3/ Structure beats willpower every single time. Build systems so execution becomes default.",
                    f"4/ Master {selected['theme'].lower()}. If you want tools to automate your workflow, check out the pinned link."
                ]
            },
            "tiktok_shop": {
                "hook": f"If you're trying to lock in for the rest of this year, listen to this.",
                "script": f"🔥 {selected['core_message']} Motivation is temporary, but physical systems stay fixed. Grab our recommended workspace focus gear linked in the shop below before inventory runs out.",
                "cta": "Tap the orange basket below to upgrade your focus setup."
            },
            "linkedin": {
                "headline": f"The Strategic Advantage of {selected['theme']}",
                "post": f"{selected['core_message']}\n\nIn high-stakes execution, emotional variance is a liability. Sustainable performance comes from automated systems, intentional boundary setting, and continuous operational discipline.\n\nHow do you structure your focus periods under high load?"
            }
        },
        "status": "STAGED_FOR_REVIEW"
    }
    
    return content_payload

if __name__ == "__main__":
    print(json.dumps(generate_daily_content(), indent=2))
