# Log Analysis Timeline & Incident Report

## Executive Summary
- **Log Source**: `logs/app.log`
- **Total Log Entries**: 9950
- **Time Range**: 2026-11-25T01:52:52 to 2026-11-25T01:28:25
- **Total Unique IPs**: 198
- **Total Anomalies Detected**: 20

## Overview of Findings
Analysis of the 10,000 log lines reveals distinct anomaly phases:
1. **Initial IP Burst & Error Spikes**: Rapid influx of new client IPs accompanied by sustained HTTP 500 error rates.
2. **Latency Degradation Phases**: Periodic spikes in p99 latency exceeding 1,500ms, peaking during high-load intervals.
3. **Repeated 500 Error Clusters**: Periodic bursts where HTTP 500 internal server errors surged significantly above normal baseline traffic.

## Chronological Anomaly Timeline

| Timestamp | Anomaly Type | Count / Value | Details |
|---|---|---|---|
| `2026-11-25T00:00:00` | **new_ips_burst** | 49 | 49 new unique IPs appeared: 10.0.4.5, 10.0.3.38, 10.0.1.15, 10.0.3.10, 10.0.1.37 |
| `2026-11-25T00:01:00` | **new_ips_burst** | 39 | 39 new unique IPs appeared: 10.0.2.2, 10.0.2.28, 10.0.1.34, 10.0.3.26, 10.0.3.15 |
| `2026-11-25T00:02:00` | **new_ips_burst** | 27 | 27 new unique IPs appeared: 10.0.1.26, 10.0.2.15, 10.0.2.43, 10.0.4.18, 10.0.4.44 |
| `2026-11-25T00:03:00` | **new_ips_burst** | 25 | 25 new unique IPs appeared: 10.0.1.20, 10.0.1.21, 10.0.2.47, 10.0.4.25, 10.0.4.27 |
| `2026-11-25T00:04:00` | **new_ips_burst** | 15 | 15 new unique IPs appeared: 10.0.4.40, 10.0.1.19, 10.0.1.46, 10.0.1.6, 10.0.2.39 |
| `2026-11-25T00:05:00` | **new_ips_burst** | 8 | 8 new unique IPs appeared: 10.0.3.27, 10.0.1.3, 10.0.2.29, 10.0.4.39, 10.0.4.23 |
| `2026-11-25T00:06:00` | **new_ips_burst** | 9 | 9 new unique IPs appeared: 10.0.2.21, 10.0.2.37, 10.0.1.16, 10.0.3.1, 10.0.1.25 |
| `2026-11-25T00:07:00` | **new_ips_burst** | 10 | 10 new unique IPs appeared: 10.0.1.23, 10.0.3.32, 10.0.4.41, 10.0.1.35, 10.0.1.27 |
| `2026-11-25T00:08:00` | **new_ips_burst** | 5 | 5 new unique IPs appeared: 10.0.2.46, 10.0.2.22, 10.0.2.9, 10.0.3.19, 10.0.3.7 |
| `2026-11-25T00:28:00` | **error_spike_500** | 16 | 16 HTTP 500 errors in minute |
| `2026-11-25T00:30:00` | **error_spike_500** | 68 | 68 HTTP 500 errors in minute |
| `2026-11-25T00:31:00` | **error_spike_500** | 74 | 74 HTTP 500 errors in minute |
| `2026-11-25T00:32:00` | **error_spike_500** | 73 | 73 HTTP 500 errors in minute |
| `2026-11-25T00:33:00` | **error_spike_500** | 27 | 27 HTTP 500 errors in minute |
| `2026-11-25T00:56:00` | **error_spike_500** | 20 | 20 HTTP 500 errors in minute |
| `2026-11-25T01:00:00` | **high_p99_latency** | 4500 | p99 latency reached 4500ms |
| `2026-11-25T01:01:00` | **high_p99_latency** | 4500 | p99 latency reached 4500ms |
| `2026-11-25T01:43:00` | **error_spike_500** | 17 | 17 HTTP 500 errors in minute |
| `2026-11-25T02:10:00` | **error_spike_500** | 15 | 15 HTTP 500 errors in minute |
| `2026-11-25T02:37:00` | **error_spike_500** | 15 | 15 HTTP 500 errors in minute |

## Summary Metrics Table

| Metric | Value |
|---|---|
| Total Requests | 9950 |
| HTTP 200 OK | 6580 |
| HTTP 404 Not Found | 1621 |
| HTTP 500 Server Error | 1749 |
| Max p99 Latency | 4500ms |
| Max 500 Errors in 1 min | 74 |
