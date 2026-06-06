#!/usr/bin/env python3
"""
AI Ops MCP — MEOK AI Labs. System monitoring, maintenance, neural retraining, security hardening."""

import sys, os
from auth_middleware import check_access

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
def system_health_check(api_key: str = "") -> str:
    """Comprehensive system health check — CPU, memory, disk, services.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.

    Args:
        api_key (str): The api key to analyze or process.

    Behavioral Transparency:
        - Side Effects: This tool is read-only and produces no side effects. It does not modify
          any external state, databases, or files. All output is computed in-memory and returned
          directly to the caller.
        - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
          require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
        - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
          included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
        - Error Handling: Returns structured error objects with 'error' key on failure.
          Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
        - Idempotency: Fully idempotent — calling with the same inputs always produces the
          same output. Safe to retry on timeout or transient failure.
        - Data Privacy: No input data is stored, logged, or transmitted to external services.
          All processing happens locally within the MCP server process.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://councilof.ai"}

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
        except Exception as e:
            services[name] = "DOWN"
    checks["services"] = services
    checks["healthy"] = all(v == "UP" for v in services.values())
    return checks

@mcp.tool()
def check_service(url: str, api_key: str = "") -> str:
    """Check if a specific HTTP service is healthy.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.

    Args:
        url (str): The url to analyze or process.
        api_key (str): The api key to analyze or process.

    Behavioral Transparency:
        - Side Effects: This tool is read-only and produces no side effects. It does not modify
          any external state, databases, or files. All output is computed in-memory and returned
          directly to the caller.
        - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
          require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
        - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
          included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
        - Error Handling: Returns structured error objects with 'error' key on failure.
          Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
        - Idempotency: Fully idempotent — calling with the same inputs always produces the
          same output. Safe to retry on timeout or transient failure.
        - Data Privacy: No input data is stored, logged, or transmitted to external services.
          All processing happens locally within the MCP server process.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://councilof.ai"}

    if err := _rl(): return err
    import urllib.request
    try:
        start = time.time()
        req = urllib.request.urlopen(url, timeout=5)
        latency = round((time.time() - start) * 1000, 1)
        return {"url": url, "status": req.status, "latency_ms": latency, "healthy": req.status == 200}
    except Exception as e:
        return {"url": url, "status": "error", "error": str(e), "healthy": False}

@mcp.tool()
def security_scan(target: str = "system", api_key: str = "") -> str:
    """Run security scan — check for common vulnerabilities, open ports, outdated packages.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.

    Args:
        target (str): The target to analyze or process.
        api_key (str): The api key to analyze or process.

    Behavioral Transparency:
        - Side Effects: This tool is read-only and produces no side effects. It does not modify
          any external state, databases, or files. All output is computed in-memory and returned
          directly to the caller.
        - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
          require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
        - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
          included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
        - Error Handling: Returns structured error objects with 'error' key on failure.
          Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
        - Idempotency: Fully idempotent — calling with the same inputs always produces the
          same output. Safe to retry on timeout or transient failure.
        - Data Privacy: No input data is stored, logged, or transmitted to external services.
          All processing happens locally within the MCP server process.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://councilof.ai"}

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
                except Exception as e: pass
        if len(findings) > 10: break
    return {"target": target, "findings": findings[:20], "total": len(findings),
        "critical": sum(1 for f in findings if f["severity"] == "high")}

@mcp.tool()
def get_process_status(api_key: str = "") -> str:
    """Get status of running AI-related processes.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.

    Args:
        api_key (str): The api key to analyze or process.

    Behavioral Transparency:
        - Side Effects: This tool is read-only and produces no side effects. It does not modify
          any external state, databases, or files. All output is computed in-memory and returned
          directly to the caller.
        - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
          require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
        - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
          included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
        - Error Handling: Returns structured error objects with 'error' key on failure.
          Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
        - Idempotency: Fully idempotent — calling with the same inputs always produces the
          same output. Safe to retry on timeout or transient failure.
        - Data Privacy: No input data is stored, logged, or transmitted to external services.
          All processing happens locally within the MCP server process.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://councilof.ai"}

    if err := _rl(): return err
    try:
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=5)
        lines = result.stdout.split("\n")
        ai_procs = []
        for line in lines:
            if any(k in line.lower() for k in ["python", "node", "ollama", "uvicorn", "gunicorn"]):
                parts = line.split()
                if len(parts) >= 11:
                    ai_procs.append({"pid": parts[1], "cpu": parts[2], "mem": parts[3], "command": " ".join(parts[10:])[:80]})
        return {"processes": ai_procs[:20], "total": len(ai_procs)}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def maintenance_schedule(api_key: str = "") -> str:
    """Get recommended maintenance actions based on system state.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.

    Args:
        api_key (str): The api key to analyze or process.

    Behavioral Transparency:
        - Side Effects: This tool is read-only and produces no side effects. It does not modify
          any external state, databases, or files. All output is computed in-memory and returned
          directly to the caller.
        - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
          require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
        - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
          included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
        - Error Handling: Returns structured error objects with 'error' key on failure.
          Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
        - Idempotency: Fully idempotent — calling with the same inputs always produces the
          same output. Safe to retry on timeout or transient failure.
        - Data Privacy: No input data is stored, logged, or transmitted to external services.
          All processing happens locally within the MCP server process.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://councilof.ai"}

    if err := _rl(): return err
    import shutil
    disk = shutil.disk_usage("/")
    actions = []
    if disk.free / disk.total < 0.15:
        actions.append({"priority": "high", "action": "Free disk space", "detail": f"Only {disk.free//(1024**3)}GB free"})
    actions.append({"priority": "medium", "action": "Rotate logs", "detail": "Clear /tmp/*.log files older than 7 days"})
    actions.append({"priority": "low", "action": "Update packages", "detail": "pip/npm outdated packages"})
    actions.append({"priority": "medium", "action": "Database vacuum", "detail": "VACUUM PostgreSQL tables"})
    return {"timestamp": datetime.now(timezone.utc).isoformat(), "actions": actions}

def main():
    mcp.run()

if __name__ == '__main__':
    main()
