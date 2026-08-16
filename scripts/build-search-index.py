#!/usr/bin/env python3
"""构建 docs/search-index.json（首页全文搜索索引）。

数据源：
  - docs/index.json            元数据（title/summary/tags/platform/date/duration/outputs）
  - scripts/scene-data/{slug}.json  结构化正文（中/英文，优先）
  - docs/{slug}-图文实录.html        中文正文回退（scene-data 缺失时）
  - docs/{slug}-场景英译.html        英文正文回退（scene-data 缺失时）

输出：
  docs/search-index.json，数组，每条含 title/title_en/summary/tags/platform/date/
  duration/html/svg/html_en/body/body_en。body 为中文全文、body_en 为英文全文，
  供前端中英文搜索匹配与摘要。
"""
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
SCENE = os.path.join(ROOT, "scripts", "scene-data")

_SCRIPT_STYLE = re.compile(r"<(script|style)[\s\S]*?</\1>", re.I)


class _TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip += 1
        elif tag in ("p", "div", "li", "h1", "h2", "h3", "h4", "blockquote", "figcaption", "br", "tr"):
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip > 0:
            self._skip -= 1

    def handle_data(self, data):
        if self._skip == 0:
            self.parts.append(data)


def extract_text_from_html(path):
    """提取 HTML 正文纯文本，去 script/style 与空白折叠。"""
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    raw = _SCRIPT_STYLE.sub(" ", raw)
    parser = _TextExtractor()
    parser.feed(raw)
    text = "".join(parser.parts)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_title_en(path, zh_title):
    """从场景英译 HTML 提取英文标题。

    策略：英文标题紧跟在中文标题之后（正文开头 `中文标题 英文标题` 连续出现），
    找到中文标题的结束位置，取其后第一个含至少 3 个英文单词的句段。
    """
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    raw = _SCRIPT_STYLE.sub(" ", raw)
    parser = _TextExtractor()
    parser.feed(raw)
    text = "".join(parser.parts)
    text = re.sub(r"\s+", " ", text).strip()

    idx = text.rfind(zh_title) if zh_title else -1
    start = idx + len(zh_title) if idx != -1 else 0
    tail = text[start:]
    # 英文标题以日期（YYYY-MM-DD）结束，取日期前的英文句段
    m = re.search(r"([A-Za-z][A-Za-z ,'’\-&()]{5,})\s+\d{4}-\d{2}-\d{2}", tail)
    if not m:
        # 无日期时，取第一个含 >=3 个英文单词的句段
        m = re.search(r"([A-Za-z][A-Za-z ,'’\-&()]{10,})", tail)
    if not m:
        return ""
    cand = m.group(1).strip().rstrip("，。.!?,")
    if len(re.findall(r"[A-Za-z]{3,}", cand)) < 3:
        return ""
    return cand


def slug_from_outputs(item):
    html = (item.get("outputs") or {}).get("html") or ""
    html_en = (item.get("outputs") or {}).get("html_en") or ""
    for candidate in (html, html_en, item.get("filename") or ""):
        if not candidate:
            continue
        base = candidate.rsplit("/", 1)[-1]
        for suffix in ("-图文实录.html", "-场景英译.html", ".html"):
            if base.endswith(suffix):
                return base[: -len(suffix)]
    return ""


def scene_body(slug):
    """从 scene-data JSON 提取中文全文。失败返回 None。"""
    path = os.path.join(SCENE, slug + ".json")
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    parts = []
    scenes = data.get("scenes") or []
    for s in scenes:
        if s.get("title_cn"):
            parts.append(s["title_cn"])
        if s.get("context"):
            parts.append(s["context"])
        for row in s.get("sentences") or []:
            if row and isinstance(row, list) and row[0]:
                parts.append(row[0])
        for row in s.get("paraphrase") or []:
            if row and isinstance(row, list) and row[0]:
                parts.append(row[0])
    for row in data.get("pitfalls") or []:
        if isinstance(row, list):
            parts.extend(str(x) for x in row if x)
    for row in data.get("shifts") or []:
        if isinstance(row, list):
            parts.extend(str(x) for x in row if x)
    for row in data.get("practice") or []:
        if isinstance(row, list):
            parts.extend(str(x) for x in row if x)
    if data.get("footer_notes"):
        parts.append(data["footer_notes"])

    return re.sub(r"\s+", " ", " ".join(parts)).strip()


def scene_body_en(slug):
    """从 scene-data JSON 提取英文全文。失败返回 None。"""
    path = os.path.join(SCENE, slug + ".json")
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    parts = []
    meta = data.get("meta") or {}
    if meta.get("title_en"):
        parts.append(meta["title_en"])
    scenes = data.get("scenes") or []
    for s in scenes:
        if s.get("title_en"):
            parts.append(s["title_en"])
        for row in s.get("sentences") or []:
            if row and isinstance(row, list) and len(row) > 1 and row[1]:
                parts.append(row[1])
        if s.get("speak"):
            parts.append(s["speak"])
        for row in s.get("paraphrase") or []:
            if row and isinstance(row, list):
                parts.extend(str(x) for x in row[:2] if x)
    for row in data.get("practice") or []:
        if isinstance(row, list) and len(row) > 1 and row[1]:
            parts.append(str(row[1]))
    for row in data.get("pitfalls") or []:
        if isinstance(row, list):
            parts.extend(str(x) for x in row[:2] if x)
    for row in data.get("shifts") or []:
        if isinstance(row, list) and len(row) > 1 and row[1]:
            parts.append(str(row[1]))
    for w in data.get("difficult_words") or []:
        if w:
            parts.append(str(w))
    if data.get("footer_notes"):
        parts.append(data["footer_notes"])

    return re.sub(r"\s+", " ", " ".join(parts)).strip()


def main():
    with open(os.path.join(DOCS, "index.json"), encoding="utf-8") as f:
        index = json.load(f)

    out = []
    missing_scene = []
    no_body = []
    no_body_en = []

    for item in index:
        slug = slug_from_outputs(item)
        body = scene_body(slug) if slug else None
        if body is None:
            missing_scene.append(slug)
            if slug:
                html_path = os.path.join(DOCS, f"{slug}-图文实录.html")
                if os.path.isfile(html_path):
                    body = extract_text_from_html(html_path)
        if not body:
            no_body.append(slug)

        body_en = scene_body_en(slug) if slug else None
        title_en = ""
        scene_path = os.path.join(SCENE, slug + ".json") if slug else ""
        if scene_path and os.path.isfile(scene_path):
            with open(scene_path, encoding="utf-8") as f:
                title_en = ((json.load(f).get("meta") or {}).get("title_en")) or ""
        if body_en is None and slug:
            en_path = os.path.join(DOCS, f"{slug}-场景英译.html")
            if os.path.isfile(en_path):
                body_en = extract_text_from_html(en_path)
                if not title_en:
                    title_en = extract_title_en(en_path, item.get("title", ""))
        if not body_en:
            no_body_en.append(slug)

        outputs = item.get("outputs") or {}
        entry = {
            "title": item.get("title", ""),
            "title_en": title_en,
            "summary": item.get("summary", ""),
            "tags": item.get("tags") or [],
            "platform": item.get("platform", ""),
            "date": item.get("date", ""),
            "duration": item.get("duration", ""),
            "html": outputs.get("html", ""),
            "svg": outputs.get("svg", ""),
            "html_en": outputs.get("html_en", ""),
            "body": body or "",
            "body_en": body_en or "",
        }
        out.append(entry)

    out_path = os.path.join(DOCS, "search-index.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))

    size = os.path.getsize(out_path)
    print(f"索引条数: {len(out)} / {len(index)}")
    print(f"scene-data 缺失(HTML 回退): {len(missing_scene)} 条 -> {missing_scene[:5]}")
    print(f"无正文: {len(no_body)} 条 -> {no_body[:5]}")
    print(f"无英文正文: {len(no_body_en)} 条 -> {no_body_en[:5]}")
    print(f"输出: {out_path} ({size/1024:.1f} KB)")

    if len(out) != len(index):
        sys.exit("错误：索引条数与 index.json 不一致")


if __name__ == "__main__":
    main()
