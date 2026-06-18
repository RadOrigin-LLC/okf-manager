import sys, os, unittest, tempfile, pathlib, subprocess, io, zipapp, shutil
from contextlib import redirect_stdout, redirect_stderr
SCRIPTS = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, SCRIPTS)
import okf_cli

class TDispatch(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_no_args_prints_usage_and_zero(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = okf_cli.main([])
        self.assertEqual(rc, 0)
        out = buf.getvalue().lower()
        self.assertIn("commands", out)
        for c in ("check", "seed", "map", "new"):
            self.assertIn(c, out)

    def test_unknown_command_returns_2(self):
        buf = io.StringIO()
        with redirect_stderr(buf):
            rc = okf_cli.main(["frobnicate"])
        self.assertEqual(rc, 2)
        self.assertIn("unknown", buf.getvalue().lower())

    def test_version_is_semver(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = okf_cli.main(["--version"])
        self.assertEqual(rc, 0)
        self.assertRegex(buf.getvalue().strip(), r"^\d+\.\d+\.\d+$")

    def test_dispatch_new_then_check(self):
        with redirect_stdout(io.StringIO()):
            rc = okf_cli.main(["new", "notes/a.md", "--bundle", str(self.root),
                               "--init", "--name", "B", "--type", "Note", "--title", "A",
                               "--timestamp", "2026-06-18T00:00:00Z", "--json"])
        self.assertEqual(rc, 0)
        self.assertTrue((self.root / "notes" / "a.md").exists())   # routed to okf_new
        with redirect_stdout(io.StringIO()):
            rc2 = okf_cli.main(["check", str(self.root), "--json"])
        self.assertIn(rc2, (0, 1))   # routed to okf_check; 0=clean / 1=findings, not a crash

class TZipapp(unittest.TestCase):
    def test_built_pyz_runs_check(self):
        with tempfile.TemporaryDirectory() as d:
            d = pathlib.Path(d)
            stage = d / "okf"; stage.mkdir()
            for p in pathlib.Path(SCRIPTS).glob("*.py"):
                shutil.copy2(p, stage / p.name)
            (stage / "__main__.py").write_text(
                "import sys, okf_cli\nsys.exit(okf_cli.main())\n", encoding="utf-8")
            pyz = d / "okf.pyz"
            zipapp.create_archive(stage, pyz)
            bundle = d / "b"; bundle.mkdir()
            (bundle / "index.md").write_text("# B\n", encoding="utf-8")
            (bundle / "a.md").write_text("---\ntype: Note\n---\nx\n", encoding="utf-8")
            proc = subprocess.run([sys.executable, str(pyz), "check", str(bundle), "--json"],
                                  capture_output=True, text=True)
            self.assertIn(proc.returncode, (0, 1), proc.stderr)   # zero-install run works
            self.assertIn("findings", proc.stdout)

if __name__ == "__main__":
    unittest.main()
