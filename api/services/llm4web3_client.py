import os
import httpx

LLM_ENDPOINT = os.getenv("LLM4WEB3_URL")  # если у тебя HTTP сервис
LLM_TOKEN = os.getenv("LLM4WEB3_TOKEN", "")


async def analyze_with_llm(coin: str, metrics: dict, news: list):
    if not LLM_ENDPOINT:
        # Фоллбэк: короткая эвристика
        risk = "умеренный"
        rsi_val = metrics.get("rsi", 50)
        
        if rsi_val > 70:
            risk = "высокий (перекупленность)"
        elif rsi_val < 30:
            risk = "повышенная волатильность/перепроданность"
            
        ma20 = metrics.get("ma20", 0)
        ma50 = metrics.get("ma50", 0)
        
        signal_note = ""
        if ma20 > ma50:
            signal_note = "Бычий тренд (MA20 выше MA50)"
        else:
            signal_note = "Медвежий тренд (MA20 ниже MA50)"
            
        return {
            "summary": f"{coin.upper()}: риск {risk}. {signal_note}. MA20=${ma20:.2f}, MA50=${ma50:.2f}, RSI={rsi_val:.1f}. Волатильность 30д: {metrics.get('vol30', 0):.2%}.",
            "risk_level": risk,
        }

    # Если есть LLM4WEB3 сервис
    try:
        async with httpx.AsyncClient(timeout=20) as c:
            r = await c.post(
                LLM_ENDPOINT,
                headers={"Authorization": f"Bearer {LLM_TOKEN}"},
                json={"coin": coin, "metrics": metrics, "news": news},
            )
            r.raise_for_status()
            return r.json()
    except Exception as e:
        print(f"LLM4WEB3 error: {e}")
        # Fallback на эвристику
        risk = "умеренный"
        if metrics.get("rsi", 50) > 70:
            risk = "высокий (перекупленность)"
        elif metrics.get("rsi", 50) < 30:
            risk = "повышенная волатильность/перепроданность"
        return {
            "summary": f"{coin.upper()}: риск {risk} на основе технических индикаторов.",
            "risk_level": risk,
        }

