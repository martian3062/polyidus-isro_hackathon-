"use client";

import useSWR from "swr";
import { Cpu, KeyRound, Lock, Settings2 } from "lucide-react";
import { api } from "@/lib/api";

export default function SettingsPage() {
  const { data } = useSWR("settings-airgap", () => api.airgapStatus(), { refreshInterval: 30000 });

  return (
    <div className="mx-auto max-w-4xl space-y-5">
      <div className="flex items-center gap-3">
        <div className="rounded-lg bg-cyan-50 p-2 text-cyan-700 dark:bg-cyan-950/40 dark:text-cyan-300">
          <Settings2 size={17} />
        </div>
        <div>
          <h1 className="text-xl font-semibold text-slate-900 dark:text-slate-50">Settings</h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">Local model and air-gap runtime configuration.</p>
        </div>
      </div>

      <section className="rounded-lg border border-slate-200 bg-white/75 p-5 shadow-sm dark:border-slate-800 dark:bg-slate-950/50">
          <h2 className="flex items-center gap-2 text-sm font-semibold text-slate-800 dark:text-slate-100">
          <Cpu size={16} />
          Planner Model
        </h2>
        <div className="mt-4 grid gap-3 text-sm">
          <Setting label="Backend" value="Groq API" />
          <Setting label="Default model" value="llama-3.3-70b-versatile" />
          <Setting label="Fallback path" value="Ollama local API" />
          <Setting label="Transport" value="https://api.groq.com/openai/v1/chat/completions" />
        </div>
      </section>

      <section className="rounded-lg border border-slate-200 bg-white/75 p-5 shadow-sm dark:border-slate-800 dark:bg-slate-950/50">
        <h2 className="flex items-center gap-2 text-sm font-semibold text-slate-800 dark:text-slate-100">
          <Lock size={16} />
          Air-Gap Status
        </h2>
        <div className="mt-4 grid gap-3 text-sm">
          <Setting label="Policy" value={data?.policy ?? "deny-all-egress"} />
          <Setting label="Outbound reachable" value={`${data?.outbound_attempts ?? 0}`} />
          <Setting label="Blocked cloud hosts" value={`${data?.blocked_hostnames.length ?? 0}`} />
          <Setting label="Audit signature" value={data?.auditor_signature ? `${data.auditor_signature.slice(0, 24)}...` : "pending"} />
        </div>
      </section>

      <section className="rounded-lg border border-slate-200 bg-white/75 p-5 shadow-sm dark:border-slate-800 dark:bg-slate-950/50">
        <h2 className="flex items-center gap-2 text-sm font-semibold text-slate-800 dark:text-slate-100">
          <KeyRound size={16} />
          Runtime Environment
        </h2>
        <div className="mt-4 grid gap-3 text-sm">
          <Setting label="NEXT_PUBLIC_API_URL" value={process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"} />
          <Setting label="OVERLAY_LLM_BACKEND" value="groq" />
          <Setting label="GROQ_MODEL" value="llama-3.3-70b-versatile" />
          <Setting label="HF_TOKEN" value="configured on server" />
          <Setting label="GROQ_API_KEY" value="configured on server" />
        </div>
      </section>
    </div>
  );
}

function Setting({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between gap-4 border-b border-slate-100 py-2 last:border-0 dark:border-slate-800">
      <span className="text-slate-500 dark:text-slate-400">{label}</span>
      <span className="max-w-[60%] truncate rounded bg-slate-100 px-2 py-1 font-mono text-xs text-slate-700 dark:bg-slate-900 dark:text-slate-200">
        {value}
      </span>
    </div>
  );
}
