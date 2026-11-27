#!/usr/bin/env python3
"""Validate a visual-anchor segment prompt built from assets/anchor-segment-prompt-template.txt."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from prompt_blocks import ENGLISH_TAG, effective_chars, read_prompt

SEGMENT = re.compile(r"【\s*(\d+(?:\.\d+)?)\s*[—\-–~～]+\s*(\d+(?:\.\d+)?)\s*秒\s*[｜|]\s*([^】]*)】")
DURATION = re.compile(r"【时长】\s*(\d+(?:\.\d+)?)\s*秒")
ANCHOR_NAME = re.compile(r"分镜图\s*0?(\d+)")
REQUIRED = ("【参考资产】", "【时长】", "【整体事件】", "【结束状态】", "【限制条件】")
FOCAL = re.compile(r"\d+(?:\.\d+)?\s*mm", re.IGNORECASE)
STOP = re.compile(r"\b(?:T\s?\d+(?:\.\d+)?|f\s?/\s?\d+(?:\.\d+)?)", re.IGNORECASE)
SPEAKER = re.compile(r"(?:^|\n)\s*<?([^<>\s：:“\"]{1,12})>?说[：:]?\s*[“\"]")

MIN_LEAD, MIN_EXIT, MIN_GAP = 1.5, 1.5, 3.0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt_file", type=Path)
    parser.add_argument("--max-chars", type=int, default=5000, help="平台输入上限更短时请传入平台值")
    parser.add_argument("--production", action="store_true", help="正式项目关卡：每段焦段与 T 档、表演段、声音档案")
    args = parser.parse_args()

    try:
        prompt = read_prompt(args.prompt_file)
    except (OSError, UnicodeError) as exc:
        print(f"INVALID: 无法读取 UTF-8 提示词: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []
    warnings: list[str] = []
    count = effective_chars(prompt)
    if count > args.max_chars:
        errors.append(f"有效字符 {count}，超过上限 {args.max_chars}")
    tags = sorted(set(ENGLISH_TAG.findall(prompt)))
    if tags:
        errors.append(f"素材标签必须用 @图片N/@视频N/@音频N（或平台语法），发现: {', '.join(tags)}")
    for marker in REQUIRED:
        if marker not in prompt:
            errors.append(f"缺少区块: {marker}")

    segments = [(float(a), float(b), title.strip(), m.start()) for m in SEGMENT.finditer(prompt)
                for a, b, title in [m.groups()]]
    if not segments:
        errors.append("未找到时间段【a—b秒｜标题】")
    else:
        if segments[0][0] != 0:
            errors.append(f"第一段应从 0 秒开始，当前 {segments[0][0]}")
        for (a1, b1, t1, _), (a2, _, t2, _) in zip(segments, segments[1:]):
            if abs(b1 - a2) > 0.05:
                errors.append(f"时间段不连续：「{t1}」止于 {b1}，「{t2}」始于 {a2}")
        duration = DURATION.search(prompt)
        total = float(duration.group(1)) if duration else segments[-1][1]
        if duration and abs(segments[-1][1] - total) > 0.05:
            errors.append(f"最后一段止于 {segments[-1][1]} 秒，与时长 {total} 秒不一致")

        anchors = [s for s in segments if "抵达" in s[2] and ANCHOR_NAME.search(s[2])]
        if not anchors:
            errors.append("没有“抵达分镜图NN”的锚点段")
        else:
            if anchors[0][0] < MIN_LEAD:
                errors.append(f"第一锚点 {anchors[0][0]} 秒就开始抵达，锚点前至少留 {MIN_LEAD} 秒引入段（不是首帧）")
            if total - anchors[-1][1] < MIN_EXIT:
                errors.append(f"最后锚点之后只剩 {total - anchors[-1][1]:.1f} 秒，至少留 {MIN_EXIT} 秒出口段（不是尾帧）")
            for prev, nxt in zip(anchors, anchors[1:]):
                if nxt[0] - prev[1] < MIN_GAP:
                    warnings.append(f"「{prev[2]}」与「{nxt[2]}」之间过程段 {nxt[0] - prev[1]:.1f} 秒，建议 ≥{MIN_GAP} 秒")
            limit = 2 if total <= 12 else 3
            if len(anchors) > limit:
                warnings.append(f"{total:g} 秒片段有 {len(anchors)} 个锚点，建议 ≤{limit}")
            for a, b, title, start in anchors:
                end = next((s[3] for s in segments if s[3] > start), prompt.find("【结束状态】"))
                body = prompt[start:end if end > start else len(prompt)]
                if "忠实抵达" not in body:
                    warnings.append(f"「{title}」没写抵达方式（忠实抵达…的主体关系和构图）")
            preamble = prompt[: segments[0][3]]
            for number in sorted({n for *_, t, _ in anchors for n in ANCHOR_NAME.findall(t)}):
                if not re.search(rf"分镜图\s*0?{number}[^。\n]*不是(?:首帧|尾帧)", preamble):
                    errors.append(f"【参考资产】没写明分镜图{int(number):02d}“不是首帧/不是尾帧”")

        if args.production:
            for a, b, title, start in segments:
                nxt = next((s[3] for s in segments if s[3] > start), prompt.find("【结束状态】"))
                body = prompt[start:nxt if nxt > start else len(prompt)]
                cam = "\n".join(l for l in body.splitlines() if l.strip().startswith("摄影"))
                if not (FOCAL.search(cam) and STOP.search(cam)):
                    errors.append(f"「{title}」缺“摄影：”行的器材焦段或 T 档/光圈")
            speakers = {n.strip("<>") for n in SPEAKER.findall(prompt)}
            for name in sorted(speakers):
                if not re.search(rf"⚠️{re.escape(name)}表演", prompt):
                    errors.append(f"缺人物表演段：⚠️{name}表演（本片段）")
                if f"{name}声音" not in prompt:
                    errors.append(f"有台词但缺声音档案：{name}声音：…")

    limits = prompt[prompt.find("【限制条件】"):] if "【限制条件】" in prompt else ""
    if limits and not re.search(r"变形|直接从", limits):
        warnings.append("【限制条件】建议写“不要直接从图01变形成图02”")

    for w in warnings:
        print(f"WARNING: {w}")
    if errors:
        for e in errors:
            print(f"INVALID: {e}", file=sys.stderr)
        return 1
    mode = "; production gates passed" if args.production else "; format only (正式项目请加 --production)"
    print(f"VALID: {count}/{args.max_chars} effective characters; {len(segments)} segments{mode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
