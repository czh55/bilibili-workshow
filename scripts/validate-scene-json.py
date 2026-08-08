#!/usr/bin/env python3
"""校验并修复 scene-data/{slug}.json。

用法：
  python3 scripts/validate-scene-json.py {slug}        # 校验并显示统计
  python3 scripts/validate-scene-json.py --fix {slug}  # 尝试自动修复常见笔误

修复规则（仅处理我在编写 JSON 时容易犯的 Python 元组风格笔误）：
  1. 行尾 "),   →  "],   （句子三元组最后元素）
  2. 行尾 "),  且前面是 ） →  "]  （无需逗号时）
  3. 数组闭合前多余的逗号移除
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "scripts" / "scene-data"


def try_fix(s: str) -> str:
    # 1. 行尾 "), → "],   （保持逗号）
    s = re.sub(r'"\)(,)\s*$', r'"],', s, flags=re.M)
    # 2. 行尾 ")   →  "]   （无逗号）
    s = re.sub(r'"\)\s*$', r'"]', s, flags=re.M)
    # 3. 去掉数组闭合（]）前的多余逗号
    lines = s.split("\n")
    out = []
    for i, line in enumerate(lines):
        st = line.strip()
        if st.endswith("],"):
            nxt = None
            for j in range(i + 1, len(lines)):
                if lines[j].strip():
                    nxt = lines[j].strip()
                    break
            if nxt in ("]", "],"):
                line = line[:-1]
        out.append(line)
    return "\n".join(out)


def main() -> None:
    args = [a for a in sys.argv[1:]]
    do_fix = "--fix" in args
    slugs = [a for a in args if not a.startswith("--")]

    for slug in slugs:
        p = DATA_DIR / f"{slug}.json"
        if not p.exists():
            print(f"✗ missing {p}")
            continue
        s = p.read_text(encoding="utf-8")
        try:
            data = json.loads(s)
        except json.JSONDecodeError as e:
            if not do_fix:
                print(f"✗ {slug}: line {e.lineno} col {e.colno}: {e.msg}")
                continue
            s2 = try_fix(s)
            try:
                data = json.loads(s2)
                p.write_text(s2, encoding="utf-8")
                print(f"✓ {slug}: fixed ({e.msg})")
            except json.JSONDecodeError as e2:
                print(f"✗ {slug}: cannot auto-fix: line {e2.lineno}: {e2.msg}")
                continue
        scenes = data.get("scenes", [])
        total_sent = sum(len(sc.get("sentences", [])) for sc in scenes)
        total_para = sum(len(sc.get("paraphrase", [])) for sc in scenes)
        print(
            f"✓ {slug}: scenes={len(scenes)} sentences={total_sent} "
            f"paraphrase={total_para} practice={len(data.get('practice', []))} "
            f"pitfalls={len(data.get('pitfalls', []))} shifts={len(data.get('shifts', []))} "
            f"words={len(data.get('difficult_words', []))}"
        )


if __name__ == "__main__":
    main()
