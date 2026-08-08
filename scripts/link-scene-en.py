#!/usr/bin/env python3
"""为第一批 10 篇中文图文实录页加入英文学习卡链接，并更新 index.json 的 html_en 字段。"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
INDEX = DOCS / "index.json"

SLUGS = ["seville-vlog", "paris-vlog", "vietnam-lazy", "bali-crab", "hupao-park",
         "jingmai-photo", "toronto-animal-shelter"]


def main() -> None:
    # 支持命令行传 slug：python3 scripts/link-scene-en.py slug1 slug2 ...
    slugs = sys.argv[1:] or SLUGS
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    by_html = {e["outputs"]["html"]: e for e in data if isinstance(e.get("outputs"), dict)} if isinstance(data, list) else data

    for slug in slugs:
        zh_file = DOCS / f"{slug}-图文实录.html"
        if not zh_file.exists():
            print(f"  ✗ 缺中文页 {zh_file.name}")
            continue
        en_file = f"{slug}-场景英译.html"
        html = zh_file.read_text(encoding="utf-8")

        if f'href="{en_file}"' in html:
            print(f"  ~ {slug}: 链接已存在")
        else:
            # 在 </header> 前的原视频链接后追加语言切换链接
            if 'lang-switch' not in html:
                link = f'\n<a class="source-link lang-switch" href="{en_file}" hreflang="en">English Version</a>'
                if not re.search(r"</header>", html):
                    print(f"  ✗ {slug}: 找不到 </header>")
                    continue
                html = re.sub(r"</header>", link + "</header>", html, count=1)
                zh_file.write_text(html, encoding="utf-8")
                print(f"  ✓ {slug}: 加入 English Version 链接")
            else:
                html = re.sub(r'href="[^"]*场景英译\.html"', f'href="{en_file}"', html, count=1)
                zh_file.write_text(html, encoding="utf-8")
                print(f"  ~ {slug}: 更新已有链接 -> {en_file}")

        entry = by_html.get(f"{slug}-图文实录.html")
        if entry is None:
            print(f"  ✗ {slug}: index.json 无对应条目")
            continue
        entry["outputs"]["html_en"] = en_file
        entry["outputs"]["html_en_type"] = "scene-english"
        print(f"  ✓ index.json: {slug} -> html_en={en_file}")

    json.dump(data, open(INDEX, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("完成")


if __name__ == "__main__":
    main()
