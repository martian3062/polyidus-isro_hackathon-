"use client";

import { useMemo, useState } from "react";
import useSWR from "swr";
import { Check, MessageSquare, ShieldAlert } from "lucide-react";
import { api } from "@/lib/api";

export default function CopilotPage() {
  const [question, setQuestion] = useState("Why is link p1-p2 risk elevated?");
  const { data: forecasts } = useSWR("copilot-forecasts", () => api.forecasts("mpls"), { refreshInterval: 10000 });
  const { data: divergence } = useSWR("copilot-divergence", () => api.flowDivergence("mpls"), { refreshInterval: 8000 });

  const answer = useMemo(() => {
    const breach = forecasts?.forecasts.find((f) => f.time_to_breach_seconds !== null);
    const maxDiv = Object.entries(divergence?.flow_divergence.nodes ?? {}).sort((a, b) => b[1] - a[1])[0];
    return {
      breach,
      maxDiv,
      text: breach
        ? `${breach.target_metric} is projected to breach ${breach.breach_threshold}% in ${breach.time_to_breach_seconds} seconds at ${(breach.forecast_confidence * 100).toFixed(0)}% confidence.`
        : "No threshold breach is currently predicted across the MPLS fabric.",
    };
  }, [forecasts, divergence]);

  return (
    <div className="mx-auto max-w-4xl space-y-5">
      <div>
        <h1 className="text-xl font-semibold text-slate-900 dark:text-slate-50">Offline MPLS Copilot</h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">Local RAG-style answer surface with citation discipline.</p>
      </div>
      <div className="rounded-lg border border-slate-200 bg-white/75 p-5 shadow-sm dark:border-slate-800 dark:bg-slate-950/50">
        <label className="text-xs font-medium text-slate-500 dark:text-slate-400">Operator question</label>
        <div className="mt-2 flex gap-2">
          <input
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            className="min-w-0 flex-1 rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 outline-none focus:border-cyan-400 dark:border-slate-800 dark:bg-slate-900 dark:text-slate-100"
          />
          <button className="rounded-lg bg-cyan-600 px-3 py-2 text-sm font-medium text-white">
            <MessageSquare size={15} />
          </button>
        </div>
        <div className="mt-5 rounded-lg border border-slate-200 bg-slate-50 p-4 dark:border-slate-800 dark:bg-slate-900/70">
          <div className="mb-3 flex items-center gap-2 text-sm font-semibold text-slate-800 dark:text-slate-100">
            <ShieldAlert size={16} />
            Overlay
          </div>
          <p className="text-sm leading-6 text-slate-700 dark:text-slate-300">
            {answer.text} The strongest flow-divergence contributor is {answer.maxDiv?.[0]?.toUpperCase() ?? "unknown"} at {(answer.maxDiv?.[1] ?? 0).toFixed(2)}. Recommended first action is reroute_lsp to the backup path because it is reversible before isolating core links.
          </p>
          <div className="mt-4 flex flex-wrap gap-2 text-xs">
            <span className="rounded border border-slate-200 bg-white px-2 py-1 text-slate-600 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-300">[RB-009]</span>
            <span className="rounded border border-slate-200 bg-white px-2 py-1 text-slate-600 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-300">[RFC-3209]</span>
            <span className="flex items-center gap-1 rounded border border-emerald-200 bg-emerald-50 px-2 py-1 text-emerald-700 dark:border-emerald-900 dark:bg-emerald-950/40 dark:text-emerald-300">
              <Check size={12} /> citations present
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
