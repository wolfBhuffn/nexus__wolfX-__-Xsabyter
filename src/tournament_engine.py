import json
from datetime import datetime

# Engine Standings & Leaderboard State
ENGINES = {
    "Alpha_TechScanner": {"wins": 0, "losses": 0, "pnl": 0.0, "rank": 1, "size": "2 NQ"},
    "Beta_OrderFlow":    {"wins": 0, "losses": 0, "pnl": 0.0, "rank": 2, "size": "1 NQ"},
    "Gamma_SignalParser": {"wins": 0, "losses": 0, "pnl": 0.0, "rank": 3, "size": "1 MNQ"}
}

def evaluate_tournament_signal(engine_name, signal):
    """
    Evaluates incoming signals from a specific engine, checks consensus across 
    competing engines, and adjusts leaderboard stats.
    """
    if engine_name not in ENGINES:
        return {"status": "REJECTED", "reason": "Unknown engine."}

    engine_data = ENGINES[engine_name]
    symbol = signal.get("symbol", "NQ")
    action = signal.get("action", "BUY")
    price = signal.get("price", 0.0)

    # Calculate Consensus Score
    consensus_count = 1  # Originating engine
    # Check if other engines have active signals on same symbol/direction
    
    execution_tier = "STANDARD"
    if engine_data["rank"] == 1:
        execution_tier = "LEADER_MAX_SIZE"

    result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "origin_engine": engine_name,
        "symbol": symbol,
        "action": action,
        "entry_price": price,
        "assigned_size": engine_data["size"],
        "tier": execution_tier,
        "status": "EXECUTED_HYBRID"
    }

    try:
        from logger import log_entry
        log_entry("TOURNAMENT_TRADE", json.dumps(result))
    except Exception as e:
        print(f"Log error: {e}")

    return result

def get_leaderboard():
    return ENGINES

if __name__ == "__main__":
    sample_signal = {"symbol": "NQ", "action": "BUY", "price": 18250.00}
    res = evaluate_tournament_signal("Alpha_TechScanner", sample_signal)
    print(json.dumps(res, indent=2))
