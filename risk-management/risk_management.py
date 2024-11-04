import redis
import time

r = redis.Redis(host='redis', port=6379, db=0)
MAX_POSITION = 100
STOP_LOSS_THRESHOLD = 0.05
initial_price = {
    "TLT": float(r.hget("prices", "TLT")),
    "TLTW": float(r.hget("prices", "TLTW"))
}

def check_risk(symbol):
    position = float(r.get(f"position:{symbol}") or 0)
    current_price = float(r.hget("prices", symbol))
    initial = initial_price[symbol]
    if position > MAX_POSITION:
        print(f"Reducing {symbol} position to max limit")
        r.set(f"signal:{symbol}", "SELL")
    if (initial - current_price) / initial >= STOP_LOSS_THRESHOLD:
        print(f"Stop-loss for {symbol} triggered")
        r.set(f"signal:{symbol}", "SELL")

def risk_management():
    while True:
        for symbol in ["TLT", "TLTW"]:
            check_risk(symbol)
        time.sleep(5)

risk_management()
