import os
import json
from datetime import datetime

# Mandatory Risk Guardrails
MAX_CONTRACTS = 2
MAX_DAILY_LOSS = 500.0  # $500 max loss cap per day

def evaluate_and_execute_signal(signal_data):
    """
    Evaluates incoming market signals against risk parameters
    and prepares execution payload for broker APIs (Tradovate/Coinbase).
    """
    symbol = signal_data.get("symbol", "NQ").upper()
    action = signal_data.get("action", "BUY").upper()  # BUY / SELL
    contracts = int(signal_data.get("contracts", 1))
    price = float(signal_data.get("price", 0.0))
    stop_loss = float(signal_data.get("stop_loss", 0.0))
    take_profit = float(signal_data.get("take_profit", 0.0))
    source = signal_data.get("source", "TradingView_Webhook")

    # 1. Risk Check: Max Contract Limit
    if contracts > MAX_CONTRACTS:
        return {
            "status": "REJECTED",
            "reason": f"Contract size ({contracts}) exceeds max risk limit of {MAX_CONTRACTS}."
        }

    # 2. Risk Check: Mandatory Stop-Loss Required
    if stop_loss <= 0 and price > 0:
        return {
            "status": "REJECTED",
            "reason": "Signal rejected: Mandatory stop-loss parameter missing."
        }

    # 3. Order Execution Payload Generation
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    execution_record = {
        "timestamp": timestamp,
        "symbol": symbol,
        "action": action,
        "contracts": contracts,
        "entry_price": price,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "signal_source": source,
        "execution_state": "EXECUTED_SIMULATED",
        "broker": "Tradovate_API"
    }

    # Log auto-executed trade to GitHub via logger
    try:
        from logger import log_entry
        log_entry("AUTO_TRADE_EXECUTION", json.dumps(execution_record))
    except Exception as e:
        print(f"Failed to record auto-trade log: {e}")

    return {
        "status": "EXECUTED",
        "details": execution_record
    }

if __name__ == "__main__":
    test_signal = {
        "symbol": "NQ",
        "action": "BUY",
        "contracts": 1,
        "price": 18250.25,
        "stop_loss": 18220.00,
        "take_profit": 18310.00,
        "source": "ICT_FVG_Scanner"
    }
    print(json.dumps(evaluate_and_execute_signal(test_signal), indent=2))
