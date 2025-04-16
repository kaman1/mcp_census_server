#!/usr/bin/env python3
"""
MCP Census Server: FastAPI-based JSON-RPC implementation for US Census Bureau data.
"""
import os
import json
import logging
from typing import Any, Dict, List, Union

from fastapi import FastAPI, Request, HTTPException, Header, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
from cachetools import TTLCache, cached

# Logging configuration
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("mcp_census_server")

# Load environment variables
from dotenv import load_dotenv

load_dotenv()
CENSUS_API_KEY = os.getenv("CENSUS_API_KEY")
SERVER_API_KEY = os.getenv("SERVER_API_KEY")

if not SERVER_API_KEY:
    logger.error("SERVER_API_KEY is not set in environment")
    raise RuntimeError("SERVER_API_KEY missing")


async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != SERVER_API_KEY:
        logger.warning("Unauthorized access attempt with API key: %s", x_api_key)
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True


# JSON-RPC request/response models
class JSONRPCRequest(BaseModel):
    jsonrpc: str
    id: Union[str, int]
    method: str
    params: Dict[str, Any] = {}


class JSONRPCError(BaseModel):
    code: int
    message: str
    data: Any = None


class JSONRPCResponse(BaseModel):
    jsonrpc: str = "2.0"
    id: Union[str, int]
    result: Any = None
    error: JSONRPCError = None


# Cache for Census responses (max 100 entries, TTL 300s)
cache = TTLCache(maxsize=100, ttl=300)


@cached(cache)
def fetch_census_data(url: str, params: Dict[str, Any]) -> List[Any]:
    logger.debug("Fetching Census data: url=%s params=%s", url, params)
    with httpx.Client(timeout=10) as client:
        response = client.get(url, params=params)
        response.raise_for_status()
        return response.json()


# FastAPI app setup
app = FastAPI(title="MCP Census Server", docs_url="/docs", openapi_url="/openapi.json")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)


@app.post("/")
async def jsonrpc_endpoint(request: Request, auth: bool = Depends(verify_api_key)):
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    is_batch = isinstance(payload, list)
    requests = payload if is_batch else [payload]
    responses = []
    for call in requests:
        try:
            req = JSONRPCRequest(**call)
            resp = await handle_rpc(req)
            responses.append(resp.dict(exclude_none=True))
        except HTTPException as he:
            err = JSONRPCError(code=he.status_code, message=str(he.detail))
            responses.append(
                JSONRPCResponse(id=call.get("id"), error=err).dict(exclude_none=True)
            )
        except Exception as e:
            logger.exception("Internal error in RPC handler")
            err = JSONRPCError(code=-32603, message="Internal error")
            responses.append(
                JSONRPCResponse(id=call.get("id"), error=err).dict(exclude_none=True)
            )
    return JSONResponse(responses if is_batch else responses[0])


async def handle_rpc(req: JSONRPCRequest) -> JSONRPCResponse:
    if req.jsonrpc != "2.0":
        return JSONRPCResponse(
            id=req.id,
            error=JSONRPCError(code=-32600, message="Invalid JSON-RPC version"),
        )
    method = req.method
    params = req.params or {}
    # initialize
    if method == "initialize":
        result = {
            "protocolVersion": "2025-03-26",
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": "CensusMCPServer", "version": "0.2.0"},
        }
        return JSONRPCResponse(id=req.id, result=result)
    # notifications/initialized
    if method == "notifications/initialized":
        return JSONRPCResponse(id=req.id, result=None)
    # tools/list
    if method == "tools/list":
        tools = [
            {
                "name": "census/get",
                "description": "Retrieve data from the US Census Bureau API",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "year": {"type": "integer"},
                        "dataset": {"type": "string"},
                        "get": {"type": "array", "items": {"type": "string"}},
                        "for": {"type": "string"},
                    },
                    "required": ["year", "dataset", "get", "for"],
                },
            }
        ]
        return JSONRPCResponse(id=req.id, result={"tools": tools})
    # tools/call
    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name != "census/get":
            return JSONRPCResponse(
                id=req.id,
                error=JSONRPCError(code=-32601, message=f"Unknown tool: {name}"),
            )
        missing = [p for p in ("year", "dataset", "get", "for") if p not in args]
        if missing:
            return JSONRPCResponse(
                id=req.id,
                error=JSONRPCError(
                    code=-32602, message=f"Missing parameters: {missing}"
                ),
            )
        year = args["year"]
        dataset = args["dataset"]
        get_vars = args["get"]
        geo = args["for"]
        key = args.get("key") or CENSUS_API_KEY
        if not key:
            return JSONRPCResponse(
                id=req.id,
                result={
                    "content": [
                        {"type": "text", "text": "Census API key not provided"}
                    ],
                    "isError": True,
                },
            )
        url = f"https://api.census.gov/data/{year}/{dataset}"
        try:
            data = fetch_census_data(
                url, {"get": ",".join(get_vars), "for": geo, "key": key}
            )
            content = [{"type": "text", "text": json.dumps(data)}]
            return JSONRPCResponse(
                id=req.id, result={"content": content, "isError": False}
            )
        except httpx.HTTPStatusError as e:
            msg = f"HTTPError: {e.response.status_code} {e.response.text}"
            return JSONRPCResponse(
                id=req.id,
                result={"content": [{"type": "text", "text": msg}], "isError": True},
            )
        except Exception as e:
            return JSONRPCResponse(
                id=req.id,
                result={"content": [{"type": "text", "text": str(e)}], "isError": True},
            )
    # method not found
    return JSONRPCResponse(
        id=req.id,
        error=JSONRPCError(code=-32601, message=f"Method not found: {method}"),
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
