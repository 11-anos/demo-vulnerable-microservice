# demo-vulnerable-microservice

A **demo repository** for the [Hindsight DevOps Guardrail AI](https://github.com/MasirJafri1/hack-baroda) project.

This repo contains a realistic Python microservice with **intentionally introduced security anti-patterns** in its commit history. It is designed to trigger the full agentic audit pipeline — including all 9 stages through to a `BLOCKED` verdict.

---

## What This Repo Demonstrates

| Commit | Description | Expected Verdict |
|---|---|---|
| `initial-safe-service` | Clean, production-grade code | ✅ APPROVED |
| `feat/scale-optimizations` | Risky changes — pool/websocket/SQL/Dockerfile issues | ❌ BLOCKED |

---

## How to Test

1. Open the **Hindsight DevOps Guardrail AI** dashboard
2. Select **GitHub Crawler** mode
3. Enter: `MasirJafri1/demo-vulnerable-microservice`
4. Click **Start Audit** — watch all 9 agents run

The second commit will trigger matches against historical incidents **INC-001** through **INC-005** in the Hindsight database, causing the full expert review path to activate.

---

## Files

```
app/
  main.py          # FastAPI entrypoint
  db.py            # Database layer
  ws_handler.py    # WebSocket handler
  config.py        # App configuration
infra/
  main.tf          # Terraform security groups
Dockerfile
requirements.txt
```
