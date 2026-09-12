#!/usr/bin/env python3
"""Generate per-primary category summary HTML + topics.json entries.

Reads:
  docs/taxonomy.json
  docs/index.json
  docs/category-summaries/content.json

Writes:
  docs/category-summaries/{id}-总结.html
  docs/topics.json  (category summary topics; preserves non-category topics if any)
"""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TAX = DOCS / "taxonomy.json"
INDEX = DOCS / "index.json"
CONTENT = DOCS / "category-summaries" / "content.json"
OUT_DIR = DOCS / "category-summaries"
TOPICS = DOCS / "topics.json"

CSS = """
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.8;color:#292524;background:#fafaf9}
.container{width:min(920px,100%);margin:0 auto;padding:48px 28px 80px}
header{margin-bottom:36px}
.back{display:inline-block;margin-bottom:16px;color:#64748b;font-size:14px;text-decoration:none}
.back:hover{color:#3b82f6}
header h1{font-size:30px;font-weight:900;color:#1c1917;margin:0 0 12px;line-height:1.3}
.meta-row{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:14px}
.meta-tag{display:inline-block;padding:4px 12px;border-radius:999px;font-size:12px;font-weight:600}
.tag-cat{background:#1e293b;color:#fff}
.tag-count{background:#e2e8f0;color:#334155}
.tag-dim{background:#dbeafe;color:#1e40af}
.thesis{background:#fff;border-left:4px solid #3b82f6;border-radius:12px;padding:18px 20px;box-shadow:0 2px 12px rgba(0,0,0,.04);font-size:16px;color:#334155}
.section{margin:40px 0}
.section h2{font-size:22px;font-weight:700;margin:0 0 16px;padding-bottom:8px;border-bottom:2px solid #e7e5e4;color:#1c1917}
.card{background:#fff;border-radius:14px;padding:18px 20px;margin:0 0 14px;box-shadow:0 2px 12px rgba(0,0,0,.04);border-left:4px solid #94a3b8}
.card h3{margin:0 0 8px;font-size:17px;color:#0f172a}
.card p{margin:0 0 10px;color:#57534e;font-size:15px}
.evidence{display:flex;flex-wrap:wrap;gap:8px}
.evidence a{font-size:13px;color:#1d4ed8;text-decoration:none;background:#eff6ff;padding:4px 10px;border-radius:8px}
.evidence a:hover{background:#dbeafe}
.list{background:#fff;border-radius:14px;padding:18px 22px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.list li{margin:0 0 10px;color:#44403c}
.list.pitfalls{border-left:4px solid #f59e0b}
.list.actions{border-left:4px solid #10b981}
.footer{margin-top:48px;padding-top:20px;border-top:1px solid #e7e5e4;color:#78716c;font-size:13px}
@media(max-width:640px){.container{padding:28px 16px 56px}header h1{font-size:24px}}
"""


def slug_of(item: dict) -> str:
    if item.get("slug"):
        return item["slug"]
    html_name = (item.get("outputs") or {}).get("html") or ""
    if html_name.endswith("-图文实录.html"):
        return html_name[: -len("-图文实录.html")]
    return ""


def by_slug(index: list) -> dict:
    m = {}
    for it in index:
        s = slug_of(it)
        if s:
            m[s] = it
    return m


def page_html(primary: dict, body: dict, items: list, slug_map: dict) -> str:
    pid = primary["id"]
    label = primary["label"]
    n = len(items)
    creators = sorted({it.get("creator") for it in items if it.get("creator")})
    tools = sorted({it.get("tool") for it in items if it.get("tool")})

    vp_html = []
    for i, vp in enumerate(body.get("viewpoints") or [], 1):
        links = []
        for s in vp.get("evidence_slugs") or []:
            it = slug_map.get(s)
            if not it:
                continue
            href = (it.get("outputs") or {}).get("html") or f"{s}-图文实录.html"
            title = it.get("title") or s
            links.append(
                f'<a href="../{html.escape(href)}" target="_blank" rel="noopener">{html.escape(title[:36])}</a>'
            )
        ev = f'<div class="evidence">{"".join(links)}</div>' if links else ""
        vp_html.append(
            f'<article class="card"><h3>{i}. {html.escape(vp.get("title") or "")}</h3>'
            f'<p>{html.escape(vp.get("body") or "")}</p>{ev}</article>'
        )

    def ul(items_list, cls):
        lis = "".join(f"<li>{html.escape(x)}</li>" for x in items_list)
        return f'<ul class="list {cls}">{lis}</ul>'

    dim_tags = ""
    if creators or tools:
        bits = []
        for c in creators[:4]:
            bits.append(f'<span class="meta-tag tag-dim">{html.escape(c)}</span>')
        for t in tools[:4]:
            bits.append(f'<span class="meta-tag tag-dim">{html.escape(t)}</span>')
        dim_tags = "".join(bits)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="{html.escape(body.get('thesis') or '')}">
<title>{html.escape(label)} · 类目核心观点｜总结</title>
<style>{CSS}</style>
</head>
<body>
<main class="container">
<a class="back" href="../index.html">← 返回总结墙</a>
<header>
<h1>{html.escape(label)} · 核心观点总结</h1>
<div class="meta-row">
<span class="meta-tag tag-cat">类目导读</span>
<span class="meta-tag tag-count">{n} 篇</span>
{dim_tags}
</div>
<p class="thesis">{html.escape(body.get("thesis") or "")}</p>
</header>

<section class="section">
<h2>核心观点</h2>
{"".join(vp_html)}
</section>

<section class="section">
<h2>避坑</h2>
{ul(body.get("pitfalls") or [], "pitfalls")}
</section>

<section class="section">
<h2>行动清单</h2>
{ul(body.get("actions") or [], "actions")}
</section>

<p class="footer">由 taxonomy primary=<code>{html.escape(pid)}</code> 汇总 · 证据链指向站内图文实录 · 可用 scripts/generate-category-summaries.py 重生</p>
</main>
</body>
</html>
"""


def main() -> None:
    tax = json.loads(TAX.read_text(encoding="utf-8"))
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    content = json.loads(CONTENT.read_text(encoding="utf-8"))
    slug_map = by_slug(index)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    missing = []
    topics = []
    for primary in tax["primaries"]:
        pid = primary["id"]
        if pid == "other":
            continue
        body = content.get(pid)
        if not body:
            print("skip missing content", pid)
            continue
        items = [
            it
            for it in index
            if it.get("primary") == pid
            and it.get("platform") != "personal"
            and "个人专栏" not in (it.get("tags") or [])
        ]
        # validate evidence
        for vp in body.get("viewpoints") or []:
            kept = []
            for s in vp.get("evidence_slugs") or []:
                if s in slug_map:
                    kept.append(s)
                else:
                    missing.append((pid, s))
            vp["evidence_slugs"] = kept[:3]

        filename = f"{pid}-总结.html"
        path = OUT_DIR / filename
        path.write_text(page_html(primary, body, items, slug_map), encoding="utf-8")
        print("wrote", path.relative_to(ROOT), "items", len(items))

        # representative chapter cards: evidence first, then latest
        seen = set()
        chapter_items = []
        for vp in body.get("viewpoints") or []:
            for s in vp.get("evidence_slugs") or []:
                if s in seen:
                    continue
                seen.add(s)
                it = slug_map[s]
                chapter_items.append(
                    {
                        "order": len(chapter_items) + 1,
                        "title": it.get("title") or s,
                        "summary": (it.get("summary") or "")[:80],
                        "filename": (it.get("outputs") or {}).get("html") or f"{s}-图文实录.html",
                    }
                )
                if len(chapter_items) >= 8:
                    break
            if len(chapter_items) >= 8:
                break

        topics.append(
            {
                "id": f"cat-{pid}",
                "primary": pid,
                "title": f"{primary['label']} · 核心观点",
                "subtitle": f"类目导读 · {len(items)} 篇",
                "summary": body.get("thesis") or "",
                "tags": [primary["label"], "类目总结"],
                "stats": {"images": len(items)},
                "cover": f"category-summaries/{filename}",
                "items": chapter_items,
            }
        )

    # Keep any existing non cat-* topics
    existing = []
    if TOPICS.exists():
        try:
            raw = json.loads(TOPICS.read_text(encoding="utf-8"))
            existing = [t for t in raw if not str(t.get("id", "")).startswith("cat-")]
        except Exception:
            existing = []
    TOPICS.write_text(json.dumps(existing + topics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote", TOPICS.relative_to(ROOT), "topics", len(existing) + len(topics))
    if missing:
        print("missing evidence slugs:", len(missing))
        for m in missing[:20]:
            print(" ", m)


if __name__ == "__main__":
    main()
