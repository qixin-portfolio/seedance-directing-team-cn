#!/usr/bin/env python3
"""Workbench check: only the declared PATCH blocks may differ between two prompt versions."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from prompt_blocks import read_prompt, split_any


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("old_prompt", type=Path)
    parser.add_argument("new_prompt", type=Path)
    parser.add_argument(
        "--patch",
        required=True,
        help="允许修改的区块，逗号分隔。15-Block 用区块名（如 'LOCATION MAP,ACTION TIMING'）；"
        "多镜头分镜用 前置/镜头N/环境活动/风格",
    )
    args = parser.parse_args()

    try:
        old_kind, old_blocks = split_any(read_prompt(args.old_prompt))
        new_kind, new_blocks = split_any(read_prompt(args.new_prompt))
    except (OSError, UnicodeError) as exc:
        print(f"INVALID: 无法读取 UTF-8 提示词: {exc}", file=sys.stderr)
        return 1

    if old_kind != new_kind:
        print(f"INVALID: 两版格式不同（{old_kind} → {new_kind}），这是重写而不是 PATCH", file=sys.stderr)
        return 1

    patch = {name.strip() for name in args.patch.split(",") if name.strip()}
    old_map, new_map = dict(old_blocks), dict(new_blocks)
    all_names = list(dict.fromkeys([name for name, _ in old_blocks] + [name for name, _ in new_blocks]))

    unknown = sorted(patch - set(all_names))
    errors: list[str] = []
    warnings: list[str] = []
    if unknown:
        errors.append("PATCH 声明了不存在的区块: " + ", ".join(unknown))

    for name in all_names:
        changed = old_map.get(name) != new_map.get(name)
        if changed and name not in patch:
            if name not in old_map:
                errors.append(f"新增了未声明的区块: {name}")
            elif name not in new_map:
                errors.append(f"删除了未声明的区块: {name}")
            else:
                errors.append(f"未声明 PATCH 却被修改: {name}")
        if not changed and name in patch:
            warnings.append(f"声明 PATCH 但内容未变: {name}")

    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"INVALID: {error}", file=sys.stderr)
        return 1

    kept = [name for name in all_names if name not in patch]
    print(f"VALID: {old_kind}；PATCH {sorted(patch)}；其余 {len(kept)} 个区块逐字不变")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
