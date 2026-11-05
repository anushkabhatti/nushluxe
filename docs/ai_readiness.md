# Nushluxe AI Readiness

## Purpose

Nushluxe is designed so AI interprets structured facts
rather than calculating core planning information itself.

The application must continue to work completely without AI.

---

## Current Status

Real AI is currently disabled.

In:

intelligence/intelligence_service.py

the feature flag is:

ENABLE_AI = False

The current intelligence layer provides:

- build_ai_context()
- explain_plan()

explain_plan() is currently only a placeholder.

No external AI API is required for the foundation version.

---

## AI Context Contract

build_ai_context() returns structured information similar to:

{
    "today": "YYYY-MM-DD",
    "maintenance": [],
    "products": [],
    "summary": {},
    "budget": null,
    "constraints": []
}

The AI should receive already-calculated facts.

---

## Deterministic Rules

Python remains responsible for:

- maintenance due dates
- product replenishment dates
- statuses
- costs
- overdue logic
- planning summaries

AI must not replace these calculations.

---

## AI Responsibilities

Future AI may:

- explain the user's planning facts
- summarize priorities
- make structured information conversational
- explain why something needs attention
- help the user understand a plan

---

## AI Restrictions

Future AI must not:

- invent due dates
- invent replenishment dates
- invent costs
- alter stored user data without an explicit action
- become the source of truth for deterministic calculations

---

## Future Environment Variables

A future AI integration may require an API credential.

The credential must never be written directly inside Python files.

It should be loaded through a secure environment variable
or Streamlit secrets configuration.

Example variable name:

OPENAI_API_KEY

Do not place a real key in:

- app.py
- intelligence_service.py
- documentation
- tests
- GitHub

---

## Secrets

Local secrets may eventually be stored in:

.streamlit/secrets.toml

That file must not be committed to GitHub.

A future .gitignore will exclude it.

Never paste a real secret into documentation or example files.

---

## Future Prompt Contract

The future Nushluxe AI prompt should follow these principles:

1. Use only the structured facts provided by Nushluxe.
2. Do not invent dates.
3. Do not invent costs.
4. Do not silently change user data.
5. Clearly distinguish facts from suggestions.
6. Keep recommendations grounded in the provided context.
7. If information is missing, state that it is missing.

---

## Example Future Flow

Maintenance
+
Products
↓
Planning Facts
↓
AI Context
↓
AI Interpretation
↓
User-Friendly Explanation

---

## Feature Flag

Real AI must remain optional.

Current setting:

ENABLE_AI = False

The application must function normally when AI is disabled.

---

## Foundation Acceptance Criteria

Nushluxe is AI-ready when:

- build_ai_context() returns structured facts
- AI does not calculate dates or costs
- a prompt contract is documented
- secrets are not committed
- ENABLE_AI remains False
- the application works without AI

Real AI integration will happen after the foundation roadmap.