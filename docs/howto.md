---
title: How to Run
---

# How to Run MCP Census Server & Client

> This guide explains how to configure environment variables and start both the server and client applications.

## Prerequisites

- Python 3.9+ (for the server)
- Node.js 18+ and npm (for the client)

## Single Command Setup

From the project root (`mcp_census_server/`), run the helper script:

```bash
chmod +x start.sh
./start.sh
```

Follow the prompts to enter:

- CENSUS_API_KEY (Census Bureau API key)
- SERVER_API_KEY (server auth key)
- OPENAI_API_KEY (for client chat functionality)
- MCP_SERVER_URL (e.g., `http://localhost:8000`)
- SERVER_API_KEY (same as above)

This script will:

1. Create and populate `.env` in the server folder
2. Create and populate `.env.local` in the client folder
3. Launch the FastAPI server on port 8000
4. Launch the Next.js client on port 3000

## Manual Setup

### 1. Server

```bash
cd mcp_census_server
cp .env.example .env
# Edit .env → set CENSUS_API_KEY and SERVER_API_KEY
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Client

```bash
cd client
cp .env.example .env.local
# Edit .env.local → set OPENAI_API_KEY, MCP_SERVER_URL, SERVER_API_KEY
npm install
npm run dev
```

Then open [http://localhost:3000](http://localhost:3000) in your browser.