# Postmortem: API Outage (2026-11-20)

## Summary
On November 20, 2026, the primary API experienced a 45-minute outage starting at 10:00 UTC, returning HTTP 500 errors to clients. The incident was triggered by a database connection pool exhaustion issue. Service was fully restored at 10:45 UTC following a restart of the connection pool.

## Impact
- **Duration:** 45 minutes (10:00 UTC – 10:45 UTC)
- **Services Affected:** Primary API service
- **User Impact:** Clients experienced HTTP 500 internal server errors and failed API requests during the outage window.

## Root Cause
The database connection pool became exhausted, preventing incoming API requests from acquiring database connections. This led to cascading request failures and HTTP 500 error responses across the API service.

## Timeline
| Time (UTC) | Event |
|------------|-------|
| 10:00 | First 500 errors observed |
| 10:15 | Monitoring alert fired |
| 10:30 | Investigation started |
| 10:45 | Resolved (connection pool restarted) |

## Action Items
1. **Investigate connection pool exhaustion:** Determine the underlying cause of the connection pool depletion (e.g., connection leaks, slow queries, traffic spike, or insufficient pool sizing).
2. **Improve connection pool monitoring:** Add real-time metrics and alerts for connection pool utilization thresholds before exhaustion occurs.
3. **Automate recovery / failover:** Implement automatic recovery or graceful handling for exhausted connection pools to reduce mean time to resolution (MTTR).
