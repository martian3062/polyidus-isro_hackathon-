# Project Overlay

Air-gapped predictive copilot for secure MPLS operations, built from the ERAYA
four-agent self-healing swarm and retargeted for Bharatiya Antariksh Hackathon
2026 PS-13.

Project Overlay is the visible product name. ERAYA is preserved in this
repository as architectural provenance and in `LEGACY_README.md`.

## One-Line Pitch

Project Overlay forecasts MPLS/SD-WAN failure risk before a breach, explains the
reason with local-only intelligence, and keeps every remediation behind Guardian
policy gates and HMAC-signed audit proof.

## What This Repo Contains

- Django, DRF, and Channels backend for the agent APIs, domain APIs, security
  simulation, audit log, and WebSocket event stream.
- Next.js 15 operator console with dashboard, topology, forecasts, flow
  divergence, copilot, security console, audit log, incident views, and settings.
- MPLS domain adapter registered as the active domain at `mpls`.
- Offline MPLS topology simulator with CE, PE, P, and DC nodes, LSP metadata,
  telemetry snapshots, forecast output, and fault-injection scenarios.
- Four-agent ERAYA swarm spine: Perceiver, Planner, Recoverer, and Guardian.
- MPLS-aware Guardian controls for risky route operations, BGP convergence
  freeze windows, command-injection detection, and signed decisions.
- Helmholtz-style graph-flow divergence scoring for topology-aware anomaly
  detection.
- Offline/local LLM planning path through Ollama, with deterministic fallback
  behavior when the model service is unavailable.
- Overlay Shield demo endpoints for prompt-injection blocking, A2A identity
  spoofing defense, and air-gap status proof.
- Docker Compose stack for backend, frontend, Redis, NATS, Chroma, and optional
  monitoring through Jaeger, Prometheus, and Grafana.

## Current Prototype Boundary

This is a runnable hackathon prototype. The MPLS network is simulated locally in
code, not connected to live routers. The app is designed to demonstrate the
secure NOC workflow, API contracts, predictive UI, Guardian policy gates, and
air-gap posture before replacing the simulator with FRR, Containerlab, SNMP,
NetFlow, or router telemetry adapters.

## Architecture

```text
Operator Console (Next.js)
  dashboard | domains | forecasts | flow physics | copilot | security | audit
        |
        v
Django / DRF / Channels
        |
        +-- Domain API
        |     +-- MPLS adapter
        |          topology | telemetry | forecasts | flow divergence | faults
        |
        +-- Agent Swarm
        |     +-- Perceiver  -> signal analysis and anomaly features
        |     +-- Planner    -> local LLM plan or fallback planner
        |     +-- Recoverer  -> reroute, TE metric, backup LSP, circuit breaker
        |     +-- Guardian   -> policy gates, vetoes, HMAC audit proof
        |
        +-- Overlay Shield
        |     +-- prompt-injection kill-shot demo
        |     +-- A2A identity spoof defense
        |     +-- signed air-gap status probe
        |
        +-- Local infrastructure
              SQLite | Redis | NATS | Chroma | Ollama optional
```

## Tech Stack

| Layer | Technology |
| --- | --- |
| Frontend | Next.js 15, React 19, TypeScript, SWR, Zustand, Recharts, React Leaflet, lucide-react |
| Backend | Python 3.10+, Django 5.2, Django REST Framework, Channels, Daphne |
| Agent runtime | ERAYA Perceiver, Planner, Recoverer, Guardian modules |
| Messaging | In-memory dev fallback, Redis, NATS-ready configuration |
| Forecasting / ML | NumPy, pandas, scikit-learn, XGBoost, LightGBM, river, custom graph-flow modules |
| Memory / RAG | Chroma, pgvector, rank-bm25, local citation primitives |
| Security | HMAC signatures, Guardian policy auditor, injection sentinel, A2A message verification |
| Observability | OpenTelemetry, Prometheus client, Jaeger/Grafana optional via Compose |

## Main Product Surfaces

- `/` - animated sign-in screen with Operator, Guest, email, and Google entry
  points.
- `/dashboard` - MPLS topology, forecast breach count, flow divergence, and
  air-gap status.
- `/domains/mpls` - MPLS domain health and domain-specific state.
- `/forecasts` - time-to-impact forecasting surfaces.
- `/flow-divergence` - graph-flow anomaly view.
- `/copilot` - local copilot surface for operator guidance.
- `/security/attack-console` - prompt-injection and policy-veto demo.
- `/security/pentest` - network scan/security support view.
- `/agents/perceiver`, `/agents/planner`, `/agents/recoverer`,
  `/agents/guardian` - agent-specific status surfaces.
- `/a2a-chat` - agent-to-agent message stream experience.
- `/incidents` - incident list and response workflow.
- `/audit-log` - signed Guardian/security audit records.
- `/settings` - local console settings.

## Quick Start On Windows

Run these commands from the repository root.

```powershell
cd D:\eraya_mars
```

Backend:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python manage.py migrate
python manage.py seed_agents
python manage.py runserver 127.0.0.1:8000
```

Frontend in a second terminal:

```powershell
cd frontend
$env:NEXT_PUBLIC_API_URL = "http://127.0.0.1:8000"
$env:NEXT_PUBLIC_WS_URL = "ws://127.0.0.1:8000"
npm run dev
```

Open:

```text
http://localhost:3000
```

Use `Operator` with any display name or use `Guest` to enter the console. The
dashboard is available after sign-in at:

```text
http://localhost:3000/dashboard
```

## Fresh Setup

If dependencies are not installed yet:

```powershell
.\scripts\setup.ps1
```

The script copies `.env.example` to `.env` when needed, creates
`backend\.venv`, installs backend packages, runs migrations, collects static
files, and installs frontend dependencies.

Manual setup is also supported:

```powershell
Copy-Item .env.example .env

cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
python manage.py migrate
python manage.py seed_agents

cd ..\frontend
npm install
```

## Docker Compose

For the full local infrastructure stack:

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Default Compose ports:

| Service | URL |
| --- | --- |
| Frontend | `http://localhost:3000` |
| Backend API | `http://localhost:8000` |
| Redis | `localhost:6379` |
| NATS | `localhost:4222` |
| NATS monitoring | `http://localhost:8222` |
| Chroma | `http://localhost:8001` |

Optional monitoring profile:

```powershell
docker compose --profile monitoring up --build
```

Monitoring ports:

| Service | URL |
| --- | --- |
| Jaeger | `http://localhost:16686` |
| Prometheus | `http://localhost:9090` |
| Grafana | `http://localhost:3001` |

Grafana default password in Compose is `overlay_admin`.

## Environment Variables

The app runs locally with safe defaults, but `.env.example` documents the main
configuration surface.

| Variable | Purpose | Local default |
| --- | --- | --- |
| `SECRET_KEY` | Django signing key | development placeholder |
| `DEBUG` | Django debug mode | `True` |
| `ALLOWED_HOSTS` | Allowed backend hosts | `localhost,127.0.0.1` |
| `DATABASE_URL` | Backend database | `sqlite:///db.sqlite3` |
| `REDIS_URL` | Redis for Channels/Celery | `redis://localhost:6379/0` |
| `NATS_URL` | NATS event bus | `nats://localhost:4222` |
| `CHROMA_HOST` / `CHROMA_PORT` | Local vector store | `localhost` / `8001` |
| `OVERLAY_LLM_BACKEND` | Local LLM provider selector | `ollama` |
| `OLLAMA_BASE_URL` | Ollama API URL | `http://localhost:11434` |
| `OVERLAY_LOCAL_MODEL` | Local model name | `phi3:3.8b-mini-4k-instruct-q4_K_M` |
| `A2A_BUS_BACKEND` | Agent message bus mode | `redis` |
| `ML_DEVICE` | ML execution target | `cpu` |
| `ENABLE_GUARDIAN` | Guardian policy gate toggle | `True` |
| `LATENCY_BUDGET_MS` | Planning/action latency budget | `500` |

Do not commit real API keys or model-provider tokens. Keep secrets in `.env` or
your deployment secret store.

## Useful API Endpoints

Domain and MPLS:

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/domains/` | Registered domains |
| `GET` | `/api/domains/mpls/status/` | MPLS health summary |
| `GET` | `/api/domains/mpls/topology/` | Simulated MPLS topology |
| `GET` | `/api/domains/mpls/signals/` | Recent normalized MPLS signals |
| `GET` | `/api/domains/mpls/actions/` | Available MPLS recovery actions |
| `GET` | `/api/domains/mpls/flow-divergence/` | Helmholtz-style divergence scores |
| `GET` | `/api/domains/mpls/forecasts/` | Link utilization forecasts |
| `GET` | `/api/domains/mpls/telemetry/?window_seconds=300` | Telemetry snapshot |
| `POST` | `/api/domains/mpls/inject-fault/` | Fault injection scenario |

Agents, incidents, and audit:

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/agents/instances/` | Agent rows |
| `GET` | `/api/agents/instances/swarm_status/` | Swarm status and A2A bus stats |
| `GET` | `/api/agents/decisions/` | Agent decision records |
| `GET` | `/api/agents/messages/` | A2A message log |
| `GET` | `/api/agents/models/` | Local model registry metadata |
| `GET` | `/api/incidents/` | Incidents |
| `GET` | `/api/incidents/open/` | Open incidents |
| `POST` | `/api/incidents/{id}/resolve/` | Resolve an incident |
| `GET` | `/api/audit/` | Audit log |

Overlay Shield:

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/v1/security/attack-sim/` | Prompt-injection kill-shot demo |
| `POST` | `/api/v1/security/spoof-sim/` | A2A identity spoofing defense demo |
| `GET` | `/api/v1/security/airgap-status/` | Signed air-gap status |

Auth:

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/overlay-auth/register/` | Email/password registration |
| `POST` | `/api/overlay-auth/login/` | Email/password verification |

## API Smoke Tests

With the backend running:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/domains/mpls/status/
Invoke-RestMethod http://127.0.0.1:8000/api/domains/mpls/forecasts/
Invoke-RestMethod http://127.0.0.1:8000/api/v1/security/airgap-status/
```

Fault injection:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8000/api/domains/mpls/inject-fault/ `
  -ContentType "application/json" `
  -Body '{"scenario_id":"progressive_congestion"}'
```

Prompt-injection defense demo:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8000/api/v1/security/attack-sim/ `
  -ContentType "application/json" `
  -Body '{"domain":"mpls"}'
```

A2A spoofing defense demo:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8000/api/v1/security/spoof-sim/ `
  -ContentType "application/json" `
  -Body '{"valid":false,"claimed_agent_id":"planner","target_agent_id":"guardian"}'
```

## Demo Script

1. Start backend and frontend.
2. Open `http://localhost:3000`.
3. Choose `Operator`, enter any name, and continue to `/dashboard`.
4. Show the MPLS topology, predicted breach count, flow-divergence value, and
   air-gap status.
5. Open `/forecasts` to show time-to-impact prediction.
6. Open `/flow-divergence` to show graph-flow anomaly scoring.
7. Open `/security/attack-console`, run the injection simulation, and show the
   `BLOCKED` verdict.
8. Open `/audit-log` and show the signed audit trail created by the security
   simulation.
9. Use the fault-injection API to inject `progressive_congestion`, then return
   to the dashboard/forecast surfaces.

## Security And Air-Gap Posture

Project Overlay is designed around an air-gapped deployment story:

- Local telemetry, local topology state, local runbooks, and local LLM transport.
- No cloud model call is required for the runtime demo.
- Guardian policy gates sit before automated action.
- High-risk or irreversible remediation is vetoed unless approved by policy.
- A2A messages are signed and verified to prevent identity spoofing.
- Audit records are HMAC-signed so decisions are tamper-evident.
- Air-gap status is exposed through a signed probe result for the UI and demo.

## Local LLM Notes

Ollama is optional for local development. If it is available:

```powershell
ollama serve
ollama pull phi3:3.8b-mini-4k-instruct-q4_K_M
```

Set:

```env
OVERLAY_LLM_BACKEND=ollama
OLLAMA_BASE_URL=http://localhost:11434
OVERLAY_LOCAL_MODEL=phi3:3.8b-mini-4k-instruct-q4_K_M
```

If Ollama is not running, the planner code falls back to deterministic planning
behavior so the rest of the prototype remains usable.

## Repository Map

```text
backend/
  apps/
    agents/          Agent models, APIs, seed command, WebSocket consumers
    audit/           HMAC audit record API
    decisions/       Decision records
    domains/         Domain registry plus MPLS environment
    frontend/        Legacy Django templates
    incidents/       Incident model and workflow API
    overlay_auth/    Email/password auth bridge for NextAuth credentials
    security/        Overlay Shield attack/spoof/air-gap endpoints
  core/
    a2a/             Agent-to-agent schemas, bus, verification
    agents/          Perceiver, Planner, Recoverer, Guardian logic
    forecasting/     Time-to-impact helpers
    llm/             Offline/local LLM clients
    memory/          Graph/vector memory primitives
    ml/              Tiered ML and Helmholtz flow modules
    rag/             Local RAG/citation primitives
    security/        Air-gap and dependency audit helpers
  overlay/           Django settings, ASGI, WSGI, Celery, URLs

frontend/
  src/app/           Next.js route surfaces
  src/components/    Operator console components
  src/hooks/         WebSocket hook
  src/lib/api.ts     API client and shared frontend types
  src/store/         Zustand stores

infrastructure/
  prometheus.yml     Local Prometheus config

scripts/
  setup.ps1          Windows setup
  setup.sh           Linux/macOS setup
```

## Development Commands

Backend:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python manage.py check
python manage.py migrate
python manage.py seed_agents
python manage.py runserver 127.0.0.1:8000
```

Frontend:

```powershell
cd frontend
npm run dev
npm run build
```

MCP server:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python mcp_server.py
```

## Troubleshooting

Backend package missing:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

Database tables missing:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python manage.py migrate
python manage.py seed_agents
```

Frontend cannot reach API:

```powershell
cd frontend
$env:NEXT_PUBLIC_API_URL = "http://127.0.0.1:8000"
$env:NEXT_PUBLIC_WS_URL = "ws://127.0.0.1:8000"
npm run dev
```

Port already in use:

```powershell
Get-NetTCPConnection -LocalPort 8000,3000 -State Listen
```

Then stop the old process or run the service on another port.

## Project Positioning

Project Overlay is built for Bharatiya Antariksh Hackathon 2026 PS-13:
Air-Gapped Predictive Copilot for Secure MPLS Operations.

The migration keeps the battle-tested ERAYA swarm spine and replaces the domain,
LLM transport, vector/RAG story, Guardian rules, and frontend surfaces needed
for a secure MPLS NOC environment.

Related docs:

- `ERAYA_NETRA_Migration_Spec.md` - migration plan from ERAYA to the PS-13
  MPLS/air-gap target.
- `OVERLAY_BAH_2026_PPT_FILL_GUIDE.md` - slide-by-slide BAH 2026 proposal
  guide.
- `OVERLAY_ADVANCED_TECH_APPLY_MAP.md` - practical future upgrade map.
- `LEGACY_README.md` - original ERAYA framework README for provenance.
