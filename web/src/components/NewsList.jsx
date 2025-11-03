export default function NewsList({ items = [] }) {
    if (!items.length) {
        return (
            <div style={{ padding: 20, textAlign: "center", color: "#666" }}>
                Новостей пока нет.
            </div>
        );
    }

    return (
        <div style={{ display: "grid", gap: 12, marginTop: 10 }}>
            {items.map((n, i) => (
                <a
                    key={i}
                    href={n.url}
                    target="_blank"
                    rel="noreferrer"
                    style={{
                        border: "1px solid #eee",
                        padding: 12,
                        borderRadius: 8,
                        textDecoration: "none",
                        color: "inherit",
                        display: "block",
                        backgroundColor: "#fff",
                        transition: "box-shadow 0.2s",
                    }}
                    onMouseEnter={(e) => {
                        e.currentTarget.style.boxShadow = "0 2px 8px rgba(0,0,0,0.1)";
                    }}
                    onMouseLeave={(e) => {
                        e.currentTarget.style.boxShadow = "none";
                    }}
                >
                    <div style={{ fontWeight: 600, marginBottom: 6, color: "#333" }}>
                        {n.title}
                    </div>
                    <div style={{ fontSize: 12, opacity: 0.7, color: "#666" }}>
                        {n.source} · {new Date(n.published_at).toLocaleString("ru-RU")}
                    </div>
                </a>
            ))}
        </div>
    );
}

