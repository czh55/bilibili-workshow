#!/usr/bin/env python3
"""修复「完整转录」章节默认展开的问题。

部分页面的转录区是 <details class="transcript-collapsible" open>，
带 open 属性导致页面加载即展开。本脚本：
1. 移除 open 属性，让转录区默认折叠；
2. 注入展开脚本：点击目录「完整转录」导航链接时自动展开并定位。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"

OPEN_RE = re.compile(r'<details class="transcript-collapsible" open>')
JS_ID = "transcript-open-script"
JS_BLOCK = (
    '<script id="%s">'
    '(function(){var d=document.querySelector(".transcript-collapsible");'
    'if(!d)return;function o(){d.setAttribute("open","")}'
    'document.querySelectorAll(\'a[href="#transcript"]\').forEach(function(a){a.addEventListener("click",o)});'
    'if(location.hash==="#transcript")o()})();'
    "</script>" % JS_ID
)


def fix_file(path: Path) -> int:
    html = path.read_text(encoding="utf-8")
    if not OPEN_RE.search(html):
        return 0
    html = OPEN_RE.sub('<details class="transcript-collapsible">', html)
    if JS_ID not in html:
        if "</body>" in html:
            html = html.replace("</body>", JS_BLOCK + "</body>", 1)
        else:
            html += JS_BLOCK
    path.write_text(html, encoding="utf-8")
    return 1


def main() -> None:
    fixed = 0
    for f in sorted(DOCS.glob("*-图文实录.html")):
        if fix_file(f):
            print(f"  fixed {f.name}")
            fixed += 1
    print(f"done: {fixed} files now collapsed by default")
    sys.exit(0)


if __name__ == "__main__":
    main()
