// API URL: в продакшене используем переменную окружения или дефолтный URL
// Для Telegram WebApp нужно использовать публичный URL, не localhost!
const API = import.meta.env.VITE_API || (import.meta.env.PROD 
  ? "https://your-api-domain.com"  // Замените на ваш продакшен API URL
  : (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
      ? "http://localhost:8081"  // Только для локальной разработки
      : "https://your-api-domain.com"));  // Для Telegram нужно использовать публичный URL

export async function getCoins() {
    return (await fetch(`${API}/coins`)).json();
}

export async function getPrice(id) {
    return (await fetch(`${API}/price/${id}`)).json();
}

export async function getOHLC(id, days = 30) {
    return (await fetch(`${API}/ohlc/${id}?days=${days}`)).json();
}

export async function getNews(id) {
    return (await fetch(`${API}/news/${id}`)).json();
}

export async function getAnalysis(id) {
    return (await fetch(`${API}/analysis/${id}`, { method: "POST" })).json();
}

