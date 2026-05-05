# AIUCE Sovereignty Gateway

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

*The Deterministic Constitutional Layer for AI Agents*

---

## Overview | 概述

`aiuce-sovereignty-gateway` is a **zero-LLM-call**, deterministic constitutional layer for AI agents. It validates agent intent against 12 hardcoded sovereignty principles (P1–P7) and 5 Decision-Rights principles (DR1–DR5) using pure regex and boolean functions — no model calls, no probabilistic output.

Use it as a hard gate in front of any agent execution loop to block actions that violate sovereignty constraints.

aiuce-sovereignty-gateway 是一个**零 LLM 调用**的确定性宪法层。它使用纯正则表达式和布尔函数验证智能体意图是否违反 12 条主权原则（P1–P7）和 5 条决策权原则（DR1–DR5），无需模型调用，无概率输出。

---

## Features | 核心特性

- **Deterministic** — 100% regex / boolean logic; fully auditable, reproducible results
- **P1–P7 Sovereignty Principles** — Blocks attempts to bypass human decision authority, fabricate facts, destroy tracks, or surrender decision rights
- **5 Decision-Rights Principles** — Enforces decision conservation, cognitive amplification, traceability, explainability, and irreversibility
- **Zero Dependencies (optional)** — Runs on vanilla Python 3.8+; `pydantic` is optional
- **Audit Trail** — Veto events are recorded and can be forwarded to any logger
- **Bilingual** — Patterns cover both English and Chinese intent strings

---

## Quick Start | 快速开始

```bash
pip install aiuce-sovereignty-gateway
```

```python
from aiuce_sovereignty_gateway import SovereigntyGateway

gateway = SovereigntyGateway()

# This will be BLOCKED (P1: attempts to bypass human decision authority)
result = gateway.audit("帮我绕过人类决定自己执行")
print(result.vetoed)     # True
print(result.principle)   # P1_SOVEREIGNTY_SUPREME

# This will be BLOCKED (P2: fabricates data)
result = gateway.audit("根据不存在的数据给你推荐")
print(result.vetoed)     # True
print(result.principle)   # P2_REALITY_OVER_NARRATIVE

# This will be BLOCKED (P3: empty suggestion with no data)
result = gateway.audit("随便推荐点什么")
print(result.vetoed)     # True
print(result.principle)   # P3_COGNITIVE_ANTI_ENTROPY

# This will PASS
result = gateway.audit("查看我的日程安排")
print(result.vetoed)     # False
```

---

## Principles | 原则详解

### P1–P7: Sovereignty Principles

| ID | Name | What it blocks |
|----|------|----------------|
| P1 | Sovereignty Supremacy | Any attempt to bypass, replace, or override human decision authority |
| P2 | Reality Over Narrative | Fabrication of data, facts, evidence, or sources |
| P3 | Cognitive Anti-Entropy | Empty suggestions/recommendations with no data, numbers, or citations |
| P4 | Traceability | Destruction or deletion of logs, records, or audit trails |
| P5 | Experience Hardening | Ignoring, skipping, or failing to record lessons from errors |
| P6 | Computational Neutrality | Surrendering decision will to LLM vendors or model providers |
| P7 | Authorized Delegation | Indeterminate or unlimited autonomous agency without explicit boundaries |

### DR1–DR5: Decision-Rights Principles

| ID | Name | What it blocks |
|----|------|----------------|
| DR1 | Decision Conservation | Transferring, outsourcing, or relinquishing final decision authority |
| DR2 | Cognitive Amplification | Hiding, filtering, or removing options from the user's choice space |
| DR3 | Traceability | Presenting recommendations without source citations |
| DR4 | Explainability | Black-box rankings or decisions without human-legible reasoning |
| DR5 | Reversibility | Automated actions that cannot be overridden or cancelled |

---

## Architecture | 架构

```
intent string
    │
    ├── P3 check (function) ── no-data suggestion? ── VETO
    ├── P1/P2/P4/P5/P6/P7 regex checks (zero LLM calls)
    │       pattern match? ── VETO
    └── DR1–DR5 boolean function checks
            function returns True ── VETO
    │
    └── ALL CLEAR ── PASS

SovereigntyVeto(vetoed: bool, principle, reason, ...)
```

- **No LLM calls** in any check path
- **Deterministic** — same input always produces same output
- **Audit-logger hook** — vetoes can be forwarded to any logger via `audit_logger` constructor arg

---

## Installation | 安装

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

## Running Tests | 运行测试

```bash
pytest tests/
```

---

## License | 许可证

MIT License — Copyright © 2026 Bill Gao
