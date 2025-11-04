function Card({ label, value }) {
    return (
        <div className="p-3 rounded-lg glass-card">
            <div className="text-xs text-gray-400 mb-1">{label}</div>
            <div className="text-lg font-semibold text-white">{value}</div>
        </div>
    );
}

export default function RiskPanel({ analysis }) {
    if (!analysis) {
        return <div className="p-6 text-center text-gray-400">Загрузка...</div>;
    }

    const { metrics, signal, llm } = analysis;

    const signalColor = signal === "bullish" ? 'text-green-400' : 'text-red-400';

    const rsiColor = metrics.rsi > 70 ? 'text-red-400' : metrics.rsi < 30 ? 'text-yellow-400' : 'text-green-400';

    return (
        <div className="mt-2 space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <Card label="RSI(14)" value={<span className={rsiColor}>{metrics.rsi?.toFixed(1)}</span>} />
                <Card label="MA20 / MA50" value={`$${metrics.ma20?.toFixed(2)} / $${metrics.ma50?.toFixed(2)}`} />
                <Card label="Vol(30d, ann.)" value={`${(metrics.vol30 * 100)?.toFixed(2)}%`} />
                <Card label="Max DD(30d)" value={<span className="text-red-400">{(metrics.dd30 * 100)?.toFixed(2)}%</span>} />
                <Card label="Сигнал MA" value={<span className={signalColor}>{signal === 'bullish' ? '📈 Бычий' : '📉 Медвежий'}</span>} />
            </div>

            <div className="p-4 rounded-lg glass-card">
                <div className="font-semibold text-white mb-2">📊 LLM4Web3 Анализ:</div>
                <div className="text-sm text-gray-300 leading-relaxed">{llm?.summary || 'Анализ недоступен'}</div>
                {llm?.risk_level && (
                    <div className={`mt-3 inline-block px-3 py-1 rounded-md text-sm font-semibold ${llm.risk_level.includes('высокий') ? 'bg-red-800 text-red-200' : llm.risk_level.includes('низкий') ? 'bg-green-800 text-green-200' : 'bg-yellow-900 text-yellow-200'}`}>
                        Уровень риска: {llm.risk_level}
                    </div>
                )}
            </div>
        </div>
    );
}

