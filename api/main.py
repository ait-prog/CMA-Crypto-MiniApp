from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pathlib import Path

# Импортируем сервисы с обработкой ошибок
try:
    print("[API] Starting service imports...")
    from services import coingecko, news as news_svc, indicators, llm4web3_client
    print("[API] Services imported successfully")
    print(f"[API] coingecko: {coingecko}")
    print(f"[API] coingecko.COINS: {len(coingecko.COINS) if hasattr(coingecko, 'COINS') else 'N/A'}")
    print(f"[API] news_svc: {news_svc}")
    print(f"[API] indicators: {indicators}")
    print(f"[API] llm4web3_client: {llm4web3_client}")
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
    print("[API] Using dummy services")

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
    return {
        "message": "Crypto MiniApp API", 
        "version": "1.0.0", 
        "endpoints": ["/healthz", "/coins", "/price/{coin_id}", "/ohlc/{coin_id}", "/news/{coin_id}", "/analysis/{coin_id}", "/docs"],
        "status": "ok"
    }

@app.get("/healthz")
def health():
    return {"ok": True}


@app.get("/coins")
def coins():
    try:
        if not coingecko or not hasattr(coingecko, 'COINS'):
            print("[WARNING] coingecko.COINS is not available, returning default list")
            # Возвращаем дефолтный список монет
            return [
                {"id": "bitcoin", "symbol": "BTC", "name": "Bitcoin"},
                {"id": "ethereum", "symbol": "ETH", "name": "Ethereum"},
                {"id": "solana", "symbol": "SOL", "name": "Solana"},
                {"id": "binancecoin", "symbol": "BNB", "name": "BNB"},
                {"id": "ripple", "symbol": "XRP", "name": "XRP"},
                {"id": "cardano", "symbol": "ADA", "name": "Cardano"},
                {"id": "dogecoin", "symbol": "DOGE", "name": "Dogecoin"},
                {"id": "avalanche-2", "symbol": "AVAX", "name": "Avalanche"},
                {"id": "the-open-network", "symbol": "TON", "name": "TON"},
                {"id": "tron", "symbol": "TRX", "name": "TRON"},
            ]
        if not coingecko.COINS:
            print("[WARNING] coingecko.COINS is empty, returning default list")
            return [
                {"id": "bitcoin", "symbol": "BTC", "name": "Bitcoin"},
                {"id": "ethereum", "symbol": "ETH", "name": "Ethereum"},
                {"id": "solana", "symbol": "SOL", "name": "Solana"},
                {"id": "binancecoin", "symbol": "BNB", "name": "BNB"},
                {"id": "ripple", "symbol": "XRP", "name": "XRP"},
                {"id": "cardano", "symbol": "ADA", "name": "Cardano"},
                {"id": "dogecoin", "symbol": "DOGE", "name": "Dogecoin"},
                {"id": "avalanche-2", "symbol": "AVAX", "name": "Avalanche"},
                {"id": "the-open-network", "symbol": "TON", "name": "TON"},
                {"id": "tron", "symbol": "TRX", "name": "TRON"},
            ]
        return coingecko.COINS
    except Exception as e:
        print(f"[ERROR] Failed to get coins: {e}")
        import traceback
        traceback.print_exc()
        # Возвращаем дефолтный список вместо ошибки
        return [
            {"id": "bitcoin", "symbol": "BTC", "name": "Bitcoin"},
            {"id": "ethereum", "symbol": "ETH", "name": "Ethereum"},
            {"id": "solana", "symbol": "SOL", "name": "Solana"},
            {"id": "binancecoin", "symbol": "BNB", "name": "BNB"},
            {"id": "ripple", "symbol": "XRP", "name": "XRP"},
            {"id": "cardano", "symbol": "ADA", "name": "Cardano"},
            {"id": "dogecoin", "symbol": "DOGE", "name": "Dogecoin"},
            {"id": "avalanche-2", "symbol": "AVAX", "name": "Avalanche"},
            {"id": "the-open-network", "symbol": "TON", "name": "TON"},
            {"id": "tron", "symbol": "TRX", "name": "TRON"},
        ]


@app.get("/price/{coin_id}")
async def price(coin_id: str):
    try:
        print(f"[API] /price/{coin_id} called")
        if not coingecko or not hasattr(coingecko, 'simple_price'):
            print(f"[ERROR] CoinGecko service not available for price/{coin_id}")
            raise HTTPException(500, "CoinGecko service not available")
        print(f"[API] Fetching price for {coin_id}")
        try:
            data = await coingecko.simple_price(coin_id)
            print(f"[API] Price data received: {data}")
        except Exception as e:
            print(f"[ERROR] CoinGecko API error for price/{coin_id}: {e}")
            import traceback
            traceback.print_exc()
            raise
        if coin_id not in data:
            print(f"[ERROR] Coin {coin_id} not found in response: {list(data.keys())}")
            raise HTTPException(404, "unknown coin")
        d = data[coin_id]
        result = {"usd": d["usd"], "change_24h": d.get("usd_24h_change")}
        print(f"[API] Price result: {result}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to get price for {coin_id}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Error fetching price: {str(e)}")


@app.get("/ohlc/{coin_id}")
async def get_ohlc(coin_id: str, days: int = 30):
    try:
        print(f"[API] /ohlc/{coin_id}?days={days} called")
        if not coingecko or not hasattr(coingecko, 'ohlc'):
            print(f"[ERROR] CoinGecko service not available for ohlc/{coin_id}")
            raise HTTPException(500, "CoinGecko service not available")
        print(f"[API] Fetching OHLC for {coin_id}, days={days}")
        try:
            data = await coingecko.ohlc(coin_id, days)
            print(f"[API] OHLC data received, rows: {len(data) if data else 0}")
        except Exception as e:
            print(f"[ERROR] CoinGecko API error for ohlc/{coin_id}: {e}")
            import traceback
            traceback.print_exc()
            raise
        if not data or len(data) == 0:
            print(f"[ERROR] No OHLC data for {coin_id}")
            raise HTTPException(500, "No OHLC data available")
        result = [
            {"t": row[0], "o": row[1], "h": row[2], "l": row[3], "c": row[4]}
            for row in data
        ]
        print(f"[API] OHLC result: {len(result)} rows")
        return result
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to get OHLC for {coin_id}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Error fetching OHLC: {str(e)}")


@app.get("/news/{coin_id}")
async def news(coin_id: str, limit: int = 10):
    try:
        if not news_svc:
            print("[WARNING] news_svc is not available, returning empty list")
            return []
        return await news_svc.fetch_news(coin_id, limit)
    except Exception as e:
        print(f"[ERROR] Failed to get news for {coin_id}: {e}")
        import traceback
        traceback.print_exc()
        # Возвращаем пустой список вместо ошибки
        return []


@app.post("/analysis/{coin_id}")
async def get_analysis(coin_id: str):
    try:
        print(f"[API] Starting analysis for {coin_id}")
        if not coingecko or not hasattr(coingecko, 'ohlc'):
            print(f"[ERROR] CoinGecko service not available for analysis/{coin_id}")
            raise HTTPException(500, "CoinGecko service not available")
        
        print(f"[API] Fetching OHLC data for analysis ({coin_id}, 90 days)")
        ohlc_data = await coingecko.ohlc(coin_id, 90)
        print(f"[API] OHLC data received, rows: {len(ohlc_data) if ohlc_data else 0}")
        
        if not ohlc_data or len(ohlc_data) == 0:
            print(f"[ERROR] No OHLC data for {coin_id}")
            raise HTTPException(500, "No OHLC data available")
        
        closes = pd.Series([x[4] for x in ohlc_data])
        print(f"[API] Calculated closes series, length: {len(closes)}")
        
        if not indicators:
            print(f"[ERROR] Indicators service not available")
            raise HTTPException(500, "Indicators service not available")
        
        print(f"[API] Calculating metrics")
        import math
        
        def safe_float(value):
            """Преобразует недопустимые float значения в None для JSON"""
            try:
                if value is None:
                    return None
                if isinstance(value, (int, float)):
                    if math.isnan(value) or math.isinf(value):
                        print(f"[API] WARNING: Invalid float value detected: {value}, replacing with None")
                        return None
                    return float(value)
                return value
            except Exception as e:
                print(f"[API] ERROR in safe_float: {e}, value: {value}")
                return None
        
        try:
            rsi_val = indicators.rsi(closes, 14)
            print(f"[API] RSI calculated: {rsi_val} (type: {type(rsi_val)})")
        except Exception as e:
            print(f"[API] ERROR calculating RSI: {e}")
            rsi_val = None
        
        try:
            ma20_val = indicators.ma(closes, 20)
            print(f"[API] MA20 calculated: {ma20_val} (type: {type(ma20_val)})")
        except Exception as e:
            print(f"[API] ERROR calculating MA20: {e}")
            ma20_val = None
        
        try:
            ma50_val = indicators.ma(closes, 50)
            print(f"[API] MA50 calculated: {ma50_val} (type: {type(ma50_val)})")
        except Exception as e:
            print(f"[API] ERROR calculating MA50: {e}")
            ma50_val = None
        
        try:
            vol30_val = indicators.realized_vol(closes, 30)
            print(f"[API] VOL30 calculated: {vol30_val} (type: {type(vol30_val)})")
        except Exception as e:
            print(f"[API] ERROR calculating VOL30: {e}")
            vol30_val = None
        
        try:
            dd30_val = indicators.max_drawdown(closes, 30)
            print(f"[API] DD30 calculated: {dd30_val} (type: {type(dd30_val)})")
        except Exception as e:
            print(f"[API] ERROR calculating DD30: {e}")
            dd30_val = None
        
        metrics = {
            "rsi": safe_float(rsi_val),
            "ma20": safe_float(ma20_val),
            "ma50": safe_float(ma50_val),
            "vol30": safe_float(vol30_val),
            "dd30": safe_float(dd30_val),
        }
        print(f"[API] Metrics after safe_float: {metrics}")
        
        # Дополнительная проверка перед возвратом
        for key, value in metrics.items():
            if isinstance(value, float):
                if math.isnan(value) or math.isinf(value):
                    print(f"[API] WARNING: Found invalid float in metrics[{key}]: {value}, replacing with None")
                    metrics[key] = None
        
        nw = []
        if news_svc:
            try:
                print(f"[API] Fetching news for analysis")
                nw = await news_svc.fetch_news(coin_id, 5)
                print(f"[API] News fetched: {len(nw)} items")
            except Exception as e:
                print(f"[WARNING] News unavailable for analysis: {e}")
                pass  # Новости не критичны
        
        llm = None
        if llm4web3_client:
            try:
                print(f"[API] Calling LLM for analysis")
                # Передаем метрики без None для LLM
                llm_metrics = {k: v for k, v in metrics.items() if v is not None}
                llm = await llm4web3_client.analyze_with_llm(coin_id, llm_metrics, nw)
                print(f"[API] LLM analysis received")
                # Проверяем LLM ответ на недопустимые значения
                if isinstance(llm, dict):
                    for key, value in llm.items():
                        if isinstance(value, float):
                            if math.isnan(value) or math.isinf(value):
                                print(f"[API] WARNING: Invalid float in LLM response[{key}]: {value}")
                                llm[key] = None
            except Exception as e:
                print(f"[WARNING] LLM unavailable: {e}")
                pass  # LLM не критичен
        
        # базовый сигнал MA (с проверкой на None)
        ma20 = metrics.get("ma20")
        ma50 = metrics.get("ma50")
        if ma20 is not None and ma50 is not None:
            signal = "bullish" if ma20 > ma50 else "bearish"
        else:
            signal = "neutral"  # Если данные недоступны
        print(f"[API] Analysis complete, signal: {signal}")
        
        # Финальная проверка перед возвратом
        result = {"metrics": metrics, "signal": signal, "llm": llm}
        print(f"[API] Final result before return: metrics keys={list(result['metrics'].keys())}, signal={result['signal']}, llm={'present' if result['llm'] else 'None'}")
        
        # Проверяем каждое значение на недопустимые float
        def clean_dict(d):
            """Рекурсивно очищает словарь от недопустимых float значений"""
            if isinstance(d, dict):
                return {k: clean_dict(v) for k, v in d.items()}
            elif isinstance(d, list):
                return [clean_dict(item) for item in d]
            elif isinstance(d, float):
                if math.isnan(d) or math.isinf(d):
                    return None
                return d
            return d
        
        result = clean_dict(result)
        print(f"[API] Result after cleaning: {result}")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to get analysis for {coin_id}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Error fetching analysis: {str(e)}")

