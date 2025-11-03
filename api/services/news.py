import httpx
import os

BASE = "https://cryptopanic.com/api/v1/posts/"

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
    params = {
        "auth_token": API_KEY,
        "currencies": curr,
        "filter": "news",
        "public": "true",
    }
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(BASE, params=params)
            r.raise_for_status()
            data = r.json().get("results", [])[:limit]
            return [
                {
                    "title": x["title"],
                    "source": x["source"]["title"],
                    "url": x["url"],
                    "published_at": x["published_at"],
                }
                for x in data
            ]
    except Exception as e:
        # Fallback: возвращаем пустой список если API недоступен
        print(f"News API error: {e}")
        return []

