"use client";

import useSWR from "swr";
import { Waves } from "lucide-react";
import { api } from "@/lib/api";

export default function FlowDivergencePage() {
  const { data } = useSWR("flow-divergence-page", () => api.flowDivergence("mpls"), { refreshInterval: 8000 });
  const rows = Object.entries(data?.flow_divergence.nodes ?? {}).sort((a, b) => b[1] - a[1]);

  return (
    <div className="mx-auto max-w-5xl space-y-5">
      <div>
        <h1 className="text-xl font-semibold text-slate-900 dark:text-slate-50">Helmholtz Flow Divergence</h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">Physics-aware anomaly signal derived from graph flow accumulation.</p>
      </div>
      <div className="rounded-lg border border-slate-200 bg-white/75 p-5 shadow-sm dark:border-slate-800 dark:bg-slate-950/50">
        <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
          {rows.map(([node, score]) => (
            <div key={node} className="rounded-lg border border-slate-200 bg-slate-50 p-4 dark:border-slate-800 dark:bg-slate-900/60">
              <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400">
                <span>{node.toUpperCase()}</span>
                <Waves size={14} />
              </div>
              <div className="mt-3 font-mono text-2xl font-semibold text-slate-900 dark:text-slate-50">{score.toFixed(2)}</div>
              <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-200 dark:bg-slate-800">
                <div className="h-full rounded-full bg-cyan-500" style={{ width: `${score * 100}%` }} />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
