# Nushluxe

Nushluxe is a personal maintenance intelligence platform for recurring beauty and wellness maintenance and product replenishment.

The current V1 combines maintenance routines and product replenishment into one structured planning system.

Nushluxe is currently in customer discovery. Major new product features are intentionally paused while customer interviews are used to determine which problems and features should be prioritized next.

---

## Current Version

This repository contains the Nushluxe V1 foundation prototype.

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
- isolated temporary demo data for each visitor
- demo data reset
- user feedback link

Real AI is intentionally disabled in the current V1.

---

## Live Demo

Nushluxe is live at:

https://nushluxe.streamlit.app

> Demo version: data is temporary and may reset. Do not enter personal or sensitive information.

---

## How to Run Locally

### Requirements

- Python 3.12
- Conda
- Git

### 1. Clone the repository

```bash
git clone https://github.com/anushkabhatti/nushluxe.git
cd nushluxe