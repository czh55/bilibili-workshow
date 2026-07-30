#!/usr/bin/env python3
"""Build HTML + SVG article pair from whisper JSON and chapter definitions."""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

COLLAPSE_CSS = (
    ".transcript-collapsible{border:none;margin:0;padding:0}"
    ".transcript-collapsible summary{display:flex;align-items:center;gap:10px;cursor:pointer;"
    "list-style:none;user-select:none;font-size:24px;font-weight:700;color:#1c1917;margin:0;"
    "padding-bottom:8px;border-bottom:2px solid #e7e5e4}"
    ".transcript-collapsible summary::-webkit-details-marker,.transcript-collapsible summary::marker{display:none}"
    ".transcript-collapsible summary::before{content:\"▶\";font-size:12px;color:#b45309;transition:transform .2s;flex-shrink:0}"
    ".transcript-collapsible[open] summary::before{transform:rotate(90deg)}"
    ".transcript-collapsible[open] summary{margin-bottom:16px}"
    ".transcript-collapsible .transcript-body{margin-top:0}"
)

TRANSCRIPT_SCRIPT = (
    '<script>(function(){var d=document.querySelector(".transcript-collapsible");if(!d)return;'
    'function open(){d.setAttribute("open","")}'
    'document.querySelectorAll(\'a[href="#transcript"]\').forEach(function(a){a.addEventListener("click",open)});'
    'if(location.hash==="#transcript")open()})();</script>'
)

BASE_CSS = """*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font-family:"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.8;color:#292524;background:#fafaf9}
a{color:#9a3412;text-underline-offset:3px}
.container{width:min(960px,100%);margin:0 auto;padding:48px 32px 80px}
header{margin-bottom:40px}
header h1{font-size:32px;font-weight:900;color:#1c1917;margin:0 0 12px;line-height:1.3}
.meta-row{display:flex;gap:16px;flex-wrap:wrap;align-items:center;margin-bottom:16px}
.meta-tag{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600}
.tag-platform{background:#ff2442;color:#fff}
.tag-duration{background:#f1f5f9;color:#64748b}
.source-link{color:#3b82f6;font-size:14px;text-decoration:none}
h2{font-size:24px;font-weight:700;color:#1c1917;margin:0 0 16px;padding-bottom:8px;border-bottom:2px solid #e7e5e4}
h3{font-size:20px;font-weight:700;color:#1c1917;margin:28px 0 14px}
p{margin:0 0 14px;color:#44403c}
.time-marker{display:inline-block;padding:2px 8px;background:#fef3c7;border-radius:6px;font-size:13px;font-weight:700;color:#b45309;margin-right:6px;font-variant-numeric:tabular-nums}
img{display:block;max-width:100%;height:auto}
figure{margin:28px 0;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(41,37,36,.1)}
figcaption{padding:14px 18px;color:#57534e;font-size:14px}
figcaption .time-badge{font-weight:700;color:#b45309;margin-right:6px}
.story-section{margin:48px 0}
.transcript-section{margin-top:48px}
.transcript-note{font-size:14px;color:#78716c;margin-bottom:24px}
.transcript-list{list-style:none;padding:0}
.transcript-row{display:grid;grid-template-columns:72px 1fr;gap:16px;padding:14px 0;border-bottom:1px solid #e7e5e4}
.transcript-row time{font-variant-numeric:tabular-nums;color:#b45309;font-weight:700}
.transcript-row p{margin:0}
.summary-row{display:flex;gap:12px;padding:16px 20px;background:#fff;border-radius:12px;margin-bottom:12px;box-shadow:0 2px 12px rgba(0,0,0,.04);align-items:flex-start}
.summary-row .time-marker{flex-shrink:0;margin-top:2px}
.summary-row strong{display:block;font-size:16px;color:#1c1917;margin-bottom:4px}
.summary-row p{color:#57534e;margin:0;font-size:15px}
.takeaway-box{background:#eff6ff;border-left:4px solid #3b82f6;border-radius:12px;padding:16px 20px;margin-top:20px}
.takeaway-box strong{display:block;font-size:16px;color:#1e40af;margin-bottom:6px}
.takeaway-box p{color:#3b82f6;margin:0;font-size:15px}
@media(max-width:640px){.container{padding:28px 18px 56px}header h1{font-size:24px}.transcript-row{grid-template-columns:56px 1fr;gap:10px}}
"""


def fmt_time(sec: float) -> str:
    sec = max(0, int(sec))
    return f"{sec // 60:02d}:{sec % 60:02d}"


def build_transcript_rows(segments):
    rows = []
    for seg in segments:
        text = (seg.get("text") or "").strip()
        if not text:
            continue
        rows.append(
            f'<li class="transcript-row"><time>{fmt_time(seg["start"])}</time>'
            f"<p>{html.escape(text)}</p></li>"
        )
    return "\n".join(rows)


def build_html(meta: dict) -> str:
    slug = meta["slug"]
    whisper = json.loads((ROOT / f"{slug}.json").read_text(encoding="utf-8"))
    segments = whisper.get("segments") or []
    seg_count = len([s for s in segments if (s.get("text") or "").strip()])

    summary_rows = []
    for row in meta.get("summary_rows", []):
        summary_rows.append(
            f'<div class="summary-row"><span class="time-marker">{html.escape(row["time"])}</span>'
            f"<div><strong>{html.escape(row['title'])}</strong>"
            f"<p>{html.escape(row['text'])}</p></div></div>"
        )

    sections = []
    for sec in meta.get("sections", []):
        fig = ""
        if sec.get("shot"):
            fig = (
                f'<figure><img src="assets/{slug}/{sec["shot"]}" '
                f'alt="{html.escape(sec.get("alt", ""))}" loading="lazy">'
                f'<figcaption><span class="time-badge">[{sec.get("shot_time", "")}]</span>'
                f'{html.escape(sec.get("caption", ""))}</figcaption></figure>'
            )
        sections.append(
            f'<section class="story-section" id="{sec["id"]}">'
            f'<span class="time-marker">{html.escape(sec["time"])}</span>'
            f"<h3>{html.escape(sec['title'])}</h3>"
            f"<p>{html.escape(sec['body'])}</p>{fig}</section>"
        )

    transcript = build_transcript_rows(segments)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="{html.escape(meta['description'])}">
<title>{html.escape(meta['title'])}｜图文实录</title>
<style>{BASE_CSS}{COLLAPSE_CSS}</style>
</head><body><main class="container">
<header><h1>{html.escape(meta['title'])}</h1>
<div class="meta-row"><span class="meta-tag tag-platform">小红书</span>
<span class="meta-tag tag-duration">{html.escape(meta['duration'])}</span></div>
<a class="source-link" href="{html.escape(meta['url'])}" target="_blank" rel="noopener">原视频链接</a></header>
<article><h2>内容要点</h2>
<p>{html.escape(meta['intro'])}</p>
<h3>知识结构</h3>
{''.join(summary_rows)}
<div class="takeaway-box"><strong>总结</strong><p>{html.escape(meta['takeaway'])}</p></div>
{''.join(sections)}
</article>
<section class="transcript-section" id="transcript"><details class="transcript-collapsible"><summary>详细文字转录</summary><div class="transcript-body">
<p class="transcript-note">以下内容按 Whisper 原始分段完整呈现，可能包含识别误差。</p>
<ol class="transcript-list">{transcript}</ol>
</div></details></section>
</main>{TRANSCRIPT_SCRIPT}</body></html>"""


def card(title, blocks: list[str]) -> str:
    inner = "".join(blocks)
    return f'<div class="card"><h3>{html.escape(title)}</h3>{inner}</div>'


def build_svg(meta: dict) -> str:
    slug = meta["slug"]
    cards_html = []
    for c in meta.get("svg_cards", []):
        blocks = []
        if c.get("highlight"):
            blocks.append(f'<div class="highlight">{html.escape(c["highlight"])}</div>')
        if c.get("quote"):
            blocks.append(f'<div class="quote">{html.escape(c["quote"])}</div>')
        if c.get("action"):
            blocks.append(f'<div class="action">{html.escape(c["action"])}</div>')
        if c.get("pitfall"):
            blocks.append(f'<div class="pitfall">{html.escape(c["pitfall"])}</div>')
        cards_html.append(card(c["title"], blocks))

    timeline = []
    for t in meta.get("timeline", []):
        timeline.append(
            f'<div class="timeline-item"><span class="timeline-time">{html.escape(t["time"])}</span>'
            f'<span class="timeline-text">{html.escape(t["text"])}</span></div>'
        )

    tags = "".join(f'<span class="tag tag-blue">{html.escape(t)}</span>' for t in meta.get("tags", []))

    body = f"""
<div class="container root-wrap">
  <h1>{html.escape(meta['title'])}</h1>
  <div class="meta">{tags}<span class="tag tag-gray">时长 {html.escape(meta['duration'])}</span></div>
  <a class="source-link" href="{html.escape(meta['url'])}">原视频链接</a>
  <div class="summary-line">{html.escape(meta['svg_summary'])}</div>
  <div class="timeline"><h3>关键证据时间轴</h3>{''.join(timeline)}</div>
  <div class="section"><div class="sec-title">观点拆解</div>{''.join(cards_html)}</div>
  <div class="conclusion"><h2>行动清单</h2><ul>{''.join(f'<li>{html.escape(x)}</li>' for x in meta.get('actions', []))}</ul>
  <h2>适用边界</h2><p>{html.escape(meta.get('boundary', ''))}</p></div>
  <div class="footer">双轨产物之二 · SVG 理性分析 · {html.escape(meta['url'])}</div>
</div>"""

    svg_css = open(DOCS / "zara-efficient-shopping-理性分析.svg", encoding="utf-8").read()
    style_match = re.search(r"<style>(.*?)</style>", svg_css, re.S)
    style = style_match.group(1) if style_match else ""

    # rough height estimate
    height = 1200 + len(meta.get("svg_cards", [])) * 280 + len(meta.get("timeline", [])) * 40

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1320" height="{height}" viewBox="0 0 1320 {height}">
  <foreignObject x="0" y="0" width="1320" height="{height}">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <style>{style}</style>
      {body}
    </div>
  </foreignObject>
</svg>"""


def main():
    meta_path = Path(sys.argv[1])
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    slug = meta["slug"]
    html_out = DOCS / f"{slug}-图文实录.html"
    svg_out = DOCS / f"{slug}-理性分析.svg"
    html_out.write_text(build_html(meta), encoding="utf-8")
    svg_out.write_text(build_svg(meta), encoding="utf-8")
    print("Wrote", html_out.name, svg_out.name)


if __name__ == "__main__":
    main()
