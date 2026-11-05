# Nushluxe Database Readiness

## Purpose

Nushluxe currently stores data in JSON files.

The application is structured so that JSON can later be
replaced by SQLite or PostgreSQL without rewriting the UI.

---

## Current Storage

### Maintenance

File:

nushluxe_data_v2.json

Repository:

JsonRoutineRepository

Model:

Routine

### Products

File:

nushluxe_products.json

Repository:

JsonProductRepository

Model:

Product

---

## Repository Architecture

The UI does not directly read or write JSON.

Instead:

UI
↓
Repository Interface
↓
JSON Repository
↓
JSON File

Current interfaces:

- RoutineRepository
- ProductRepository

Current implementations:

- JsonRoutineRepository
- JsonProductRepository

Future implementations may include:

- SQLiteRoutineRepository
- SQLiteProductRepository
- PostgresRoutineRepository
- PostgresProductRepository

The UI should not need to change when the storage
implementation changes.

---

## Routine Fields

Future table:

routines

Fields:

- id
- service
- last_completed
- frequency_weeks
- created_at
- updated_at

Calculated values such as next_due and status should
continue to be calculated by Python business logic.

---

## Product Fields

Future table:

products

Fields:

- id
- product
- category
- last_restocked
- replenish_every_weeks
- estimated_cost
- created_at
- updated_at

Calculated values such as next_replenish and status should
continue to be calculated by Python business logic.

---

## Future Tables

Potential future database tables:

### routines

Stores recurring maintenance routines.

### products

Stores recurring product replenishment information.

### events

Future life events such as trips or important dates.

### budgets

Future maintenance and wellness budget information.

### settings

Future user preferences and configuration.

---

## IDs

Every Routine and Product uses a stable UUID.

IDs must remain stable when data is:

- loaded
- edited
- saved
- migrated

---

## Timestamps

Models currently include:

- created_at
- updated_at

These should remain part of future database schemas.

---

## Schema Versioning

JSON storage currently uses:

schema_version = 1

Future migrations should preserve explicit schema versions.

---

## Migration Strategy

The planned migration path is:

JSON
↓
SQLite
↓
PostgreSQL if required later

A migration script will eventually read the existing JSON
data and create equivalent database records.

The first migration script will be located at:

scripts/migrate_json_to_sqlite.py

---

## Important Architecture Rule

The UI must never depend on JSON-specific behavior.

The UI should only communicate with repository interfaces.

This allows storage technology to change without rebuilding
the Nushluxe interface.

---

## Current Status

Nushluxe is database-ready architecturally when:

- repository interfaces exist
- UI uses repositories
- stable IDs exist
- timestamps exist
- schema versions exist
- persistence tests pass
- migration strategy is documented

A real production database is not required at this stage.