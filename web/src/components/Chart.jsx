import React, { useEffect, useRef } from "react";
import { createChart } from "lightweight-charts";

export default function Chart({ data = [] }) {
    const chartRef = useRef(null);
    const chartInstanceRef = useRef(null);

    useEffect(() => {
        if (!chartRef.current || !data.length) return;

        // Очищаем предыдущий график
        if (chartInstanceRef.current) {
            chartInstanceRef.current.remove();
        }

        const chart = createChart(chartRef.current, {
            width: chartRef.current.clientWidth,
            height: 360,
            layout: {
                backgroundColor: "#07060a",
                textColor: "#d1d5db",
            },
            grid: {
                vertLines: { color: 'rgba(255,255,255,0.03)' },
                horzLines: { color: 'rgba(255,255,255,0.03)' },
            },
            timeScale: { borderColor: 'rgba(255,255,255,0.04)' },
            crosshair: { vertLine: { color: 'rgba(255,255,255,0.02)' }, horzLine: { color: 'rgba(255,255,255,0.02)' } },
        });

        const series = chart.addCandlestickSeries({
            upColor: "#4ade80",
            downColor: "#ff6b6b",
            borderVisible: false,
            wickUpColor: "#4ade80",
            wickDownColor: "#ff6b6b",
        });

        const formattedData = data.map((d) => ({
            time: Math.floor(d.t / 1000),
            open: d.o,
            high: d.h,
            low: d.l,
            close: d.c,
        }));

        series.setData(formattedData);
        chart.timeScale().fitContent();

        chartInstanceRef.current = chart;

        const handleResize = () => {
            if (chartInstanceRef.current && chartRef.current) {
                chartInstanceRef.current.applyOptions({
                    width: chartRef.current.clientWidth,
                });
            }
        };

        window.addEventListener("resize", handleResize);

        return () => {
            window.removeEventListener("resize", handleResize);
            if (chartInstanceRef.current) {
                chartInstanceRef.current.remove();
            }
        };
    }, [data]);

    if (!data.length) {
        return <div className="p-6 text-center text-gray-400">Нет данных для графика</div>;
    }

    // responsive heights: compact on small screens, larger on md+
    return <div ref={chartRef} className="w-full h-[220px] md:h-[360px] chart-dark" />;
}

