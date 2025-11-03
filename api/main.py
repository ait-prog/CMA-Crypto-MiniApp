from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from services import coingecko, news as news_svc, indicators, llm4web3_client

app = FastAPI(title="Crypto MiniApp API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
def health():
    return {"ok": True}


@app.get("/coins")
def coins():
    return coingecko.COINS


@app.get("/price/{coin_id}")
async def price(coin_id: str):
    try:
        data = await coingecko.simple_price(coin_id)
        if coin_id not in data:
            raise HTTPException(404, "unknown coin")
        d = data[coin_id]
        return {"usd": d["usd"], "change_24h": d.get("usd_24h_change")}
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/ohlc/{coin_id}")
async def get_ohlc(coin_id: str, days: int = 30):
    try:
        data = await coingecko.ohlc(coin_id, days)
        return [
            {"t": row[0], "o": row[1], "h": row[2], "l": row[3], "c": row[4]}
            for row in data
        ]
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/news/{coin_id}")
async def news(coin_id: str, limit: int = 10):
    try:
        return await news_svc.fetch_news(coin_id, limit)
    except Exception as e:
        raise HTTPException(500, str(e))


@app.post("/analysis/{coin_id}")
async def get_analysis(coin_id: str):
    try:
        ohlc_data = await coingecko.ohlc(coin_id, 90)
        closes = pd.Series([x[4] for x in ohlc_data])
        
        metrics = {
            "rsi": indicators.rsi(closes, 14),
            "ma20": indicators.ma(closes, 20),
            "ma50": indicators.ma(closes, 50),
            "vol30": indicators.realized_vol(closes, 30),
            "dd30": indicators.max_drawdown(closes, 30),
        }
        
        nw = await news_svc.fetch_news(coin_id, 5)
        llm = await llm4web3_client.analyze_with_llm(coin_id, metrics, nw)
        
        # базовый сигнал MA
        signal = "bullish" if metrics["ma20"] > metrics["ma50"] else "bearish"
        
        return {"metrics": metrics, "signal": signal, "llm": llm}
    except Exception as e:
        raise HTTPException(500, str(e))

