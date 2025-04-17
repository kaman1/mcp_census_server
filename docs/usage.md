---
title: Usage
---

# Usage

This document provides example workflows for using the MCP Census Server.
+
## Initialization

```json
POST /
Content-Type: application/json
X-API-Key: <SERVER_API_KEY>

{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-03-26",
    "capabilities": {},
    "clientInfo": {"name":"ExampleClient","version":"1.0.0"}
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-03-26",
    "capabilities": {"tools": {"listChanged": false}},
    "serverInfo": {"name":"CensusMCPServer","version":"0.2.0"}
  }
}
```
+
## List Tools

```bash
curl -X POST http://localhost:8000/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $SERVER_API_KEY" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {"name":"census/get","description":"Retrieve data from the US Census Bureau API","inputSchema":{...}}
    ]
  }
}
```
+
## Call census/get

```bash
curl -X POST http://localhost:8000/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $SERVER_API_KEY" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"census/get","arguments":{"year":2020,"dataset":"acs/acs5","get":["P001001"],"for":"state:06"}}}'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [ {"type":"text","text":"[...JSON data...]"} ],
    "isError": false
  }
}
```