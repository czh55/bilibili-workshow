#!/usr/bin/env python3
"""把 SRT 转录转成紧凑文本，便于阅读与场景切分。

用法：python3 scripts/srt-to-text.py {slug} [--window 120]
输出：terminal 打印 [MM:SS] 文本，按自然停顿分组。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def parse_srt(p: Path) -> list[tuple[int, str]]:
    text = p.read_text(encoding="utf-8")
    blocks = re.split(r"\n\s*\n", text.strip())
    out = []
    for b in blocks:
        lines = [l.strip() for l in b.split("\n") if l.strip()]
        if len(lines) >= 2 and re.match(r"\d+$", lines[0]) and "-->" in lines[1]:
            m = re.match(r"(\d+):(\d+):(\d+)[,.]\d+", lines[1])
            sec = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
            txt = " ".join(lines[2:])
            out.append((sec, txt))
    return out


def main() -> None:
    slug = sys.argv[1]
    window = 120
    if "--window" in sys.argv:
        window = int(sys.argv[sys.argv.index("--window") + 1])

    srt = ROOT / f"{slug}.srt"
    if not srt.exists():
        raise SystemExit(f"no srt: {srt}")
    segs = parse_srt(srt)
    print(f"== {slug}: {len(segs)} segments, total {segs[-1][0]//60}:{segs[-1][0]%60:02d} ==")

    # 按时间窗口分组，组内句子用 / 连接
    group_secs: list[int] = []
    group_text: list[str] = []
    for sec, txt in segs:
        if group_secs and sec - group_secs[-1] > window:
            print(f"[{group_secs[0]//60:02d}:{group_secs[0]%60:02d}] {' / '.join(group_text)}")
            group_secs, group_text = [], []
        group_secs.append(sec)
        group_text.append(txt)
    if group_text:
        print(f"[{group_secs[0]//60:02d}:{group_secs[0]%60:02d}] {' / '.join(group_text)}")


if __name__ == "__main__":
    main()
