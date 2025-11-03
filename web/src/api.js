// API URL: в продакшене используем переменную окружения или дефолтный URL
// Для Telegram WebApp нужно использовать публичный URL, не localhost!
const getApiUrl = () => {
    // Если указана переменная окружения - используем её
    if (import.meta.env.VITE_API) {
        return import.meta.env.VITE_API;
    }
    
    // В продакшене (GitHub Pages) используем публичный URL Render
    if (import.meta.env.PROD) {
        // Если не указан VITE_API, используем дефолтный URL Render
        return "https://cma-crypto-miniapp.onrender.com";
    }
    
    // В разработке проверяем hostname
    const hostname = window.location.hostname;
    if (hostname === "localhost" || hostname === "127.0.0.1") {
        // Локальная разработка - можно использовать localhost
        return "http://localhost:8081";
    }
    
    // Если открыто из Telegram или другого домена - используем публичный URL
    console.warn("[API] Используется публичный API URL для Telegram");
    return "https://cma-crypto-miniapp.onrender.com";
};

const API = getApiUrl();

// Логируем используемый API URL для отладки
console.log("[API] Using API URL:", API);

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

