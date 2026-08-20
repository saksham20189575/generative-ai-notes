# 🕸️ Module 9 — Multi-Agent Systems & Automation

One agent doing everything hits a ceiling. This module splits work across **role-based agents** — researcher, writer, editor — and wires them into real automation with **HTTP APIs**, **triggers**, and **signed webhooks**.

## Topics

| # | Topic | Notes |
|---|-------|:-----:|
| 36 | Multi-Agent Architecture, HTTP & Automation Foundations | [📖](36-Multi-Agent-Architecture-and-HTTP-Automation/) |
| 38 | n8n LLM Integration and AI Workflow Nodes | [📖](38-n8n-LLM-Integration-and-AI-Workflow-Nodes/) |
| 39 | Building End-to-End AI Automation Pipelines with n8n | [📖](39-End-to-End-AI-Automation-Pipelines-with-n8n/) |
| 40 | CrewAI: Roles, Tasks, and First Multi-Agent Crew | [📖](40-CrewAI-Roles-Tasks-and-First-Multi-Agent-Crew/) |

## Related hands-on labs

See [`Coding-Examples/multi_agent_http_automation/`](../Coding-Examples/multi_agent_http_automation/) — the researcher → writer → editor pipeline behind a `POST` trigger, with an HMAC-signed webhook callback, signature verification, and idempotent retry handling. Run `python3 main.py` for the zero-dependency version.

⬅️ [Back to course home](../)
