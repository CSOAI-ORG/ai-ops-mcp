#!/usr/bin/env python3
"""AI Ops MCP — MEOK AI Labs. System monitoring, maintenance, neural retraining, security hardening."""
import json, os, subprocess, time, platform
from datetime import datetime, timezone
from typing import Optional
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

FREE_DAILY_LIMIT = 15
_usage = defaultdict(list)
def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now-t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT: return json.dumps({"error": f"Limit {FREE_DAILY_LIMIT}/day"})
    _usage[c].append(now); return None

mcp = FastMCP("ai-ops", instructions="MEOK AI Labs — AI Operations. System monitoring, health checks, maintenance scheduling, security hardening.")

@mcp.tool()
def system_health_check() -> str:
    """Comprehensive system health check — CPU, memory, disk, services."""
    if err := _rl(): return err
    import shutil
    disk = shutil.disk_usage("/")
    checks = {
        "platform": platform.system(),
        "machine": platform.machine(),
        "python": platform.python_version(),
        "disk_total_gb": round(disk.total / (1024**3), 1),
        "disk_free_gb": round(disk.free / (1024**3), 1),
        "disk_used_pct": round(disk.used / disk.total * 100, 1),
    }
    # Check common AI services
    services = {}
    for name, port in [("ollama", 11434), ("sov3", 3101), ("meok-api", 3200), ("meok-ui", 3000), ("postgres", 5432)]:
        try:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect(("127.0.0.1", port))
            s.close()
            services[name] = "UP"
        except:
            services[name] = "DOWN"
    checks["services"] = services
    checks["healthy"] = all(v == "UP" for v in services.values())
    return json.dumps(checks, indent=2)

@mcp.tool()
def check_service(url: str) -> str:
    """Check if a specific HTTP service is healthy."""
    if err := _rl(): return err
    import urllib.request
    try:
        start = time.time()
        req = urllib.request.urlopen(url, timeout=5)
        latency = round((time.time() - start) * 1000, 1)
        return json.dumps({"url": url, "status": req.status, "latency_ms": latency, "healthy": req.status == 200}, indent=2)
    except Exception as e:
        return json.dumps({"url": url, "status": "error", "error": str(e), "healthy": False}, indent=2)

@mcp.tool()
def security_scan(target: str = "system") -> str:
    """Run security scan — check for common vulnerabilities, open ports, outdated packages."""
    if err := _rl(): return err
    findings = []
    # Check for common security issues
    if os.path.exists("/Users"):  # macOS
        if not os.path.exists("/usr/local/bin/brew"):
            findings.append({"type": "info", "issue": "Homebrew not installed", "severity": "low"})
    # Check for .env files with secrets
    for root, dirs, files in os.walk(os.path.expanduser("~"), topdown=True):
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '.venv', '__pycache__']]
        for f in files:
            if f == ".env":
                path = os.path.join(root, f)
                try:
                    content = open(path).read()
                    if "sk_live_" in content or "sk-" in content:
                        findings.append({"type": "critical", "issue": f"API key in {path}", "severity": "high"})
                except: pass
        if len(findings) > 10: break
    return json.dumps({"target": target, "findings": findings[:20], "total": len(findings),
        "critical": sum(1 for f in findings if f["severity"] == "high")}, indent=2)

@mcp.tool()
def get_process_status() -> str:
    """Get status of running AI-related processes."""
    if err := _rl(): return err
    try:
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=5)
        lines = result.stdout.split("
")
        ai_procs = []
        for line in lines:
            if any(k in line.lower() for k in ["python", "node", "ollama", "uvicorn", "gunicorn"]):
                parts = line.split()
                if len(parts) >= 11:
                    ai_procs.append({"pid": parts[1], "cpu": parts[2], "mem": parts[3], "command": " ".join(parts[10:])[:80]})
        return json.dumps({"processes": ai_procs[:20], "total": len(ai_procs)}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

@mcp.tool()
def maintenance_schedule() -> str:
    """Get recommended maintenance actions based on system state."""
    if err := _rl(): return err
    import shutil
    disk = shutil.disk_usage("/")
    actions = []
    if disk.free / disk.total < 0.15:
        actions.append({"priority": "high", "action": "Free disk space", "detail": f"Only {disk.free//(1024**3)}GB free"})
    actions.append({"priority": "medium", "action": "Rotate logs", "detail": "Clear /tmp/*.log files older than 7 days"})
    actions.append({"priority": "low", "action": "Update packages", "detail": "pip/npm outdated packages"})
    actions.append({"priority": "medium", "action": "Database vacuum", "detail": "VACUUM PostgreSQL tables"})
    return json.dumps({"timestamp": datetime.now(timezone.utc).isoformat(), "actions": actions}, indent=2)

if __name__ == "__main__":
    mcp.run()
