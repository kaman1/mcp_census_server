#!/usr/bin/env bash
# Convenience script to configure env files and run both MCP server and client
set -e

# --- Server setup ---
echo "\n=== MCP Census Server Environment Setup ==="
if [ ! -f .env ]; then
  cp .env.example .env
  read -p "Enter CENSUS_API_KEY: " CENSUS_API_KEY
  read -p "Enter SERVER_API_KEY: " SERVER_API_KEY
  cat <<EOF >> .env
CENSUS_API_KEY=$CENSUS_API_KEY
SERVER_API_KEY=$SERVER_API_KEY
EOF
  echo ".env created for server."
else
  echo ".env already exists, skipping server setup."
fi

# --- Client setup ---
echo "\n=== MCP Client Environment Setup ==="
pushd client > /dev/null
if [ ! -f .env.local ]; then
  cp .env.example .env.local
  read -p "Enter OPENAI_API_KEY: " OPENAI_API_KEY
  read -p "Enter MCP_SERVER_URL (e.g. http://localhost:8000): " MCP_SERVER_URL
  read -p "Enter SERVER_API_KEY for client: " CLIENT_SERVER_API_KEY
  cat <<EOF >> .env.local
OPENAI_API_KEY=$OPENAI_API_KEY
MCP_SERVER_URL=$MCP_SERVER_URL
SERVER_API_KEY=$CLIENT_SERVER_API_KEY
EOF
  echo ".env.local created for client."
else
  echo ".env.local already exists, skipping client setup."
fi
popd > /dev/null

# --- Run processes ---
echo "\n=== Starting MCP Census Server and Client ==="
# Start server in background
uvicorn app:app --reload --host 0.0.0.0 --port 8000 &
SERVER_PID=$!

# Start client in background
pushd client > /dev/null
npm run dev &
CLIENT_PID=$!
popd > /dev/null

echo "Server PID: $SERVER_PID, Client PID: $CLIENT_PID"
echo "Press Ctrl+C to stop both."

# Wait for both processes
wait $SERVER_PID $CLIENT_PID