from fastapi import FastAPI
from redis import Redis
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = FastAPI()
r = Redis(host='redis', port=6379, db=0)

@app.get("/plot")
def plot_spread():
    tlt_prices = [float(p) for p in r.lrange("prices:TLT", -20, -1)]
    tltw_prices = [float(p) for p in r.lrange("prices:TLTW", -20, -1)]
    spread = [tlt - tltw for tlt, tltw in zip(tlt_prices, tltw_prices)]

    plt.figure(figsize=(10, 6))
    plt.plot(spread, label="TLT ATM Covered Call vs TLTW Spread")
    plt.legend()
    plt.xlabel("Time")
    plt.ylabel("Spread")
    
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    return {"plot": img_base64}
