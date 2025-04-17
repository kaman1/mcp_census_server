---
title: About
---

# About MCP Census Server

The MCP Census Server implements the Model Context Protocol (MCP) for accessing
US Census Bureau data via JSON-RPC over HTTP.

## Key Features

- **JSON-RPC 2.0**: Supports single and batch requests, proper error codes.
- **Lifecycle Management**: `initialize` and `notifications/initialized` flows.
- **API Key Security**: `X-API-Key` authentication for all endpoints.
- **Census Tools**: Exposes a `census/get` tool for flexible Census API queries.
- **Caching**: In-memory TTL cache for repeated Census calls (default 5 minutes).
- **Health Check**: `/health` endpoint for liveness monitoring.
- **Interactive Docs**: Swagger UI at `/docs` and MDX-based site built with Mintlify.
- **Client App**: Bundled Next.js MCP client in the `client/` subfolder.

## Repository Layout

```
├── app.py                   # FastAPI JSON-RPC server
├── start.sh                 # Setup script for server + client
├── docs/                    # Documentation site (MDX + Mintlify)
│   ├── index.md             # Intro page
│   ├── about.md             # This about page
│   ├── howto.md             # How to run and setup
│   ├── authentication.md    # API key instructions
│   ├── usage.md             # Usage examples
│   └── architecture.md      # System architecture
├── client/                  # Next.js MCP client app
└── tests/                   # Pytest suite for server
```