# Friday Infra Cleanup Incident Notes

- DevOps rotated TLS certs on the public CDN (note: staging nginx uses plain HTTP port 80 internally, so CDN TLS is unrelated).
- DBA ran `VACUUM ANALYZE` on analytics replica (unrelated to payment-worker).
- Someone renamed `REDIS_URL` to `REDIS_URI` during env cleanup and trimmed keys from `staging.env`.
- Ops also reported payment-worker container marked unhealthy even after startup; check `logs/worker_crash.log`.
