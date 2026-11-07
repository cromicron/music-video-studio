#!/usr/bin/env python3
"""Inspect Hedra's configured MCP connection without submitting or spending.

Uses only HEDRA_MCP_TOKEN and only https://mcp.hedra.com. Keeps inherited proxy
and CA trust. The endpoint is fixed; redirects are rejected to prevent sending
the credential to another host. No generation or billing mutation is exposed.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


ENDPOINT = "https://mcp.hedra.com"
READ_ONLY = frozenset({
    "get_balance", "list_workspaces", "list_models", "get_model", "estimate",
    "query_assets", "get_generations",
})


class RejectRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        raise RuntimeError("Hedra redirected the request; refusing credential forwarding")


def call(tool, arguments):
    if tool not in READ_ONLY:
        raise ValueError("Only the explicitly listed read-only tools are allowed")
    token = os.environ.get("HEDRA_MCP_TOKEN")
    if not token:
        raise RuntimeError("HEDRA_MCP_TOKEN is not configured in this environment")
    payload = {
        "jsonrpc": "2.0", "id": 1, "method": "tools/call",
        "params": {"name": tool, "arguments": arguments},
    }
    request = urllib.request.Request(
        ENDPOINT, data=json.dumps(payload).encode(),
        headers={
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
    )
    opener = urllib.request.build_opener(RejectRedirect())
    try:
        with opener.open(request, timeout=45) as response:
            raw = response.read().decode()
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"Hedra returned HTTP {error.code}") from None
    # Streamable HTTP can return JSON directly or one JSON-RPC SSE payload.
    if raw.lstrip().startswith("event:") or raw.lstrip().startswith("data:"):
        payloads = [line[5:].strip() for line in raw.splitlines() if line.startswith("data:")]
        messages = [json.loads(value) for value in payloads]
        message = next((value for value in messages if value.get("id") == 1), None)
        if message is None:
            raise RuntimeError("Hedra returned no matching JSON-RPC response")
    else:
        message = json.loads(raw)
    if "error" in message:
        raise RuntimeError("Hedra JSON-RPC error: " + json.dumps(message["error"]))
    result = message["result"]
    if result.get("isError"):
        raise RuntimeError("Hedra tool error: " + json.dumps(result.get("content", [])))
    return result.get("structuredContent", result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tool", choices=sorted(READ_ONLY), nargs="?", default="get_balance")
    parser.add_argument("--args", default="{}", help="JSON object matching the live tool schema")
    args = parser.parse_args()
    try:
        arguments = json.loads(args.args)
        if not isinstance(arguments, dict):
            parser.error("--args must be a JSON object")
        print(json.dumps(call(args.tool, arguments), indent=2))
    except (RuntimeError, ValueError, urllib.error.URLError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
