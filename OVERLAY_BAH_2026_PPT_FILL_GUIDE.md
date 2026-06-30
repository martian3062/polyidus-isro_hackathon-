# Project Overlay (ERAYA) - BAH 2026 PPT Fill Guide

Use this file to fill: `[Pub] ISRO BAH 2026 _ Idea Submission Template.pptx`

Project name to use on slides: **Project Overlay**

Use **ERAYA** only in Markdown/provenance notes, not as the visible product name in the PPT.

Problem statement: **PS-13: Air-Gapped Predictive Copilot for Secure MPLS Operations**

One-line pitch:

> Overlay is an air-gapped predictive NOC copilot that forecasts MPLS/SD-WAN failures, explains risk through a local LLM and offline runbooks, and keeps remediation behind signed Guardian policy controls.

Advanced technology angle to include where space allows:

```text
Overlay can be upgraded with physics-inspired network digital twin models: The Well-style spatiotemporal simulation datasets, neural operators, graph neural networks, and modern time-series foundation models such as Chronos-2, TimesFM, MOMENT, and Granite TTM.
```

Why this is useful:

- The Well is a 15TB physics simulation collection from Polymathic AI. It is useful as an inspiration/training reference for spatiotemporal surrogate models, flow fields, wave propagation, turbulence, and anomaly dynamics.
- NVIDIA PhysicsNeMo provides neural operators, Fourier Neural Operators, graph neural networks, and physics-ML tooling that fit the "physics-aware network digital twin" story.
- Hugging Face hosts strong time-series foundation models that can be used for zero-shot or few-shot telemetry forecasting before custom MPLS data is available.
- OpenTelemetry eBPF Instrumentation can add zero-code Linux/network-layer observability for the local demo stack.

---

## Slide 1 - Cover

Template fields:

- Team Name
- Problem Statement
- Team Leader Name

Fill:

```text
Team Name: Project Overlay

Problem Statement: PS-13 - Air-Gapped Predictive Copilot for Secure MPLS Operations

Team Leader Name: [Your Name]
```

Optional small subtitle if there is space:

```text
The offline predictive eye for secure MPLS networks
```

Visual suggestion:

- Keep the existing template branding.
- Add a small MPLS network motif: CE -> PE -> P -> PE -> DC.
- Do not clutter the cover. The first read should be `Project Overlay`.

---

## Slide 2 - Team Members

Template title:

```text
Team Members
```

Fill:

```text
1. [Member 1 Name] - Team Lead / Product + Architecture
2. [Member 2 Name] - Backend + Agent Swarm
3. [Member 3 Name] - Network Simulation + MPLS Telemetry
4. [Member 4 Name] - Frontend + UX
5. [Member 5 Name] - ML / Forecasting + RAG
```

If solo:

```text
[Your Name] - Full-stack architecture, MPLS simulation, offline AI, security, and proposal
```

Optional bottom line:

```text
Focus areas: MPLS operations, air-gap compliance, predictive analytics, secure agentic remediation
```

---

## Slide 3 - Opportunity / Problem Fit / USP

Template asks:

- How different is it from existing ideas?
- How will it solve the problem?
- USP of proposed solution

Recommended slide title:

```text
Opportunity: Predict before MPLS failure becomes outage
```

Paste-ready content:

```text
Current NOC tools are reactive: alarms fire after congestion, flap, tunnel degradation, or policy drift has already affected users.

Overlay changes the workflow from monitor -> alarm -> troubleshoot to predict -> explain -> approve -> safely remediate.

How it is different:
- Fully air-gapped: local LLM, local runbooks, local telemetry, no runtime cloud dependency
- Physics-aware anomaly detection: Helmholtz flow divergence spots traffic build-up before threshold breach
- Simulation-aware digital twin: learns spatiotemporal failure patterns using The Well/PhysicsNeMo-style surrogate modeling
- Time-series foundation models: cold-start forecasting with Chronos-2, TimesFM, MOMENT, or Granite TTM before full custom training
- Time-to-impact forecasting: predicts when a link/LSP will breach risk thresholds
- Guarded remediation: every risky action is checked by Overlay Shield and HMAC-signed

USP:
An offline predictive copilot that combines MPLS telemetry, graph-flow physics, simulation-inspired digital twins, local RAG explanations, and policy-gated agent actions in one secure NOC workflow.
```

Shorter version if the slide is tight:

```text
Overlay moves MPLS operations from reactive alarms to predictive, explainable, guarded remediation.

USP:
Air-gapped local AI + graph-flow anomaly detection + time-to-impact forecasting + HMAC-signed Guardian controls.
```

Visual suggestion:

Use a left-to-right transformation:

```text
Reactive NOC
Alarm after breach -> Manual triage -> Risky late action

Project Overlay
Predict breach -> Explain cause -> Guardian approval -> Safe remediation
```

---

## Slide 4 - Features Offered

Template asks:

- List of features offered by the solution
- Add visuals/sketches/illustrations

Recommended slide title:

```text
Core Features
```

Paste-ready content:

```text
1. Offline MPLS telemetry ingestion
   SNMP, NetFlow/IPFIX, syslog, RSVP-TE, BGP adjacency and LSP state signals

2. Predictive risk engine
   Forecasts link/LSP saturation, route-flap cascades, tunnel degradation, and policy drift

3. Helmholtz flow-divergence view
   Finds where traffic is accumulating or disappearing abnormally across the topology graph

4. Physics-inspired network digital twin
   Uses The Well/PhysicsNeMo-style spatiotemporal simulation learning, neural operators, and graph neural networks to model how congestion or instability propagates

5. Time-series foundation forecasting
   Tests Chronos-2, TimesFM, MOMENT, and Granite TTM for zero-shot/few-shot telemetry forecasts before custom MPLS fine-tuning

6. eBPF-assisted observability
   Optional OpenTelemetry eBPF instrumentation captures service and network behavior without changing application code

7. Local copilot with citations
   Answers operator questions using offline RFCs, vendor docs, runbooks, and incident history

8. Overlay Shield
   Blocks unsafe actions, prompt injection, routing-process restarts, and BGP convergence-window thrashing

9. Human-in-the-loop remediation
   Recommends reversible actions first: reroute LSP, adjust TE metric, fail over to backup LSP, drain traffic

10. Tamper-evident audit
   Every high-risk decision is HMAC-signed for offline compliance review
```

Visual suggestion:

Use ten compact feature icons around a simple MPLS core diagram. Suggested icon labels:

```text
Telemetry | Forecast | Flow Physics | Digital Twin | TSFM | eBPF | Copilot | Shield | Remediation | Audit
```

---

## Slide 5 - Process Flow / Use Case Diagram

Template asks:

- Process flow diagram or use-case diagram
- Add flow/use-case/architecture diagram

Recommended slide title:

```text
Operator Workflow
```

Paste-ready process flow:

```text
1. Router telemetry enters local collector
2. Overlay normalizes MPLS signals
3. Perceiver detects current risk + flow divergence
4. Digital twin estimates propagation pattern using graph/physics surrogate
5. Forecaster estimates time-to-impact
6. Copilot explains cause with offline citations
7. Planner recommends reversible action
8. Overlay Shield approves, warns, blocks, or quarantines
9. Operator approves high-risk action
10. Recoverer executes/remediates
11. Audit signer seals the event
```

Diagram to draw:

```text
Routers / SD-WAN Controller
        |
        v
Telemetry Collector
SNMP | NetFlow | IPFIX | Syslog
        |
        v
MPLS Signal Normalizer
        |
        v
Perceiver + Helmholtz Divergence
        |
        v
Physics Surrogate / Digital Twin
The Well-style spatiotemporal learning
PhysicsNeMo neural operators + GNNs
        |
        v
Forecasting Node
        |
        v
Offline Copilot + RAG
        |
        v
Planner Recommendation
        |
        v
Overlay Shield Policy Gate
        |
        v
Operator Approval -> Recoverer Action -> HMAC Audit
```

Use-case caption:

```text
Example: p1-p2 link predicted to breach 95% utilization in 4 minutes -> reroute LSP to backup path -> Guardian approves because action is reversible.
```

---

## Slide 6 - Wireframes / Mock Diagrams

Template asks:

- Wireframes / mock diagrams of proposed solution
- Optional

Recommended slide title:

```text
Operator Console Mockups
```

Paste-ready content:

```text
Primary screens:

1. Dashboard
   Live MPLS topology, router health, risky links, air-gap status

2. Forecasts
   Time-to-impact cards for predicted link/LSP breaches

3. Flow Divergence
   Heatmap showing where network traffic is building up abnormally

4. Copilot
   Operator asks: "Why is p1-p2 risk elevated?"
   Overlay answers with forecast, contributing signals, recommended action, and citations

5. Security Console
   Injection/spoof simulation, blocked actions, signed audit trail
```

Wireframe sketch to draw:

```text
Dashboard
------------------------------------------------
| Overlay | Air-gap: verified | Alerts: 2      |
------------------------------------------------
| MPLS topology graph                            |
| CE-A -> PE1 -> P1 -> P2 -> PE2 -> DC          |
| Link colors: green / amber / red              |
------------------------------------------------
| Predicted Breaches | Flow Divergence | Audit  |
------------------------------------------------

Copilot
------------------------------------------------
| Question: Why is p1-p2 risk elevated?          |
| Answer: Utilization will breach in 4m 12s...   |
| Evidence: divergence, BGP update rate, jitter  |
| Recommendation: reroute_lsp backup path        |
| [Approve] [Reject] [Modify]                    |
------------------------------------------------
```

---

## Slide 7 - Architecture Diagram

Template asks:

- Architecture diagram of the proposed solution

Recommended slide title:

```text
Air-Gapped Architecture
```

Paste-ready architecture blocks:

```text
Air-gap boundary:
All services run locally. No runtime cloud API calls.

Layer 1 - Network simulation / telemetry
Containerlab + FRR topology, SNMP, NetFlow/IPFIX, syslog, RSVP-TE, BGP events

Layer 2 - Domain adapter
MPLS Environment normalizes signals and exposes topology, actions, forecasts, and fault injection

Layer 3 - Agent swarm
Perceiver: anomaly + Helmholtz flow divergence
Planner: offline LLM + bandit fallback
Recoverer: reroute, failover, circuit breaker
Guardian: policy gates, injection detection, HMAC audit

Layer 4 - Advanced prediction layer
Time-series foundation models: Chronos-2, TimesFM, MOMENT, Granite TTM
Physics surrogate path: The Well-style datasets, PhysicsNeMo, FNO/PINO, graph neural networks

Layer 5 - Offline intelligence
Ollama local model, Chroma local vector store, offline RFC/vendor/runbook corpus

Layer 6 - Operator console
Dashboard, forecasts, flow-divergence heatmap, copilot, security/audit console
```

Diagram to draw:

```text
                         AIR-GAP BOUNDARY
+------------------------------------------------------------------+
| Operator Console                                                 |
| Dashboard | Forecasts | Flow View | Copilot | Security | Audit   |
|                          |                                       |
|                          v                                       |
| Django API + WebSocket + MCP                                     |
|                          |                                       |
|      +-------------------+-------------------+                   |
|      v                   v                   v                   |
| MPLS Domain        Agent Swarm          Offline AI               |
| Adapter            Perceiver            Ollama                   |
| Topology           Planner              Chroma/RAG               |
| Telemetry          Recoverer            RFC/runbooks             |
| Faults             Guardian                                      |
|      |                   |                                       |
|      v                   v                                       |
| Containerlab/FRR   HMAC Audit Store                              |
|      |                                                           |
|      v                                                           |
| Advanced Prediction Layer                                        |
| The Well-style spatiotemporal learning | PhysicsNeMo FNO/GNN     |
| Chronos-2 | TimesFM | MOMENT | Granite TTM telemetry forecasting |
+------------------------------------------------------------------+
```

Important callout:

```text
Zero outbound runtime dependency: cloud LLM and cloud vector DB are replaced by local Ollama and local Chroma.
```

---

## Slide 8 - Technologies Used

Template asks:

- Technologies to be used in the solution

Recommended slide title:

```text
Technology Stack
```

Paste-ready content:

```text
Backend:
Django, Django REST Framework, Channels/WebSocket, SQLite/PostgreSQL

Agent system:
4-agent swarm: Perceiver, Planner, Recoverer, Guardian
A2A signed messaging, three-tier fallback cascade

MPLS simulation and telemetry:
Containerlab, FRR, SNMP, NetFlow/IPFIX, syslog, NetworkX topology graph

Prediction and anomaly:
NumPy, scikit-learn, XGBoost/Kalman/HMM fallback, Helmholtz graph-flow decomposition, time-to-impact forecasting

Advanced forecasting and simulation:
Hugging Face time-series models: Chronos-2, TimesFM, MOMENT, IBM Granite TTM
Physics-inspired AI: The Well datasets, NVIDIA PhysicsNeMo, FNO/PINO neural operators, graph neural networks

Offline AI:
Ollama local model: Phi-3 Mini Q4 default, Mistral 7B optional
ChromaDB local vector store
Offline RFC/vendor docs/runbooks

Security:
HMAC-SHA256 audit signing, injection sentinel, policy auditor, air-gap egress monitor

Frontend:
Next.js, React, Tailwind, SWR, Zustand, topology/forecast/security views

Observability:
OpenTelemetry, OpenTelemetry eBPF Instrumentation, Prometheus, Jaeger, local audit logs
```

Suggested visual:

Use a 4-column stack:

```text
Network | AI/ML | Security | UI/Operations
```

---

## Slide 9 - Estimated Implementation Cost

Template asks:

- Estimated implementation cost
- Optional

Recommended slide title:

```text
Estimated Prototype Cost
```

Paste-ready content:

```text
Prototype target: local/offline demo for shortlisted phase

Estimated cost range: INR 80,000 - 1,50,000

Cost heads:
- Development workstation / GPU access: INR 40,000 - 70,000
- Network simulation environment: INR 0 - 15,000
  Containerlab + FRR are open-source; cost mainly compute/storage
- Offline model setup: INR 0 - 20,000
  Ollama + quantized open models; optional GPU upgrade
- Documentation and proposal assets: INR 10,000 - 20,000
- Testing, validation, and deployment packaging: INR 30,000 - 40,000

Open-source leverage:
Most stack components are open-source, keeping recurring cost low.
```

If you want a simpler version:

```text
Prototype cost: INR 80,000 - 1,50,000

Major cost drivers:
1. GPU/local compute
2. MPLS simulation setup
3. Offline model and RAG packaging
4. Validation against PS-13 scenarios

Recurring runtime cost:
Low, because the system is air-gapped and does not depend on paid cloud APIs.
```

Optional table:

| Item | Estimate |
|---|---:|
| Local compute/GPU | INR 40k-70k |
| Simulation + storage | INR 0-15k |
| Offline AI setup | INR 0-20k |
| Testing/documentation | INR 40k-60k |
| Total | INR 80k-150k |

---

## Slide 10 - Closing / Thank You

Template has no visible text placeholder, so use it as a final closing slide.

Recommended title:

```text
Project Overlay
```

Main line:

```text
Predict. Explain. Guard. Remediate.
```

Closing pitch:

```text
An offline predictive copilot for secure MPLS operations, built for environments where network intelligence must stay inside the air-gap.
```

Footer:

```text
Bharatiya Antariksh Hackathon 2026 | PS-13
Team Project Overlay
Contact: [email / phone]
```

Optional final diagram:

```text
Telemetry -> Prediction -> Explanation -> Guardian Approval -> Safe Action -> Signed Audit
```

---

## Extra: 30-Second Spoken Pitch

Use this if the judges ask for a quick explanation:

```text
Overlay is an air-gapped predictive copilot for MPLS and SD-WAN operations. It ingests local router telemetry, detects graph-flow anomalies using Helmholtz divergence, forecasts time-to-impact for link or LSP failures, and explains each risk through an offline LLM with local runbook citations. It does not call cloud APIs at runtime. Before any remediation, Overlay Shield checks policy, blocks unsafe actions, and signs every decision with HMAC audit proof. The result is a secure NOC workflow that moves from reactive alarm handling to predictive, explainable, human-approved remediation.
```

---

## Extra: 10-Second Pitch

```text
Overlay is the offline predictive eye for MPLS networks: it forecasts failures, explains the cause, and safely gates remediation inside an air-gapped environment.
```

---

## Extra: Advanced Technology Sources To Cite Verbally

Use these only if judges ask why the technology stack is modern:

- The Well / Polymathic AI: 15TB physics simulation collection for spatiotemporal physical systems; useful inspiration for network-flow surrogate modeling. Source: https://polymathic-ai.org/the_well/
- Hugging Face Polymathic AI: several The Well-style datasets are hosted on Hugging Face, but they are HDF5/scientific datasets, not always standard Dataset Viewer tables. Source: https://huggingface.co/polymathic-ai
- NVIDIA PhysicsNeMo: physics-ML framework with neural operators, Fourier Neural Operators, graph neural networks, and digital-twin style workflows. Source: https://developer.nvidia.com/physicsnemo
- Amazon Chronos-2: public time-series foundation model for zero-shot/universal forecasting. Source: https://huggingface.co/amazon/chronos-2
- Google TimesFM: open time-series foundation model family for forecasting. Source: https://huggingface.co/google/timesfm-2.5-200m-pytorch
- AutonLab MOMENT: open time-series foundation models for forecasting, classification, anomaly detection, and imputation. Source: https://huggingface.co/AutonLab/MOMENT-1-large
- IBM Granite Time Series / TinyTimeMixer: compact time-series models suitable for lightweight offline forecasting. Source: https://huggingface.co/ibm-granite/granite-timeseries-ttm-r2
- OpenTelemetry eBPF Instrumentation: zero-code Linux/application/network observability useful for local telemetry capture. Source: https://opentelemetry.io/docs/zero-code/obi/

Short judge-safe wording:

```text
We are not claiming to train a 15TB model during the hackathon. We use these modern tools as an upgrade path: The Well and PhysicsNeMo inform the physics-style digital twin, while Hugging Face time-series foundation models give us cold-start forecasting before enough MPLS-specific telemetry is collected.
```
