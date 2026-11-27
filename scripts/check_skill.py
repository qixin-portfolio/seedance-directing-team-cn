#!/usr/bin/env python3
"""Consistency checks for the seedance-directing-team-cn skill itself."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STALE_FILES = ("acting-system.md", "scene-geography.md", "continuity-and-review.md", "continuity-and-learning.md",
               "troubleshooting.md", "spatial-and-assets.md", "knowledge-and-provenance.md")
STALE_PHRASES = {
    "通过”“可以了”“锁定": "旧 APPROVED 规则：“通过/可以了”不再自动锁定",
    "通过/可以了/锁定": "旧 APPROVED 规则：“通过/可以了”不再自动锁定",
    "WHAT HE HIDES": "改用 WHAT THEY HIDE（人物隐藏什么）",
    "每 1–2 秒安排": "微事件不再机械排程",
}


def main() -> int:
    errors: list[str] = []
    for path in ROOT.rglob("*.md"):
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        for link in re.findall(r"\]\(([^)]+)\)", text):
            if link.startswith(("http://", "https://")):
                continue
            if not (path.parent / link.split("#")[0]).resolve().exists():
                errors.append(f"断链: {rel} -> {link}")
        for ref in re.findall(r"`((?:assets|scripts)/[^` ]+)", text):
            if not (ROOT / ref).exists():
                errors.append(f"缺文件: {rel} -> {ref}")
        if rel.name == "CHANGELOG.md":
            continue
        for name in STALE_FILES:
            if name in text:
                errors.append(f"引用已合并的旧文件 {name}: {rel}")
        for phrase, why in STALE_PHRASES.items():
            if phrase in text:
                errors.append(f"{rel}: {why}")

    front = (ROOT / "SKILL.md").read_text(encoding="utf-8").split("---", 2)[1]
    for field in ("name:", "version:", "updated_at:", "description:"):
        if field not in front:
            errors.append(f"SKILL.md frontmatter 缺 {field}")

    template = (ROOT / "assets/video-prompt-template.txt").read_text(encoding="utf-8")
    if re.search(r"@(?:image|video|audio)\s*\d", template, re.IGNORECASE):
        errors.append("模板中出现英文素材标签")

    if errors:
        print("FAIL")
        print("\n".join(errors))
        return 1
    print("PASS: 链接、文件引用、旧规则残留、frontmatter、模板标签")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
