#!/usr/bin/env python3
from __future__ import annotations

import csv
import html
import os
import re
import shutil
from dataclasses import dataclass, field
from itertools import islice
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = ROOT / "outputs"
ATLAS_DIR = ROOT / "atlas"
ENTRIES_DIR = ATLAS_DIR / "entries"
ASSETS_DIR = ATLAS_DIR / "assets"

FIG_EXTS = {".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp"}
TABLE_EXTS = {".csv", ".tsv"}
DATA_EXTS = {".json", ".txt", ".log"}
DOC_EXTS = {".md"}
SOURCE_EXTS = {".py"}


CSS = r"""
:root{
  --bg:#0f1116;
  --panel:#171a21;
  --panel-2:#1f2430;
  --text:#e8ecf1;
  --muted:#aab4c3;
  --accent:#79c0ff;
  --accent-2:#c9a227;
  --border:#2a3140;
  --good:#6dd3a0;
  --shadow:0 10px 30px rgba(0,0,0,.28);
  --radius:18px;
  --radius-sm:12px;
  --maxw:1380px;
}

*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0;
  font-family:Inter,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
  background:linear-gradient(180deg,#0d1015 0%, #11151c 100%);
  color:var(--text);
}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
img{max-width:100%;display:block}
code{
  background:#0e131a;
  border:1px solid var(--border);
  border-radius:8px;
  padding:.12rem .38rem;
}
.container{
  width:min(var(--maxw), calc(100% - 2rem));
  margin:0 auto;
}
.site-header{
  position:sticky;
  top:0;
  z-index:20;
  backdrop-filter:blur(10px);
  background:rgba(15,17,22,.82);
  border-bottom:1px solid rgba(255,255,255,.05);
}
.header-inner{
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:1rem;
  padding:.9rem 0;
}
.brand{
  font-weight:800;
  letter-spacing:.02em;
  color:var(--text);
}
.brand small{
  display:block;
  color:var(--muted);
  font-weight:500;
  letter-spacing:0;
}
.nav-links{
  display:flex;
  gap:.75rem;
  flex-wrap:wrap;
}
.button, .button-secondary{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  gap:.45rem;
  padding:.7rem 1rem;
  border-radius:999px;
  border:1px solid var(--border);
  text-decoration:none;
  font-weight:650;
  white-space:nowrap;
}
.button{
  background:var(--accent);
  color:#08111b;
  border-color:transparent;
}
.button:hover{text-decoration:none;filter:brightness(1.06)}
.button-secondary{
  background:var(--panel);
  color:var(--text);
}
.button-secondary:hover{text-decoration:none;background:var(--panel-2)}
.hero{
  padding:2.35rem 0 1.5rem;
}
.hero-grid{
  display:grid;
  grid-template-columns:1.3fr .9fr;
  gap:1.2rem;
}
.panel{
  background:linear-gradient(180deg, rgba(255,255,255,.02), rgba(255,255,255,.01));
  border:1px solid var(--border);
  border-radius:var(--radius);
  box-shadow:var(--shadow);
}
.hero-copy{padding:1.6rem}
.hero h1{
  margin:.15rem 0 .7rem;
  font-size:clamp(1.8rem, 2.6vw, 3rem);
  line-height:1.06;
}
.hero p{
  color:var(--muted);
  font-size:1rem;
  line-height:1.6;
  margin:.5rem 0 0;
}
.hero-side{
  padding:1.4rem;
  display:grid;
  gap:.95rem;
}
.stat-grid{
  display:grid;
  grid-template-columns:repeat(2,minmax(0,1fr));
  gap:.8rem;
}
.stat{
  background:rgba(255,255,255,.03);
  border:1px solid var(--border);
  border-radius:14px;
  padding:.85rem .95rem;
}
.stat .value{
  font-size:1.35rem;
  font-weight:800;
}
.stat .label{
  color:var(--muted);
  font-size:.92rem;
  margin-top:.15rem;
}
.legend{
  display:flex;
  flex-wrap:wrap;
  gap:.55rem;
}
.chip{
  display:inline-flex;
  align-items:center;
  gap:.4rem;
  padding:.4rem .72rem;
  border-radius:999px;
  background:#11161d;
  border:1px solid var(--border);
  color:var(--muted);
  font-size:.88rem;
}
.section{
  padding:1.15rem 0 2rem;
}
.section h2{
  margin:.1rem 0 1rem;
  font-size:1.55rem;
}
.section p.section-note{
  color:var(--muted);
  margin-top:-.35rem;
  margin-bottom:1.25rem;
}
.card-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit, minmax(300px, 1fr));
  gap:1rem;
}
.entry-card{
  display:flex;
  flex-direction:column;
  overflow:hidden;
}
.entry-card .content{
  padding:1rem 1rem 1.05rem;
  display:flex;
  flex-direction:column;
  gap:.8rem;
}
.entry-card h3{
  margin:0;
  font-size:1.08rem;
}
.entry-card .kicker{
  color:var(--accent-2);
  font-size:.85rem;
  font-weight:800;
  letter-spacing:.05em;
  text-transform:uppercase;
}
.entry-card .summary{
  color:var(--muted);
  font-size:.95rem;
  line-height:1.55;
  min-height:4.3rem;
}
.meta-row{
  display:flex;
  flex-wrap:wrap;
  gap:.5rem;
}
.card-preview{
  padding:1rem 1rem 0;
}
.preview-split{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:.75rem;
}
.figure-thumb{
  aspect-ratio:16/10;
  border-radius:14px;
  overflow:hidden;
  border:1px solid var(--border);
  background:#0d1218;
}
.figure-thumb img{
  width:100%;
  height:100%;
  object-fit:cover;
}
.placeholder{
  display:flex;
  align-items:center;
  justify-content:center;
  aspect-ratio:16/10;
  border-radius:14px;
  border:1px dashed var(--border);
  color:var(--muted);
  background:#0d1218;
  font-size:.92rem;
  text-align:center;
  padding:1rem;
}
.preview-table{
  border:1px solid var(--border);
  border-radius:14px;
  overflow:hidden;
  background:#0d1218;
}
.preview-table .table-caption{
  padding:.55rem .75rem;
  font-weight:700;
  border-bottom:1px solid var(--border);
  background:#11161d;
  font-size:.9rem;
}
.preview-table .table-wrap{
  overflow:auto;
  max-height:240px;
}
.preview-table.compact .table-wrap{
  max-height:168px;
}
table{
  width:100%;
  border-collapse:collapse;
  font-size:.88rem;
}
th, td{
  padding:.45rem .55rem;
  border-bottom:1px solid rgba(255,255,255,.05);
  border-right:1px solid rgba(255,255,255,.05);
  text-align:left;
  vertical-align:top;
}
th{
  position:sticky;
  top:0;
  background:#141b24;
  color:#eff4fb;
  z-index:1;
}
tr:last-child td{border-bottom:none}
th:last-child, td:last-child{border-right:none}
.table-note{
  color:var(--muted);
  padding:.6rem .8rem .8rem;
  font-size:.82rem;
}
.entry-actions{
  display:flex;
  flex-wrap:wrap;
  gap:.7rem;
  margin-top:auto;
}
.entry-hero{
  padding:1.45rem 0 1rem;
}
.breadcrumbs{
  color:var(--muted);
  font-size:.92rem;
  margin-bottom:.65rem;
}
.entry-header-card{
  padding:1.25rem;
}
.entry-title-row{
  display:flex;
  justify-content:space-between;
  align-items:flex-start;
  gap:1rem;
  flex-wrap:wrap;
}
.entry-title-row h1{
  margin:.15rem 0 .2rem;
  font-size:clamp(1.55rem,2.2vw,2.35rem);
}
.entry-subsummary{
  color:var(--muted);
  line-height:1.6;
  max-width:1000px;
}
.entry-stats{
  display:flex;
  flex-wrap:wrap;
  gap:.55rem;
  margin-top:.9rem;
}
.two-col{
  display:grid;
  grid-template-columns:1.55fr .95fr;
  gap:1rem;
}
.gallery{
  display:grid;
  grid-template-columns:repeat(auto-fit, minmax(240px,1fr));
  gap:1rem;
}
.figure-card{
  overflow:hidden;
}
.figure-card .frame{
  aspect-ratio:16/10;
  background:#0d1218;
  border-bottom:1px solid var(--border);
}
.figure-card .frame img{
  width:100%;
  height:100%;
  object-fit:cover;
  cursor:zoom-in;
}
.figure-card .caption{
  padding:.85rem .9rem 1rem;
}
.figure-card .caption h4{
  margin:0 0 .45rem;
  font-size:.96rem;
}
.figure-card .caption .caption-links{
  display:flex;
  gap:.8rem;
  flex-wrap:wrap;
  font-size:.9rem;
}
.file-list{
  list-style:none;
  margin:0;
  padding:0;
  display:grid;
  gap:.6rem;
}
.file-list li{
  background:#0f141b;
  border:1px solid var(--border);
  border-radius:12px;
  padding:.7rem .85rem;
}
.file-name{
  font-weight:700;
  word-break:break-word;
}
.file-meta{
  color:var(--muted);
  font-size:.86rem;
  margin-top:.18rem;
}
.stack{
  display:grid;
  gap:1rem;
}
.footer{
  padding:2rem 0 2.4rem;
  color:var(--muted);
  font-size:.92rem;
}
.lightbox{
  position:fixed;
  inset:0;
  display:none;
  align-items:center;
  justify-content:center;
  padding:2rem;
  background:rgba(0,0,0,.84);
  z-index:200;
}
.lightbox.open{display:flex}
.lightbox img{
  max-width:min(94vw, 1500px);
  max-height:88vh;
  border-radius:14px;
  box-shadow:0 20px 55px rgba(0,0,0,.5);
}
.lightbox-close{
  position:absolute;
  top:1rem;
  right:1rem;
  border:none;
  border-radius:999px;
  padding:.75rem 1rem;
  cursor:pointer;
  background:#fff;
  color:#111;
  font-weight:800;
}
.note{
  padding:.85rem 1rem;
  border-left:4px solid var(--accent-2);
  background:#121821;
  border-radius:12px;
  color:var(--muted);
}
.small{
  font-size:.85rem;
  color:var(--muted);
}
@media (max-width:1080px){
  .hero-grid,.two-col{grid-template-columns:1fr}
}
@media (max-width:680px){
  .container{width:min(var(--maxw), calc(100% - 1rem))}
  .preview-split{grid-template-columns:1fr}
  .header-inner{align-items:flex-start;flex-direction:column}
}
"""

JS = r"""
document.addEventListener("DOMContentLoaded", () => {
  const box = document.getElementById("lightbox");
  if (!box) return;
  const boxImg = box.querySelector("img");
  const closeBtn = box.querySelector(".lightbox-close");

  function closeLightbox() {
    box.classList.remove("open");
    boxImg.src = "";
    boxImg.alt = "";
  }

  document.querySelectorAll(".lightbox-trigger").forEach(img => {
    img.addEventListener("click", () => {
      boxImg.src = img.dataset.full || img.src;
      boxImg.alt = img.alt || "";
      box.classList.add("open");
    });
  });

  closeBtn?.addEventListener("click", closeLightbox);

  box.addEventListener("click", (ev) => {
    if (ev.target === box) closeLightbox();
  });

  document.addEventListener("keydown", (ev) => {
    if (ev.key === "Escape") closeLightbox();
  });
});
"""


@dataclass
class Entry:
    number: int
    slug: str
    path: Path
    title: str
    summary: str
    notes: list[Path] = field(default_factory=list)
    sources: list[Path] = field(default_factory=list)
    figures: list[Path] = field(default_factory=list)
    tables: list[Path] = field(default_factory=list)
    data_files: list[Path] = field(default_factory=list)
    misc_files: list[Path] = field(default_factory=list)
    cover: Path | None = None


def entry_number_from_name(name: str) -> int:
    m = re.search(r"(\d+)$", name)
    return int(m.group(1)) if m else 999


def sort_key(path: Path):
    return (entry_number_from_name(path.name), path.name.lower())


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def human_count(n: int, singular: str, plural: str | None = None) -> str:
    if n == 1:
        return f"1 {singular}"
    return f"{n} {plural or singular + 's'}"


def file_size_str(path: Path) -> str:
    size = path.stat().st_size
    units = ["B", "KB", "MB", "GB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(value)} {unit}"
            return f"{value:.1f} {unit}"
        value /= 1024.0
    return f"{size} B"


def rel_href(page_path: Path, target_path: Path) -> str:
    return os.path.relpath(target_path, start=page_path.parent).replace(os.sep, "/")


def parse_note_file(note_path: Path) -> tuple[str | None, str | None]:
    text = note_path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    headings = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            headings.append(clean_text(re.sub(r"^#+\s*", "", stripped)))

    title = None
    if headings:
        if len(headings) >= 2 and "Entry" in headings[0]:
            title = headings[1]
        else:
            title = headings[0]

    summary = None
    in_code = False
    current_paragraph: list[str] = []
    paragraphs: list[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if not stripped or stripped.startswith("#"):
            if current_paragraph:
                paragraphs.append(clean_text(" ".join(current_paragraph)))
                current_paragraph = []
            continue
        current_paragraph.append(stripped)

    if current_paragraph:
        paragraphs.append(clean_text(" ".join(current_paragraph)))

    if paragraphs:
        summary = paragraphs[0]

    return title, summary


def parse_python_docstring(py_path: Path) -> tuple[str | None, str | None]:
    text = py_path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r'^[\sruRUbBfF]*("""|\'\'\')(?P<body>.*?)(\1)', text, flags=re.S)
    if not m:
        return None, None

    lines = [line.strip() for line in m.group("body").splitlines()]
    lines = [line for line in lines if line]

    if not lines:
        return None, None

    if len(lines) >= 2 and "Entry" in lines[0]:
        title = lines[1]
        remainder = lines[2:]
    else:
        title = lines[0]
        remainder = lines[1:]

    filtered = []
    for line in remainder:
        if set(line) == {"-"}:
            continue
        if len(filtered) >= 3:
            break
        filtered.append(line)

    summary = clean_text(" ".join(filtered)) if filtered else None
    return title, summary


def choose_cover(figures: list[Path]) -> Path | None:
    if not figures:
        return None
    preferred = [".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif"]
    for ext in preferred:
        for fig in figures:
            if fig.suffix.lower() == ext:
                return fig
    return figures[0]


def discover_entries() -> list[Entry]:
    if not OUTPUTS_DIR.exists():
        raise FileNotFoundError(f"Missing outputs directory: {OUTPUTS_DIR}")

    entry_dirs = sorted(
        [p for p in OUTPUTS_DIR.iterdir() if p.is_dir() and p.name.startswith("entry_")],
        key=sort_key,
    )

    entries: list[Entry] = []

    for entry_dir in entry_dirs:
        number = entry_number_from_name(entry_dir.name)
        root_files = sorted([p for p in entry_dir.iterdir() if p.is_file()], key=lambda p: p.name.lower())
        notes = [p for p in root_files if p.suffix.lower() in DOC_EXTS]
        sources = [p for p in root_files if p.suffix.lower() in SOURCE_EXTS]

        output_dir = entry_dir / "output"
        if output_dir.exists():
            artifact_files = sorted(
                [p for p in output_dir.rglob("*") if p.is_file()],
                key=lambda p: p.as_posix().lower(),
            )
        else:
            artifact_files = [
                p for p in root_files
                if p.suffix.lower() not in DOC_EXTS | SOURCE_EXTS
            ]

        figures = [p for p in artifact_files if p.suffix.lower() in FIG_EXTS]
        tables = [p for p in artifact_files if p.suffix.lower() in TABLE_EXTS]
        data_files = [p for p in artifact_files if p.suffix.lower() in DATA_EXTS]
        misc_files = [
            p for p in artifact_files
            if p.suffix.lower() not in (FIG_EXTS | TABLE_EXTS | DATA_EXTS)
        ]

        title = None
        summary = None

        for note in notes:
            title, summary = parse_note_file(note)
            if title or summary:
                break

        if not title or not summary:
            for src in sources:
                py_title, py_summary = parse_python_docstring(src)
                if not title and py_title:
                    title = py_title
                if not summary and py_summary:
                    summary = py_summary
                if title and summary:
                    break

        if not title:
            title = f"Entry {number:02d}"
        if not summary:
            summary = "Computational entry in the EDF Dynamic Closure sequence."

        entries.append(
            Entry(
                number=number,
                slug=entry_dir.name,
                path=entry_dir,
                title=title,
                summary=summary,
                notes=notes,
                sources=sources,
                figures=figures,
                tables=tables,
                data_files=data_files,
                misc_files=misc_files,
                cover=choose_cover(figures),
            )
        )

    return entries


def read_delimited_preview(path: Path, max_rows: int = 6, max_cols: int = 8):
    try:
        text = path.read_text(encoding="utf-8-sig", errors="ignore")
    except Exception:
        return None

    if not text.strip():
        return {"header": [], "rows": [], "truncated_cols": False, "truncated_rows": False}

    lines = text.splitlines()
    sample = "\n".join(lines[:10])

    delimiter = "\t" if path.suffix.lower() == ".tsv" else ","
    if path.suffix.lower() == ".csv":
        try:
            dialect = csv.Sniffer().sniff(sample)
            delimiter = dialect.delimiter
        except Exception:
            delimiter = ","

    reader = csv.reader(lines, delimiter=delimiter)
    rows = list(islice(reader, max_rows + 2))
    if not rows:
        return {"header": [], "rows": [], "truncated_cols": False, "truncated_rows": False}

    header = rows[0]
    body = rows[1:max_rows + 1]
    truncated_rows = len(rows) > (max_rows + 1)
    truncated_cols = len(header) > max_cols

    if truncated_cols:
        header = header[:max_cols] + ["…"]
    else:
        header = header[:max_cols]

    normalized_rows = []
    for row in body:
        row = row[:max_cols]
        if truncated_cols:
            row = row + ["…"]
        while len(row) < len(header):
            row.append("")
        normalized_rows.append(row)

    return {
        "header": header,
        "rows": normalized_rows,
        "truncated_cols": truncated_cols,
        "truncated_rows": truncated_rows,
    }


def render_table_preview(page_path: Path, csv_path: Path, compact: bool = False) -> str:
    preview = read_delimited_preview(csv_path, max_rows=4 if compact else 6, max_cols=4 if compact else 8)
    href = rel_href(page_path, csv_path)
    title = html.escape(csv_path.name)

    if preview is None:
        return (
            f'<div class="preview-table{" compact" if compact else ""}">'
            f'<div class="table-caption"><a href="{href}">{title}</a></div>'
            f'<div class="table-note">Preview unavailable.</div>'
            f"</div>"
        )

    header = preview["header"]
    rows = preview["rows"]
    truncated_rows = preview["truncated_rows"]
    truncated_cols = preview["truncated_cols"]

    if not header:
        return (
            f'<div class="preview-table{" compact" if compact else ""}">'
            f'<div class="table-caption"><a href="{href}">{title}</a></div>'
            f'<div class="table-note">Empty table.</div>'
            f"</div>"
        )

    thead = "".join(f"<th>{html.escape(col)}</th>" for col in header)
    tbody = "".join(
        "<tr>" + "".join(f"<td>{html.escape(cell)}</td>" for cell in row) + "</tr>"
        for row in rows
    )

    notes = []
    if truncated_cols:
        notes.append("columns truncated")
    if truncated_rows:
        notes.append("rows truncated")

    note_text = "Preview only"
    if notes:
        note_text += " — " + ", ".join(notes)
    note_text += f'. <a href="{href}">Open full file</a>'

    return (
        f'<div class="preview-table{" compact" if compact else ""}">'
        f'<div class="table-caption"><a href="{href}">{title}</a></div>'
        f'<div class="table-wrap"><table><thead><tr>{thead}</tr></thead>'
        f"<tbody>{tbody}</tbody></table></div>"
        f'<div class="table-note">{note_text}</div>'
        f"</div>"
    )


def render_file_list(page_path: Path, files: list[Path]) -> str:
    if not files:
        return '<div class="note">No files in this category.</div>'

    items = []
    for f in files:
        href = rel_href(page_path, f)
        items.append(
            "<li>"
            f'<div class="file-name"><a href="{href}">{html.escape(f.name)}</a></div>'
            f'<div class="file-meta">{html.escape(file_size_str(f))}</div>'
            "</li>"
        )

    return f'<ul class="file-list">{"".join(items)}</ul>'


def page_shell(title: str, body: str, css_href: str, js_href: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="EDF Dynamic Closure computational atlas">
  <link rel="stylesheet" href="{css_href}">
</head>
<body>
  {body}
  <div id="lightbox" class="lightbox" aria-hidden="true">
    <button class="lightbox-close" type="button">Close</button>
    <img src="" alt="">
  </div>
  <script src="{js_href}"></script>
</body>
</html>
"""


def render_overview_page(entries: list[Entry]) -> str:
    page_path = ATLAS_DIR / "index.html"
    total_figures = sum(len(e.figures) for e in entries)
    total_tables = sum(len(e.tables) for e in entries)
    total_data = sum(len(e.data_files) for e in entries)
    total_sources = sum(len(e.sources) for e in entries)

    cards = []
    for entry in entries:
        entry_page = ENTRIES_DIR / f"{entry.slug}.html"
        entry_href = rel_href(page_path, entry_page)

        preview_blocks = []
        if entry.cover:
            cover_href = rel_href(page_path, entry.cover)
            preview_blocks.append(
                f'<div class="figure-thumb"><img src="{cover_href}" alt="{html.escape(entry.title)} preview"></div>'
            )
        else:
            preview_blocks.append('<div class="placeholder">No figure preview available</div>')

        if entry.tables:
            preview_blocks.append(render_table_preview(page_path, entry.tables[0], compact=True))
        else:
            preview_blocks.append('<div class="placeholder">No table preview available</div>')

        cards.append(
            f"""
            <article class="entry-card panel">
              <div class="card-preview">
                <div class="preview-split">
                  {preview_blocks[0]}
                  {preview_blocks[1]}
                </div>
              </div>
              <div class="content">
                <div class="kicker">Entry {entry.number:02d}</div>
                <h3>{html.escape(entry.title)}</h3>
                <div class="summary">{html.escape(entry.summary)}</div>
                <div class="meta-row">
                  <span class="chip">{human_count(len(entry.figures), "figure")}</span>
                  <span class="chip">{human_count(len(entry.tables), "table")}</span>
                  <span class="chip">{human_count(len(entry.data_files), "data file")}</span>
                  <span class="chip">{human_count(len(entry.sources), "source file")}</span>
                </div>
                <div class="entry-actions">
                  <a class="button" href="{entry_href}">Explore entry</a>
                </div>
              </div>
            </article>
            """
        )

    body = f"""
    <header class="site-header">
      <div class="container header-inner">
        <div class="brand">
          EDF Dynamic Closure — Computational Atlas
          <small>Interactive visual index for notebook Entries 01–16</small>
        </div>
        <nav class="nav-links">
        <a class="button-secondary" href="../README.md">Repository README</a>
        <a class="button-secondary" href="#entries">Entries</a>
        </nav>
      </div>
    </header>

    <main>
      <section class="hero">
        <div class="container hero-grid">
          <div class="panel hero-copy">
            <div class="kicker">Atlas overview</div>
            <h1>Computational Atlas of the EDF Dynamic Closure Notebook</h1>
            <p>
              This atlas provides a compact visual map of the complete Entry 01–16
              output corpus. Each card leads to an entry page with enlarged figures,
              table previews, and direct links to the underlying raw files and source code.
            </p>
            <p>
              The repository README remains the narrative front door; this atlas is the
              evidence map.
            </p>
            <div class="entry-actions" style="margin-top:1rem">
              <a class="button" href="#entries">Browse the entries</a>
            </div>
          </div>

          <aside class="panel hero-side">
            <div class="stat-grid">
              <div class="stat">
                <div class="value">{len(entries)}</div>
                <div class="label">entries discovered</div>
              </div>
              <div class="stat">
                <div class="value">{total_figures}</div>
                <div class="label">figures</div>
              </div>
              <div class="stat">
                <div class="value">{total_tables}</div>
                <div class="label">tables</div>
              </div>
              <div class="stat">
                <div class="value">{total_data + total_sources}</div>
                <div class="label">data/source files</div>
              </div>
            </div>
            <div class="legend">
              <span class="chip">Figures are clickable in each entry page</span>
              <span class="chip">CSV previews are embedded</span>
              <span class="chip">Entry 15 is treated as consolidation/architecture</span>
            </div>
          </aside>
        </div>
      </section>

      <section class="section" id="entries">
        <div class="container">
          <h2>Entries 01–16</h2>
          <p class="section-note">
            Each entry card shows one graphical miniature and one table miniature whenever available.
          </p>
          <div class="card-grid">
            {''.join(cards)}
          </div>
        </div>
      </section>
    </main>

    <footer class="footer">
      <div class="container">
        Generated automatically from the <code>outputs/</code> directory by <code>tools/build_atlas.py</code>.
      </div>
    </footer>
    """

    return page_shell(
        "EDF Dynamic Closure — Computational Atlas",
        body,
        css_href="assets/style.css",
        js_href="assets/viewer.js",
    )


def render_entry_page(entries: list[Entry], idx: int) -> str:
    entry = entries[idx]
    page_path = ENTRIES_DIR / f"{entry.slug}.html"
    overview_href = rel_href(page_path, ATLAS_DIR / "index.html")

    prev_link = ""
    next_link = ""
    if idx > 0:
        prev_link = rel_href(page_path, ENTRIES_DIR / f"{entries[idx-1].slug}.html")
    if idx < len(entries) - 1:
        next_link = rel_href(page_path, ENTRIES_DIR / f"{entries[idx+1].slug}.html")

    figure_cards = []
    for fig in entry.figures:
        fig_href = rel_href(page_path, fig)
        figure_cards.append(
            f"""
            <article class="figure-card panel">
              <div class="frame">
                <img class="lightbox-trigger" src="{fig_href}" data-full="{fig_href}"
                     alt="{html.escape(fig.name)}">
              </div>
              <div class="caption">
                <h4>{html.escape(fig.name)}</h4>
                <div class="caption-links">
                  <a href="{fig_href}">Open image</a>
                </div>
              </div>
            </article>
            """
        )

    tables_html = (
        "".join(render_table_preview(page_path, table) for table in entry.tables)
        if entry.tables else
        '<div class="note">No CSV/TSV tables were found for this entry.</div>'
    )

    source_block = render_file_list(page_path, entry.sources)
    notes_block = render_file_list(page_path, entry.notes)
    data_block = render_file_list(page_path, entry.data_files)
    misc_block = render_file_list(page_path, entry.misc_files)

    nav_buttons = []
    if prev_link:
        nav_buttons.append(f'<a class="button-secondary" href="{prev_link}">← Previous entry</a>')
    nav_buttons.append(f'<a class="button-secondary" href="{overview_href}">Atlas overview</a>')
    if next_link:
        nav_buttons.append(f'<a class="button-secondary" href="{next_link}">Next entry →</a>')

    cover_panel = ""
    if entry.cover:
        cover_href = rel_href(page_path, entry.cover)
        cover_panel = f"""
        <div class="panel" style="overflow:hidden">
          <div class="frame" style="aspect-ratio:16/10">
            <img class="lightbox-trigger" src="{cover_href}" data-full="{cover_href}" alt="{html.escape(entry.title)} cover">
          </div>
        </div>
        """

    body = f"""
    <header class="site-header">
      <div class="container header-inner">
        <div class="brand">
          EDF Dynamic Closure — Computational Atlas
          <small>{html.escape(entry.slug)}</small>
        </div>
        <nav class="nav-links">
          {''.join(nav_buttons)}
        </nav>
      </div>
    </header>

    <main>
      <section class="entry-hero">
        <div class="container">
          <div class="breadcrumbs">
            <a href="{overview_href}">Atlas</a> / Entry {entry.number:02d}
          </div>

          <div class="panel entry-header-card">
            <div class="entry-title-row">
              <div>
                <div class="kicker">Entry {entry.number:02d}</div>
                <h1>{html.escape(entry.title)}</h1>
              </div>
              <div class="meta-row">
                <span class="chip">{human_count(len(entry.figures), "figure")}</span>
                <span class="chip">{human_count(len(entry.tables), "table")}</span>
                <span class="chip">{human_count(len(entry.data_files), "data file")}</span>
                <span class="chip">{human_count(len(entry.notes), "note")}</span>
                <span class="chip">{human_count(len(entry.sources), "source file")}</span>
              </div>
            </div>

            <p class="entry-subsummary">{html.escape(entry.summary)}</p>

            <div class="entry-stats">
              <span class="chip">{entry.slug}</span>
              <span class="chip">Outputs folder: {html.escape((entry.path / "output").name if (entry.path / "output").exists() else entry.path.name)}</span>
            </div>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="container two-col">
          <div class="stack">
            <div>
              <h2>Figures</h2>
              <p class="section-note">Click any figure to enlarge it.</p>
              <div class="gallery">
                {''.join(figure_cards) if figure_cards else '<div class="note">No figures found for this entry.</div>'}
              </div>
            </div>

            <div>
              <h2>Tables</h2>
              <p class="section-note">Embedded previews of CSV/TSV outputs with links to the full raw files.</p>
              <div class="stack">
                {tables_html}
              </div>
            </div>
          </div>

          <div class="stack">
            {cover_panel}

            <div class="panel" style="padding:1rem">
              <h2 style="margin-top:0">Source files</h2>
              {source_block}
            </div>

            <div class="panel" style="padding:1rem">
              <h2 style="margin-top:0">Theoretical notes</h2>
              {notes_block}
            </div>

            <div class="panel" style="padding:1rem">
              <h2 style="margin-top:0">Data files</h2>
              {data_block}
            </div>

            <div class="panel" style="padding:1rem">
              <h2 style="margin-top:0">Other artifacts</h2>
              {misc_block}
            </div>
          </div>
        </div>
      </section>
    </main>

    <footer class="footer">
      <div class="container">
        Generated automatically from <code>{html.escape(entry.path.as_posix())}</code>.
      </div>
    </footer>
    """

    return page_shell(
        f"EDF Atlas — Entry {entry.number:02d}",
        body,
        css_href="../assets/style.css",
        js_href="../assets/viewer.js",
    )


def write_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main():
    entries = discover_entries()

    if ATLAS_DIR.exists():
        shutil.rmtree(ATLAS_DIR)

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    ENTRIES_DIR.mkdir(parents=True, exist_ok=True)

    write_text(ASSETS_DIR / "style.css", CSS)
    write_text(ASSETS_DIR / "viewer.js", JS)

    write_text(ATLAS_DIR / "index.html", render_overview_page(entries))

    for idx, _entry in enumerate(entries):
        write_text(ENTRIES_DIR / f"{_entry.slug}.html", render_entry_page(entries, idx))

    write_text(
        ROOT / "index.html",
        """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="0; url=atlas/index.html">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>EDF Dynamic Closure — Computational Atlas</title>
</head>
<body style="font-family:Arial,Helvetica,sans-serif;padding:2rem">
  <p>Redirecting to <a href="atlas/index.html">atlas/index.html</a> ...</p>
</body>
</html>
""",
    )

    write_text(ROOT / ".nojekyll", "")

    print("Atlas generated successfully.")
    print(f"Entries found: {len(entries)}")
    print(f"Atlas folder: {ATLAS_DIR}")
    print("Created:")
    print("  - atlas/index.html")
    print("  - atlas/entries/*.html")
    print("  - atlas/assets/style.css")
    print("  - atlas/assets/viewer.js")
    print("  - index.html (redirect)")
    print("  - .nojekyll")


if __name__ == "__main__":
    main()
