# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp>=1.10,<2", "httpx[socks]>=0.27"]
# ///
"""DeepSeek Search/Fetch API -> MCP stdio server.

Wraps the official raw JSON endpoints:
  POST https://api.deepseek.com/v1/tools/search
  POST https://api.deepseek.com/v1/tools/fetch

Key lookup mirrors the anysearch skill convention:
  .env next to this script (or repo root .env) > DEEPSEEK_API_KEY env var.

Run:  uv run scripts/mcp/deepseek_search_mcp.py
Config (Devin user scope, ~/.config/devin/mcp_config.json):
  "deepseek-search": {"command": "uv", "args": ["run", "<abs path to this file>"]}
"""
import os
import sys

import httpx
from mcp.server.fastmcp import FastMCP

API_BASE = os.environ.get("DEEPSEEK_API_BASE_URL", "https://api.deepseek.com").rstrip("/")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))


def _load_env() -> None:
    """Load .env next to this script, then repo root .env (same convention as
    anysearch-skill CLIs). .env values intentionally override environment."""
    for env_path in (os.path.join(SCRIPT_DIR, ".env"), os.path.join(REPO_ROOT, ".env")):
        if not os.path.isfile(env_path):
            continue
        with open(env_path, "r", encoding="utf-8-sig") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key, value = key.strip(), value.strip().strip("\"'").strip()
                if key and value:
                    os.environ[key] = value


_load_env()
API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")

mcp = FastMCP("deepseek-search")
_NO_KEY = (
    "DEEPSEEK_API_KEY is not set. Add it to scripts/mcp/.env "
    "(see .env.example) or export it in the environment, then restart the session."
)


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }


@mcp.tool()
async def deepseek_search(
    query: str,
    count: int = 10,
    need_content: bool = False,
    ori_question: str | None = None,
) -> str:
    """Search the live web with DeepSeek's in-house search engine.

    query supports operators: site:example.com, -site:example.com,
    la:zh / la:en (language), after:YYYY-MM-DD, before:YYYY-MM-DD.
    count: 1-50 results (default 10). need_content=True embeds each result's
    full page text (heavy — use only when snippets are insufficient).
    ori_question: the user's original question, improves query understanding.
    """
    if not API_KEY:
        return _NO_KEY
    payload: dict = {
        "query": query[:128],
        "count": max(1, min(int(count), 50)),
        "need_content": bool(need_content),
    }
    if ori_question:
        payload["ori_question"] = ori_question[:128]

    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{API_BASE}/v1/tools/search", headers=_headers(), json=payload)
    if r.status_code != 200:
        return f"DeepSeek Search API error {r.status_code}: {r.text[:500]}"

    results = r.json().get("results", [])
    if not results:
        return "No results."

    parts = []
    for i, item in enumerate(results, 1):
        line = (
            f"{i}. {item.get('title', '')}\n"
            f"   {item.get('url', '')}\n"
            f"   {item.get('site_name', '')}  score={item.get('rerank_score', '?')}  {item.get('date', '')}\n"
            f"   {item.get('snippet') or item.get('summary', '')}"
        )
        content = item.get("content") or ""
        if content:
            line += f"\n   --- content ---\n{content}"
        parts.append(line)
    return "\n\n".join(parts)


@mcp.tool()
async def deepseek_fetch(url: str) -> str:
    """Fetch a single web page and return its content as Markdown."""
    if not API_KEY:
        return _NO_KEY
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{API_BASE}/v1/tools/fetch", headers=_headers(), json={"url": url})
    if r.status_code != 200:
        return f"DeepSeek Fetch API error {r.status_code}: {r.text[:500]}"
    return r.json().get("content") or "(empty content)"


if __name__ == "__main__":
    if not API_KEY:
        print("warning: DEEPSEEK_API_KEY not set (tools will return a setup error)", file=sys.stderr)
    mcp.run()
