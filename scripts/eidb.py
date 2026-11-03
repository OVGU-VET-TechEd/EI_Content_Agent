#!/usr/bin/env python3
"""eidb: the EI_Content_Agent literature database.

A single CSV file is the source of truth for every reference the agent
records. This script is the only thing that should write to it. It needs only
the Python standard library (3.10+).

    python3 scripts/eidb.py init                 create the data folder and an empty CSV
    python3 scripts/eidb.py search "query"       find DOI candidates on Crossref
    python3 scripts/eidb.py fetch DOI            show APA, BibTeX and metadata for a DOI
    python3 scripts/eidb.py add --doi DOI ...    add a reference (APA/BibTeX fetched from the DOI)
    python3 scripts/eidb.py add-batch FILE.json  add many references
    python3 scripts/eidb.py update ID --summary ...
    python3 scripts/eidb.py rename OLD NEW       change a citekey everywhere (CSV, BibTeX, wiki)
    python3 scripts/eidb.py show ID | list | stats | status
    python3 scripts/eidb.py sync                 derive the wiki_pages column from wiki citations
    python3 scripts/eidb.py validate [--wiki-only]
    python3 scripts/eidb.py export               write library.bib, library.ris, references_apa.md
    python3 scripts/eidb.py backup [--reason R]  timestamped copy of the CSV
    python3 scripts/eidb.py restore BACKUP       restore a backup (backs up the current CSV first)
    python3 scripts/eidb.py wiki-index           rebuild the generated index in wiki/README.md

Paths come from ei.config.json in the repository root (see
ei.config.example.json). EI_CONFIG, EI_DATA_DIR and EI_WIKI_DIR override them.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import html
import json
import os
import re
import shutil
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_NAME = "ei_literature.csv"
VERSION = "0.1.0"

COLUMNS = [
    "id", "type", "authors", "year", "title", "venue", "volume", "issue", "pages",
    "doi", "url", "apa", "bibtex", "summary", "topics", "ei_criteria", "ei_role",
    "wiki_pages", "source_status", "verified_via", "local_file", "added_on",
    "added_by_query", "notes",
]
REQUIRED = ["id", "type", "title", "year", "apa", "bibtex", "summary", "source_status"]

TYPES = {"article", "book", "chapter", "report", "conference", "preprint", "thesis",
         "web", "standard", "law", "dataset", "other"}
STATUS = {
    "P": "primary text read directly",
    "R": "cited in the anchor paper; not re-read",
    "S": "confirmed through DOI record, abstract or index; full text not read",
    "D": "from the user's notes or slides; not checked at source",
    "M": "from model memory; unconfirmed",
}
CRITERIA = ["object", "knowledge", "theory", "terminology", "methods", "institutions"]
CRITERIA_LABEL = {
    "object": "C1 Object of research",
    "knowledge": "C2 Accumulated specialist knowledge",
    "theory": "C3 Organising theories and concepts",
    "terminology": "C4 Specific terminology",
    "methods": "C5 Specific research methods",
    "institutions": "C6 Institutional manifestation",
}
ROLES = {"foundation", "evidence", "rival", "critique", "method", "policy-legal", "context"}
VERIFIED_VIA = {"doi", "crossref-search", "publisher-page", "local-pdf", "url-check", "manual"}
WIKI_KINDS = ["index", "log", "discipline", "concept", "approach", "method",
              "proposition", "governance", "rival", "other"]
WIKI_STATUS = {"seed", "draft", "reviewed"}
WIKI_REQUIRED = ["title", "kind", "status", "updated", "summary"]
LIST_FIELDS = {"topics", "ei_criteria", "ei_role", "wiki_pages"}

CSL_TYPE = {
    "journal-article": "article", "article-journal": "article", "article": "article",
    "book": "book", "monograph": "book", "edited-book": "book",
    "book-chapter": "chapter", "chapter": "chapter", "book-section": "chapter",
    "report": "report", "proceedings-article": "conference", "paper-conference": "conference",
    "posted-content": "preprint", "dataset": "dataset", "dissertation": "thesis",
    "thesis": "thesis", "standard": "standard", "legislation": "law", "webpage": "web",
}
BIBTYPE = {"article": "article", "book": "book", "chapter": "incollection",
           "report": "techreport", "conference": "inproceedings", "preprint": "misc",
           "thesis": "phdthesis", "web": "misc", "standard": "misc", "law": "misc",
           "dataset": "misc", "other": "misc"}
RISTYPE = {"article": "JOUR", "book": "BOOK", "chapter": "CHAP", "report": "RPRT",
           "conference": "CPAPER", "preprint": "UNPB", "thesis": "THES", "web": "ELEC",
           "standard": "STAND", "law": "GOVDOC", "dataset": "DATA", "other": "GEN"}
STOPWORDS = {"a", "an", "the", "on", "of", "in", "for", "and", "to", "from", "with", "at", "by",
             "it", "its", "is", "are", "be", "why", "what", "how", "when", "toward", "towards",
             "into", "not", "do", "we", "our", "can", "let", "lets", "focus", "article", "editorial"}

AUTO_START = "<!-- AUTO-INDEX:START (generated by scripts/eidb.py wiki-index; do not edit by hand) -->"
AUTO_END = "<!-- AUTO-INDEX:END -->"
CITE_GROUP = re.compile(r"\[([^\[\]]*@[^\[\]]*)\]")
CITE_KEY = re.compile(r"(?<![\w.])@([A-Za-z][A-Za-z0-9_-]*)")
FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)


# --------------------------------------------------------------------------- config

class Ctx:
    """Resolved paths for one run."""

    def __init__(self) -> None:
        cfg = {"data_dir": str(ROOT / "data"), "literature_dirs": [], "wiki_dir": "wiki", "mailto": ""}
        cfg_path = Path(os.environ.get("EI_CONFIG", ROOT / "ei.config.json"))
        if cfg_path.exists():
            cfg.update(json.loads(cfg_path.read_text("utf-8")))
        if os.environ.get("EI_DATA_DIR"):
            cfg["data_dir"] = os.environ["EI_DATA_DIR"]
        if os.environ.get("EI_WIKI_DIR"):
            cfg["wiki_dir"] = os.environ["EI_WIKI_DIR"]
        self.cfg = cfg
        self.data_dir = Path(cfg["data_dir"]).expanduser()
        wiki = Path(cfg["wiki_dir"]).expanduser()
        self.wiki_dir = wiki if wiki.is_absolute() else ROOT / wiki
        self.csv = self.data_dir / CSV_NAME
        self.backups = self.data_dir / "backups"
        self.exports = self.data_dir / "exports"
        self.literature_dirs = [Path(p).expanduser() for p in cfg.get("literature_dirs", [])]
        self.mailto = cfg.get("mailto", "")


def die(msg: str, code: int = 1) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def today() -> str:
    return dt.date.today().isoformat()


# --------------------------------------------------------------------------- CSV io

def read_db(ctx: Ctx) -> tuple[list[dict], list[str]]:
    """Return (rows, extra_columns). Extra columns added by hand are preserved."""
    if not ctx.csv.exists():
        die(f"no database at {ctx.csv}. Run: python3 scripts/eidb.py init")
    with ctx.csv.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        missing = [c for c in COLUMNS if c not in header]
        if missing:
            die(f"{ctx.csv} is missing columns {missing}")
        extra = [c for c in header if c not in COLUMNS]
        rows = [{**{c: "" for c in COLUMNS + extra},
                 **{k: (v or "") for k, v in row.items() if k is not None}} for row in reader]
    return rows, extra


def write_db(ctx: Ctx, rows: list[dict], extra: list[str]) -> None:
    ctx.data_dir.mkdir(parents=True, exist_ok=True)
    tmp = ctx.csv.with_name(ctx.csv.name + ".tmp")
    with tmp.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS + extra, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({c: row.get(c, "") for c in COLUMNS + extra})
    os.replace(tmp, ctx.csv)


def split_list(value: str) -> list[str]:
    return [x.strip() for x in re.split(r"[;,]", value or "") if x.strip()]


def join_list(items) -> str:
    seen, out = set(), []
    for x in items:
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    return "; ".join(out)


# --------------------------------------------------------------------------- network

def user_agent(ctx: Ctx) -> str:
    ua = f"EI_Content_Agent/{VERSION} (+https://github.com/OVGU-VET-TechEd/EI_Content_Agent)"
    return f"{ua[:-1]}; mailto:{ctx.mailto})" if ctx.mailto else ua


def http_get(ctx: Ctx, url: str, accept: str, timeout: int = 25) -> str:
    req = urllib.request.Request(url, headers={"Accept": accept, "User-Agent": user_agent(ctx)})
    last = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            if e.code in (404, 400, 406):
                raise
            last = e
        except (urllib.error.URLError, TimeoutError) as e:
            last = e
        time.sleep(1.5 * (attempt + 1))
    raise last  # type: ignore[misc]


def normalize_doi(doi: str) -> str:
    doi = (doi or "").strip()
    doi = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:\s*)", "", doi, flags=re.I)
    return doi.strip().rstrip(".").lower()


def clean_text(s: str) -> str:
    s = html.unescape(s or "")
    s = re.sub(r"<[^>]+>", " ", s)          # JATS / HTML tags in abstracts and titles
    return re.sub(r"\s+", " ", s).strip()


def csl_to_record(csl: dict) -> dict:
    """Map CSL-JSON (from doi.org content negotiation) to database fields."""
    def first(v):
        return (v[0] if v else "") if isinstance(v, list) else (v or "")

    authors = []
    for a in csl.get("author") or csl.get("editor") or []:
        if a.get("family"):
            authors.append(f"{a['family']}, {a.get('given', '')}".strip().rstrip(","))
        elif a.get("literal") or a.get("name"):
            authors.append(a.get("literal") or a.get("name"))
    year = ""
    for key in ("issued", "published-print", "published-online", "created"):
        parts = (csl.get(key) or {}).get("date-parts") or [[None]]
        if parts and parts[0] and parts[0][0]:
            year = str(parts[0][0])
            break
    venue = clean_text(first(csl.get("container-title"))) or clean_text(csl.get("publisher", ""))
    return {
        "type": CSL_TYPE.get(csl.get("type", ""), "other"),
        "authors": "; ".join(authors),
        "year": year,
        "title": clean_text(first(csl.get("title"))),
        "venue": venue,
        "volume": str(csl.get("volume", "") or ""),
        "issue": str(csl.get("issue", "") or ""),
        "pages": str(csl.get("page", "") or "").replace("-", "–"),
        "doi": normalize_doi(csl.get("DOI", "")),
        "url": csl.get("URL", "") or "",
        "abstract": clean_text(csl.get("abstract", "")),
    }


def fetch_doi(ctx: Ctx, doi: str) -> dict:
    """Metadata, APA (CSL apa style) and BibTeX for a DOI via doi.org content negotiation.
    Works for Crossref and DataCite DOIs."""
    doi = normalize_doi(doi)
    url = "https://doi.org/" + urllib.parse.quote(doi, safe="/")
    rec = csl_to_record(json.loads(http_get(ctx, url, "application/vnd.citationstyles.csl+json")))
    rec["doi"] = rec["doi"] or doi
    rec["apa"] = clean_text(http_get(ctx, url, "text/x-bibliography; style=apa"))
    rec["bibtex"] = re.sub(r"\s+", " ", http_get(ctx, url, "application/x-bibtex")).strip()
    return rec


def crossref_search(ctx: Ctx, query: str, rows: int = 5) -> list[dict]:
    params = {"query.bibliographic": query, "rows": str(rows),
              "select": "DOI,title,author,issued,container-title,type,score,publisher"}
    if ctx.mailto:
        params["mailto"] = ctx.mailto
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(params)
    items = json.loads(http_get(ctx, url, "application/json"))["message"]["items"]
    out = []
    for it in items:
        rec = csl_to_record(it)
        rec["score"] = round(it.get("score", 0), 1)
        out.append(rec)
    return out


# --------------------------------------------------------------------------- formatting

def ascii_fold(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def make_id(authors: str, year: str, title: str, taken: set[str]) -> str:
    first_author = split_authors(authors)[0] if authors else "Anon"
    family = first_author.split(",")[0] if "," in first_author else first_author.split()[0]
    family = re.sub(r"[^A-Za-z]", "", ascii_fold(family)) or "Anon"
    if family.isupper() and len(family) > 1:
        family = family.capitalize()  # IVANOVA -> Ivanova
    words = [w for w in re.findall(r"[A-Za-z]+", ascii_fold(title))
             if w.lower() not in STOPWORDS and len(w) > 2]
    word = (words[0] if words else "Untitled").capitalize()
    yr = re.sub(r"\D", "", year or "")[:4] or "nd"
    base = f"{family[0].upper()}{family[1:]}{yr}{word}"
    key, n = base, 0
    while key in taken:
        n += 1
        key = base + "abcdefghijklmnopqrstuvwxyz"[n] if n < 26 else f"{base}{n}"
    return key


def split_authors(authors: str) -> list[str]:
    return [a.strip() for a in (authors or "").split(";") if a.strip()]


def apa_name(a: str) -> str:
    """'Becher, Ayelet' -> 'Becher, A.'; 'Biesta, G.J.J.' -> 'Biesta, G. J. J.'; corporate names unchanged."""
    if "," not in a:
        return a
    family, given = [x.strip() for x in a.split(",", 1)]
    initials: list[str] = []
    for part in given.split():
        if re.fullmatch(r"(?:[A-Z]\.)+", part):
            initials += re.findall(r"[A-Z]\.", part)
        else:
            initials.append("-".join(p[0].upper() + "." for p in part.split("-") if p))
    return f"{family}, {' '.join(initials)}" if initials else family


def format_apa(rec: dict) -> str:
    """APA 7 reference built from fields. Used only when no DOI record is available."""
    names = [apa_name(a) for a in split_authors(rec.get("authors", ""))]
    if len(names) == 1:
        who = names[0]
    elif 1 < len(names) <= 20:
        who = ", ".join(names[:-1]) + ", & " + names[-1]
    else:
        who = ", ".join(names[:19]) + ", . . . " + names[-1] if names else ""
    year = rec.get("year") or "n.d."
    title = rec.get("title", "").rstrip(".")
    head = f"{who} ({year}). {title}." if who else f"{title}. ({year})."
    t = rec.get("type", "other")
    venue = rec.get("venue", "")
    if t == "article":
        tail = venue
        if rec.get("volume"):
            tail += f", {rec['volume']}" + (f"({rec['issue']})" if rec.get("issue") else "")
        if rec.get("pages"):
            tail += f", {rec['pages']}"
        tail = f"{tail}." if tail else ""
    elif t == "chapter":
        tail = f"In {venue}" + (f" (pp. {rec['pages']})" if rec.get("pages") else "") + "." if venue else ""
    else:
        tail = f"{venue}." if venue and venue != who else ""
    link = f"https://doi.org/{rec['doi']}" if rec.get("doi") else rec.get("url", "")
    return re.sub(r"\s+", " ", f"{head} {tail} {link}").strip()


def bib_escape(s: str) -> str:
    return s.replace("{", "").replace("}", "").replace("&", r"\&").replace("%", r"\%")


def format_bibtex(rec: dict) -> str:
    t = rec.get("type", "other")
    authors = []
    for a in split_authors(rec.get("authors", "")):
        authors.append(a if "," in a else "{" + a + "}")
    fields = [("author", " and ".join(authors)), ("title", "{" + bib_escape(rec.get("title", "")) + "}"),
              ("year", rec.get("year", ""))]
    venue_field = {"article": "journal", "chapter": "booktitle", "conference": "booktitle",
                   "report": "institution", "book": "publisher", "thesis": "school"}.get(t, "howpublished")
    if rec.get("venue"):
        fields.append((venue_field, bib_escape(rec["venue"])))
    for src, dst in (("volume", "volume"), ("issue", "number"), ("pages", "pages"), ("doi", "doi"), ("url", "url")):
        if rec.get(src):
            val = rec[src].replace("–", "--") if src == "pages" else rec[src]
            fields.append((dst, val))
    body = ", ".join(f"{k}={{{v}}}" for k, v in fields if v)
    return f"@{BIBTYPE.get(t, 'misc')}{{{rec['id']}, {body} }}"


def set_bibtex_key(bib: str, key: str) -> str:
    return re.sub(r"^\s*@(\w+)\s*\{\s*[^,]*,", lambda m: f"@{m.group(1)}{{{key},", bib, count=1)


def norm_title(t: str) -> str:
    return re.sub(r"[^a-z0-9]", "", ascii_fold(t or "").lower())


# --------------------------------------------------------------------------- wiki

def parse_front_matter(text: str) -> tuple[dict | None, str]:
    """Tiny YAML subset: `key: value` and `key: [a, b]` lines only."""
    m = FRONT_MATTER.match(text)
    if not m:
        return None, text
    meta: dict = {}
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        k, _, v = line.partition(":")
        k, v = k.strip(), v.strip()
        if v.startswith("[") and v.endswith("]"):
            meta[k] = [unquote(x.strip()) for x in v[1:-1].split(",") if x.strip()]
        else:
            meta[k] = unquote(v)
    return meta, text[m.end():]


def unquote(v: str) -> str:
    return v[1:-1] if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"" else v


def wiki_pages(ctx: Ctx) -> dict[str, Path]:
    """slug (path relative to wiki dir, without .md) -> file."""
    if not ctx.wiki_dir.exists():
        return {}
    return {p.relative_to(ctx.wiki_dir).with_suffix("").as_posix(): p
            for p in sorted(ctx.wiki_dir.rglob("*.md")) if not p.name.startswith("_")}


CODE = re.compile(r"```.*?```|`[^`\n]*`", re.S)


def citations_in(text: str) -> list[str]:
    """Pandoc-style citation keys, ignoring code blocks and inline code (examples)."""
    keys = []
    for group in CITE_GROUP.findall(CODE.sub("", text)):
        keys += CITE_KEY.findall(group)
    return keys


def wiki_citations(ctx: Ctx) -> dict[str, set[str]]:
    """citekey -> set of page slugs that cite it."""
    out: dict[str, set[str]] = {}
    for slug, path in wiki_pages(ctx).items():
        for key in citations_in(path.read_text("utf-8")):
            out.setdefault(key, set()).add(slug)
    return out


def check_wiki(ctx: Ctx, errors: list[str], warnings: list[str]) -> dict[str, dict]:
    pages = wiki_pages(ctx)
    metas = {}
    for slug, path in pages.items():
        rel = f"wiki/{slug}.md"
        meta, body = parse_front_matter(path.read_text("utf-8"))
        if meta is None:
            errors.append(f"{rel}: missing front matter")
            continue
        metas[slug] = meta
        missing = [k for k in WIKI_REQUIRED if not meta.get(k)]
        if missing:
            errors.append(f"{rel}: missing front-matter fields {missing}")
        if meta.get("kind") and meta["kind"] not in WIKI_KINDS:
            errors.append(f"{rel}: unknown kind {meta['kind']!r} (allowed: {', '.join(WIKI_KINDS)})")
        if meta.get("status") and meta["status"] not in WIKI_STATUS:
            errors.append(f"{rel}: unknown status {meta['status']!r} (allowed: {', '.join(sorted(WIKI_STATUS))})")
        if meta.get("updated") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(meta["updated"])):
            errors.append(f"{rel}: updated must be YYYY-MM-DD")
        for c in meta.get("criteria", []) if isinstance(meta.get("criteria"), list) else []:
            if c not in CRITERIA:
                errors.append(f"{rel}: unknown criterion {c!r} (allowed: {', '.join(CRITERIA)})")
        for r in meta.get("related", []) if isinstance(meta.get("related"), list) else []:
            if r not in pages:
                errors.append(f"{rel}: related page {r!r} does not exist")
        for link in re.findall(r"\]\(([^)#\s]+\.md)(?:#[^)]*)?\)", body):
            if link.startswith(("http://", "https://")):
                continue
            target = (path.parent / link).resolve()
            if not target.exists():
                errors.append(f"{rel}: broken link {link}")
        if "TODO" in body:
            warnings.append(f"{rel}: contains TODO")
    return metas


# --------------------------------------------------------------------------- commands

def cmd_init(ctx: Ctx, args) -> None:
    for d in (ctx.data_dir, ctx.backups, ctx.exports, ctx.data_dir / "drafts"):
        d.mkdir(parents=True, exist_ok=True)
    if ctx.csv.exists():
        print(f"database already exists: {ctx.csv}")
    else:
        write_db(ctx, [], [])
        print(f"created {ctx.csv}")
    readme = ctx.data_dir / "README.md"
    if not readme.exists():
        readme.write_text(
            "# EI knowledge base (private data)\n\n"
            "Written by EI_Content_Agent (`scripts/eidb.py`). Not under version control.\n\n"
            f"- `{CSV_NAME}`: the literature database (one row per reference). Edit only via `eidb.py`.\n"
            "- `backups/`: one timestamped copy per Claude Code session, plus one before every restore.\n"
            "- `exports/`: `library.bib`, `library.ris` (import into Zotero), `references_apa.md`.\n"
            "- `drafts/`: paper and proposal drafts written by the agent.\n", "utf-8")
    print(f"data folder: {ctx.data_dir}")


def cmd_backup(ctx: Ctx, args) -> Path | None:
    if not ctx.csv.exists():
        print("no database yet; nothing to back up")
        return None
    ctx.backups.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    reason = re.sub(r"[^A-Za-z0-9_-]", "-", getattr(args, "reason", "") or "manual")
    dest = ctx.backups / f"ei_literature_{stamp}_{reason}.csv"
    shutil.copy2(ctx.csv, dest)
    keep = getattr(args, "keep", 0) or 0
    if keep > 0:
        olds = sorted(ctx.backups.glob("ei_literature_*.csv"))[:-keep]
        for p in olds:
            p.unlink()
    print(f"backup: {dest}")
    return dest


def cmd_restore(ctx: Ctx, args) -> None:
    src = Path(args.backup)
    if not src.is_absolute():
        src = ctx.backups / src
    if not src.exists():
        die(f"backup not found: {src}")
    args.reason = "before-restore"
    cmd_backup(ctx, args)
    shutil.copy2(src, ctx.csv)
    print(f"restored {src.name} -> {ctx.csv}")


def cmd_fetch(ctx: Ctx, args) -> None:
    try:
        rec = fetch_doi(ctx, args.doi)
    except urllib.error.HTTPError as e:
        die(f"DOI {args.doi} not resolvable ({e.code})")
    if not args.full and rec.get("abstract"):
        rec["abstract"] = rec["abstract"][:1200] + ("…" if len(rec["abstract"]) > 1200 else "")
    print(json.dumps(rec, ensure_ascii=False, indent=2))


def cmd_search(ctx: Ctx, args) -> None:
    for r in crossref_search(ctx, args.query, args.rows):
        authors = "; ".join(split_authors(r["authors"])[:3]) + (" et al." if r["authors"].count(";") >= 3 else "")
        print(f"{r['doi']}\n    {authors} ({r['year']}). {r['title']}. {r['venue']} [{r['type']}, score {r['score']}]")


def build_record(ctx: Ctx, data: dict, rows: list[dict]) -> dict:
    """Assemble a full row from user-supplied fields, fetching DOI metadata when given."""
    aliases = {"criteria": "ei_criteria", "role": "ei_role", "status": "source_status",
               "query": "added_by_query", "wiki": "wiki_pages"}
    data = {aliases.get(k, k): v for k, v in data.items()}
    rec = {c: "" for c in COLUMNS}
    doi = normalize_doi(data.get("doi", ""))
    fetched: dict = {}
    if doi and not data.get("no_fetch"):
        try:
            fetched = fetch_doi(ctx, doi)
        except urllib.error.HTTPError as e:
            raise ValueError(f"DOI {doi} not resolvable ({e.code}); check it or add without --doi")
        except Exception as e:  # network down etc.
            raise ValueError(f"could not fetch DOI {doi}: {e}")
    for c in COLUMNS:
        if c in ("apa", "bibtex"):
            continue
        val = data.get(c)
        if isinstance(val, list):
            val = join_list(val)
        rec[c] = str(val).strip() if val not in (None, "") else str(fetched.get(c, "") or "")
    # Fetched bibliographic data wins over hand-typed data for these fields, unless forced.
    if fetched and not data.get("keep_manual_metadata"):
        for c in ("authors", "year", "title", "venue", "volume", "issue", "pages", "doi"):
            if fetched.get(c):
                rec[c] = fetched[c]
        if not data.get("type"):
            rec["type"] = fetched.get("type", "other")
    rec["doi"] = normalize_doi(rec["doi"])
    if rec["type"] not in TYPES:
        raise ValueError(f"type {rec['type']!r} not in {sorted(TYPES)}")
    if not rec["title"]:
        raise ValueError("a title is required (or a DOI to fetch it from)")
    # duplicates
    for r in rows:
        if rec["doi"] and normalize_doi(r["doi"]) == rec["doi"]:
            raise FileExistsError(r["id"])
        if norm_title(r["title"]) == norm_title(rec["title"]) and (r["year"] == rec["year"] or not rec["year"]):
            raise FileExistsError(r["id"])
    taken = {r["id"] for r in rows}
    rec["id"] = data.get("id") or make_id(rec["authors"], rec["year"], rec["title"], taken)
    if rec["id"] in taken:
        raise ValueError(f"id {rec['id']} already used")
    # A DOI record without authors (e.g. corporate reports) gives an APA string starting with "(".
    authorless_record = bool(fetched) and not fetched.get("authors") and bool(rec["authors"])
    if data.get("apa"):
        rec["apa"] = data["apa"]
    elif fetched.get("apa") and not authorless_record:
        rec["apa"] = fetched["apa"]
    else:
        rec["apa"] = format_apa(rec)
    if data.get("bibtex"):
        rec["bibtex"] = set_bibtex_key(re.sub(r"\s+", " ", data["bibtex"]).strip(), rec["id"])
    elif fetched.get("bibtex") and not authorless_record:
        rec["bibtex"] = set_bibtex_key(fetched["bibtex"], rec["id"])
    else:
        rec["bibtex"] = format_bibtex(rec)
    if not rec["verified_via"]:
        rec["verified_via"] = "doi" if fetched else "manual"
    rec["source_status"] = (rec["source_status"] or "M").upper()
    if rec["source_status"] not in STATUS:
        raise ValueError(f"source_status must be one of {sorted(STATUS)}")
    for c in ("topics", "ei_criteria", "ei_role"):
        rec[c] = join_list(split_list(rec[c]))
    bad = [c for c in split_list(rec["ei_criteria"]) if c not in CRITERIA]
    if bad:
        raise ValueError(f"unknown ei_criteria {bad}; allowed {CRITERIA}")
    bad = [r for r in split_list(rec["ei_role"]) if r not in ROLES]
    if bad:
        raise ValueError(f"unknown ei_role {bad}; allowed {sorted(ROLES)}")
    if not rec["summary"]:
        raise ValueError("a summary is required (1–3 sentences, say what the source is based on)")
    rec["added_on"] = rec["added_on"] or today()
    if fetched.get("abstract") and data.get("print_abstract"):
        print(f"abstract: {fetched['abstract'][:600]}")
    return rec


def args_to_data(args) -> dict:
    keys = ["id", "doi", "type", "authors", "year", "title", "venue", "volume", "issue", "pages",
            "url", "apa", "bibtex", "summary", "topics", "ei_criteria", "ei_role", "source_status",
            "verified_via", "local_file", "added_by_query", "notes"]
    data = {k: getattr(args, k) for k in keys if getattr(args, k, None)}
    data["no_fetch"] = args.no_fetch
    data["keep_manual_metadata"] = args.keep_manual_metadata
    return data


def cmd_add(ctx: Ctx, args) -> None:
    rows, extra = read_db(ctx)
    try:
        rec = build_record(ctx, args_to_data(args), rows)
    except FileExistsError as e:
        print(f"duplicate: already in database as {e.args[0]} (use `update` to change it)")
        sys.exit(3)
    except ValueError as e:
        die(str(e))
    rows.append(rec)
    write_db(ctx, rows, extra)
    print(f"added {rec['id']}  [{rec['source_status']}, via {rec['verified_via']}]\n  {rec['apa']}")


def cmd_add_batch(ctx: Ctx, args) -> None:
    items = json.loads(Path(args.file).read_text("utf-8"))
    rows, extra = read_db(ctx)
    added, dupes, failed = [], [], []
    for i, item in enumerate(items):
        try:
            rec = build_record(ctx, item, rows)
            rows.append(rec)
            added.append(rec["id"])
            print(f"added {rec['id']}")
            if item.get("doi"):
                time.sleep(0.3)  # be polite to doi.org
        except FileExistsError as e:
            dupes.append(f"{item.get('doi') or item.get('title')} -> {e.args[0]}")
        except Exception as e:
            failed.append(f"item {i} ({item.get('doi') or item.get('title', '?')[:50]}): {e}")
    write_db(ctx, rows, extra)
    print(f"\n{len(added)} added, {len(dupes)} duplicate(s), {len(failed)} failed")
    for d in dupes:
        print(f"  duplicate: {d}")
    for f in failed:
        print(f"  FAILED: {f}")
    if failed:
        sys.exit(4)


def find_row(rows: list[dict], key: str) -> dict:
    for r in rows:
        if r["id"] == key or (r["doi"] and r["doi"] == normalize_doi(key)):
            return r
    die(f"no entry {key!r}")
    raise SystemExit  # for type checkers


def cmd_update(ctx: Ctx, args) -> None:
    rows, extra = read_db(ctx)
    row = find_row(rows, args.id)
    changed = []
    for field, value in (args.set or []):
        if field not in COLUMNS or field in ("id", "added_on"):
            die(f"cannot set field {field!r}")
        row[field] = value
        changed.append(field)
    for field in ("summary", "topics", "ei_criteria", "ei_role", "source_status", "verified_via",
                  "local_file", "notes", "url", "apa", "bibtex", "type"):
        val = getattr(args, field, None)
        if val is not None:
            row[field] = val
            changed.append(field)
    for field, attr in (("topics", "add_topics"), ("ei_criteria", "add_criteria"), ("ei_role", "add_role")):
        val = getattr(args, attr, None)
        if val:
            row[field] = join_list(split_list(row[field]) + split_list(val))
            changed.append(field)
    if args.append_note:
        row["notes"] = (row["notes"] + " | " if row["notes"] else "") + f"{today()}: {args.append_note}"
        changed.append("notes")
    if "bibtex" in changed:
        row["bibtex"] = set_bibtex_key(row["bibtex"], row["id"])
    if row["source_status"] not in STATUS:
        die(f"source_status must be one of {sorted(STATUS)}")
    write_db(ctx, rows, extra)
    print(f"updated {row['id']}: {', '.join(sorted(set(changed))) or 'nothing'}")


def cmd_rename(ctx: Ctx, args) -> None:
    """Change a citekey everywhere: CSV id, BibTeX key, and @citations in the wiki."""
    rows, extra = read_db(ctx)
    row = find_row(rows, args.old)
    old, new = row["id"], args.new
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", new):
        die("new id must start with a letter and contain only letters, digits, _ or -")
    if any(r["id"] == new for r in rows):
        die(f"id {new} already exists")
    row["id"] = new
    row["bibtex"] = set_bibtex_key(row["bibtex"], new)
    write_db(ctx, rows, extra)
    pattern = re.compile(r"(?<![\w.])@" + re.escape(old) + r"(?![A-Za-z0-9_-])")
    touched = []
    for slug, path in wiki_pages(ctx).items():
        text = path.read_text("utf-8")
        new_text = pattern.sub("@" + new, text)
        if new_text != text:
            path.write_text(new_text, "utf-8")
            touched.append(slug)
    print(f"renamed {old} -> {new}; wiki pages updated: {', '.join(touched) or 'none'}")


def cmd_show(ctx: Ctx, args) -> None:
    rows, _ = read_db(ctx)
    row = find_row(rows, args.id)
    if args.json:
        print(json.dumps(row, ensure_ascii=False, indent=2))
        return
    for c in COLUMNS:
        if row.get(c):
            print(f"{c:>15}: {row[c]}")


def matches(row: dict, args) -> bool:
    if args.topic and args.topic not in split_list(row["topics"]):
        return False
    if args.status and row["source_status"] not in args.status.upper():
        return False
    if args.criterion and args.criterion not in split_list(row["ei_criteria"]):
        return False
    if args.role and args.role not in split_list(row["ei_role"]):
        return False
    if args.text:
        hay = " ".join(row[c] for c in ("title", "authors", "summary", "topics", "notes")).lower()
        if not all(t in hay for t in args.text.lower().split()):
            return False
    return True


def cmd_list(ctx: Ctx, args) -> None:
    rows, _ = read_db(ctx)
    hits = [r for r in rows if matches(r, args)]
    for r in sorted(hits, key=lambda r: r["id"]):
        if args.ids:
            print(r["id"])
        else:
            print(f"{r['id']:<32} {r['source_status']}  {r['year']:<5} {r['title'][:70]}")
    if not args.ids:
        print(f"-- {len(hits)} of {len(rows)}")


def counts(rows: list[dict], field: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for r in rows:
        for v in split_list(r[field]) if field in LIST_FIELDS else [r[field]]:
            out[v] = out.get(v, 0) + 1
    return dict(sorted(out.items(), key=lambda kv: (-kv[1], kv[0])))


def cmd_stats(ctx: Ctx, args) -> None:
    rows, _ = read_db(ctx)
    print(f"database: {ctx.csv}\nreferences: {len(rows)}")
    print("source status: " + ", ".join(f"{k}={v}" for k, v in counts(rows, "source_status").items()))
    print("verified via:  " + ", ".join(f"{k}={v}" for k, v in counts(rows, "verified_via").items()))
    print("\ndisciplinarity criteria (references tagged):")
    cc = counts(rows, "ei_criteria")
    for c in CRITERIA:
        print(f"  {CRITERIA_LABEL[c]:<40} {cc.get(c, 0)}")
    print("\nroles: " + ", ".join(f"{k}={v}" for k, v in counts(rows, "ei_role").items()))
    print("\ntop topics: " + ", ".join(f"{k} ({v})" for k, v in list(counts(rows, "topics").items())[:25]))
    uncited = [r["id"] for r in rows if not r["wiki_pages"]]
    print(f"\nnot yet discussed in the wiki: {len(uncited)}" + (f" ({', '.join(uncited[:12])}{' …' if len(uncited) > 12 else ''})" if uncited else ""))


def cmd_status(ctx: Ctx, args) -> None:
    """Short summary for the SessionStart hook."""
    pages = wiki_pages(ctx)
    if not ctx.csv.exists():
        print(f"EI knowledge base: no database at {ctx.csv} — run `python3 scripts/eidb.py init` "
              "(and check ei.config.json).")
        return
    rows, _ = read_db(ctx)
    st = counts(rows, "source_status")
    weak = sum(st.get(k, 0) for k in ("D", "M"))
    print(f"EI knowledge base: {len(rows)} references "
          f"({', '.join(f'{k}={v}' for k, v in st.items())}); {len(pages)} wiki pages; "
          f"{weak} references still unverified (D/M). Data: {ctx.data_dir}")


def cmd_sync(ctx: Ctx, args) -> None:
    rows, extra = read_db(ctx)
    cites = wiki_citations(ctx)
    changed = 0
    for r in rows:
        new = "; ".join(sorted(cites.get(r["id"], set())))
        if new != r["wiki_pages"]:
            r["wiki_pages"] = new
            changed += 1
    write_db(ctx, rows, extra)
    unknown = sorted(k for k in cites if k not in {r["id"] for r in rows})
    print(f"wiki_pages updated for {changed} reference(s)")
    if unknown:
        print("wiki cites keys that are not in the database: " + ", ".join(unknown))


def cmd_validate(ctx: Ctx, args) -> None:
    errors: list[str] = []
    warnings: list[str] = []
    check_wiki(ctx, errors, warnings)
    n_rows = 0
    if not args.wiki_only:
        rows, _ = read_db(ctx)
        n_rows = len(rows)
        ids, dois = {}, {}
        pages = wiki_pages(ctx)
        for i, r in enumerate(rows, start=2):
            where = f"csv line {i} ({r.get('id') or '?'})"
            for c in REQUIRED:
                if not r.get(c):
                    errors.append(f"{where}: empty {c}")
            if r["id"] and not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", r["id"]):
                errors.append(f"{where}: id must be letters/digits")
            if r["id"] in ids:
                errors.append(f"{where}: duplicate id (also line {ids[r['id']]})")
            ids[r["id"]] = i
            if r["doi"]:
                if not re.fullmatch(r"10\.\d{4,9}/\S+", r["doi"]):
                    errors.append(f"{where}: malformed doi {r['doi']!r}")
                if r["doi"] in dois:
                    errors.append(f"{where}: duplicate doi (also line {dois[r['doi']]})")
                dois[r["doi"]] = i
            if r["type"] and r["type"] not in TYPES:
                errors.append(f"{where}: unknown type {r['type']!r}")
            if r["source_status"] and r["source_status"] not in STATUS:
                errors.append(f"{where}: unknown source_status {r['source_status']!r}")
            if r["verified_via"] and r["verified_via"] not in VERIFIED_VIA:
                errors.append(f"{where}: unknown verified_via {r['verified_via']!r}")
            for c in split_list(r["ei_criteria"]):
                if c not in CRITERIA:
                    errors.append(f"{where}: unknown criterion {c!r}")
            for c in split_list(r["ei_role"]):
                if c not in ROLES:
                    errors.append(f"{where}: unknown role {c!r}")
            m = re.match(r"\s*@\w+\s*\{\s*([^,\s]+)\s*,", r["bibtex"] or "")
            if r["bibtex"] and (not m or m.group(1) != r["id"]):
                errors.append(f"{where}: bibtex key does not match id")
            for slug in split_list(r["wiki_pages"]):
                if slug not in pages:
                    errors.append(f"{where}: wiki page {slug!r} does not exist")
            if r["local_file"] and ctx.literature_dirs:
                if not any((d / r["local_file"]).exists() for d in ctx.literature_dirs):
                    warnings.append(f"{where}: local_file not found in literature_dirs: {r['local_file']}")
        weak = [r["id"] for r in rows if r["source_status"] in ("D", "M")]
        if weak:
            warnings.append(f"{len(weak)} reference(s) with status D/M; verify before citing: "
                            + ", ".join(weak[:15]) + (" …" if len(weak) > 15 else ""))
        cites = wiki_citations(ctx)
        for key, slugs in sorted(cites.items()):
            if key not in ids:
                errors.append(f"wiki cites unknown key @{key} in {', '.join(sorted(slugs))}")
        stale = [r["id"] for r in rows if set(split_list(r["wiki_pages"])) != cites.get(r["id"], set())]
        if stale:
            warnings.append(f"wiki_pages out of date for {len(stale)} reference(s); run `eidb.py sync`")
    if not args.quiet:
        for w in warnings:
            print(f"warning: {w}")
    for e in errors:
        print(f"error:   {e}")
    scope = "wiki only" if args.wiki_only else f"{n_rows} references"
    print(f"validate ({scope}, {len(wiki_pages(ctx))} wiki pages): {len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1 if errors else 0)


def pages_range(pages: str) -> tuple[str, str]:
    parts = re.split(r"\s*[–-]+\s*", pages or "", maxsplit=1)
    return (parts[0], parts[1] if len(parts) > 1 else "")


def cmd_export(ctx: Ctx, args) -> None:
    rows, _ = read_db(ctx)
    ctx.exports.mkdir(parents=True, exist_ok=True)
    rows = sorted(rows, key=lambda r: r["id"].lower())
    fmt = args.format
    if fmt in ("bib", "all"):
        p = ctx.exports / "library.bib"
        p.write_text(f"% Generated by EI_Content_Agent on {today()} from {CSV_NAME}. Do not edit.\n\n" +
                     "\n\n".join(r["bibtex"] for r in rows) + "\n", "utf-8")
        print(f"wrote {p}")
    if fmt in ("ris", "all"):
        out = []
        for r in rows:
            lines = [f"TY  - {RISTYPE.get(r['type'], 'GEN')}", f"ID  - {r['id']}"]
            lines += [f"AU  - {a}" for a in split_authors(r["authors"])]
            lines += [f"TI  - {r['title']}"]
            if r["venue"]:
                lines.append(("PB  - " if r["type"] in ("book", "report") else "T2  - ") + r["venue"])
            for tag, field in (("PY", "year"), ("VL", "volume"), ("IS", "issue"), ("DO", "doi"), ("UR", "url")):
                if r[field] and not (field == "year" and not re.fullmatch(r"\d{4}", r[field])):
                    lines.append(f"{tag}  - {r[field]}")
            sp, ep = pages_range(r["pages"])
            if sp:
                lines.append(f"SP  - {sp}")
            if ep:
                lines.append(f"EP  - {ep}")
            lines += [f"KW  - {t}" for t in split_list(r["topics"])]
            if r["summary"]:
                lines.append(f"N1  - EI summary [{r['source_status']}]: {r['summary']}")
            lines.append("ER  - ")
            out.append("\n".join(lines))
        p = ctx.exports / "library.ris"
        p.write_text("\n\n".join(out) + "\n", "utf-8")
        print(f"wrote {p}")
    if fmt in ("apa", "all"):
        p = ctx.exports / "references_apa.md"
        body = "\n\n".join(f"{r['apa']} `[{r['id']}, {r['source_status']}]`"
                           for r in sorted(rows, key=lambda r: r["apa"].lower()))
        p.write_text(f"# References (APA)\n\nGenerated {today()} from `{CSV_NAME}`. "
                     "Status codes: " + ", ".join(f"{k} = {v}" for k, v in STATUS.items()) + ".\n\n" + body + "\n", "utf-8")
        print(f"wrote {p}")


def cmd_wiki_index(ctx: Ctx, args) -> None:
    readme = ctx.wiki_dir / "README.md"
    if not readme.exists():
        die(f"{readme} not found")
    errors: list[str] = []
    metas = check_wiki(ctx, errors, [])
    rows = read_db(ctx)[0] if ctx.csv.exists() else None
    lines = [AUTO_START, ""]
    for kind in WIKI_KINDS:
        if kind in ("index", "log"):
            continue
        entries = [(s, m) for s, m in metas.items() if m.get("kind") == kind]
        if not entries:
            continue
        lines.append(f"### {kind.capitalize()} pages\n")
        lines.append("| Page | What it holds | Status | Updated |\n|---|---|---|---|")
        for slug, m in sorted(entries, key=lambda e: e[1].get("title", "")):
            lines.append(f"| [{m.get('title', slug)}]({slug}.md) | {m.get('summary', '')} | {m.get('status', '')} | {m.get('updated', '')} |")
        lines.append("")
    lines.append("### Evidence per disciplinarity criterion\n")
    lines.append("| Criterion | Wiki pages | References tagged |\n|---|---|---|")
    cc = counts(rows, "ei_criteria") if rows is not None else {}
    for c in CRITERIA:
        n_pages = sum(1 for m in metas.values() if c in (m.get("criteria") or []))
        refs = str(cc.get(c, 0)) if rows is not None else "n/a"
        lines.append(f"| {CRITERIA_LABEL[c]} | {n_pages} | {refs} |")
    total = f"{len(rows)} references in the private database" if rows is not None else "database not available"
    lines += ["", f"_Generated {today()}: {len(metas)} pages; {total}._", "", AUTO_END]
    text = readme.read_text("utf-8")
    block = "\n".join(lines)
    if AUTO_START in text and AUTO_END in text:
        text = text[:text.index(AUTO_START)] + block + text[text.index(AUTO_END) + len(AUTO_END):]
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    readme.write_text(text, "utf-8")
    print(f"rebuilt index in {readme} ({len(metas)} pages)")


def cmd_cites(ctx: Ctx, args) -> None:
    """Citations of one wiki page, with their status in the database."""
    pages = wiki_pages(ctx)
    slug = args.page.removesuffix(".md").removeprefix("wiki/")
    if slug not in pages:
        die(f"no wiki page {slug!r}")
    keys = sorted(set(citations_in(pages[slug].read_text("utf-8"))))
    rows = {r["id"]: r for r in read_db(ctx)[0]} if ctx.csv.exists() else {}
    for k in keys:
        r = rows.get(k)
        print(f"{k:<32} {r['source_status'] + '  ' + r['title'][:60] if r else 'MISSING FROM DATABASE'}")


# --------------------------------------------------------------------------- cli

def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="eidb", description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="create the data folder and an empty CSV")
    b = sub.add_parser("backup", help="timestamped copy of the CSV")
    b.add_argument("--reason", default="manual")
    b.add_argument("--keep", type=int, default=0, help="keep only the newest N backups (0 = keep all)")
    r = sub.add_parser("restore", help="restore a backup (current CSV is backed up first)")
    r.add_argument("backup")
    f = sub.add_parser("fetch", help="show APA, BibTeX and metadata for a DOI (no write)")
    f.add_argument("doi")
    f.add_argument("--full", action="store_true", help="do not truncate the abstract")
    s = sub.add_parser("search", help="Crossref bibliographic search")
    s.add_argument("query")
    s.add_argument("--rows", type=int, default=5)

    a = sub.add_parser("add", help="add one reference")
    a.add_argument("--doi")
    a.add_argument("--id", help="override the generated citekey")
    a.add_argument("--type", choices=sorted(TYPES))
    for fld in ("authors", "year", "title", "venue", "volume", "issue", "pages", "url", "apa", "bibtex",
                "summary", "topics", "local_file", "notes"):
        a.add_argument(f"--{fld.replace('_', '-')}", dest=fld)
    a.add_argument("--criteria", dest="ei_criteria", help=f"; separated: {', '.join(CRITERIA)}")
    a.add_argument("--role", dest="ei_role", help=f"; separated: {', '.join(sorted(ROLES))}")
    a.add_argument("--status", dest="source_status", choices=sorted(STATUS))
    a.add_argument("--verified-via", dest="verified_via", choices=sorted(VERIFIED_VIA))
    a.add_argument("--query", dest="added_by_query", help="the user prompt that triggered this entry")
    a.add_argument("--no-fetch", action="store_true", help="do not contact doi.org")
    a.add_argument("--keep-manual-metadata", action="store_true", help="prefer typed fields over DOI metadata")

    ab = sub.add_parser("add-batch", help="add references from a JSON list (same keys as the CSV columns)")
    ab.add_argument("file")

    u = sub.add_parser("update", help="change fields of one reference")
    u.add_argument("id")
    for fld in ("summary", "topics", "local_file", "notes", "url", "apa", "bibtex"):
        u.add_argument(f"--{fld.replace('_', '-')}", dest=fld)
    u.add_argument("--type", choices=sorted(TYPES))
    u.add_argument("--criteria", dest="ei_criteria")
    u.add_argument("--role", dest="ei_role")
    u.add_argument("--status", dest="source_status", choices=sorted(STATUS))
    u.add_argument("--verified-via", dest="verified_via", choices=sorted(VERIFIED_VIA))
    u.add_argument("--add-topics")
    u.add_argument("--add-criteria")
    u.add_argument("--add-role")
    u.add_argument("--append-note")
    u.add_argument("--set", nargs=2, action="append", metavar=("FIELD", "VALUE"))

    rn = sub.add_parser("rename", help="change a citekey in the CSV, its BibTeX and all wiki citations")
    rn.add_argument("old")
    rn.add_argument("new")
    sh = sub.add_parser("show", help="show one reference")
    sh.add_argument("id")
    sh.add_argument("--json", action="store_true")
    ls = sub.add_parser("list", help="list references")
    ls.add_argument("--topic")
    ls.add_argument("--status", help="e.g. DM for unverified")
    ls.add_argument("--criterion", choices=CRITERIA)
    ls.add_argument("--role", choices=sorted(ROLES))
    ls.add_argument("--text", help="words that must all appear in title/authors/summary/topics/notes")
    ls.add_argument("--ids", action="store_true", help="print ids only")
    sub.add_parser("stats", help="counts by status, criterion, role and topic")
    sub.add_parser("status", help="one-line summary (used by the SessionStart hook)")
    sub.add_parser("sync", help="set wiki_pages from the citations found in the wiki")
    v = sub.add_parser("validate", help="check the CSV and the wiki")
    v.add_argument("--wiki-only", action="store_true")
    v.add_argument("--quiet", action="store_true", help="errors only")
    e = sub.add_parser("export", help="write library.bib, library.ris and references_apa.md")
    e.add_argument("--format", choices=["bib", "ris", "apa", "all"], default="all")
    sub.add_parser("wiki-index", help="rebuild the generated index in wiki/README.md")
    c = sub.add_parser("cites", help="citations in one wiki page")
    c.add_argument("page")

    args = p.parse_args(argv)
    ctx = Ctx()
    handler = {
        "init": cmd_init, "backup": cmd_backup, "restore": cmd_restore, "fetch": cmd_fetch,
        "search": cmd_search, "add": cmd_add, "add-batch": cmd_add_batch, "update": cmd_update,
        "rename": cmd_rename, "show": cmd_show, "list": cmd_list, "stats": cmd_stats, "status": cmd_status,
        "sync": cmd_sync, "validate": cmd_validate, "export": cmd_export,
        "wiki-index": cmd_wiki_index, "cites": cmd_cites,
    }[args.cmd]
    handler(ctx, args)


if __name__ == "__main__":
    main()
