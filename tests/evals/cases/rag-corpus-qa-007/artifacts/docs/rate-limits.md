# API Rate Limits

Limits are per minute, per API key:

| Tier | Requests/min |
|---|---|
| Free | 60 |
| Pro | 1000 |
| Enterprise | 10000 |

Bursts above the limit return HTTP 429 with a Retry-After header.
