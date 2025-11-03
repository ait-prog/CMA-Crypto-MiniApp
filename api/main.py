from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pathlib import Path

# Импортируем сервисы с обработкой ошибок
try:
    from services import coingecko, news as news_svc, indicators, llm4web3_client
    print("[API] Services imported successfully")
except Exception as e:
    print(f"[ERROR] Failed to import services: {e}")
    import traceback
    traceback.print_exc()
    # Создаем заглушки для тестирования
    class DummyCoingecko:
        COINS = []
    coingecko = DummyCoingecko()
    news_svc = None
    indicators = None
    llm4web3_client = None

# Загружаем переменные окружения из .env файла
try:
    from dotenv import load_dotenv
    import os
    # Ищем .env файл в корне проекта (на уровень выше)
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path)
    print(f"[API] Загружен .env файл: {env_path.exists()}")
    print(f"[API] CRYPTOPANIC_KEY: {'SET' if os.getenv('CRYPTOPANIC_KEY') else 'NOT SET'}")
except ImportError:
    print("[API] python-dotenv не установлен, используем системные переменные окружения")
except Exception as e:
    print(f"[API] Ошибка загрузки .env: {e}")

import os

# Получаем порт из переменной окружения (для Railway/Render)
PORT = int(os.getenv("PORT", 8080))

app = FastAPI(title="Crypto MiniApp API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Crypto MiniApp API", "version": "1.0.0", "endpoints": ["/healthz", "/coins", "/price/{coin_id}", "/ohlc/{coin_id}", "/news/{coin_id}", "/analysis/{coin_id}", "/docs"]}

@app.get("/healthz")
def health():
    return {"ok": True}


@app.get("/coins")
def coins():
    try:
        return coingecko.COINS
    except Exception as e:
        print(f"[ERROR] Failed to get coins: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Error loading coins: {str(e)}")


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

