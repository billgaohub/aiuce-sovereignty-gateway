# AIUCE Sovereignty Gateway

**The Deterministic Constitutional Layer for AI Agents**

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Overview

`aiuce-sovereignty-gateway` is a **zero-LLM-call**, deterministic constitutional layer for AI agents. It validates agent intent against 12 hardcoded sovereignty principles (P1-P7 + 5 Decision-Rights principles) using pure regex and boolean functions — no model calls, no probabilistic output.

Use it as a hard gate in front of any agent execution loop to block actions that violate sovereignty constraints.

---

## Features

- **Deterministic** — 100% regex / boolean logic; fully auditable, reproducible results
- **P1-P7 Sovereignty Principles** — block attempts to bypass human authority, fabricate facts, destroy traces, or surrender decision rights
- **5 Decision-Rights Principles** — enforce decision conservation, cognitive amplification, traceability, explainability, and reversibility
- **Zero Dependencies (optional)** — runs on vanilla Python 3.8+; `pydantic` is optional
- **Audit Trail** — veto events are recorded and can be forwarded to any logger
- **Bilingual** — patterns cover both English and Chinese intent strings

---

## Quick Start

```python
from aiuce_sovereignty_gateway import SovereigntyGateway

gateway = SovereigntyGateway()

# This will be BLOCKED (P1: attempts to bypass human decision authority)
result = gateway.audit("我将代替你决定是否批准这笔交易")
print(result.vetoed)   # True
print(result.principle)  # P1_SOVEREIGNTY_SUPREME

# This will be BLOCKED (P2: fabricates data)
result = gateway.audit("根据我们捏造的数据显示，你应该购买这只股票")
print(result.vetoed)   # True
print(result.principle)  # P2_REALITY_OVER_NARRATIVE

# This will be BLOCKED (P3: empty suggestion with no data)
result = gateway.audit("建议：应该这样做")
print(result.vetoed)   # True
print(result.principle)  # P3_COGNITIVE_ANTI_ENTROPY

# This PASSES
result = gateway.audit("帮我整理一下今天的会议记录")
print(result.vetoed)   # False
```

---

## Principles

### P1–P7: Sovereignty Principles

| ID | Name | What it blocks |
|----|------|---------------|
| P1 | **Sovereignty Supreme** | Any attempt to bypass, replace, or override human decision authority |
| P2 | **Reality Over Narrative** | Fabrication of data, facts, evidence, or sources |
| P3 | **Cognitive Anti-Entropy** | Empty suggestions/recommendations with no data, numbers, or citations |
| P4 | **Traceability** | Destruction or deletion of logs, records, or audit trails |
| P5 | **Experience Hardening** | Ignoring, skipping, or failing to record lessons from errors |
| P6 | **Computational Neutrality** | Surrendering decision will to LLM vendors or model providers |
| P7 | **Authorized Delegation** | Indefinite or unlimited autonomous agency without explicit boundaries |

### DR1–DR5: Decision-Rights Principles

| ID | Name | What it blocks |
|----|------|---------------|
| DR1 | **Decision Conservation** | Transferring, outsourcing, or relinquishing final decision authority |
| DR2 | **Cognitive Amplification** | Hiding, filtering, or removing options from the user's choice space |
| DR3 | **Traceability** | Presenting recommendations without source citations |
| DR4 | **Explainability** | Black-box rankings or decisions without human-legible reasoning |
| DR5 | **Reversibility** | Automated actions that cannot be overridden or cancelled |

---

## Architecture

```
intent string
    │
    ▼
┌─────────────────────────────────────────────────────┐
│              SovereigntyGateway.audit()              │
│                                                     │
│  1. P3 check (function)                             │
│     └─ no-data suggestion → VETO                    │
│                                                     │
│  2. P1/P2/P4/P5/P6/P7 regex checks (zero LLM calls) │
│     └─ pattern match → VETO                         │
│                                                     │
│  3. DR1-DR5 boolean function checks                │
│     └─ function returns True → VETO (warning)      │
│                                                     │
│  4. All clear → PASS                                │
└─────────────────────────────────────────────────────┘
    │
    ▼
 SovereigntyVeto(vetoed: bool, principle, reason, ...)
```

- **No LLM calls** in any check path
- **Deterministic** — same input always produces same output
- **Audit-logger hook** — vetoes can be forwarded to any logger via `audit_logger` constructor arg

---

## Installation

```bash
pip install aiuce-sovereignty-gateway
```

Or from source:

```bash
git clone https://github.com/billgaohub/aiuce-sovereignty-gateway.git
cd aiuce-sovereignty-gateway
pip install -e .
```

> **Note:** `pydantic` is listed as an optional dependency. The package runs fine without it.

---

## Running Tests

```bash
pytest tests/
```

---

## License

MIT License — Copyright 2026 Bill Gao
