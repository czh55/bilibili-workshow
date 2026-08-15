#!/usr/bin/env python3
"""b47：批量处理内容 JSON → 生成四类产物。

流程（对每个 slug）：
  1. 校验 content/{slug}.json 结构完整
  2. 合并进 b47_data.py / b47_svg_data.mjs / scene-data / shots-{slug}.json
  3. 生成 HTML 图文实录
  4. 提取截图
  5. 生成 SVG 理性分析
  6. 生成场景英译 HTML + 音频

用法：
  python3 scripts/b47-pipeline.py {slug} [{slug} ...]     # 指定处理
  python3 scripts/b47-pipeline.py --all                    # 处理全部 content/*.json
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
CONTENT = ROOT / "_work" / "b47" / "content"

REQUIRED = ("html", "svg", "scene", "shots")


def run(cmd: list[str], cwd: Path) -> bool:
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  ✗ {' '.join(cmd[:2])}...\n    {r.stderr.strip()[:300]}")
        return False
    return True


def process(slug: str) -> None:
    p = CONTENT / f"{slug}.json"
    if not p.exists():
        print(f"✗ 缺少 {p.name}")
        return
    data = json.loads(p.read_text(encoding="utf-8"))
    missing = [k for k in REQUIRED if k not in data]
    if missing:
        print(f"✗ {slug}: 缺少字段 {missing}")
        return
    print(f"== {slug}")
    # 1. 合并
    if not run(["python3", "scripts/merge-b47-content.py", slug], ROOT):
        return
    # 2. HTML
    run(["python3", "scripts/b47-html.py", slug], ROOT)
    # 3. 截图
    run(["python3", "scripts/b47-make-shots.py", slug], ROOT)
    # 4. SVG
    run(["node", "scripts/build-b47-svg.mjs", slug], ROOT)
    # 5. 场景英译（音频+HTML）
    run(["python3", "scripts/gen-scene-en.py", "--slug", slug], ROOT)
    print(f"✓ {slug} 完成")


def main() -> None:
    args = sys.argv[1:]
    if "--all" in args:
        slugs = sorted(p.stem for p in CONTENT.glob("*.json"))
    else:
        slugs = [a for a in args if a and not a.startswith("--")]
    if not slugs:
        print(__doc__)
        return
    for slug in slugs:
        process(slug)
    print("全部完成")


if __name__ == "__main__":
    main()
