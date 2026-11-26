import re
from collections import defaultdict
import statistics
import csv

LOG_PATH = "logs/app.log"
TIMELINE_PATH = "timeline.md"
ANOMALIES_PATH = "anomalies.csv"

# Regex pattern for log lines:
# 2026-11-25T01:52:52 10.0.3.27 GET /api/x 500 64ms
log_pattern = re.compile(
    r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})\s+(\S+)\s+(\S+)\s+(\S+)\s+(\d+)\s+(\d+)ms$'
)

def percentile(vals, p):
    if not vals:
        return 0.0
    vals = sorted(vals)
    k = (len(vals) - 1) * (p / 100.0)
    f = int(k)
    c = min(f + 1, len(vals) - 1)
    if f == c:
        return float(vals[f])
    return vals[f] * (c - k) + vals[c] * (k - f)

def parse_logs():
    events = []
    seen_ips = set()
    
    with open(LOG_PATH, 'r') as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            m = log_pattern.match(line)
            if not m:
                continue
            timestamp, ip, method, path, status_str, latency_str = m.groups()
            status = int(status_str)
            latency = int(latency_str)
            
            is_new_ip = ip not in seen_ips
            seen_ips.add(ip)
            
            events.append({
                'timestamp': timestamp,
                'ip': ip,
                'method': method,
                'path': path,
                'status': status,
                'latency': latency,
                'is_new_ip': is_new_ip
            })
    return events

def detect_anomalies(events):
    # Group by minute: YYYY-MM-DDTHH:MM
    by_minute = defaultdict(list)
    for ev in events:
        minute_key = ev['timestamp'][:16]
        by_minute[minute_key].append(ev)
        
    all_minutes = sorted(by_minute.keys())
    
    minute_stats = []
    for m in all_minutes:
        evs = by_minute[m]
        errors = [e for e in evs if e['status'] >= 500]
        latencies = [e['latency'] for e in evs]
        p99 = percentile(latencies, 99) if latencies else 0.0
        minute_stats.append({
            'minute': m,
            'count': len(evs),
            'error_count': len(errors),
            'p99_latency': p99,
            'events': evs
        })
        
    error_counts = [s['error_count'] for s in minute_stats]
    p99_latencies = [s['p99_latency'] for s in minute_stats]
    
    err_mean = statistics.mean(error_counts) if error_counts else 0
    err_stdev = statistics.stdev(error_counts) if len(error_counts) > 1 else 0
    
    p99_mean = statistics.mean(p99_latencies) if p99_latencies else 0
    p99_stdev = statistics.stdev(p99_latencies) if len(p99_latencies) > 1 else 0
    
    err_threshold = err_mean + 2 * err_stdev
    p99_threshold = p99_mean + 2 * p99_stdev
    
    print(f"Error counts per minute - min: {min(error_counts)}, max: {max(error_counts)}, avg: {err_mean:.1f}")
    print(f"P99 latency per minute - min: {min(p99_latencies):.1f}, max: {max(p99_latencies):.1f}, avg: {p99_mean:.1f}")
    print(f"Error mean: {err_mean:.2f}, std: {err_stdev:.2f} (threshold: {err_threshold:.2f})")
    print(f"P99 mean: {p99_mean:.2f}, std: {p99_stdev:.2f} (threshold: {p99_threshold:.2f})")
    
    anomalies = []
    
    # Track minute-level spikes
    for s in minute_stats:
        m = s['minute']
        # Error spike anomaly (minute level)
        if s['error_count'] > err_threshold and s['error_count'] > 5:
            anomalies.append({
                'timestamp': f"{m}:00",
                'type': 'ERROR_SPIKE',
                'description': f"Error spike in minute {m}: {s['error_count']} errors (mean {err_mean:.1f})",
                'metric_value': s['error_count'],
                'ip': ''
            })
        # P99 latency anomaly (minute level)
        if s['p99_latency'] > p99_threshold and s['p99_latency'] > 200:
            anomalies.append({
                'timestamp': f"{m}:00",
                'type': 'LATENCY_SPIKE_P99',
                'description': f"P99 latency spike in minute {m}: {s['p99_latency']:.1f}ms (mean {p99_mean:.1f}ms)",
                'metric_value': round(s['p99_latency'], 2),
                'ip': ''
            })
            
        # Individual event level anomalies (new IPs, individual server errors 500/503/etc)
        for ev in s['events']:
            if ev['is_new_ip']:
                anomalies.append({
                    'timestamp': ev['timestamp'],
                    'type': 'NEW_IP',
                    'description': f"New client IP detected: {ev['ip']}",
                    'metric_value': 1,
                    'ip': ev['ip']
                })
            if ev['status'] >= 500:
                anomalies.append({
                    'timestamp': ev['timestamp'],
                    'type': 'SERVER_ERROR',
                    'description': f"HTTP {ev['status']} on {ev['method']} {ev['path']} from IP {ev['ip']} (latency {ev['latency']}ms)",
                    'metric_value': ev['status'],
                    'ip': ev['ip']
                })
                
    # Sort anomalies by timestamp
    anomalies.sort(key=lambda x: x['timestamp'])
    return anomalies, minute_stats

def write_outputs(anomalies, minute_stats, events):
    # Write anomalies.csv
    with open(ANOMALIES_PATH, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['timestamp', 'type', 'description', 'metric_value', 'ip'])
        writer.writeheader()
        for a in anomalies:
            writer.writerow(a)
    print(f"Wrote {len(anomalies)} anomalies to {ANOMALIES_PATH}")
    
    # Write timeline.md
    with open(TIMELINE_PATH, 'w') as f:
        f.write("# Log Analysis Timeline & Anomaly Report\n\n")
        f.write(f"Total log lines parsed: **{len(events):,}**\n")
        f.write(f"Total anomalies recorded: **{len(anomalies):,}**\n\n")
        
        f.write("## Executive Summary\n")
        f.write("This report details anomalies detected in `logs/app.log`, including HTTP server errors, high P99 latency spikes, and newly appearing client IP addresses across the time window.\n\n")
        
        f.write("## Minute-by-Minute Summary\n")
        f.write("| Minute | Total Requests | Errors (>=500) | P99 Latency (ms) |\n")
        f.write("|---|---|---|---|\n")
        for s in minute_stats:
            f.write(f"| {s['minute']} | {s['count']} | {s['error_count']} | {s['p99_latency']:.1f} |\n")
            
        f.write("\n## Detected Anomalies Timeline\n")
        f.write("| Timestamp | Type | IP | Metric | Description |\n")
        f.write("|---|---|---|---|---|\n")
        for a in anomalies:
            f.write(f"| {a['timestamp']} | `{a['type']}` | {a.get('ip', '')} | {a['metric_value']} | {a['description']} |\n")
            
    print(f"Wrote report to {TIMELINE_PATH}")

if __name__ == '__main__':
    events = parse_logs()
    print(f"Parsed {len(events)} valid log events.")
    anomalies, minute_stats = detect_anomalies(events)
    write_outputs(anomalies, minute_stats, events)
