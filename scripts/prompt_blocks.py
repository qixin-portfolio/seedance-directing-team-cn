"""Shared parsing helpers for Seedance prompt validators."""

from __future__ import annotations

import re
from pathlib import Path

BLOCKS_15 = (
    "SCENE CONTEXT",
    "ACTIVE REFERENCES",
    "LOCATION MAP",
    "FIRST FRAME AND SPATIAL BLOCKING",
    "FORMAT MODE",
    "OPTICS",
    "CAMERA",
    "ACTION TIMING",
    "PHYSICS",
    "LIGHTING",
    "AUDIO",
    "CHARACTER ACTING",
    "STYLE",
    "QUALITY",
    "POSITIVE CONSTRAINTS",
)

# 区块标题独占一行开头，允许 "1. "、"【】"、"**" 包裹，后接中英文冒号或换行。
HEADER_15 = re.compile(
    r"^[ \t]*(?:\d+[.、)]\s*)?(?:\*\*|【)?\s*("
    + "|".join(re.escape(name) for name in BLOCKS_15)
    + r")\s*(?:\*\*|】)?\s*(?:[—\-–]|[:：]|$)",
    re.MULTILINE,
)
SHOT_HEADER = re.compile(r"【镜头(\d+)】")
TAIL_HEADER = re.compile(r"^[ \t]*(环境活动|风格)[:：]", re.MULTILINE)
ENGLISH_TAG = re.compile(r"@(?:image|video|audio)\s*\d+", re.IGNORECASE)


def read_prompt(path: Path) -> str:
    text = path.read_text(encoding="utf-8").strip()
    fence = re.match(r"^```[a-zA-Z]*\n(.*)\n```$", text, re.DOTALL)
    return fence.group(1).strip() if fence else text


def effective_chars(text: str) -> int:
    return sum(1 for char in text if not char.isspace())


def split_15block(text: str) -> list[tuple[str, str]]:
    matches = list(HEADER_15.finditer(text))
    blocks = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks.append((match.group(1), text[match.start() : end].strip()))
    return blocks


def split_multishot(text: str) -> list[tuple[str, str]]:
    cuts = [(m.start(), f"镜头{m.group(1)}") for m in SHOT_HEADER.finditer(text)]
    cuts += [(m.start(), m.group(1)) for m in TAIL_HEADER.finditer(text)]
    cuts.sort()
    blocks = []
    if not cuts or cuts[0][0] > 0:
        blocks.append(("前置", text[: cuts[0][0] if cuts else len(text)].strip()))
    for index, (start, name) in enumerate(cuts):
        end = cuts[index + 1][0] if index + 1 < len(cuts) else len(text)
        blocks.append((name, text[start:end].strip()))
    return blocks


def split_any(text: str) -> tuple[str, list[tuple[str, str]]]:
    if len(split_15block(text)) >= 3:
        return "15-Block", split_15block(text)
    return "多镜头分镜", split_multishot(text)
