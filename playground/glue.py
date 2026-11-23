"""Glue between the playground page and the vendored detector (poison.py).

Runs identically under CPython (tests) and Pyodide (browser): ``analyze(raw_json)`` takes the tool
definition as JSON text and returns a JSON string.
"""
from __future__ import annotations

import json
import re

import poison

MAX_CHARS = 20_000
_NAMES = {"inputSchema": "input_schema"}


def _normalise(tool: dict) -> dict:
    """Accept MCP's camelCase ``inputSchema`` as well as the scanner's ``input_schema``."""
    out = dict(tool)
    for camel, snake in _NAMES.items():
        if camel in out and snake not in out:
            out[snake] = out.pop(camel)
    if not isinstance(out.get("input_schema", {}), dict):
        out["input_schema"] = {}
    if not isinstance(out.get("description", ""), str):
        out["description"] = ""
    return out


def _visible(text: str, limit: int = 600) -> str:
    """Make invisible characters visible so the page can show what was hidden."""
    def show(m: re.Match) -> str:
        return "".join(f"<U+{ord(c):04X}>" for c in m.group(0))

    text = re.sub("[\U000e0000-\U000e007f​-‏‪-‮⁠-⁤⁦-⁩﻿­]+", show, text)
    return text if len(text) <= limit else text[:limit] + " …"


def analyze(raw: str) -> str:
    if len(raw) > MAX_CHARS:
        return json.dumps({"error": f"Input is {len(raw):,} characters; the playground limit is {MAX_CHARS:,}."})
    try:
        tool = json.loads(raw)
    except json.JSONDecodeError as exc:
        return json.dumps({"error": f"Not valid JSON: {exc}"})
    if not isinstance(tool, dict):
        return json.dumps({"error": "Expected a JSON object describing one tool."})
    tool = _normalise(tool)

    score, severity, why = poison.explain(tool)
    parts = []
    for where, text in poison._parts(tool):
        if not text:
            continue
        part_score, features, layers = poison.score_text(text)
        features = list(dict.fromkeys(features))  # the detector may report a signal twice
        parts.append({"where": where, "score": round(part_score, 1), "features": features, "layers": layers})
    parts.sort(key=lambda p: -p["score"])

    decoded = []
    if parts and parts[0]["layers"]:
        top = next(t for w, t in poison._parts(tool) if w == parts[0]["where"])
        views, _ = poison.views(top)
        shown = [_visible(v) for v in views[1:] if v != top]
        decoded = list(dict.fromkeys(shown))[:4]  # drop views that only differ in invisible characters or spacing

    return json.dumps(
        {
            "score": round(score, 1),
            "severity": severity,
            "summary": why,
            "thresholds": {"medium": poison.THRESHOLD_MEDIUM, "high": poison.THRESHOLD_HIGH},
            "parts": parts,
            "decoded_views": decoded,
        }
    )
