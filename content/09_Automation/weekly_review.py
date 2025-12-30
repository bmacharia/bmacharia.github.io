#!/usr/bin/env python3
from __future__ import annotations

import sys
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

try:
    import yaml  # pip install pyyaml
except ImportError:
    print(
        "Missing dependency: pyyaml. Install with: pip install pyyaml", file=sys.stderr
    )
    sys.exit(1)

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
STAGES = [1, 3, 7, 21, 60]

EXCLUDE_TOP = {
    "05_Templates",
    "08_Export",
    "09_Automation",
    "attachments",
    "Blog",  # exclude blog posts from review queue by default
}


@dataclass
class Note:
    path: Path
    title: str
    tags: List[str]
    reviewed: date | None
    stage: int


def parse_frontmatter(md: str) -> Tuple[Dict, str]:
    m = FRONTMATTER_RE.match(md)
    if not m:
        return {}, md
    fm_raw = m.group(1)
    body = md[m.end() :]
    try:
        fm = yaml.safe_load(fm_raw) or {}
    except Exception:
        fm = {}
    return fm, body


def parse_date(s: str) -> date | None:
    try:
        return datetime.strptime(s.strip(), "%Y-%m-%d").date()
    except Exception:
        return None


def normalize_tags(tags) -> List[str]:
    if tags is None:
        return []
    if isinstance(tags, str):
        return [tags]
    if isinstance(tags, list):
        return [str(t) for t in tags]
    return []


def load_note(p: Path) -> Note:
    md = p.read_text(encoding="utf-8")
    fm, _ = parse_frontmatter(md)

    title = (fm.get("title") or p.stem) if isinstance(fm, dict) else p.stem
    tags = normalize_tags(fm.get("tags") if isinstance(fm, dict) else [])
    reviewed = (
        parse_date(str(fm.get("reviewed")))
        if isinstance(fm, dict) and fm.get("reviewed")
        else None
    )

    stage = 1
    if isinstance(fm, dict) and fm.get("review_stage"):
        try:
            stage = int(fm["review_stage"])
        except Exception:
            stage = 1
    if stage not in STAGES:
        stage = 1

    return Note(path=p, title=title, tags=tags, reviewed=reviewed, stage=stage)


def due_date(n: Note) -> date:
    if not n.reviewed:
        return date.min
    return n.reviewed + timedelta(days=n.stage)


def week_id(d: date) -> str:
    iso = d.isocalendar()
    return f"{iso.year}-W{iso.week:02d}"


def top_folder(content_root: Path, p: Path) -> str:
    rel = p.relative_to(content_root)
    return rel.parts[0] if rel.parts else "Other"


def should_skip(content_root: Path, p: Path, n: Note) -> bool:
    if top_folder(content_root, p) in EXCLUDE_TOP:
        return True
    tags = set(n.tags)
    if "private" in tags:
        return True
    return False


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: weekly_review.py <content_root>", file=sys.stderr)
        return 2

    content_root = Path(sys.argv[1]).expanduser().resolve()
    today = date.today()
    this_week_start = today - timedelta(days=today.weekday())
    this_week_end = this_week_start + timedelta(days=6)

    notes: List[Note] = []
    for p in content_root.rglob("*.md"):
        n = load_note(p)
        if should_skip(content_root, p, n):
            continue
        notes.append(n)

    due: List[Note] = []
    upcoming: List[Note] = []

    for n in notes:
        d = due_date(n)
        if d <= this_week_end:
            due.append(n)
        elif d <= this_week_end + timedelta(days=14):
            upcoming.append(n)

    due.sort(key=lambda x: (due_date(x), x.title.lower()))
    upcoming.sort(key=lambda x: (due_date(x), x.title.lower()))

    # Group by top folder (Kubernetes, Docker, 02_Notes, etc.)
    groups: Dict[str, List[Note]] = {}
    for n in due:
        k = top_folder(content_root, n.path)
        groups.setdefault(k, []).append(n)

    out_dir = content_root / "00_Index" / "Weekly_Review"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{week_id(today)}.md"

    def fmt_note(n: Note) -> str:
        rel = n.path.relative_to(content_root)
        d = due_date(n)
        d_str = "NEW" if d == date.min else d.isoformat()
        return (
            f"- [[{rel.as_posix()}|{n.title}]]\n"
            f"  - due: {d_str}, stage: {n.stage}, reviewed: {n.reviewed.isoformat() if n.reviewed else '—'}"
        )

    md: List[str] = []
    md.append(f"# Weekly Review — {week_id(today)}\n")
    md.append(
        f"**Window:** {this_week_start.isoformat()} → {this_week_end.isoformat()}\n"
    )
    md.append("## 1) Due This Week\n")

    for k in sorted(groups.keys()):
        md.append(f"### {k}")
        md.append(
            "\n".join(fmt_note(n) for n in groups[k]) if groups[k] else "- _(none)_"
        )
        md.append("")

    md.append("## 2) Upcoming (Next 2 Weeks)\n")
    if not upcoming:
        md.append("- _(none)_\n")
    else:
        for n in upcoming[:80]:
            rel = n.path.relative_to(content_root)
            md.append(f"- [[{rel.as_posix()}|{n.title}]]")

    md.append("\n## 3) Synthesis Commit\n")
    md.append("- Strengthen one concept: [[00_Index/Knowledge_Index|Knowledge Index]]")
    md.append("- Write/promote one synthesis note: [[04_Synthesis/]]\n")

    md.append("## 4) Mark a note as reviewed\n")
    md.append("Add/update frontmatter in the note:\n")
    md.append("```yaml\nreviewed: YYYY-MM-DD\nreview_stage: 1|3|7|21|60\n```\n")

    out_path.write_text("\n".join(md).strip() + "\n", encoding="utf-8")
    print(f"Generated weekly review: {out_path}")
    print(f"Due this week: {len(due)} | Upcoming: {len(upcoming)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
