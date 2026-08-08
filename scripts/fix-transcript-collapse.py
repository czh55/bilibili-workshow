#!/usr/bin/env python3
"""修复早期批次页面：把「详细文字转录」包进 <details class="transcript-collapsible">。

背景：部分页面模板已有 .transcript-collapsible 的 CSS 与点击导航展开的 JS，
但转录区缺少 <details> 包裹，导致无法折叠。此脚本补齐 details 结构。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
SECTION_RE = re.compile(r'(<section class="transcript-section" id="transcript">)(.*?)(</section>)', re.S)


def fix_file(path: Path) -> int:
    html = path.read_text(encoding="utf-8")
    m = SECTION_RE.search(html)
    if not m:
        return 0
    inner = m.group(2)
    if "<details" in inner:
        return 0
    if "<h2>详细文字转录</h2>" not in inner:
        return 0
    inner = inner.replace(
        "<h2>详细文字转录</h2>",
        '<details class="transcript-collapsible"><summary>详细文字转录</summary><div class="transcript-body">',
        1,
    )
    end = inner.rfind("</ol>")
    if end == -1:
        return 0
    inner = inner[: end + 5] + "\n      </div></details>" + inner[end + 5 :]
    html = html[: m.start()] + m.group(1) + inner + html[m.end() :]
    path.write_text(html, encoding="utf-8")
    return 1


def main() -> None:
    fixed = 0
    for f in sorted(DOCS.glob("*-图文实录.html")):
        if fix_file(f):
            print(f"  fixed {f.name}")
            fixed += 1
    print(f"done: {fixed} files wrapped in <details>")
    sys.exit(0)


if __name__ == "__main__":
    main()
