"""Generate dhxpyt/pytincture-assets.json for a dhxpyt source tree.

Pytincture verifies every widgetset JS/CSS asset against a SHA-256 manifest
before injecting it. It resolves that manifest from, in order: runtime config,
an owned `<package>/pytincture-assets.json` inside the wheel, then a builtin
compatibility lock. The builtin lock covers dhxpyt 0.9.18 only, so any other
version must ship its own manifest or the app cannot boot.

Asset order is load order and is preserved from the 0.9.18 lock.

    python scripts/generate_assets_manifest.py .           # write
    python scripts/generate_assets_manifest.py . --check   # verify, for CI

The manifest carries the package version, so it must be regenerated on every
version bump as well as whenever a file under dhxsrc/ changes.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

# Load order, mirroring Pytincture's 0.9.18 compatibility lock.
ASSETS: list[tuple[str, str]] = [
    ("dhxsrc/suite.css", "css"),
    ("dhxsrc/fonts/inter.css", "css"),
    ("dhxsrc/dhx_custom.css", "css"),
    ("dhxsrc/suite.js", "javascript"),
    ("dhxsrc/cardflow.js", "javascript"),
    ("dhxsrc/cardpanel.js", "javascript"),
    ("dhxsrc/chat.js", "javascript"),
    ("dhxsrc/kanban.css", "css"),
    ("dhxsrc/kanban.js", "javascript"),
    ("dhxsrc/kanban_board.js", "javascript"),
    ("dhxsrc/ragwidget.js", "javascript"),
    ("dhxsrc/theme.js", "javascript"),
    ("dhxsrc/webgpu.js", "javascript"),
]
PACKAGE = "dhxpyt"


def project_version(root: Path) -> str:
    text = (root / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
    if not match:
        raise SystemExit("could not read version from pyproject.toml")
    return match.group(1)


def main() -> int:
    argv = [a for a in sys.argv[1:] if a != "--check"]
    check_only = "--check" in sys.argv
    root = Path(argv[0] if argv else ".").resolve()
    package_dir = root / PACKAGE
    if not package_dir.is_dir():
        raise SystemExit(f"no {PACKAGE}/ package under {root}")

    assets = []
    for relative, kind in ASSETS:
        source = package_dir / relative
        if not source.is_file():
            raise SystemExit(f"missing declared asset: {source}")
        assets.append({
            "path": f"{PACKAGE}/{relative}",
            "type": kind,
            "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        })

    manifest = {
        "schema": 1,
        "package": PACKAGE,
        "version": project_version(root),
        "assets": assets,
    }
    target = package_dir / "pytincture-assets.json"
    payload = json.dumps(manifest, indent=2) + "\n"

    if check_only:
        # The manifest is verified at load time in the browser, so a stale one
        # fails closed and the app will not boot. Catch drift in CI instead.
        if not target.exists():
            print(f"MISSING {target} -- run: python {sys.argv[0]} {root}")
            return 1
        if target.read_text(encoding="utf-8") != payload:
            print(f"STALE {target} -- run: python {sys.argv[0]} {root}")
            return 1
        print(f"up to date: {target} ({len(assets)} assets, version {manifest['version']})")
        return 0

    target.write_text(payload, encoding="utf-8")
    print(f"wrote {target} ({len(assets)} assets, version {manifest['version']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
