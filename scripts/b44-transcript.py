#!/usr/bin/env python3
"""b44：为图文实录 HTML 生成逐段完整转录区块并替换。

- 读取 {slug}.json（whisper）+ terms-{slug}.json（采用项做术语校正）
- 简体转换（opencc t2s）+ 术语校正
- 替换 HTML 中 <div class="transcript-list">...</div> 的内容
"""
from __future__ import annotations

import json
import re
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

# slug -> whisper JSON 文件名
SLUG_TO_AUDIO = {
    "no-many-clothes": "d01",
    "wulingshan-aranya": "d02",
    "easy-pose-simple": "d03",
    "urban-village-answer": "d04",
    "one-house-vs-zijian": "d05",
}


def fmt(t: float) -> str:
    t = max(0, int(t))
    return f"{t // 60:02d}:{t % 60:02d}"


def to_simplified(s: str) -> str:
    if _T2S:
        return _T2S.convert(s)
    if _zh_convert:
        return _zh_convert(s, "zh-cn")
    return s


def build_transcript(slug: str) -> str:
    whisper = json.loads((ROOT / f"{SLUG_TO_AUDIO[slug]}.json").read_text(encoding="utf-8"))
    terms_path = ROOT / f"terms-{slug}.json"
    replacements: dict[str, str] = {}
    if terms_path.exists():
        terms = json.loads(terms_path.read_text(encoding="utf-8"))["terms"]
        for t in terms:
            if t.get("adopted") and t.get("corrected") not in ("无法确认",):
                replacements[to_simplified(t["original"])] = to_simplified(t["corrected"])

    rows = []
    for seg in whisper.get("segments", []):
        text = (seg.get("text") or "").strip()
        if not text:
            continue
        text = to_simplified(text)
        for orig, corr in replacements.items():
            text = text.replace(orig, corr)
        rows.append(
            f'<div class="transcript-row"><time>{fmt(seg["start"])}</time>'
            f"<p>{text}</p></div>"
        )
    return "\n".join(rows)


def replace_in_html(slug: str) -> None:
    path = DOCS / f"{slug}-图文实录.html"
    html = path.read_text(encoding="utf-8")
    rows = build_transcript(slug)
    n = len(re.findall(r'class="transcript-row"', rows))
    # 替换 transcript-list 容器内容
    pattern = re.compile(
        r'(<div class="transcript-list">).*?(</div>\s*</div>\s*</details>)',
        re.S,
    )
    m = pattern.search(html)
    if not m:
        print(f"✗ {slug}: 找不到 transcript-list 容器")
        return
    html = html[: m.start()] + m.group(1) + "\n" + rows + "\n" + m.group(2) + html[m.end():]
    # 更新 summary 中的段数
    html = re.sub(
        r"(<summary>完整转录（)\d+(段）)",
        lambda mm: mm.group(1) + str(n) + mm.group(2),
        html,
    )
    path.write_text(html, encoding="utf-8")
    print(f"✓ {slug}: 转录 {n} 段已替换")


if __name__ == "__main__":
    for s in sys.argv[1:] or [
        "no-many-clothes",
        "wulingshan-aranya",
        "easy-pose-simple",
        "urban-village-answer",
        "one-house-vs-zijian",
    ]:
        replace_in_html(s)
    print("完成")
