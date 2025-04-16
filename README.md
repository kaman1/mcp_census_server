# Census MCP Server

This is a Model Context Protocol (MCP) server that provides a tool for retrieving data from the United States Census Bureau API.

## Requirements

- Python 3.7 or higher
- No external Python dependencies (uses standard library)
- Set environment variable `CENSUS_API_KEY` to your Census Bureau API key.

## Usage

1. Export your Census API key:
   ```bash
   export CENSUS_API_KEY=your_api_key_here
   ```
2. Run the server:
   ```bash
   python server.py
   ```
   By default, the server listens on port 8000. To change the port:
   ```bash
   export PORT=9000
   python server.py
   ```

## JSON-RPC Methods

- **initialize**: Handshake to negotiate protocol version and capabilities.
- **notifications/initialized**: Notification that the client is ready.
- **tools/list**: Returns the list of available tools, including `census/get`.
- **tools/call**: Invoke the `census/get` tool to fetch data. Example:
  ```json
  {
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "census/get",
      "arguments": {
        "year": 2020,
        "dataset": "acs/acs5",
        "get": ["P001001"],
        "for": "state:06"
      }
    }
  }
  ```
The response `result.content[0].text` contains the JSON response from the Census API.