# Using okfm (the `okf` CLI)

okfm builds and maintains an Open Knowledge Format (OKF) knowledge base — a directory of markdown files with YAML frontmatter, readable by humans and any AI agent. This file is the harness-neutral operating manual: with it and the `okf` CLI, any agent can run okfm without a skill or plugin system.

## Invoking the CLI

The engine is plain stdlib Python 3 — no pip, no network. `okf <command>` below means whichever of these your environment supports:

- `okf <command>` — if the CLI is on your PATH.
- `python okf.pyz <command>` — build the single-file artifact first with `python build-okf-pyz.py`.
- `python /path/to/okf-manager/scripts <command>` — run the engine directory in place.
- Claude Code only: `python "${CLAUDE_PLUGIN_ROOT}/scripts" <command>`.

`okf --help` lists commands; `okf <command> --help` shows a command's options.

## Subcommands

| Command | What it does | Key flags |
|---|---|---|
| `new <path>` | Create one concept; `--init` also scaffolds a fresh bundle. | `--init --name`, `--type --title --description --tag`, `--resource`, `--citation`, `--body`, `--bundle`, `--dry-run --json` |
| `add <src> <dest>` | Import an existing markdown file; fills only missing frontmatter. | `--type --title …`, `--resource`, `--bundle`, `--dry-run` |
| `convert <src> <dest>` | Turn a `.txt/.html/.csv/.json` file into a concept with a `# Citations` block. | `--type --title`, `--citation`, `--bundle`, `--dry-run` |
| `seed <source>` | Bulk-generate concepts from a SQLite DB, OpenAPI/JSON-Schema file, or directory tree. | `--mode auto\|sqlite\|openapi\|tree`, `--dest-dir`, `--bundle`, `--dry-run` |
| `move <src> <dest>` | Rename/relocate a concept and rewrite inbound links bundle-wide. | `--bundle`, `--dry-run --json` |
| `check [path]` | Validate the bundle (frontmatter, links, orphans, staleness, index drift, …). | `--fix` (preview with `--dry-run`), `--stale-days`, `--json` |
| `map [path]` | Write a self-contained HTML browser (`viz.html`). | `--out`, `--name` |
| `find [path]` | Ranked keyword/field search; returns matches plus their linked concepts. | `--text --type --tag --status --limit --json` |
| `scan [path]` | Propose importable files from a repo or notes folder. | `--json` |

Writing commands accept `--dry-run` (preview) and `--json` (machine-readable). Drive them with `--dry-run` first to see the change set, then run without it to write.

## Core workflow

1. **Initialize:** `okf new welcome.md --bundle knowledge --init --name "My KB" --type Note --title Welcome`
2. **Populate:** `okf scan <repo-or-notes>` to triage, `okf seed <source>` for bulk, `okf add`/`okf convert` for single files, `okf new` to hand-author the high-value pieces.
3. **Maintain:** `okf check knowledge --fix` (preview first), `okf move` for renames.
4. **Read:** `okf find --tag <tag>`, or `okf map knowledge` and open `viz.html`.

## Conventions (so the base stays healthy)

- **Preview first.** Use `--dry-run` before writing. The engine never deletes files, and `--fix` never retargets broken links.
- **Standard markdown links only** — `[text](/path.md)` (absolute from bundle root) or relative. Not `[[wikilinks]]`.
- **Trust tiers.** Generated concepts carry `curated_by: agent`; flip to `human` once a person has verified them.
- **The engine owns** the nested `index.md` tree and `log.md` — regenerate the index via `check --fix`, don't hand-edit it.
- **Capture filter.** Keep what is Relevant, Actionable, has Depth, and is Authoritative. A small accurate base beats a large noisy one.

## Wiring it into a project

Commit the bundle folder, then point the consuming project's agent instructions (`CLAUDE.md` / `AGENTS.md` / `GEMINI.md`) at it: tell the agent to read `knowledge/index.md` before non-trivial work, treat concepts as orientation and verify against live code, and update the relevant concept when a durable decision changes.

## The one networked flow: `enrich`

`enrich` (growing the base from web pages) is the only flow that needs network, and the engine deliberately has none. Fetch pages with your harness's own web-fetch capability, then write each as a reference: `okf new references/<slug>.md --type Reference --title "<title>" --citation "<url>" --body "<summary>"`. If your harness has no web tool, save the page locally and `okf convert` it instead. There is no `okf` subcommand for `enrich` — it is agent-orchestrated, not a single engine call.
