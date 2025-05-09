# MCP Census Server

A robust Model Context Protocol (MCP) server for accessing US Census Bureau data via JSON-RPC over HTTP.

## Features

- JSON-RPC 2.0 (single and batch requests)
- Pydantic models for request/response validation
- Caching of Census API responses (TTL 5 minutes)
- Structured logging (via Python `logging`)
- API key authentication via `X-API-Key` header
- Health check endpoint (`/health`)
- Interactive API docs (Swagger UI available at `/docs`)
- MCP methods:
  - `initialize`: negotiate protocol version and capabilities
  - `notifications/initialized`: client ready notification
  - `tools/list`: list available tools (`census/get`)
  - `tools/call`: invoke `census/get` to retrieve Census Bureau data

## Quickstart

1. Clone the repository and enter the directory:
   ```bash
   git clone https://github.com/kaman1/mcp_census_server.git
   cd mcp_census_server
   ```
2. Copy the environment template and set your keys:
   ```bash
   cp .env.example .env
   # Edit .env:
   # CENSUS_API_KEY=<your_census_api_key>
   # SERVER_API_KEY=<your_mcp_server_secret_key>
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the server:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```
5. Send JSON-RPC requests to `http://localhost:8000/` with header `X-API-Key: <SERVER_API_KEY>`.

Example `tools/list` call:
```bash
curl -X POST http://localhost:8000/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $SERVER_API_KEY" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## Development

- **Tests**: `pytest`
- **Formatting**: `black .`
- **Imports**: `isort .`
- **Linting**: `flake8 .`
- CI pipeline configured in `.github/workflows/ci.yml`

## Documentation

- **Architecture**: `docs/architecture.md`
- **Usage Examples**: `docs/usage.md`
- **Authentication**: `docs/authentication.md`
- **Styled Documentation (MDX + Mintlify)**:
  ```bash
  npm install
  npm run serve:docs
  ```

## Hosted Documentation

You can publish these docs via GitHub Pages:

1. In your GitHub repository, go to **Settings** > **Pages**.
2. Under **Source**, choose the **main** branch and `/docs` folder.
3. Click **Save**.

The docs will be available at:

    https://<username>.github.io/mcp_census_server/

You can add this URL in the repository **About** section as the project website.

## Client Application

The `client/` directory contains a Next.js-based MCP client that can interact with this server.

1. Change into the client folder:
   ```bash
   cd client
   ```
2. Copy the example environment file and fill in your keys and server URL:
   ```bash
   cp .env.example .env.local
   # Set OPENAI_API_KEY, MCP_SERVER_URL (e.g. https://your-server), SERVER_API_KEY
   ```
3. Install dependencies and start the development server:
   ```bash
   npm install
   npm run dev
   ```
4. Open [http://localhost:3000](http://localhost:3000) to use the client UI.

## Quick Start Script

You can configure environments and launch both server and client in one step:
```bash
chmod +x start.sh
./start.sh
```
This will prompt for all required keys and run the MCP server and client concurrently.