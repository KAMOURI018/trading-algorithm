import redis
import numpy as np

r = redis.Redis(host='redis', port=6379, db=0)
window_size = 20
entry_threshold = 2
exit_threshold = 0.5
tlt_prices, tltw_prices = [], []

def fractional_kelly(returns, fraction=0.5):
    mean_return = np.mean(returns)
    var_return = np.var(returns)
    kelly_fraction = mean_return / var_return
    return fraction * kelly_fraction

def pairs_trading():
    while True:
        tlt_price = float(r.hget("prices", "TLT"))
        tltw_price = float(r.hget("prices", "TLTW"))
        spread = tlt_price - tltw_price

        tlt_prices.append(tlt_price)
        tltw_prices.append(tltw_price)

        if len(tlt_prices) > window_size:
            tlt_prices.pop(0)
            tltw_prices.pop(0)

        if len(tlt_prices) == window_size:
            mean_spread = np.mean([t - w for t, w in zip(tlt_prices, tltw_prices)])
            std_spread = np.std([t - w for t, w in zip(tlt_prices, tltw_prices)])
            z_score = (spread - mean_spread) / std_spread

            if z_score > entry_threshold:
                print("Signal: Short TLT, Buy TLTW")
                r.set("signal:TLT", "SELL")
                r.set("signal:TLTW", "BUY")
            elif z_score < -entry_threshold:
                print("Signal: Buy TLT, Short TLTW")
                r.set("signal:TLT", "BUY")
                r.set("signal:TLTW", "SELL")
            elif abs(z_score) < exit_threshold:
                print("Signal: Close positions")
                r.delete("signal:TLT")
                r.delete("signal:TLTW")

pairs_trading()
