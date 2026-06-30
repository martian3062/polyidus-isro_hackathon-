# ERAYA → ERAYA-NETRA: PS-13 Migration Specification
**Target:** Bharatiya Antariksh Hackathon 2026 — Problem Statement 13 (Air-Gapped Predictive Copilot for Secure MPLS Operations)
**Source repo:** `eraya_microsoft` (Microsoft Build AI Hackathon 2026 submission)
**Migration mode:** retarget existing scaffold — no greenfield rewrite
**Submission deadline:** July 1, 2026 (idea proposal only, prototype not required at this stage)

---

## 0. TL;DR — What Stays, What Moves, What's New

| Layer | Action | Effort |
|---|---|---|
| 4-archetype swarm (Perceiver/Planner/Recoverer/Guardian) | **KEEP** structure, add MPLS tiers | Low |
| 3-tier cascade engine (`base.py`) | **KEEP AS-IS** | None |
| A2A protocol + HMAC verification | **KEEP AS-IS** | None |
| KAVACHA (InjectionSentinel + AuditSigner + PolicyAuditor) | **KEEP**, reframe rules R001–R003 for MPLS | Low |
| MCP server | **KEEP**, add 4 MPLS-specific tools | Low |
| OTel + Prometheus observability | **KEEP AS-IS** | None |
| Domain adapters (5G/Cloud/ICU) | **DEMOTE** to `legacy/`, add new `mpls/` | Medium |
| Groq LLM API | **REPLACE** with Ollama + local quantized model | **HIGH — air-gap critical** |
| Pinecone vector DB | **REPLACE** with ChromaDB local | Medium |
| External HuggingFace model pulls at runtime | **REPLACE** with offline-bundled models | Medium |
| Frontend (Next.js 15) | **KEEP** scaffolding, retheme + new MPLS dashboards | Medium |
| Telemetry pipeline (SNMP/NetFlow/IPFIX/syslog) | **NEW** | High |
| Simulated MPLS topology (Containerlab + FRR) | **NEW** | High |
| Helmholtz-decomposition anomaly layer | **NEW** (CloudFlow import — novel differentiator) | Medium |
| Forecasting node (LSTM/N-BEATS + time-to-impact) | **NEW** | Medium |
| Local RAG over Cisco/Juniper/RFC docs | **NEW** | Medium |
| Air-gap egress verification | **NEW** (critical for 20% scoring weight) | Low |

**Reuse ratio:** ~70% of ERAYA's code transfers unchanged. The remaining 30% is the MPLS domain + air-gap retrofit + new predictive layer.

---

## 1. Branding & Naming

| What | From | To |
|---|---|---|
| Project name | ERAYA | **ERAYA-NETRA** (Sanskrit: *netra* = eye, the watcher) |
| Tagline | "Self-Healing Agent Swarm Framework" | "Air-Gapped Predictive Copilot for Secure MPLS Operations" |
| Hackathon banner | Microsoft Build AI Hackathon 2026 | Bharatiya Antariksh Hackathon (BAH) 2026 — PS-13 |
| Sanskrit framing | एरया (eraya — that which moves toward) | एरया-नेत्र (eraya-netra — the watching guide) |
| Primary domain | 5G telecom (multi-domain agnostic) | **MPLS/SD-WAN** (single domain, deep specialization) |
| Security layer name | KAVACHA (कवच, armour) | **KAVACHA-NETRA** — keep KAVACHA, frame as ISRO-grade air-gap envelope |

**Repo move:** `martian3062/eraya_microsoft` → fork to `martian3062/eraya-netra` (or new repo). Keep git history; PS-13 submission must show provenance of reused work.

---

## 2. The Air-Gap Mandate — Critical Tech Swaps

PS-13 evaluation gives **20% weight to "verifiably zero outbound dependency during runtime."** Every cloud call must die.

| Current dependency | Outbound? | Replacement | Notes |
|---|---|---|---|
| Groq API (`llama-3.3-70b-versatile`) | **YES** | Ollama + `mistral:7b-instruct-q4_K_M` (or `phi3:3.8b-mini-4k-instruct-q4_K_M`) | Fits 4 GB VRAM on RTX 4050. Same JSON-mode contract. |
| Pinecone API | **YES** | ChromaDB (local persistence) or Qdrant local | Drop-in: same `add/query/delete` semantics. |
| HuggingFace pipeline downloads at runtime | **YES** | Pre-download to `models/` dir, set `TRANSFORMERS_OFFLINE=1` | DeBERTa-v3-base for InjectionSentinel — bundle the .bin file. |
| Sentence-transformers (`all-MiniLM-L6-v2`) for embeddings | **YES on first run** | Pre-download, ship in `models/embeddings/` | ~80 MB, tiny. |
| Anthropic MCP (Claude Desktop) | Optional — local stdio | **KEEP** — it's stdio-only, no network. Reframe in proposal as "MCP gateway for SOC integration." | Not an air-gap violation since MCP runs over stdio. |
| OpenTelemetry OTLP exporter to Jaeger | Localhost only | **KEEP AS-IS** | Already air-gapped. |
| Docker base images | Network on pull | Build offline-ready image + `docker save` to .tar | Document the offline install path. |
| `pip install` at runtime | **YES** | Pre-bake all deps into image. No runtime install. | Pin every version in `requirements.txt`. |

**New file:** `core/security/egress_monitor.py` — startup-time check that asserts no outbound TCP connections succeed (binds a sentinel, fails loudly if `requests.get("https://api.groq.com")` resolves). This becomes a **demoable claim** for the 20% air-gap rubric.

---

## 3. New Domain Adapter: MPLS

The existing `apps/domains/base.py` (ErayaEnvironment ABC, 3 methods) is unchanged. Add a new subclass.

```
apps/domains/mpls/
├── __init__.py
├── environment.py          # MPLSEnvironment(ErayaEnvironment)
├── simulator.py            # ContainerlabRunner — spawns/stops topology
├── topology.py             # NetworkX graph of CE/PE/P nodes + LSPs
├── signals.py              # SNMP/NetFlow/IPFIX/syslog → unified Signal schema
├── ingestors/
│   ├── snmp.py             # pysnmp polling loop
│   ├── netflow.py          # netflow-collector (UDP 2055)
│   ├── ipfix.py            # IPFIX collector
│   └── syslog.py           # syslog UDP 514 listener
├── fault_injection.py      # scripted: link_flap, bgp_withdraw, queue_saturation, mpls_label_corruption, controller_drift
└── actions.py              # available_actions: reroute_lsp, adjust_te_metric, isolate_link, drain_traffic, increase_bandwidth_reservation
```

### MPLSEnvironment contract (3 methods, like every other domain):

```python
class MPLSEnvironment(ErayaEnvironment):
    def available_actions(self) -> list[Action]: ...
    def step(self, action: Action) -> StepResult: ...
    def signal_snapshot(self) -> dict[str, Any]: ...
```

### Action set (replaces `handover_to_cell`, `scale_pod`, `adjust_drip_rate`):

| Action | Reversibility | Risk default | Guardian gate? |
|---|---|---|---|
| `reroute_lsp(lsp_id, new_path)` | 0.9 | 0.4 | No (low risk) |
| `adjust_te_metric(link_id, metric)` | 0.95 | 0.3 | No |
| `isolate_link(link_id)` | 0.6 | 0.7 | Yes (R003) |
| `drain_traffic(node_id)` | 0.7 | 0.6 | Soft (WARN) |
| `increase_bandwidth_reservation(lsp_id, bw_mbps)` | 0.95 | 0.2 | No |
| `failover_to_backup_lsp(lsp_id)` | 0.5 | 0.5 | Soft (WARN) |
| `restart_routing_process(node_id)` | 0.3 | 0.9 | **R004 — new rule, operator approval mandatory** |

---

## 4. PerceiverAgent — Add MPLS Tiers

`core/agents/perceiver.py` — add MPLS-specific methods alongside existing telecom/cloud/icu paths.

| Tier | Existing (5G/cloud/ICU) | New (MPLS) |
|---|---|---|
| **Tier 1 (GPU, HEAVY)** | Transformer + GNN over UE topology | **GNN over LSP topology graph + Helmholtz flow decomposition** (see §8) |
| **Tier 2 (CPU, MEDIUM)** | Kalman + XGBoost + HMM per feature | **Same algorithms** — features become `interface_util`, `latency_ms`, `jitter_ms`, `packet_loss`, `bgp_adj_changes_per_min`, `lsp_rsvp_state` |
| **Tier 3 (LIGHT, always)** | Bayesian rule: `σ/(μ+ε)` | **Same rule** — applied to per-link rolling stats. Plus a hard threshold layer (interface_util > 90% AND duration > 5 min → critical). |

**State labels remain:** `normal` / `degraded` / `critical` / `recovering`.

**New features computed at Tier 2:**
- `route_flap_rate_5m` — BGP UPDATE messages per 5 min per neighbor
- `lsp_jitter_variance` — rolling std-dev of RSVP-TE refresh delays
- `path_asymmetry_score` — forward-vs-reverse path divergence
- `divergence_magnitude` — output from Helmholtz layer, fed into XGBoost

---

## 5. PlannerAgent + LLMPlannerAgent — Replace Groq

`core/agents/llm_planner.py` is the critical change point.

### Current:
```python
from groq import Groq
client = Groq(api_key=os.environ["GROQ_API_KEY"])
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    response_format={"type": "json_object"},
    messages=[...],
)
```

### Replacement:
```python
# core/llm/offline_client.py — NEW FILE
from typing import Protocol
import httpx, json

class OfflineLLM(Protocol):
    def chat_json(self, system: str, user: str, schema: dict) -> dict: ...

class OllamaClient:
    def __init__(self, base_url="http://localhost:11434", model="mistral:7b-instruct-q4_K_M"):
        self.base_url = base_url
        self.model = model

    def chat_json(self, system: str, user: str, schema: dict) -> dict:
        # Ollama supports `format: "json"` natively as of 0.1.32
        r = httpx.post(f"{self.base_url}/api/chat", json={
            "model": self.model,
            "format": "json",
            "stream": False,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }, timeout=60.0)
        return json.loads(r.json()["message"]["content"])
```

### `LLMPlannerAgent` modification:
- Drop the `from groq import Groq` import.
- Import `OfflineLLM` and select implementation by env var `ERAYA_LLM_BACKEND=ollama|llamacpp`.
- **Keep** the JSON schema, prompt template, and `requires_guardian_approval` logic identical — only the transport changes.
- **Keep** the Thompson Sampling Tier 2 fallback unchanged.

### Model selection rubric:
| Model | Size (Q4_K_M) | VRAM | Tokens/s on RTX 4050 | Use case |
|---|---|---|---|---|
| `phi3:3.8b-mini-4k-instruct` | 2.3 GB | 3 GB | ~50 | Default — fastest, fits comfortably |
| `mistral:7b-instruct` | 4.4 GB | 4.5 GB | ~25 | Better reasoning, tight fit |
| `llama3:8b-instruct` | 4.7 GB | 5 GB | ~22 | If VRAM permits (test first) |

**Recommendation:** ship with `phi3` as default for VRAM safety; allow `mistral` via env var. Justify in proposal: "Phi-3 chosen for sub-second response latency on commodity NOC hardware; Mistral-7B available for higher-reasoning deployments."

---

## 6. RecovererAgent — MPLS-Specific Recovery

`core/agents/recoverer.py` — add MPLS tier methods.

| Tier | Method | Replacement for MPLS |
|---|---|---|
| **Tier 1** | Monte Carlo rollout simulator + RL replanning | **Monte Carlo rollout on topology graph** — sample N=100 reroute paths, score by expected congestion delta + reversibility |
| **Tier 2** | Tabular Q-learning + exponential backoff | **Q-learning over `(link_state, action)` pairs**, backoff for retry semantics on `restart_routing_process` |
| **Tier 3** | Circuit breaker + static fallback | **Circuit breaker per node**, static fallback = "reroute to backup LSP" |

Circuit breaker registrations to add:
```python
recoverer.register_circuit_breaker("link_flap", failure_threshold=5, recovery_timeout_s=30)
recoverer.register_circuit_breaker("bgp_session_down", failure_threshold=3, recovery_timeout_s=60)
recoverer.register_circuit_breaker("lsp_rsvp_timeout", failure_threshold=4, recovery_timeout_s=45)
```

---

## 7. GuardianAgent — Keep Core, Reframe Rules

`core/agents/guardian.py` — minimal changes. The Guardian framework already does what PS-13 needs.

### Updated hard rules:

| Rule | Old | New (MPLS) |
|---|---|---|
| **R001** | ICU actions require perception confidence > 0.8 | **P-router (provider core) actions require confidence > 0.85** — P routers carry aggregated traffic; mistakes cascade. |
| **R002** | Actions cannot override Guardian quarantine | **Unchanged** |
| **R003** | High-risk actions require guardian approval flag | **Unchanged** — applies to `isolate_link`, etc. |
| **R004 — NEW** | — | **`restart_routing_process` or any action on a P router with active LSPs > 50 requires operator approval flag** |
| **R005 — NEW** | — | **No automated action during BGP convergence window** (10 sec after any BGP UPDATE from a peer) — prevents thrashing |

### InjectionSentinel:
- **Keep** the DeBERTa primary + 13-pattern regex fallback **AS-IS**.
- **Add** 4 MPLS-specific patterns to `regex_patterns`:
  - `disable\s+ospf|disable\s+bgp`
  - `clear\s+ip\s+route\s+\*`
  - `no\s+mpls\s+ip`
  - `shutdown\s+interface`

These match Cisco IOS / Junos commands that could be injected via syslog or operator notes.

### AuditSigner: **completely unchanged**. HMAC-SHA256 tamper-evident audit is exactly what air-gap compliance review will demand.

---

## 8. NEW: Helmholtz Anomaly Decomposition Layer

This is the **CloudFlow PS-12 import** — your novel differentiator for PS-13. No other team will pitch this.

```
core/ml/helmholtz/
├── __init__.py
├── decomposition.py        # decompose_flow_field(flow: np.ndarray) -> (advective, divergent)
├── network_flow_field.py   # build_flow_field(topology: nx.Graph, telemetry: dict) -> np.ndarray
└── anomaly_score.py        # divergence_magnitude_per_node(advective, divergent) -> dict[node_id, float]
```

### Intuition:
Treat the network as a graph where each edge carries a flow rate (Mbps) and a direction. The flow field over the topology can be decomposed via discrete Helmholtz decomposition:

- **Advective component** = curl-free, divergence-free flow = normal traffic moving along established LSPs
- **Divergent component** = sources/sinks of flow = where traffic is *building up* or *draining anomalously*

### Anomaly signal:
`divergence_magnitude[node]` is the L2 norm of net flow accumulation at a node. High values precede:
- Congestion onset (traffic arriving faster than it leaves)
- LSP failure (traffic disappearing from a path)
- Microburst (transient divergence spike)
- Route flap (sustained sign-flipping in divergence)

### Math sketch (proposal-grade):
For a graph $G = (V, E)$ with flow $\mathbf{f}: E \to \mathbb{R}$, the discrete divergence at node $v$ is:
$$
\text{div}(v) = \sum_{e \in \text{out}(v)} f(e) - \sum_{e \in \text{in}(v)} f(e)
$$
Helmholtz decomposition splits $\mathbf{f} = \mathbf{f}_a + \mathbf{f}_d$ where $\nabla \cdot \mathbf{f}_a = 0$ (advective) and $\nabla \times \mathbf{f}_d = 0$ (divergent). Solved as a Hodge decomposition via the graph Laplacian.

### Implementation: ~150 lines of NumPy.
- Build node-edge incidence matrix
- Solve $L \phi = \text{div}(\mathbf{f})$ for the scalar potential $\phi$
- Divergent component = $\nabla \phi$ (gradient on graph)
- Advective = $\mathbf{f} - \nabla \phi$

### Integration point:
Fed into `PerceiverAgent._perceive_tier1_mpls()` as an additional feature. Also surfaced standalone via:
```python
GET /api/v1/mpls/flow-divergence/    # node-by-node divergence heatmap data
```

**Proposal framing:** *"Physics-aware anomaly detection: where every other PS-13 submission uses LSTM-on-time-series as a black box, ERAYA-NETRA decomposes the network's instantaneous flow field into advective (normal) and divergent (anomalous) components — surfacing congestion buildup before any threshold is breached."*

---

## 9. NEW: Forecasting Node — Time-to-Impact

PS-13 explicitly demands **prediction lead time** as the #1 evaluation criterion. Build a dedicated forecasting module.

```
core/forecasting/
├── __init__.py
├── lstm_forecaster.py      # per-feature LSTM, 5-min input → 30-min forecast
├── nbeats_forecaster.py    # N-BEATS ensemble (darts library, offline-compatible)
├── prophet_baseline.py     # Prophet for seasonal patterns (baseline only)
├── time_to_impact.py       # estimate seconds until threshold breach given forecast + confidence
└── ensemble.py             # weighted combiner with confidence calibration
```

### Output schema:
```python
class ForecastResult(BaseModel):
    target_metric: str                  # e.g. "link_util_eth0_1"
    horizon_seconds: int                # e.g. 1800
    forecast: list[float]               # one value per 30s step
    confidence_band_low: list[float]
    confidence_band_high: list[float]
    time_to_breach_seconds: int | None  # None if no breach predicted
    breach_threshold: float
    forecast_confidence: float          # 0.0–1.0
    fallback_to_persistence: bool       # CloudFlow-style — true if confidence < 0.5
```

### Integration:
- Called from `PerceiverAgent._perceive_tier1_mpls()` after Helmholtz decomposition
- Output flows into `PerceptionResult.risk_score` and a new field `PerceptionResult.time_to_impact_seconds`
- LLMPlannerAgent receives this in context: *"Link eth0/1 will saturate in 7 min 23 sec at 87% confidence"*

---

## 10. NEW: Local RAG Pipeline

```
core/rag/
├── __init__.py
├── ingest/
│   ├── cisco_iosxr.py      # parse Cisco IOS-XR config guides (offline PDFs)
│   ├── juniper_junos.py    # parse Junos doc set
│   ├── rfc_loader.py       # ingest RFC 3031, 3209, 5036, 4364, 7510
│   ├── runbooks.py         # custom YAML/Markdown runbooks
│   └── incident_history.py # past resolved incidents from AuditLog
├── embedder.py             # sentence-transformers, local-only
├── vector_store.py         # ChromaDB persistent client
├── retriever.py            # hybrid: dense (Chroma) + sparse (BM25 via rank_bm25)
└── citation.py             # every LLM response carries citation IDs
```

### Pre-ingest at build time (one-time, no runtime cloud calls):
```bash
python -m core.rag.ingest.cisco_iosxr --docs ./offline_corpus/cisco/
python -m core.rag.ingest.juniper_junos --docs ./offline_corpus/juniper/
python -m core.rag.ingest.rfc_loader --rfcs 3031,3209,5036,4364,7510
```

### Embeddings model:
- `sentence-transformers/all-MiniLM-L6-v2` (80 MB, CPU-friendly, ship in `models/embeddings/`)
- Set `HF_HUB_OFFLINE=1` and `TRANSFORMERS_OFFLINE=1` at runtime

### Retrieval contract (called by LLMPlannerAgent):
```python
context_chunks = rag.retrieve(
    query="BGP route flap with downstream cascade — Cisco IOS-XR remediation",
    k=5,
    filters={"vendor": "cisco", "doc_type": ["config_guide", "runbook"]}
)
# Each chunk carries: text, source, page, citation_id
```

### Hallucination guard:
LLM is instructed to cite every claim. Responses missing citations get **downgraded confidence** by the Guardian. If `cited_chunks < 1` AND `confidence > 0.7`, the Guardian triggers WARN.

---

## 11. Telemetry Pipeline — New Infrastructure

```
infra/telemetry/
├── docker-compose.yml      # telegraf + prometheus + (optional) elasticsearch
├── telegraf.conf
├── prometheus.yml
└── ingestors/
    ├── snmp_collector.py
    ├── netflow_collector.py    # UDP 2055
    ├── ipfix_collector.py
    └── syslog_collector.py     # UDP 514
```

### Data flow:
```
Simulated routers (Containerlab + FRR)
  → SNMP traps + NetFlow exports + syslog
    → Telegraf (collector)
      → Prometheus (TSDB) + local file sink
        → ERAYA-NETRA ingestors
          → MPLSEnvironment.signal_snapshot()
            → PerceiverAgent.perceive()
```

All localhost — zero outbound.

---

## 12. Simulated MPLS Network

PS-13 explicitly lists **Containerlab** as a suggested tool. Use it. EVE-NG and GNS3 require GUI licensing that complicates the air-gap demo.

```
infra/topology/
├── topology.clab.yml       # Containerlab topology definition
├── configs/                # per-node FRR configs
│   ├── pe1.conf
│   ├── pe2.conf
│   ├── p1.conf, p2.conf    # provider core
│   ├── ce1.conf … ce6.conf # branch CE routers
│   └── controller.conf     # SD-WAN controller emulation
└── fault_scenarios/
    ├── progressive_congestion.py
    ├── bgp_flap_cascade.py
    ├── mpls_underlay_intermittent.py
    └── controller_policy_drift.py
```

### Minimal topology (proposal-friendly):
- 3 sites: Branch-A, Branch-B, Datacenter
- Each site has 1 CE router
- 2 PE routers, 2 P routers in the provider core
- Full IS-IS + LDP + BGP-VPNv4
- 2 IPSec overlay tunnels (Branch-A → DC, Branch-B → DC)
- Mock SD-WAN controller (FastAPI) emulating Cisco vManage / VMware VeloCloud Orchestrator behavior

### Fault injection coverage (matches PS-13 Phase 6):
| Scenario | Status |
|---|---|
| Progressive congestion buildup on hub-spoke link | Required |
| BGP route flap with downstream reroute cascade | Required |
| Intermittent MPLS underlay failure with tunnel degradation | Required |
| Controller misconfiguration leading to policy drift | Required |

---

## 13. MCP Server — Add MPLS Tools

`mcp_server.py` — extend with 4 new tools.

| New tool | Description |
|---|---|
| `get_mpls_topology()` | Returns full topology graph as JSON (nodes, edges, LSPs) |
| `predict_lsp_failure(lsp_id)` | Runs forecaster, returns time-to-impact + confidence |
| `get_telemetry_snapshot(window_seconds)` | Last N seconds of all metrics |
| `inject_fault(scenario_id)` | Triggers a fault scenario for demo |

**Keep all 8 existing tools** — Claude Desktop integration is a clean "SOC operator chat-ops" demo that judges will appreciate.

---

## 14. Frontend Changes (Next.js 15)

Most of the operator console transfers untouched. Specific changes:

| Component | Action |
|---|---|
| `/dashboard` | Repurpose: replace 5G cell map with MPLS topology view (react-flow already in stack) |
| `/agents` | Unchanged — same 4 agents, just labeled with MPLS context |
| `/domains` | Hide 5G/Cloud/ICU (move to `/legacy`), default to `/domains/mpls` |
| `/context-graph` | Becomes the LSP graph view — nodes are routers, edges are LSPs colored by utilization |
| `/security/attack-console` | **Keep AS-IS** — KAVACHA demo works identically. Add 1 new MPLS-flavored injection payload. |
| `/audit-log` | Unchanged |
| **NEW** `/forecasts` | Time-to-impact widget: list of predicted failures with countdown timers |
| **NEW** `/flow-divergence` | Heatmap of Helmholtz divergence per node — the "physics view" |
| **NEW** `/copilot` | Chat interface — operator types NL questions, gets cited LLM answers |

### `/copilot` page (the headline UX):
```
┌────────────────────────────────────────────────┐
│ Operator: "Why is link eth0/1 risk elevated?"  │
├────────────────────────────────────────────────┤
│ ERAYA-NETRA:                                   │
│ Link eth0/1 utilization will breach 95%        │
│ in 4 min 12 sec at 0.84 confidence.            │
│                                                 │
│ Contributing signals:                           │
│   • Divergence magnitude: 0.67 (high)          │
│   • LSP RSVP refresh delay variance ↑ 3.2σ     │
│   • BGP UPDATE rate from peer 10.1.1.2 ↑ 4×    │
│                                                 │
│ Recommended action:                             │
│   reroute_lsp(lsp-7, backup_path=p2-pe2)       │
│   Confidence: 0.78 | Reversibility: 0.9        │
│                                                 │
│ [Sources: Cisco MPLS-TE Config Guide p.142,    │
│           Runbook RB-009 "Congestion Preempt"] │
│                                                 │
│ [Approve] [Reject] [Modify]                    │
└────────────────────────────────────────────────┘
```

---

## 15. Air-Gap Verification — The 20% Scoring Layer

```
core/security/airgap/
├── __init__.py
├── egress_monitor.py       # startup + runtime probe
├── dependency_audit.py     # scans Python deps for any cloud client libraries
└── runtime_assertions.py
```

### Startup assertion:
```python
def assert_airgap_at_startup():
    forbidden_hosts = [
        "api.groq.com", "api.openai.com", "api.anthropic.com",
        "huggingface.co", "pinecone.io", "amazonaws.com",
    ]
    for host in forbidden_hosts:
        try:
            socket.gethostbyname(host)
            socket.create_connection((host, 443), timeout=2)
            raise AirgapViolation(f"Outbound reachable: {host}")
        except (socket.gaierror, OSError):
            pass  # expected in air-gapped env
    log.info("✅ Air-gap verified: 0 outbound connections succeeded")
```

### Runtime audit endpoint:
```
GET /api/v1/security/airgap-status/
→ {
    "outbound_attempts": 0,
    "blocked_hostnames": [],
    "verified_at": "2026-06-28T...",
    "policy": "deny-all-egress",
    "auditor_signature": "<hmac>"
  }
```

This becomes a **live demo bullet** during the finale: judges watch ERAYA-NETRA refuse to make any outbound call, with HMAC-signed proof.

---

## 16. File-by-File Diff Summary

| Path | Action | Estimated LOC delta |
|---|---|---|
| `core/agents/base.py` | KEEP | 0 |
| `core/agents/perceiver.py` | MODIFY — add MPLS tier methods | +200 |
| `core/agents/llm_planner.py` | MODIFY — replace Groq with OfflineLLM | +30, −20 |
| `core/agents/planner.py` | KEEP | 0 |
| `core/agents/recoverer.py` | MODIFY — add MPLS tier methods | +150 |
| `core/agents/guardian.py` | MODIFY — add R004, R005 + MPLS injection patterns | +60 |
| `core/a2a/*` | KEEP | 0 |
| `core/llm/offline_client.py` | NEW | +180 |
| `core/llm/groq_client.py` | DELETE | −120 |
| `core/ml/helmholtz/` | NEW (5 files) | +400 |
| `core/forecasting/` | NEW (5 files) | +600 |
| `core/rag/` | NEW (8 files) | +700 |
| `core/security/airgap/` | NEW (3 files) | +250 |
| `apps/domains/mpls/` | NEW (10 files) | +1200 |
| `apps/domains/telecom/`, `cloud/`, `icu/` | MOVE to `apps/domains/legacy/` | path change only |
| `infra/topology/` | NEW | +500 (YAML + configs) |
| `infra/telemetry/` | NEW | +300 |
| `frontend/app/dashboard/page.tsx` | MODIFY — MPLS topology view | +150 |
| `frontend/app/forecasts/` | NEW | +400 |
| `frontend/app/flow-divergence/` | NEW | +300 |
| `frontend/app/copilot/` | NEW | +500 |
| `mcp_server.py` | MODIFY — add 4 MPLS tools | +200 |
| `README.md` | REWRITE | full rewrite |
| `requirements.txt` | MODIFY — add ollama/chromadb, remove groq/pinecone | +5, −2 |
| `docker-compose.yml` | MODIFY — add ollama, chromadb, telegraf, prometheus | +50 |

**Total estimated new code:** ~5,000 LOC (mostly MPLS domain + RAG + forecasting + topology configs).
**Total deleted/moved:** ~150 LOC.

---

## 17. Proposal Submission Deliverables (Due July 1)

The hackathon's initial phase is **idea proposal only** — no code required. Produce these documents:

### 17.1 Architecture diagram (1 page, visual)
Modified version of the ERAYA architecture diagram (lines 39–78 of current README) with:
- "5G/Cloud/ICU" boxes greyed out
- "MPLS" box prominent and the only active domain adapter
- New Helmholtz layer drawn into the Perceiver block
- New Forecasting node drawn between Perceiver and Planner
- Ollama + ChromaDB shown as local services, with an **air-gap perimeter line** explicitly drawn around the entire stack
- KAVACHA-NETRA framed as the perimeter enforcer

### 17.2 Proposal document (8–12 pages, structured to PS-13 evaluation rubric)

**Suggested structure** (mirroring the CloudFlow PS-12 doc you uploaded):

1. **Executive Summary** — 1 page. Lead with "85% of this system is already built and demoable. The remaining 15% is MPLS-specific."
2. **Problem Analysis** — Why reactive NOC tooling fails (paraphrase PS-13 problem). 1 page.
3. **Proposed Solution: ERAYA-NETRA** — Key innovations:
   - 4-archetype swarm with defined failure paths for every agent
   - Helmholtz-decomposition anomaly layer (physics-aware, novel)
   - Time-to-impact forecasting with confidence-driven fallback
   - Fully offline LLM (Phi-3 / Mistral-7B) with local RAG
   - KAVACHA security envelope (HMAC-signed audit, injection sentinel, identity verification)
   - **Reused from a prior Microsoft Build hackathon — proves production-readiness** (this is a *strength*, not a weakness — frame it)
4. **Architecture Detail** — the diagram + module breakdown
5. **Air-Gap Compliance** — section dedicated to the 20% rubric weight. Every cloud dep replaced; runtime egress monitor; HMAC audit.
6. **Predictive Analytics Engine** — Helmholtz + LSTM/N-BEATS + time-to-impact estimation. Math sketch.
7. **Offline Copilot** — Ollama + ChromaDB + sentence-transformers. Citation enforcement.
8. **Scenario Validation Plan** — the 4 PS-13 scenarios mapped to expected lead times.
9. **Evaluation Metrics** — for each PS-13 evaluation dimension, what we'll measure.
10. **Implementation Roadmap** — 4 phases mirroring PS-13's Phase 1–6, with realistic timelines.
11. **Tech Stack** — table.
12. **Team & Roles** — placeholder for now.
13. **Closing Note** — emphasize reuse + novelty combo.

### 17.3 Naming asset
- Logo concept (can be text + Sanskrit "नेत्र"-styled mark)
- Tagline: *"The unblinking eye for India's secure networks."*

### 17.4 README rewrite (for submission)
Replace the Microsoft Build framing with BAH 2026 framing. Move the existing README to `LEGACY_README.md` to preserve provenance.

---

## 18. Migration Order (4-Day Plan)

| Day | Task | Output |
|---|---|---|
| **Day 1 (Jun 28)** | Skim MPLS fundamentals (LSP, RSVP-TE, BGP-VPNv4, NetFlow, SNMP). Write proposal sections 1–4. | First half of proposal doc |
| **Day 2 (Jun 29)** | Helmholtz math sketch + forecasting design + air-gap section. Draft architecture diagram. | Sections 5–8 + diagram |
| **Day 3 (Jun 30)** | Scenario validation plan + roadmap + tech stack + team. Polish prose. | Full draft proposal |
| **Day 4 (Jul 1)** | Review, format, finalize. Submit by deadline. | Submitted PDF |

**No code changes required for the July 1 submission.** Code work begins only if shortlisted.

---

## 19. Risk Register

| Risk | Likelihood | Mitigation |
|---|---|---|
| Judges spot reuse and penalize originality | Medium | Frame reuse as production-readiness; only ERAYA-NETRA arrives at the hackathon already battle-tested in 5G + cloud + ICU domains. Reuse is a strength signal. |
| MPLS domain knowledge gap shows in proposal | Medium | Day 1 dedicated to MPLS literature; lean on RFC 3031, 3209, 5036 vocabulary; reference Cisco/Juniper config guides directly. |
| "Ollama on RTX 4050" sounds fragile | Low | Spec Phi-3 default with Mistral as upgrade path; cite published benchmarks. |
| Helmholtz framing reads as gimmick | Low | Cite the math rigorously (graph Laplacian, Hodge decomposition); contrast with vanilla LSTM baselines explicitly. |
| Containerlab on Windows is painful | Medium | Document WSL2 path; offer Linux VM as alternative; not relevant for July 1 submission. |

---

## 20. The One-Sentence Pitch

> *ERAYA-NETRA is an air-gapped agentic NOC copilot that decomposes network flow fields into physics-aware divergence components, forecasts failures with calibrated time-to-impact estimates, and explains every prediction through a fully offline LLM with HMAC-signed tamper-evident audit — built on a self-healing 4-agent swarm whose every method has defined failure paths.*

---

## 21. Working Prompt for Claude Code / Cursor

Use this prompt when you start the actual code migration:

```
You are migrating the ERAYA repository (Microsoft Build AI Hackathon 2026, https://github.com/martian3062/eraya_microsoft) to ERAYA-NETRA for BAH 2026 PS-13 (Air-Gapped Predictive Copilot for Secure MPLS Operations).

CONSTRAINTS:
- Air-gap compliance is mandatory. Zero outbound HTTP/HTTPS at runtime. Verify with core/security/airgap/egress_monitor.py.
- Reuse the 4-archetype cascade architecture, A2A protocol, KAVACHA security layer, MCP server, and OTel observability AS-IS.
- Replace Groq (cloud LLM) with Ollama running Phi-3 or Mistral-7B-Q4_K_M locally.
- Replace Pinecone with ChromaDB local.
- Add a new `apps/domains/mpls/` adapter following the existing ErayaEnvironment ABC.
- Add MPLS-specific tier methods to Perceiver, Planner, Recoverer (do NOT touch base.py).
- Add Helmholtz flow decomposition module under `core/ml/helmholtz/`.
- Add forecasting module under `core/forecasting/`.
- Add local RAG under `core/rag/` with citation enforcement.
- Add new Guardian rules R004 and R005 for MPLS-specific safety.
- Demote 5G/cloud/ICU adapters to `apps/domains/legacy/`.

NEW FILES (priority order):
1. core/llm/offline_client.py
2. apps/domains/mpls/{environment,simulator,topology,signals,actions}.py
3. core/security/airgap/{egress_monitor,dependency_audit}.py
4. core/ml/helmholtz/{decomposition,network_flow_field,anomaly_score}.py
5. core/forecasting/{lstm_forecaster,nbeats_forecaster,time_to_impact,ensemble}.py
6. core/rag/{embedder,vector_store,retriever,citation}.py + ingest/

MODIFY:
- core/agents/perceiver.py: add _perceive_tier1_mpls, _perceive_tier2_mpls, _perceive_tier3_mpls
- core/agents/llm_planner.py: swap Groq for OfflineLLM, keep interface identical
- core/agents/recoverer.py: add MPLS tier methods + new circuit breakers
- core/agents/guardian.py: add R004, R005, MPLS injection patterns
- mcp_server.py: add 4 MPLS tools

DO NOT TOUCH:
- core/agents/base.py (cascade engine is perfect)
- core/a2a/* (A2A protocol)
- KAVACHA core (AuditSigner, InjectionSentinel structure)
- OTel telemetry layer

For each modified file, show me the diff first. Wait for confirmation before applying.
```

---

*End of migration spec. Reuse leverage: ~70%. Time-to-proposal: 4 days. Time-to-working-prototype if shortlisted: ~3 weeks.*
