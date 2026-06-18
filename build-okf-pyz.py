#!/usr/bin/env python3
"""Build a zero-install `okf.pyz` from scripts/ using the stdlib (no pip).

Run:  python build-okf-pyz.py
Then: python okf.pyz check <bundle>     (any platform)
  or: ./okf.pyz check <bundle>          (Unix, via the shebang)

The result is a single self-contained file any harness can invoke as `okf`."""
import shutil, tempfile, zipapp
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "scripts"

def build(out=None):
    out = Path(out) if out else ROOT / "okf.pyz"
    with tempfile.TemporaryDirectory() as d:
        stage = Path(d) / "okf"
        stage.mkdir()
        for p in SRC.glob("*.py"):            # all engine modules + okf_cli, no caches
            shutil.copy2(p, stage / p.name)
        (stage / "__main__.py").write_text(   # entry that preserves the exit code
            "import sys, okf_cli\nsys.exit(okf_cli.main())\n", encoding="utf-8")
        zipapp.create_archive(stage, out, interpreter="/usr/bin/env python3")
    return out

if __name__ == "__main__":
    print("wrote", build())
