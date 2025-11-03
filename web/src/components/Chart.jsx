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
            height: 320,
            layout: {
                backgroundColor: "#ffffff",
                textColor: "#333",
            },
            grid: {
                vertLines: {
                    color: "#f0f0f0",
                },
                horzLines: {
                    color: "#f0f0f0",
                },
            },
        });

        const series = chart.addCandlestickSeries({
            upColor: "#26a69a",
            downColor: "#ef5350",
            borderVisible: false,
            wickUpColor: "#26a69a",
            wickDownColor: "#ef5350",
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
        return <div style={{ padding: 20, textAlign: "center" }}>Нет данных для графика</div>;
    }

    return <div ref={chartRef} style={{ width: "100%", height: 320 }} />;
}

