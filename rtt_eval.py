import asyncio
import sys, time
import pandas as pd
import ccxt.pro as ccxtpro

pd.set_option('display.float_format', lambda x: '%.2f' % x)


async def eval_rtt_by_ticker(exchanges):
    exs = [getattr(ccxtpro, exchange)() for exchange in exchanges]
    ex_rtts = {}
    for ex in exs:
        print("eval {}...".format(ex.id))
        await ex.fetch_ticker("BTC/USDT")
        await asyncio.sleep(5)
        rtts = []
        for i in range(50):
            start = time.perf_counter()
            ticker = await ex.fetch_ticker("BTC/USDT")
            end = time.perf_counter()
            rtts.append((end - start) * 1000)
            await asyncio.sleep(1)
        ex_rtts[ex.id] = rtts
        await ex.close()
    df = pd.DataFrame(ex_rtts)
    print(df.describe())


if __name__ == '__main__':
    exchanges = sys.argv[1:]
    asyncio.run(eval_rtt_by_ticker(exchanges))
