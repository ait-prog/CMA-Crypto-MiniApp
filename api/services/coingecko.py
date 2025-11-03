import httpx

BASE = "https://api.coingecko.com/api/v3"

COINS = [
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


async def simple_price(id: str):
    try:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as c:
            url = f"{BASE}/simple/price"
            params = {"ids": id, "vs_currencies": "usd", "include_24hr_change": "true"}
            print(f"[CoinGecko] Fetching price for {id}")
            print(f"[CoinGecko] URL: {url}, params: {params}")
            r = await c.get(url, params=params)
            print(f"[CoinGecko] Response status: {r.status_code}")
            r.raise_for_status()
            data = r.json()
            print(f"[CoinGecko] Price data received: {data}")
            return data
    except httpx.HTTPStatusError as e:
        print(f"[CoinGecko] HTTP error: {e.response.status_code} - {e.response.text}")
        raise
    except Exception as e:
        print(f"[CoinGecko] Error fetching price: {e}")
        raise


async def ohlc(id: str, days: int = 30):
    try:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as c:
            url = f"{BASE}/coins/{id}/ohlc"
            params = {"vs_currency": "usd", "days": days}
            print(f"[CoinGecko] Fetching OHLC for {id}, days={days}")
            print(f"[CoinGecko] URL: {url}, params: {params}")
            r = await c.get(url, params=params)
            print(f"[CoinGecko] Response status: {r.status_code}")
            r.raise_for_status()
            data = r.json()
            print(f"[CoinGecko] OHLC data received, rows: {len(data) if isinstance(data, list) else 'N/A'}")
            # формат: [timestamp, open, high, low, close]
            return data
    except httpx.HTTPStatusError as e:
        print(f"[CoinGecko] HTTP error: {e.response.status_code} - {e.response.text}")
        raise
    except Exception as e:
        print(f"[CoinGecko] Error fetching OHLC: {e}")
        raise

