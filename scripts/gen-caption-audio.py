#!/usr/bin/env python3
"""为所有图文实录 HTML 的图片 caption 生成英文朗读音频。

逻辑：
- 收集全部 HTML 中 figcaption 的中文文本（与 extract-captions.py 同源）
- 按中文文本去重，用 edge-tts 生成 docs/audio/{md5(zh)[:12]}.mp3
- 已存在的文件跳过，可重复执行续跑
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import re
import sys
from pathlib import Path

import edge_tts

DOCS = Path(__file__).resolve().parent.parent / "docs"
AUDIO_DIR = DOCS / "audio"
EN_VOICE = "en-US-JennyNeural"
CONCURRENCY = 8

TIME_RE = re.compile(r"\[(\d{1,2}:\d{2}(?::\d{2})?)\]")
BADGE_RE = re.compile(r"<span class=\"time-badge\">\[.*?\]</span>", re.S)


def strip_html(s: str) -> str:
    return (
        re.sub(r"<[^>]+>", "", s)
        .replace("&quot;", '"')
        .replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .strip()
    )


def collect_captions() -> list[tuple[str, str]]:
    """返回 [(zh, en), ...] 去重后的 caption 对。"""
    translations = json.loads(
        (Path(__file__).resolve().parent.parent / "translations.json").read_text(encoding="utf-8")
    )
    items: list[tuple[str, str]] = []
    seen: set[str] = set()
    for f in sorted(DOCS.glob("*-图文实录.html")):
        html = f.read_text(encoding="utf-8")
        for fig in re.findall(r"<figure>.*?</figure>", html, re.S):
            cap_m = re.search(r"<figcaption>(.*?)</figcaption>", fig, re.S)
            if not cap_m:
                continue
            text = strip_html(cap_m.group(1))
            time_m = TIME_RE.search(text)
            zh = text[time_m.end():].strip(" ：: ") if time_m else text
            zh = zh.strip()
            if zh and zh not in seen:
                seen.add(zh)
                items.append((zh, translations.get(zh, "")))
    return items


def audio_path(zh: str) -> Path:
    h = hashlib.md5(zh.encode("utf-8")).hexdigest()[:12]
    return AUDIO_DIR / f"{h}.mp3"


async def synthesize_one(pair: tuple[str, str], sem: asyncio.Semaphore) -> bool:
    zh, en = pair
    if not en:
        print(f"  ! no-en {zh[:20]}...")
        return False
    out = audio_path(zh)
    if out.exists() and out.stat().st_size > 100:
        return True
    async with sem:
        try:
            out.parent.mkdir(parents=True, exist_ok=True)
            communicate = edge_tts.Communicate(en, EN_VOICE)
            await communicate.save(str(out))
            return out.exists() and out.stat().st_size > 100
        except Exception as exc:  # noqa: BLE001
            print(f"  ✗ {en[:30]}... → {exc}")
            return False


async def main() -> None:
    texts = collect_captions()
    print(f"unique captions: {len(texts)}")
    sem = asyncio.Semaphore(CONCURRENCY)
    results = await asyncio.gather(*(synthesize_one(t, sem) for t in texts))
    ok = sum(1 for r in results if r)
    print(f"done: {ok}/{len(texts)} audio files")
    sys.exit(0 if ok == len(texts) else 1)


if __name__ == "__main__":
    asyncio.run(main())
