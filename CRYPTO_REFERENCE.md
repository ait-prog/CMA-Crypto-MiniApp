# Справочник криптовалют

Список поддерживаемых криптовалют и их ID для CoinGecko API:

| Символ | Название | CoinGecko ID | Использование в поиске |
|--------|----------|--------------|------------------------|
| BTC | Bitcoin | `bitcoin` | "bitcoin", "btc", "биткоин" |
| ETH | Ethereum | `ethereum` | "ethereum", "eth", "эфир" |
| SOL | Solana | `solana` | "solana", "sol" |
| BNB | BNB | `binancecoin` | "binancecoin", "bnb" |
| XRP | XRP | `ripple` | "ripple", "xrp" |
| ADA | Cardano | `cardano` | "cardano", "ada" |
| DOGE | Dogecoin | `dogecoin` | "dogecoin", "doge" |
| AVAX | Avalanche | `avalanche-2` | "avalanche", "avax" |
| TON | TON | `the-open-network` | "ton", "the-open-network" |
| TRX | TRON | `tron` | "tron", "trx" |

## Добавление новых монет

Чтобы добавить новую криптовалюту:

1. Откройте `api/services/coingecko.py`
2. Добавьте в список `COINS`:
   ```python
   {"id": "coin-id", "symbol": "SYMBOL", "name": "Name"}
   ```
3. Добавьте маппинг символа в `api/services/news.py`:
   ```python
   "coin-id": "SYMBOL",
   ```
4. Перезапустите API

## CoinGecko ID

CoinGecko ID можно найти на https://www.coingecko.com/:
1. Найдите монету
2. Откройте страницу монеты
3. ID находится в URL: `https://www.coingecko.com/en/coins/{ID}`

## Примеры использования API

```bash
# Получить цену Bitcoin
curl http://localhost:8080/price/bitcoin

# Получить график Ethereum за 90 дней
curl http://localhost:8080/ohlc/ethereum?days=90

# Получить новости о Solana
curl http://localhost:8080/news/solana

# Получить анализ Bitcoin
curl -X POST http://localhost:8080/analysis/bitcoin
```

