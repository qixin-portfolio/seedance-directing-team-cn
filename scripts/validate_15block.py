#!/usr/bin/env python3
"""Validate a Production 15-Block Seedance prompt: all blocks present, in order, non-empty."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from prompt_blocks import BLOCKS_15, ENGLISH_TAG, effective_chars, read_prompt, split_15block

SEEDANCE_TAG = re.compile(r"@(?:图片|视频|音频)\d+")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt_file", type=Path)
    parser.add_argument("--max-chars", type=int, default=None, help="平台输入上限（可选）")
    args = parser.parse_args()

    try:
        prompt = read_prompt(args.prompt_file)
    except (OSError, UnicodeError) as exc:
        print(f"INVALID: 无法读取 UTF-8 提示词: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []
    warnings: list[str] = []
    blocks = split_15block(prompt)
    names = [name for name, _ in blocks]

    missing = [name for name in BLOCKS_15 if name not in names]
    duplicated = sorted({name for name in names if names.count(name) > 1})
    if missing:
        errors.append("缺少区块: " + ", ".join(missing))
    if duplicated:
        errors.append("重复区块: " + ", ".join(duplicated))
    present_order = [name for name in BLOCKS_15 if name in names]
    if not duplicated and names != present_order:
        errors.append("区块顺序与标准不一致: " + " → ".join(names))

    for name, body in blocks:
        content = body.split("\n", 1)[1] if "\n" in body else re.sub(r"^.*?[:：—\-–]", "", body, count=1)
        if not content.strip():
            errors.append(f"区块为空: {name}")

    english_tags = sorted(set(ENGLISH_TAG.findall(prompt)))
    if english_tags:
        errors.append(f"素材标签必须用 @图片N/@视频N/@音频N，发现: {', '.join(english_tags)}")

    references = dict(blocks).get("ACTIVE REFERENCES", "")
    declared_tags = set(SEEDANCE_TAG.findall(references))
    for name, body in blocks:
        if name == "ACTIVE REFERENCES":
            continue
        stray = sorted(set(SEEDANCE_TAG.findall(body)) - declared_tags)
        if stray:
            errors.append(f"{name} 引用了未在 ACTIVE REFERENCES 声明的素材: {', '.join(stray)}")
        elif SEEDANCE_TAG.search(body):
            warnings.append(f"{name} 重复出现 @标签；生产约定建议后文用语义名指代")

    count = effective_chars(prompt)
    if args.max_chars is not None and count > args.max_chars:
        errors.append(f"有效字符 {count}，超过上限 {args.max_chars}")

    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"INVALID: {error}", file=sys.stderr)
        return 1

    print(f"VALID: 15/15 blocks; {count} effective characters")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
