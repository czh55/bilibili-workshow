#!/usr/bin/env python3
"""b47：生成 93 篇本地视频图文实录 HTML。

数据来源：scripts/b47_data.py（内容数据）+ _work/b47/transcripts/{key}.json（Whisper 转录）
用法：
  python3 scripts/b47-html.py {slug} [{slug} ...]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import opencc
    _T2S = opencc.OpenCC("t2s")
except ImportError:
    _T2S = None
try:
    from zhconv import convert as _zh_convert
except ImportError:
    _zh_convert = None

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
TRANSCRIPTS = ROOT / "_work" / "b47" / "transcripts"


def to_simplified(s: str) -> str:
    if _T2S:
        return _T2S.convert(s)
    if _zh_convert:
        return _zh_convert(s, "zh-cn")
    return s


def fmt(t: float) -> str:
    t = max(0, int(t))
    return f"{t // 60:02d}:{t % 60:02d}"


def build_transcript(key: str) -> tuple[str, int]:
    whisper = json.loads((TRANSCRIPTS / f"{key}.json").read_text(encoding="utf-8"))
    rows = []
    for seg in whisper.get("segments", []):
        text = (seg.get("text") or "").strip()
        if not text:
            continue
        text = to_simplified(text)
        rows.append(
            f'<div class="transcript-row"><time>{fmt(seg["start"])}</time>'
            f"<p>{text}</p></div>"
        )
    return "\n".join(rows), len(rows)


def build_html(slug: str, d: dict) -> str:
    shots = json.loads((ROOT / f"shots-{slug}.json").read_text(encoding="utf-8"))["shots"]
    fig_desc: dict[int, dict] = {}
    for s in shots:
        num = int(s["file"].replace("shot-", "").replace(".jpg", ""))
        fig_desc[num] = s

    transcript, n_seg = build_transcript(d["key"])

    summary_rows = "\n".join(
        f'<div class="summary-row"><span class="time-marker">[{tr}]</span>'
        f"<div><strong>{label}</strong><p>{txt}</p></div></div>"
        for tr, label, txt in d["summary_rows"]
    )

    toc_links = "".join(
        f'<a href="#{c["id"]}">{c["title"]}</a>' for c in d.get("chapters", [])
    )
    toc_links += '<a href="#transcript">完整转录</a>'

    story = []
    for c in d.get("chapters", []):
        paras = "".join(f"<p>{p}</p>" for p in c["paras"])
        figs = ""
        for num in c.get("figs", []):
            meta = fig_desc.get(num)
            if not meta:
                continue
            figs += f'<figure><img src="assets/{slug}/shot-{num:02d}.jpg" alt="{meta["scene"]}" loading="lazy"><figcaption><span class="time-badge">[{meta["time"]}]</span>{meta["scene"]}</figcaption></figure>'
        story.append(
            f'<section class="story-section" id="{c["id"]}">'
            f'<h2><span class="time-marker">{c["time"]}</span>{c["title"]}</h2>{paras}{figs}'
            f"</section>"
        )
    story_html = "\n".join(story)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="{d['intro'][:140]}">
<title>{d['title']}｜图文实录</title>
<style>*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}
body{{margin:0;font-family:"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.8;color:#292524;background:#fafaf9}}
.container{{width:min(960px,100%);margin:0 auto;padding:48px 32px 80px}}header{{margin-bottom:40px}}
header h1{{font-size:32px;font-weight:900;color:#1c1917;margin:0 0 12px;line-height:1.3}}
.meta-row{{display:flex;gap:16px;flex-wrap:wrap;align-items:center;margin-bottom:16px}}
.meta-tag{{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600}}
.tag-platform{{background:#ff2442;color:#fff}}.tag-duration{{background:#f1f5f9;color:#64748b}}.tag-topic{{background:#dbeafe;color:#1e40af}}
.source-link{{color:#3b82f6;font-size:14px;text-decoration:none}}.source-link:hover{{text-decoration:underline}}
.toc{{background:#fff;border-radius:16px;padding:20px 24px;margin-bottom:32px;box-shadow:0 2px 12px rgba(0,0,0,.04)}}
.toc h3{{font-size:16px;color:#1e40af;margin:0 0 12px}}.toc a{{display:block;color:#475569;font-size:14px;text-decoration:none;padding:4px 0;border-bottom:1px solid #f1f5f9}}.toc a:hover{{color:#3b82f6}}
.documentary{{font-size:17px}}.story-section{{margin:48px 0}}
.story-section h2{{font-size:24px;font-weight:700;color:#1c1917;margin:0 0 16px;padding-bottom:8px;border-bottom:2px solid #e7e5e4}}
.story-section p{{margin:0 0 14px;color:#44403c}}
.time-marker{{display:inline-block;padding:2px 8px;background:#fef3c7;border-radius:6px;font-size:13px;font-weight:700;color:#b45309;margin-right:6px;font-variant-numeric:tabular-nums}}
img{{display:block;max-width:100%;height:auto}}figure{{margin:28px 0;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(41,37,36,.1)}}
figcaption{{padding:14px 18px;color:#57534e;font-size:14px}}figcaption .time-badge{{font-weight:700;color:#b45309;margin-right:6px}}
.transcript-section{{margin-top:48px}}.transcript-section h2{{font-size:24px;font-weight:700;color:#1c1917}}
.transcript-note{{font-size:14px;color:#78716c;margin-bottom:24px}}.transcript-list{{list-style:none;padding:0}}
.transcript-row{{display:grid;grid-template-columns:72px 1fr;gap:16px;padding:14px 0;border-bottom:1px solid #e7e5e4}}
.transcript-row time{{font-variant-numeric:tabular-nums;color:#b45309;font-weight:700}}.transcript-row p{{margin:0}}
@media(max-width:640px){{.container{{padding:28px 18px 56px}}header h1{{font-size:24px}}.transcript-row{{grid-template-columns:56px 1fr;gap:10px}}}}
.transcript-collapsible{{border:none;margin:0;padding:0}}.transcript-collapsible summary{{display:flex;align-items:center;gap:10px;cursor:pointer;list-style:none;user-select:none;font-size:24px;font-weight:700;color:#1c1917;margin:0;padding-bottom:8px;border-bottom:2px solid #e7e5e4}}
.transcript-collapsible summary::-webkit-details-marker,.transcript-collapsible summary::marker{{display:none}}
.transcript-collapsible summary::before{{content:"▶";font-size:12px;color:#b45309;transition:transform .2s;flex-shrink:0}}
.transcript-collapsible[open] summary::before{{transform:rotate(90deg)}}.transcript-collapsible[open] summary{{margin-bottom:16px}}.transcript-collapsible .transcript-body{{margin-top:0}}
.summary-row{{display:flex;gap:12px;padding:16px 20px;background:#fff;border-radius:12px;margin-bottom:12px;box-shadow:0 2px 12px rgba(0,0,0,.04);align-items:flex-start}}
.summary-row .time-marker{{flex-shrink:0;margin-top:2px}}
.summary-row strong{{display:block;font-size:16px;color:#1c1917;margin-bottom:4px}}
.summary-row p{{color:#57534e;margin:0;font-size:15px}}
.takeaway-box{{background:#eff6ff;border-left:4px solid #3b82f6;border-radius:12px;padding:16px 20px;margin-top:20px}}
.takeaway-box strong{{display:block;font-size:16px;color:#1e40af;margin-bottom:6px}}
.takeaway-box p{{color:#3b82f6;margin:0;font-size:15px}}
.content-points h2{{font-size:24px;font-weight:700;color:#1c1917;margin:0 0 14px;padding-bottom:8px;border-bottom:2px solid #e7e5e4}}
.content-points h3{{font-size:20px;font-weight:700;color:#1c1917;margin:22px 0 14px}}
</style>
</head>
<body><main class="container">
<header><h1>{d['title_display']}</h1>
<div class="meta-row"><span class="meta-tag tag-platform">本地视频</span><span class="meta-tag tag-duration">{d['duration']}</span><span class="meta-tag tag-topic">{d['tags']}</span></div>
<a class="source-link" href="{d['url']}" target="_blank" rel="noopener">→ 原视频（本地文件）</a></header>
<nav class="toc"><h3>内容导航</h3>
{toc_links}</nav>
<article class="documentary"><div class="content-points"><h2>内容要点</h2><p>{d['intro']}</p><h3>知识结构</h3>
{summary_rows}
<div class="takeaway-box"><strong>总结</strong><p>{d['takeaway']}</p></div></div>
{story_html}
<section class="transcript-section" id="transcript"><details class="transcript-collapsible"><summary>完整转录（{n_seg}段）</summary>
<div class="transcript-body"><p class="transcript-note">以下文本由 Whisper medium 模型自动转录，可能存在少量识别误差，已尽可能修正。</p>
<div class="transcript-list">
{transcript}
</div></div></details></section>
</article>
</main>
</body></html>
"""


def generate(slug: str, data: dict) -> None:
    html = build_html(slug, data)
    out = DOCS / f"{slug}-图文实录.html"
    out.write_text(html, encoding="utf-8")
    print(f"✓ {slug}: {out.name} 生成")


def main() -> None:
    from b47_data import DATA

    args = sys.argv[1:]
    for s in args or list(DATA.keys()):
        generate(s, DATA[s])
    print("完成")


if __name__ == "__main__":
    main()
