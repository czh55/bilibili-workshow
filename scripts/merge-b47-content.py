#!/usr/bin/env python3
"""b47：把 _work/b47/content/{slug}.json 中间数据转换成四类目标数据。

每个 {slug}.json 结构：
{
  "key": "f31",
  "html": { ...b47_data.py 条目所需字段... },
  "svg": { ...b47_svg_data.mjs 条目所需字段... },
  "scene": { ...scene-data/{slug}.json 结构... },
  "shots": { "shots": [ {"file","time","chapter","scene"}, ... ] }
}

转换产物：
1. scripts/b47_data.py       追加 html 条目
2. scripts/b47_svg_data.mjs  追加 svg 条目
3. scripts/scene-data/{slug}.json
4. shots-{slug}.json
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "_work" / "b47" / "content"
DATA_PY = ROOT / "scripts" / "b47_data.py"
SVG_MJS = ROOT / "scripts" / "b47_svg_data.mjs"
SCENE_DIR = ROOT / "scripts" / "scene-data"


def esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def js_string(s: str) -> str:
    return f'"{esc(s)}"'


def append_to_data_py(slug: str, d: dict) -> None:
    text = DATA_PY.read_text(encoding="utf-8")
    assert text.rstrip().endswith("}"), "b47_data.py 应以 } 结尾"
    body = json.dumps(d, ensure_ascii=False, indent=1)
    lines = body.split("\n")
    out = []
    out.append(f' "{slug}": {{')
    for i, ln in enumerate(lines):
        if i == 0:
            continue
        if i == len(lines) - 1:
            continue
        out.append((" " + ln).rstrip())
    out.append(" }")
    block = "\n".join(out)
    new_text = text.rstrip()[:-1] + ",\n" + block + "\n}"
    DATA_PY.write_text(new_text, encoding="utf-8")
    print(f"  b47_data.py: +{slug}")


def append_to_svg_mjs(slug: str, d: dict) -> None:
    text = SVG_MJS.read_text(encoding="utf-8")
    assert text.rstrip().endswith("};"), "b47_svg_data.mjs 应以 }; 结尾"
    # 用 JSON dump 生成 JS 对象（键顺序保持）
    body = json.dumps(d, ensure_ascii=False, indent=1)
    lines = body.split("\n")
    out = [f' "{slug}": {{']
    for i, ln in enumerate(lines):
        if i == 0 or i == len(lines) - 1:
            continue
        out.append((" " + ln).rstrip())
    out.append(" }")
    block = "\n".join(out)
    new_text = text.rstrip()[:-2] + ",\n" + block + "\n};"
    SVG_MJS.write_text(new_text, encoding="utf-8")
    print(f"  b47_svg_data.mjs: +{slug}")


def main() -> None:
    args = sys.argv[1:]
    slugs = args or sorted(p.stem for p in CONTENT.glob("*.json"))
    for slug in slugs:
        p = CONTENT / f"{slug}.json"
        if not p.exists():
            print(f"✗ 缺少 {p.name}")
            continue
        data = json.loads(p.read_text(encoding="utf-8"))
        print(f"== {slug} ({data.get('key')})")
        if "html" in data:
            append_to_data_py(slug, data["html"])
        if "svg" in data:
            append_to_svg_mjs(slug, data["svg"])
        if "scene" in data:
            sp = SCENE_DIR / f"{slug}.json"
            sp.write_text(json.dumps(data["scene"], ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            print(f"  scene-data/{slug}.json")
        if "shots" in data:
            sh = data["shots"]
            sh.setdefault("slug", slug)
            sh.setdefault("key", data.get("key"))
            (ROOT / f"shots-{slug}.json").write_text(
                json.dumps(sh, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            print(f"  shots-{slug}.json")
    print("完成")


if __name__ == "__main__":
    main()
