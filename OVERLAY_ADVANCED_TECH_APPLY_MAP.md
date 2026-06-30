# Project Overlay Advanced Technology Apply Map

Checked on: 2026-06-28

Use this file as the practical upgrade list for Overlay. The goal is not to add buzzwords; it is to choose tools that can really improve an air-gapped predictive copilot for MPLS / SD-WAN operations.

Visible project name: **Project Overlay**

Use **ERAYA** only in Markdown/provenance notes.

---

## Best Technologies To Apply

| Priority | Technology | Apply In Overlay As | Why It Fits | Effort |
|---|---|---|---|---|
| P0 | Hugging Face time-series foundation models | Forecasting adapters for link utilization, jitter, drops, LSP risk, BGP update bursts | Gives cold-start forecasting before enough MPLS-specific data is collected | Medium |
| P0 | OpenTelemetry eBPF Instrumentation | Zero-code observability for local Linux services and network paths | Captures service/network telemetry without modifying code | Low-Medium |
| P0 | Kuzu embedded graph database | Local topology graph store for routers, links, LSPs, risks, incidents, and evidence | Air-gap friendly graph reasoning without a separate graph server | Medium |
| P0 | Qdrant local hybrid search | Better offline RAG for RFCs, vendor docs, runbooks, incident notes | Dense + sparse retrieval improves citation quality over basic vector search | Medium |
| P1 | River online ML | Streaming anomaly detector for telemetry drift and live risk scoring | Learns incrementally from continuous telemetry | Low |
| P1 | PyWhy / DoWhy causal inference | Root-cause explanation: "Which factor likely caused this risk?" | Moves copilot from correlation to cause-oriented reasoning | Medium |
| P1 | OpenConfig gNMI telemetry | Modern streaming network telemetry adapter | More realistic than only SNMP polling for NOC-grade proposal | Medium |
| P1 | SRv6 / Segment Routing in FRR | Advanced network simulation mode | Makes the demo more modern than classic MPLS-only paths | Medium-High |
| P2 | The Well / Polymathic AI | Physics-inspired digital twin training reference | Useful for spatiotemporal flow-surrogate thinking | High |
| P2 | NVIDIA PhysicsNeMo | Neural operator / GNN surrogate model path | Strong story for scientific digital-twin style forecasting | High |
| P2 | MCP with strict allowlist | Tool interface between local copilot and safe operations | Useful, but must be heavily guarded in air-gapped/security context | Medium |

---

## 1. Hugging Face Time-Series Foundation Models

Apply this first for forecasting.

Candidate models:

- Amazon Chronos-2
- Google TimesFM
- AutonLab MOMENT
- IBM Granite Time Series / TinyTimeMixer

How to apply:

```text
Overlay telemetry sequence
router_id, link_id, timestamp, utilization, packet_loss, jitter, latency, bgp_updates, lsp_state
        |
        v
Time-series foundation model adapter
        |
        v
Predicted risk windows:
- link breach in next N minutes
- jitter spike probability
- tunnel degradation probability
- route-flap cascade probability
```

Best use in the project:

- Add a `forecasting_adapters/` module.
- Keep a simple baseline model first: EWMA, Kalman, XGBoost, River.
- Add model adapters behind feature flags:
  - `granite_ttm`
  - `chronos2`
  - `timesfm`
  - `moment`
- Show the winner on the dashboard as "Forecast Engine: Baseline / TSFM".

Judge-safe wording:

```text
Overlay supports a pluggable forecasting layer. Baseline models run by default, and modern time-series foundation models can be used offline where compute allows.
```

Sources:

- https://huggingface.co/amazon/chronos-2
- https://huggingface.co/google/timesfm-2.5-200m-pytorch
- https://huggingface.co/AutonLab/MOMENT-1-large
- https://huggingface.co/ibm-granite/granite-timeseries-ttm-r2

---

## 2. The Well + PhysicsNeMo Digital Twin Path

The Well is useful, but do not overclaim.

What it is:

- A 15TB collection of numerical physics simulations for spatiotemporal physical systems.
- Good inspiration for learning how fields evolve over time.
- Relevant to Overlay because network congestion behaves like flow over a graph: pressure, accumulation, propagation, and dissipation.

How to apply realistically:

```text
MPLS topology graph + telemetry time series
        |
        v
Graph-flow state tensor
        |
        v
Small neural operator / GNN surrogate
        |
        v
Digital twin forecast:
"If link p1-p2 degrades, which LSPs become risky next?"
```

Implementation path:

1. Start with graph-flow features already in Overlay.
2. Add a small synthetic simulator that generates congestion propagation cases.
3. Train a small GNN or FNO-like surrogate on synthetic local data.
4. Use The Well / PhysicsNeMo as the research reference and future scale path.
5. Optionally test Polymathic AI pretrained FNO models to show feasibility, not as core network logic.

What to say:

```text
The Well and PhysicsNeMo guide the digital-twin design. For the hackathon prototype, Overlay uses a smaller local graph-flow surrogate trained on synthetic MPLS scenarios.
```

What not to say:

```text
Do not say: "We trained Overlay on all 15TB of The Well."
```

Sources:

- https://polymathic-ai.org/the_well/
- https://huggingface.co/polymathic-ai
- https://huggingface.co/polymathic-ai/FNO-MHD_64
- https://developer.nvidia.com/physicsnemo

---

## 3. OpenTelemetry eBPF Instrumentation

Apply this for observability.

Why it fits:

- Overlay is a NOC tool, so telemetry credibility matters.
- eBPF can capture service and OS networking behavior without application code changes.
- Works best in Linux demo/VM/container environment.

How to apply:

```text
Django API / WebSocket / simulator containers
        |
        v
OpenTelemetry eBPF Instrumentation
        |
        v
OpenTelemetry Collector
        |
        v
Prometheus + Jaeger + Overlay dashboard
```

Project feature:

```text
Air-gap Observability Console:
- service latency
- request rate
- error rate
- network flow hints
- API-to-agent trace spans
```

Source:

- https://opentelemetry.io/docs/zero-code/obi/

---

## 4. Kuzu Embedded Graph Database

Apply this for topology reasoning.

Why it fits:

- Overlay thinks in graphs: routers, links, LSPs, incidents, actions, policies.
- Kuzu is embedded, so it is air-gap friendly.
- It can replace fragile JSON-only topology storage later.

Graph model:

```text
(Router)-[:HAS_LINK]->(Link)-[:CONNECTS]->(Router)
(LSP)-[:USES]->(Link)
(Incident)-[:AFFECTS]->(Router)
(Action)-[:REMEDIATES]->(Incident)
(Policy)-[:BLOCKS_OR_ALLOWS]->(Action)
```

Queries to support:

```text
Which LSPs traverse this risky link?
Which incidents looked similar?
Which actions were safe last time?
Which policy blocked this remediation?
```

Source:

- https://kuzudb.github.io/docs/

---

## 5. Qdrant Local Hybrid Search

Apply this to improve offline RAG.

Why it fits:

- Current local RAG can become stronger with hybrid search.
- Dense vector search finds semantic matches.
- Sparse keyword search finds exact RFC/vendor terms.
- Reranking improves citation quality.

How to apply:

```text
RFCs + vendor docs + runbooks + incident notes
        |
        v
Chunking + metadata
        |
        v
Qdrant local:
- dense vectors
- sparse vectors
- reranking
        |
        v
Copilot answer with citations
```

Use this when:

- Judge asks: "How do you avoid hallucination?"
- Your answer: "Hybrid retrieval plus local citations, no cloud dependency."

Source:

- https://qdrant.tech/documentation/tutorials-basics/reranking-hybrid-search/

---

## 6. River Online ML

Apply this for streaming anomaly detection.

Why it fits:

- Network telemetry is continuous.
- Conditions drift over time.
- River supports online learning instead of full retraining.

How to apply:

```text
Telemetry event stream
        |
        v
River anomaly model
        |
        v
Live anomaly score
        |
        v
Overlay risk score + alert
```

Good first detectors:

- Half-Space Trees
- Robust random cut style scoring
- Online mean/std drift score
- Per-link adaptive thresholds

Source:

- https://riverml.xyz/dev/api/overview/

---

## 7. PyWhy / DoWhy Causal Root Cause

Apply this for better explanations.

Why it fits:

- Forecasting says "what may happen."
- Causal analysis helps answer "why is it happening?"

Example:

```text
Question:
Why is p1-p2 risk high?

Signals:
- utilization increased
- BGP updates increased
- jitter increased
- backup LSP unavailable

Causal graph:
BGP churn -> path shift -> utilization spike -> jitter -> LSP risk
```

Dashboard feature:

```text
Root Cause Lens:
Likely cause: BGP churn on PE1
Contributing factor: backup LSP unavailable
Confidence: medium
Recommended verification: check BGP update source and RSVP-TE reservation state
```

Source:

- https://www.pywhy.org/

---

## 8. OpenConfig gNMI Telemetry

Apply this to make telemetry modern.

Why it fits:

- SNMP polling is classic but not modern enough for a high-end proposal.
- gNMI streams structured telemetry over gRPC using OpenConfig/YANG paths.
- It makes Overlay look realistic for modern network operations.

How to apply:

```text
Router / simulator / mock gNMI target
        |
        v
gNMI subscriber
        |
        v
Overlay telemetry normalizer
        |
        v
Risk engine + dashboard
```

Demo path:

- Add a mock gNMI JSON stream first.
- Later integrate a real gNMI gateway or vendor/router target.

Sources:

- https://www.openconfig.net/docs/gnmi/gnmi-specification/
- https://github.com/openconfig/gnmi-gateway

---

## 9. SRv6 / Segment Routing Simulation

Apply this as an advanced simulation mode.

Why it fits:

- MPLS is strong, but SRv6 is a modern carrier-network direction.
- FRRouting supports SRv6 pieces.
- This lets Overlay say it supports MPLS today and can extend to SRv6 tomorrow.

How to apply:

```text
Mode 1: MPLS / RSVP-TE
Mode 2: SRv6 / Segment Routing
```

Dashboard label:

```text
Transport Mode: MPLS-TE / SRv6-ready
```

Sources:

- https://docs.frrouting.org/en/latest/isisd.html
- https://datatracker.ietf.org/doc/rfc8986/

---

## 10. MCP For Tooling, But With Strong Guardrails

Apply carefully.

Why it fits:

- MCP is useful for exposing tools to local agents.
- Overlay can expose safe operations:
  - `get_topology`
  - `get_risk_summary`
  - `simulate_fault`
  - `recommend_action`
  - `draft_change_plan`

What to avoid:

- Do not expose direct dangerous actions without Guardian approval.
- Do not allow arbitrary shell commands.
- Do not allow tool names to be injected from retrieved documents.

Safe design:

```text
Copilot
  |
  v
MCP tool call
  |
  v
Tool allowlist + schema validation
  |
  v
Overlay Shield
  |
  v
Read-only result or human-approved action
```

Source:

- https://modelcontextprotocol.io/specification/2025-06-18/server/tools

---

## Recommended Build Order

Do this first:

1. Add River online anomaly scoring for streaming telemetry.
2. Add forecasting adapter interface and start with Granite TTM or TimesFM as optional offline engines.
3. Replace/improve topology storage with Kuzu graph queries.
4. Improve RAG using Qdrant local hybrid retrieval.
5. Add OpenTelemetry eBPF path for Linux demo observability.

Do this second:

1. Add PyWhy/DoWhy root-cause lens.
2. Add OpenConfig/gNMI mock telemetry adapter.
3. Add SRv6-ready simulation mode in the architecture/proposal.

Do this as advanced research:

1. Build a small graph-flow digital twin.
2. Use PhysicsNeMo/FNO/PINO/GNN ideas.
3. Reference The Well as the physics simulation learning source.

---

## PPT Upgrade Wording

Short version:

```text
Overlay combines local telemetry, graph-flow anomaly detection, time-series foundation forecasting, causal root-cause analysis, and a guarded offline copilot.
```

Advanced version:

```text
Overlay extends from an MPLS monitoring copilot into an air-gapped network digital twin: time-series foundation models forecast risk, graph/physics surrogates estimate propagation, causal AI explains root cause, and Guardian policy controls keep remediation safe.
```

Judge-safe line:

```text
The Well and PhysicsNeMo are used as the research direction for physics-inspired digital twin modeling. The hackathon prototype uses smaller local synthetic MPLS scenarios and pluggable forecasting models.
```

---

## Final Recommendation

For the actual Overlay project, the highest value additions are:

1. **Granite TTM / TimesFM forecasting adapter**
2. **River streaming anomaly detection**
3. **Kuzu graph topology store**
4. **Qdrant hybrid RAG**
5. **OpenTelemetry eBPF observability**
6. **PyWhy causal root-cause lens**
7. **The Well + PhysicsNeMo as advanced digital-twin roadmap**

This makes Overlay more advanced without making impossible claims.
