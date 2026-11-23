"""Refresh playground/poison.py from the aisec-suite repository.

    python playground/sync_detector.py [commit-sha-or-branch]

Fetches aisec/poison.py, removes the one import that needs the aisec package (and the helper that
uses it), prepends a provenance header and writes playground/poison.py. Then run the tests:
    python -m pytest playground
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request

REPO = "Pyhroff/aisec-suite"


def main() -> None:
    ref = sys.argv[1] if len(sys.argv) > 1 else "master"
    commit = json.load(urllib.request.urlopen(f"https://api.github.com/repos/{REPO}/commits/{ref}"))["sha"]
    src = urllib.request.urlopen(f"https://raw.githubusercontent.com/{REPO}/{commit}/aisec/poison.py").read().decode("utf-8")
    marker = "from aisec.model import Finding\n\n"
    if marker not in src or "def findings_for(" not in src:
        sys.exit("poison.py has changed shape; update this script before syncing")
    src = src.replace(marker, "")
    src = src[: src.index("def findings_for(")].rstrip() + "\n"
    header = (
        f"# Vendored from https://github.com/{REPO} (aisec/poison.py at commit {commit}), MIT licence.\n"
        "# Only change: the aisec.model.Finding import and findings_for() were removed so the module is\n"
        "# self-contained for the browser playground. Update with: python playground/sync_detector.py\n"
    )
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "poison.py")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(header + src)
    print(f"wrote {out} from {REPO}@{commit}")


if __name__ == "__main__":
    main()
