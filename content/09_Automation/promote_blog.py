#!/usr/bin/env python3
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

try:
    import yaml  # pip install pyyaml
except ImportError:
    print("Install dependency: pip install pyyaml", file=sys.stderr)
    raise SystemExit(1)

FRONT = "---\n"


def split_frontmatter(md: str):
    if md.startswith(FRONT):
        end = md.find("\n---\n", 4)
        if end != -1:
            fm_raw = md[4:end]
            body = md[end + 5 :]
            fm = yaml.safe_load(fm_raw) or {}
            if not isinstance(fm, dict):
                fm = {}
            return fm, body
    return {}, md


def join_frontmatter(fm: dict, body: str) -> str:
    return (
        "---\n"
        + yaml.safe_dump(fm, sort_keys=False).strip()
        + "\n---\n"
        + body.lstrip()
    )


def normalize_tags(tags):
    if tags is None:
        return []
    if isinstance(tags, str):
        return [tags]
    if isinstance(tags, list):
        return [str(t) for t in tags]
    return []


def ensure_blog_frontmatter(fm: dict, src_stem: str):
    tags = normalize_tags(fm.get("tags"))
    if "blog" not in tags:
        tags.append("blog")
    fm["tags"] = tags
    fm.setdefault("title", src_stem)
    fm.setdefault("date", date.today().isoformat())
    return fm


def main() -> int:
    """
    Run from Quartz repo root.

    Promote/copy a note into Blog/Drafts or Blog/Published:

      python3 content/09_Automation/promote_blog.py content/Kubernetes/Kubernetes\ Basics.md
      python3 content/09_Automation/promote_blog.py content/Blog/Drafts/My\ Post.md --publish
    """
    if len(sys.argv) < 2:
        print("Usage: promote_blog.py <path-to-note.md> [--publish]", file=sys.stderr)
        return 2

    note_path = Path(sys.argv[1]).resolve()
    do_publish = "--publish" in sys.argv[2:]

    repo_root = Path.cwd()
    content_root = repo_root / "content"
    if content_root not in note_path.parents:
        print("Error: note must be inside ./content", file=sys.stderr)
        return 2

    blog_drafts = content_root / "Blog" / "Drafts"
    blog_published = content_root / "Blog" / "Published"
    blog_drafts.mkdir(parents=True, exist_ok=True)
    blog_published.mkdir(parents=True, exist_ok=True)

    md = note_path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(md)
    fm = ensure_blog_frontmatter(fm, note_path.stem)

    # Determine destination
    rel = note_path.relative_to(content_root)
    in_blog_drafts = rel.parts[:2] == ("Blog", "Drafts")
    in_blog_published = rel.parts[:2] == ("Blog", "Published")

    if do_publish:
        # publish into Blog/Published + set publish true
        fm["publish"] = True
        dest = blog_published / note_path.name if not in_blog_published else note_path
    else:
        # copy into Blog/Drafts but keep publish false
        fm["publish"] = False
        dest = blog_drafts / note_path.name if not in_blog_drafts else note_path

    out_md = join_frontmatter(fm, body)
    dest.write_text(out_md, encoding="utf-8")

    # If you prefer "move" semantics, uncomment:
    # if dest != note_path: note_path.unlink()

    action = "Published" if do_publish else "Drafted"
    print(f"{action} → {dest.relative_to(repo_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
