function Card({ label, value }) {
    return (
        <div
            style={{
                border: "1px solid #eee",
                padding: 12,
                borderRadius: 8,
                backgroundColor: "#fff",
            }}
        >
            <div style={{ opacity: 0.7, fontSize: 12, marginBottom: 4 }}>{label}</div>
            <div style={{ fontSize: 18, fontWeight: 600 }}>{value}</div>
        </div>
    );
}

export default function RiskPanel({ analysis }) {
    if (!analysis) {
        return <div style={{ padding: 20, textAlign: "center" }}>Загрузка...</div>;
    }

    const { metrics, signal, llm } = analysis;

    const signalColor = signal === "bullish" ? "#28a745" : "#dc3545";
    const rsiColor =
        metrics.rsi > 70
            ? "#dc3545"
            : metrics.rsi < 30
            ? "#ffc107"
            : "#28a745";

    return (
        <div style={{ marginTop: 10 }}>
            <div
                style={{
                    display: "grid",
                    gridTemplateColumns: "1fr 1fr",
                    gap: 10,
                    marginBottom: 16,
                }}
            >
                <Card
                    label="RSI(14)"
                    value={
                        <span style={{ color: rsiColor }}>
                            {metrics.rsi?.toFixed(1)}
                        </span>
                    }
                />
                <Card
                    label="MA20 / MA50"
                    value={`$${metrics.ma20?.toFixed(2)} / $${metrics.ma50?.toFixed(2)}`}
                />
                <Card
                    label="Vol(30d, ann.)"
                    value={`${(metrics.vol30 * 100)?.toFixed(2)}%`}
                />
                <Card
                    label="Max DD(30d)"
                    value={
                        <span style={{ color: "#dc3545" }}>
                            {(metrics.dd30 * 100)?.toFixed(2)}%
                        </span>
                    }
                />
                <Card
                    label="Сигнал MA"
                    value={
                        <span style={{ color: signalColor }}>
                            {signal === "bullish" ? "📈 Бычий" : "📉 Медвежий"}
                        </span>
                    }
                />
            </div>
            <div
                style={{
                    marginTop: 12,
                    padding: 16,
                    border: "1px solid #eee",
                    borderRadius: 8,
                    backgroundColor: "#f8f9fa",
                }}
            >
                <div style={{ fontWeight: 600, marginBottom: 8 }}>
                    📊 LLM4Web3 Анализ:
                </div>
                <div style={{ lineHeight: 1.6, color: "#333" }}>
                    {llm?.summary || "Анализ недоступен"}
                </div>
                {llm?.risk_level && (
                    <div
                        style={{
                            marginTop: 8,
                            padding: 6,
                            borderRadius: 4,
                            backgroundColor:
                                llm.risk_level.includes("высокий")
                                    ? "#fee"
                                    : llm.risk_level.includes("низкий")
                                    ? "#efe"
                                    : "#fff9e6",
                            fontSize: 12,
                            fontWeight: 600,
                        }}
                    >
                        Уровень риска: {llm.risk_level}
                    </div>
                )}
            </div>
        </div>
    );
}

