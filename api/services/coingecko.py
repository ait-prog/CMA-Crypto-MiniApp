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


# Статичные цены для демо
STATIC_PRICES = {
    "bitcoin": {"bitcoin": {"usd": 125430.50, "usd_24h_change": 2.45}},
    "ethereum": {"ethereum": {"usd": 3420.75, "usd_24h_change": 1.87}},
    "solana": {"solana": {"usd": 145.20, "usd_24h_change": 3.12}},
    "binancecoin": {"binancecoin": {"usd": 615.30, "usd_24h_change": 0.92}},
    "ripple": {"ripple": {"usd": 0.58, "usd_24h_change": -0.45}},
    "cardano": {"cardano": {"usd": 0.52, "usd_24h_change": 1.23}},
    "dogecoin": {"dogecoin": {"usd": 0.18, "usd_24h_change": 2.15}},
    "avalanche-2": {"avalanche-2": {"usd": 28.45, "usd_24h_change": 1.56}},
    "the-open-network": {"the-open-network": {"usd": 6.78, "usd_24h_change": 0.89}},
    "tron": {"tron": {"usd": 0.12, "usd_24h_change": -0.23}}
}

async def simple_price(id: str):
    # Используем статичные цены для демо
    print(f"[CoinGecko] Using static price for {id} (demo mode)")
    static_data = STATIC_PRICES.get(id)
    
    if static_data:
        print(f"[CoinGecko] Static price data: {static_data}")
        return static_data
    
    # Если нет статичных данных, возвращаем дефолт
    print(f"[CoinGecko] No static price for {id}, using default")
    return {id: {"usd": 0.0, "usd_24h_change": 0.0}}
    
    # Оригинальный код для API (закомментирован для демо)
    """
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
    """


async def ohlc(id: str, days: int = 30):
    # Генерируем статичные OHLC данные для демо
    print(f"[CoinGecko] Generating static OHLC data for {id}, days={days} (demo mode)")
    
    import time
    base_prices = {
        "bitcoin": 125000,
        "ethereum": 3400,
        "solana": 145,
        "binancecoin": 615,
        "ripple": 0.58,
        "cardano": 0.52,
        "dogecoin": 0.18,
        "avalanche-2": 28.45,
        "the-open-network": 6.78,
        "tron": 0.12
    }
    
    base_price = base_prices.get(id, 1000)
    current_time = int(time.time() * 1000)  # миллисекунды
    data_points = min(days * 24, 720)  # Максимум 720 точек (30 дней * 24 часа)
    
    import random
    ohlc_data = []
    for i in range(data_points):
        # Генерируем случайные колебания цены
        hours_ago = data_points - i
        timestamp = current_time - (hours_ago * 3600 * 1000)
        
        # Симулируем цену с небольшими колебаниями
        price_multiplier = 1.0 + (random.random() - 0.5) * 0.1  # ±5% колебания
        close_price = base_price * price_multiplier
        open_price = close_price * (1.0 + (random.random() - 0.5) * 0.02)  # ±1%
        high_price = max(open_price, close_price) * (1.0 + random.random() * 0.02)
        low_price = min(open_price, close_price) * (1.0 - random.random() * 0.02)
        
        ohlc_data.append([
            timestamp,
            open_price,
            high_price,
            low_price,
            close_price
        ])
    
    print(f"[CoinGecko] Generated {len(ohlc_data)} OHLC data points")
    return ohlc_data
    
    # Оригинальный код для API (закомментирован для демо)
    """
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
    """

