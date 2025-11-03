import React, { useEffect, useMemo, useState } from "react";
import WebApp from "@twa-dev/sdk";
import { getCoins, getPrice, getOHLC, getNews, getAnalysis } from "./api";
import Chart from "./components/Chart";
import NewsList from "./components/NewsList";
import RiskPanel from "./components/RiskPanel";

export default function App() {
    const url = new URL(window.location.href);
    const initialCoin = url.searchParams.get("coin") || "bitcoin";
    
    const [coins, setCoins] = useState([]);
    const [coin, setCoin] = useState(initialCoin);
    const [tab, setTab] = useState("charts"); // charts | news | risks
    const [ohlc, setOHLC] = useState([]);
    const [price, setPrice] = useState(null);
    const [news, setNews] = useState([]);
    const [analysis, setAnalysis] = useState(null);
    const [q, setQ] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        WebApp.ready();
        WebApp.expand();
    }, []);

    useEffect(() => {
        getCoins()
            .then(setCoins)
            .catch((error) => {
                console.error("Ошибка загрузки монет:", error);
                setError(`Ошибка загрузки монет: ${error.message}`);
            });
    }, []);

    useEffect(() => {
        setLoading(true);
        (async () => {
            try {
                const [ohlcData, priceData, newsData, analysisData] = await Promise.all([
                    getOHLC(coin, 30),
                    getPrice(coin),
                    getNews(coin),
                    getAnalysis(coin),
                ]);
                setOHLC(ohlcData);
                setPrice(priceData);
                setNews(newsData);
                setAnalysis(analysisData);
            } catch (error) {
                console.error("Ошибка загрузки данных:", error);
                const errorMsg = error.message || "Неизвестная ошибка";
                
                // Более детальное сообщение об ошибке
                if (errorMsg.includes("NetworkError") || errorMsg.includes("Failed to fetch")) {
                    const apiUrl = import.meta.env.VITE_API || "https://cma-crypto-miniapp.onrender.com";
                    setError(`Ошибка подключения к API: ${apiUrl}. Проверьте, что API доступен.`);
                } else {
                    setError(`Ошибка загрузки: ${errorMsg}`);
                }
            } finally {
                setLoading(false);
            }
        })();
    }, [coin]);

    const filtered = useMemo(() => {
        if (!q) return [];
        return coins.filter((c) =>
            (c.name + c.symbol + c.id).toLowerCase().includes(q.toLowerCase())
        );
    }, [coins, q]);

    const currentCoinInfo = coins.find((c) => c.id === coin);

    return (
        <div style={{ padding: 12, fontFamily: "system-ui" }}>
            {error && (
                <div style={{ 
                    padding: 12, 
                    backgroundColor: "#fee", 
                    border: "1px solid #fcc", 
                    borderRadius: 6, 
                    marginBottom: 12,
                    color: "#c00"
                }}>
                    {error}
                </div>
            )}
            <div style={{ marginBottom: 12 }}>
                <input
                    placeholder="Поиск: bitcoin / btc"
                    value={q}
                    onChange={(e) => setQ(e.target.value)}
                    style={{
                        width: "100%",
                        padding: 8,
                        borderRadius: 6,
                        border: "1px solid #ddd",
                        fontSize: 14,
                    }}
                />
                {q && filtered.length > 0 && (
                    <div
                        style={{
                            border: "1px solid #eee",
                            borderRadius: 8,
                            marginTop: 4,
                            backgroundColor: "#fff",
                            boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
                        }}
                    >
                        {filtered.slice(0, 8).map((c) => (
                            <div
                                key={c.id}
                                onClick={() => {
                                    setCoin(c.id);
                                    setQ("");
                                }}
                                style={{
                                    padding: 12,
                                    cursor: "pointer",
                                    borderBottom: "1px solid #eee",
                                }}
                                onMouseEnter={(e) => {
                                    e.target.style.backgroundColor = "#f5f5f5";
                                }}
                                onMouseLeave={(e) => {
                                    e.target.style.backgroundColor = "#fff";
                                }}
                            >
                                <strong>{c.symbol}</strong> — {c.name}
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {currentCoinInfo && (
                <div style={{ marginBottom: 12, fontSize: 18, fontWeight: 600 }}>
                    {currentCoinInfo.symbol} — {currentCoinInfo.name}
                </div>
            )}

            <div
                style={{
                    display: "flex",
                    gap: 8,
                    marginTop: 10,
                    marginBottom: 16,
                    flexWrap: "wrap",
                }}
            >
                <button
                    onClick={() => setTab("news")}
                    style={{
                        padding: "8px 16px",
                        borderRadius: 6,
                        border: "1px solid #ddd",
                        backgroundColor: tab === "news" ? "#007bff" : "#fff",
                        color: tab === "news" ? "#fff" : "#000",
                        cursor: "pointer",
                    }}
                >
                    Новости
                </button>
                <button
                    onClick={() => setTab("charts")}
                    style={{
                        padding: "8px 16px",
                        borderRadius: 6,
                        border: "1px solid #ddd",
                        backgroundColor: tab === "charts" ? "#007bff" : "#fff",
                        color: tab === "charts" ? "#fff" : "#000",
                        cursor: "pointer",
                    }}
                >
                    Графики
                </button>
                <button
                    onClick={() => setTab("risks")}
                    style={{
                        padding: "8px 16px",
                        borderRadius: 6,
                        border: "1px solid #ddd",
                        backgroundColor: tab === "risks" ? "#007bff" : "#fff",
                        color: tab === "risks" ? "#fff" : "#000",
                        cursor: "pointer",
                    }}
                >
                    Риски
                </button>
                {price && (
                    <span
                        style={{
                            marginLeft: "auto",
                            fontSize: 14,
                            fontWeight: 600,
                            color: (price.change_24h || 0) >= 0 ? "#28a745" : "#dc3545",
                        }}
                    >
                        ${price.usd.toLocaleString()} (
                        {((price.change_24h || 0) >= 0 ? "+" : "")}
                        {(price.change_24h || 0).toFixed(2)}%)
                    </span>
                )}
            </div>

            {loading && <div>Загрузка...</div>}

            {tab === "charts" && <Chart data={ohlc} />}
            {tab === "news" && <NewsList items={news} />}
            {tab === "risks" && <RiskPanel analysis={analysis} />}
        </div>
    );
}

