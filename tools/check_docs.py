#!/usr/bin/env python3
"""Validate local Markdown links and required documentation structure.

Uses only the Python standard library. Does not fetch external URLs.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
MD_LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+[\"'][^\"']+[\"'])?\)")
HTML_ATTR = re.compile(r"\b(?:href|src)=[\"']([^\"']+)[\"']")
REQUIRED = [
    ROOT / "README.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "LICENSE",
    ROOT / "assets" / "hero.svg",
    *[ROOT / "docs" / f"{i:02d}-{name}.md" for i, name in enumerate([
        "start-here", "ps2-architecture", "disc-and-formats",
        "reverse-engineering", "code-reconstruction", "asset-pipeline",
        "xbox360-architecture", "platform-porting", "build-and-xex",
        "testing", "roadmap", "legal", "troubleshooting",
        "glossary", "references",
    ])],
]


def is_external(link: str) -> bool:
    return link.startswith(("#", "//")) or bool(urlsplit(link).scheme)


def check_link(source: Path, link: str) -> str | None:
    link = html.unescape(link)
    if not link or is_external(link):
        return None
    relative = unquote(link.split("#", 1)[0].split("?", 1)[0])
    if not relative:
        return None
    target = (source.parent / relative).resolve()
    if not target.is_relative_to(ROOT.resolve()):
        return f"{source.relative_to(ROOT)}: link escapes repository: {link}"
    if not target.exists():
        return f"{source.relative_to(ROOT)}: broken link: {link}"
    return None


def main() -> int:
    problems: list[str] = []
    for path in REQUIRED:
        if not path.is_file():
            problems.append(f"Required file missing: {path.relative_to(ROOT)}")

    pages = sorted(ROOT.rglob("*.md"))
    for page in pages:
        if ".git" in page.parts:
            continue
        content = page.read_text(encoding="utf-8")
        for match in (*MD_LINK.finditer(content), *HTML_ATTR.finditer(content)):
            err = check_link(page, match.group(1))
            if err:
                problems.append(err)

    if problems:
        print("Documentation check failed:")
        print("\n".join(f"  - {item}" for item in sorted(set(problems))))
        return 1

    print(f"Documentation check passed: {len(pages)} Markdown files validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
