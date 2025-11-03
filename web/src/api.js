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
    try {
        const response = await fetch(`${API}/coins`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error("[API] Error fetching coins:", error);
        // Извлекаем более детальную информацию об ошибке
        let errorMessage = error.message || "Неизвестная ошибка";
        if (error instanceof TypeError && error.message.includes("fetch")) {
            errorMessage = "Ошибка подключения к API. API может быть в режиме сна (Render free tier).";
        } else if (error.message.includes("500")) {
            errorMessage = `Ошибка сервера (500): ${error.message}`;
        }
        throw new Error(errorMessage);
    }
}

export async function getPrice(id) {
    try {
        const response = await fetch(`${API}/price/${id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error(`[API] Error fetching price for ${id}:`, error);
        let errorMessage = error.message || "Неизвестная ошибка";
        if (error.message.includes("500")) {
            errorMessage = `Ошибка сервера (500) при загрузке цены: ${error.message}`;
        }
        throw new Error(errorMessage);
    }
}

export async function getOHLC(id, days = 30) {
    try {
        const response = await fetch(`${API}/ohlc/${id}?days=${days}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error(`[API] Error fetching OHLC for ${id}:`, error);
        let errorMessage = error.message || "Неизвестная ошибка";
        if (error.message.includes("500")) {
            errorMessage = `Ошибка сервера (500) при загрузке графика: ${error.message}`;
        }
        throw new Error(errorMessage);
    }
}

export async function getNews(id) {
    try {
        const response = await fetch(`${API}/news/${id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error(`[API] Error fetching news for ${id}:`, error);
        // Новости не критичны, возвращаем пустой список
        console.warn(`[API] News unavailable for ${id}, returning empty list`);
        return [];
    }
}

export async function getAnalysis(id) {
    try {
        const response = await fetch(`${API}/analysis/${id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error(`[API] Error fetching analysis for ${id}:`, error);
        let errorMessage = error.message || "Неизвестная ошибка";
        if (error.message.includes("500")) {
            errorMessage = `Ошибка сервера (500) при загрузке анализа: ${error.message}`;
        }
        throw new Error(errorMessage);
    }
}

