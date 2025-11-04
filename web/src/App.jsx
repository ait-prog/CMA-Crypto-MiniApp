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
            .then((data) => setCoins(data))
            .catch((error) => {
                console.error("[App] Error loading coins:", error);
                const errorMsg = error.message || "Неизвестная ошибка";
                if (errorMsg.includes("NetworkError") || errorMsg.includes("Failed to fetch")) {
                    setError(`Ошибка подключения к API. Попробуйте обновить страницу через несколько секунд.`);
                } else {
                    setError(`Ошибка загрузки монет: ${errorMsg}`);
                }
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
                if (errorMsg.includes("NetworkError") || errorMsg.includes("Failed to fetch")) {
                    const apiUrl = import.meta.env.VITE_API || "https://cma-crypto-miniapp.onrender.com";
                    setError(`Ошибка подключения к API: ${apiUrl}.`);
                } else if (errorMsg.includes("500")) {
                    setError(`Ошибка сервера (500): ${errorMsg}.`);
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
        <div className="container mx-auto p-4">
            {/* Header */}
            <header className="decorative-header mb-6 flex items-center gap-4">
                <div className="flex-none">
                    <div className="px-3 py-2 rounded-md bg-gradient-to-r from-black via-gray-900 to-black glass-card accent-glow border-0">
                        <div className="text-sm text-gray-300">CMA Crypto</div>
                        <div className="text-xl font-bold text-white">Дашборд</div>
                    </div>
                </div>
                <div className="flex-1">
                    <div className="w-full relative">
                        <input
                            placeholder="Поиск: bitcoin / btc"
                            value={q}
                            onChange={(e) => setQ(e.target.value)}
                            className="w-full px-3 py-2 rounded-lg bg-gray-800 border border-gray-700 text-gray-200 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-red-600"
                        />
                        {q && filtered.length > 0 && (
                            <div className="absolute left-0 right-0 mt-2 bg-gray-900 border border-gray-800 rounded-lg overflow-hidden z-20">
                                {filtered.slice(0, 8).map((c) => (
                                    <div
                                        key={c.id}
                                        onClick={() => { setCoin(c.id); setQ(""); }}
                                        className="px-3 py-2 cursor-pointer hover:bg-gray-800 text-gray-200 border-b border-gray-800"
                                    >
                                        <strong className="text-sm text-red-400 mr-2">{c.symbol}</strong>
                                        <span className="text-sm text-gray-300">{c.name}</span>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
                <div className="flex-none">
                    {price && (
                        <div className={`px-3 py-2 rounded-md text-sm font-semibold ${price.change_24h >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                            ${price.usd.toLocaleString()} {price.change_24h >= 0 ? '+' : ''}{(price.change_24h || 0).toFixed(2)}%
                        </div>
                    )}
                </div>
            </header>

            {error && (
                <div className="mb-4 p-3 rounded-md bg-red-900 text-red-200 border border-red-700">
                    {error}
                </div>
            )}

            {/* Tabs */}
            <div className="flex gap-3 items-center mb-4 flex-wrap">
                <button onClick={() => setTab('news')} className={`px-4 py-2 rounded-lg text-sm font-medium ${tab==='news' ? 'bg-red-600 text-white' : 'bg-gray-800 text-gray-200'}`}>Новости</button>
                <button onClick={() => setTab('charts')} className={`px-4 py-2 rounded-lg text-sm font-medium ${tab==='charts' ? 'bg-red-600 text-white' : 'bg-gray-800 text-gray-200'}`}>Графики</button>
                <button onClick={() => setTab('risks')} className={`px-4 py-2 rounded-lg text-sm font-medium ${tab==='risks' ? 'bg-red-600 text-white' : 'bg-gray-800 text-gray-200'}`}>Риски</button>
                <div className="ml-auto text-gray-400 text-sm">{currentCoinInfo ? `${currentCoinInfo.symbol} — ${currentCoinInfo.name}` : 'Выберите монету'}</div>
            </div>

            {/* Content */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <main className="md:col-span-2 space-y-4">
                    <div className="glass-card p-4 rounded-lg accent-border">
                        {loading ? <div className="text-center text-gray-400 py-8">Загрузка...</div> : (tab === 'charts' ? <Chart data={ohlc} /> : (tab === 'news' ? <NewsList items={news} /> : <RiskPanel analysis={analysis} />))}
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                        <div className="glass-card p-4 rounded-lg">
                            <div className="text-xs text-gray-400">Доп. метрика</div>
                            <div className="text-lg font-semibold text-white">—</div>
                        </div>
                        <div className="glass-card p-4 rounded-lg">
                            <div className="text-xs text-gray-400">Другая метрика</div>
                            <div className="text-lg font-semibold text-white">—</div>
                        </div>
                    </div>
                </main>

                <aside className="space-y-4 md:sticky md:top-6">
                    <div className="glass-card p-3 rounded-lg">
                        <div className="text-sm text-gray-300 font-semibold">Монеты</div>
                        <div className="mt-2 space-y-1 max-h-48 sm:max-h-64 overflow-auto">
                            {coins.slice(0, 12).map((c) => (
                                <div key={c.id} onClick={() => setCoin(c.id)} className={`flex items-center justify-between p-2 rounded-md cursor-pointer hover:bg-gray-800 ${c.id===coin? 'bg-gray-800 ring-1 ring-red-600':''}`}>
                                    <div className="text-sm text-gray-200"><strong className="text-red-400 mr-2">{c.symbol}</strong>{c.name}</div>
                                    <div className="text-xs text-gray-400">{c.market_cap_rank}</div>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="glass-card p-4 rounded-lg">
                        <div className="text-sm text-gray-300 font-semibold">Риски / Анализ</div>
                        <div className="mt-2 text-sm text-gray-400">Быстрый обзор и LLM-анализ справа в основном окне.</div>
                    </div>
                </aside>
            </div>

            {/* Footer intentionally removed for a cleaner, more minimal UI */}
        </div>
    );
}

