# ethos-check

A lightweight [Hermes Agent](https://github.com/NousResearch/hermes-agent) plugin to query on-chain reputation scores and credibility levels from the [Ethos Network](https://www.ethos.network) API directly inside your agent workflows.

## Features

- Look up any **X (Twitter) handle** or **0x Ethereum address** on Ethos Network.
- Returns credibility `score`, reputation `level` (e.g., `neutral`, `revered`), and `found` status.
- Optional `min_score` threshold check (`meets_min_score`) for automated trust gating.
- Zero external dependencies — built purely on Python's standard library.

## Installation

Install directly via the Hermes CLI:

```bash
hermes plugins install iborazzi/ethos-check
hermes plugins enable ethos-check
```

Restart your Hermes session after enabling so the tool registers cleanly.

## Usage

Ask your Hermes agent naturally:

> Use `ethos_check` to look up @ethos_networkn.

Or enforce a minimum score threshold:

> Check @iborazzi with `ethos_check` and verify a minimum score of `1200`.

### Example Output

```json
{"subject": "service:x.com:username:ethos_network", "found": true, "score": 2426, "level": "revered"}
```

```json
{"subject": "service:x.com:username:iborazzi", "found": true, "score": 1214, "level": "neutral", "meets_min_score": true}
```

## How It Works

Queries `GET https://api.ethos.network/api/v2/score/userkey?userkey=<userkey>` with explicit `X-Ethos-Client`, `User-Agent`, and `Accept: application/json` headers per the [Ethos Developer Docs](https://developers.ethos.network).

## Testing

```bash
python test_offline.py
python test_live.py
```

## Status

`v0.1.0` — Issues, PRs, and feedback welcome.
