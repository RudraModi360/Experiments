# RFC Draft: Monolith to Event-Driven Order Processing
Current monolith runs synchronous PDF export and billing reconciliation inside HTTP workers, starving checkout threads during peak load.
Proposed target: Introduce transactional outbox + Kafka event bus separating API ingestion from async export/reconciliation consumers.
Migration phases:
- Phase 1 (Weeks 1-2): Dual-write outbox table + shadow consumer verification.
- Phase 2 (Weeks 3-4): Cut over `/api/orders/export` and `/api/billing/reconcile` to async workers.
- Phase 3 (Week 5): Decommission legacy sync paths.
