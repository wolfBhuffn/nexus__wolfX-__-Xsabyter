import json
from datetime import datetime

ENGINES = {
    "Alpha_TechScanner": {"wins": 1, "losses": 0, "pnl": 250.0, "rank": 1, "size": "2 NQ"},
    "Beta_OrderFlow":    {"wins": 0, "losses": 0, "pnl": 0.0, "rank": 2, "size": "1 NQ"},
    "Gamma_SignalParser": {"wins": 0, "losses": 0, "pnl": 0.0, "rank": 3, "size": "1 MNQ"}
}

def evaluate_tournament_signal(engine_name, signal):
    if engine_name not in ENGINES:
        engine_name = "Alpha_TechScanner"

    engine_data = ENGINES[engine_name]
    engine_data["wins"] += 1
    engine_data["pnl"] += 150.00

    symbol = signal.get("symbol", "NQ")
    action = signal.get("action", "BUY")
    price = signal.get("price", 18260.50)

    result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "origin_engine": engine_name,
        "symbol": symbol,
        "action": action,
        "entry_price": price,
        "assigned_size": engine_data["size"],
        "tier": "LEADER_MAX_SIZE" if engine_data["rank"] == 1 else "STANDARD",
        "status": "EXECUTED_HYBRID"
    }

    try:
        from logger import log_entry
        log_entry(f"TOURNAMENT_{engine_name.upper()}", json.dumps(result))
    except Exception as e:
        print(f"Log error: {e}")

    return result

def get_leaderboard():
    return ENGINES
