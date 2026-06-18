# AGENTS.md — okfm (OKF Manager)

Canonical, cross-harness operating instructions for this repo. `CLAUDE.md` and `GEMINI.md` are thin shims that point here.

## What this repo is

A single toolkit for building and maintaining an Open Knowledge Format (OKF) knowledge base. It is a dependency-free stdlib Python 3 engine in `scripts/`, exposed as the `okf` CLI, plus harness-neutral skills in `skills/<name>/SKILL.md`. It also ships as a Claude Code plugin (`.claude-plugin/`), but nothing in the engine depends on Claude.

## Operating the toolkit

The engine is the `okf` CLI. Resolve it for your environment:

- `okf <command>` — if the CLI is on PATH, or
- `python okf.pyz <command>` — build once with `python build-okf-pyz.py`, or
- `python <repo>/scripts <command>` — run the engine directory in place.

Full operating manual: **`USAGE.md`**. Task-by-task guidance: **`skills/<name>/SKILL.md`**, written in the neutral `okf <command>` vocabulary (the per-harness invocation prefix is documented in `skills/okf/SKILL.md` → "Engine invocation"). Subcommands: `new`, `add`, `convert`, `seed`, `move`, `check`, `map`, `find`, `scan`.

`enrich` is the only flow that needs network; supply your harness's own web-fetch tool. The engine never goes online.

## Developing this repo

- **Stdlib only.** No third-party dependencies in `scripts/`; keep the engine offline.
- **Tests** use stdlib `unittest` (no pytest): `for t in tests/test_*.py; do python "$t" || break; done`.
- **Every write previews first and is never destructive** — preserve that guarantee. The engine owns the nested `index.md` tree and `log.md`.
- **Match existing module idioms.** License: Apache-2.0.

## Origin

Extracted from `rad-claude-skills` (formerly the `rad-okf` plugin) on 2026-06-18; renamed `rad-okf` → `okfm`.
