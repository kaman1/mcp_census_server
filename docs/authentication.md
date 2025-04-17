---
title: Authentication
---
# Authentication

All requests to the MCP Census Server must include a valid API key in the `X-API-Key` header.

```http
X-API-Key: <SERVER_API_KEY>
```

- If the header is missing or incorrect, the server returns **401 Unauthorized**.
- If the server is misconfigured (no key set), requests return **500 Server configuration error**.

Use this header on every JSON-RPC call (`initialize`, `tools/list`, `tools/call`).

## Environment Setup

Environment variables can be defined in a `.env` file at the project root. Copy the included example and fill in your keys:

```bash
cp .env.example .env
```

Then edit `.env`:
```dotenv
CENSUS_API_KEY=your_census_api_key_here
SERVER_API_KEY=your_server_api_key_here
# Optional: LOG_LEVEL=INFO
```