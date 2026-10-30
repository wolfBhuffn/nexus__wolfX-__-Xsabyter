import os
import json
from datetime import datetime
from coinbase_connector import place_coinbase_order

MAX_CONTRACTS = 2

def evaluate_and_execute_signal(signal_data):
    symbol = signal_data.get("symbol", "BTC-USD").upper()
    action = signal_data.get("action", "BUY").upper()
    contracts = int(signal_data.get("contracts", 1))
    price = float(signal_data.get("price", 0.0))
    stop_loss = float(signal_data.get("stop_loss", 0.0))
    take_profit = float(signal_data.get("take_profit", 0.0))
    source = signal_data.get("source", "TradingView_Webhook")

    if contracts > MAX_CONTRACTS:
        return {
            "status": "REJECTED",
            "reason": f"Contract size ({contracts}) exceeds max risk limit of {MAX_CONTRACTS}."
        }

    # Dispatch to Coinbase Connector
    coinbase_result = place_coinbase_order(
        symbol=symbol if "-" in symbol else f"{symbol}-USD",
        side=action,
        size=str(contracts * 0.001)
    )

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
        "coinbase_response": coinbase_result,
        "broker": "Coinbase_Advanced_API"
    }

    try:
        from logger import log_entry
        log_entry("COINBASE_AUTO_TRADE", json.dumps(execution_record))
    except Exception as e:
        print(f"Failed to record trade log: {e}")

    return {
        "status": "EXECUTED",
        "details": execution_record
    }
