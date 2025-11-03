import httpx
import os
from pathlib import Path

# Загружаем переменные окружения из .env
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent.parent / '.env'
    load_dotenv(env_path)
except ImportError:
    pass
except Exception:
    pass

BASE = "https://cryptopanic.com/api/v1/posts"

API_KEY = os.getenv("CRYPTOPANIC_KEY", "")

SYMBOL_MAP = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "solana": "SOL",
    "binancecoin": "BNB",
    "ripple": "XRP",
    "cardano": "ADA",
    "dogecoin": "DOGE",
    "avalanche-2": "AVAX",
    "the-open-network": "TON",
    "tron": "TRX",
}


async def fetch_news(id: str, limit: int = 20):
    curr = SYMBOL_MAP.get(id, "BTC")
    
    if not API_KEY:
        print(f"[News] WARNING: CRYPTOPANIC_KEY не установлен!")
        return []
    
    # Developer план имеет ограничения: 24 часа задержка, 100 req/mo
    # Пробуем разные фильтры для получения новостей
    params = {
        "auth_token": API_KEY,
        "currencies": curr,
        "filter": "hot",  # Попробуем "hot" для получения популярных новостей
        "public": "true",
    }
    
    print(f"[News] API Key length: {len(API_KEY)}")
    print(f"[News] Request params: currencies={curr}, filter=hot")
    
    print(f"[News] Fetching news for {id} (symbol: {curr})")
    print(f"[News] API_KEY: {'SET' if API_KEY else 'NOT SET'}")
    
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            print(f"[News] Request URL: {BASE}")
            r = await c.get(BASE, params=params)
            print(f"[News] Response status: {r.status_code}")
            
            if r.status_code != 200:
                print(f"[News] Error response status: {r.status_code}")
                print(f"[News] Error response body: {r.text[:500]}")
                return []
            
            try:
                response_data = r.json()
                print(f"[News] Response type: {type(response_data)}")
            except Exception as e:
                print(f"[News] Error parsing JSON: {e}")
                print(f"[News] Response text: {r.text[:500]}")
                return []
            
            if not isinstance(response_data, dict):
                print(f"[News] Response is not a dict: {response_data}")
                return []
            
            print(f"[News] Response keys: {list(response_data.keys())}")
            data = response_data.get("results", [])
            print(f"[News] Total results: {len(data)}")
            
            if not data:
                print("[News] No results in response")
                # Попробуем без фильтра
                params_no_filter = {
                    "auth_token": API_KEY,
                    "currencies": curr,
                    "public": "true",
                }
                r2 = await c.get(BASE, params=params_no_filter)
                if r2.status_code == 200:
                    try:
                        response_data2 = r2.json()
                        data = response_data2.get("results", [])
                        print(f"[News] Results without filter: {len(data)}")
                    except Exception as e:
                        print(f"[News] Error parsing JSON (no filter): {e}")
                        print(f"[News] Response text: {r2.text[:500]}")
                        data = []
            
                   result = []
                   for x in data[:limit]:
                       try:
                           if not isinstance(x, dict):
                               print(f"[News] Skipping invalid news item: {x}")
                               continue
                           result.append({
                               "title": x.get("title", "No title"),
                               "source": x.get("source", {}).get("title", "Unknown") if isinstance(x.get("source"), dict) else "Unknown",
                               "url": x.get("url", "#"),
                               "published_at": x.get("published_at", ""),
                           })
                       except Exception as e:
                           print(f"[News] Error parsing news item: {e}")
                           print(f"[News] Item data: {x}")
                           continue
                   
                   print(f"[News] Returning {len(result)} news items")
                   if len(result) == 0:
                       print(f"[News] WARNING: No news items parsed from {len(data)} results")
                   return result
    except Exception as e:
        print(f"[News] API error: {e}")
        import traceback
        traceback.print_exc()
        return []
