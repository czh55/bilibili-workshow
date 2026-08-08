#!/usr/bin/env python3
"""从图文实录 HTML 提取详细转录文本（含时间戳），便于场景切分。

用法：python3 scripts/html-transcript-to-text.py {slug}
输出：stdout 打印 [MM:SS] 文本。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"


def extract(slug: str) -> str:
    html = (DOCS / f"{slug}-图文实录.html").read_text(encoding="utf-8")
    # 解析 <div/li class="transcript-row"><time>MM:SS</time><p>text</p></div/li>
    rows = re.findall(
        r'<(?:li|div) class="transcript-row"[^>]*>\s*<time[^>]*>(\d+:\d+)</time>\s*<p>(.*?)</p>',
        html,
        re.S,
    )
    if rows:
        out = []
        for ts, p in rows:
            text = re.sub(r"<[^>]+>", "", p)
            text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").strip()
            if text:
                out.append(f"[{ts}] {text}")
        return "\n".join(out)

    # 兜底：解析 transcript-body 内纯 <p> 段落
    m = re.search(r'id="transcript".*?<div class="transcript-body">(.*?)</div>', html, re.S)
    if not m:
        m = re.search(r'id="transcript"(.*?)</details>', html, re.S)
    if not m:
        raise SystemExit(f"no transcript block in {slug}-图文实录.html")
    body = m.group(1)
    paras = re.findall(r"<p[^>]*>(.*?)</p>", body, re.S)
    out = []
    for p in paras:
        text = re.sub(r"<[^>]+>", "", p)
        text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").strip()
        if text:
            out.append(text)
    return "\n".join(out)


def main() -> None:
    slug = sys.argv[1]
    text = extract(slug)
    # 打印带行号，同时按时间戳分组便于阅读
    for i, line in enumerate(text.split("\n"), 1):
        print(f"{i:04d}| {line[:120]}")


if __name__ == "__main__":
    main()
