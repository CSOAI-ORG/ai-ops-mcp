# AI Ops MCP Server

> By [MEOK AI Labs](https://meok.ai) — System monitoring, health checks, maintenance scheduling, and security hardening

## Installation

```bash
pip install ai-ops-mcp
```

## Usage

```bash
# Run standalone
python server.py

# Or via MCP
mcp install ai-ops-mcp
```

## Tools

### `system_health_check`
Comprehensive system health check — CPU, memory, disk, and service status for common AI services.

### `check_service`
Check if a specific HTTP service is healthy. Returns status code and latency.

**Parameters:**
- `url` (str): URL to check

### `security_scan`
Run security scan — check for common vulnerabilities, exposed API keys in .env files, and open ports.

**Parameters:**
- `target` (str): Scan target (default 'system')

### `get_process_status`
Get status of running AI-related processes (Python, Node, Ollama, Uvicorn, etc.).

### `maintenance_schedule`
Get recommended maintenance actions based on system state (disk space, logs, packages, database).

## Authentication

Free tier: 15 calls/day. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## License

MIT — MEOK AI Labs
