"""ethos-check: Hermes plugin that reads Ethos reputation data (read-only).

Uses only the standard library. Calls the free public Ethos v2 API, which
asks callers to send an X-Ethos-Client header naming the app.
"""
import json
import re
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://api.ethos.network/api/v2"
CLIENT_HEADER = "hermes-ethos-check@0.1.0"
_HANDLE_RE = re.compile(r"^[A-Za-z0-9_]{1,15}$")
_ADDRESS_RE = re.compile(r"^0x[0-9a-fA-F]{40}$")

SCHEMA = {
    "name": "ethos_check",
    "description": (
        "Look up the Ethos credibility score and level of an X account or "
        "EVM address. Use before trusting, recommending, or transacting with "
        "an unknown counterparty. Read-only. A low or missing score is a "
        "signal to be careful, not proof of wrongdoing."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "subject": {
                "type": "string",
                "description": "X handle (with or without @) or an 0x EVM address.",
            },
            "min_score": {
                "type": "integer",
                "description": "Optional. If set, the result also says whether the score meets this threshold.",
            },
        },
        "required": ["subject"],
    },
}


def _userkey(subject: str):
    s = subject.strip().lstrip("@")
    if _ADDRESS_RE.match(s):
        return f"address:{s}"
    if _HANDLE_RE.match(s):
        return f"service:x.com:username:{s}"
    return None


def _get(path: str, params: dict):
    url = f"{BASE_URL}{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"X-Ethos-Client": CLIENT_HEADER, "User-Agent": CLIENT_HEADER, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def ethos_check(args: dict, **kwargs) -> str:
    key = _userkey(str(args.get("subject", "")))
    if key is None:
        return json.dumps({"error": "subject must be an X handle or a 0x address"})
    try:
        data = _get("/score/userkey", {"userkey": key})
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return json.dumps({"subject": key, "found": False,
                               "note": "No Ethos profile found for this subject."})
        return json.dumps({"error": f"Ethos API returned HTTP {e.code}"})
    except Exception as e:  # network, timeout, bad JSON
        return json.dumps({"error": f"lookup failed: {type(e).__name__}"})

    result = {"subject": key, "found": True,
              "score": data.get("score"), "level": data.get("level")}
    min_score = args.get("min_score")
    if isinstance(min_score, int) and isinstance(result["score"], (int, float)):
        result["meets_min_score"] = result["score"] >= min_score
    return json.dumps(result)


def register(ctx):
    ctx.register_tool(
        name="ethos_check",
        toolset="ethos",
        schema=SCHEMA,
        handler=ethos_check,
    )
