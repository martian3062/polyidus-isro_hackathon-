"use client";

import useSWR from "swr";
import { Timer } from "lucide-react";
import { api } from "@/lib/api";
import type { ForecastResult } from "@/lib/api";

export default function ForecastsPage() {
  const { data } = useSWR("forecasts-page", () => api.forecasts("mpls"), { refreshInterval: 10000 });
  const forecasts = data?.forecasts ?? [];

  return (
    <div className="mx-auto max-w-6xl space-y-5">
      <div>
        <h1 className="text-xl font-semibold text-slate-900 dark:text-slate-50">Time-To-Impact Forecasts</h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">Calibrated lead-time estimates for MPLS link saturation.</p>
      </div>
      <div className="grid gap-3">
        {forecasts.map((forecast) => <ForecastCard key={forecast.target_metric} forecast={forecast} />)}
      </div>
    </div>
  );
}

function ForecastCard({ forecast }: { forecast: ForecastResult }) {
  const breach = forecast.time_to_breach_seconds;
  const maxValue = Math.max(...forecast.forecast, forecast.breach_threshold);
  return (
    <div className="rounded-lg border border-slate-200 bg-white/75 p-4 shadow-sm dark:border-slate-800 dark:bg-slate-950/50">
      <div className="flex items-center justify-between gap-4">
        <div>
          <div className="text-sm font-semibold text-slate-800 dark:text-slate-100">{forecast.target_metric}</div>
          <div className="text-xs text-slate-500 dark:text-slate-400">
            Threshold {forecast.breach_threshold}% | confidence {(forecast.forecast_confidence * 100).toFixed(0)}%
          </div>
        </div>
        <div className="flex items-center gap-2 text-sm font-semibold text-slate-800 dark:text-slate-100">
          <Timer size={16} />
          {breach ? `${breach}s` : "No breach"}
        </div>
      </div>
      <div className="mt-4 flex h-24 items-end gap-1">
        {forecast.forecast.map((value, idx) => (
          <div key={idx} className="flex-1 rounded-t bg-cyan-500/80" style={{ height: `${Math.max(6, (value / maxValue) * 100)}%` }} />
        ))}
      </div>
    </div>
  );
}
