"""Offline tests for scripts/eidb.py (no network: DOI fetching is stubbed).

Run: python3 -m unittest discover -s tests -v
"""
import contextlib
import csv
import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("eidb", ROOT / "scripts" / "eidb.py")
eidb = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(eidb)

FAKE_DOI = {
    "type": "article", "authors": "Becher, Ayelet; Lefstein, Adam", "year": "2020",
    "title": "Teaching as a Clinical Profession: Adapting the Medical Model",
    "venue": "Journal of Teacher Education", "volume": "72", "issue": "4", "pages": "477–488",
    "doi": "10.1177/0022487120972633", "url": "http://dx.doi.org/10.1177/0022487120972633", "abstract": "x",
    "apa": "Becher, A., & Lefstein, A. (2020). Teaching as a Clinical Profession. Journal of Teacher Education, 72(4), 477–488. https://doi.org/10.1177/0022487120972633",
    "bibtex": "@article{Becher_2020, title={Teaching as a Clinical Profession}, year={2020} }",
}

PAGE = """---
title: Test page
kind: concept
status: seed
updated: 2026-11-03
summary: A test page
criteria: [methods]
related: []
---

# Test page

Clinical reasoning [@{key}]. Example in code: `[@NotAKey]`.
"""


class EidbTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.data = base / "data"
        self.wiki = base / "wiki"
        (self.wiki / "concepts").mkdir(parents=True)
        self.env = {k: os.environ.get(k) for k in ("EI_DATA_DIR", "EI_WIKI_DIR", "EI_CONFIG")}
        os.environ["EI_DATA_DIR"] = str(self.data)
        os.environ["EI_WIKI_DIR"] = str(self.wiki)
        os.environ["EI_CONFIG"] = str(base / "no-config.json")
        self._orig_fetch = eidb.fetch_doi
        eidb.fetch_doi = lambda ctx, doi: dict(FAKE_DOI)
        self.run_cli("init")

    def tearDown(self):
        eidb.fetch_doi = self._orig_fetch
        for k, v in self.env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        self.tmp.cleanup()

    def run_cli(self, *args, expect_exit=None):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            try:
                eidb.main(list(args))
                code = 0
            except SystemExit as e:
                code = e.code or 0
        if expect_exit is not None:
            self.assertEqual(code, expect_exit, out.getvalue())
        return out.getvalue(), code

    def rows(self):
        with (self.data / eidb.CSV_NAME).open(encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))

    def add_doi(self, **extra):
        args = ["add", "--doi", FAKE_DOI["doi"], "--summary", "Adapts the clinical model.",
                "--topics", "clinical-model; medical-analogy", "--criteria", "theory; methods",
                "--role", "foundation", "--status", "S"]
        for k, v in extra.items():
            args += [f"--{k}", v]
        return self.run_cli(*args)


class TestInitAndAdd(EidbTestCase):
    def test_init_creates_structure(self):
        for sub in ("backups", "exports", "drafts"):
            self.assertTrue((self.data / sub).is_dir())
        self.assertEqual(self.rows(), [])

    def test_add_with_doi_uses_registry_metadata(self):
        out, code = self.add_doi()
        self.assertEqual(code, 0, out)
        row = self.rows()[0]
        self.assertEqual(row["id"], "Becher2020Teaching")
        self.assertTrue(row["bibtex"].startswith("@article{Becher2020Teaching,"))
        self.assertEqual(row["verified_via"], "doi")
        self.assertEqual(row["source_status"], "S")
        self.assertEqual(row["ei_criteria"], "theory; methods")

    def test_duplicate_doi_is_rejected(self):
        self.add_doi()
        out, code = self.add_doi()
        self.assertEqual(code, 3)
        self.assertIn("Becher2020Teaching", out)
        self.assertEqual(len(self.rows()), 1)

    def test_manual_entry_builds_apa_and_bibtex(self):
        out, code = self.run_cli(
            "add", "--type", "report", "--authors", "National Center on Intensive Intervention",
            "--year", "2013", "--title", "Data-based individualization: A framework",
            "--venue", "U.S. Department of Education", "--url", "https://example.org/dbi.pdf",
            "--summary", "Framework.", "--status", "D", "--verified-via", "url-check")
        self.assertEqual(code, 0, out)
        row = self.rows()[0]
        self.assertEqual(row["id"], "National2013Data")
        self.assertIn("National Center on Intensive Intervention (2013).", row["apa"])
        self.assertIn("{National Center on Intensive Intervention}", row["bibtex"])
        self.assertTrue(row["bibtex"].startswith("@techreport{National2013Data,"))

    def test_invalid_values_are_rejected(self):
        _, code = self.add_doi(criteria="novelty")
        self.assertEqual(code, 1)
        _, code = self.run_cli("add", "--title", "No summary", "--year", "2020", "--no-fetch")
        self.assertEqual(code, 1)

    def test_extra_columns_survive_rewrite(self):
        self.add_doi()
        path = self.data / eidb.CSV_NAME
        rows = self.rows()
        with path.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=eidb.COLUMNS + ["my_rating"])
            w.writeheader()
            for r in rows:
                w.writerow({**r, "my_rating": "5"})
        self.run_cli("update", "Becher2020Teaching", "--append-note", "checked", expect_exit=0)
        self.assertEqual(self.rows()[0]["my_rating"], "5")
        self.assertIn("checked", self.rows()[0]["notes"])


class TestFormatting(unittest.TestCase):
    def test_apa_names(self):
        self.assertEqual(eidb.apa_name("Becher, Ayelet"), "Becher, A.")
        self.assertEqual(eidb.apa_name("Biesta, G.J.J."), "Biesta, G. J. J.")
        self.assertEqual(eidb.apa_name("Sartre, Jean-Paul"), "Sartre, J.-P.")
        self.assertEqual(eidb.apa_name("UNESCO"), "UNESCO")

    def test_apa_article(self):
        rec = {"authors": "Becher, Ayelet; Lefstein, Adam", "year": "2021", "title": "Teaching",
               "type": "article", "venue": "JTE", "volume": "72", "issue": "4", "pages": "477–488",
               "doi": "10.1/x"}
        self.assertEqual(eidb.format_apa(rec),
                         "Becher, A., & Lefstein, A. (2021). Teaching. JTE, 72(4), 477–488. https://doi.org/10.1/x")

    def test_make_id_skips_stopwords_and_collides(self):
        taken = set()
        a = eidb.make_id("Turner, Laurah", "2024", "It Takes More Than Enthusiasm", taken)
        self.assertEqual(a, "Turner2024Takes")
        taken.add(a)
        self.assertEqual(eidb.make_id("Turner, L.", "2024", "It takes more", taken), "Turner2024Takesb")
        self.assertEqual(eidb.make_id("IVANOVA, Malinka", "2020", "eLearning Informatics", set()),
                         "Ivanova2020Elearning")

    def test_bibtex_key_rewrite(self):
        self.assertEqual(eidb.set_bibtex_key("@article{Becher_2020, title={T} }", "Becher2020Teaching"),
                         "@article{Becher2020Teaching, title={T} }")

    def test_csl_mapping(self):
        rec = eidb.csl_to_record({"type": "journal-article", "author": [{"family": "Kane", "given": "Michael T."}],
                                  "issued": {"date-parts": [[2013, 3]]}, "title": "Validating <i>scores</i>",
                                  "container-title": ["Journal of Educational Measurement"], "page": "1-73",
                                  "DOI": "10.1111/JEDM.12000"})
        self.assertEqual(rec["authors"], "Kane, Michael T.")
        self.assertEqual(rec["year"], "2013")
        self.assertEqual(rec["title"], "Validating scores")
        self.assertEqual(rec["pages"], "1–73")
        self.assertEqual(rec["doi"], "10.1111/jedm.12000")

    def test_front_matter_parser(self):
        meta, body = eidb.parse_front_matter('---\ntitle: A "quoted" title\nrelated: [a/b, "c/d"]\n---\nBody')
        self.assertEqual(meta["title"], 'A "quoted" title')
        self.assertEqual(meta["related"], ["a/b", "c/d"])
        self.assertEqual(body, "Body")

    def test_citations_ignore_code(self):
        text = "See [@A2020X; @B2021Y, p. 3] and `[@NotMe]`.\n```\n[@NorMe]\n```\nmail [x@y.org]"
        self.assertEqual(eidb.citations_in(text), ["A2020X", "B2021Y"])


class TestWikiAndExport(EidbTestCase):
    def write_page(self, key):
        (self.wiki / "concepts" / "test.md").write_text(PAGE.replace("{key}", key), "utf-8")

    def test_validate_sync_and_unknown_keys(self):
        self.add_doi()
        self.write_page("Becher2020Teaching")
        out, code = self.run_cli("validate")
        self.assertEqual(code, 0, out)
        self.assertIn("wiki_pages out of date", out)
        self.run_cli("sync", expect_exit=0)
        self.assertEqual(self.rows()[0]["wiki_pages"], "concepts/test")
        out, code = self.run_cli("validate")
        self.assertEqual(code, 0, out)
        self.assertNotIn("out of date", out)
        self.write_page("Missing2020Key")
        out, code = self.run_cli("validate")
        self.assertEqual(code, 1)
        self.assertIn("@Missing2020Key", out)

    def test_validate_wiki_front_matter_errors(self):
        (self.wiki / "concepts" / "bad.md").write_text("---\ntitle: Bad\nkind: essay\n---\nx", "utf-8")
        out, code = self.run_cli("validate", "--wiki-only")
        self.assertEqual(code, 1)
        self.assertIn("unknown kind 'essay'", out)
        self.assertIn("missing front-matter fields", out)

    def test_rename_updates_wiki(self):
        self.add_doi()
        self.write_page("Becher2020Teaching")
        self.run_cli("rename", "Becher2020Teaching", "Becher2021Clinical", expect_exit=0)
        self.assertEqual(self.rows()[0]["id"], "Becher2021Clinical")
        self.assertTrue(self.rows()[0]["bibtex"].startswith("@article{Becher2021Clinical,"))
        self.assertIn("[@Becher2021Clinical]", (self.wiki / "concepts" / "test.md").read_text("utf-8"))

    def test_export_backup_restore(self):
        self.add_doi()
        self.run_cli("export", expect_exit=0)
        bib = (self.data / "exports" / "library.bib").read_text("utf-8")
        ris = (self.data / "exports" / "library.ris").read_text("utf-8")
        self.assertIn("@article{Becher2020Teaching,", bib)
        self.assertIn("TY  - JOUR", ris)
        self.assertIn("SP  - 477", ris)
        self.assertIn("EP  - 488", ris)
        out, _ = self.run_cli("backup", "--reason", "test")
        backup = Path(out.split("backup: ")[1].strip())
        self.assertTrue(backup.exists())
        self.run_cli("update", "Becher2020Teaching", "--summary", "changed", expect_exit=0)
        self.run_cli("restore", backup.name, expect_exit=0)
        self.assertEqual(self.rows()[0]["summary"], "Adapts the clinical model.")
        self.assertTrue(any("before-restore" in p.name for p in (self.data / "backups").iterdir()))

    def test_wiki_index_block(self):
        self.add_doi()
        self.write_page("Becher2020Teaching")
        (self.wiki / "README.md").write_text(
            "---\ntitle: Index\nkind: index\nstatus: draft\nupdated: 2026-11-03\nsummary: s\n---\n# Index\n", "utf-8")
        self.run_cli("wiki-index", expect_exit=0)
        text = (self.wiki / "README.md").read_text("utf-8")
        self.assertIn(eidb.AUTO_START, text)
        self.assertIn("[Test page](concepts/test.md)", text)
        self.run_cli("wiki-index", expect_exit=0)  # idempotent: one block only
        self.assertEqual((self.wiki / "README.md").read_text("utf-8").count(eidb.AUTO_START), 1)


class TestGuardHook(unittest.TestCase):
    def run_guard(self, path):
        import subprocess
        payload = json.dumps({"tool_name": "Edit", "tool_input": {"file_path": path}})
        env = {**os.environ, "EI_DATA_DIR": "/tmp/ei-test-data"}
        return subprocess.run([sys.executable, str(ROOT / "scripts" / "hooks" / "guard_data.py")],
                              input=payload, capture_output=True, text=True, env=env).returncode

    def test_blocks_database_and_backups(self):
        self.assertEqual(self.run_guard("/tmp/ei-test-data/ei_literature.csv"), 2)
        self.assertEqual(self.run_guard("/tmp/ei-test-data/backups/old.csv"), 2)

    def test_allows_other_files(self):
        self.assertEqual(self.run_guard(str(ROOT / "wiki" / "log.md")), 0)
        self.assertEqual(self.run_guard("/tmp/ei-test-data/drafts/paper.md"), 0)


if __name__ == "__main__":
    unittest.main()
