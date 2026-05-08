<div align="center">

# Ai Ops MCP

**MCP server for ai ops mcp operations**

[![PyPI](https://img.shields.io/pypi/v/meok-ai-ops-mcp)](https://pypi.org/project/meok-ai-ops-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Ai Ops MCP provides AI-powered tools via the Model Context Protocol (MCP).

## Tools

| Tool | Description |
|------|-------------|
| `system_health_check` | Comprehensive system health check — CPU, memory, disk, services. |
| `check_service` | Check if a specific HTTP service is healthy. |
| `security_scan` | Run security scan — check for common vulnerabilities, open ports, outdated packa |
| `get_process_status` | Get status of running AI-related processes. |
| `maintenance_schedule` | Get recommended maintenance actions based on system state. |

## Installation

```bash
pip install meok-ai-ops-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "ai-ops": {
      "command": "python",
      "args": ["-m", "meok_ai_ops_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 5 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
