# Nushluxe

Nushluxe is a personal maintenance intelligence platform
for recurring beauty and wellness maintenance and product
replenishment.

The current version combines maintenance routines and
product replenishment into one structured planning system.

Future versions will add financial planning, life-event
context, personalization, and AI interpretation.

---

## Current Version

This repository contains the Nushluxe foundation prototype.

Current capabilities include:

- recurring maintenance tracking
- product replenishment tracking
- automatic next-date calculations
- maintenance statuses
- product replenishment statuses
- product cost tracking
- Products dashboard
- combined Maintenance + Products planning facts
- combined planning overview
- JSON persistence
- stable IDs
- timestamps
- schema versioning
- repository architecture
- JSON-to-SQLite migration tooling
- data backup/export
- AI-ready structured context
- automated tests

Real AI is intentionally disabled in this foundation version.
---

## Live Demo

Nushluxe is live at:

https://nushluxe.streamlit.app

> Demo version: data may reset and is not intended for personal or sensitive information.

---

## How to Run Locally

### Requirements

- Python 3.12
- Conda
- Git

### 1. Create the local environment

```bash
conda create -n nushluxe -c conda-forge python=3.12 -y
---

## Product Vision

Nushluxe aims to turn personal maintenance from a
collection of reminders into a plan.

The long-term system is intended to combine:

Maintenance
+
Products
+
Costs
+
Budget
+
Life Events
+
Personal Context
↓
Nushluxe Intelligence
↓
Personalized Planning

The eventual goal is to help users understand:

- what needs attention
- what needs replenishing
- what is overdue
- what upcoming maintenance may cost
- what should be prioritized
- what can reasonably wait

---

## Current Architecture

The project uses a modular architecture:

```text
Nushluxe_Streamlit/
├── app.py
├── core/
│   ├── maintenance.py
│   ├── products.py
│   └── planning.py
├── storage/
│   ├── repositories.py
│   └── json_repository.py
├── ui/
│   ├── maintenance_ui.py
│   ├── products_ui.py
│   └── planning_ui.py
├── intelligence/
│   └── intelligence_service.py
├── utils/
│   └── dates.py
├── tests/
├── scripts/
│   ├── migrate_json_to_sqlite.py
│   └── export_backup.py
├── docs/
│   ├── database_readiness.md
│   └── ai_readiness.md
└── README.md