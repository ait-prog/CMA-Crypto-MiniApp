export default function NewsList({ items = [] }) {
    if (!items.length) {
        return (
            <div className="p-6 text-center text-gray-400">Новостей пока нет.</div>
        );
    }

    return (
        <div className="grid gap-4 mt-2">
            {items.map((n, i) => (
                <a
                    key={i}
                    href={n.url}
                    target="_blank"
                    rel="noreferrer"
                    className="block p-4 rounded-lg glass-card hover:shadow-lg transition-shadow duration-150 text-gray-100"
                >
                    <div className="font-semibold text-white mb-1">{n.title}</div>
                    <div className="text-xs text-gray-400">{n.source} · {new Date(n.published_at).toLocaleString("ru-RU")}</div>
                </a>
            ))}
        </div>
    );
}

