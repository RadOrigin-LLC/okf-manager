# CLAUDE.md — okfm (OKF Manager)

Operating and development instructions for this repo are in **`AGENTS.md`** (canonical, cross-harness). Read it first.

## Claude Code specifics

- This repo is also a Claude Code plugin (`.claude-plugin/plugin.json`) and a marketplace of one (`.claude-plugin/marketplace.json`, `source: "."`). User-facing commands are `/okfm:<skill>`.
- In Claude Code, the `okf` CLI is invoked as `python "${CLAUDE_PLUGIN_ROOT}/scripts" <command>` (the form used in the command skills). `enrich` uses Claude's `WebFetch`.

Everything else — the engine, tests, conventions, and the full command reference — is in `AGENTS.md` and `USAGE.md`.
