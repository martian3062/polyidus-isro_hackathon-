"use client";

import useSWR from "swr";
import { Activity, AlertTriangle, Lock, Network, ShieldCheck, Timer } from "lucide-react";
import { api } from "@/lib/api";
import { cn } from "@/lib/utils";
import type { AirgapStatus, ForecastResult, FlowDivergence, MplsTopology } from "@/lib/api";

export default function DashboardPage() {
  const { data: topo } = useSWR<{ topology: MplsTopology }>("mpls-topology", () => api.domainTopology("mpls"), {
    refreshInterval: 10000,
  });
  const { data: div } = useSWR<{ flow_divergence: FlowDivergence }>("mpls-divergence", () => api.flowDivergence("mpls"), {
    refreshInterval: 8000,
  });
  const { data: forecasts } = useSWR<{ forecasts: ForecastResult[] }>("mpls-forecasts", () => api.forecasts("mpls"), {
    refreshInterval: 10000,
  });
  const { data: airgap } = useSWR<AirgapStatus>("airgap", () => api.airgapStatus(), {
    refreshInterval: 30000,
  });

  const topology = topo?.topology;
  const risky = forecasts?.forecasts.filter((f) => f.time_to_breach_seconds !== null) ?? [];
  const maxDiv = Math.max(0, ...Object.values(div?.flow_divergence.nodes ?? {}));

  return (
    <div className="mx-auto max-w-7xl space-y-5">
      <div className="flex items-end justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900 dark:text-slate-50">Project Overlay</h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Air-gapped predictive copilot for secure MPLS operations
          </p>
        </div>
        <div className="flex items-center gap-2 rounded-lg border border-emerald-200 bg-emerald-50 px-3 py-2 text-xs text-emerald-700 dark:border-emerald-900/60 dark:bg-emerald-950/30 dark:text-emerald-300">
          <Lock size={14} />
          {airgap ? `${airgap.outbound_attempts} outbound egress paths reachable` : "Checking air-gap"}
        </div>
      </div>

      <div className="grid grid-cols-4 gap-3">
        <Kpi icon={Network} label="Routers" value={`${topology?.nodes.length ?? 0}`} />
        <Kpi icon={Activity} label="Links" value={`${topology?.edges.length ?? 0}`} />
        <Kpi icon={Timer} label="Predicted Breaches" value={`${risky.length}`} tone={risky.length ? "amber" : "emerald"} />
        <Kpi icon={ShieldCheck} label="Max Divergence" value={maxDiv.toFixed(2)} tone={maxDiv > 0.7 ? "red" : "blue"} />
      </div>

      <section className="grid grid-cols-[1.5fr_1fr] gap-4">
        <div className="rounded-lg border border-slate-200 bg-white/75 p-5 shadow-sm dark:border-slate-800 dark:bg-slate-950/50">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h2 className="text-sm font-semibold text-slate-800 dark:text-slate-100">MPLS Topology</h2>
              <p className="text-xs text-slate-500 dark:text-slate-400">CE, PE, and P routers with LSP pressure</p>
            </div>
            <span className="rounded bg-slate-100 px-2 py-1 text-[11px] text-slate-500 dark:bg-slate-800 dark:text-slate-300">
              offline simulator
            </span>
          </div>
          <TopologyCanvas topology={topology} divergence={div?.flow_divergence.nodes ?? {}} />
        </div>

        <div className="space-y-4">
          <div className="rounded-lg border border-slate-200 bg-white/75 p-5 shadow-sm dark:border-slate-800 dark:bg-slate-950/50">
            <h2 className="text-sm font-semibold text-slate-800 dark:text-slate-100">Time To Impact</h2>
            <div className="mt-4 space-y-3">
              {(forecasts?.forecasts ?? []).slice(0, 5).map((f) => (
                <ForecastRow key={f.target_metric} forecast={f} />
              ))}
            </div>
          </div>
          <div className="rounded-lg border border-slate-200 bg-white/75 p-5 shadow-sm dark:border-slate-800 dark:bg-slate-950/50">
            <h2 className="text-sm font-semibold text-slate-800 dark:text-slate-100">Overlay Shield</h2>
            <div className="mt-4 grid grid-cols-2 gap-2 text-xs">
              <Badge label="R004 routing restart gate" />
              <Badge label="R005 BGP convergence freeze" />
              <Badge label="HMAC audit proof" />
              <Badge label="Groq demo LLM" />
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

function Kpi({ icon: Icon, label, value, tone = "blue" }: {
  icon: React.ElementType;
  label: string;
  value: string;
  tone?: "blue" | "amber" | "emerald" | "red";
}) {
  const toneClass = {
    blue: "text-sky-600 bg-sky-50 border-sky-200 dark:text-sky-300 dark:bg-sky-950/30 dark:border-sky-900/50",
    amber: "text-amber-600 bg-amber-50 border-amber-200 dark:text-amber-300 dark:bg-amber-950/30 dark:border-amber-900/50",
    emerald: "text-emerald-600 bg-emerald-50 border-emerald-200 dark:text-emerald-300 dark:bg-emerald-950/30 dark:border-emerald-900/50",
    red: "text-red-600 bg-red-50 border-red-200 dark:text-red-300 dark:bg-red-950/30 dark:border-red-900/50",
  }[tone];
  return (
    <div className={cn("rounded-lg border p-4", toneClass)}>
      <div className="flex items-center justify-between text-xs">
        <span>{label}</span>
        <Icon size={15} />
      </div>
      <div className="mt-2 font-mono text-2xl font-semibold text-slate-900 dark:text-slate-50">{value}</div>
    </div>
  );
}

function TopologyCanvas({ topology, divergence }: { topology?: MplsTopology; divergence: Record<string, number> }) {
  const positions: Record<string, { x: number; y: number }> = {
    "ce-a": { x: 7, y: 28 },
    "ce-b": { x: 7, y: 70 },
    pe1: { x: 28, y: 50 },
    p1: { x: 48, y: 34 },
    p2: { x: 66, y: 58 },
    pe2: { x: 82, y: 50 },
    dc: { x: 94, y: 50 },
  };
  return (
    <div className="relative h-[430px] overflow-hidden rounded-lg bg-slate-950">
      <svg className="absolute inset-0 h-full w-full">
        {(topology?.edges ?? []).map((edge) => {
          const a = positions[edge.source];
          const b = positions[edge.target];
          const risk = Math.min(1, edge.utilization_pct / 100);
          return (
            <line
              key={edge.link_id}
              x1={`${a.x}%`}
              y1={`${a.y}%`}
              x2={`${b.x}%`}
              y2={`${b.y}%`}
              stroke={risk > 0.9 ? "#fb7185" : risk > 0.75 ? "#f59e0b" : "#22d3ee"}
              strokeWidth={2 + risk * 5}
              strokeLinecap="round"
              opacity={0.8}
            />
          );
        })}
      </svg>
      {(topology?.nodes ?? []).map((node) => {
        const pos = positions[node.node_id];
        const div = divergence[node.node_id] ?? 0;
        return (
          <div
            key={node.node_id}
            className="absolute grid h-16 w-16 place-items-center rounded-lg border text-center shadow-lg"
            style={{
              left: `calc(${pos.x}% - 32px)`,
              top: `calc(${pos.y}% - 32px)`,
              borderColor: div > 0.7 ? "#fb7185" : "#38bdf8",
              background: node.role === "P" ? "#0f172a" : node.role === "PE" ? "#172554" : "#083344",
            }}
          >
            <div>
              <div className="text-xs font-semibold text-white">{node.node_id.toUpperCase()}</div>
              <div className="text-[10px] text-slate-300">{node.role} div {div.toFixed(2)}</div>
            </div>
          </div>
        );
      })}
      {!topology && <div className="grid h-full place-items-center text-sm text-slate-400">Loading topology</div>}
    </div>
  );
}

function ForecastRow({ forecast }: { forecast: ForecastResult }) {
  const breach = forecast.time_to_breach_seconds;
  return (
    <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 dark:border-slate-800 dark:bg-slate-900/60">
      <div className="flex items-center justify-between gap-3">
        <span className="truncate text-xs font-medium text-slate-700 dark:text-slate-200">{forecast.target_metric}</span>
        <span className={cn("text-xs font-semibold", breach ? "text-amber-600" : "text-emerald-600")}>
          {breach ? `${Math.round(breach / 60)} min` : "stable"}
        </span>
      </div>
      <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-slate-200 dark:bg-slate-800">
        <div className="h-full rounded-full bg-cyan-500" style={{ width: `${forecast.forecast_confidence * 100}%` }} />
      </div>
    </div>
  );
}

function Badge({ label }: { label: string }) {
  return <span className="rounded border border-slate-200 bg-slate-50 px-2 py-1 text-slate-600 dark:border-slate-800 dark:bg-slate-900 dark:text-slate-300">{label}</span>;
}
