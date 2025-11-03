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


# Статичные новости для демо
STATIC_NEWS = {
    "bitcoin": [
        {
            "title": "This Is Crazy'—Elon Musk Issues Serious $38 Trillion U.S. 'Bankruptcy' Warning Amid Growing Bitcoin Price Crash Fears",
            "source": "Forbes",
            "url": "https://www.forbes.com/sites/billybambrough/2025/11/03/this-is-crazy-elon-musk-issues-serious-38-trillion-us-bankruptcy-warning-amid-growing-bitcoin-price-crash-fears/",
            "published_at": "2025-11-03T08:19:00Z"
        },
        {
            "title": "Bitcoin Price Surges Past $126,000 as Traders Brace for Federal Reserve Policy Shift",
            "source": "CoinDesk",
            "url": "https://www.coindesk.com/bitcoin-price-surge",
            "published_at": "2025-11-02T10:00:00Z"
        },
        {
            "title": "Institutional Investors Pour $2 Billion Into Bitcoin ETFs in October",
            "source": "Bloomberg Crypto",
            "url": "https://www.bloomberg.com/bitcoin-etf-inflows",
            "published_at": "2025-11-01T14:30:00Z"
        },
        {
            "title": "Bitcoin Mining Difficulty Hits All-Time High as Hash Rate Continues to Grow",
            "source": "The Block",
            "url": "https://www.theblock.co/bitcoin-mining-difficulty",
            "published_at": "2025-10-31T09:15:00Z"
        },
        {
            "title": "Major Banks Announce Bitcoin Custody Services for Institutional Clients",
            "source": "Reuters",
            "url": "https://www.reuters.com/bitcoin-custody-services",
            "published_at": "2025-10-30T16:45:00Z"
        }
    ],
    "ethereum": [
        {
            "title": "Ethereum 2.0 Staking Reaches 50 Million ETH Milestone",
            "source": "Ethereum Foundation",
            "url": "https://ethereum.org/eth2-staking-milestone",
            "published_at": "2025-11-03T07:00:00Z"
        },
        {
            "title": "Major DeFi Protocol Launches on Ethereum Layer 2",
            "source": "DeFi Pulse",
            "url": "https://defipulse.com/ethereum-l2-launch",
            "published_at": "2025-11-02T12:00:00Z"
        }
    ],
    "solana": [
        {
            "title": "Solana Network Processes Record 100 Million Transactions in 24 Hours",
            "source": "Solana Foundation",
            "url": "https://solana.org/record-transactions",
            "published_at": "2025-11-03T06:00:00Z"
        }
    ]
}

async def fetch_news(id: str, limit: int = 20):
    curr = SYMBOL_MAP.get(id, "BTC")
    
    # Используем статичные новости для демо
    print(f"[News] Using static news for {id} (demo mode)")
    static_news = STATIC_NEWS.get(id, [])
    
    if static_news:
        result = static_news[:limit]
        print(f"[News] Returning {len(result)} static news items for {id}")
        return result
    
    # Если нет статичных новостей, возвращаем пустой список
    print(f"[News] No static news available for {id}, returning empty list")
    return []
    
    # Оригинальный код для API (закомментирован для демо)
    """
    if not API_KEY:
        print(f"[News] WARNING: CRYPTOPANIC_KEY не установлен!")
        return []
    
    # Developer план имеет ограничения: 24 часа задержка, 100 req/mo
    # Пробуем разные фильтры для получения новостей
    # CryptoPanic API требует auth_token в параметрах запроса
    params = {
        "auth_token": API_KEY,
        "currencies": curr,
        "filter": "hot",  # Попробуем "hot" для получения популярных новостей
        "public": "true",
    }
    
    # Проверяем, что API_KEY действительно установлен
    if not API_KEY or len(API_KEY) == 0:
        print(f"[News] ERROR: API_KEY is empty or not set!")
        return []
    
    print(f"[News] API Key length: {len(API_KEY) if API_KEY else 0}")
    print(f"[News] API Key set: {bool(API_KEY)}")
    print(f"[News] API Key preview: {API_KEY[:5]}..." if API_KEY and len(API_KEY) > 5 else "N/A")
    print(f"[News] Request params: currencies={curr}, filter=hot")
    print(f"[News] Request params dict: auth_token={'SET' if params.get('auth_token') else 'MISSING'}, currencies={params.get('currencies')}, filter={params.get('filter')}")
    
    print(f"[News] Fetching news for {id} (symbol: {curr})")
    
    try:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as c:
            print(f"[News] Request URL: {BASE}")
            print(f"[News] Full request URL with params: {BASE}?auth_token={'***' if API_KEY else 'MISSING'}&currencies={curr}&filter=hot&public=true")
            r = await c.get(BASE, params=params)
            print(f"[News] Response status: {r.status_code}")
            print(f"[News] Response URL (after redirects): {r.url}")
            
            # Проверяем, есть ли ошибка в ответе (даже если статус 200)
            try:
                response_data = r.json()
                if isinstance(response_data, dict) and response_data.get("status") == "api_error":
                    error_info = response_data.get('info', 'Unknown error')
                    print(f"[News] API error in response (status={r.status_code}): {error_info}")
                    return []  # Возвращаем пустой список при ошибке API
            except Exception as e:
                print(f"[News] Error parsing response JSON: {e}")
            
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
                print(f"[News] Retrying without filter parameter")
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
