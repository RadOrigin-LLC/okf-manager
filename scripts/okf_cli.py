# scripts/okf_cli.py
"""Unified `okf` command-line entry point.

Dispatches subcommands to the individual engine modules so any agent harness can
drive okfm with `okf <command> ...` instead of invoking each script by path.
The engine stays plain stdlib Python; this is just the front door that makes the
toolkit usable from any harness (or a plain shell)."""
import sys

__version__ = "1.0.0"

# subcommand -> module name (each module exposes main(argv) -> exit code)
COMMANDS = {
    "new": "okf_new",
    "add": "okf_add",
    "convert": "okf_convert",
    "seed": "okf_seed",
    "move": "okf_move",
    "check": "okf_check",
    "map": "okf_map",
    "find": "okf_find",
    "scan": "okf_scan",
}

def _usage(stream):
    stream.write("usage: okf <command> [args...]\n\ncommands:\n")
    for name in COMMANDS:
        stream.write("  %s\n" % name)
    stream.write("\nRun `okf <command> --help` for a command's options.\n")

def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help", "help"):
        _usage(sys.stdout)
        return 0
    cmd = argv[0]
    if cmd in ("--version", "-V"):
        sys.stdout.write(__version__ + "\n")
        return 0
    if cmd not in COMMANDS:
        sys.stderr.write("okf: unknown command %r\n" % cmd)
        _usage(sys.stderr)
        return 2
    module = __import__(COMMANDS[cmd])
    rc = module.main(argv[1:])
    return 0 if rc is None else rc

if __name__ == "__main__":
    sys.exit(main())
