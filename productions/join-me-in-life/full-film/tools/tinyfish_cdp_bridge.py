#!/usr/bin/env python3
"""Forward an authorized TinyFish CDP session through the managed HTTPS proxy.

Playwright's CDP transport otherwise tries a direct route unavailable in this
Cloud VM. No policy/proxy/TLS settings are weakened. Session credentials remain
in the private file supplied by --session; neither endpoint nor payload is logged.
Requires websockets 16, already present in this task. Closing this bridge does
not close the provider session: save/cancel it through TinyFish's documented API.
"""
import argparse
import asyncio
import json
import os
from pathlib import Path
import ssl
from urllib.parse import urlsplit

import websockets


async def serve(args):
    session = json.loads(Path(args.session).read_text())
    endpoint = session["cdp_url"]
    url = urlsplit(endpoint)
    if url.scheme != "wss" or not (url.hostname or "").endswith(".tinyfish.io"):
        raise ValueError("Unexpected TinyFish CDP endpoint; inspect the private API response")
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if not proxy:
        policy = json.loads(Path("/etc/codex/network-policy.json").read_text())
        proxy = policy["http_proxy"]

    async def forward(source, destination):
        async for message in source:
            await destination.send(message)

    async def handle(local):
        try:
            async with websockets.connect(endpoint, proxy=proxy,
                                          ssl=ssl.create_default_context(),
                                          max_size=None, open_timeout=30) as remote:
                tasks = [asyncio.create_task(forward(local, remote)),
                         asyncio.create_task(forward(remote, local))]
                done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                for task in pending:
                    task.cancel()
                await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as exc:
            print(f"CDP transport ended: {type(exc).__name__}", flush=True)
            await local.close(code=1011, reason="Upstream CDP transport ended")

    async with websockets.serve(handle, "127.0.0.1", args.port, max_size=None):
        print(f"Authorized CDP bridge ready on loopback port {args.port}", flush=True)
        await asyncio.sleep(args.lifetime)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", required=True)
    parser.add_argument("--port", type=int, default=8877)
    parser.add_argument("--lifetime", type=int, default=480)
    asyncio.run(serve(parser.parse_args()))
