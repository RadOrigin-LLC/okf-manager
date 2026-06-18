# Lets the engine run as a directory or zipapp: `python scripts check .`
# or, after building, `python okf.pyz check .`. Preserves the dispatcher's exit code.
import sys
import okf_cli

sys.exit(okf_cli.main())
