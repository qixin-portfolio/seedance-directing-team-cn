#!/usr/bin/env python3
"""Validate that every director-group role reviews every shot in a Markdown table."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path


ROLES = (
    "总导演",
    "表演指导",
    "镜内执行导演",
    "摄影指导",
    "提示词导演",
    "场记/连续性监督",
)
ALIASES = {"场记": "场记/连续性监督", "连续性监督": "场记/连续性监督"}
ROW_PATTERN = re.compile(r"^\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|", re.MULTILINE)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("review_file", type=Path)
    parser.add_argument("--shots", type=int, required=True)
    parser.add_argument("--roles", default=None, help="只检查部分角色，逗号分隔；默认六角色全部")
    args = parser.parse_args()

    roles = ROLES
    if args.roles:
        roles = tuple(ALIASES.get(r.strip(), r.strip()) for r in args.roles.split(",") if r.strip())
        unknown = [r for r in roles if r not in ROLES]
        if unknown:
            print(f"INVALID: 未知角色 {unknown}，可选 {list(ROLES)}", file=sys.stderr)
            return 1

    if args.shots < 1:
        print("INVALID: --shots 必须大于 0", file=sys.stderr)
        return 1

    try:
        text = args.review_file.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        print(f"INVALID: 无法读取 UTF-8 审稿表: {exc}", file=sys.stderr)
        return 1

    pairs = [
        (ALIASES.get(role.strip(), role.strip()), int(shot))
        for role, shot in ROW_PATTERN.findall(text)
        if ALIASES.get(role.strip(), role.strip()) in roles
    ]
    counts = Counter(pairs)
    expected = {(role, shot) for role in roles for shot in range(1, args.shots + 1)}
    actual = set(pairs)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    duplicates = sorted(pair for pair, count in counts.items() if count > 1)

    errors: list[str] = []
    if missing:
        errors.append("缺少: " + ", ".join(f"{role}-镜头{shot}" for role, shot in missing))
    if extra:
        errors.append("超出镜头范围: " + ", ".join(f"{role}-镜头{shot}" for role, shot in extra))
    if duplicates:
        errors.append("重复: " + ", ".join(f"{role}-镜头{shot}" for role, shot in duplicates))

    if errors:
        for error in errors:
            print(f"INVALID: {error}", file=sys.stderr)
        return 1

    print(f"VALID: {len(actual)} role-shot rows = {len(roles)} roles × {args.shots} shots")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
