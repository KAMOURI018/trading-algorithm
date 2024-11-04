from ib_async import *
from ib_insync import IB, Stock, util, Option
util.startLoop()
ib = IB()
ib.connect('127.0.0.1', 7497, 1)


tlt = Stock('TLT', 'SMART', 'USD')
tltw = Stock('TLTW', 'SMART', 'USD')
atm_call = Option('TLT', '2024-11-20', 100, 'C', 'SMART')

ib.qualifyContracts(tlt, tltw, atm_call)

def update_data():
    tlt_price = ib.reqMktData(tlt)
    tltw_price = ib.reqMktData(tltw)
    option_data = ib.reqMktData(atm_call, "", True)

    r.hset("prices", "TLT", tlt_price.last)
    r.hset("prices", "TLTW", tltw_price.last)
    r.hmset("options:TLT_ATM_CALL", {
        "price": option_data.last,
        "delta": option_data.delta,
        "theta": option_data.theta,
        "vega": option_data.vega
    })

while True:
    update_data()
    ib.sleep(5)
