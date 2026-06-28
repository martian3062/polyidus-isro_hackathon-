# Polyidus (ERAYA)

Air-gapped predictive copilot for secure MPLS operations, retargeted from the
ERAYA four-archetype self-healing agent swarm.

## What This Build Contains

- MPLS/SD-WAN domain adapter registered as the primary domain: `mpls`
- Perceiver MPLS tiers with link-utilization rules and Helmholtz flow divergence
- Recoverer MPLS tiers for reroute, TE metric adjustment, backup LSP failover,
  and circuit-breaker fallback
- Polyidus Shield Guardian updates: R004 routing restart gate, R005 BGP
  convergence freeze, and MPLS command-injection detection
- Offline LLM transport through local Ollama instead of Groq
- Local RAG primitives with citation IDs for offline runbooks and RFC context
- Air-gap status endpoint with HMAC-signed egress probe result
- Next.js operator console rethemed around MPLS topology, forecasts,
  flow-divergence, and copilot views
- MCP tools for topology, telemetry, forecasts, and fault injection

The original ERAYA README is preserved in `LEGACY_README.md` for provenance.

## Core Claim

Polyidus forecasts MPLS failure risk before breach, explains the prediction
through local-only context, and keeps every automated action behind Guardian
policy gates and HMAC audit proof.

## Architecture

```text
Operator Console
  dashboard | forecasts | flow-divergence | copilot | Polyidus Shield
        |
        v
Django / DRF / Channels
        |
        +-- Perceiver -> Helmholtz flow divergence + MPLS risk tiers
        +-- Planner   -> Ollama local JSON planner + Thompson fallback
        +-- Recoverer -> topology reroute + backup LSP fallback
        +-- Guardian  -> R001-R005 policy gates + HMAC audit
        |
        +-- MPLS domain adapter
        |     topology | telemetry snapshot | forecasts | fault injection
        |
        +-- Air-gap monitor
              forbidden cloud-host probe + signed status response
```

## Run Locally

Backend:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

Frontend:

```powershell
cd frontend
npm install
npm run dev
```

Default frontend URL: `http://localhost:3000/dashboard`

## Useful Endpoints

- `GET /api/domains/`
- `GET /api/domains/mpls/status/`
- `GET /api/domains/mpls/topology/`
- `GET /api/domains/mpls/flow-divergence/`
- `GET /api/domains/mpls/forecasts/`
- `GET /api/domains/mpls/telemetry/?window_seconds=300`
- `POST /api/domains/mpls/inject-fault/`
- `GET /api/v1/security/airgap-status/`
- `POST /api/v1/security/attack-sim/`

## Offline LLM

Set the local model through environment variables:

```env
POLYIDUS_LLM_BACKEND=ollama
OLLAMA_BASE_URL=http://localhost:11434
POLYIDUS_LOCAL_MODEL=phi3:3.8b-mini-4k-instruct-q4_K_M
```

If Ollama is unavailable, `LLMPlannerAgent` falls back through the existing
PlannerAgent tier cascade.

## Proposal Positioning

Polyidus is built for Bharatiya Antariksh Hackathon 2026 PS-13:
Air-Gapped Predictive Copilot for Secure MPLS Operations.

The migration keeps the battle-tested ERAYA swarm spine and replaces the domain,
LLM transport, vector/RAG story, Guardian rules, and frontend surfaces needed
for a secure MPLS NOC environment.

# polyidus-isro_hackathon-
