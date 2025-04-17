---
title: Architecture
---

# Architecture

This document outlines the design and architecture of the MCP Census Server.
+
## Overview
+
The server implements the Model Context Protocol (MCP) over HTTP using JSON-RPC 2.0.
It is built with FastAPI for high performance and developer productivity.
+
Key components:
+
- **FastAPI app**: HTTP server and routing
- **JSON-RPC endpoint**: Single POST `/` accepts both single and batch requests
- **Authentication**: `X-API-Key` header validated against `SERVER_API_KEY`
- **Validation**: Pydantic models enforce JSON-RPC schema and tool input schemas
- **Business logic**: Handles `initialize`, `tools/list`, `tools/call` methods
- **Census API client**: `httpx` client with timeout, retry, and TTL cache (via `cachetools`)
- **Logging**: Structured logs using Python `logging`
- **Health check**: Simple `/health` endpoint for liveness
+
## Directory Structure
+
```
.
├── app.py               # FastAPI application entrypoint
├── requirements.txt     # Dependencies
├── .env.example         # Environment variable template
├── .gitignore
├── docs/
│   ├── architecture.md  # This document
│   └── usage.md         # Usage examples and patterns
├── tests/
│   └── test_app.py      # Pytest suite
└── .github/
    └── workflows/
        └── ci.yml       # CI configuration
```