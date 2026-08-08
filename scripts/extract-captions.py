#!/usr/bin/env python3
"""提取所有图文实录 HTML 中 figcaption 的中文文本，生成翻译清单。

输出 caption-extract.json:
{
  "docs/makeup-class-prep-图文实录.html": {
    "slug": "makeup-class-prep",
    "captions": [
      {"shot": "shot-01", "time": "00:32", "zh": "说明文字", "raw_html": "<span class=\"time-badge\">[00:32]</span> 说明文字"}
    ]
  }
}
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
OUT = Path(__file__).resolve().parent.parent / "caption-extract.json"

TIME_RE = re.compile(r"\[(\d{1,2}:\d{2}(?::\d{2})?)\]")
BADGE_RE = re.compile(r"<span class=\"time-badge\">\[.*?\]</span>", re.S)


def strip_html(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).replace("&quot;", '"').replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").strip()


def extract_from_file(path: Path) -> dict | None:
    html = path.read_text(encoding="utf-8")
    slug = path.name.replace("-图文实录.html", "")
    figures = re.findall(r"<figure>.*?</figure>", html, re.S)
    captions: list[dict] = []
    for fig in figures:
        img_m = re.search(r'src="assets/[^"/]+/([^"/]+?)\.jpg"', fig)
        cap_m = re.search(r"<figcaption>(.*?)</figcaption>", fig, re.S)
        if not cap_m:
            continue
        cap_html = cap_m.group(1)
        shot = img_m.group(1) if img_m else None
        text = strip_html(cap_html)
        time_m = TIME_RE.search(text)
        time = time_m.group(1) if time_m else ""
        zh = text[time_m.end():].strip(" ：: ") if time_m else text
        if not zh:
            continue
        captions.append({"shot": shot, "time": time, "zh": zh, "raw_html": cap_html.strip()})
    if not captions:
        return None
    return {"slug": slug, "captions": captions}


def main() -> None:
    files = sorted(DOCS.glob("*-图文实录.html"))
    result: dict[str, dict] = {}
    total = 0
    for f in files:
        data = extract_from_file(f)
        if data:
            result[str(f.relative_to(DOCS.parent))] = data
            total += len(data["captions"])
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"files: {len(result)}, captions: {total} → {OUT.name}")


if __name__ == "__main__":
    main()
