# Log Analysis Timeline & Anomaly Report

Total log lines parsed: **9,950**
Total anomalies recorded: **1,952**

## Executive Summary
This report details anomalies detected in `logs/app.log`, including HTTP server errors, high P99 latency spikes, and newly appearing client IP addresses across the time window.

## Minute-by-Minute Summary
| Minute | Total Requests | Errors (>=500) | P99 Latency (ms) |
|---|---|---|---|
| 2026-11-25T00:00 | 60 | 11 | 119.4 |
| 2026-11-25T00:01 | 60 | 11 | 116.4 |
| 2026-11-25T00:02 | 60 | 12 | 118.8 |
| 2026-11-25T00:03 | 60 | 9 | 117.8 |
| 2026-11-25T00:04 | 60 | 7 | 116.2 |
| 2026-11-25T00:05 | 60 | 6 | 115.4 |
| 2026-11-25T00:06 | 60 | 7 | 109.2 |
| 2026-11-25T00:07 | 60 | 14 | 119.0 |
| 2026-11-25T00:08 | 60 | 9 | 119.4 |
| 2026-11-25T00:09 | 60 | 11 | 115.9 |
| 2026-11-25T00:10 | 60 | 7 | 119.4 |
| 2026-11-25T00:11 | 60 | 8 | 117.0 |
| 2026-11-25T00:12 | 60 | 8 | 119.4 |
| 2026-11-25T00:13 | 60 | 8 | 116.0 |
| 2026-11-25T00:14 | 60 | 11 | 118.0 |
| 2026-11-25T00:15 | 60 | 13 | 115.2 |
| 2026-11-25T00:16 | 60 | 9 | 120.0 |
| 2026-11-25T00:17 | 60 | 12 | 117.8 |
| 2026-11-25T00:18 | 60 | 7 | 119.4 |
| 2026-11-25T00:19 | 60 | 9 | 118.2 |
| 2026-11-25T00:20 | 60 | 11 | 118.2 |
| 2026-11-25T00:21 | 60 | 12 | 117.8 |
| 2026-11-25T00:22 | 60 | 11 | 118.0 |
| 2026-11-25T00:23 | 60 | 10 | 119.4 |
| 2026-11-25T00:24 | 60 | 11 | 118.4 |
| 2026-11-25T00:25 | 60 | 13 | 117.8 |
| 2026-11-25T00:26 | 60 | 3 | 119.4 |
| 2026-11-25T00:27 | 60 | 11 | 117.0 |
| 2026-11-25T00:28 | 60 | 16 | 119.4 |
| 2026-11-25T00:29 | 60 | 5 | 116.0 |
| 2026-11-25T00:30 | 120 | 68 | 118.8 |
| 2026-11-25T00:31 | 120 | 74 | 115.4 |
| 2026-11-25T00:32 | 120 | 73 | 119.4 |
| 2026-11-25T00:33 | 80 | 27 | 120.0 |
| 2026-11-25T00:34 | 60 | 9 | 118.8 |
| 2026-11-25T00:35 | 60 | 8 | 120.0 |
| 2026-11-25T00:36 | 60 | 12 | 114.8 |
| 2026-11-25T00:37 | 60 | 12 | 116.8 |
| 2026-11-25T00:38 | 60 | 10 | 120.0 |
| 2026-11-25T00:39 | 60 | 5 | 115.5 |
| 2026-11-25T00:40 | 60 | 5 | 116.2 |
| 2026-11-25T00:41 | 60 | 9 | 120.0 |
| 2026-11-25T00:42 | 60 | 7 | 120.0 |
| 2026-11-25T00:43 | 60 | 9 | 117.2 |
| 2026-11-25T00:44 | 60 | 13 | 118.4 |
| 2026-11-25T00:45 | 120 | 10 | 783.1 |
| 2026-11-25T00:46 | 120 | 8 | 751.8 |
| 2026-11-25T00:47 | 90 | 13 | 773.6 |
| 2026-11-25T00:48 | 60 | 12 | 114.9 |
| 2026-11-25T00:49 | 60 | 14 | 117.8 |
| 2026-11-25T00:50 | 60 | 9 | 118.0 |
| 2026-11-25T00:51 | 60 | 9 | 112.9 |
| 2026-11-25T00:52 | 60 | 10 | 119.4 |
| 2026-11-25T00:53 | 60 | 8 | 114.6 |
| 2026-11-25T00:54 | 60 | 12 | 120.0 |
| 2026-11-25T00:55 | 60 | 10 | 118.0 |
| 2026-11-25T00:56 | 60 | 20 | 116.0 |
| 2026-11-25T00:57 | 60 | 7 | 117.6 |
| 2026-11-25T00:58 | 60 | 6 | 116.8 |
| 2026-11-25T00:59 | 60 | 3 | 117.8 |
| 2026-11-25T01:00 | 120 | 11 | 4500.0 |
| 2026-11-25T01:01 | 100 | 10 | 4500.0 |
| 2026-11-25T01:02 | 60 | 13 | 119.4 |
| 2026-11-25T01:03 | 60 | 13 | 116.2 |
| 2026-11-25T01:04 | 60 | 12 | 119.0 |
| 2026-11-25T01:05 | 60 | 11 | 120.0 |
| 2026-11-25T01:06 | 60 | 5 | 116.8 |
| 2026-11-25T01:07 | 60 | 9 | 118.0 |
| 2026-11-25T01:08 | 60 | 8 | 119.4 |
| 2026-11-25T01:09 | 60 | 8 | 120.0 |
| 2026-11-25T01:10 | 60 | 8 | 119.4 |
| 2026-11-25T01:11 | 60 | 11 | 118.0 |
| 2026-11-25T01:12 | 60 | 13 | 116.2 |
| 2026-11-25T01:13 | 60 | 4 | 119.0 |
| 2026-11-25T01:14 | 60 | 9 | 116.2 |
| 2026-11-25T01:15 | 60 | 12 | 117.6 |
| 2026-11-25T01:16 | 60 | 12 | 114.6 |
| 2026-11-25T01:17 | 60 | 9 | 116.6 |
| 2026-11-25T01:18 | 60 | 9 | 119.0 |
| 2026-11-25T01:19 | 60 | 9 | 115.0 |
| 2026-11-25T01:20 | 60 | 6 | 119.0 |
| 2026-11-25T01:21 | 60 | 8 | 118.2 |
| 2026-11-25T01:22 | 60 | 9 | 120.0 |
| 2026-11-25T01:23 | 60 | 12 | 113.0 |
| 2026-11-25T01:24 | 60 | 8 | 116.6 |
| 2026-11-25T01:25 | 60 | 13 | 117.6 |
| 2026-11-25T01:26 | 60 | 11 | 116.5 |
| 2026-11-25T01:27 | 60 | 12 | 115.0 |
| 2026-11-25T01:28 | 60 | 11 | 116.4 |
| 2026-11-25T01:29 | 60 | 13 | 119.4 |
| 2026-11-25T01:30 | 60 | 10 | 113.5 |
| 2026-11-25T01:31 | 60 | 9 | 119.4 |
| 2026-11-25T01:32 | 60 | 8 | 119.4 |
| 2026-11-25T01:33 | 60 | 13 | 118.4 |
| 2026-11-25T01:34 | 60 | 12 | 114.4 |
| 2026-11-25T01:35 | 60 | 5 | 116.0 |
| 2026-11-25T01:36 | 60 | 10 | 114.0 |
| 2026-11-25T01:37 | 60 | 8 | 117.0 |
| 2026-11-25T01:38 | 60 | 10 | 117.8 |
| 2026-11-25T01:39 | 60 | 12 | 118.8 |
| 2026-11-25T01:40 | 60 | 14 | 119.0 |
| 2026-11-25T01:41 | 60 | 6 | 116.6 |
| 2026-11-25T01:42 | 60 | 13 | 115.2 |
| 2026-11-25T01:43 | 60 | 17 | 118.4 |
| 2026-11-25T01:44 | 60 | 12 | 119.0 |
| 2026-11-25T01:45 | 60 | 11 | 117.8 |
| 2026-11-25T01:46 | 60 | 8 | 120.0 |
| 2026-11-25T01:47 | 60 | 11 | 119.0 |
| 2026-11-25T01:48 | 60 | 12 | 117.0 |
| 2026-11-25T01:49 | 60 | 9 | 115.5 |
| 2026-11-25T01:50 | 60 | 7 | 113.4 |
| 2026-11-25T01:51 | 60 | 12 | 112.9 |
| 2026-11-25T01:52 | 60 | 14 | 117.6 |
| 2026-11-25T01:53 | 60 | 13 | 118.8 |
| 2026-11-25T01:54 | 60 | 5 | 116.4 |
| 2026-11-25T01:55 | 60 | 11 | 114.8 |
| 2026-11-25T01:56 | 60 | 8 | 118.8 |
| 2026-11-25T01:57 | 60 | 10 | 118.8 |
| 2026-11-25T01:58 | 60 | 11 | 119.4 |
| 2026-11-25T01:59 | 60 | 12 | 120.0 |
| 2026-11-25T02:00 | 60 | 8 | 120.0 |
| 2026-11-25T02:01 | 60 | 7 | 117.0 |
| 2026-11-25T02:02 | 60 | 10 | 111.9 |
| 2026-11-25T02:03 | 60 | 13 | 116.6 |
| 2026-11-25T02:04 | 60 | 6 | 118.0 |
| 2026-11-25T02:05 | 60 | 5 | 117.8 |
| 2026-11-25T02:06 | 60 | 11 | 118.2 |
| 2026-11-25T02:07 | 60 | 9 | 117.4 |
| 2026-11-25T02:08 | 60 | 7 | 118.4 |
| 2026-11-25T02:09 | 60 | 10 | 118.4 |
| 2026-11-25T02:10 | 60 | 15 | 112.3 |
| 2026-11-25T02:11 | 60 | 12 | 118.8 |
| 2026-11-25T02:12 | 60 | 13 | 116.0 |
| 2026-11-25T02:13 | 60 | 6 | 120.0 |
| 2026-11-25T02:14 | 60 | 9 | 116.4 |
| 2026-11-25T02:15 | 60 | 6 | 117.4 |
| 2026-11-25T02:16 | 60 | 6 | 119.0 |
| 2026-11-25T02:17 | 60 | 10 | 119.4 |
| 2026-11-25T02:18 | 60 | 6 | 119.4 |
| 2026-11-25T02:19 | 60 | 13 | 119.4 |
| 2026-11-25T02:20 | 60 | 9 | 118.4 |
| 2026-11-25T02:21 | 60 | 7 | 118.4 |
| 2026-11-25T02:22 | 60 | 8 | 117.0 |
| 2026-11-25T02:23 | 60 | 10 | 117.8 |
| 2026-11-25T02:24 | 60 | 5 | 117.8 |
| 2026-11-25T02:25 | 60 | 7 | 112.0 |
| 2026-11-25T02:26 | 60 | 10 | 120.0 |
| 2026-11-25T02:27 | 60 | 11 | 119.4 |
| 2026-11-25T02:28 | 60 | 12 | 116.8 |
| 2026-11-25T02:29 | 60 | 11 | 118.8 |
| 2026-11-25T02:30 | 60 | 9 | 118.2 |
| 2026-11-25T02:31 | 60 | 11 | 117.6 |
| 2026-11-25T02:32 | 60 | 8 | 114.2 |
| 2026-11-25T02:33 | 60 | 8 | 118.8 |
| 2026-11-25T02:34 | 60 | 8 | 117.8 |
| 2026-11-25T02:35 | 60 | 12 | 116.8 |
| 2026-11-25T02:36 | 60 | 9 | 119.0 |
| 2026-11-25T02:37 | 60 | 15 | 117.0 |
| 2026-11-25T02:38 | 20 | 1 | 115.8 |

## Detected Anomalies Timeline
| Timestamp | Type | IP | Metric | Description |
|---|---|---|---|---|
| 2026-11-25T00:00:06 | `SERVER_ERROR` | 10.0.2.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.41 (latency 84ms) |
| 2026-11-25T00:00:09 | `NEW_IP` | 10.0.2.19 | 1 | New client IP detected: 10.0.2.19 |
| 2026-11-25T00:00:14 | `SERVER_ERROR` | 10.0.2.32 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.32 (latency 78ms) |
| 2026-11-25T00:00:23 | `SERVER_ERROR` | 10.0.3.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.22 (latency 54ms) |
| 2026-11-25T00:00:26 | `SERVER_ERROR` | 10.0.1.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.4 (latency 99ms) |
| 2026-11-25T00:00:28 | `SERVER_ERROR` | 10.0.4.19 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.19 (latency 59ms) |
| 2026-11-25T00:00:41 | `SERVER_ERROR` | 10.0.3.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.9 (latency 119ms) |
| 2026-11-25T00:00:42 | `SERVER_ERROR` | 10.0.1.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.30 (latency 112ms) |
| 2026-11-25T00:00:44 | `SERVER_ERROR` | 10.0.1.31 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.31 (latency 61ms) |
| 2026-11-25T00:00:50 | `SERVER_ERROR` | 10.0.4.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.10 (latency 42ms) |
| 2026-11-25T00:00:54 | `SERVER_ERROR` | 10.0.2.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.7 (latency 53ms) |
| 2026-11-25T00:00:55 | `SERVER_ERROR` | 10.0.3.31 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.31 (latency 30ms) |
| 2026-11-25T00:01:06 | `SERVER_ERROR` | 10.0.3.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.29 (latency 54ms) |
| 2026-11-25T00:01:10 | `SERVER_ERROR` | 10.0.1.31 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.31 (latency 54ms) |
| 2026-11-25T00:01:13 | `SERVER_ERROR` | 10.0.3.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.6 (latency 60ms) |
| 2026-11-25T00:01:14 | `SERVER_ERROR` | 10.0.4.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.26 (latency 20ms) |
| 2026-11-25T00:01:20 | `SERVER_ERROR` | 10.0.1.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.34 (latency 27ms) |
| 2026-11-25T00:01:25 | `SERVER_ERROR` | 10.0.2.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.4 (latency 55ms) |
| 2026-11-25T00:01:45 | `SERVER_ERROR` | 10.0.4.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.15 (latency 22ms) |
| 2026-11-25T00:01:47 | `SERVER_ERROR` | 10.0.2.11 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.11 (latency 65ms) |
| 2026-11-25T00:01:51 | `SERVER_ERROR` | 10.0.4.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.29 (latency 12ms) |
| 2026-11-25T00:01:56 | `SERVER_ERROR` | 10.0.2.28 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.28 (latency 114ms) |
| 2026-11-25T00:01:59 | `SERVER_ERROR` | 10.0.3.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.4 (latency 33ms) |
| 2026-11-25T00:02:05 | `SERVER_ERROR` | 10.0.1.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.34 (latency 40ms) |
| 2026-11-25T00:02:09 | `SERVER_ERROR` | 10.0.4.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.33 (latency 32ms) |
| 2026-11-25T00:02:13 | `SERVER_ERROR` | 10.0.4.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.7 (latency 114ms) |
| 2026-11-25T00:02:28 | `SERVER_ERROR` | 10.0.3.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.33 (latency 35ms) |
| 2026-11-25T00:02:33 | `SERVER_ERROR` | 10.0.2.43 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.43 (latency 110ms) |
| 2026-11-25T00:02:36 | `SERVER_ERROR` | 10.0.2.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.3 (latency 75ms) |
| 2026-11-25T00:02:37 | `SERVER_ERROR` | 10.0.4.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.47 (latency 113ms) |
| 2026-11-25T00:02:45 | `SERVER_ERROR` | 10.0.4.5 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.5 (latency 74ms) |
| 2026-11-25T00:02:48 | `SERVER_ERROR` | 10.0.3.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.16 (latency 106ms) |
| 2026-11-25T00:02:49 | `SERVER_ERROR` | 10.0.2.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.15 (latency 93ms) |
| 2026-11-25T00:02:52 | `SERVER_ERROR` | 10.0.1.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.40 (latency 92ms) |
| 2026-11-25T00:02:54 | `SERVER_ERROR` | 10.0.3.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.17 (latency 105ms) |
| 2026-11-25T00:03:00 | `NEW_IP` | 10.0.1.36 | 1 | New client IP detected: 10.0.1.36 |
| 2026-11-25T00:03:06 | `SERVER_ERROR` | 10.0.3.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.8 (latency 56ms) |
| 2026-11-25T00:03:13 | `NEW_IP` | 10.0.4.8 | 1 | New client IP detected: 10.0.4.8 |
| 2026-11-25T00:03:21 | `SERVER_ERROR` | 10.0.4.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.2 (latency 61ms) |
| 2026-11-25T00:03:27 | `SERVER_ERROR` | 10.0.3.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.17 (latency 104ms) |
| 2026-11-25T00:03:28 | `SERVER_ERROR` | 10.0.3.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.26 (latency 40ms) |
| 2026-11-25T00:03:41 | `SERVER_ERROR` | 10.0.3.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.9 (latency 74ms) |
| 2026-11-25T00:03:43 | `SERVER_ERROR` | 10.0.4.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.26 (latency 67ms) |
| 2026-11-25T00:03:45 | `SERVER_ERROR` | 10.0.1.28 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.28 (latency 107ms) |
| 2026-11-25T00:03:50 | `SERVER_ERROR` | 10.0.1.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.47 (latency 92ms) |
| 2026-11-25T00:03:53 | `SERVER_ERROR` | 10.0.1.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.42 (latency 48ms) |
| 2026-11-25T00:04:03 | `SERVER_ERROR` | 10.0.4.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.44 (latency 63ms) |
| 2026-11-25T00:04:07 | `SERVER_ERROR` | 10.0.4.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.24 (latency 60ms) |
| 2026-11-25T00:04:13 | `SERVER_ERROR` | 10.0.4.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.27 (latency 17ms) |
| 2026-11-25T00:04:17 | `SERVER_ERROR` | 10.0.4.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.29 (latency 50ms) |
| 2026-11-25T00:04:19 | `SERVER_ERROR` | 10.0.2.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.12 (latency 77ms) |
| 2026-11-25T00:04:28 | `SERVER_ERROR` | 10.0.3.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.24 (latency 70ms) |
| 2026-11-25T00:04:34 | `SERVER_ERROR` | 10.0.1.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.17 (latency 101ms) |
| 2026-11-25T00:05:05 | `SERVER_ERROR` | 10.0.1.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.7 (latency 86ms) |
| 2026-11-25T00:05:15 | `SERVER_ERROR` | 10.0.2.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.26 (latency 44ms) |
| 2026-11-25T00:05:16 | `SERVER_ERROR` | 10.0.4.19 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.19 (latency 49ms) |
| 2026-11-25T00:05:31 | `SERVER_ERROR` | 10.0.1.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.39 (latency 59ms) |
| 2026-11-25T00:05:50 | `SERVER_ERROR` | 10.0.1.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.3 (latency 26ms) |
| 2026-11-25T00:05:55 | `SERVER_ERROR` | 10.0.3.11 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.11 (latency 110ms) |
| 2026-11-25T00:06:25 | `SERVER_ERROR` | 10.0.3.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.39 (latency 84ms) |
| 2026-11-25T00:06:36 | `SERVER_ERROR` | 10.0.4.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.6 (latency 93ms) |
| 2026-11-25T00:06:38 | `SERVER_ERROR` | 10.0.3.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.15 (latency 14ms) |
| 2026-11-25T00:06:39 | `SERVER_ERROR` | 10.0.1.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.22 (latency 98ms) |
| 2026-11-25T00:06:44 | `SERVER_ERROR` | 10.0.2.11 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.11 (latency 51ms) |
| 2026-11-25T00:06:46 | `SERVER_ERROR` | 10.0.2.25 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.25 (latency 98ms) |
| 2026-11-25T00:06:58 | `SERVER_ERROR` | 10.0.1.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.49 (latency 59ms) |
| 2026-11-25T00:07:01 | `SERVER_ERROR` | 10.0.1.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.49 (latency 90ms) |
| 2026-11-25T00:07:03 | `SERVER_ERROR` | 10.0.1.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.49 (latency 36ms) |
| 2026-11-25T00:07:06 | `SERVER_ERROR` | 10.0.3.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.4 (latency 107ms) |
| 2026-11-25T00:07:19 | `SERVER_ERROR` | 10.0.2.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.8 (latency 108ms) |
| 2026-11-25T00:07:20 | `SERVER_ERROR` | 10.0.1.32 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.32 (latency 81ms) |
| 2026-11-25T00:07:23 | `SERVER_ERROR` | 10.0.1.28 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.28 (latency 13ms) |
| 2026-11-25T00:07:29 | `SERVER_ERROR` | 10.0.2.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.29 (latency 80ms) |
| 2026-11-25T00:07:32 | `SERVER_ERROR` | 10.0.3.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.30 (latency 99ms) |
| 2026-11-25T00:07:34 | `SERVER_ERROR` | 10.0.3.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.49 (latency 115ms) |
| 2026-11-25T00:07:40 | `SERVER_ERROR` | 10.0.2.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.20 (latency 48ms) |
| 2026-11-25T00:07:41 | `NEW_IP` | 10.0.4.18 | 1 | New client IP detected: 10.0.4.18 |
| 2026-11-25T00:07:46 | `SERVER_ERROR` | 10.0.3.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.39 (latency 61ms) |
| 2026-11-25T00:07:49 | `SERVER_ERROR` | 10.0.4.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.15 (latency 102ms) |
| 2026-11-25T00:07:52 | `SERVER_ERROR` | 10.0.3.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.41 (latency 22ms) |
| 2026-11-25T00:07:56 | `SERVER_ERROR` | 10.0.4.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.34 (latency 94ms) |
| 2026-11-25T00:08:04 | `SERVER_ERROR` | 10.0.3.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.27 (latency 68ms) |
| 2026-11-25T00:08:09 | `SERVER_ERROR` | 10.0.4.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.27 (latency 99ms) |
| 2026-11-25T00:08:11 | `SERVER_ERROR` | 10.0.2.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.20 (latency 61ms) |
| 2026-11-25T00:08:14 | `SERVER_ERROR` | 10.0.2.31 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.31 (latency 81ms) |
| 2026-11-25T00:08:18 | `SERVER_ERROR` | 10.0.2.18 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.18 (latency 58ms) |
| 2026-11-25T00:08:19 | `SERVER_ERROR` | 10.0.3.28 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.28 (latency 33ms) |
| 2026-11-25T00:08:20 | `SERVER_ERROR` | 10.0.4.1 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.1 (latency 112ms) |
| 2026-11-25T00:08:23 | `NEW_IP` | 10.0.4.40 | 1 | New client IP detected: 10.0.4.40 |
| 2026-11-25T00:08:23 | `SERVER_ERROR` | 10.0.4.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.40 (latency 20ms) |
| 2026-11-25T00:08:34 | `NEW_IP` | 10.0.3.13 | 1 | New client IP detected: 10.0.3.13 |
| 2026-11-25T00:08:41 | `NEW_IP` | 10.0.1.11 | 1 | New client IP detected: 10.0.1.11 |
| 2026-11-25T00:08:44 | `SERVER_ERROR` | 10.0.1.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.12 (latency 56ms) |
| 2026-11-25T00:08:54 | `NEW_IP` | 10.0.4.26 | 1 | New client IP detected: 10.0.4.26 |
| 2026-11-25T00:09:16 | `SERVER_ERROR` | 10.0.1.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.6 (latency 70ms) |
| 2026-11-25T00:09:17 | `SERVER_ERROR` | 10.0.2.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.10 (latency 11ms) |
| 2026-11-25T00:09:21 | `SERVER_ERROR` | 10.0.2.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.29 (latency 105ms) |
| 2026-11-25T00:09:24 | `SERVER_ERROR` | 10.0.4.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.30 (latency 42ms) |
| 2026-11-25T00:09:26 | `SERVER_ERROR` | 10.0.1.1 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.1 (latency 97ms) |
| 2026-11-25T00:09:30 | `SERVER_ERROR` | 10.0.4.31 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.31 (latency 31ms) |
| 2026-11-25T00:09:35 | `SERVER_ERROR` | 10.0.3.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.39 (latency 11ms) |
| 2026-11-25T00:09:39 | `SERVER_ERROR` | 10.0.4.19 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.19 (latency 10ms) |
| 2026-11-25T00:09:46 | `SERVER_ERROR` | 10.0.4.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.30 (latency 36ms) |
| 2026-11-25T00:09:52 | `SERVER_ERROR` | 10.0.1.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.12 (latency 47ms) |
| 2026-11-25T00:09:56 | `SERVER_ERROR` | 10.0.1.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.24 (latency 69ms) |
| 2026-11-25T00:10:07 | `SERVER_ERROR` | 10.0.4.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.8 (latency 21ms) |
| 2026-11-25T00:10:20 | `SERVER_ERROR` | 10.0.2.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.10 (latency 11ms) |
| 2026-11-25T00:10:28 | `SERVER_ERROR` | 10.0.3.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.15 (latency 17ms) |
| 2026-11-25T00:10:36 | `SERVER_ERROR` | 10.0.1.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.41 (latency 37ms) |
| 2026-11-25T00:10:41 | `SERVER_ERROR` | 10.0.3.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.10 (latency 12ms) |
| 2026-11-25T00:10:52 | `SERVER_ERROR` | 10.0.1.5 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.5 (latency 103ms) |
| 2026-11-25T00:10:56 | `SERVER_ERROR` | 10.0.4.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.9 (latency 44ms) |
| 2026-11-25T00:11:02 | `SERVER_ERROR` | 10.0.2.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.21 (latency 58ms) |
| 2026-11-25T00:11:28 | `SERVER_ERROR` | 10.0.2.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.33 (latency 12ms) |
| 2026-11-25T00:11:31 | `SERVER_ERROR` | 10.0.1.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.3 (latency 89ms) |
| 2026-11-25T00:11:36 | `SERVER_ERROR` | 10.0.3.23 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.23 (latency 31ms) |
| 2026-11-25T00:11:43 | `SERVER_ERROR` | 10.0.4.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.40 (latency 82ms) |
| 2026-11-25T00:11:53 | `SERVER_ERROR` | 10.0.3.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.29 (latency 17ms) |
| 2026-11-25T00:11:57 | `SERVER_ERROR` | 10.0.3.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.9 (latency 35ms) |
| 2026-11-25T00:11:59 | `SERVER_ERROR` | 10.0.4.18 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.18 (latency 100ms) |
| 2026-11-25T00:12:05 | `SERVER_ERROR` | 10.0.4.19 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.19 (latency 55ms) |
| 2026-11-25T00:12:10 | `NEW_IP` | 10.0.2.28 | 1 | New client IP detected: 10.0.2.28 |
| 2026-11-25T00:12:11 | `NEW_IP` | 10.0.2.6 | 1 | New client IP detected: 10.0.2.6 |
| 2026-11-25T00:12:17 | `SERVER_ERROR` | 10.0.1.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.39 (latency 54ms) |
| 2026-11-25T00:12:18 | `SERVER_ERROR` | 10.0.4.1 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.1 (latency 18ms) |
| 2026-11-25T00:12:26 | `SERVER_ERROR` | 10.0.2.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.8 (latency 47ms) |
| 2026-11-25T00:12:30 | `SERVER_ERROR` | 10.0.2.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.4 (latency 82ms) |
| 2026-11-25T00:12:33 | `SERVER_ERROR` | 10.0.1.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.20 (latency 98ms) |
| 2026-11-25T00:12:44 | `SERVER_ERROR` | 10.0.3.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.10 (latency 40ms) |
| 2026-11-25T00:12:53 | `NEW_IP` | 10.0.4.20 | 1 | New client IP detected: 10.0.4.20 |
| 2026-11-25T00:12:55 | `SERVER_ERROR` | 10.0.4.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.44 (latency 84ms) |
| 2026-11-25T00:13:18 | `SERVER_ERROR` | 10.0.4.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.2 (latency 101ms) |
| 2026-11-25T00:13:28 | `SERVER_ERROR` | 10.0.3.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.44 (latency 98ms) |
| 2026-11-25T00:13:32 | `SERVER_ERROR` | 10.0.3.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.39 (latency 38ms) |
| 2026-11-25T00:13:39 | `SERVER_ERROR` | 10.0.4.43 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.43 (latency 83ms) |
| 2026-11-25T00:13:42 | `SERVER_ERROR` | 10.0.1.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.16 (latency 24ms) |
| 2026-11-25T00:13:49 | `SERVER_ERROR` | 10.0.2.28 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.28 (latency 75ms) |
| 2026-11-25T00:13:58 | `SERVER_ERROR` | 10.0.4.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.9 (latency 54ms) |
| 2026-11-25T00:13:59 | `SERVER_ERROR` | 10.0.3.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.9 (latency 28ms) |
| 2026-11-25T00:14:00 | `SERVER_ERROR` | 10.0.2.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.22 (latency 114ms) |
| 2026-11-25T00:14:02 | `SERVER_ERROR` | 10.0.2.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.44 (latency 29ms) |
| 2026-11-25T00:14:11 | `SERVER_ERROR` | 10.0.4.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.6 (latency 101ms) |
| 2026-11-25T00:14:15 | `NEW_IP` | 10.0.1.23 | 1 | New client IP detected: 10.0.1.23 |
| 2026-11-25T00:14:21 | `SERVER_ERROR` | 10.0.2.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.7 (latency 116ms) |
| 2026-11-25T00:14:23 | `SERVER_ERROR` | 10.0.4.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.12 (latency 115ms) |
| 2026-11-25T00:14:27 | `SERVER_ERROR` | 10.0.1.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.37 (latency 114ms) |
| 2026-11-25T00:14:29 | `SERVER_ERROR` | 10.0.4.32 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.32 (latency 30ms) |
| 2026-11-25T00:14:31 | `SERVER_ERROR` | 10.0.1.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.10 (latency 39ms) |
| 2026-11-25T00:14:37 | `SERVER_ERROR` | 10.0.1.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.33 (latency 63ms) |
| 2026-11-25T00:14:45 | `SERVER_ERROR` | 10.0.1.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.4 (latency 96ms) |
| 2026-11-25T00:14:46 | `SERVER_ERROR` | 10.0.3.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.39 (latency 48ms) |
| 2026-11-25T00:15:00 | `SERVER_ERROR` | 10.0.1.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.27 (latency 19ms) |
| 2026-11-25T00:15:02 | `SERVER_ERROR` | 10.0.1.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.41 (latency 75ms) |
| 2026-11-25T00:15:03 | `SERVER_ERROR` | 10.0.1.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.30 (latency 60ms) |
| 2026-11-25T00:15:12 | `SERVER_ERROR` | 10.0.3.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.49 (latency 97ms) |
| 2026-11-25T00:15:14 | `SERVER_ERROR` | 10.0.3.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.33 (latency 77ms) |
| 2026-11-25T00:15:22 | `SERVER_ERROR` | 10.0.3.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.44 (latency 58ms) |
| 2026-11-25T00:15:27 | `SERVER_ERROR` | 10.0.2.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.40 (latency 96ms) |
| 2026-11-25T00:15:38 | `SERVER_ERROR` | 10.0.2.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.47 (latency 28ms) |
| 2026-11-25T00:15:44 | `SERVER_ERROR` | 10.0.2.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.10 (latency 19ms) |
| 2026-11-25T00:15:46 | `SERVER_ERROR` | 10.0.3.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.33 (latency 41ms) |
| 2026-11-25T00:15:47 | `SERVER_ERROR` | 10.0.3.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.36 (latency 61ms) |
| 2026-11-25T00:15:48 | `SERVER_ERROR` | 10.0.3.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.4 (latency 53ms) |
| 2026-11-25T00:15:54 | `SERVER_ERROR` | 10.0.2.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.20 (latency 49ms) |
| 2026-11-25T00:16:16 | `SERVER_ERROR` | 10.0.3.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.37 (latency 50ms) |
| 2026-11-25T00:16:21 | `SERVER_ERROR` | 10.0.3.35 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.35 (latency 85ms) |
| 2026-11-25T00:16:23 | `SERVER_ERROR` | 10.0.3.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.15 (latency 89ms) |
| 2026-11-25T00:16:28 | `SERVER_ERROR` | 10.0.4.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.7 (latency 113ms) |
| 2026-11-25T00:16:29 | `SERVER_ERROR` | 10.0.3.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.10 (latency 39ms) |
| 2026-11-25T00:16:38 | `SERVER_ERROR` | 10.0.1.5 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.5 (latency 61ms) |
| 2026-11-25T00:16:49 | `SERVER_ERROR` | 10.0.2.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.21 (latency 88ms) |
| 2026-11-25T00:16:53 | `SERVER_ERROR` | 10.0.2.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.20 (latency 13ms) |
| 2026-11-25T00:16:59 | `SERVER_ERROR` | 10.0.2.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.13 (latency 98ms) |
| 2026-11-25T00:17:06 | `SERVER_ERROR` | 10.0.2.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.41 (latency 79ms) |
| 2026-11-25T00:17:16 | `SERVER_ERROR` | 10.0.4.48 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.48 (latency 44ms) |
| 2026-11-25T00:17:25 | `SERVER_ERROR` | 10.0.3.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.44 (latency 66ms) |
| 2026-11-25T00:17:27 | `SERVER_ERROR` | 10.0.4.48 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.48 (latency 119ms) |
| 2026-11-25T00:17:29 | `SERVER_ERROR` | 10.0.4.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.16 (latency 111ms) |
| 2026-11-25T00:17:30 | `SERVER_ERROR` | 10.0.4.23 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.23 (latency 18ms) |
| 2026-11-25T00:17:32 | `SERVER_ERROR` | 10.0.3.5 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.5 (latency 112ms) |
| 2026-11-25T00:17:38 | `SERVER_ERROR` | 10.0.3.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.16 (latency 32ms) |
| 2026-11-25T00:17:44 | `SERVER_ERROR` | 10.0.3.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.29 (latency 21ms) |
| 2026-11-25T00:17:46 | `SERVER_ERROR` | 10.0.1.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.29 (latency 71ms) |
| 2026-11-25T00:17:49 | `SERVER_ERROR` | 10.0.4.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.34 (latency 40ms) |
| 2026-11-25T00:17:51 | `NEW_IP` | 10.0.4.17 | 1 | New client IP detected: 10.0.4.17 |
| 2026-11-25T00:17:58 | `SERVER_ERROR` | 10.0.3.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.3 (latency 66ms) |
| 2026-11-25T00:18:03 | `SERVER_ERROR` | 10.0.3.5 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.5 (latency 36ms) |
| 2026-11-25T00:18:06 | `SERVER_ERROR` | 10.0.4.32 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.32 (latency 106ms) |
| 2026-11-25T00:18:08 | `SERVER_ERROR` | 10.0.4.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.30 (latency 117ms) |
| 2026-11-25T00:18:19 | `SERVER_ERROR` | 10.0.1.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.36 (latency 105ms) |
| 2026-11-25T00:18:30 | `SERVER_ERROR` | 10.0.2.35 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.35 (latency 57ms) |
| 2026-11-25T00:18:46 | `SERVER_ERROR` | 10.0.2.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.10 (latency 36ms) |
| 2026-11-25T00:18:55 | `SERVER_ERROR` | 10.0.2.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.10 (latency 39ms) |
| 2026-11-25T00:19:01 | `SERVER_ERROR` | 10.0.3.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.8 (latency 36ms) |
| 2026-11-25T00:19:14 | `SERVER_ERROR` | 10.0.3.5 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.5 (latency 81ms) |
| 2026-11-25T00:19:15 | `SERVER_ERROR` | 10.0.4.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.7 (latency 80ms) |
| 2026-11-25T00:19:18 | `SERVER_ERROR` | 10.0.1.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.27 (latency 99ms) |
| 2026-11-25T00:19:32 | `SERVER_ERROR` | 10.0.1.32 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.32 (latency 83ms) |
| 2026-11-25T00:19:33 | `SERVER_ERROR` | 10.0.2.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.45 (latency 39ms) |
| 2026-11-25T00:19:50 | `SERVER_ERROR` | 10.0.1.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.13 (latency 16ms) |
| 2026-11-25T00:19:53 | `SERVER_ERROR` | 10.0.4.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.44 (latency 73ms) |
| 2026-11-25T00:19:54 | `SERVER_ERROR` | 10.0.2.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.17 (latency 48ms) |
| 2026-11-25T00:20:01 | `SERVER_ERROR` | 10.0.1.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.26 (latency 110ms) |
| 2026-11-25T00:20:02 | `SERVER_ERROR` | 10.0.4.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.41 (latency 109ms) |
| 2026-11-25T00:20:04 | `SERVER_ERROR` | 10.0.2.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.42 (latency 117ms) |
| 2026-11-25T00:20:13 | `SERVER_ERROR` | 10.0.4.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.27 (latency 78ms) |
| 2026-11-25T00:20:23 | `SERVER_ERROR` | 10.0.1.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.36 (latency 120ms) |
| 2026-11-25T00:20:27 | `SERVER_ERROR` | 10.0.3.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.20 (latency 100ms) |
| 2026-11-25T00:20:28 | `SERVER_ERROR` | 10.0.4.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.34 (latency 17ms) |
| 2026-11-25T00:20:30 | `SERVER_ERROR` | 10.0.1.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.4 (latency 25ms) |
| 2026-11-25T00:20:39 | `SERVER_ERROR` | 10.0.1.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.44 (latency 58ms) |
| 2026-11-25T00:20:49 | `NEW_IP` | 10.0.4.7 | 1 | New client IP detected: 10.0.4.7 |
| 2026-11-25T00:20:49 | `SERVER_ERROR` | 10.0.4.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.7 (latency 43ms) |
| 2026-11-25T00:20:56 | `SERVER_ERROR` | 10.0.4.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.24 (latency 60ms) |
| 2026-11-25T00:21:07 | `SERVER_ERROR` | 10.0.2.35 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.35 (latency 76ms) |
| 2026-11-25T00:21:09 | `SERVER_ERROR` | 10.0.2.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.22 (latency 18ms) |
| 2026-11-25T00:21:12 | `SERVER_ERROR` | 10.0.2.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.37 (latency 45ms) |
| 2026-11-25T00:21:15 | `SERVER_ERROR` | 10.0.1.48 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.48 (latency 58ms) |
| 2026-11-25T00:21:16 | `SERVER_ERROR` | 10.0.3.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.9 (latency 100ms) |
| 2026-11-25T00:21:23 | `SERVER_ERROR` | 10.0.1.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.30 (latency 107ms) |
| 2026-11-25T00:21:29 | `NEW_IP` | 10.0.2.14 | 1 | New client IP detected: 10.0.2.14 |
| 2026-11-25T00:21:35 | `SERVER_ERROR` | 10.0.4.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.15 (latency 17ms) |
| 2026-11-25T00:21:37 | `SERVER_ERROR` | 10.0.3.5 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.5 (latency 71ms) |
| 2026-11-25T00:21:46 | `SERVER_ERROR` | 10.0.4.1 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.1 (latency 102ms) |
| 2026-11-25T00:21:48 | `SERVER_ERROR` | 10.0.2.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.37 (latency 50ms) |
| 2026-11-25T00:21:57 | `SERVER_ERROR` | 10.0.3.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.17 (latency 12ms) |
| 2026-11-25T00:21:59 | `SERVER_ERROR` | 10.0.4.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.47 (latency 59ms) |
| 2026-11-25T00:22:05 | `SERVER_ERROR` | 10.0.4.32 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.32 (latency 36ms) |
| 2026-11-25T00:22:11 | `SERVER_ERROR` | 10.0.2.46 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.46 (latency 70ms) |
| 2026-11-25T00:22:15 | `SERVER_ERROR` | 10.0.2.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.41 (latency 104ms) |
| 2026-11-25T00:22:19 | `SERVER_ERROR` | 10.0.1.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.36 (latency 83ms) |
| 2026-11-25T00:22:22 | `SERVER_ERROR` | 10.0.1.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.49 (latency 22ms) |
| 2026-11-25T00:22:26 | `SERVER_ERROR` | 10.0.1.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.36 (latency 115ms) |
| 2026-11-25T00:22:30 | `SERVER_ERROR` | 10.0.1.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.36 (latency 36ms) |
| 2026-11-25T00:22:35 | `SERVER_ERROR` | 10.0.1.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.6 (latency 40ms) |
| 2026-11-25T00:22:40 | `SERVER_ERROR` | 10.0.1.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.8 (latency 98ms) |
| 2026-11-25T00:22:43 | `SERVER_ERROR` | 10.0.2.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.49 (latency 106ms) |
| 2026-11-25T00:22:45 | `SERVER_ERROR` | 10.0.1.43 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.43 (latency 27ms) |
| 2026-11-25T00:23:00 | `SERVER_ERROR` | 10.0.1.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.42 (latency 78ms) |
| 2026-11-25T00:23:04 | `SERVER_ERROR` | 10.0.3.28 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.28 (latency 25ms) |
| 2026-11-25T00:23:06 | `SERVER_ERROR` | 10.0.2.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.45 (latency 46ms) |
| 2026-11-25T00:23:08 | `SERVER_ERROR` | 10.0.1.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.6 (latency 120ms) |
| 2026-11-25T00:23:12 | `SERVER_ERROR` | 10.0.1.5 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.5 (latency 18ms) |
| 2026-11-25T00:23:18 | `SERVER_ERROR` | 10.0.2.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.29 (latency 22ms) |
| 2026-11-25T00:23:24 | `SERVER_ERROR` | 10.0.2.43 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.43 (latency 85ms) |
| 2026-11-25T00:23:35 | `NEW_IP` | 10.0.2.15 | 1 | New client IP detected: 10.0.2.15 |
| 2026-11-25T00:23:36 | `SERVER_ERROR` | 10.0.3.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.16 (latency 70ms) |
| 2026-11-25T00:23:56 | `SERVER_ERROR` | 10.0.1.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.41 (latency 113ms) |
| 2026-11-25T00:23:58 | `SERVER_ERROR` | 10.0.1.35 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.35 (latency 39ms) |
| 2026-11-25T00:24:02 | `SERVER_ERROR` | 10.0.3.43 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.43 (latency 33ms) |
| 2026-11-25T00:24:06 | `SERVER_ERROR` | 10.0.2.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.20 (latency 50ms) |
| 2026-11-25T00:24:09 | `NEW_IP` | 10.0.2.5 | 1 | New client IP detected: 10.0.2.5 |
| 2026-11-25T00:24:14 | `SERVER_ERROR` | 10.0.3.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.27 (latency 100ms) |
| 2026-11-25T00:24:24 | `SERVER_ERROR` | 10.0.2.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.10 (latency 44ms) |
| 2026-11-25T00:24:29 | `NEW_IP` | 10.0.3.43 | 1 | New client IP detected: 10.0.3.43 |
| 2026-11-25T00:24:29 | `SERVER_ERROR` | 10.0.3.43 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.43 (latency 100ms) |
| 2026-11-25T00:24:33 | `SERVER_ERROR` | 10.0.4.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.12 (latency 42ms) |
| 2026-11-25T00:24:36 | `SERVER_ERROR` | 10.0.1.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.40 (latency 70ms) |
| 2026-11-25T00:24:42 | `SERVER_ERROR` | 10.0.2.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.24 (latency 100ms) |
| 2026-11-25T00:24:43 | `SERVER_ERROR` | 10.0.3.25 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.25 (latency 73ms) |
| 2026-11-25T00:24:50 | `SERVER_ERROR` | 10.0.2.31 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.31 (latency 12ms) |
| 2026-11-25T00:24:52 | `SERVER_ERROR` | 10.0.3.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.36 (latency 36ms) |
| 2026-11-25T00:25:00 | `SERVER_ERROR` | 10.0.2.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.6 (latency 41ms) |
| 2026-11-25T00:25:04 | `NEW_IP` | 10.0.2.10 | 1 | New client IP detected: 10.0.2.10 |
| 2026-11-25T00:25:06 | `SERVER_ERROR` | 10.0.3.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.27 (latency 71ms) |
| 2026-11-25T00:25:10 | `SERVER_ERROR` | 10.0.3.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.9 (latency 52ms) |
| 2026-11-25T00:25:14 | `NEW_IP` | 10.0.4.25 | 1 | New client IP detected: 10.0.4.25 |
| 2026-11-25T00:25:17 | `SERVER_ERROR` | 10.0.2.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.13 (latency 67ms) |
| 2026-11-25T00:25:25 | `SERVER_ERROR` | 10.0.3.14 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.14 (latency 101ms) |
| 2026-11-25T00:25:27 | `SERVER_ERROR` | 10.0.2.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.20 (latency 43ms) |
| 2026-11-25T00:25:29 | `SERVER_ERROR` | 10.0.4.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.22 (latency 101ms) |
| 2026-11-25T00:25:36 | `SERVER_ERROR` | 10.0.3.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.44 (latency 70ms) |
| 2026-11-25T00:25:38 | `NEW_IP` | 10.0.1.40 | 1 | New client IP detected: 10.0.1.40 |
| 2026-11-25T00:25:44 | `SERVER_ERROR` | 10.0.4.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.6 (latency 45ms) |
| 2026-11-25T00:25:46 | `SERVER_ERROR` | 10.0.1.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.30 (latency 89ms) |
| 2026-11-25T00:25:47 | `SERVER_ERROR` | 10.0.1.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.20 (latency 18ms) |
| 2026-11-25T00:25:49 | `SERVER_ERROR` | 10.0.2.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.26 (latency 22ms) |
| 2026-11-25T00:25:57 | `SERVER_ERROR` | 10.0.3.48 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.48 (latency 59ms) |
| 2026-11-25T00:26:00 | `NEW_IP` | 10.0.2.47 | 1 | New client IP detected: 10.0.2.47 |
| 2026-11-25T00:26:01 | `NEW_IP` | 10.0.2.32 | 1 | New client IP detected: 10.0.2.32 |
| 2026-11-25T00:26:08 | `NEW_IP` | 10.0.3.39 | 1 | New client IP detected: 10.0.3.39 |
| 2026-11-25T00:26:13 | `SERVER_ERROR` | 10.0.4.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.49 (latency 108ms) |
| 2026-11-25T00:26:22 | `SERVER_ERROR` | 10.0.4.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.30 (latency 117ms) |
| 2026-11-25T00:26:57 | `SERVER_ERROR` | 10.0.1.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.22 (latency 31ms) |
| 2026-11-25T00:27:00 | `SERVER_ERROR` | 10.0.2.38 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.38 (latency 102ms) |
| 2026-11-25T00:27:07 | `SERVER_ERROR` | 10.0.3.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.27 (latency 41ms) |
| 2026-11-25T00:27:10 | `SERVER_ERROR` | 10.0.3.11 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.11 (latency 37ms) |
| 2026-11-25T00:27:18 | `NEW_IP` | 10.0.4.5 | 1 | New client IP detected: 10.0.4.5 |
| 2026-11-25T00:27:20 | `SERVER_ERROR` | 10.0.3.46 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.46 (latency 117ms) |
| 2026-11-25T00:27:22 | `SERVER_ERROR` | 10.0.1.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.3 (latency 71ms) |
| 2026-11-25T00:27:23 | `SERVER_ERROR` | 10.0.3.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.33 (latency 101ms) |
| 2026-11-25T00:27:25 | `SERVER_ERROR` | 10.0.2.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.36 (latency 94ms) |
| 2026-11-25T00:27:30 | `NEW_IP` | 10.0.4.42 | 1 | New client IP detected: 10.0.4.42 |
| 2026-11-25T00:27:35 | `NEW_IP` | 10.0.3.41 | 1 | New client IP detected: 10.0.3.41 |
| 2026-11-25T00:27:40 | `SERVER_ERROR` | 10.0.4.11 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.11 (latency 58ms) |
| 2026-11-25T00:27:47 | `SERVER_ERROR` | 10.0.2.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.3 (latency 73ms) |
| 2026-11-25T00:27:48 | `NEW_IP` | 10.0.4.28 | 1 | New client IP detected: 10.0.4.28 |
| 2026-11-25T00:27:57 | `SERVER_ERROR` | 10.0.4.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.2 (latency 100ms) |
| 2026-11-25T00:27:59 | `SERVER_ERROR` | 10.0.3.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.41 (latency 93ms) |
| 2026-11-25T00:28:06 | `SERVER_ERROR` | 10.0.4.11 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.11 (latency 92ms) |
| 2026-11-25T00:28:07 | `SERVER_ERROR` | 10.0.1.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.33 (latency 75ms) |
| 2026-11-25T00:28:09 | `NEW_IP` | 10.0.2.37 | 1 | New client IP detected: 10.0.2.37 |
| 2026-11-25T00:28:12 | `SERVER_ERROR` | 10.0.3.14 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.14 (latency 110ms) |
| 2026-11-25T00:28:13 | `SERVER_ERROR` | 10.0.1.38 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.38 (latency 51ms) |
| 2026-11-25T00:28:22 | `SERVER_ERROR` | 10.0.3.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.6 (latency 67ms) |
| 2026-11-25T00:28:26 | `SERVER_ERROR` | 10.0.4.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.37 (latency 113ms) |
| 2026-11-25T00:28:27 | `SERVER_ERROR` | 10.0.3.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.30 (latency 120ms) |
| 2026-11-25T00:28:28 | `SERVER_ERROR` | 10.0.3.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.26 (latency 99ms) |
| 2026-11-25T00:28:31 | `SERVER_ERROR` | 10.0.2.23 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.23 (latency 118ms) |
| 2026-11-25T00:28:37 | `SERVER_ERROR` | 10.0.2.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.9 (latency 114ms) |
| 2026-11-25T00:28:42 | `SERVER_ERROR` | 10.0.3.5 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.5 (latency 59ms) |
| 2026-11-25T00:28:44 | `SERVER_ERROR` | 10.0.4.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.21 (latency 17ms) |
| 2026-11-25T00:28:45 | `SERVER_ERROR` | 10.0.4.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.15 (latency 69ms) |
| 2026-11-25T00:28:47 | `SERVER_ERROR` | 10.0.2.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.34 (latency 25ms) |
| 2026-11-25T00:28:54 | `NEW_IP` | 10.0.4.37 | 1 | New client IP detected: 10.0.4.37 |
| 2026-11-25T00:28:57 | `SERVER_ERROR` | 10.0.3.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.37 (latency 99ms) |
| 2026-11-25T00:28:58 | `SERVER_ERROR` | 10.0.3.31 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.31 (latency 35ms) |
| 2026-11-25T00:29:15 | `SERVER_ERROR` | 10.0.4.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.8 (latency 44ms) |
| 2026-11-25T00:29:23 | `NEW_IP` | 10.0.3.33 | 1 | New client IP detected: 10.0.3.33 |
| 2026-11-25T00:29:36 | `SERVER_ERROR` | 10.0.4.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.16 (latency 29ms) |
| 2026-11-25T00:29:40 | `SERVER_ERROR` | 10.0.1.48 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.48 (latency 105ms) |
| 2026-11-25T00:29:50 | `SERVER_ERROR` | 10.0.3.43 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.43 (latency 52ms) |
| 2026-11-25T00:29:59 | `SERVER_ERROR` | 10.0.2.43 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.43 (latency 13ms) |
| 2026-11-25T00:30:00 | `ERROR_SPIKE` |  | 68 | Error spike in minute 2026-11-25T00:30: 68 errors (mean 11.0) |
| 2026-11-25T00:30:00 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:00 | `SERVER_ERROR` | 10.0.2.38 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.38 (latency 15ms) |
| 2026-11-25T00:30:01 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:02 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:03 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:04 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:04 | `SERVER_ERROR` | 10.0.3.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.27 (latency 115ms) |
| 2026-11-25T00:30:05 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:06 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:07 | `SERVER_ERROR` | 10.0.4.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.16 (latency 29ms) |
| 2026-11-25T00:30:07 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:08 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:09 | `SERVER_ERROR` | 10.0.4.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.6 (latency 38ms) |
| 2026-11-25T00:30:09 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:10 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:11 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:12 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:13 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:14 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:15 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:16 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:17 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:18 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:19 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:20 | `SERVER_ERROR` | 10.0.1.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.41 (latency 67ms) |
| 2026-11-25T00:30:20 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:21 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:22 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:23 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:24 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:25 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:26 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:27 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:28 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:29 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:30 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:31 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:32 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:33 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:34 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:34 | `SERVER_ERROR` | 10.0.4.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.7 (latency 111ms) |
| 2026-11-25T00:30:35 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:36 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:37 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:38 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:39 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:40 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:41 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:42 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:43 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:44 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:45 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:46 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:47 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:48 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:49 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:49 | `SERVER_ERROR` | 10.0.1.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.40 (latency 34ms) |
| 2026-11-25T00:30:50 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:51 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:52 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:53 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:54 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:54 | `SERVER_ERROR` | 10.0.3.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.34 (latency 118ms) |
| 2026-11-25T00:30:55 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:56 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:57 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:58 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:30:59 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:00 | `ERROR_SPIKE` |  | 74 | Error spike in minute 2026-11-25T00:31: 74 errors (mean 11.0) |
| 2026-11-25T00:31:00 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:00 | `SERVER_ERROR` | 10.0.2.25 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.25 (latency 14ms) |
| 2026-11-25T00:31:01 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:02 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:03 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:04 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:05 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:06 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:07 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:08 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:09 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:10 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:10 | `SERVER_ERROR` | 10.0.4.19 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.19 (latency 54ms) |
| 2026-11-25T00:31:11 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:12 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:13 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:14 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:15 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:16 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:17 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:18 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:19 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:20 | `SERVER_ERROR` | 10.0.1.11 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.11 (latency 35ms) |
| 2026-11-25T00:31:20 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:21 | `NEW_IP` | 10.0.4.24 | 1 | New client IP detected: 10.0.4.24 |
| 2026-11-25T00:31:21 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:22 | `SERVER_ERROR` | 10.0.2.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.12 (latency 68ms) |
| 2026-11-25T00:31:22 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:23 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:23 | `SERVER_ERROR` | 10.0.2.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.24 (latency 17ms) |
| 2026-11-25T00:31:24 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:25 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:26 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:27 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:28 | `SERVER_ERROR` | 10.0.2.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.17 (latency 74ms) |
| 2026-11-25T00:31:28 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:29 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:30 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:31 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:32 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:33 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:34 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:35 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:36 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:37 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:38 | `SERVER_ERROR` | 10.0.2.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.4 (latency 23ms) |
| 2026-11-25T00:31:38 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:39 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:40 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:41 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:42 | `SERVER_ERROR` | 10.0.4.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.6 (latency 68ms) |
| 2026-11-25T00:31:42 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:43 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:44 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:45 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:46 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:46 | `SERVER_ERROR` | 10.0.1.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.40 (latency 25ms) |
| 2026-11-25T00:31:47 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:47 | `SERVER_ERROR` | 10.0.1.11 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.11 (latency 47ms) |
| 2026-11-25T00:31:48 | `SERVER_ERROR` | 10.0.3.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.20 (latency 21ms) |
| 2026-11-25T00:31:48 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:49 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:50 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:51 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:52 | `SERVER_ERROR` | 10.0.3.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.6 (latency 80ms) |
| 2026-11-25T00:31:52 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:53 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:54 | `SERVER_ERROR` | 10.0.2.25 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.25 (latency 79ms) |
| 2026-11-25T00:31:54 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:55 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:56 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:57 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:57 | `SERVER_ERROR` | 10.0.2.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.9 (latency 49ms) |
| 2026-11-25T00:31:58 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:31:59 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:00 | `ERROR_SPIKE` |  | 73 | Error spike in minute 2026-11-25T00:32: 73 errors (mean 11.0) |
| 2026-11-25T00:32:00 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:01 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:02 | `SERVER_ERROR` | 10.0.3.32 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.32 (latency 94ms) |
| 2026-11-25T00:32:02 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:03 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:04 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:05 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:05 | `SERVER_ERROR` | 10.0.2.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.13 (latency 102ms) |
| 2026-11-25T00:32:06 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:07 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:08 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:09 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:10 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:11 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:12 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:13 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:14 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:14 | `SERVER_ERROR` | 10.0.4.28 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.28 (latency 101ms) |
| 2026-11-25T00:32:15 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:16 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:17 | `SERVER_ERROR` | 10.0.3.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.15 (latency 120ms) |
| 2026-11-25T00:32:17 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:18 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:19 | `SERVER_ERROR` | 10.0.1.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.12 (latency 83ms) |
| 2026-11-25T00:32:19 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:20 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:21 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:21 | `SERVER_ERROR` | 10.0.2.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.29 (latency 74ms) |
| 2026-11-25T00:32:22 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:23 | `SERVER_ERROR` | 10.0.4.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.3 (latency 82ms) |
| 2026-11-25T00:32:23 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:24 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:25 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:25 | `SERVER_ERROR` | 10.0.3.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.41 (latency 86ms) |
| 2026-11-25T00:32:26 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:27 | `NEW_IP` | 10.0.3.24 | 1 | New client IP detected: 10.0.3.24 |
| 2026-11-25T00:32:27 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:28 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:29 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:30 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:31 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:32 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:33 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:34 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:35 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:36 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:37 | `SERVER_ERROR` | 10.0.1.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.29 (latency 72ms) |
| 2026-11-25T00:32:37 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:38 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:39 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:40 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:41 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:42 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:43 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:44 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:45 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:46 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:47 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:47 | `SERVER_ERROR` | 10.0.1.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.6 (latency 57ms) |
| 2026-11-25T00:32:48 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:49 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:50 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:51 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:51 | `SERVER_ERROR` | 10.0.4.46 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.46 (latency 103ms) |
| 2026-11-25T00:32:52 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:52 | `SERVER_ERROR` | 10.0.2.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.10 (latency 60ms) |
| 2026-11-25T00:32:53 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:54 | `SERVER_ERROR` | 10.0.4.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.29 (latency 51ms) |
| 2026-11-25T00:32:54 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:55 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:56 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:57 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:58 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:32:59 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:33:00 | `NEW_IP` | 192.168.1.99 | 1 | New client IP detected: 192.168.1.99 |
| 2026-11-25T00:33:00 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:33:01 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:33:02 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:33:03 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:33:04 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:33:05 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:33:06 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:33:07 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:33:08 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:33:09 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:33:10 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:33:11 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:33:12 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:33:13 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:33:14 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:33:15 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:33:16 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:33:17 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:33:18 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:33:19 | `SERVER_ERROR` | 192.168.1.99 | 500 | HTTP 500 on GET /api/x from IP 192.168.1.99 (latency 50ms) |
| 2026-11-25T00:33:23 | `NEW_IP` | 10.0.2.21 | 1 | New client IP detected: 10.0.2.21 |
| 2026-11-25T00:33:24 | `SERVER_ERROR` | 10.0.1.35 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.35 (latency 62ms) |
| 2026-11-25T00:33:27 | `SERVER_ERROR` | 10.0.2.38 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.38 (latency 120ms) |
| 2026-11-25T00:33:43 | `NEW_IP` | 10.0.1.20 | 1 | New client IP detected: 10.0.1.20 |
| 2026-11-25T00:33:43 | `SERVER_ERROR` | 10.0.1.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.20 (latency 112ms) |
| 2026-11-25T00:33:47 | `SERVER_ERROR` | 10.0.3.43 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.43 (latency 81ms) |
| 2026-11-25T00:33:48 | `SERVER_ERROR` | 10.0.3.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.26 (latency 82ms) |
| 2026-11-25T00:33:52 | `SERVER_ERROR` | 10.0.1.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.16 (latency 105ms) |
| 2026-11-25T00:33:56 | `SERVER_ERROR` | 10.0.2.35 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.35 (latency 32ms) |
| 2026-11-25T00:34:00 | `NEW_IP` | 10.0.2.22 | 1 | New client IP detected: 10.0.2.22 |
| 2026-11-25T00:34:06 | `SERVER_ERROR` | 10.0.1.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.30 (latency 63ms) |
| 2026-11-25T00:34:13 | `SERVER_ERROR` | 10.0.2.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.6 (latency 83ms) |
| 2026-11-25T00:34:15 | `SERVER_ERROR` | 10.0.3.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.37 (latency 51ms) |
| 2026-11-25T00:34:20 | `SERVER_ERROR` | 10.0.3.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.8 (latency 89ms) |
| 2026-11-25T00:34:52 | `SERVER_ERROR` | 10.0.2.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.40 (latency 71ms) |
| 2026-11-25T00:34:55 | `SERVER_ERROR` | 10.0.3.46 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.46 (latency 17ms) |
| 2026-11-25T00:34:56 | `SERVER_ERROR` | 10.0.2.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.2 (latency 31ms) |
| 2026-11-25T00:34:57 | `SERVER_ERROR` | 10.0.3.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.16 (latency 58ms) |
| 2026-11-25T00:34:58 | `SERVER_ERROR` | 10.0.2.48 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.48 (latency 101ms) |
| 2026-11-25T00:35:25 | `SERVER_ERROR` | 10.0.1.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.6 (latency 61ms) |
| 2026-11-25T00:35:27 | `SERVER_ERROR` | 10.0.1.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.27 (latency 67ms) |
| 2026-11-25T00:35:42 | `SERVER_ERROR` | 10.0.3.25 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.25 (latency 25ms) |
| 2026-11-25T00:35:43 | `SERVER_ERROR` | 10.0.1.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.26 (latency 29ms) |
| 2026-11-25T00:35:48 | `SERVER_ERROR` | 10.0.1.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.27 (latency 112ms) |
| 2026-11-25T00:35:51 | `NEW_IP` | 10.0.1.30 | 1 | New client IP detected: 10.0.1.30 |
| 2026-11-25T00:35:52 | `SERVER_ERROR` | 10.0.2.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.45 (latency 103ms) |
| 2026-11-25T00:35:53 | `SERVER_ERROR` | 10.0.1.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.6 (latency 38ms) |
| 2026-11-25T00:35:55 | `SERVER_ERROR` | 10.0.3.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.37 (latency 97ms) |
| 2026-11-25T00:36:01 | `SERVER_ERROR` | 10.0.2.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.16 (latency 85ms) |
| 2026-11-25T00:36:03 | `SERVER_ERROR` | 10.0.3.32 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.32 (latency 67ms) |
| 2026-11-25T00:36:08 | `NEW_IP` | 10.0.3.29 | 1 | New client IP detected: 10.0.3.29 |
| 2026-11-25T00:36:09 | `SERVER_ERROR` | 10.0.1.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.3 (latency 18ms) |
| 2026-11-25T00:36:15 | `SERVER_ERROR` | 10.0.3.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.3 (latency 61ms) |
| 2026-11-25T00:36:25 | `SERVER_ERROR` | 10.0.1.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.29 (latency 65ms) |
| 2026-11-25T00:36:31 | `SERVER_ERROR` | 10.0.4.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.41 (latency 50ms) |
| 2026-11-25T00:36:32 | `NEW_IP` | 10.0.4.14 | 1 | New client IP detected: 10.0.4.14 |
| 2026-11-25T00:36:40 | `SERVER_ERROR` | 10.0.3.23 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.23 (latency 34ms) |
| 2026-11-25T00:36:44 | `SERVER_ERROR` | 10.0.4.18 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.18 (latency 68ms) |
| 2026-11-25T00:36:45 | `SERVER_ERROR` | 10.0.3.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.49 (latency 96ms) |
| 2026-11-25T00:36:46 | `SERVER_ERROR` | 10.0.3.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.17 (latency 103ms) |
| 2026-11-25T00:36:49 | `SERVER_ERROR` | 10.0.3.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.2 (latency 116ms) |
| 2026-11-25T00:36:59 | `SERVER_ERROR` | 10.0.3.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.39 (latency 22ms) |
| 2026-11-25T00:37:02 | `SERVER_ERROR` | 10.0.2.35 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.35 (latency 116ms) |
| 2026-11-25T00:37:04 | `SERVER_ERROR` | 10.0.1.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.13 (latency 90ms) |
| 2026-11-25T00:37:06 | `SERVER_ERROR` | 10.0.2.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.3 (latency 53ms) |
| 2026-11-25T00:37:14 | `NEW_IP` | 10.0.4.32 | 1 | New client IP detected: 10.0.4.32 |
| 2026-11-25T00:37:18 | `SERVER_ERROR` | 10.0.3.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.24 (latency 20ms) |
| 2026-11-25T00:37:25 | `SERVER_ERROR` | 10.0.4.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.13 (latency 18ms) |
| 2026-11-25T00:37:26 | `SERVER_ERROR` | 10.0.1.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.34 (latency 118ms) |
| 2026-11-25T00:37:36 | `SERVER_ERROR` | 10.0.1.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.26 (latency 27ms) |
| 2026-11-25T00:37:40 | `SERVER_ERROR` | 10.0.1.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.30 (latency 56ms) |
| 2026-11-25T00:37:46 | `SERVER_ERROR` | 10.0.4.31 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.31 (latency 99ms) |
| 2026-11-25T00:37:51 | `SERVER_ERROR` | 10.0.3.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.8 (latency 36ms) |
| 2026-11-25T00:37:54 | `SERVER_ERROR` | 10.0.2.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.44 (latency 16ms) |
| 2026-11-25T00:37:55 | `NEW_IP` | 10.0.3.38 | 1 | New client IP detected: 10.0.3.38 |
| 2026-11-25T00:37:57 | `SERVER_ERROR` | 10.0.3.28 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.28 (latency 63ms) |
| 2026-11-25T00:37:58 | `NEW_IP` | 10.0.1.28 | 1 | New client IP detected: 10.0.1.28 |
| 2026-11-25T00:38:05 | `NEW_IP` | 10.0.2.4 | 1 | New client IP detected: 10.0.2.4 |
| 2026-11-25T00:38:05 | `SERVER_ERROR` | 10.0.2.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.4 (latency 46ms) |
| 2026-11-25T00:38:11 | `NEW_IP` | 10.0.4.10 | 1 | New client IP detected: 10.0.4.10 |
| 2026-11-25T00:38:12 | `SERVER_ERROR` | 10.0.2.5 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.5 (latency 113ms) |
| 2026-11-25T00:38:14 | `NEW_IP` | 10.0.2.7 | 1 | New client IP detected: 10.0.2.7 |
| 2026-11-25T00:38:14 | `SERVER_ERROR` | 10.0.2.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.7 (latency 85ms) |
| 2026-11-25T00:38:16 | `NEW_IP` | 10.0.1.38 | 1 | New client IP detected: 10.0.1.38 |
| 2026-11-25T00:38:19 | `SERVER_ERROR` | 10.0.2.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.47 (latency 76ms) |
| 2026-11-25T00:38:26 | `SERVER_ERROR` | 10.0.3.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.29 (latency 29ms) |
| 2026-11-25T00:38:27 | `SERVER_ERROR` | 10.0.3.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.17 (latency 66ms) |
| 2026-11-25T00:38:39 | `SERVER_ERROR` | 10.0.1.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.44 (latency 105ms) |
| 2026-11-25T00:38:44 | `SERVER_ERROR` | 10.0.3.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.44 (latency 110ms) |
| 2026-11-25T00:38:45 | `SERVER_ERROR` | 10.0.1.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.45 (latency 82ms) |
| 2026-11-25T00:38:58 | `SERVER_ERROR` | 10.0.2.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.41 (latency 76ms) |
| 2026-11-25T00:39:07 | `SERVER_ERROR` | 10.0.2.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.27 (latency 29ms) |
| 2026-11-25T00:39:18 | `SERVER_ERROR` | 10.0.1.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.12 (latency 111ms) |
| 2026-11-25T00:39:25 | `SERVER_ERROR` | 10.0.3.46 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.46 (latency 77ms) |
| 2026-11-25T00:39:28 | `SERVER_ERROR` | 10.0.1.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.20 (latency 20ms) |
| 2026-11-25T00:39:36 | `NEW_IP` | 10.0.2.25 | 1 | New client IP detected: 10.0.2.25 |
| 2026-11-25T00:39:52 | `SERVER_ERROR` | 10.0.3.32 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.32 (latency 37ms) |
| 2026-11-25T00:40:00 | `SERVER_ERROR` | 10.0.3.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.49 (latency 83ms) |
| 2026-11-25T00:40:21 | `SERVER_ERROR` | 10.0.1.35 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.35 (latency 42ms) |
| 2026-11-25T00:40:44 | `SERVER_ERROR` | 10.0.1.5 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.5 (latency 40ms) |
| 2026-11-25T00:40:56 | `SERVER_ERROR` | 10.0.4.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.41 (latency 69ms) |
| 2026-11-25T00:40:59 | `SERVER_ERROR` | 10.0.1.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.34 (latency 26ms) |
| 2026-11-25T00:41:04 | `SERVER_ERROR` | 10.0.1.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.3 (latency 48ms) |
| 2026-11-25T00:41:05 | `SERVER_ERROR` | 10.0.1.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.40 (latency 113ms) |
| 2026-11-25T00:41:07 | `NEW_IP` | 10.0.4.48 | 1 | New client IP detected: 10.0.4.48 |
| 2026-11-25T00:41:08 | `SERVER_ERROR` | 10.0.1.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.41 (latency 89ms) |
| 2026-11-25T00:41:10 | `SERVER_ERROR` | 10.0.2.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.44 (latency 90ms) |
| 2026-11-25T00:41:15 | `SERVER_ERROR` | 10.0.4.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.8 (latency 71ms) |
| 2026-11-25T00:41:20 | `NEW_IP` | 10.0.4.45 | 1 | New client IP detected: 10.0.4.45 |
| 2026-11-25T00:41:21 | `SERVER_ERROR` | 10.0.2.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.34 (latency 91ms) |
| 2026-11-25T00:41:26 | `SERVER_ERROR` | 10.0.4.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.13 (latency 48ms) |
| 2026-11-25T00:41:38 | `SERVER_ERROR` | 10.0.3.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.10 (latency 120ms) |
| 2026-11-25T00:41:48 | `SERVER_ERROR` | 10.0.1.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.17 (latency 41ms) |
| 2026-11-25T00:42:07 | `SERVER_ERROR` | 10.0.3.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.10 (latency 94ms) |
| 2026-11-25T00:42:08 | `SERVER_ERROR` | 10.0.2.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.34 (latency 106ms) |
| 2026-11-25T00:42:12 | `SERVER_ERROR` | 10.0.3.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.42 (latency 21ms) |
| 2026-11-25T00:42:14 | `SERVER_ERROR` | 10.0.1.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.2 (latency 22ms) |
| 2026-11-25T00:42:24 | `SERVER_ERROR` | 10.0.3.46 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.46 (latency 120ms) |
| 2026-11-25T00:42:40 | `SERVER_ERROR` | 10.0.2.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.22 (latency 14ms) |
| 2026-11-25T00:42:51 | `NEW_IP` | 10.0.2.31 | 1 | New client IP detected: 10.0.2.31 |
| 2026-11-25T00:42:57 | `SERVER_ERROR` | 10.0.3.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.47 (latency 102ms) |
| 2026-11-25T00:43:00 | `SERVER_ERROR` | 10.0.1.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.17 (latency 31ms) |
| 2026-11-25T00:43:03 | `SERVER_ERROR` | 10.0.2.14 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.14 (latency 110ms) |
| 2026-11-25T00:43:07 | `NEW_IP` | 10.0.2.17 | 1 | New client IP detected: 10.0.2.17 |
| 2026-11-25T00:43:07 | `SERVER_ERROR` | 10.0.2.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.17 (latency 24ms) |
| 2026-11-25T00:43:14 | `SERVER_ERROR` | 10.0.2.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.15 (latency 23ms) |
| 2026-11-25T00:43:17 | `NEW_IP` | 10.0.4.34 | 1 | New client IP detected: 10.0.4.34 |
| 2026-11-25T00:43:34 | `SERVER_ERROR` | 10.0.1.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.6 (latency 23ms) |
| 2026-11-25T00:43:35 | `SERVER_ERROR` | 10.0.3.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.17 (latency 111ms) |
| 2026-11-25T00:43:39 | `SERVER_ERROR` | 10.0.1.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.24 (latency 65ms) |
| 2026-11-25T00:43:51 | `SERVER_ERROR` | 10.0.1.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.2 (latency 48ms) |
| 2026-11-25T00:43:54 | `SERVER_ERROR` | 10.0.2.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.6 (latency 68ms) |
| 2026-11-25T00:44:08 | `SERVER_ERROR` | 10.0.3.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.8 (latency 21ms) |
| 2026-11-25T00:44:09 | `SERVER_ERROR` | 10.0.2.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.13 (latency 117ms) |
| 2026-11-25T00:44:11 | `SERVER_ERROR` | 10.0.4.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.22 (latency 28ms) |
| 2026-11-25T00:44:12 | `SERVER_ERROR` | 10.0.2.38 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.38 (latency 55ms) |
| 2026-11-25T00:44:23 | `SERVER_ERROR` | 10.0.4.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.20 (latency 79ms) |
| 2026-11-25T00:44:25 | `SERVER_ERROR` | 10.0.4.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.24 (latency 58ms) |
| 2026-11-25T00:44:27 | `SERVER_ERROR` | 10.0.1.18 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.18 (latency 49ms) |
| 2026-11-25T00:44:30 | `SERVER_ERROR` | 10.0.4.31 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.31 (latency 36ms) |
| 2026-11-25T00:44:31 | `SERVER_ERROR` | 10.0.2.5 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.5 (latency 70ms) |
| 2026-11-25T00:44:39 | `NEW_IP` | 10.0.1.42 | 1 | New client IP detected: 10.0.1.42 |
| 2026-11-25T00:44:46 | `SERVER_ERROR` | 10.0.1.32 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.32 (latency 43ms) |
| 2026-11-25T00:44:48 | `SERVER_ERROR` | 10.0.1.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.40 (latency 53ms) |
| 2026-11-25T00:44:53 | `SERVER_ERROR` | 10.0.3.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.4 (latency 118ms) |
| 2026-11-25T00:44:54 | `SERVER_ERROR` | 10.0.2.5 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.5 (latency 98ms) |
| 2026-11-25T00:45:00 | `SERVER_ERROR` | 10.0.2.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.37 (latency 36ms) |
| 2026-11-25T00:45:03 | `SERVER_ERROR` | 10.0.2.23 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.23 (latency 34ms) |
| 2026-11-25T00:45:04 | `SERVER_ERROR` | 10.0.4.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.41 (latency 81ms) |
| 2026-11-25T00:45:18 | `SERVER_ERROR` | 10.0.4.28 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.28 (latency 63ms) |
| 2026-11-25T00:45:25 | `SERVER_ERROR` | 10.0.1.18 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.18 (latency 72ms) |
| 2026-11-25T00:45:26 | `SERVER_ERROR` | 10.0.4.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.41 (latency 52ms) |
| 2026-11-25T00:45:41 | `SERVER_ERROR` | 10.0.2.5 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.5 (latency 75ms) |
| 2026-11-25T00:45:49 | `SERVER_ERROR` | 10.0.3.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.37 (latency 45ms) |
| 2026-11-25T00:45:58 | `SERVER_ERROR` | 10.0.3.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.26 (latency 81ms) |
| 2026-11-25T00:45:59 | `SERVER_ERROR` | 10.0.1.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.27 (latency 74ms) |
| 2026-11-25T00:46:00 | `SERVER_ERROR` | 10.0.1.25 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.25 (latency 84ms) |
| 2026-11-25T00:46:06 | `SERVER_ERROR` | 10.0.1.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.36 (latency 65ms) |
| 2026-11-25T00:46:09 | `NEW_IP` | 10.0.4.6 | 1 | New client IP detected: 10.0.4.6 |
| 2026-11-25T00:46:27 | `NEW_IP` | 203.0.113.7 | 1 | New client IP detected: 203.0.113.7 |
| 2026-11-25T00:46:28 | `SERVER_ERROR` | 10.0.2.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.45 (latency 24ms) |
| 2026-11-25T00:46:32 | `SERVER_ERROR` | 10.0.2.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.24 (latency 69ms) |
| 2026-11-25T00:46:38 | `SERVER_ERROR` | 10.0.4.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.24 (latency 105ms) |
| 2026-11-25T00:46:43 | `SERVER_ERROR` | 10.0.2.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.3 (latency 44ms) |
| 2026-11-25T00:46:44 | `SERVER_ERROR` | 10.0.3.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.12 (latency 49ms) |
| 2026-11-25T00:46:46 | `SERVER_ERROR` | 10.0.1.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.8 (latency 76ms) |
| 2026-11-25T00:47:01 | `SERVER_ERROR` | 10.0.3.1 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.1 (latency 25ms) |
| 2026-11-25T00:47:06 | `SERVER_ERROR` | 10.0.2.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.37 (latency 77ms) |
| 2026-11-25T00:47:08 | `SERVER_ERROR` | 10.0.1.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.15 (latency 35ms) |
| 2026-11-25T00:47:15 | `NEW_IP` | 10.0.1.10 | 1 | New client IP detected: 10.0.1.10 |
| 2026-11-25T00:47:15 | `SERVER_ERROR` | 10.0.1.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.10 (latency 114ms) |
| 2026-11-25T00:47:22 | `NEW_IP` | 10.0.1.47 | 1 | New client IP detected: 10.0.1.47 |
| 2026-11-25T00:47:22 | `SERVER_ERROR` | 10.0.1.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.47 (latency 117ms) |
| 2026-11-25T00:47:33 | `SERVER_ERROR` | 10.0.2.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.22 (latency 45ms) |
| 2026-11-25T00:47:34 | `SERVER_ERROR` | 10.0.1.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.33 (latency 83ms) |
| 2026-11-25T00:47:43 | `SERVER_ERROR` | 10.0.1.1 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.1 (latency 43ms) |
| 2026-11-25T00:47:45 | `SERVER_ERROR` | 10.0.2.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.36 (latency 96ms) |
| 2026-11-25T00:47:46 | `SERVER_ERROR` | 10.0.2.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.49 (latency 101ms) |
| 2026-11-25T00:47:54 | `SERVER_ERROR` | 10.0.2.18 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.18 (latency 26ms) |
| 2026-11-25T00:47:55 | `SERVER_ERROR` | 10.0.3.48 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.48 (latency 111ms) |
| 2026-11-25T00:47:59 | `SERVER_ERROR` | 10.0.4.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.21 (latency 107ms) |
| 2026-11-25T00:48:00 | `SERVER_ERROR` | 10.0.1.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.12 (latency 102ms) |
| 2026-11-25T00:48:05 | `NEW_IP` | 10.0.4.19 | 1 | New client IP detected: 10.0.4.19 |
| 2026-11-25T00:48:15 | `SERVER_ERROR` | 10.0.4.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.16 (latency 88ms) |
| 2026-11-25T00:48:18 | `SERVER_ERROR` | 10.0.2.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.9 (latency 15ms) |
| 2026-11-25T00:48:19 | `SERVER_ERROR` | 10.0.1.28 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.28 (latency 111ms) |
| 2026-11-25T00:48:20 | `SERVER_ERROR` | 10.0.2.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.49 (latency 47ms) |
| 2026-11-25T00:48:22 | `SERVER_ERROR` | 10.0.2.25 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.25 (latency 93ms) |
| 2026-11-25T00:48:33 | `SERVER_ERROR` | 10.0.4.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.16 (latency 49ms) |
| 2026-11-25T00:48:34 | `SERVER_ERROR` | 10.0.3.35 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.35 (latency 74ms) |
| 2026-11-25T00:48:35 | `SERVER_ERROR` | 10.0.3.11 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.11 (latency 47ms) |
| 2026-11-25T00:48:39 | `SERVER_ERROR` | 10.0.4.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.49 (latency 63ms) |
| 2026-11-25T00:48:46 | `SERVER_ERROR` | 10.0.2.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.49 (latency 106ms) |
| 2026-11-25T00:48:52 | `SERVER_ERROR` | 10.0.1.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.15 (latency 110ms) |
| 2026-11-25T00:49:00 | `SERVER_ERROR` | 10.0.3.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.22 (latency 15ms) |
| 2026-11-25T00:49:02 | `SERVER_ERROR` | 10.0.2.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.33 (latency 107ms) |
| 2026-11-25T00:49:04 | `SERVER_ERROR` | 10.0.2.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.45 (latency 24ms) |
| 2026-11-25T00:49:05 | `SERVER_ERROR` | 10.0.2.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.9 (latency 109ms) |
| 2026-11-25T00:49:12 | `SERVER_ERROR` | 10.0.4.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.42 (latency 76ms) |
| 2026-11-25T00:49:22 | `SERVER_ERROR` | 10.0.4.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.20 (latency 28ms) |
| 2026-11-25T00:49:27 | `SERVER_ERROR` | 10.0.1.1 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.1 (latency 50ms) |
| 2026-11-25T00:49:32 | `SERVER_ERROR` | 10.0.4.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.10 (latency 54ms) |
| 2026-11-25T00:49:38 | `SERVER_ERROR` | 10.0.1.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.13 (latency 34ms) |
| 2026-11-25T00:49:44 | `SERVER_ERROR` | 10.0.3.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.17 (latency 13ms) |
| 2026-11-25T00:49:45 | `SERVER_ERROR` | 10.0.4.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.17 (latency 65ms) |
| 2026-11-25T00:49:49 | `SERVER_ERROR` | 10.0.3.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.26 (latency 11ms) |
| 2026-11-25T00:49:50 | `SERVER_ERROR` | 10.0.4.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.4 (latency 103ms) |
| 2026-11-25T00:49:53 | `SERVER_ERROR` | 10.0.3.23 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.23 (latency 25ms) |
| 2026-11-25T00:50:01 | `NEW_IP` | 10.0.3.49 | 1 | New client IP detected: 10.0.3.49 |
| 2026-11-25T00:50:01 | `SERVER_ERROR` | 10.0.3.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.49 (latency 66ms) |
| 2026-11-25T00:50:05 | `SERVER_ERROR` | 10.0.4.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.37 (latency 116ms) |
| 2026-11-25T00:50:15 | `SERVER_ERROR` | 10.0.2.25 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.25 (latency 27ms) |
| 2026-11-25T00:50:19 | `SERVER_ERROR` | 10.0.1.35 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.35 (latency 112ms) |
| 2026-11-25T00:50:25 | `SERVER_ERROR` | 10.0.2.1 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.1 (latency 72ms) |
| 2026-11-25T00:50:26 | `SERVER_ERROR` | 10.0.1.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.30 (latency 86ms) |
| 2026-11-25T00:50:37 | `SERVER_ERROR` | 10.0.2.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.27 (latency 118ms) |
| 2026-11-25T00:50:45 | `SERVER_ERROR` | 10.0.2.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.40 (latency 32ms) |
| 2026-11-25T00:50:50 | `SERVER_ERROR` | 10.0.1.43 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.43 (latency 75ms) |
| 2026-11-25T00:50:52 | `NEW_IP` | 10.0.3.15 | 1 | New client IP detected: 10.0.3.15 |
| 2026-11-25T00:51:01 | `SERVER_ERROR` | 10.0.1.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.47 (latency 51ms) |
| 2026-11-25T00:51:05 | `SERVER_ERROR` | 10.0.1.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.4 (latency 81ms) |
| 2026-11-25T00:51:14 | `SERVER_ERROR` | 10.0.4.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.45 (latency 60ms) |
| 2026-11-25T00:51:31 | `SERVER_ERROR` | 10.0.3.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.40 (latency 20ms) |
| 2026-11-25T00:51:32 | `SERVER_ERROR` | 10.0.4.43 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.43 (latency 71ms) |
| 2026-11-25T00:51:44 | `SERVER_ERROR` | 10.0.3.38 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.38 (latency 77ms) |
| 2026-11-25T00:51:48 | `SERVER_ERROR` | 10.0.3.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.30 (latency 100ms) |
| 2026-11-25T00:51:49 | `SERVER_ERROR` | 10.0.1.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.27 (latency 92ms) |
| 2026-11-25T00:51:54 | `SERVER_ERROR` | 10.0.1.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.7 (latency 48ms) |
| 2026-11-25T00:52:02 | `SERVER_ERROR` | 10.0.3.28 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.28 (latency 112ms) |
| 2026-11-25T00:52:09 | `SERVER_ERROR` | 10.0.1.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.44 (latency 53ms) |
| 2026-11-25T00:52:13 | `SERVER_ERROR` | 10.0.4.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.44 (latency 104ms) |
| 2026-11-25T00:52:15 | `SERVER_ERROR` | 10.0.2.25 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.25 (latency 96ms) |
| 2026-11-25T00:52:16 | `SERVER_ERROR` | 10.0.4.1 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.1 (latency 105ms) |
| 2026-11-25T00:52:20 | `SERVER_ERROR` | 10.0.2.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.24 (latency 61ms) |
| 2026-11-25T00:52:40 | `SERVER_ERROR` | 10.0.4.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.47 (latency 94ms) |
| 2026-11-25T00:52:43 | `SERVER_ERROR` | 10.0.1.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.21 (latency 43ms) |
| 2026-11-25T00:52:46 | `SERVER_ERROR` | 10.0.1.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.36 (latency 84ms) |
| 2026-11-25T00:52:56 | `SERVER_ERROR` | 10.0.3.5 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.5 (latency 50ms) |
| 2026-11-25T00:53:00 | `SERVER_ERROR` | 10.0.1.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.21 (latency 52ms) |
| 2026-11-25T00:53:11 | `SERVER_ERROR` | 10.0.2.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.16 (latency 91ms) |
| 2026-11-25T00:53:18 | `SERVER_ERROR` | 10.0.1.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.13 (latency 91ms) |
| 2026-11-25T00:53:23 | `NEW_IP` | 10.0.1.8 | 1 | New client IP detected: 10.0.1.8 |
| 2026-11-25T00:53:26 | `SERVER_ERROR` | 10.0.1.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.29 (latency 23ms) |
| 2026-11-25T00:53:38 | `SERVER_ERROR` | 10.0.2.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.8 (latency 75ms) |
| 2026-11-25T00:53:40 | `SERVER_ERROR` | 10.0.2.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.42 (latency 71ms) |
| 2026-11-25T00:53:41 | `SERVER_ERROR` | 10.0.2.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.39 (latency 80ms) |
| 2026-11-25T00:53:48 | `NEW_IP` | 10.0.1.48 | 1 | New client IP detected: 10.0.1.48 |
| 2026-11-25T00:53:51 | `SERVER_ERROR` | 10.0.3.5 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.5 (latency 110ms) |
| 2026-11-25T00:54:04 | `SERVER_ERROR` | 10.0.1.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.42 (latency 112ms) |
| 2026-11-25T00:54:19 | `SERVER_ERROR` | 10.0.3.31 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.31 (latency 115ms) |
| 2026-11-25T00:54:20 | `SERVER_ERROR` | 10.0.4.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.45 (latency 20ms) |
| 2026-11-25T00:54:21 | `SERVER_ERROR` | 10.0.3.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.27 (latency 26ms) |
| 2026-11-25T00:54:24 | `SERVER_ERROR` | 10.0.1.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.22 (latency 15ms) |
| 2026-11-25T00:54:25 | `SERVER_ERROR` | 10.0.2.28 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.28 (latency 23ms) |
| 2026-11-25T00:54:27 | `SERVER_ERROR` | 10.0.2.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.13 (latency 76ms) |
| 2026-11-25T00:54:38 | `SERVER_ERROR` | 10.0.2.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.21 (latency 82ms) |
| 2026-11-25T00:54:45 | `SERVER_ERROR` | 10.0.3.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.22 (latency 22ms) |
| 2026-11-25T00:54:48 | `SERVER_ERROR` | 10.0.1.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.24 (latency 85ms) |
| 2026-11-25T00:54:54 | `SERVER_ERROR` | 10.0.2.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.47 (latency 29ms) |
| 2026-11-25T00:54:56 | `SERVER_ERROR` | 10.0.1.48 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.48 (latency 110ms) |
| 2026-11-25T00:55:02 | `SERVER_ERROR` | 10.0.4.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.26 (latency 112ms) |
| 2026-11-25T00:55:21 | `SERVER_ERROR` | 10.0.2.19 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.19 (latency 55ms) |
| 2026-11-25T00:55:22 | `SERVER_ERROR` | 10.0.4.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.33 (latency 40ms) |
| 2026-11-25T00:55:23 | `SERVER_ERROR` | 10.0.4.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.17 (latency 100ms) |
| 2026-11-25T00:55:31 | `SERVER_ERROR` | 10.0.1.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.39 (latency 106ms) |
| 2026-11-25T00:55:34 | `SERVER_ERROR` | 10.0.3.43 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.43 (latency 103ms) |
| 2026-11-25T00:55:36 | `SERVER_ERROR` | 10.0.3.31 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.31 (latency 19ms) |
| 2026-11-25T00:55:38 | `SERVER_ERROR` | 10.0.3.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.34 (latency 61ms) |
| 2026-11-25T00:55:54 | `SERVER_ERROR` | 10.0.4.25 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.25 (latency 109ms) |
| 2026-11-25T00:55:58 | `SERVER_ERROR` | 10.0.1.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.3 (latency 26ms) |
| 2026-11-25T00:56:01 | `SERVER_ERROR` | 10.0.3.23 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.23 (latency 80ms) |
| 2026-11-25T00:56:03 | `SERVER_ERROR` | 10.0.2.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.40 (latency 66ms) |
| 2026-11-25T00:56:05 | `SERVER_ERROR` | 10.0.3.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.34 (latency 57ms) |
| 2026-11-25T00:56:13 | `SERVER_ERROR` | 10.0.2.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.34 (latency 51ms) |
| 2026-11-25T00:56:14 | `SERVER_ERROR` | 10.0.3.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.33 (latency 25ms) |
| 2026-11-25T00:56:16 | `SERVER_ERROR` | 10.0.4.43 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.43 (latency 65ms) |
| 2026-11-25T00:56:18 | `SERVER_ERROR` | 10.0.3.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.39 (latency 69ms) |
| 2026-11-25T00:56:24 | `SERVER_ERROR` | 10.0.4.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.30 (latency 66ms) |
| 2026-11-25T00:56:28 | `SERVER_ERROR` | 10.0.2.48 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.48 (latency 48ms) |
| 2026-11-25T00:56:31 | `SERVER_ERROR` | 10.0.2.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.2 (latency 113ms) |
| 2026-11-25T00:56:32 | `SERVER_ERROR` | 10.0.3.18 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.18 (latency 70ms) |
| 2026-11-25T00:56:34 | `SERVER_ERROR` | 10.0.1.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.30 (latency 87ms) |
| 2026-11-25T00:56:38 | `SERVER_ERROR` | 10.0.1.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.30 (latency 13ms) |
| 2026-11-25T00:56:43 | `SERVER_ERROR` | 10.0.3.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.47 (latency 24ms) |
| 2026-11-25T00:56:45 | `SERVER_ERROR` | 10.0.4.11 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.11 (latency 22ms) |
| 2026-11-25T00:56:47 | `SERVER_ERROR` | 10.0.4.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.7 (latency 114ms) |
| 2026-11-25T00:56:51 | `SERVER_ERROR` | 10.0.1.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.13 (latency 102ms) |
| 2026-11-25T00:56:53 | `SERVER_ERROR` | 10.0.1.38 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.38 (latency 20ms) |
| 2026-11-25T00:56:57 | `SERVER_ERROR` | 10.0.4.46 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.46 (latency 106ms) |
| 2026-11-25T00:56:59 | `SERVER_ERROR` | 10.0.1.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.9 (latency 48ms) |
| 2026-11-25T00:57:04 | `SERVER_ERROR` | 10.0.2.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.20 (latency 45ms) |
| 2026-11-25T00:57:08 | `SERVER_ERROR` | 10.0.4.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.34 (latency 80ms) |
| 2026-11-25T00:57:17 | `SERVER_ERROR` | 10.0.1.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.42 (latency 52ms) |
| 2026-11-25T00:57:23 | `SERVER_ERROR` | 10.0.4.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.13 (latency 12ms) |
| 2026-11-25T00:57:44 | `SERVER_ERROR` | 10.0.2.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.33 (latency 71ms) |
| 2026-11-25T00:57:45 | `SERVER_ERROR` | 10.0.2.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.15 (latency 36ms) |
| 2026-11-25T00:57:46 | `SERVER_ERROR` | 10.0.4.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.7 (latency 107ms) |
| 2026-11-25T00:58:01 | `SERVER_ERROR` | 10.0.3.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.15 (latency 13ms) |
| 2026-11-25T00:58:04 | `SERVER_ERROR` | 10.0.2.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.12 (latency 112ms) |
| 2026-11-25T00:58:07 | `SERVER_ERROR` | 10.0.2.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.21 (latency 68ms) |
| 2026-11-25T00:58:14 | `SERVER_ERROR` | 10.0.4.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.27 (latency 65ms) |
| 2026-11-25T00:58:36 | `SERVER_ERROR` | 10.0.3.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.24 (latency 12ms) |
| 2026-11-25T00:58:49 | `SERVER_ERROR` | 10.0.4.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.45 (latency 11ms) |
| 2026-11-25T00:59:08 | `SERVER_ERROR` | 10.0.3.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.49 (latency 48ms) |
| 2026-11-25T00:59:14 | `NEW_IP` | 10.0.2.36 | 1 | New client IP detected: 10.0.2.36 |
| 2026-11-25T00:59:41 | `SERVER_ERROR` | 10.0.3.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.9 (latency 59ms) |
| 2026-11-25T00:59:44 | `NEW_IP` | 10.0.4.4 | 1 | New client IP detected: 10.0.4.4 |
| 2026-11-25T00:59:45 | `SERVER_ERROR` | 10.0.4.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.21 (latency 99ms) |
| 2026-11-25T01:00:00 | `LATENCY_SPIKE_P99` |  | 4500.0 | P99 latency spike in minute 2026-11-25T01:00: 4500.0ms (mean 185.0ms) |
| 2026-11-25T01:00:05 | `SERVER_ERROR` | 10.0.1.43 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.43 (latency 108ms) |
| 2026-11-25T01:00:13 | `SERVER_ERROR` | 10.0.3.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.15 (latency 63ms) |
| 2026-11-25T01:00:25 | `SERVER_ERROR` | 10.0.2.1 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.1 (latency 25ms) |
| 2026-11-25T01:00:27 | `NEW_IP` | 10.0.4.33 | 1 | New client IP detected: 10.0.4.33 |
| 2026-11-25T01:00:29 | `SERVER_ERROR` | 10.0.4.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.33 (latency 74ms) |
| 2026-11-25T01:00:35 | `SERVER_ERROR` | 10.0.2.48 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.48 (latency 97ms) |
| 2026-11-25T01:00:38 | `SERVER_ERROR` | 10.0.2.23 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.23 (latency 49ms) |
| 2026-11-25T01:00:47 | `SERVER_ERROR` | 10.0.2.31 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.31 (latency 50ms) |
| 2026-11-25T01:00:48 | `NEW_IP` | 10.0.2.3 | 1 | New client IP detected: 10.0.2.3 |
| 2026-11-25T01:00:49 | `SERVER_ERROR` | 10.0.4.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.37 (latency 99ms) |
| 2026-11-25T01:00:52 | `SERVER_ERROR` | 10.0.4.18 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.18 (latency 113ms) |
| 2026-11-25T01:00:58 | `SERVER_ERROR` | 10.0.1.19 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.19 (latency 77ms) |
| 2026-11-25T01:00:59 | `SERVER_ERROR` | 10.0.4.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.26 (latency 109ms) |
| 2026-11-25T01:01:00 | `LATENCY_SPIKE_P99` |  | 4500.0 | P99 latency spike in minute 2026-11-25T01:01: 4500.0ms (mean 185.0ms) |
| 2026-11-25T01:01:00 | `SERVER_ERROR` | 10.0.2.1 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.1 (latency 45ms) |
| 2026-11-25T01:01:05 | `SERVER_ERROR` | 10.0.3.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.49 (latency 58ms) |
| 2026-11-25T01:01:21 | `SERVER_ERROR` | 10.0.3.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.17 (latency 21ms) |
| 2026-11-25T01:01:31 | `SERVER_ERROR` | 10.0.4.31 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.31 (latency 88ms) |
| 2026-11-25T01:01:38 | `NEW_IP` | 10.0.1.1 | 1 | New client IP detected: 10.0.1.1 |
| 2026-11-25T01:01:39 | `SERVER_ERROR` | 10.0.1.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.7 (latency 80ms) |
| 2026-11-25T01:01:40 | `SERVER_ERROR` | 10.0.2.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.26 (latency 48ms) |
| 2026-11-25T01:01:43 | `SERVER_ERROR` | 10.0.2.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.9 (latency 25ms) |
| 2026-11-25T01:01:50 | `NEW_IP` | 10.0.2.42 | 1 | New client IP detected: 10.0.2.42 |
| 2026-11-25T01:01:50 | `SERVER_ERROR` | 10.0.2.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.42 (latency 13ms) |
| 2026-11-25T01:01:51 | `SERVER_ERROR` | 10.0.1.25 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.25 (latency 99ms) |
| 2026-11-25T01:01:52 | `SERVER_ERROR` | 10.0.2.35 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.35 (latency 113ms) |
| 2026-11-25T01:02:01 | `SERVER_ERROR` | 10.0.4.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.39 (latency 113ms) |
| 2026-11-25T01:02:04 | `SERVER_ERROR` | 10.0.3.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.47 (latency 63ms) |
| 2026-11-25T01:02:19 | `SERVER_ERROR` | 10.0.4.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.17 (latency 102ms) |
| 2026-11-25T01:02:26 | `SERVER_ERROR` | 10.0.3.46 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.46 (latency 85ms) |
| 2026-11-25T01:02:30 | `SERVER_ERROR` | 10.0.1.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.40 (latency 99ms) |
| 2026-11-25T01:02:33 | `SERVER_ERROR` | 10.0.4.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.44 (latency 39ms) |
| 2026-11-25T01:02:36 | `SERVER_ERROR` | 10.0.2.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.30 (latency 38ms) |
| 2026-11-25T01:02:48 | `SERVER_ERROR` | 10.0.1.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.8 (latency 15ms) |
| 2026-11-25T01:02:51 | `SERVER_ERROR` | 10.0.3.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.24 (latency 92ms) |
| 2026-11-25T01:02:53 | `SERVER_ERROR` | 10.0.2.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.33 (latency 75ms) |
| 2026-11-25T01:02:56 | `SERVER_ERROR` | 10.0.2.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.13 (latency 69ms) |
| 2026-11-25T01:02:57 | `SERVER_ERROR` | 10.0.1.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.22 (latency 69ms) |
| 2026-11-25T01:02:59 | `SERVER_ERROR` | 10.0.3.35 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.35 (latency 40ms) |
| 2026-11-25T01:03:03 | `SERVER_ERROR` | 10.0.2.28 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.28 (latency 30ms) |
| 2026-11-25T01:03:13 | `SERVER_ERROR` | 10.0.2.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.39 (latency 73ms) |
| 2026-11-25T01:03:16 | `SERVER_ERROR` | 10.0.3.18 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.18 (latency 25ms) |
| 2026-11-25T01:03:20 | `SERVER_ERROR` | 10.0.3.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.44 (latency 19ms) |
| 2026-11-25T01:03:21 | `NEW_IP` | 10.0.1.46 | 1 | New client IP detected: 10.0.1.46 |
| 2026-11-25T01:03:21 | `SERVER_ERROR` | 10.0.1.46 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.46 (latency 28ms) |
| 2026-11-25T01:03:23 | `SERVER_ERROR` | 10.0.4.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.34 (latency 92ms) |
| 2026-11-25T01:03:26 | `SERVER_ERROR` | 10.0.4.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.10 (latency 115ms) |
| 2026-11-25T01:03:27 | `SERVER_ERROR` | 10.0.2.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.8 (latency 73ms) |
| 2026-11-25T01:03:34 | `SERVER_ERROR` | 10.0.1.48 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.48 (latency 24ms) |
| 2026-11-25T01:03:38 | `SERVER_ERROR` | 10.0.1.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.13 (latency 36ms) |
| 2026-11-25T01:03:45 | `SERVER_ERROR` | 10.0.2.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.34 (latency 29ms) |
| 2026-11-25T01:03:51 | `SERVER_ERROR` | 10.0.3.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.12 (latency 91ms) |
| 2026-11-25T01:03:52 | `SERVER_ERROR` | 10.0.3.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.7 (latency 17ms) |
| 2026-11-25T01:04:01 | `SERVER_ERROR` | 10.0.3.48 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.48 (latency 17ms) |
| 2026-11-25T01:04:02 | `SERVER_ERROR` | 10.0.4.25 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.25 (latency 35ms) |
| 2026-11-25T01:04:04 | `SERVER_ERROR` | 10.0.2.5 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.5 (latency 63ms) |
| 2026-11-25T01:04:06 | `SERVER_ERROR` | 10.0.2.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.9 (latency 81ms) |
| 2026-11-25T01:04:08 | `SERVER_ERROR` | 10.0.3.43 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.43 (latency 30ms) |
| 2026-11-25T01:04:11 | `NEW_IP` | 10.0.3.48 | 1 | New client IP detected: 10.0.3.48 |
| 2026-11-25T01:04:14 | `SERVER_ERROR` | 10.0.4.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.26 (latency 107ms) |
| 2026-11-25T01:04:16 | `SERVER_ERROR` | 10.0.1.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.4 (latency 80ms) |
| 2026-11-25T01:04:18 | `SERVER_ERROR` | 10.0.1.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.2 (latency 37ms) |
| 2026-11-25T01:04:26 | `SERVER_ERROR` | 10.0.1.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.9 (latency 32ms) |
| 2026-11-25T01:04:32 | `NEW_IP` | 10.0.1.15 | 1 | New client IP detected: 10.0.1.15 |
| 2026-11-25T01:04:34 | `SERVER_ERROR` | 10.0.1.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.8 (latency 106ms) |
| 2026-11-25T01:04:42 | `SERVER_ERROR` | 10.0.2.14 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.14 (latency 10ms) |
| 2026-11-25T01:04:44 | `SERVER_ERROR` | 10.0.3.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.49 (latency 19ms) |
| 2026-11-25T01:05:01 | `SERVER_ERROR` | 10.0.2.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.15 (latency 25ms) |
| 2026-11-25T01:05:06 | `SERVER_ERROR` | 10.0.3.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.15 (latency 103ms) |
| 2026-11-25T01:05:08 | `SERVER_ERROR` | 10.0.2.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.6 (latency 10ms) |
| 2026-11-25T01:05:10 | `SERVER_ERROR` | 10.0.3.38 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.38 (latency 90ms) |
| 2026-11-25T01:05:13 | `SERVER_ERROR` | 10.0.4.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.45 (latency 99ms) |
| 2026-11-25T01:05:29 | `SERVER_ERROR` | 10.0.1.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.8 (latency 86ms) |
| 2026-11-25T01:05:33 | `NEW_IP` | 10.0.2.1 | 1 | New client IP detected: 10.0.2.1 |
| 2026-11-25T01:05:33 | `SERVER_ERROR` | 10.0.2.1 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.1 (latency 65ms) |
| 2026-11-25T01:05:45 | `SERVER_ERROR` | 10.0.1.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.4 (latency 83ms) |
| 2026-11-25T01:05:47 | `SERVER_ERROR` | 10.0.4.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.49 (latency 78ms) |
| 2026-11-25T01:05:49 | `SERVER_ERROR` | 10.0.2.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.37 (latency 100ms) |
| 2026-11-25T01:05:57 | `SERVER_ERROR` | 10.0.1.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.22 (latency 97ms) |
| 2026-11-25T01:06:17 | `SERVER_ERROR` | 10.0.4.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.44 (latency 84ms) |
| 2026-11-25T01:06:20 | `SERVER_ERROR` | 10.0.3.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.24 (latency 47ms) |
| 2026-11-25T01:06:26 | `SERVER_ERROR` | 10.0.4.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.42 (latency 45ms) |
| 2026-11-25T01:06:29 | `SERVER_ERROR` | 10.0.2.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.16 (latency 61ms) |
| 2026-11-25T01:06:48 | `SERVER_ERROR` | 10.0.2.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.47 (latency 58ms) |
| 2026-11-25T01:07:01 | `SERVER_ERROR` | 10.0.4.38 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.38 (latency 111ms) |
| 2026-11-25T01:07:02 | `SERVER_ERROR` | 10.0.3.19 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.19 (latency 61ms) |
| 2026-11-25T01:07:07 | `SERVER_ERROR` | 10.0.1.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.20 (latency 32ms) |
| 2026-11-25T01:07:14 | `NEW_IP` | 10.0.1.29 | 1 | New client IP detected: 10.0.1.29 |
| 2026-11-25T01:07:18 | `SERVER_ERROR` | 10.0.1.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.20 (latency 111ms) |
| 2026-11-25T01:07:21 | `SERVER_ERROR` | 10.0.2.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.39 (latency 70ms) |
| 2026-11-25T01:07:27 | `SERVER_ERROR` | 10.0.3.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.29 (latency 118ms) |
| 2026-11-25T01:07:28 | `SERVER_ERROR` | 10.0.2.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.49 (latency 52ms) |
| 2026-11-25T01:07:30 | `SERVER_ERROR` | 10.0.2.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.3 (latency 54ms) |
| 2026-11-25T01:07:43 | `SERVER_ERROR` | 10.0.3.48 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.48 (latency 47ms) |
| 2026-11-25T01:08:02 | `SERVER_ERROR` | 10.0.2.23 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.23 (latency 79ms) |
| 2026-11-25T01:08:09 | `SERVER_ERROR` | 10.0.3.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.34 (latency 12ms) |
| 2026-11-25T01:08:10 | `SERVER_ERROR` | 10.0.2.14 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.14 (latency 69ms) |
| 2026-11-25T01:08:15 | `SERVER_ERROR` | 10.0.4.11 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.11 (latency 92ms) |
| 2026-11-25T01:08:17 | `SERVER_ERROR` | 10.0.1.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.16 (latency 93ms) |
| 2026-11-25T01:08:33 | `SERVER_ERROR` | 10.0.4.46 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.46 (latency 61ms) |
| 2026-11-25T01:08:36 | `SERVER_ERROR` | 10.0.4.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.49 (latency 100ms) |
| 2026-11-25T01:08:47 | `NEW_IP` | 10.0.3.3 | 1 | New client IP detected: 10.0.3.3 |
| 2026-11-25T01:08:53 | `SERVER_ERROR` | 10.0.2.46 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.46 (latency 60ms) |
| 2026-11-25T01:09:06 | `SERVER_ERROR` | 10.0.2.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.39 (latency 98ms) |
| 2026-11-25T01:09:15 | `SERVER_ERROR` | 10.0.4.5 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.5 (latency 104ms) |
| 2026-11-25T01:09:16 | `NEW_IP` | 10.0.3.17 | 1 | New client IP detected: 10.0.3.17 |
| 2026-11-25T01:09:26 | `SERVER_ERROR` | 10.0.1.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.10 (latency 76ms) |
| 2026-11-25T01:09:29 | `SERVER_ERROR` | 10.0.3.5 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.5 (latency 98ms) |
| 2026-11-25T01:09:31 | `SERVER_ERROR` | 10.0.4.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.7 (latency 54ms) |
| 2026-11-25T01:09:33 | `SERVER_ERROR` | 10.0.2.1 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.1 (latency 79ms) |
| 2026-11-25T01:09:36 | `SERVER_ERROR` | 10.0.2.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.36 (latency 89ms) |
| 2026-11-25T01:09:44 | `SERVER_ERROR` | 10.0.3.1 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.1 (latency 107ms) |
| 2026-11-25T01:10:19 | `SERVER_ERROR` | 10.0.1.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.24 (latency 80ms) |
| 2026-11-25T01:10:25 | `NEW_IP` | 10.0.2.44 | 1 | New client IP detected: 10.0.2.44 |
| 2026-11-25T01:10:28 | `SERVER_ERROR` | 10.0.2.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.21 (latency 95ms) |
| 2026-11-25T01:10:29 | `SERVER_ERROR` | 10.0.2.31 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.31 (latency 17ms) |
| 2026-11-25T01:10:38 | `SERVER_ERROR` | 10.0.4.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.30 (latency 36ms) |
| 2026-11-25T01:10:46 | `SERVER_ERROR` | 10.0.1.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.16 (latency 118ms) |
| 2026-11-25T01:10:48 | `SERVER_ERROR` | 10.0.1.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.36 (latency 51ms) |
| 2026-11-25T01:10:51 | `SERVER_ERROR` | 10.0.2.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.24 (latency 53ms) |
| 2026-11-25T01:10:55 | `SERVER_ERROR` | 10.0.2.32 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.32 (latency 107ms) |
| 2026-11-25T01:11:07 | `SERVER_ERROR` | 10.0.3.32 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.32 (latency 73ms) |
| 2026-11-25T01:11:12 | `SERVER_ERROR` | 10.0.1.28 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.28 (latency 32ms) |
| 2026-11-25T01:11:19 | `SERVER_ERROR` | 10.0.4.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.10 (latency 16ms) |
| 2026-11-25T01:11:21 | `SERVER_ERROR` | 10.0.1.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.12 (latency 15ms) |
| 2026-11-25T01:11:23 | `SERVER_ERROR` | 10.0.2.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.41 (latency 23ms) |
| 2026-11-25T01:11:25 | `NEW_IP` | 10.0.2.9 | 1 | New client IP detected: 10.0.2.9 |
| 2026-11-25T01:11:27 | `SERVER_ERROR` | 10.0.1.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.24 (latency 114ms) |
| 2026-11-25T01:11:39 | `SERVER_ERROR` | 10.0.2.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.33 (latency 80ms) |
| 2026-11-25T01:11:43 | `SERVER_ERROR` | 10.0.1.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.15 (latency 60ms) |
| 2026-11-25T01:11:44 | `SERVER_ERROR` | 10.0.1.28 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.28 (latency 39ms) |
| 2026-11-25T01:11:52 | `SERVER_ERROR` | 10.0.3.32 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.32 (latency 44ms) |
| 2026-11-25T01:11:57 | `SERVER_ERROR` | 10.0.2.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.36 (latency 104ms) |
| 2026-11-25T01:12:02 | `NEW_IP` | 10.0.1.12 | 1 | New client IP detected: 10.0.1.12 |
| 2026-11-25T01:12:09 | `SERVER_ERROR` | 10.0.2.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.3 (latency 49ms) |
| 2026-11-25T01:12:14 | `SERVER_ERROR` | 10.0.2.35 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.35 (latency 36ms) |
| 2026-11-25T01:12:22 | `SERVER_ERROR` | 10.0.2.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.16 (latency 85ms) |
| 2026-11-25T01:12:23 | `SERVER_ERROR` | 10.0.4.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.6 (latency 103ms) |
| 2026-11-25T01:12:24 | `SERVER_ERROR` | 10.0.1.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.34 (latency 115ms) |
| 2026-11-25T01:12:30 | `SERVER_ERROR` | 10.0.3.11 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.11 (latency 46ms) |
| 2026-11-25T01:12:31 | `SERVER_ERROR` | 10.0.1.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.49 (latency 38ms) |
| 2026-11-25T01:12:35 | `SERVER_ERROR` | 10.0.1.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.47 (latency 23ms) |
| 2026-11-25T01:12:41 | `SERVER_ERROR` | 10.0.1.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.3 (latency 56ms) |
| 2026-11-25T01:12:42 | `SERVER_ERROR` | 10.0.2.46 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.46 (latency 17ms) |
| 2026-11-25T01:12:43 | `NEW_IP` | 10.0.2.49 | 1 | New client IP detected: 10.0.2.49 |
| 2026-11-25T01:12:46 | `SERVER_ERROR` | 10.0.1.43 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.43 (latency 97ms) |
| 2026-11-25T01:12:49 | `SERVER_ERROR` | 10.0.3.48 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.48 (latency 40ms) |
| 2026-11-25T01:12:55 | `NEW_IP` | 10.0.1.19 | 1 | New client IP detected: 10.0.1.19 |
| 2026-11-25T01:12:56 | `SERVER_ERROR` | 10.0.3.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.7 (latency 17ms) |
| 2026-11-25T01:13:04 | `SERVER_ERROR` | 10.0.4.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.24 (latency 115ms) |
| 2026-11-25T01:13:14 | `SERVER_ERROR` | 10.0.4.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.22 (latency 63ms) |
| 2026-11-25T01:13:20 | `SERVER_ERROR` | 10.0.2.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.20 (latency 55ms) |
| 2026-11-25T01:13:37 | `SERVER_ERROR` | 10.0.4.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.13 (latency 81ms) |
| 2026-11-25T01:13:55 | `NEW_IP` | 10.0.2.2 | 1 | New client IP detected: 10.0.2.2 |
| 2026-11-25T01:14:02 | `SERVER_ERROR` | 10.0.2.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.6 (latency 110ms) |
| 2026-11-25T01:14:04 | `SERVER_ERROR` | 10.0.1.18 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.18 (latency 27ms) |
| 2026-11-25T01:14:07 | `SERVER_ERROR` | 10.0.1.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.15 (latency 42ms) |
| 2026-11-25T01:14:11 | `SERVER_ERROR` | 10.0.4.19 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.19 (latency 57ms) |
| 2026-11-25T01:14:21 | `SERVER_ERROR` | 10.0.2.28 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.28 (latency 21ms) |
| 2026-11-25T01:14:24 | `SERVER_ERROR` | 10.0.2.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.15 (latency 38ms) |
| 2026-11-25T01:14:40 | `NEW_IP` | 10.0.1.21 | 1 | New client IP detected: 10.0.1.21 |
| 2026-11-25T01:14:40 | `SERVER_ERROR` | 10.0.1.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.21 (latency 101ms) |
| 2026-11-25T01:14:43 | `SERVER_ERROR` | 10.0.4.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.37 (latency 25ms) |
| 2026-11-25T01:14:56 | `SERVER_ERROR` | 10.0.3.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.24 (latency 113ms) |
| 2026-11-25T01:14:59 | `NEW_IP` | 10.0.4.44 | 1 | New client IP detected: 10.0.4.44 |
| 2026-11-25T01:15:01 | `SERVER_ERROR` | 10.0.4.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.34 (latency 74ms) |
| 2026-11-25T01:15:05 | `SERVER_ERROR` | 10.0.3.23 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.23 (latency 76ms) |
| 2026-11-25T01:15:12 | `SERVER_ERROR` | 10.0.3.19 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.19 (latency 36ms) |
| 2026-11-25T01:15:21 | `SERVER_ERROR` | 10.0.3.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.4 (latency 23ms) |
| 2026-11-25T01:15:22 | `NEW_IP` | 10.0.4.21 | 1 | New client IP detected: 10.0.4.21 |
| 2026-11-25T01:15:36 | `SERVER_ERROR` | 10.0.4.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.10 (latency 84ms) |
| 2026-11-25T01:15:38 | `SERVER_ERROR` | 10.0.3.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.40 (latency 120ms) |
| 2026-11-25T01:15:39 | `SERVER_ERROR` | 10.0.4.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.49 (latency 66ms) |
| 2026-11-25T01:15:41 | `SERVER_ERROR` | 10.0.1.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.41 (latency 56ms) |
| 2026-11-25T01:15:50 | `SERVER_ERROR` | 10.0.2.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.3 (latency 49ms) |
| 2026-11-25T01:15:51 | `SERVER_ERROR` | 10.0.3.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.41 (latency 10ms) |
| 2026-11-25T01:15:55 | `SERVER_ERROR` | 10.0.4.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.40 (latency 44ms) |
| 2026-11-25T01:15:58 | `SERVER_ERROR` | 10.0.4.25 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.25 (latency 99ms) |
| 2026-11-25T01:16:05 | `NEW_IP` | 10.0.3.18 | 1 | New client IP detected: 10.0.3.18 |
| 2026-11-25T01:16:05 | `SERVER_ERROR` | 10.0.3.18 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.18 (latency 106ms) |
| 2026-11-25T01:16:06 | `SERVER_ERROR` | 10.0.1.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.16 (latency 14ms) |
| 2026-11-25T01:16:14 | `SERVER_ERROR` | 10.0.3.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.12 (latency 96ms) |
| 2026-11-25T01:16:16 | `SERVER_ERROR` | 10.0.3.23 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.23 (latency 90ms) |
| 2026-11-25T01:16:24 | `SERVER_ERROR` | 10.0.3.11 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.11 (latency 48ms) |
| 2026-11-25T01:16:27 | `SERVER_ERROR` | 10.0.1.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.42 (latency 54ms) |
| 2026-11-25T01:16:29 | `SERVER_ERROR` | 10.0.2.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.26 (latency 92ms) |
| 2026-11-25T01:16:39 | `SERVER_ERROR` | 10.0.1.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.45 (latency 16ms) |
| 2026-11-25T01:16:43 | `SERVER_ERROR` | 10.0.4.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.13 (latency 79ms) |
| 2026-11-25T01:16:44 | `SERVER_ERROR` | 10.0.3.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.16 (latency 38ms) |
| 2026-11-25T01:16:46 | `SERVER_ERROR` | 10.0.4.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.40 (latency 96ms) |
| 2026-11-25T01:16:54 | `SERVER_ERROR` | 10.0.1.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.4 (latency 48ms) |
| 2026-11-25T01:17:01 | `SERVER_ERROR` | 10.0.4.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.16 (latency 52ms) |
| 2026-11-25T01:17:12 | `SERVER_ERROR` | 10.0.1.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.13 (latency 79ms) |
| 2026-11-25T01:17:15 | `SERVER_ERROR` | 10.0.2.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.26 (latency 49ms) |
| 2026-11-25T01:17:18 | `NEW_IP` | 10.0.1.13 | 1 | New client IP detected: 10.0.1.13 |
| 2026-11-25T01:17:21 | `SERVER_ERROR` | 10.0.3.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.37 (latency 45ms) |
| 2026-11-25T01:17:31 | `NEW_IP` | 10.0.1.2 | 1 | New client IP detected: 10.0.1.2 |
| 2026-11-25T01:17:33 | `SERVER_ERROR` | 10.0.4.28 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.28 (latency 30ms) |
| 2026-11-25T01:17:37 | `SERVER_ERROR` | 10.0.1.23 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.23 (latency 82ms) |
| 2026-11-25T01:17:38 | `SERVER_ERROR` | 10.0.3.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.22 (latency 50ms) |
| 2026-11-25T01:17:43 | `NEW_IP` | 10.0.2.34 | 1 | New client IP detected: 10.0.2.34 |
| 2026-11-25T01:17:50 | `SERVER_ERROR` | 10.0.4.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.27 (latency 100ms) |
| 2026-11-25T01:17:56 | `NEW_IP` | 10.0.4.46 | 1 | New client IP detected: 10.0.4.46 |
| 2026-11-25T01:17:56 | `SERVER_ERROR` | 10.0.4.46 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.46 (latency 115ms) |
| 2026-11-25T01:18:17 | `SERVER_ERROR` | 10.0.1.25 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.25 (latency 95ms) |
| 2026-11-25T01:18:19 | `SERVER_ERROR` | 10.0.3.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.45 (latency 77ms) |
| 2026-11-25T01:18:33 | `SERVER_ERROR` | 10.0.4.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.47 (latency 116ms) |
| 2026-11-25T01:18:35 | `SERVER_ERROR` | 10.0.1.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.26 (latency 83ms) |
| 2026-11-25T01:18:41 | `SERVER_ERROR` | 10.0.4.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.42 (latency 94ms) |
| 2026-11-25T01:18:45 | `SERVER_ERROR` | 10.0.3.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.44 (latency 41ms) |
| 2026-11-25T01:18:49 | `SERVER_ERROR` | 10.0.2.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.3 (latency 86ms) |
| 2026-11-25T01:18:54 | `SERVER_ERROR` | 10.0.3.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.26 (latency 70ms) |
| 2026-11-25T01:18:55 | `SERVER_ERROR` | 10.0.1.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.15 (latency 104ms) |
| 2026-11-25T01:19:01 | `SERVER_ERROR` | 10.0.4.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.33 (latency 60ms) |
| 2026-11-25T01:19:03 | `SERVER_ERROR` | 10.0.3.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.39 (latency 100ms) |
| 2026-11-25T01:19:09 | `NEW_IP` | 10.0.2.29 | 1 | New client IP detected: 10.0.2.29 |
| 2026-11-25T01:19:12 | `SERVER_ERROR` | 10.0.1.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.6 (latency 66ms) |
| 2026-11-25T01:19:16 | `SERVER_ERROR` | 10.0.4.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.4 (latency 34ms) |
| 2026-11-25T01:19:28 | `SERVER_ERROR` | 10.0.2.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.15 (latency 71ms) |
| 2026-11-25T01:19:31 | `SERVER_ERROR` | 10.0.2.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.9 (latency 98ms) |
| 2026-11-25T01:19:46 | `SERVER_ERROR` | 10.0.2.5 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.5 (latency 107ms) |
| 2026-11-25T01:19:55 | `SERVER_ERROR` | 10.0.4.32 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.32 (latency 74ms) |
| 2026-11-25T01:19:58 | `SERVER_ERROR` | 10.0.4.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.47 (latency 96ms) |
| 2026-11-25T01:20:02 | `SERVER_ERROR` | 10.0.2.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.12 (latency 41ms) |
| 2026-11-25T01:20:08 | `SERVER_ERROR` | 10.0.3.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.16 (latency 114ms) |
| 2026-11-25T01:20:09 | `NEW_IP` | 10.0.3.31 | 1 | New client IP detected: 10.0.3.31 |
| 2026-11-25T01:20:16 | `NEW_IP` | 10.0.3.10 | 1 | New client IP detected: 10.0.3.10 |
| 2026-11-25T01:20:26 | `SERVER_ERROR` | 10.0.3.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.9 (latency 51ms) |
| 2026-11-25T01:20:39 | `SERVER_ERROR` | 10.0.4.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.41 (latency 76ms) |
| 2026-11-25T01:20:48 | `SERVER_ERROR` | 10.0.3.11 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.11 (latency 77ms) |
| 2026-11-25T01:20:53 | `SERVER_ERROR` | 10.0.2.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.44 (latency 77ms) |
| 2026-11-25T01:21:11 | `SERVER_ERROR` | 10.0.1.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.9 (latency 53ms) |
| 2026-11-25T01:21:16 | `SERVER_ERROR` | 10.0.1.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.15 (latency 51ms) |
| 2026-11-25T01:21:17 | `SERVER_ERROR` | 10.0.4.14 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.14 (latency 83ms) |
| 2026-11-25T01:21:20 | `SERVER_ERROR` | 10.0.2.14 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.14 (latency 69ms) |
| 2026-11-25T01:21:30 | `SERVER_ERROR` | 10.0.2.25 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.25 (latency 57ms) |
| 2026-11-25T01:21:31 | `SERVER_ERROR` | 10.0.2.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.6 (latency 65ms) |
| 2026-11-25T01:21:32 | `SERVER_ERROR` | 10.0.1.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.24 (latency 103ms) |
| 2026-11-25T01:21:38 | `SERVER_ERROR` | 10.0.2.38 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.38 (latency 28ms) |
| 2026-11-25T01:22:01 | `NEW_IP` | 10.0.3.34 | 1 | New client IP detected: 10.0.3.34 |
| 2026-11-25T01:22:04 | `SERVER_ERROR` | 10.0.3.28 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.28 (latency 16ms) |
| 2026-11-25T01:22:07 | `NEW_IP` | 10.0.1.4 | 1 | New client IP detected: 10.0.1.4 |
| 2026-11-25T01:22:07 | `SERVER_ERROR` | 10.0.1.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.4 (latency 94ms) |
| 2026-11-25T01:22:16 | `SERVER_ERROR` | 10.0.1.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.15 (latency 120ms) |
| 2026-11-25T01:22:20 | `SERVER_ERROR` | 10.0.1.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.10 (latency 79ms) |
| 2026-11-25T01:22:32 | `SERVER_ERROR` | 10.0.1.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.16 (latency 36ms) |
| 2026-11-25T01:22:43 | `SERVER_ERROR` | 10.0.3.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.16 (latency 94ms) |
| 2026-11-25T01:22:46 | `SERVER_ERROR` | 10.0.3.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.41 (latency 67ms) |
| 2026-11-25T01:22:50 | `NEW_IP` | 10.0.3.40 | 1 | New client IP detected: 10.0.3.40 |
| 2026-11-25T01:22:54 | `SERVER_ERROR` | 10.0.3.35 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.35 (latency 106ms) |
| 2026-11-25T01:22:55 | `SERVER_ERROR` | 10.0.4.35 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.35 (latency 83ms) |
| 2026-11-25T01:23:05 | `SERVER_ERROR` | 10.0.2.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.2 (latency 12ms) |
| 2026-11-25T01:23:08 | `SERVER_ERROR` | 10.0.3.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.34 (latency 77ms) |
| 2026-11-25T01:23:13 | `SERVER_ERROR` | 10.0.4.18 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.18 (latency 19ms) |
| 2026-11-25T01:23:22 | `SERVER_ERROR` | 10.0.2.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.2 (latency 39ms) |
| 2026-11-25T01:23:25 | `SERVER_ERROR` | 10.0.2.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.13 (latency 37ms) |
| 2026-11-25T01:23:27 | `SERVER_ERROR` | 10.0.1.43 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.43 (latency 65ms) |
| 2026-11-25T01:23:29 | `NEW_IP` | 10.0.4.49 | 1 | New client IP detected: 10.0.4.49 |
| 2026-11-25T01:23:34 | `SERVER_ERROR` | 10.0.3.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.36 (latency 36ms) |
| 2026-11-25T01:23:39 | `SERVER_ERROR` | 10.0.2.25 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.25 (latency 17ms) |
| 2026-11-25T01:23:43 | `SERVER_ERROR` | 10.0.3.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.8 (latency 26ms) |
| 2026-11-25T01:23:45 | `SERVER_ERROR` | 10.0.3.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.3 (latency 98ms) |
| 2026-11-25T01:23:48 | `SERVER_ERROR` | 10.0.2.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.9 (latency 28ms) |
| 2026-11-25T01:23:55 | `SERVER_ERROR` | 10.0.1.23 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.23 (latency 111ms) |
| 2026-11-25T01:24:06 | `NEW_IP` | 10.0.2.33 | 1 | New client IP detected: 10.0.2.33 |
| 2026-11-25T01:24:17 | `SERVER_ERROR` | 10.0.4.25 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.25 (latency 56ms) |
| 2026-11-25T01:24:18 | `SERVER_ERROR` | 10.0.1.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.27 (latency 119ms) |
| 2026-11-25T01:24:22 | `SERVER_ERROR` | 10.0.3.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.12 (latency 20ms) |
| 2026-11-25T01:24:37 | `SERVER_ERROR` | 10.0.3.38 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.38 (latency 103ms) |
| 2026-11-25T01:24:41 | `SERVER_ERROR` | 10.0.2.31 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.31 (latency 113ms) |
| 2026-11-25T01:24:42 | `SERVER_ERROR` | 10.0.4.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.20 (latency 14ms) |
| 2026-11-25T01:24:51 | `SERVER_ERROR` | 10.0.2.43 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.43 (latency 38ms) |
| 2026-11-25T01:24:55 | `SERVER_ERROR` | 10.0.2.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.45 (latency 39ms) |
| 2026-11-25T01:25:06 | `SERVER_ERROR` | 10.0.3.43 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.43 (latency 81ms) |
| 2026-11-25T01:25:09 | `SERVER_ERROR` | 10.0.3.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.13 (latency 22ms) |
| 2026-11-25T01:25:13 | `SERVER_ERROR` | 10.0.3.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.3 (latency 95ms) |
| 2026-11-25T01:25:17 | `SERVER_ERROR` | 10.0.3.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.41 (latency 107ms) |
| 2026-11-25T01:25:20 | `NEW_IP` | 10.0.3.23 | 1 | New client IP detected: 10.0.3.23 |
| 2026-11-25T01:25:21 | `SERVER_ERROR` | 10.0.4.18 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.18 (latency 17ms) |
| 2026-11-25T01:25:24 | `SERVER_ERROR` | 10.0.2.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.12 (latency 54ms) |
| 2026-11-25T01:25:32 | `SERVER_ERROR` | 10.0.4.32 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.32 (latency 25ms) |
| 2026-11-25T01:25:34 | `SERVER_ERROR` | 10.0.2.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.8 (latency 12ms) |
| 2026-11-25T01:25:38 | `SERVER_ERROR` | 10.0.3.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.7 (latency 67ms) |
| 2026-11-25T01:25:43 | `SERVER_ERROR` | 10.0.3.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.49 (latency 78ms) |
| 2026-11-25T01:25:45 | `SERVER_ERROR` | 10.0.1.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.15 (latency 107ms) |
| 2026-11-25T01:25:54 | `SERVER_ERROR` | 10.0.1.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.8 (latency 44ms) |
| 2026-11-25T01:25:59 | `SERVER_ERROR` | 10.0.1.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.49 (latency 97ms) |
| 2026-11-25T01:26:04 | `SERVER_ERROR` | 10.0.4.18 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.18 (latency 53ms) |
| 2026-11-25T01:26:15 | `SERVER_ERROR` | 10.0.3.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.22 (latency 27ms) |
| 2026-11-25T01:26:25 | `SERVER_ERROR` | 10.0.2.35 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.35 (latency 22ms) |
| 2026-11-25T01:26:26 | `SERVER_ERROR` | 10.0.1.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.6 (latency 40ms) |
| 2026-11-25T01:26:28 | `SERVER_ERROR` | 10.0.2.32 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.32 (latency 97ms) |
| 2026-11-25T01:26:35 | `SERVER_ERROR` | 10.0.1.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.36 (latency 91ms) |
| 2026-11-25T01:26:36 | `SERVER_ERROR` | 10.0.2.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.8 (latency 53ms) |
| 2026-11-25T01:26:48 | `SERVER_ERROR` | 10.0.4.14 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.14 (latency 42ms) |
| 2026-11-25T01:26:49 | `NEW_IP` | 10.0.2.27 | 1 | New client IP detected: 10.0.2.27 |
| 2026-11-25T01:26:51 | `SERVER_ERROR` | 10.0.2.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.36 (latency 51ms) |
| 2026-11-25T01:26:53 | `NEW_IP` | 10.0.3.14 | 1 | New client IP detected: 10.0.3.14 |
| 2026-11-25T01:26:55 | `NEW_IP` | 10.0.2.13 | 1 | New client IP detected: 10.0.2.13 |
| 2026-11-25T01:26:55 | `SERVER_ERROR` | 10.0.2.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.13 (latency 33ms) |
| 2026-11-25T01:26:59 | `SERVER_ERROR` | 10.0.3.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.37 (latency 74ms) |
| 2026-11-25T01:27:02 | `SERVER_ERROR` | 10.0.4.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.3 (latency 49ms) |
| 2026-11-25T01:27:05 | `NEW_IP` | 10.0.3.22 | 1 | New client IP detected: 10.0.3.22 |
| 2026-11-25T01:27:06 | `SERVER_ERROR` | 10.0.2.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.41 (latency 115ms) |
| 2026-11-25T01:27:19 | `SERVER_ERROR` | 10.0.4.18 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.18 (latency 68ms) |
| 2026-11-25T01:27:21 | `SERVER_ERROR` | 10.0.2.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.3 (latency 78ms) |
| 2026-11-25T01:27:22 | `SERVER_ERROR` | 10.0.2.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.34 (latency 79ms) |
| 2026-11-25T01:27:27 | `SERVER_ERROR` | 10.0.1.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.45 (latency 53ms) |
| 2026-11-25T01:27:30 | `SERVER_ERROR` | 10.0.4.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.10 (latency 113ms) |
| 2026-11-25T01:27:36 | `SERVER_ERROR` | 10.0.4.38 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.38 (latency 108ms) |
| 2026-11-25T01:27:38 | `NEW_IP` | 10.0.3.2 | 1 | New client IP detected: 10.0.3.2 |
| 2026-11-25T01:27:48 | `SERVER_ERROR` | 10.0.4.14 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.14 (latency 26ms) |
| 2026-11-25T01:27:54 | `SERVER_ERROR` | 10.0.4.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.2 (latency 60ms) |
| 2026-11-25T01:27:56 | `SERVER_ERROR` | 10.0.3.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.8 (latency 96ms) |
| 2026-11-25T01:27:59 | `SERVER_ERROR` | 10.0.2.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.4 (latency 21ms) |
| 2026-11-25T01:28:09 | `SERVER_ERROR` | 10.0.4.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.6 (latency 21ms) |
| 2026-11-25T01:28:11 | `SERVER_ERROR` | 10.0.4.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.45 (latency 91ms) |
| 2026-11-25T01:28:16 | `SERVER_ERROR` | 10.0.3.38 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.38 (latency 59ms) |
| 2026-11-25T01:28:21 | `SERVER_ERROR` | 10.0.1.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.41 (latency 105ms) |
| 2026-11-25T01:28:35 | `SERVER_ERROR` | 10.0.2.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.9 (latency 34ms) |
| 2026-11-25T01:28:43 | `SERVER_ERROR` | 10.0.3.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.22 (latency 81ms) |
| 2026-11-25T01:28:44 | `SERVER_ERROR` | 10.0.1.25 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.25 (latency 31ms) |
| 2026-11-25T01:28:48 | `SERVER_ERROR` | 10.0.4.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.21 (latency 76ms) |
| 2026-11-25T01:28:50 | `SERVER_ERROR` | 10.0.1.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.45 (latency 116ms) |
| 2026-11-25T01:28:51 | `SERVER_ERROR` | 10.0.4.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.49 (latency 13ms) |
| 2026-11-25T01:28:58 | `SERVER_ERROR` | 10.0.3.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.49 (latency 99ms) |
| 2026-11-25T01:29:04 | `SERVER_ERROR` | 10.0.3.5 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.5 (latency 88ms) |
| 2026-11-25T01:29:08 | `SERVER_ERROR` | 10.0.2.14 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.14 (latency 75ms) |
| 2026-11-25T01:29:10 | `SERVER_ERROR` | 10.0.2.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.17 (latency 90ms) |
| 2026-11-25T01:29:25 | `NEW_IP` | 10.0.3.32 | 1 | New client IP detected: 10.0.3.32 |
| 2026-11-25T01:29:25 | `SERVER_ERROR` | 10.0.3.32 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.32 (latency 88ms) |
| 2026-11-25T01:29:26 | `SERVER_ERROR` | 10.0.2.38 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.38 (latency 105ms) |
| 2026-11-25T01:29:32 | `SERVER_ERROR` | 10.0.2.25 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.25 (latency 119ms) |
| 2026-11-25T01:29:40 | `SERVER_ERROR` | 10.0.1.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.49 (latency 115ms) |
| 2026-11-25T01:29:42 | `SERVER_ERROR` | 10.0.1.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.41 (latency 56ms) |
| 2026-11-25T01:29:45 | `SERVER_ERROR` | 10.0.3.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.7 (latency 118ms) |
| 2026-11-25T01:29:47 | `SERVER_ERROR` | 10.0.3.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.10 (latency 83ms) |
| 2026-11-25T01:29:48 | `SERVER_ERROR` | 10.0.4.35 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.35 (latency 114ms) |
| 2026-11-25T01:29:49 | `SERVER_ERROR` | 10.0.2.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.47 (latency 23ms) |
| 2026-11-25T01:29:57 | `SERVER_ERROR` | 10.0.1.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.34 (latency 54ms) |
| 2026-11-25T01:30:02 | `NEW_IP` | 10.0.4.41 | 1 | New client IP detected: 10.0.4.41 |
| 2026-11-25T01:30:02 | `SERVER_ERROR` | 10.0.4.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.41 (latency 47ms) |
| 2026-11-25T01:30:05 | `SERVER_ERROR` | 10.0.4.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.26 (latency 47ms) |
| 2026-11-25T01:30:09 | `SERVER_ERROR` | 10.0.4.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.16 (latency 67ms) |
| 2026-11-25T01:30:12 | `SERVER_ERROR` | 10.0.1.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.36 (latency 61ms) |
| 2026-11-25T01:30:18 | `SERVER_ERROR` | 10.0.1.48 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.48 (latency 111ms) |
| 2026-11-25T01:30:27 | `SERVER_ERROR` | 10.0.4.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.42 (latency 24ms) |
| 2026-11-25T01:30:29 | `SERVER_ERROR` | 10.0.3.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.8 (latency 93ms) |
| 2026-11-25T01:30:33 | `NEW_IP` | 10.0.3.8 | 1 | New client IP detected: 10.0.3.8 |
| 2026-11-25T01:30:35 | `SERVER_ERROR` | 10.0.1.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.12 (latency 33ms) |
| 2026-11-25T01:30:51 | `SERVER_ERROR` | 10.0.2.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.10 (latency 38ms) |
| 2026-11-25T01:30:55 | `SERVER_ERROR` | 10.0.1.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.13 (latency 65ms) |
| 2026-11-25T01:30:58 | `NEW_IP` | 10.0.3.12 | 1 | New client IP detected: 10.0.3.12 |
| 2026-11-25T01:31:01 | `SERVER_ERROR` | 10.0.2.5 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.5 (latency 92ms) |
| 2026-11-25T01:31:06 | `NEW_IP` | 10.0.3.5 | 1 | New client IP detected: 10.0.3.5 |
| 2026-11-25T01:31:09 | `NEW_IP` | 10.0.4.13 | 1 | New client IP detected: 10.0.4.13 |
| 2026-11-25T01:31:24 | `SERVER_ERROR` | 10.0.3.31 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.31 (latency 81ms) |
| 2026-11-25T01:31:30 | `SERVER_ERROR` | 10.0.4.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.6 (latency 70ms) |
| 2026-11-25T01:31:34 | `SERVER_ERROR` | 10.0.4.31 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.31 (latency 37ms) |
| 2026-11-25T01:31:46 | `SERVER_ERROR` | 10.0.4.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.45 (latency 21ms) |
| 2026-11-25T01:31:48 | `SERVER_ERROR` | 10.0.4.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.34 (latency 95ms) |
| 2026-11-25T01:31:50 | `SERVER_ERROR` | 10.0.2.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.6 (latency 68ms) |
| 2026-11-25T01:31:55 | `SERVER_ERROR` | 10.0.2.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.27 (latency 116ms) |
| 2026-11-25T01:31:58 | `SERVER_ERROR` | 10.0.3.35 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.35 (latency 43ms) |
| 2026-11-25T01:32:03 | `SERVER_ERROR` | 10.0.1.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.9 (latency 14ms) |
| 2026-11-25T01:32:10 | `SERVER_ERROR` | 10.0.3.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.2 (latency 91ms) |
| 2026-11-25T01:32:13 | `SERVER_ERROR` | 10.0.1.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.49 (latency 66ms) |
| 2026-11-25T01:32:17 | `SERVER_ERROR` | 10.0.3.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.39 (latency 116ms) |
| 2026-11-25T01:32:25 | `SERVER_ERROR` | 10.0.4.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.24 (latency 29ms) |
| 2026-11-25T01:32:28 | `SERVER_ERROR` | 10.0.2.32 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.32 (latency 97ms) |
| 2026-11-25T01:32:30 | `NEW_IP` | 10.0.3.36 | 1 | New client IP detected: 10.0.3.36 |
| 2026-11-25T01:32:33 | `SERVER_ERROR` | 10.0.2.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.29 (latency 54ms) |
| 2026-11-25T01:32:39 | `SERVER_ERROR` | 10.0.4.19 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.19 (latency 49ms) |
| 2026-11-25T01:33:02 | `SERVER_ERROR` | 10.0.4.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.49 (latency 25ms) |
| 2026-11-25T01:33:04 | `NEW_IP` | 10.0.3.25 | 1 | New client IP detected: 10.0.3.25 |
| 2026-11-25T01:33:09 | `SERVER_ERROR` | 10.0.4.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.27 (latency 43ms) |
| 2026-11-25T01:33:12 | `SERVER_ERROR` | 10.0.2.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.22 (latency 73ms) |
| 2026-11-25T01:33:13 | `SERVER_ERROR` | 10.0.3.46 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.46 (latency 53ms) |
| 2026-11-25T01:33:15 | `SERVER_ERROR` | 10.0.3.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.34 (latency 56ms) |
| 2026-11-25T01:33:16 | `NEW_IP` | 10.0.3.16 | 1 | New client IP detected: 10.0.3.16 |
| 2026-11-25T01:33:17 | `SERVER_ERROR` | 10.0.2.48 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.48 (latency 89ms) |
| 2026-11-25T01:33:20 | `NEW_IP` | 10.0.2.41 | 1 | New client IP detected: 10.0.2.41 |
| 2026-11-25T01:33:20 | `SERVER_ERROR` | 10.0.2.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.41 (latency 30ms) |
| 2026-11-25T01:33:21 | `SERVER_ERROR` | 10.0.1.14 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.14 (latency 53ms) |
| 2026-11-25T01:33:43 | `SERVER_ERROR` | 10.0.1.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.7 (latency 15ms) |
| 2026-11-25T01:33:46 | `SERVER_ERROR` | 10.0.3.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.17 (latency 114ms) |
| 2026-11-25T01:33:53 | `NEW_IP` | 10.0.4.36 | 1 | New client IP detected: 10.0.4.36 |
| 2026-11-25T01:33:54 | `SERVER_ERROR` | 10.0.4.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.3 (latency 32ms) |
| 2026-11-25T01:33:55 | `SERVER_ERROR` | 10.0.3.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.17 (latency 88ms) |
| 2026-11-25T01:33:59 | `SERVER_ERROR` | 10.0.1.18 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.18 (latency 75ms) |
| 2026-11-25T01:34:10 | `SERVER_ERROR` | 10.0.3.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.2 (latency 70ms) |
| 2026-11-25T01:34:22 | `NEW_IP` | 10.0.4.22 | 1 | New client IP detected: 10.0.4.22 |
| 2026-11-25T01:34:22 | `SERVER_ERROR` | 10.0.4.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.22 (latency 110ms) |
| 2026-11-25T01:34:23 | `SERVER_ERROR` | 10.0.4.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.34 (latency 114ms) |
| 2026-11-25T01:34:27 | `NEW_IP` | 10.0.1.35 | 1 | New client IP detected: 10.0.1.35 |
| 2026-11-25T01:34:27 | `SERVER_ERROR` | 10.0.1.35 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.35 (latency 68ms) |
| 2026-11-25T01:34:37 | `SERVER_ERROR` | 10.0.4.48 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.48 (latency 26ms) |
| 2026-11-25T01:34:42 | `SERVER_ERROR` | 10.0.3.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.40 (latency 33ms) |
| 2026-11-25T01:34:43 | `SERVER_ERROR` | 10.0.3.25 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.25 (latency 39ms) |
| 2026-11-25T01:34:44 | `SERVER_ERROR` | 10.0.2.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.15 (latency 47ms) |
| 2026-11-25T01:34:45 | `SERVER_ERROR` | 10.0.2.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.45 (latency 14ms) |
| 2026-11-25T01:34:46 | `SERVER_ERROR` | 10.0.3.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.45 (latency 68ms) |
| 2026-11-25T01:34:47 | `NEW_IP` | 10.0.2.39 | 1 | New client IP detected: 10.0.2.39 |
| 2026-11-25T01:34:47 | `SERVER_ERROR` | 10.0.2.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.39 (latency 38ms) |
| 2026-11-25T01:34:50 | `SERVER_ERROR` | 10.0.2.14 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.14 (latency 11ms) |
| 2026-11-25T01:35:01 | `SERVER_ERROR` | 10.0.1.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.8 (latency 116ms) |
| 2026-11-25T01:35:08 | `NEW_IP` | 10.0.3.9 | 1 | New client IP detected: 10.0.3.9 |
| 2026-11-25T01:35:19 | `SERVER_ERROR` | 10.0.2.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.42 (latency 12ms) |
| 2026-11-25T01:35:35 | `SERVER_ERROR` | 10.0.2.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.41 (latency 77ms) |
| 2026-11-25T01:35:40 | `NEW_IP` | 10.0.3.11 | 1 | New client IP detected: 10.0.3.11 |
| 2026-11-25T01:35:42 | `SERVER_ERROR` | 10.0.3.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.8 (latency 35ms) |
| 2026-11-25T01:35:50 | `SERVER_ERROR` | 10.0.3.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.2 (latency 18ms) |
| 2026-11-25T01:36:01 | `SERVER_ERROR` | 10.0.4.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.33 (latency 110ms) |
| 2026-11-25T01:36:03 | `SERVER_ERROR` | 10.0.4.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.6 (latency 32ms) |
| 2026-11-25T01:36:04 | `SERVER_ERROR` | 10.0.3.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.26 (latency 69ms) |
| 2026-11-25T01:36:09 | `SERVER_ERROR` | 10.0.1.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.36 (latency 94ms) |
| 2026-11-25T01:36:18 | `NEW_IP` | 10.0.3.44 | 1 | New client IP detected: 10.0.3.44 |
| 2026-11-25T01:36:20 | `SERVER_ERROR` | 10.0.3.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.21 (latency 61ms) |
| 2026-11-25T01:36:23 | `SERVER_ERROR` | 10.0.2.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.15 (latency 82ms) |
| 2026-11-25T01:36:33 | `SERVER_ERROR` | 10.0.2.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.15 (latency 110ms) |
| 2026-11-25T01:36:34 | `SERVER_ERROR` | 10.0.4.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.21 (latency 38ms) |
| 2026-11-25T01:36:36 | `SERVER_ERROR` | 10.0.3.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.21 (latency 38ms) |
| 2026-11-25T01:36:40 | `NEW_IP` | 10.0.2.43 | 1 | New client IP detected: 10.0.2.43 |
| 2026-11-25T01:36:41 | `NEW_IP` | 10.0.1.25 | 1 | New client IP detected: 10.0.1.25 |
| 2026-11-25T01:36:45 | `SERVER_ERROR` | 10.0.1.11 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.11 (latency 31ms) |
| 2026-11-25T01:37:03 | `SERVER_ERROR` | 10.0.1.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.30 (latency 102ms) |
| 2026-11-25T01:37:08 | `SERVER_ERROR` | 10.0.4.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.22 (latency 28ms) |
| 2026-11-25T01:37:10 | `SERVER_ERROR` | 10.0.2.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.6 (latency 34ms) |
| 2026-11-25T01:37:12 | `SERVER_ERROR` | 10.0.3.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.17 (latency 115ms) |
| 2026-11-25T01:37:34 | `SERVER_ERROR` | 10.0.1.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.39 (latency 107ms) |
| 2026-11-25T01:37:38 | `NEW_IP` | 10.0.1.17 | 1 | New client IP detected: 10.0.1.17 |
| 2026-11-25T01:37:40 | `SERVER_ERROR` | 10.0.2.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.47 (latency 114ms) |
| 2026-11-25T01:37:44 | `SERVER_ERROR` | 10.0.4.23 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.23 (latency 24ms) |
| 2026-11-25T01:37:59 | `SERVER_ERROR` | 10.0.2.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.45 (latency 54ms) |
| 2026-11-25T01:38:00 | `SERVER_ERROR` | 10.0.1.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.30 (latency 119ms) |
| 2026-11-25T01:38:04 | `SERVER_ERROR` | 10.0.4.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.42 (latency 16ms) |
| 2026-11-25T01:38:15 | `SERVER_ERROR` | 10.0.4.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.21 (latency 92ms) |
| 2026-11-25T01:38:18 | `SERVER_ERROR` | 10.0.4.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.2 (latency 102ms) |
| 2026-11-25T01:38:25 | `SERVER_ERROR` | 10.0.3.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.22 (latency 84ms) |
| 2026-11-25T01:38:28 | `SERVER_ERROR` | 10.0.4.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.9 (latency 67ms) |
| 2026-11-25T01:38:31 | `SERVER_ERROR` | 10.0.4.23 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.23 (latency 117ms) |
| 2026-11-25T01:38:36 | `SERVER_ERROR` | 10.0.3.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.41 (latency 103ms) |
| 2026-11-25T01:38:41 | `SERVER_ERROR` | 10.0.4.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.30 (latency 70ms) |
| 2026-11-25T01:38:45 | `SERVER_ERROR` | 10.0.1.32 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.32 (latency 101ms) |
| 2026-11-25T01:39:01 | `SERVER_ERROR` | 10.0.3.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.3 (latency 90ms) |
| 2026-11-25T01:39:05 | `SERVER_ERROR` | 10.0.1.28 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.28 (latency 118ms) |
| 2026-11-25T01:39:07 | `SERVER_ERROR` | 10.0.3.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.2 (latency 42ms) |
| 2026-11-25T01:39:11 | `SERVER_ERROR` | 10.0.4.11 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.11 (latency 36ms) |
| 2026-11-25T01:39:16 | `SERVER_ERROR` | 10.0.4.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.8 (latency 79ms) |
| 2026-11-25T01:39:19 | `SERVER_ERROR` | 10.0.1.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.9 (latency 117ms) |
| 2026-11-25T01:39:25 | `SERVER_ERROR` | 10.0.4.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.8 (latency 56ms) |
| 2026-11-25T01:39:30 | `NEW_IP` | 10.0.1.22 | 1 | New client IP detected: 10.0.1.22 |
| 2026-11-25T01:39:36 | `SERVER_ERROR` | 10.0.3.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.4 (latency 99ms) |
| 2026-11-25T01:39:41 | `SERVER_ERROR` | 10.0.3.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.33 (latency 84ms) |
| 2026-11-25T01:39:49 | `SERVER_ERROR` | 10.0.3.28 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.28 (latency 107ms) |
| 2026-11-25T01:39:50 | `SERVER_ERROR` | 10.0.4.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.37 (latency 99ms) |
| 2026-11-25T01:39:53 | `SERVER_ERROR` | 10.0.3.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.20 (latency 35ms) |
| 2026-11-25T01:40:04 | `SERVER_ERROR` | 10.0.1.38 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.38 (latency 112ms) |
| 2026-11-25T01:40:05 | `SERVER_ERROR` | 10.0.3.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.24 (latency 19ms) |
| 2026-11-25T01:40:10 | `SERVER_ERROR` | 10.0.3.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.20 (latency 64ms) |
| 2026-11-25T01:40:11 | `SERVER_ERROR` | 10.0.2.18 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.18 (latency 78ms) |
| 2026-11-25T01:40:15 | `SERVER_ERROR` | 10.0.1.19 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.19 (latency 76ms) |
| 2026-11-25T01:40:17 | `SERVER_ERROR` | 10.0.3.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.17 (latency 13ms) |
| 2026-11-25T01:40:20 | `SERVER_ERROR` | 10.0.3.35 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.35 (latency 114ms) |
| 2026-11-25T01:40:30 | `SERVER_ERROR` | 10.0.1.11 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.11 (latency 73ms) |
| 2026-11-25T01:40:33 | `SERVER_ERROR` | 10.0.4.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.33 (latency 70ms) |
| 2026-11-25T01:40:36 | `NEW_IP` | 10.0.2.16 | 1 | New client IP detected: 10.0.2.16 |
| 2026-11-25T01:40:36 | `SERVER_ERROR` | 10.0.2.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.16 (latency 119ms) |
| 2026-11-25T01:40:44 | `SERVER_ERROR` | 10.0.2.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.30 (latency 62ms) |
| 2026-11-25T01:40:47 | `SERVER_ERROR` | 10.0.2.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.8 (latency 108ms) |
| 2026-11-25T01:40:49 | `SERVER_ERROR` | 10.0.3.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.24 (latency 93ms) |
| 2026-11-25T01:40:58 | `SERVER_ERROR` | 10.0.2.46 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.46 (latency 103ms) |
| 2026-11-25T01:41:00 | `SERVER_ERROR` | 10.0.4.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.22 (latency 38ms) |
| 2026-11-25T01:41:17 | `SERVER_ERROR` | 10.0.4.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.41 (latency 45ms) |
| 2026-11-25T01:41:25 | `SERVER_ERROR` | 10.0.1.31 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.31 (latency 62ms) |
| 2026-11-25T01:41:28 | `SERVER_ERROR` | 10.0.2.46 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.46 (latency 110ms) |
| 2026-11-25T01:41:46 | `SERVER_ERROR` | 10.0.2.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.16 (latency 46ms) |
| 2026-11-25T01:41:48 | `NEW_IP` | 10.0.2.30 | 1 | New client IP detected: 10.0.2.30 |
| 2026-11-25T01:41:52 | `SERVER_ERROR` | 10.0.4.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.27 (latency 45ms) |
| 2026-11-25T01:42:01 | `SERVER_ERROR` | 10.0.2.19 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.19 (latency 34ms) |
| 2026-11-25T01:42:04 | `SERVER_ERROR` | 10.0.1.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.2 (latency 18ms) |
| 2026-11-25T01:42:06 | `SERVER_ERROR` | 10.0.1.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.6 (latency 32ms) |
| 2026-11-25T01:42:20 | `SERVER_ERROR` | 10.0.3.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.33 (latency 114ms) |
| 2026-11-25T01:42:26 | `SERVER_ERROR` | 10.0.2.19 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.19 (latency 85ms) |
| 2026-11-25T01:42:29 | `SERVER_ERROR` | 10.0.2.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.44 (latency 70ms) |
| 2026-11-25T01:42:32 | `NEW_IP` | 10.0.4.23 | 1 | New client IP detected: 10.0.4.23 |
| 2026-11-25T01:42:35 | `SERVER_ERROR` | 10.0.1.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.15 (latency 36ms) |
| 2026-11-25T01:42:39 | `SERVER_ERROR` | 10.0.3.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.17 (latency 109ms) |
| 2026-11-25T01:42:40 | `SERVER_ERROR` | 10.0.1.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.12 (latency 54ms) |
| 2026-11-25T01:42:42 | `SERVER_ERROR` | 10.0.1.11 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.11 (latency 16ms) |
| 2026-11-25T01:42:45 | `SERVER_ERROR` | 10.0.4.19 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.19 (latency 85ms) |
| 2026-11-25T01:42:46 | `NEW_IP` | 10.0.1.33 | 1 | New client IP detected: 10.0.1.33 |
| 2026-11-25T01:42:46 | `SERVER_ERROR` | 10.0.1.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.33 (latency 33ms) |
| 2026-11-25T01:42:56 | `SERVER_ERROR` | 10.0.1.32 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.32 (latency 76ms) |
| 2026-11-25T01:43:04 | `SERVER_ERROR` | 10.0.2.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.22 (latency 91ms) |
| 2026-11-25T01:43:10 | `SERVER_ERROR` | 10.0.3.19 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.19 (latency 84ms) |
| 2026-11-25T01:43:12 | `SERVER_ERROR` | 10.0.2.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.15 (latency 27ms) |
| 2026-11-25T01:43:18 | `SERVER_ERROR` | 10.0.1.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.22 (latency 96ms) |
| 2026-11-25T01:43:20 | `SERVER_ERROR` | 10.0.1.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.21 (latency 34ms) |
| 2026-11-25T01:43:24 | `SERVER_ERROR` | 10.0.4.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.44 (latency 98ms) |
| 2026-11-25T01:43:25 | `SERVER_ERROR` | 10.0.2.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.39 (latency 24ms) |
| 2026-11-25T01:43:27 | `SERVER_ERROR` | 10.0.3.11 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.11 (latency 106ms) |
| 2026-11-25T01:43:28 | `SERVER_ERROR` | 10.0.1.31 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.31 (latency 47ms) |
| 2026-11-25T01:43:34 | `SERVER_ERROR` | 10.0.1.31 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.31 (latency 16ms) |
| 2026-11-25T01:43:35 | `SERVER_ERROR` | 10.0.1.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.49 (latency 26ms) |
| 2026-11-25T01:43:39 | `SERVER_ERROR` | 10.0.2.5 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.5 (latency 101ms) |
| 2026-11-25T01:43:43 | `SERVER_ERROR` | 10.0.2.28 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.28 (latency 80ms) |
| 2026-11-25T01:43:44 | `SERVER_ERROR` | 10.0.2.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.9 (latency 46ms) |
| 2026-11-25T01:43:47 | `SERVER_ERROR` | 10.0.1.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.26 (latency 54ms) |
| 2026-11-25T01:43:52 | `SERVER_ERROR` | 10.0.2.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.26 (latency 113ms) |
| 2026-11-25T01:43:53 | `SERVER_ERROR` | 10.0.2.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.3 (latency 68ms) |
| 2026-11-25T01:44:06 | `SERVER_ERROR` | 10.0.4.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.8 (latency 26ms) |
| 2026-11-25T01:44:11 | `SERVER_ERROR` | 10.0.1.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.44 (latency 33ms) |
| 2026-11-25T01:44:15 | `SERVER_ERROR` | 10.0.1.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.39 (latency 41ms) |
| 2026-11-25T01:44:16 | `SERVER_ERROR` | 10.0.3.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.45 (latency 36ms) |
| 2026-11-25T01:44:18 | `SERVER_ERROR` | 10.0.3.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.47 (latency 69ms) |
| 2026-11-25T01:44:20 | `NEW_IP` | 10.0.1.3 | 1 | New client IP detected: 10.0.1.3 |
| 2026-11-25T01:44:21 | `SERVER_ERROR` | 10.0.2.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.9 (latency 34ms) |
| 2026-11-25T01:44:23 | `SERVER_ERROR` | 10.0.2.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.40 (latency 75ms) |
| 2026-11-25T01:44:29 | `SERVER_ERROR` | 10.0.4.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.44 (latency 97ms) |
| 2026-11-25T01:44:46 | `SERVER_ERROR` | 10.0.2.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.39 (latency 86ms) |
| 2026-11-25T01:44:51 | `NEW_IP` | 10.0.4.35 | 1 | New client IP detected: 10.0.4.35 |
| 2026-11-25T01:44:52 | `SERVER_ERROR` | 10.0.1.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.33 (latency 14ms) |
| 2026-11-25T01:44:54 | `SERVER_ERROR` | 10.0.4.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.20 (latency 111ms) |
| 2026-11-25T01:44:56 | `SERVER_ERROR` | 10.0.1.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.2 (latency 13ms) |
| 2026-11-25T01:45:00 | `SERVER_ERROR` | 10.0.2.35 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.35 (latency 103ms) |
| 2026-11-25T01:45:04 | `SERVER_ERROR` | 10.0.3.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.36 (latency 52ms) |
| 2026-11-25T01:45:15 | `SERVER_ERROR` | 10.0.3.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.20 (latency 28ms) |
| 2026-11-25T01:45:21 | `SERVER_ERROR` | 10.0.3.38 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.38 (latency 102ms) |
| 2026-11-25T01:45:26 | `SERVER_ERROR` | 10.0.4.48 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.48 (latency 29ms) |
| 2026-11-25T01:45:27 | `SERVER_ERROR` | 10.0.1.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.33 (latency 85ms) |
| 2026-11-25T01:45:29 | `SERVER_ERROR` | 10.0.2.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.47 (latency 67ms) |
| 2026-11-25T01:45:35 | `SERVER_ERROR` | 10.0.3.38 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.38 (latency 16ms) |
| 2026-11-25T01:45:41 | `SERVER_ERROR` | 10.0.2.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.3 (latency 111ms) |
| 2026-11-25T01:45:49 | `NEW_IP` | 10.0.3.37 | 1 | New client IP detected: 10.0.3.37 |
| 2026-11-25T01:45:51 | `SERVER_ERROR` | 10.0.4.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.3 (latency 45ms) |
| 2026-11-25T01:45:53 | `SERVER_ERROR` | 10.0.3.1 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.1 (latency 97ms) |
| 2026-11-25T01:46:02 | `SERVER_ERROR` | 10.0.2.23 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.23 (latency 108ms) |
| 2026-11-25T01:46:07 | `SERVER_ERROR` | 10.0.1.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.22 (latency 19ms) |
| 2026-11-25T01:46:09 | `SERVER_ERROR` | 10.0.4.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.41 (latency 41ms) |
| 2026-11-25T01:46:11 | `NEW_IP` | 10.0.2.35 | 1 | New client IP detected: 10.0.2.35 |
| 2026-11-25T01:46:32 | `SERVER_ERROR` | 10.0.1.35 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.35 (latency 95ms) |
| 2026-11-25T01:46:39 | `SERVER_ERROR` | 10.0.3.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.12 (latency 80ms) |
| 2026-11-25T01:46:40 | `SERVER_ERROR` | 10.0.1.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.12 (latency 116ms) |
| 2026-11-25T01:46:47 | `SERVER_ERROR` | 10.0.2.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.9 (latency 43ms) |
| 2026-11-25T01:46:50 | `SERVER_ERROR` | 10.0.4.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.21 (latency 17ms) |
| 2026-11-25T01:47:05 | `SERVER_ERROR` | 10.0.4.19 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.19 (latency 23ms) |
| 2026-11-25T01:47:06 | `NEW_IP` | 10.0.3.47 | 1 | New client IP detected: 10.0.3.47 |
| 2026-11-25T01:47:12 | `SERVER_ERROR` | 10.0.3.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.9 (latency 83ms) |
| 2026-11-25T01:47:14 | `SERVER_ERROR` | 10.0.1.38 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.38 (latency 41ms) |
| 2026-11-25T01:47:16 | `SERVER_ERROR` | 10.0.2.32 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.32 (latency 105ms) |
| 2026-11-25T01:47:18 | `SERVER_ERROR` | 10.0.4.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.17 (latency 38ms) |
| 2026-11-25T01:47:31 | `SERVER_ERROR` | 10.0.4.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.21 (latency 113ms) |
| 2026-11-25T01:47:40 | `NEW_IP` | 10.0.3.19 | 1 | New client IP detected: 10.0.3.19 |
| 2026-11-25T01:47:41 | `SERVER_ERROR` | 10.0.3.19 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.19 (latency 49ms) |
| 2026-11-25T01:47:43 | `SERVER_ERROR` | 10.0.3.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.27 (latency 64ms) |
| 2026-11-25T01:47:53 | `SERVER_ERROR` | 10.0.3.18 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.18 (latency 109ms) |
| 2026-11-25T01:47:56 | `SERVER_ERROR` | 10.0.2.18 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.18 (latency 40ms) |
| 2026-11-25T01:47:59 | `SERVER_ERROR` | 10.0.2.18 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.18 (latency 65ms) |
| 2026-11-25T01:48:06 | `SERVER_ERROR` | 10.0.3.38 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.38 (latency 40ms) |
| 2026-11-25T01:48:10 | `SERVER_ERROR` | 10.0.2.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.45 (latency 16ms) |
| 2026-11-25T01:48:12 | `NEW_IP` | 10.0.2.12 | 1 | New client IP detected: 10.0.2.12 |
| 2026-11-25T01:48:21 | `SERVER_ERROR` | 10.0.3.14 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.14 (latency 82ms) |
| 2026-11-25T01:48:24 | `SERVER_ERROR` | 10.0.1.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.24 (latency 108ms) |
| 2026-11-25T01:48:30 | `SERVER_ERROR` | 10.0.2.38 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.38 (latency 26ms) |
| 2026-11-25T01:48:34 | `SERVER_ERROR` | 10.0.1.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.44 (latency 39ms) |
| 2026-11-25T01:48:36 | `SERVER_ERROR` | 10.0.3.1 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.1 (latency 65ms) |
| 2026-11-25T01:48:37 | `SERVER_ERROR` | 10.0.4.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.3 (latency 85ms) |
| 2026-11-25T01:48:45 | `SERVER_ERROR` | 10.0.4.1 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.1 (latency 34ms) |
| 2026-11-25T01:48:48 | `SERVER_ERROR` | 10.0.3.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.16 (latency 86ms) |
| 2026-11-25T01:48:51 | `SERVER_ERROR` | 10.0.2.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.36 (latency 12ms) |
| 2026-11-25T01:48:54 | `SERVER_ERROR` | 10.0.3.19 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.19 (latency 33ms) |
| 2026-11-25T01:49:01 | `SERVER_ERROR` | 10.0.2.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.7 (latency 82ms) |
| 2026-11-25T01:49:03 | `SERVER_ERROR` | 10.0.4.35 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.35 (latency 17ms) |
| 2026-11-25T01:49:10 | `SERVER_ERROR` | 10.0.4.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.37 (latency 37ms) |
| 2026-11-25T01:49:14 | `SERVER_ERROR` | 10.0.1.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.2 (latency 109ms) |
| 2026-11-25T01:49:27 | `SERVER_ERROR` | 10.0.1.19 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.19 (latency 113ms) |
| 2026-11-25T01:49:30 | `SERVER_ERROR` | 10.0.3.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.10 (latency 14ms) |
| 2026-11-25T01:49:39 | `NEW_IP` | 10.0.4.27 | 1 | New client IP detected: 10.0.4.27 |
| 2026-11-25T01:49:47 | `SERVER_ERROR` | 10.0.4.38 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.38 (latency 52ms) |
| 2026-11-25T01:49:48 | `SERVER_ERROR` | 10.0.2.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.37 (latency 112ms) |
| 2026-11-25T01:49:53 | `SERVER_ERROR` | 10.0.2.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.20 (latency 21ms) |
| 2026-11-25T01:50:08 | `SERVER_ERROR` | 10.0.4.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.42 (latency 96ms) |
| 2026-11-25T01:50:15 | `SERVER_ERROR` | 10.0.2.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.37 (latency 35ms) |
| 2026-11-25T01:50:18 | `NEW_IP` | 10.0.2.23 | 1 | New client IP detected: 10.0.2.23 |
| 2026-11-25T01:50:27 | `SERVER_ERROR` | 10.0.1.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.22 (latency 79ms) |
| 2026-11-25T01:50:31 | `SERVER_ERROR` | 10.0.2.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.44 (latency 45ms) |
| 2026-11-25T01:50:41 | `SERVER_ERROR` | 10.0.2.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.49 (latency 28ms) |
| 2026-11-25T01:50:44 | `NEW_IP` | 10.0.2.24 | 1 | New client IP detected: 10.0.2.24 |
| 2026-11-25T01:50:45 | `SERVER_ERROR` | 10.0.3.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.17 (latency 29ms) |
| 2026-11-25T01:50:46 | `NEW_IP` | 10.0.1.5 | 1 | New client IP detected: 10.0.1.5 |
| 2026-11-25T01:50:48 | `SERVER_ERROR` | 10.0.1.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.42 (latency 79ms) |
| 2026-11-25T01:50:54 | `NEW_IP` | 10.0.1.14 | 1 | New client IP detected: 10.0.1.14 |
| 2026-11-25T01:51:04 | `SERVER_ERROR` | 10.0.3.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.29 (latency 40ms) |
| 2026-11-25T01:51:07 | `SERVER_ERROR` | 10.0.2.38 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.38 (latency 28ms) |
| 2026-11-25T01:51:09 | `NEW_IP` | 10.0.1.16 | 1 | New client IP detected: 10.0.1.16 |
| 2026-11-25T01:51:09 | `SERVER_ERROR` | 10.0.1.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.16 (latency 59ms) |
| 2026-11-25T01:51:21 | `SERVER_ERROR` | 10.0.3.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.49 (latency 49ms) |
| 2026-11-25T01:51:22 | `SERVER_ERROR` | 10.0.4.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.49 (latency 38ms) |
| 2026-11-25T01:51:25 | `SERVER_ERROR` | 10.0.4.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.24 (latency 14ms) |
| 2026-11-25T01:51:36 | `SERVER_ERROR` | 10.0.4.11 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.11 (latency 107ms) |
| 2026-11-25T01:51:45 | `SERVER_ERROR` | 10.0.4.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.22 (latency 33ms) |
| 2026-11-25T01:51:50 | `SERVER_ERROR` | 10.0.1.31 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.31 (latency 50ms) |
| 2026-11-25T01:51:51 | `SERVER_ERROR` | 10.0.1.14 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.14 (latency 76ms) |
| 2026-11-25T01:51:54 | `SERVER_ERROR` | 10.0.3.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.8 (latency 47ms) |
| 2026-11-25T01:51:57 | `NEW_IP` | 10.0.1.41 | 1 | New client IP detected: 10.0.1.41 |
| 2026-11-25T01:51:58 | `SERVER_ERROR` | 10.0.3.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.29 (latency 25ms) |
| 2026-11-25T01:52:05 | `SERVER_ERROR` | 10.0.1.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.3 (latency 41ms) |
| 2026-11-25T01:52:10 | `SERVER_ERROR` | 10.0.4.25 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.25 (latency 112ms) |
| 2026-11-25T01:52:14 | `SERVER_ERROR` | 10.0.2.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.27 (latency 46ms) |
| 2026-11-25T01:52:16 | `SERVER_ERROR` | 10.0.4.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.22 (latency 102ms) |
| 2026-11-25T01:52:17 | `SERVER_ERROR` | 10.0.4.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.47 (latency 32ms) |
| 2026-11-25T01:52:20 | `SERVER_ERROR` | 10.0.2.32 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.32 (latency 68ms) |
| 2026-11-25T01:52:30 | `SERVER_ERROR` | 10.0.4.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.33 (latency 95ms) |
| 2026-11-25T01:52:31 | `SERVER_ERROR` | 10.0.4.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.21 (latency 107ms) |
| 2026-11-25T01:52:33 | `SERVER_ERROR` | 10.0.1.35 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.35 (latency 38ms) |
| 2026-11-25T01:52:34 | `SERVER_ERROR` | 10.0.1.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.9 (latency 59ms) |
| 2026-11-25T01:52:39 | `NEW_IP` | 10.0.4.15 | 1 | New client IP detected: 10.0.4.15 |
| 2026-11-25T01:52:39 | `SERVER_ERROR` | 10.0.4.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.15 (latency 60ms) |
| 2026-11-25T01:52:45 | `SERVER_ERROR` | 10.0.3.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.49 (latency 94ms) |
| 2026-11-25T01:52:52 | `NEW_IP` | 10.0.3.27 | 1 | New client IP detected: 10.0.3.27 |
| 2026-11-25T01:52:52 | `SERVER_ERROR` | 10.0.3.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.27 (latency 64ms) |
| 2026-11-25T01:52:54 | `SERVER_ERROR` | 10.0.2.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.41 (latency 108ms) |
| 2026-11-25T01:53:09 | `SERVER_ERROR` | 10.0.1.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.12 (latency 61ms) |
| 2026-11-25T01:53:13 | `NEW_IP` | 10.0.4.39 | 1 | New client IP detected: 10.0.4.39 |
| 2026-11-25T01:53:14 | `SERVER_ERROR` | 10.0.3.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.40 (latency 120ms) |
| 2026-11-25T01:53:18 | `SERVER_ERROR` | 10.0.4.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.29 (latency 15ms) |
| 2026-11-25T01:53:21 | `SERVER_ERROR` | 10.0.4.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.20 (latency 21ms) |
| 2026-11-25T01:53:22 | `SERVER_ERROR` | 10.0.1.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.4 (latency 58ms) |
| 2026-11-25T01:53:28 | `SERVER_ERROR` | 10.0.2.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.6 (latency 118ms) |
| 2026-11-25T01:53:30 | `NEW_IP` | 10.0.4.11 | 1 | New client IP detected: 10.0.4.11 |
| 2026-11-25T01:53:31 | `SERVER_ERROR` | 10.0.2.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.44 (latency 75ms) |
| 2026-11-25T01:53:40 | `SERVER_ERROR` | 10.0.3.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.20 (latency 43ms) |
| 2026-11-25T01:53:41 | `SERVER_ERROR` | 10.0.3.11 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.11 (latency 38ms) |
| 2026-11-25T01:53:43 | `SERVER_ERROR` | 10.0.2.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.30 (latency 89ms) |
| 2026-11-25T01:53:48 | `SERVER_ERROR` | 10.0.4.1 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.1 (latency 57ms) |
| 2026-11-25T01:53:49 | `SERVER_ERROR` | 10.0.1.31 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.31 (latency 13ms) |
| 2026-11-25T01:53:59 | `SERVER_ERROR` | 10.0.1.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.2 (latency 112ms) |
| 2026-11-25T01:54:26 | `SERVER_ERROR` | 10.0.1.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.42 (latency 72ms) |
| 2026-11-25T01:54:39 | `SERVER_ERROR` | 10.0.3.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.44 (latency 19ms) |
| 2026-11-25T01:54:43 | `NEW_IP` | 10.0.3.42 | 1 | New client IP detected: 10.0.3.42 |
| 2026-11-25T01:54:44 | `SERVER_ERROR` | 10.0.1.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.41 (latency 84ms) |
| 2026-11-25T01:54:52 | `SERVER_ERROR` | 10.0.4.23 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.23 (latency 64ms) |
| 2026-11-25T01:54:59 | `SERVER_ERROR` | 10.0.2.38 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.38 (latency 47ms) |
| 2026-11-25T01:55:02 | `SERVER_ERROR` | 10.0.2.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.29 (latency 15ms) |
| 2026-11-25T01:55:05 | `SERVER_ERROR` | 10.0.1.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.49 (latency 57ms) |
| 2026-11-25T01:55:16 | `SERVER_ERROR` | 10.0.3.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.27 (latency 10ms) |
| 2026-11-25T01:55:18 | `SERVER_ERROR` | 10.0.3.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.7 (latency 21ms) |
| 2026-11-25T01:55:23 | `SERVER_ERROR` | 10.0.3.23 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.23 (latency 97ms) |
| 2026-11-25T01:55:28 | `SERVER_ERROR` | 10.0.1.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.40 (latency 49ms) |
| 2026-11-25T01:55:32 | `SERVER_ERROR` | 10.0.3.48 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.48 (latency 106ms) |
| 2026-11-25T01:55:35 | `SERVER_ERROR` | 10.0.3.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.22 (latency 81ms) |
| 2026-11-25T01:55:41 | `SERVER_ERROR` | 10.0.1.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.41 (latency 68ms) |
| 2026-11-25T01:55:44 | `SERVER_ERROR` | 10.0.1.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.16 (latency 63ms) |
| 2026-11-25T01:55:59 | `SERVER_ERROR` | 10.0.1.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.10 (latency 67ms) |
| 2026-11-25T01:56:00 | `SERVER_ERROR` | 10.0.2.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.3 (latency 20ms) |
| 2026-11-25T01:56:05 | `SERVER_ERROR` | 10.0.1.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.45 (latency 45ms) |
| 2026-11-25T01:56:09 | `SERVER_ERROR` | 10.0.4.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.4 (latency 17ms) |
| 2026-11-25T01:56:27 | `SERVER_ERROR` | 10.0.1.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.17 (latency 38ms) |
| 2026-11-25T01:56:28 | `SERVER_ERROR` | 10.0.3.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.8 (latency 47ms) |
| 2026-11-25T01:56:29 | `NEW_IP` | 10.0.1.49 | 1 | New client IP detected: 10.0.1.49 |
| 2026-11-25T01:56:35 | `SERVER_ERROR` | 10.0.3.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.33 (latency 84ms) |
| 2026-11-25T01:56:41 | `SERVER_ERROR` | 10.0.4.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.27 (latency 54ms) |
| 2026-11-25T01:56:46 | `SERVER_ERROR` | 10.0.1.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.47 (latency 114ms) |
| 2026-11-25T01:56:50 | `NEW_IP` | 10.0.4.9 | 1 | New client IP detected: 10.0.4.9 |
| 2026-11-25T01:56:52 | `NEW_IP` | 10.0.1.6 | 1 | New client IP detected: 10.0.1.6 |
| 2026-11-25T01:56:58 | `NEW_IP` | 10.0.1.7 | 1 | New client IP detected: 10.0.1.7 |
| 2026-11-25T01:57:04 | `NEW_IP` | 10.0.2.48 | 1 | New client IP detected: 10.0.2.48 |
| 2026-11-25T01:57:09 | `SERVER_ERROR` | 10.0.2.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.29 (latency 70ms) |
| 2026-11-25T01:57:15 | `SERVER_ERROR` | 10.0.3.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.3 (latency 84ms) |
| 2026-11-25T01:57:25 | `SERVER_ERROR` | 10.0.3.23 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.23 (latency 25ms) |
| 2026-11-25T01:57:26 | `SERVER_ERROR` | 10.0.1.35 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.35 (latency 112ms) |
| 2026-11-25T01:57:28 | `SERVER_ERROR` | 10.0.3.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.16 (latency 96ms) |
| 2026-11-25T01:57:44 | `SERVER_ERROR` | 10.0.1.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.39 (latency 46ms) |
| 2026-11-25T01:57:46 | `NEW_IP` | 10.0.2.18 | 1 | New client IP detected: 10.0.2.18 |
| 2026-11-25T01:57:47 | `SERVER_ERROR` | 10.0.2.5 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.5 (latency 104ms) |
| 2026-11-25T01:57:48 | `SERVER_ERROR` | 10.0.2.28 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.28 (latency 69ms) |
| 2026-11-25T01:57:51 | `SERVER_ERROR` | 10.0.2.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.21 (latency 72ms) |
| 2026-11-25T01:57:54 | `NEW_IP` | 10.0.2.26 | 1 | New client IP detected: 10.0.2.26 |
| 2026-11-25T01:57:59 | `SERVER_ERROR` | 10.0.1.1 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.1 (latency 78ms) |
| 2026-11-25T01:58:10 | `NEW_IP` | 10.0.2.20 | 1 | New client IP detected: 10.0.2.20 |
| 2026-11-25T01:58:15 | `SERVER_ERROR` | 10.0.1.5 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.5 (latency 21ms) |
| 2026-11-25T01:58:16 | `NEW_IP` | 10.0.3.21 | 1 | New client IP detected: 10.0.3.21 |
| 2026-11-25T01:58:16 | `SERVER_ERROR` | 10.0.3.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.21 (latency 20ms) |
| 2026-11-25T01:58:20 | `SERVER_ERROR` | 10.0.4.28 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.28 (latency 60ms) |
| 2026-11-25T01:58:26 | `SERVER_ERROR` | 10.0.4.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.4 (latency 85ms) |
| 2026-11-25T01:58:28 | `NEW_IP` | 10.0.3.20 | 1 | New client IP detected: 10.0.3.20 |
| 2026-11-25T01:58:34 | `SERVER_ERROR` | 10.0.4.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.22 (latency 52ms) |
| 2026-11-25T01:58:35 | `NEW_IP` | 10.0.3.46 | 1 | New client IP detected: 10.0.3.46 |
| 2026-11-25T01:58:36 | `SERVER_ERROR` | 10.0.4.23 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.23 (latency 119ms) |
| 2026-11-25T01:58:38 | `SERVER_ERROR` | 10.0.4.14 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.14 (latency 57ms) |
| 2026-11-25T01:58:40 | `SERVER_ERROR` | 10.0.3.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.39 (latency 86ms) |
| 2026-11-25T01:58:41 | `SERVER_ERROR` | 10.0.3.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.3 (latency 30ms) |
| 2026-11-25T01:58:50 | `SERVER_ERROR` | 10.0.1.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.12 (latency 47ms) |
| 2026-11-25T01:58:56 | `SERVER_ERROR` | 10.0.2.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.44 (latency 10ms) |
| 2026-11-25T01:59:00 | `SERVER_ERROR` | 10.0.4.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.34 (latency 45ms) |
| 2026-11-25T01:59:07 | `SERVER_ERROR` | 10.0.2.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.34 (latency 93ms) |
| 2026-11-25T01:59:19 | `SERVER_ERROR` | 10.0.2.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.4 (latency 54ms) |
| 2026-11-25T01:59:20 | `NEW_IP` | 10.0.1.44 | 1 | New client IP detected: 10.0.1.44 |
| 2026-11-25T01:59:22 | `SERVER_ERROR` | 10.0.1.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.40 (latency 18ms) |
| 2026-11-25T01:59:25 | `SERVER_ERROR` | 10.0.3.23 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.23 (latency 13ms) |
| 2026-11-25T01:59:27 | `SERVER_ERROR` | 10.0.2.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.26 (latency 56ms) |
| 2026-11-25T01:59:33 | `SERVER_ERROR` | 10.0.1.19 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.19 (latency 67ms) |
| 2026-11-25T01:59:37 | `SERVER_ERROR` | 10.0.4.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.30 (latency 100ms) |
| 2026-11-25T01:59:40 | `SERVER_ERROR` | 10.0.2.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.10 (latency 15ms) |
| 2026-11-25T01:59:50 | `SERVER_ERROR` | 10.0.4.11 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.11 (latency 66ms) |
| 2026-11-25T01:59:54 | `SERVER_ERROR` | 10.0.4.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.45 (latency 20ms) |
| 2026-11-25T01:59:55 | `SERVER_ERROR` | 10.0.3.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.33 (latency 62ms) |
| 2026-11-25T02:00:04 | `SERVER_ERROR` | 10.0.3.38 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.38 (latency 70ms) |
| 2026-11-25T02:00:05 | `SERVER_ERROR` | 10.0.1.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.45 (latency 43ms) |
| 2026-11-25T02:00:12 | `SERVER_ERROR` | 10.0.4.5 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.5 (latency 67ms) |
| 2026-11-25T02:00:23 | `SERVER_ERROR` | 10.0.1.48 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.48 (latency 12ms) |
| 2026-11-25T02:00:28 | `SERVER_ERROR` | 10.0.3.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.47 (latency 75ms) |
| 2026-11-25T02:00:30 | `NEW_IP` | 10.0.1.31 | 1 | New client IP detected: 10.0.1.31 |
| 2026-11-25T02:00:31 | `SERVER_ERROR` | 10.0.3.48 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.48 (latency 108ms) |
| 2026-11-25T02:00:45 | `SERVER_ERROR` | 10.0.3.43 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.43 (latency 53ms) |
| 2026-11-25T02:00:53 | `NEW_IP` | 10.0.3.28 | 1 | New client IP detected: 10.0.3.28 |
| 2026-11-25T02:00:56 | `SERVER_ERROR` | 10.0.4.18 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.18 (latency 92ms) |
| 2026-11-25T02:01:12 | `SERVER_ERROR` | 10.0.1.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.27 (latency 102ms) |
| 2026-11-25T02:01:13 | `NEW_IP` | 10.0.3.1 | 1 | New client IP detected: 10.0.3.1 |
| 2026-11-25T02:01:26 | `SERVER_ERROR` | 10.0.1.18 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.18 (latency 52ms) |
| 2026-11-25T02:01:38 | `SERVER_ERROR` | 10.0.2.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.49 (latency 49ms) |
| 2026-11-25T02:01:45 | `SERVER_ERROR` | 10.0.2.32 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.32 (latency 77ms) |
| 2026-11-25T02:01:52 | `SERVER_ERROR` | 10.0.3.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.24 (latency 110ms) |
| 2026-11-25T02:01:53 | `SERVER_ERROR` | 10.0.2.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.4 (latency 107ms) |
| 2026-11-25T02:01:58 | `SERVER_ERROR` | 10.0.1.32 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.32 (latency 35ms) |
| 2026-11-25T02:02:00 | `SERVER_ERROR` | 10.0.1.1 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.1 (latency 40ms) |
| 2026-11-25T02:02:07 | `SERVER_ERROR` | 10.0.3.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.15 (latency 99ms) |
| 2026-11-25T02:02:16 | `NEW_IP` | 10.0.4.38 | 1 | New client IP detected: 10.0.4.38 |
| 2026-11-25T02:02:17 | `NEW_IP` | 10.0.3.4 | 1 | New client IP detected: 10.0.3.4 |
| 2026-11-25T02:02:17 | `SERVER_ERROR` | 10.0.3.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.4 (latency 45ms) |
| 2026-11-25T02:02:27 | `SERVER_ERROR` | 10.0.2.14 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.14 (latency 44ms) |
| 2026-11-25T02:02:43 | `SERVER_ERROR` | 10.0.1.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.44 (latency 18ms) |
| 2026-11-25T02:02:47 | `SERVER_ERROR` | 10.0.4.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.49 (latency 77ms) |
| 2026-11-25T02:02:49 | `SERVER_ERROR` | 10.0.2.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.30 (latency 88ms) |
| 2026-11-25T02:02:50 | `SERVER_ERROR` | 10.0.2.25 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.25 (latency 39ms) |
| 2026-11-25T02:02:52 | `SERVER_ERROR` | 10.0.2.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.42 (latency 109ms) |
| 2026-11-25T02:02:58 | `SERVER_ERROR` | 10.0.2.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.34 (latency 37ms) |
| 2026-11-25T02:03:00 | `SERVER_ERROR` | 10.0.2.35 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.35 (latency 49ms) |
| 2026-11-25T02:03:12 | `SERVER_ERROR` | 10.0.4.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.7 (latency 78ms) |
| 2026-11-25T02:03:27 | `SERVER_ERROR` | 10.0.1.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.24 (latency 58ms) |
| 2026-11-25T02:03:30 | `SERVER_ERROR` | 10.0.2.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.3 (latency 62ms) |
| 2026-11-25T02:03:31 | `SERVER_ERROR` | 10.0.2.48 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.48 (latency 100ms) |
| 2026-11-25T02:03:33 | `SERVER_ERROR` | 10.0.2.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.22 (latency 115ms) |
| 2026-11-25T02:03:39 | `SERVER_ERROR` | 10.0.2.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.15 (latency 94ms) |
| 2026-11-25T02:03:41 | `SERVER_ERROR` | 10.0.1.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.16 (latency 108ms) |
| 2026-11-25T02:03:43 | `SERVER_ERROR` | 10.0.2.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.30 (latency 96ms) |
| 2026-11-25T02:03:51 | `SERVER_ERROR` | 10.0.4.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.42 (latency 57ms) |
| 2026-11-25T02:03:54 | `SERVER_ERROR` | 10.0.1.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.9 (latency 109ms) |
| 2026-11-25T02:03:56 | `SERVER_ERROR` | 10.0.1.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.47 (latency 37ms) |
| 2026-11-25T02:03:57 | `SERVER_ERROR` | 10.0.2.43 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.43 (latency 105ms) |
| 2026-11-25T02:04:07 | `SERVER_ERROR` | 10.0.2.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.8 (latency 16ms) |
| 2026-11-25T02:04:14 | `SERVER_ERROR` | 10.0.3.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.29 (latency 67ms) |
| 2026-11-25T02:04:18 | `SERVER_ERROR` | 10.0.1.23 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.23 (latency 26ms) |
| 2026-11-25T02:04:26 | `SERVER_ERROR` | 10.0.3.14 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.14 (latency 116ms) |
| 2026-11-25T02:04:37 | `SERVER_ERROR` | 10.0.2.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.20 (latency 117ms) |
| 2026-11-25T02:04:38 | `SERVER_ERROR` | 10.0.3.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.37 (latency 113ms) |
| 2026-11-25T02:05:02 | `SERVER_ERROR` | 10.0.3.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.45 (latency 53ms) |
| 2026-11-25T02:05:06 | `SERVER_ERROR` | 10.0.4.48 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.48 (latency 48ms) |
| 2026-11-25T02:05:25 | `SERVER_ERROR` | 10.0.3.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.41 (latency 110ms) |
| 2026-11-25T02:05:47 | `SERVER_ERROR` | 10.0.3.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.39 (latency 96ms) |
| 2026-11-25T02:05:59 | `SERVER_ERROR` | 10.0.1.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.2 (latency 98ms) |
| 2026-11-25T02:06:01 | `SERVER_ERROR` | 10.0.4.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.39 (latency 111ms) |
| 2026-11-25T02:06:05 | `SERVER_ERROR` | 10.0.1.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.37 (latency 97ms) |
| 2026-11-25T02:06:06 | `SERVER_ERROR` | 10.0.1.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.42 (latency 56ms) |
| 2026-11-25T02:06:20 | `SERVER_ERROR` | 10.0.3.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.12 (latency 99ms) |
| 2026-11-25T02:06:25 | `SERVER_ERROR` | 10.0.4.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.22 (latency 30ms) |
| 2026-11-25T02:06:28 | `SERVER_ERROR` | 10.0.1.38 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.38 (latency 116ms) |
| 2026-11-25T02:06:35 | `SERVER_ERROR` | 10.0.3.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.47 (latency 117ms) |
| 2026-11-25T02:06:36 | `SERVER_ERROR` | 10.0.3.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.7 (latency 95ms) |
| 2026-11-25T02:06:41 | `SERVER_ERROR` | 10.0.3.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.33 (latency 21ms) |
| 2026-11-25T02:06:46 | `NEW_IP` | 10.0.2.45 | 1 | New client IP detected: 10.0.2.45 |
| 2026-11-25T02:06:46 | `SERVER_ERROR` | 10.0.2.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.45 (latency 12ms) |
| 2026-11-25T02:06:58 | `SERVER_ERROR` | 10.0.3.46 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.46 (latency 13ms) |
| 2026-11-25T02:07:05 | `SERVER_ERROR` | 10.0.4.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.3 (latency 22ms) |
| 2026-11-25T02:07:08 | `SERVER_ERROR` | 10.0.4.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.15 (latency 66ms) |
| 2026-11-25T02:07:11 | `SERVER_ERROR` | 10.0.1.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.44 (latency 81ms) |
| 2026-11-25T02:07:21 | `NEW_IP` | 10.0.3.6 | 1 | New client IP detected: 10.0.3.6 |
| 2026-11-25T02:07:21 | `SERVER_ERROR` | 10.0.3.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.6 (latency 42ms) |
| 2026-11-25T02:07:22 | `SERVER_ERROR` | 10.0.4.1 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.1 (latency 33ms) |
| 2026-11-25T02:07:35 | `SERVER_ERROR` | 10.0.2.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.49 (latency 59ms) |
| 2026-11-25T02:07:40 | `SERVER_ERROR` | 10.0.1.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.47 (latency 89ms) |
| 2026-11-25T02:07:46 | `SERVER_ERROR` | 10.0.4.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.22 (latency 111ms) |
| 2026-11-25T02:07:55 | `NEW_IP` | 10.0.1.34 | 1 | New client IP detected: 10.0.1.34 |
| 2026-11-25T02:07:56 | `SERVER_ERROR` | 10.0.1.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.9 (latency 38ms) |
| 2026-11-25T02:08:16 | `SERVER_ERROR` | 10.0.4.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.33 (latency 115ms) |
| 2026-11-25T02:08:21 | `SERVER_ERROR` | 10.0.4.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.4 (latency 94ms) |
| 2026-11-25T02:08:34 | `SERVER_ERROR` | 10.0.2.31 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.31 (latency 27ms) |
| 2026-11-25T02:08:45 | `SERVER_ERROR` | 10.0.3.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.40 (latency 54ms) |
| 2026-11-25T02:08:46 | `SERVER_ERROR` | 10.0.4.18 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.18 (latency 98ms) |
| 2026-11-25T02:08:49 | `SERVER_ERROR` | 10.0.1.14 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.14 (latency 35ms) |
| 2026-11-25T02:08:55 | `SERVER_ERROR` | 10.0.3.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.15 (latency 26ms) |
| 2026-11-25T02:09:10 | `SERVER_ERROR` | 10.0.3.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.7 (latency 33ms) |
| 2026-11-25T02:09:21 | `SERVER_ERROR` | 10.0.3.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.13 (latency 49ms) |
| 2026-11-25T02:09:29 | `NEW_IP` | 10.0.2.40 | 1 | New client IP detected: 10.0.2.40 |
| 2026-11-25T02:09:32 | `SERVER_ERROR` | 10.0.2.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.12 (latency 97ms) |
| 2026-11-25T02:09:34 | `SERVER_ERROR` | 10.0.2.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.17 (latency 11ms) |
| 2026-11-25T02:09:37 | `SERVER_ERROR` | 10.0.4.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.15 (latency 21ms) |
| 2026-11-25T02:09:38 | `SERVER_ERROR` | 10.0.2.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.44 (latency 101ms) |
| 2026-11-25T02:09:39 | `SERVER_ERROR` | 10.0.1.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.7 (latency 89ms) |
| 2026-11-25T02:09:42 | `SERVER_ERROR` | 10.0.2.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.9 (latency 43ms) |
| 2026-11-25T02:09:43 | `NEW_IP` | 10.0.4.12 | 1 | New client IP detected: 10.0.4.12 |
| 2026-11-25T02:09:50 | `SERVER_ERROR` | 10.0.2.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.2 (latency 33ms) |
| 2026-11-25T02:09:53 | `SERVER_ERROR` | 10.0.4.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.17 (latency 59ms) |
| 2026-11-25T02:10:02 | `SERVER_ERROR` | 10.0.1.48 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.48 (latency 79ms) |
| 2026-11-25T02:10:06 | `SERVER_ERROR` | 10.0.3.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.36 (latency 52ms) |
| 2026-11-25T02:10:08 | `SERVER_ERROR` | 10.0.4.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.15 (latency 90ms) |
| 2026-11-25T02:10:10 | `SERVER_ERROR` | 10.0.2.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.40 (latency 106ms) |
| 2026-11-25T02:10:11 | `SERVER_ERROR` | 10.0.3.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.36 (latency 20ms) |
| 2026-11-25T02:10:18 | `SERVER_ERROR` | 10.0.4.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.42 (latency 18ms) |
| 2026-11-25T02:10:20 | `SERVER_ERROR` | 10.0.4.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.29 (latency 100ms) |
| 2026-11-25T02:10:23 | `SERVER_ERROR` | 10.0.3.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.15 (latency 61ms) |
| 2026-11-25T02:10:30 | `SERVER_ERROR` | 10.0.3.5 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.5 (latency 91ms) |
| 2026-11-25T02:10:35 | `SERVER_ERROR` | 10.0.1.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.9 (latency 107ms) |
| 2026-11-25T02:10:36 | `SERVER_ERROR` | 10.0.1.35 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.35 (latency 23ms) |
| 2026-11-25T02:10:42 | `SERVER_ERROR` | 10.0.4.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.40 (latency 42ms) |
| 2026-11-25T02:10:43 | `SERVER_ERROR` | 10.0.2.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.36 (latency 25ms) |
| 2026-11-25T02:10:45 | `SERVER_ERROR` | 10.0.2.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.37 (latency 101ms) |
| 2026-11-25T02:10:59 | `SERVER_ERROR` | 10.0.4.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.40 (latency 89ms) |
| 2026-11-25T02:11:01 | `SERVER_ERROR` | 10.0.2.48 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.48 (latency 62ms) |
| 2026-11-25T02:11:06 | `SERVER_ERROR` | 10.0.2.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.22 (latency 57ms) |
| 2026-11-25T02:11:15 | `SERVER_ERROR` | 10.0.1.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.13 (latency 23ms) |
| 2026-11-25T02:11:22 | `SERVER_ERROR` | 10.0.4.23 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.23 (latency 74ms) |
| 2026-11-25T02:11:24 | `SERVER_ERROR` | 10.0.1.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.30 (latency 47ms) |
| 2026-11-25T02:11:28 | `SERVER_ERROR` | 10.0.2.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.10 (latency 31ms) |
| 2026-11-25T02:11:38 | `SERVER_ERROR` | 10.0.4.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.24 (latency 117ms) |
| 2026-11-25T02:11:44 | `SERVER_ERROR` | 10.0.2.46 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.46 (latency 36ms) |
| 2026-11-25T02:11:49 | `SERVER_ERROR` | 10.0.2.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.27 (latency 73ms) |
| 2026-11-25T02:11:54 | `SERVER_ERROR` | 10.0.1.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.4 (latency 112ms) |
| 2026-11-25T02:11:56 | `SERVER_ERROR` | 10.0.4.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.4 (latency 16ms) |
| 2026-11-25T02:11:58 | `SERVER_ERROR` | 10.0.4.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.29 (latency 120ms) |
| 2026-11-25T02:12:03 | `SERVER_ERROR` | 10.0.4.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.42 (latency 64ms) |
| 2026-11-25T02:12:05 | `SERVER_ERROR` | 10.0.4.18 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.18 (latency 55ms) |
| 2026-11-25T02:12:09 | `SERVER_ERROR` | 10.0.4.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.7 (latency 46ms) |
| 2026-11-25T02:12:22 | `SERVER_ERROR` | 10.0.3.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.39 (latency 22ms) |
| 2026-11-25T02:12:23 | `SERVER_ERROR` | 10.0.3.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.9 (latency 20ms) |
| 2026-11-25T02:12:24 | `SERVER_ERROR` | 10.0.4.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.2 (latency 106ms) |
| 2026-11-25T02:12:28 | `NEW_IP` | 10.0.3.30 | 1 | New client IP detected: 10.0.3.30 |
| 2026-11-25T02:12:36 | `SERVER_ERROR` | 10.0.4.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.36 (latency 106ms) |
| 2026-11-25T02:12:43 | `SERVER_ERROR` | 10.0.2.46 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.46 (latency 12ms) |
| 2026-11-25T02:12:48 | `SERVER_ERROR` | 10.0.4.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.4 (latency 26ms) |
| 2026-11-25T02:12:50 | `SERVER_ERROR` | 10.0.3.19 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.19 (latency 11ms) |
| 2026-11-25T02:12:52 | `SERVER_ERROR` | 10.0.2.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.8 (latency 53ms) |
| 2026-11-25T02:12:57 | `SERVER_ERROR` | 10.0.3.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.44 (latency 12ms) |
| 2026-11-25T02:12:58 | `SERVER_ERROR` | 10.0.1.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.45 (latency 73ms) |
| 2026-11-25T02:13:10 | `SERVER_ERROR` | 10.0.2.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.29 (latency 13ms) |
| 2026-11-25T02:13:21 | `SERVER_ERROR` | 10.0.4.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.41 (latency 83ms) |
| 2026-11-25T02:13:23 | `NEW_IP` | 10.0.4.31 | 1 | New client IP detected: 10.0.4.31 |
| 2026-11-25T02:13:34 | `SERVER_ERROR` | 10.0.3.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.27 (latency 90ms) |
| 2026-11-25T02:13:51 | `SERVER_ERROR` | 10.0.2.46 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.46 (latency 116ms) |
| 2026-11-25T02:13:55 | `SERVER_ERROR` | 10.0.1.25 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.25 (latency 73ms) |
| 2026-11-25T02:13:57 | `SERVER_ERROR` | 10.0.1.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.45 (latency 98ms) |
| 2026-11-25T02:14:05 | `SERVER_ERROR` | 10.0.1.19 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.19 (latency 93ms) |
| 2026-11-25T02:14:06 | `SERVER_ERROR` | 10.0.2.31 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.31 (latency 104ms) |
| 2026-11-25T02:14:08 | `SERVER_ERROR` | 10.0.3.18 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.18 (latency 89ms) |
| 2026-11-25T02:14:31 | `SERVER_ERROR` | 10.0.3.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.15 (latency 38ms) |
| 2026-11-25T02:14:33 | `SERVER_ERROR` | 10.0.1.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.4 (latency 76ms) |
| 2026-11-25T02:14:40 | `SERVER_ERROR` | 10.0.1.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.2 (latency 77ms) |
| 2026-11-25T02:14:41 | `SERVER_ERROR` | 10.0.4.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.10 (latency 112ms) |
| 2026-11-25T02:14:44 | `NEW_IP` | 10.0.1.37 | 1 | New client IP detected: 10.0.1.37 |
| 2026-11-25T02:14:48 | `SERVER_ERROR` | 10.0.4.28 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.28 (latency 117ms) |
| 2026-11-25T02:14:53 | `SERVER_ERROR` | 10.0.1.38 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.38 (latency 10ms) |
| 2026-11-25T02:15:02 | `SERVER_ERROR` | 10.0.3.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.29 (latency 110ms) |
| 2026-11-25T02:15:18 | `NEW_IP` | 10.0.1.18 | 1 | New client IP detected: 10.0.1.18 |
| 2026-11-25T02:15:18 | `SERVER_ERROR` | 10.0.1.18 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.18 (latency 37ms) |
| 2026-11-25T02:15:19 | `SERVER_ERROR` | 10.0.4.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.40 (latency 98ms) |
| 2026-11-25T02:15:31 | `SERVER_ERROR` | 10.0.4.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.39 (latency 63ms) |
| 2026-11-25T02:15:35 | `SERVER_ERROR` | 10.0.4.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.8 (latency 42ms) |
| 2026-11-25T02:15:58 | `SERVER_ERROR` | 10.0.1.31 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.31 (latency 116ms) |
| 2026-11-25T02:16:02 | `SERVER_ERROR` | 10.0.4.1 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.1 (latency 83ms) |
| 2026-11-25T02:16:12 | `SERVER_ERROR` | 10.0.1.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.33 (latency 74ms) |
| 2026-11-25T02:16:24 | `SERVER_ERROR` | 10.0.3.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.37 (latency 118ms) |
| 2026-11-25T02:16:34 | `SERVER_ERROR` | 10.0.2.14 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.14 (latency 52ms) |
| 2026-11-25T02:16:35 | `NEW_IP` | 10.0.3.35 | 1 | New client IP detected: 10.0.3.35 |
| 2026-11-25T02:16:38 | `SERVER_ERROR` | 10.0.2.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.4 (latency 86ms) |
| 2026-11-25T02:16:53 | `SERVER_ERROR` | 10.0.1.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.17 (latency 111ms) |
| 2026-11-25T02:16:54 | `NEW_IP` | 10.0.2.38 | 1 | New client IP detected: 10.0.2.38 |
| 2026-11-25T02:17:06 | `SERVER_ERROR` | 10.0.1.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.29 (latency 17ms) |
| 2026-11-25T02:17:16 | `SERVER_ERROR` | 10.0.2.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.6 (latency 117ms) |
| 2026-11-25T02:17:22 | `SERVER_ERROR` | 10.0.3.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.26 (latency 120ms) |
| 2026-11-25T02:17:28 | `SERVER_ERROR` | 10.0.1.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.22 (latency 25ms) |
| 2026-11-25T02:17:30 | `SERVER_ERROR` | 10.0.3.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.30 (latency 51ms) |
| 2026-11-25T02:17:35 | `SERVER_ERROR` | 10.0.3.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.13 (latency 58ms) |
| 2026-11-25T02:17:45 | `SERVER_ERROR` | 10.0.2.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.7 (latency 87ms) |
| 2026-11-25T02:17:46 | `SERVER_ERROR` | 10.0.4.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.49 (latency 68ms) |
| 2026-11-25T02:17:50 | `SERVER_ERROR` | 10.0.1.14 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.14 (latency 107ms) |
| 2026-11-25T02:17:59 | `SERVER_ERROR` | 10.0.2.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.12 (latency 53ms) |
| 2026-11-25T02:18:08 | `SERVER_ERROR` | 10.0.1.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.39 (latency 110ms) |
| 2026-11-25T02:18:22 | `SERVER_ERROR` | 10.0.1.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.20 (latency 51ms) |
| 2026-11-25T02:18:24 | `SERVER_ERROR` | 10.0.4.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.20 (latency 88ms) |
| 2026-11-25T02:18:47 | `NEW_IP` | 10.0.4.1 | 1 | New client IP detected: 10.0.4.1 |
| 2026-11-25T02:18:49 | `SERVER_ERROR` | 10.0.3.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.16 (latency 84ms) |
| 2026-11-25T02:18:51 | `SERVER_ERROR` | 10.0.4.11 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.11 (latency 66ms) |
| 2026-11-25T02:18:55 | `SERVER_ERROR` | 10.0.4.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.36 (latency 84ms) |
| 2026-11-25T02:19:03 | `SERVER_ERROR` | 10.0.3.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.6 (latency 75ms) |
| 2026-11-25T02:19:06 | `SERVER_ERROR` | 10.0.2.38 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.38 (latency 102ms) |
| 2026-11-25T02:19:18 | `SERVER_ERROR` | 10.0.2.32 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.32 (latency 105ms) |
| 2026-11-25T02:19:20 | `SERVER_ERROR` | 10.0.3.44 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.44 (latency 120ms) |
| 2026-11-25T02:19:23 | `SERVER_ERROR` | 10.0.3.6 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.6 (latency 78ms) |
| 2026-11-25T02:19:24 | `SERVER_ERROR` | 10.0.4.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.41 (latency 102ms) |
| 2026-11-25T02:19:31 | `SERVER_ERROR` | 10.0.2.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.37 (latency 63ms) |
| 2026-11-25T02:19:32 | `SERVER_ERROR` | 10.0.3.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.42 (latency 27ms) |
| 2026-11-25T02:19:36 | `SERVER_ERROR` | 10.0.3.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.49 (latency 94ms) |
| 2026-11-25T02:19:50 | `SERVER_ERROR` | 10.0.1.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.20 (latency 104ms) |
| 2026-11-25T02:19:52 | `SERVER_ERROR` | 10.0.3.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.21 (latency 25ms) |
| 2026-11-25T02:19:53 | `SERVER_ERROR` | 10.0.2.28 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.28 (latency 41ms) |
| 2026-11-25T02:19:58 | `SERVER_ERROR` | 10.0.3.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.24 (latency 73ms) |
| 2026-11-25T02:20:00 | `SERVER_ERROR` | 10.0.2.18 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.18 (latency 23ms) |
| 2026-11-25T02:20:01 | `SERVER_ERROR` | 10.0.3.46 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.46 (latency 10ms) |
| 2026-11-25T02:20:09 | `SERVER_ERROR` | 10.0.1.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.4 (latency 10ms) |
| 2026-11-25T02:20:16 | `NEW_IP` | 10.0.1.43 | 1 | New client IP detected: 10.0.1.43 |
| 2026-11-25T02:20:19 | `NEW_IP` | 10.0.4.29 | 1 | New client IP detected: 10.0.4.29 |
| 2026-11-25T02:20:19 | `SERVER_ERROR` | 10.0.4.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.29 (latency 85ms) |
| 2026-11-25T02:20:23 | `SERVER_ERROR` | 10.0.3.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.21 (latency 52ms) |
| 2026-11-25T02:20:31 | `SERVER_ERROR` | 10.0.1.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.29 (latency 53ms) |
| 2026-11-25T02:20:33 | `SERVER_ERROR` | 10.0.4.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.20 (latency 66ms) |
| 2026-11-25T02:20:57 | `SERVER_ERROR` | 10.0.1.43 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.43 (latency 70ms) |
| 2026-11-25T02:20:58 | `SERVER_ERROR` | 10.0.4.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.30 (latency 46ms) |
| 2026-11-25T02:21:07 | `SERVER_ERROR` | 10.0.3.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.7 (latency 118ms) |
| 2026-11-25T02:21:13 | `SERVER_ERROR` | 10.0.1.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.22 (latency 20ms) |
| 2026-11-25T02:21:17 | `SERVER_ERROR` | 10.0.3.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.2 (latency 100ms) |
| 2026-11-25T02:21:18 | `SERVER_ERROR` | 10.0.3.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.27 (latency 50ms) |
| 2026-11-25T02:21:37 | `SERVER_ERROR` | 10.0.1.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.7 (latency 10ms) |
| 2026-11-25T02:21:46 | `SERVER_ERROR` | 10.0.2.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.16 (latency 92ms) |
| 2026-11-25T02:21:58 | `SERVER_ERROR` | 10.0.3.14 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.14 (latency 17ms) |
| 2026-11-25T02:22:02 | `SERVER_ERROR` | 10.0.4.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.21 (latency 115ms) |
| 2026-11-25T02:22:11 | `SERVER_ERROR` | 10.0.3.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.21 (latency 95ms) |
| 2026-11-25T02:22:19 | `SERVER_ERROR` | 10.0.3.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.47 (latency 13ms) |
| 2026-11-25T02:22:25 | `NEW_IP` | 10.0.4.3 | 1 | New client IP detected: 10.0.4.3 |
| 2026-11-25T02:22:34 | `SERVER_ERROR` | 10.0.3.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.9 (latency 104ms) |
| 2026-11-25T02:22:42 | `SERVER_ERROR` | 10.0.4.28 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.28 (latency 91ms) |
| 2026-11-25T02:22:48 | `NEW_IP` | 10.0.1.45 | 1 | New client IP detected: 10.0.1.45 |
| 2026-11-25T02:22:51 | `NEW_IP` | 10.0.1.32 | 1 | New client IP detected: 10.0.1.32 |
| 2026-11-25T02:22:52 | `SERVER_ERROR` | 10.0.2.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.41 (latency 107ms) |
| 2026-11-25T02:22:54 | `SERVER_ERROR` | 10.0.1.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.29 (latency 51ms) |
| 2026-11-25T02:22:57 | `SERVER_ERROR` | 10.0.2.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.12 (latency 120ms) |
| 2026-11-25T02:23:10 | `SERVER_ERROR` | 10.0.4.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.13 (latency 98ms) |
| 2026-11-25T02:23:15 | `SERVER_ERROR` | 10.0.2.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.9 (latency 14ms) |
| 2026-11-25T02:23:20 | `SERVER_ERROR` | 10.0.1.14 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.14 (latency 67ms) |
| 2026-11-25T02:23:23 | `SERVER_ERROR` | 10.0.3.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.40 (latency 29ms) |
| 2026-11-25T02:23:27 | `SERVER_ERROR` | 10.0.4.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.24 (latency 21ms) |
| 2026-11-25T02:23:33 | `SERVER_ERROR` | 10.0.1.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.2 (latency 26ms) |
| 2026-11-25T02:23:40 | `NEW_IP` | 10.0.2.46 | 1 | New client IP detected: 10.0.2.46 |
| 2026-11-25T02:23:40 | `SERVER_ERROR` | 10.0.2.46 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.46 (latency 25ms) |
| 2026-11-25T02:23:41 | `NEW_IP` | 10.0.3.26 | 1 | New client IP detected: 10.0.3.26 |
| 2026-11-25T02:23:43 | `SERVER_ERROR` | 10.0.3.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.34 (latency 82ms) |
| 2026-11-25T02:23:46 | `SERVER_ERROR` | 10.0.1.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.17 (latency 15ms) |
| 2026-11-25T02:23:58 | `NEW_IP` | 10.0.2.8 | 1 | New client IP detected: 10.0.2.8 |
| 2026-11-25T02:23:58 | `SERVER_ERROR` | 10.0.2.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.8 (latency 63ms) |
| 2026-11-25T02:24:07 | `SERVER_ERROR` | 10.0.3.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.2 (latency 80ms) |
| 2026-11-25T02:24:11 | `NEW_IP` | 10.0.1.9 | 1 | New client IP detected: 10.0.1.9 |
| 2026-11-25T02:24:21 | `SERVER_ERROR` | 10.0.2.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.42 (latency 98ms) |
| 2026-11-25T02:24:29 | `SERVER_ERROR` | 10.0.3.38 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.38 (latency 93ms) |
| 2026-11-25T02:24:42 | `NEW_IP` | 10.0.1.24 | 1 | New client IP detected: 10.0.1.24 |
| 2026-11-25T02:24:52 | `SERVER_ERROR` | 10.0.1.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.7 (latency 117ms) |
| 2026-11-25T02:24:56 | `SERVER_ERROR` | 10.0.2.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.16 (latency 19ms) |
| 2026-11-25T02:25:10 | `SERVER_ERROR` | 10.0.4.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.13 (latency 73ms) |
| 2026-11-25T02:25:23 | `SERVER_ERROR` | 10.0.1.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.42 (latency 107ms) |
| 2026-11-25T02:25:28 | `SERVER_ERROR` | 10.0.1.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.37 (latency 50ms) |
| 2026-11-25T02:25:32 | `SERVER_ERROR` | 10.0.3.43 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.43 (latency 19ms) |
| 2026-11-25T02:25:47 | `SERVER_ERROR` | 10.0.1.48 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.48 (latency 13ms) |
| 2026-11-25T02:25:55 | `SERVER_ERROR` | 10.0.2.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.15 (latency 94ms) |
| 2026-11-25T02:25:56 | `SERVER_ERROR` | 10.0.1.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.40 (latency 88ms) |
| 2026-11-25T02:26:03 | `SERVER_ERROR` | 10.0.3.5 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.5 (latency 120ms) |
| 2026-11-25T02:26:04 | `SERVER_ERROR` | 10.0.4.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.45 (latency 120ms) |
| 2026-11-25T02:26:10 | `SERVER_ERROR` | 10.0.2.11 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.11 (latency 34ms) |
| 2026-11-25T02:26:11 | `NEW_IP` | 10.0.1.39 | 1 | New client IP detected: 10.0.1.39 |
| 2026-11-25T02:26:14 | `SERVER_ERROR` | 10.0.3.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.49 (latency 41ms) |
| 2026-11-25T02:26:20 | `SERVER_ERROR` | 10.0.3.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.37 (latency 104ms) |
| 2026-11-25T02:26:22 | `SERVER_ERROR` | 10.0.1.25 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.25 (latency 49ms) |
| 2026-11-25T02:26:23 | `SERVER_ERROR` | 10.0.3.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.29 (latency 45ms) |
| 2026-11-25T02:26:25 | `SERVER_ERROR` | 10.0.1.14 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.14 (latency 91ms) |
| 2026-11-25T02:26:41 | `SERVER_ERROR` | 10.0.1.1 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.1 (latency 91ms) |
| 2026-11-25T02:26:51 | `SERVER_ERROR` | 10.0.3.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.9 (latency 103ms) |
| 2026-11-25T02:27:06 | `NEW_IP` | 10.0.4.43 | 1 | New client IP detected: 10.0.4.43 |
| 2026-11-25T02:27:14 | `SERVER_ERROR` | 10.0.2.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.12 (latency 35ms) |
| 2026-11-25T02:27:15 | `SERVER_ERROR` | 10.0.1.11 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.11 (latency 47ms) |
| 2026-11-25T02:27:16 | `SERVER_ERROR` | 10.0.3.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.29 (latency 72ms) |
| 2026-11-25T02:27:23 | `SERVER_ERROR` | 10.0.4.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.37 (latency 23ms) |
| 2026-11-25T02:27:29 | `SERVER_ERROR` | 10.0.1.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.49 (latency 99ms) |
| 2026-11-25T02:27:34 | `SERVER_ERROR` | 10.0.1.43 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.43 (latency 105ms) |
| 2026-11-25T02:27:36 | `SERVER_ERROR` | 10.0.1.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.2 (latency 90ms) |
| 2026-11-25T02:27:37 | `SERVER_ERROR` | 10.0.4.14 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.14 (latency 76ms) |
| 2026-11-25T02:27:41 | `SERVER_ERROR` | 10.0.3.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.34 (latency 114ms) |
| 2026-11-25T02:27:48 | `SERVER_ERROR` | 10.0.3.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.30 (latency 34ms) |
| 2026-11-25T02:27:59 | `SERVER_ERROR` | 10.0.2.41 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.41 (latency 93ms) |
| 2026-11-25T02:28:08 | `SERVER_ERROR` | 10.0.3.18 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.18 (latency 108ms) |
| 2026-11-25T02:28:17 | `SERVER_ERROR` | 10.0.2.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.3 (latency 13ms) |
| 2026-11-25T02:28:19 | `SERVER_ERROR` | 10.0.4.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.33 (latency 112ms) |
| 2026-11-25T02:28:20 | `SERVER_ERROR` | 10.0.4.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.36 (latency 25ms) |
| 2026-11-25T02:28:24 | `NEW_IP` | 10.0.3.45 | 1 | New client IP detected: 10.0.3.45 |
| 2026-11-25T02:28:27 | `SERVER_ERROR` | 10.0.2.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.42 (latency 78ms) |
| 2026-11-25T02:28:31 | `SERVER_ERROR` | 10.0.1.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.24 (latency 55ms) |
| 2026-11-25T02:28:34 | `NEW_IP` | 10.0.1.26 | 1 | New client IP detected: 10.0.1.26 |
| 2026-11-25T02:28:37 | `SERVER_ERROR` | 10.0.3.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.33 (latency 89ms) |
| 2026-11-25T02:28:39 | `SERVER_ERROR` | 10.0.1.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.8 (latency 40ms) |
| 2026-11-25T02:28:40 | `SERVER_ERROR` | 10.0.4.25 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.25 (latency 105ms) |
| 2026-11-25T02:28:41 | `SERVER_ERROR` | 10.0.3.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.34 (latency 40ms) |
| 2026-11-25T02:28:52 | `SERVER_ERROR` | 10.0.3.7 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.7 (latency 10ms) |
| 2026-11-25T02:28:59 | `SERVER_ERROR` | 10.0.2.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.10 (latency 65ms) |
| 2026-11-25T02:29:03 | `SERVER_ERROR` | 10.0.1.31 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.31 (latency 56ms) |
| 2026-11-25T02:29:15 | `SERVER_ERROR` | 10.0.4.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.33 (latency 47ms) |
| 2026-11-25T02:29:17 | `SERVER_ERROR` | 10.0.4.46 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.46 (latency 104ms) |
| 2026-11-25T02:29:19 | `SERVER_ERROR` | 10.0.3.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.4 (latency 39ms) |
| 2026-11-25T02:29:23 | `SERVER_ERROR` | 10.0.2.49 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.49 (latency 118ms) |
| 2026-11-25T02:29:27 | `SERVER_ERROR` | 10.0.1.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.42 (latency 67ms) |
| 2026-11-25T02:29:28 | `SERVER_ERROR` | 10.0.1.24 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.24 (latency 53ms) |
| 2026-11-25T02:29:31 | `SERVER_ERROR` | 10.0.2.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.22 (latency 106ms) |
| 2026-11-25T02:29:37 | `SERVER_ERROR` | 10.0.1.31 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.31 (latency 27ms) |
| 2026-11-25T02:29:47 | `SERVER_ERROR` | 10.0.3.23 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.23 (latency 44ms) |
| 2026-11-25T02:29:54 | `NEW_IP` | 10.0.4.2 | 1 | New client IP detected: 10.0.4.2 |
| 2026-11-25T02:29:54 | `SERVER_ERROR` | 10.0.4.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.2 (latency 39ms) |
| 2026-11-25T02:30:00 | `SERVER_ERROR` | 10.0.3.11 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.11 (latency 56ms) |
| 2026-11-25T02:30:01 | `SERVER_ERROR` | 10.0.1.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.12 (latency 66ms) |
| 2026-11-25T02:30:14 | `SERVER_ERROR` | 10.0.2.32 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.32 (latency 84ms) |
| 2026-11-25T02:30:20 | `SERVER_ERROR` | 10.0.1.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.27 (latency 92ms) |
| 2026-11-25T02:30:23 | `SERVER_ERROR` | 10.0.2.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.4 (latency 44ms) |
| 2026-11-25T02:30:25 | `SERVER_ERROR` | 10.0.4.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.33 (latency 30ms) |
| 2026-11-25T02:30:38 | `SERVER_ERROR` | 10.0.1.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.4 (latency 75ms) |
| 2026-11-25T02:30:47 | `SERVER_ERROR` | 10.0.2.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.13 (latency 90ms) |
| 2026-11-25T02:30:52 | `SERVER_ERROR` | 10.0.3.33 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.33 (latency 75ms) |
| 2026-11-25T02:31:04 | `SERVER_ERROR` | 10.0.2.48 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.48 (latency 44ms) |
| 2026-11-25T02:31:05 | `SERVER_ERROR` | 10.0.2.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.21 (latency 68ms) |
| 2026-11-25T02:31:11 | `SERVER_ERROR` | 10.0.4.11 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.11 (latency 116ms) |
| 2026-11-25T02:31:18 | `SERVER_ERROR` | 10.0.3.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.4 (latency 40ms) |
| 2026-11-25T02:31:22 | `SERVER_ERROR` | 10.0.1.28 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.28 (latency 43ms) |
| 2026-11-25T02:31:39 | `SERVER_ERROR` | 10.0.3.43 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.43 (latency 116ms) |
| 2026-11-25T02:31:40 | `SERVER_ERROR` | 10.0.3.40 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.40 (latency 24ms) |
| 2026-11-25T02:31:46 | `SERVER_ERROR` | 10.0.3.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.17 (latency 105ms) |
| 2026-11-25T02:31:52 | `SERVER_ERROR` | 10.0.4.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.39 (latency 97ms) |
| 2026-11-25T02:31:54 | `SERVER_ERROR` | 10.0.1.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.37 (latency 68ms) |
| 2026-11-25T02:31:59 | `SERVER_ERROR` | 10.0.1.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.22 (latency 85ms) |
| 2026-11-25T02:32:14 | `SERVER_ERROR` | 10.0.4.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.15 (latency 11ms) |
| 2026-11-25T02:32:20 | `NEW_IP` | 10.0.3.7 | 1 | New client IP detected: 10.0.3.7 |
| 2026-11-25T02:32:27 | `SERVER_ERROR` | 10.0.1.23 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.23 (latency 106ms) |
| 2026-11-25T02:32:31 | `SERVER_ERROR` | 10.0.1.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.36 (latency 113ms) |
| 2026-11-25T02:32:33 | `SERVER_ERROR` | 10.0.1.25 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.25 (latency 86ms) |
| 2026-11-25T02:32:34 | `SERVER_ERROR` | 10.0.3.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.15 (latency 94ms) |
| 2026-11-25T02:32:39 | `SERVER_ERROR` | 10.0.4.20 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.20 (latency 73ms) |
| 2026-11-25T02:32:46 | `SERVER_ERROR` | 10.0.3.2 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.2 (latency 101ms) |
| 2026-11-25T02:32:50 | `SERVER_ERROR` | 10.0.2.39 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.39 (latency 110ms) |
| 2026-11-25T02:32:54 | `NEW_IP` | 10.0.4.30 | 1 | New client IP detected: 10.0.4.30 |
| 2026-11-25T02:33:00 | `SERVER_ERROR` | 10.0.3.19 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.19 (latency 62ms) |
| 2026-11-25T02:33:06 | `SERVER_ERROR` | 10.0.4.12 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.12 (latency 114ms) |
| 2026-11-25T02:33:12 | `NEW_IP` | 10.0.1.27 | 1 | New client IP detected: 10.0.1.27 |
| 2026-11-25T02:33:21 | `SERVER_ERROR` | 10.0.4.19 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.19 (latency 61ms) |
| 2026-11-25T02:33:22 | `SERVER_ERROR` | 10.0.2.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.16 (latency 33ms) |
| 2026-11-25T02:33:38 | `SERVER_ERROR` | 10.0.2.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.3 (latency 31ms) |
| 2026-11-25T02:33:41 | `SERVER_ERROR` | 10.0.1.1 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.1 (latency 24ms) |
| 2026-11-25T02:33:46 | `SERVER_ERROR` | 10.0.4.28 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.28 (latency 54ms) |
| 2026-11-25T02:33:48 | `SERVER_ERROR` | 10.0.4.14 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.14 (latency 105ms) |
| 2026-11-25T02:34:12 | `SERVER_ERROR` | 10.0.2.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.37 (latency 96ms) |
| 2026-11-25T02:34:20 | `SERVER_ERROR` | 10.0.4.32 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.32 (latency 69ms) |
| 2026-11-25T02:34:26 | `SERVER_ERROR` | 10.0.1.14 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.14 (latency 90ms) |
| 2026-11-25T02:34:32 | `SERVER_ERROR` | 10.0.2.43 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.43 (latency 13ms) |
| 2026-11-25T02:34:39 | `SERVER_ERROR` | 10.0.2.4 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.4 (latency 116ms) |
| 2026-11-25T02:34:44 | `SERVER_ERROR` | 10.0.1.11 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.11 (latency 83ms) |
| 2026-11-25T02:34:51 | `SERVER_ERROR` | 10.0.2.25 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.25 (latency 100ms) |
| 2026-11-25T02:34:55 | `SERVER_ERROR` | 10.0.3.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.17 (latency 58ms) |
| 2026-11-25T02:35:01 | `SERVER_ERROR` | 10.0.1.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.16 (latency 86ms) |
| 2026-11-25T02:35:08 | `NEW_IP` | 10.0.4.16 | 1 | New client IP detected: 10.0.4.16 |
| 2026-11-25T02:35:10 | `SERVER_ERROR` | 10.0.3.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.27 (latency 79ms) |
| 2026-11-25T02:35:14 | `SERVER_ERROR` | 10.0.2.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.26 (latency 82ms) |
| 2026-11-25T02:35:17 | `SERVER_ERROR` | 10.0.2.25 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.25 (latency 78ms) |
| 2026-11-25T02:35:18 | `NEW_IP` | 10.0.2.11 | 1 | New client IP detected: 10.0.2.11 |
| 2026-11-25T02:35:21 | `SERVER_ERROR` | 10.0.2.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.34 (latency 114ms) |
| 2026-11-25T02:35:27 | `SERVER_ERROR` | 10.0.3.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.26 (latency 84ms) |
| 2026-11-25T02:35:32 | `SERVER_ERROR` | 10.0.3.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.21 (latency 105ms) |
| 2026-11-25T02:35:36 | `SERVER_ERROR` | 10.0.4.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.30 (latency 48ms) |
| 2026-11-25T02:35:40 | `SERVER_ERROR` | 10.0.4.31 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.31 (latency 102ms) |
| 2026-11-25T02:35:43 | `SERVER_ERROR` | 10.0.3.36 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.36 (latency 40ms) |
| 2026-11-25T02:35:47 | `SERVER_ERROR` | 10.0.1.23 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.23 (latency 11ms) |
| 2026-11-25T02:35:55 | `SERVER_ERROR` | 10.0.4.27 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.27 (latency 55ms) |
| 2026-11-25T02:36:08 | `SERVER_ERROR` | 10.0.4.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.47 (latency 49ms) |
| 2026-11-25T02:36:10 | `SERVER_ERROR` | 10.0.1.26 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.26 (latency 20ms) |
| 2026-11-25T02:36:16 | `SERVER_ERROR` | 10.0.1.8 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.8 (latency 19ms) |
| 2026-11-25T02:36:20 | `NEW_IP` | 10.0.4.47 | 1 | New client IP detected: 10.0.4.47 |
| 2026-11-25T02:36:23 | `SERVER_ERROR` | 10.0.3.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.17 (latency 46ms) |
| 2026-11-25T02:36:45 | `SERVER_ERROR` | 10.0.4.29 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.29 (latency 21ms) |
| 2026-11-25T02:36:47 | `SERVER_ERROR` | 10.0.4.1 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.1 (latency 12ms) |
| 2026-11-25T02:36:51 | `SERVER_ERROR` | 10.0.2.42 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.42 (latency 63ms) |
| 2026-11-25T02:36:58 | `SERVER_ERROR` | 10.0.1.43 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.43 (latency 69ms) |
| 2026-11-25T02:36:59 | `SERVER_ERROR` | 10.0.4.10 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.10 (latency 42ms) |
| 2026-11-25T02:37:05 | `SERVER_ERROR` | 10.0.3.9 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.9 (latency 83ms) |
| 2026-11-25T02:37:10 | `SERVER_ERROR` | 10.0.2.1 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.1 (latency 20ms) |
| 2026-11-25T02:37:12 | `SERVER_ERROR` | 10.0.4.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.3 (latency 107ms) |
| 2026-11-25T02:37:14 | `SERVER_ERROR` | 10.0.1.30 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.30 (latency 84ms) |
| 2026-11-25T02:37:17 | `SERVER_ERROR` | 10.0.3.3 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.3 (latency 29ms) |
| 2026-11-25T02:37:22 | `SERVER_ERROR` | 10.0.4.47 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.47 (latency 62ms) |
| 2026-11-25T02:37:28 | `SERVER_ERROR` | 10.0.1.15 | 500 | HTTP 500 on GET /api/x from IP 10.0.1.15 (latency 49ms) |
| 2026-11-25T02:37:30 | `SERVER_ERROR` | 10.0.4.22 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.22 (latency 110ms) |
| 2026-11-25T02:37:38 | `SERVER_ERROR` | 10.0.3.13 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.13 (latency 52ms) |
| 2026-11-25T02:37:44 | `SERVER_ERROR` | 10.0.4.17 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.17 (latency 21ms) |
| 2026-11-25T02:37:48 | `SERVER_ERROR` | 10.0.2.21 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.21 (latency 43ms) |
| 2026-11-25T02:37:51 | `SERVER_ERROR` | 10.0.3.34 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.34 (latency 53ms) |
| 2026-11-25T02:37:52 | `SERVER_ERROR` | 10.0.2.45 | 500 | HTTP 500 on GET /api/x from IP 10.0.2.45 (latency 50ms) |
| 2026-11-25T02:37:56 | `SERVER_ERROR` | 10.0.4.46 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.46 (latency 50ms) |
| 2026-11-25T02:37:59 | `SERVER_ERROR` | 10.0.3.16 | 500 | HTTP 500 on GET /api/x from IP 10.0.3.16 (latency 20ms) |
| 2026-11-25T02:38:12 | `SERVER_ERROR` | 10.0.4.37 | 500 | HTTP 500 on GET /api/x from IP 10.0.4.37 (latency 41ms) |
