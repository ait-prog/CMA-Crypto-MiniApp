# Интеграция с LLM4Web3

## Формат запроса

Ваша LLM4Web3 модель должна принимать POST запросы на эндпоинт, указанный в `LLM4WEB3_URL`.

### Входные данные

```json
{
  "coin": "bitcoin",
  "metrics": {
    "rsi": 65.5,
    "ma20": 45000.0,
    "ma50": 42000.0,
    "vol30": 0.35,
    "dd30": -0.15
  },
  "news": [
    {
      "title": "Bitcoin достиг новых высот",
      "source": "CryptoNews",
      "url": "https://...",
      "published_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

### Выходные данные

```json
{
  "summary": "Bitcoin показывает умеренный риск. Технические индикаторы указывают на бычий тренд с MA20 выше MA50. RSI на уровне 65.5 указывает на умеренную перекупленность. Волатильность на уровне 35% годовых. Рекомендуется осторожность при входе в позицию.",
  "risk_level": "умеренный"
}
```

## Пример сервера LLM4Web3 на FastAPI

```python
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class AnalysisRequest(BaseModel):
    coin: str
    metrics: dict
    news: list

class AnalysisResponse(BaseModel):
    summary: str
    risk_level: str

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(
    request: AnalysisRequest,
    authorization: Optional[str] = Header(None)
):
    # Проверка токена (если нужна)
    token = authorization.replace("Bearer ", "") if authorization else None
    # ... ваша логика проверки токена ...
    
    # Ваша LLM логика здесь
    coin = request.coin
    rsi = request.metrics.get("rsi", 50)
    ma20 = request.metrics.get("ma20", 0)
    ma50 = request.metrics.get("ma50", 0)
    vol30 = request.metrics.get("vol30", 0)
    dd30 = request.metrics.get("dd30", 0)
    news_items = request.news
    
    # Пример анализа с помощью вашей LLM
    summary = f"{coin.upper()}: "
    
    if rsi > 70:
        summary += "Высокая перекупленность. "
        risk = "высокий"
    elif rsi < 30:
        summary += "Перепроданность, возможен отскок. "
        risk = "низкий"
    else:
        summary += "Нейтральная зона RSI. "
        risk = "умеренный"
    
    if ma20 > ma50:
        summary += "Бычий тренд подтверждается. "
    else:
        summary += "Медвежий тренд. "
    
    if vol30 > 0.5:
        summary += "Высокая волатильность требует осторожности."
        risk = "высокий" if risk == "умеренный" else risk
    else:
        summary += "Волатильность в нормальном диапазоне."
    
    if news_items:
        summary += f" Последние новости: {len(news_items)} статей."
    
    return AnalysisResponse(
        summary=summary,
        risk_level=risk
    )
```

## Локальный запуск LLM4Web3 сервера

1. Создайте файл `llm4web3_server.py` с кодом выше
2. Установите зависимости:
   ```bash
   pip install fastapi uvicorn pydantic
   ```
3. Запустите сервер:
   ```bash
   uvicorn llm4web3_server:app --host 0.0.0.0 --port 8001
   ```
4. Обновите `.env`:
   ```env
   LLM4WEB3_URL=http://localhost:8001
   LLM4WEB3_TOKEN=your_secret_token
   ```

## Без LLM сервера (эвристический анализ)

Если `LLM4WEB3_URL` не установлен, система использует встроенную эвристику:

- RSI > 70 → "высокий (перекупленность)"
- RSI < 30 → "повышенная волатильность/перепроданность"
- MA20 > MA50 → бычий тренд
- MA20 < MA50 → медвежий тренд

## Тестирование интеграции

```bash
curl -X POST http://localhost:8001/analyze \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_token" \
  -d '{
    "coin": "bitcoin",
    "metrics": {
      "rsi": 65.5,
      "ma20": 45000,
      "ma50": 42000,
      "vol30": 0.35,
      "dd30": -0.15
    },
    "news": []
  }'
```

Ожидаемый ответ:
```json
{
  "summary": "...",
  "risk_level": "умеренный"
}
```

