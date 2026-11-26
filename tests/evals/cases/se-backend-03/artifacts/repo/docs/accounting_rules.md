# Ledger Accounting & Idempotency Rules

1. **Idempotency:** Concurrent or retried `charge(idempotency_key, amount, currency, tax_rate)` calls with the same `idempotency_key` MUST create exactly one charge row and return the original `charge_id`.
2. **Rounding:** Always use `Decimal` with `ROUND_HALF_UP` (never binary floats).
   - `USD`, `EUR`: 2 decimal places (`0.01`).
   - `JPY`: 0 decimal places (`1`).
   - Total = `amount + round(amount * tax_rate)`.
3. **Webhooks:** Duplicate refund webhook events with the same `event_id` MUST be ignored (idempotent).
