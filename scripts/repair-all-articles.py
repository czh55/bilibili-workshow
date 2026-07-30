#!/usr/bin/env python3
"""Batch-repair article editorial content from local HTML transcripts only."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

from opencc import OpenCC

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
INDEX_PATH = DOCS / "index.json"
ASSET_COMMIT = "4044dda"

FIXED_SLUGS = {
    "46x57MKFAHe",
    "7FNwup3V9Db",
    "6H7J3y4tlG8",
    "1AxRcAB6tiJ",
    "9tlnJv08wB7",
    "30n65p4dVJB",
    "eyebrow-face-value",
}

cc = OpenCC("t2s")

TIME_RE = re.compile(
    r'<li class="transcript-row"><time>(\d{2}):(\d{2})</time><p>(.*?)</p></li>',
    re.DOTALL,
)
SEGMENT_RE = re.compile(
    r'<section class="transcript-section">.*?</section>',
    re.DOTALL,
)
ARTICLE_RE = re.compile(r"<article>.*?</article>", re.DOTALL)


def to_simplified(text: str) -> str:
    text = html.unescape(re.sub(r"<[^>]+>", "", text or ""))
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return ""
    return cc.convert(text)


def parse_time_mmss(mm: str, ss: str) -> int:
    return int(mm) * 60 + int(ss)


def format_range(start: float, end: float) -> str:
    def fmt(sec: float) -> str:
        sec = max(0, int(sec))
        return f"{sec // 60:02d}:{sec % 60:02d}"

    return f"{fmt(start)}—{fmt(end)}"


def parse_duration_seconds(duration: str | None, segments: list[dict]) -> int:
    if duration:
        m = re.search(r"(\d+)\s*分\s*(\d+)?", duration)
        if m:
            return int(m.group(1)) * 60 + int(m.group(2) or 0)
        m = re.search(r"(\d+):(\d+)", duration)
        if m:
            return int(m.group(1)) * 60 + int(m.group(2))
        m = re.search(r"(\d+)\s*秒", duration)
        if m:
            return int(m.group(1))
    if segments:
        return int(segments[-1]["start"]) + 5
    return 60


def parse_segments(page_html: str) -> list[dict]:
    segments = []
    for mm, ss, body in TIME_RE.findall(page_html):
        text = to_simplified(body)
        if not text:
            continue
        segments.append({"start": parse_time_mmss(mm, ss), "text": text})
    return segments


def is_mostly_english(text: str) -> bool:
    ascii_letters = sum(1 for c in text if c.isascii() and c.isalpha())
    chinese = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
    return ascii_letters > max(chinese, 1) * 1.5


def clean_clause(text: str) -> str:
    text = text.strip(" 。；，,;")
    if len(text) < 2:
        return ""
    if re.fullmatch(r"(嗯|啊|哦|OK|好|对的|对吧|然后呢|就是说)", text, re.I):
        return ""
    if re.fullmatch(r"[A-Za-z0-9\W]+", text) and len(text) < 8:
        return ""
    return text


def summarize_segments(segments: list[dict]) -> str:
    clauses: list[str] = []
    for seg in segments:
        clause = clean_clause(seg["text"])
        if not clause:
            continue
        if clauses and clauses[-1] == clause:
            continue
        clauses.append(clause)

    if not clauses:
        return "本段以画面演示和配乐为主，口播内容较少。"

    joined = "。".join(clauses)
    if is_mostly_english(joined):
        picked = [c for c in clauses if len(c) > 12][:3]
        if not picked:
            picked = clauses[:2]
        return (
            "本段为英语讲解，主要内容包括："
            + "；".join(picked)
            + "。（完整英文转录见文末。）"
        )

    paragraph = "。".join(clauses[:10])
    if len(paragraph) > 320:
        cut = paragraph[:317]
        last = max(cut.rfind("。"), cut.rfind("；"), cut.rfind("，"))
        paragraph = (cut[:last] if last > 120 else cut) + "…"
    return paragraph


def chapter_count(total_sec: int) -> int:
    if total_sec < 75:
        return 2
    if total_sec < 150:
        return 3
    if total_sec < 300:
        return 4
    return 5


def chapter_title(index: int, total: int, segments: list[dict]) -> str:
    joined = " ".join(seg["text"] for seg in segments[:6])
    rules = [
        (r"第一|首先|开头|开场|介绍", "开场与主题引入"),
        (r"第二|接着|然后|下一步|第二步", "核心操作步骤"),
        (r"第三|再|另外|其次", "关键技巧展开"),
        (r"第四|进阶|优化|调整", "进阶设置与优化"),
        (r"最后|总结|以上就是|结尾|收束", "总结与收束"),
        (r"对比|区别|错误|正确", "对比与判断"),
        (r"原理|为什么|机制", "原理说明"),
        (r"设置|快捷键|参数|步骤", "设置与操作流程"),
        (r"拍摄|构图|镜头|相机|灯光", "拍摄与画面处理"),
        (r"剪辑|转场|音效|封面|排版", "剪辑与呈现处理"),
    ]
    for pattern, title in rules:
        if re.search(pattern, joined):
            return title
    defaults = ["开场引入", "核心内容", "操作演示", "进阶技巧", "总结收束"]
    return defaults[min(index, len(defaults) - 1)]


def split_chapters(segments: list[dict], total_sec: int) -> list[tuple[float, float, list[dict]]]:
    count = chapter_count(total_sec)
    if not segments:
        return []
    end_sec = max(total_sec, segments[-1]["start"] + 1)
    step = end_sec / count
    chapters = []
    for i in range(count):
        start = i * step
        end = end_sec if i == count - 1 else (i + 1) * step
        chunk = [s for s in segments if start <= s["start"] < end]
        if chunk:
            chapters.append((start, min(end, chunk[-1]["start"] + 1), chunk))
    return chapters


def list_shots(slug: str) -> list[Path]:
    asset_dir = DOCS / "assets" / slug
    if not asset_dir.exists():
        return []
    return sorted(asset_dir.glob("shot-*.jpg"))


def assign_figures(shots: list[Path], chapter_total: int) -> list[Path | None]:
    figures: list[Path | None] = [None] * chapter_total
    if not shots or chapter_total == 0:
        return figures
    picks = [shots[0]]
    if len(shots) > 2:
        picks.append(shots[len(shots) // 2])
    if len(shots) > 1:
        picks.append(shots[-1])
    unique_picks: list[Path] = []
    for shot in picks:
        if shot not in unique_picks:
            unique_picks.append(shot)
    slots = [0]
    if chapter_total > 2:
        slots.append(chapter_total // 2)
    if chapter_total > 1:
        slots.append(chapter_total - 1)
    for slot, shot in zip(slots, unique_picks):
        figures[slot] = shot
    return figures


def make_intro(title: str, chapters: list[tuple[float, float, list[dict]]]) -> str:
    title = to_simplified(title)
    if chapters:
        lead = summarize_segments(chapters[0][2])
        lead = lead.split("。")[0]
        if len(lead) > 80:
            lead = lead[:77] + "…"
        return f"这段视频围绕「{title}」展开，按时间介绍其中的关键环节。{lead}。"
    return f"这段视频围绕「{title}」展开，结合画面与口播说明相关做法与判断标准。"


def make_index_summary(intro: str, chapters: list[tuple[float, float, list[dict]]]) -> str:
    parts = [intro.split("。")[0]]
    if len(chapters) > 1:
        parts.append(summarize_segments(chapters[1][2]).split("。")[0])
    summary = "。".join(p for p in parts if p)
    summary = re.sub(r"\s+", "", summary)
    if len(summary) > 118:
        summary = summary[:117] + "…"
    return summary


def build_article(title: str, duration: str | None, slug: str, page_html: str) -> tuple[str, str]:
    segments = parse_segments(page_html)
    total_sec = parse_duration_seconds(duration, segments)
    chapters = split_chapters(segments, total_sec)
    shots = list_shots(slug)
    figures = assign_figures(shots, len(chapters))
    intro = make_intro(title, chapters)

    parts = ['<article><h2>内容要点</h2>', f"<p>{html.escape(intro)}</p>"]
    for idx, (start, end, chunk) in enumerate(chapters):
        heading = chapter_title(idx, len(chapters), chunk)
        body = summarize_segments(chunk)
        parts.append('<section class="story-section">')
        parts.append(f'<span class="time-marker">{format_range(start, end)}</span>')
        parts.append(f"<h3>{html.escape(heading)}</h3>")
        parts.append(f"<p>{html.escape(body)}</p>")
        shot = figures[idx]
        if shot:
            rel = f"assets/{slug}/{shot.name}"
            stamp = format_range(chunk[0]["start"], chunk[0]["start"]).split("—")[0]
            parts.append(
                f'<figure><img src="{rel}" alt="{html.escape(title)} {html.escape(heading)}" loading="lazy">'
                f'<figcaption>[{stamp}] {html.escape(heading)}相关画面。</figcaption></figure>'
            )
        parts.append("</section>")

    if chapters:
        parts.append(
            '<div class="takeaway-box"><strong>总结</strong>'
            f'<p>{html.escape(summarize_segments(chapters[-1][2]).split("。")[0] or intro.split("。")[0])}。</p></div>'
        )
    parts.append("</article>")
    article_html = "\n".join(parts)
    summary = make_index_summary(intro, chapters)
    return article_html, summary


def needs_repair(slug: str, page_html: str, date: str | None) -> bool:
    if slug in FIXED_SLUGS:
        return False
    if 'class="story-section"' in page_html and "summary-row" not in page_html:
        if date not in {"2026-07-29", "2026-07-30"}:
            return False
        if not re.search(r"这是一个(原理科普|步骤教学)视频|视频围绕<strong>", page_html):
            return False
    if "summary-row" in page_html:
        return True
    if re.search(r"这是一个(原理科普|步骤教学)视频|视频围绕<strong>", page_html):
        return True
    if date in {"2026-07-29", "2026-07-30"} and 'class="story-section"' not in page_html:
        return True
    return False


def restore_assets() -> None:
    subprocess.run(
        ["git", "restore", "--source", ASSET_COMMIT, "--", "docs/assets"],
        cwd=ROOT,
        check=True,
    )


def repair_file(slug: str, title: str, duration: str | None) -> tuple[str, str] | None:
    html_path = DOCS / f"{slug}-图文实录.html"
    page = html_path.read_text(encoding="utf-8")
    if not ARTICLE_RE.search(page) or not SEGMENT_RE.search(page):
        return None
    article_html, summary = build_article(title, duration, slug, page)
    new_page = ARTICLE_RE.sub(article_html, page, count=1)
    html_path.write_text(new_page, encoding="utf-8")
    return summary


def main() -> int:
    restore_assets()
    items = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    repaired = 0
    skipped = 0

    for item in items:
        if item.get("error"):
            continue
        outputs = item.get("outputs") or {}
        html_file = outputs.get("html")
        if not html_file:
            continue
        slug = html_file.replace("-图文实录.html", "")
        html_path = DOCS / html_file
        if not html_path.exists():
            skipped += 1
            continue
        page = html_path.read_text(encoding="utf-8")
        if not needs_repair(slug, page, item.get("date")):
            continue
        result = repair_file(slug, item.get("title", slug), item.get("duration"))
        if not result:
            skipped += 1
            continue
        item["summary"] = result[1]
        repaired += 1

    INDEX_PATH.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"repaired={repaired} skipped={skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
