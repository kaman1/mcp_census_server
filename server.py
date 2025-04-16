#!/usr/bin/env python3
"""
MCP server for accessing US Census Bureau data as a tool.
"""
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import urllib.parse
import urllib.error


class MCPHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _send_response(self, response_obj, status_code=200):
        response_body = json.dumps(response_obj)
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body.encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        try:
            req = json.loads(body)
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return

        jsonrpc = req.get("jsonrpc")
        method = req.get("method")
        id_val = req.get("id")

        if jsonrpc != "2.0" or not method:
            error = {"code": -32600, "message": "Invalid JSON-RPC request"}
            resp = {"jsonrpc": "2.0", "id": id_val, "error": error}
            self._send_response(resp)
            return

        if method == "initialize":
            result = {
                "protocolVersion": "2025-03-26",
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "CensusMCPServer", "version": "0.1.0"},
            }
            resp = {"jsonrpc": "2.0", "id": id_val, "result": result}
            self._send_response(resp)
        elif method == "notifications/initialized":
            self.send_response(204)
            self.end_headers()
        elif method == "tools/list":
            tools = [
                {
                    "name": "census/get",
                    "description": "Retrieve data from the US Census Bureau API",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "year": {
                                "type": "integer",
                                "description": "Year of the data, e.g. 2020",
                            },
                            "dataset": {
                                "type": "string",
                                "description": "Dataset endpoint, e.g. 'acs/acs5'",
                            },
                            "get": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Variables to retrieve",
                            },
                            "for": {
                                "type": "string",
                                "description": "Geography spec, e.g. 'state:06'",
                            },
                        },
                        "required": ["year", "dataset", "get", "for"],
                    },
                }
            ]
            resp = {"jsonrpc": "2.0", "id": id_val, "result": {"tools": tools}}
            self._send_response(resp)
        elif method == "tools/call":
            params = req.get("params", {})
            name = params.get("name")
            args = params.get("arguments", {})
            if name != "census/get":
                error = {"code": -32601, "message": f"Unknown tool: {name}"}
                resp = {"jsonrpc": "2.0", "id": id_val, "error": error}
                self._send_response(resp)
                return
            missing = [p for p in ("year", "dataset", "get", "for") if p not in args]
            if missing:
                error = {
                    "code": -32602,
                    "message": f"Missing parameters: {', '.join(missing)}",
                }
                resp = {"jsonrpc": "2.0", "id": id_val, "error": error}
                self._send_response(resp)
                return
            year = args["year"]
            dataset = args["dataset"]
            get_vars = args["get"]
            geo = args["for"]
            api_key = args.get("key") or os.getenv("CENSUS_API_KEY")
            if not api_key:
                content = [{"type": "text", "text": "Census API key not provided"}]
                result_obj = {"content": content, "isError": True}
                resp = {"jsonrpc": "2.0", "id": id_val, "result": result_obj}
                self._send_response(resp)
                return
            base_url = f"https://api.census.gov/data/{year}/{dataset}"
            query = {"get": ",".join(get_vars), "for": geo, "key": api_key}
            url = base_url + "?" + urllib.parse.urlencode(query)
            try:
                with urllib.request.urlopen(url, timeout=10) as response:
                    data = json.loads(response.read())
                    text = json.dumps(data, indent=2)
                    content = [{"type": "text", "text": text}]
                    result_obj = {"content": content, "isError": False}
            except urllib.error.HTTPError as e:
                msg = f"HTTPError: {e.code} {e.reason}"
                content = [{"type": "text", "text": msg}]
                result_obj = {"content": content, "isError": True}
            except Exception as e:
                content = [{"type": "text", "text": f"Error: {e}"}]
                result_obj = {"content": content, "isError": True}
            resp = {"jsonrpc": "2.0", "id": id_val, "result": result_obj}
            self._send_response(resp)
        else:
            error = {"code": -32601, "message": f"Method not found: {method}"}
            resp = {"jsonrpc": "2.0", "id": id_val, "error": error}
            self._send_response(resp)


def run():
    port = int(os.getenv("PORT", 8000))
    server = HTTPServer(("0.0.0.0", port), MCPHandler)
    print(f"Census MCP Server listening on port {port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
