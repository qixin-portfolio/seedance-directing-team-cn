#!/usr/bin/env python3
"""Validate a multi-shot Seedance prompt built from assets/video-prompt-template.txt."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from prompt_blocks import ENGLISH_TAG, SHOT_HEADER, effective_chars, read_prompt

DECLARED_PATTERN = re.compile(r"本视频严格只有\s*(\d+)\s*个镜头")
REQUIRED_GLOBAL = ("⚠️空间布局", "⚠️对白规则：", "环境活动：", "风格：")
REQUIRED_SHOT = ("机位：", "摄影机运动：", "摄影机位置：", "背景：", "动作：", "微表演细节", "声音：")
ACTOR_TAG = re.compile(r"<([^<>\s]{1,12})>")
SPEAKER = re.compile(r"<([^<>\s]{1,12})>说\s*\{")
SHEET_REF = re.compile(r"@图片\d+\s*—\s*ROLE:\s*IDENTITY_ONLY；ADOPT：([^（：；\s]{1,12})（(?:五格)?(?:人物)?设定板")
FOCAL = re.compile(r"\d+(?:\.\d+)?\s*mm", re.IGNORECASE)
STOP = re.compile(r"\b(?:T\s?\d+(?:\.\d+)?|f\s?/\s?\d+(?:\.\d+)?)", re.IGNORECASE)


def production_checks(prompt: str, preamble: str, blocks: list[tuple[int, str]]) -> list[str]:
    """正式项目关卡：有戏人物要有表演段，说话人要有声音档案，每个机位写焦段和光圈/T 档。"""
    errors: list[str] = []
    actors: list[str] = []
    for _, block in blocks:
        for line in block.splitlines():
            if line.startswith("动作："):
                for name in ACTOR_TAG.findall(line):
                    if name not in actors:
                        actors.append(name)
    for line in preamble.splitlines():
        ref = SHEET_REF.match(line)
        if ref and ref.group(1) not in actors:
            actors.append(ref.group(1))
    speakers = []
    for name in SPEAKER.findall(prompt):
        if name not in speakers:
            speakers.append(name)
        if name not in actors:
            actors.append(name)
    perf_lines = [l for l in preamble.splitlines() if l.startswith("⚠️") and "表演" in l]
    covered = set(ACTOR_TAG.findall("\n".join(perf_lines)))
    covered |= {m.group(1) for l in perf_lines for m in [re.match(r"⚠️([^（：<\s]{1,12})表演", l)] if m}

    def has_perf(name: str) -> bool:
        return any(c and (c in name or name in c) for c in covered)

    missing = [n for n in actors if not has_perf(n)]
    if missing:
        errors.append("缺人物表演段（⚠️<人物>表演（本组）：…）：" + "、".join(missing))
    no_voice = [n for n in speakers if f"{n}声音" not in prompt]
    if no_voice:
        errors.append("有台词但缺声音档案（<人物>声音：…，逐字复用）：" + "、".join(no_voice))
    for number, block in blocks:
        cam = next((l for l in block.splitlines() if l.startswith("机位：")), "")
        if cam and not (FOCAL.search(cam) and STOP.search(cam)):
            errors.append(f"镜头{number}机位缺器材焦段或 T 档/光圈")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt_file", type=Path)
    parser.add_argument("--max-chars", type=int, default=5000, help="平台输入上限更短时请传入平台值")
    parser.add_argument("--production", action="store_true", help="正式项目关卡：查表演段、声音档案、机位焦段与 T 档")
    args = parser.parse_args()

    try:
        prompt = read_prompt(args.prompt_file)
    except (OSError, UnicodeError) as exc:
        print(f"INVALID: 无法读取 UTF-8 提示词: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []
    warnings: list[str] = []
    count = effective_chars(prompt)

    if not prompt:
        errors.append("提示词为空")
    if prompt.lstrip().startswith(("{", "[")):
        errors.append("最终提示词不得使用 JSON 格式")
    if count > args.max_chars:
        errors.append(f"有效字符 {count}，超过上限 {args.max_chars}")
    if re.search(r"15\s*秒[。，,]\s*16:9", prompt):
        errors.append("检测到旧版固定时长/画幅结尾")
    english_tags = sorted(set(ENGLISH_TAG.findall(prompt)))
    if english_tags:
        errors.append(f"素材标签必须用 @图片N/@视频N/@音频N，发现: {', '.join(english_tags)}")

    for marker in REQUIRED_GLOBAL:
        if marker not in prompt:
            errors.append(f"缺少全局字段: {marker}")

    shot_matches = list(SHOT_HEADER.finditer(prompt))
    shot_numbers = [int(match.group(1)) for match in shot_matches]
    if not shot_numbers:
        errors.append("未找到【镜头N】结构")
    else:
        if shot_numbers != list(range(1, len(shot_numbers) + 1)):
            errors.append(f"镜头编号必须从 1 连续且不重复，当前为 {shot_numbers}")

        declared = DECLARED_PATTERN.search(prompt)
        if not declared:
            errors.append("缺少明确的镜头总数声明")
        elif int(declared.group(1)) != len(shot_numbers):
            errors.append(f"声明 {declared.group(1)} 镜，与实际 {len(shot_numbers)} 镜不一致")

        environment = prompt.find("环境活动：", shot_matches[-1].start())
        shots_end = environment if environment >= 0 else len(prompt)
        blocks: list[tuple[int, str]] = []
        for index, match in enumerate(shot_matches):
            end = shot_matches[index + 1].start() if index + 1 < len(shot_matches) else shots_end
            block = prompt[match.start() : end]
            blocks.append((shot_numbers[index], block))
            for marker in REQUIRED_SHOT:
                if marker not in block:
                    errors.append(f"镜头{shot_numbers[index]}缺少字段: {marker}")

        first_shot = shot_matches[0].start()
        if args.production:
            errors.extend(production_checks(prompt, prompt[:first_shot], blocks))
        preamble_ratio = effective_chars(prompt[:first_shot]) / max(count, 1)
        shot_ratio = effective_chars(prompt[first_shot:shots_end]) / max(count, 1)
        if preamble_ratio > 0.20:
            warnings.append(f"资产与空间占比 {preamble_ratio:.0%}（建议 ≤20%），继续压缩")
        if shot_ratio < 0.65:
            warnings.append(f"逐镜内容占比 {shot_ratio:.0%}（建议 ≥65%），把字数留给镜头")

    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"INVALID: {error}", file=sys.stderr)
        return 1

    mode = "; production gates passed" if args.production else "; format only (正式项目请加 --production)"
    print(f"VALID: {count}/{args.max_chars} effective characters; {len(shot_numbers)} shots{mode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
