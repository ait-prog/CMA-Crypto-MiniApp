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
    async with httpx.AsyncClient(timeout=10) as c:
        r = await c.get(
            f"{BASE}/simple/price",
            params={"ids": id, "vs_currencies": "usd", "include_24hr_change": "true"}
        )
        r.raise_for_status()
        return r.json()


async def ohlc(id: str, days: int = 30):
    async with httpx.AsyncClient(timeout=10) as c:
        r = await c.get(
            f"{BASE}/coins/{id}/ohlc",
            params={"vs_currency": "usd", "days": days}
        )
        r.raise_for_status()
        # формат: [timestamp, open, high, low, close]
        return r.json()

