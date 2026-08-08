#!/usr/bin/env python3
"""通用场景英译生成器：读取 scene-data/{slug}.json，批量产出音频 + HTML。

用法：
  python3 scripts/gen-scene-en.py --slug=motuo            # 音频 + HTML
  python3 scripts/gen-scene-en.py --slug=motuo --audio-only
  python3 scripts/gen-scene-en.py --slug=motuo --html-only
  python3 scripts/gen-scene-en.py --all --html-only       # 全部 scene-data 只出 HTML

scene-data/{slug}.json 结构：
{
  "meta": { "slug","title","title_en","duration","scenes","sentences","date","platform","source_url" },
  "scene_imgs": ["shot-01", ...],         # 与 scenes 等长，复用 assets/{slug}/
  "scenes": [
    {
      "id":"s1","title_cn","title_en","time","context",
      "sentences": [["zh","en","note"], ...],
      "paraphrase": [["intent -> alt","chunk · chunk"], ...],
      "speak": "场景英文口播文本"
    }, ...
  ],
  "practice": [["中文意图","英文例句"], ...],   # 4 个
  "pitfalls": [["wrong","right","why"], ...],   # 4 个
  "shifts": [["以前","新"], ...],               # 3 个
  "difficult_words": ["word", ...],             # ≥20
  "footer_notes": "ASR 校正说明"
}
"""
from __future__ import annotations

import asyncio
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DATA_DIR = ROOT / "scripts" / "scene-data"

ZH_VOICE = "zh-CN-XiaoxiaoNeural"
EN_VOICE = "en-US-JennyNeural"
MAX_CHUNK_LEN = 2000


def load_slug(slug: str) -> dict:
    p = DATA_DIR / f"{slug}.json"
    if not p.exists():
        raise SystemExit(f"missing scene-data: {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def estimate_duration(char_count: int) -> str:
    minutes = char_count / 280
    low = max(1, int(minutes))
    high = max(low, int(minutes + 0.99))
    if low == high:
        return f"约 {low} 分钟"
    return f"约 {low} 到 {high} 分钟"


def build_narration_script(data: dict) -> str:
    meta, scenes = data["meta"], data["scenes"]
    parts: list[str] = []
    total = len(scenes)
    parts.append(
        f"欢迎收听场景英译语音讲解。今天我们要学习的视频是「{meta['title']}」，"
        f"英文副标题：{meta['title_en']}。"
        f"视频总长{meta['duration']}，共分为{total}个场景、{meta['sentences']}句核心英文表达。"
        f"好，我们开始。"
    )
    for i, scene in enumerate(scenes, 1):
        parts.append(
            f"第{i}个场景，{scene['title_cn']}，{scene['title_en']}。时间范围{scene['time']}。请听场景完整英文："
        )
        parts.append(scene["speak"])
        if i < total:
            parts.append("好，进入下一个场景。")
    parts.append("下面是今日可练环节，请听完中文意图后尝试说出英文。")
    for i, (prompt, english) in enumerate(data["practice"]):
        parts.append(f"第{i+1}题：{prompt}。")
        parts.append(english)
    parts.append(
        "讲解完毕。建议回到网页查看完整逐句中英对照与表达提示，跟着朗读按钮反复练习。祝学习顺利！"
    )
    return "\n\n".join(p.strip() for p in parts if p.strip())


def split_text(text: str, max_len: int = MAX_CHUNK_LEN) -> list[str]:
    if len(text) <= max_len:
        return [text]
    chunks: list[str] = []
    current = ""
    for para in text.split("\n\n"):
        if len(para) > max_len:
            if current:
                chunks.append(current.strip())
                current = ""
            for i in range(0, len(para), max_len):
                chunks.append(para[i : i + max_len])
            continue
        candidate = f"{current}\n\n{para}".strip() if current else para
        if len(candidate) <= max_len:
            current = candidate
        else:
            if current:
                chunks.append(current.strip())
            current = para
    if current:
        chunks.append(current.strip())
    return chunks


async def _synthesize_chunk(text: str, output: Path, voice: str) -> None:
    import edge_tts

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(output))


def _concat_mp3(files: list[Path], output: Path) -> None:
    list_file = output.parent / f".concat_{output.stem}.txt"
    try:
        with open(list_file, "w", encoding="utf-8") as f:
            for p in files:
                f.write(f"file '{p.resolve()}'\n")
        subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
             "-c", "copy", str(output)],
            check=True, capture_output=True,
        )
    finally:
        if list_file.exists():
            list_file.unlink()


async def synthesize_speech(text: str, output_path: Path, voice: str) -> bool:
    chunks = split_text(text)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if len(chunks) == 1:
        await _synthesize_chunk(chunks[0], output_path, voice)
        return output_path.exists()
    temp_files: list[Path] = []
    try:
        for i, chunk in enumerate(chunks):
            tmp = output_path.parent / f".tmp_{output_path.stem}_{i}.mp3"
            await _synthesize_chunk(chunk, tmp, voice)
            temp_files.append(tmp)
        _concat_mp3(temp_files, output_path)
        return output_path.exists()
    finally:
        for f in temp_files:
            if f.exists():
                f.unlink()


def audio_dir(slug: str) -> Path:
    return DOCS / "audio" / slug


async def generate_scene_mp3(slug: str, scene: dict) -> bool:
    out = audio_dir(slug) / f"{scene['id']}.mp3"
    if out.exists():
        return True
    ok = await synthesize_speech(scene["speak"], out, EN_VOICE)
    if not ok:
        print(f"  ✗ FAIL scene {scene['id']}")
    return ok


async def generate_sentence_mp3(slug: str, scene_id: str, idx: int, text: str) -> bool:
    out = audio_dir(slug) / f"{scene_id}-{idx:02d}.mp3"
    if out.exists():
        return True
    return await synthesize_speech(text, out, EN_VOICE)


async def generate_practice_mp3(slug: str, idx: int, text: str) -> bool:
    out = audio_dir(slug) / f"practice-{idx}.mp3"
    if out.exists():
        return True
    return await synthesize_speech(text, out, EN_VOICE)


async def generate_narration(slug: str, data: dict) -> bool:
    script = build_narration_script(data)
    d = audio_dir(slug)
    d.mkdir(parents=True, exist_ok=True)
    out_mp3 = d / "narration.mp3"
    out_txt = d / "narration.txt"
    if out_mp3.exists():
        print("  (skip) narration.mp3")
    else:
        ok = await synthesize_speech(script, out_mp3, ZH_VOICE)
        if not ok:
            print("  ✗ FAIL narration.mp3")
            return False
        print("  ✓ narration.mp3")
    out_txt.write_text(script, encoding="utf-8")
    print(f"  ✓ narration.txt ({len(script)} 字)")
    return True


def build_html(data: dict) -> str:
    meta, scenes = data["meta"], data["scenes"]
    scene_imgs = data["scene_imgs"]
    slug = meta["slug"]
    img_dir = f"assets/{slug}"
    audio_base = f"audio/{slug}"

    hero = f"""<header class="hero">
    <div class="hero-inner">
      <div class="hero-flex">
        <img class="hero-cover" src="{img_dir}/{scene_imgs[0]}.jpg" alt="{meta['title']} 封面" loading="lazy">
        <div class="hero-text">
          <p class="eyebrow">Scene English · {meta.get('topic', '视频学习')}</p>
          <h1>{meta['title']}</h1>
          <p class="hero-en">{meta['title_en']}</p>
          <div class="hero-meta"><span class="chip">{meta['date']}</span><span class="chip">{meta['platform']}</span><span class="chip">{meta['duration']}</span><span class="chip">{meta['scenes']} 个场景</span><span class="chip">点下划线单词听发音</span><a class="source-link" href="{meta['source_url']}" target="_blank" rel="noopener">查看原视频 ↗</a><a class="source-link lang-switch" href="{slug}-图文实录.html" hreflang="zh" style="margin-left:12px;font-size:.8rem">中文图文实录版 ↗</a></div>
        </div>
      </div>
      <div class="toolbar"><label for="speech-rate">朗读速度</label><select id="speech-rate"><option value="0.85">慢速 0.85×</option><option value="1" selected>正常 1×</option><option value="1.15">快速 1.15×</option></select><button id="stop-speech" class="stop-btn" type="button">■ 停止朗读</button><span id="speech-status" class="speech-status" role="status" aria-live="polite"></span></div>
      <div class="narration-player"><p class="audio-label">🎧 语音讲解</p><button class="speak-btn" type="button" data-audio="{audio_base}/narration.mp3" aria-label="播放语音讲解"><span aria-hidden="true">▶</span><span>播放语音讲解</span></button></div>
    </div>
  </header>"""

    map_links = []
    for i, s in enumerate(scenes, 1):
        map_links.append(
            f'<a class="map-link" href="#{s["id"]}"><span class="map-id">S{i}</span>'
            f'<span><b>{s["title_cn"]}</b><small>{s["time"]} · {s["title_en"]}</small></span></a>'
        )
    sidebar = (
        '<aside class="sidebar" aria-label="场景地图"><div class="sidebar-box">'
        f'<h2>场景地图 · SCENE MAP</h2><nav class="map-nav">{"".join(map_links)}</nav></div></aside>'
    )

    cards = []
    for i, s in enumerate(scenes, 1):
        img_name = scene_imgs[i - 1] if i - 1 < len(scene_imgs) else scene_imgs[-1]
        sentences_html = []
        for j, (zh, en, note) in enumerate(s["sentences"], 1):
            sentences_html.append(
                f'<article class="sentence"><div class="sentence-no">{j:02d}</div>'
                '<div class="bilingual">'
                '<div class="lang-block zh-block"><span class="lang-tag">中文</span>'
                f'<p>{zh}</p></div>'
                '<div class="lang-block en-block"><div class="en-head"><span class="lang-tag">EN</span>'
                f'<button class="speak-btn compact" type="button" data-audio="{audio_base}/{s["id"]}-{j:02d}.mp3" aria-label="朗读本句">'
                '<span aria-hidden="true">▶</span><span>朗读本句</span></button></div>'
                f'<p class="english">{en}</p></div></div>'
                f'<p class="note"><span>表达提示</span>{note}</p></article>'
            )
        para_items = "".join(
            f'<li><p>{p}</p><div class="chunks">{c}</div></li>'
            for p, c in s["paraphrase"]
        )
        cards.append(
            f'<section class="scene-card" id="{s["id"]}" data-scene>'
            '<div class="scene-topline"><div>'
            f'<span class="scene-id">S{i}</span><span class="time">{s["time"]}</span></div>'
            f'<button class="speak-btn scene-speak" type="button" data-audio="{audio_base}/{s["id"]}.mp3" aria-label="朗读整个场景">'
            '<span aria-hidden="true">▶</span><span>朗读整个场景</span></button></div>'
            f'<img class="scene-frame" src="{img_dir}/{img_name}.jpg" alt="{s["title_cn"]} 场景截图" loading="lazy">'
            f'<h2>{s["title_cn"]}</h2>'
            f'<p class="scene-title-en">{s["title_en"]}</p>'
            f'<p class="context"><b>情境</b>{s["context"]}</p>'
            f'<div class="sentence-list">{"".join(sentences_html)}</div>'
            f'<details class="paraphrase"><summary>Paraphrase &amp; Chunks <span>{len(s["paraphrase"])} 组表达</span></summary>'
            f'<ol>{para_items}</ol></details>'
            "</section>"
        )

    practice_items = "".join(
        f'<article><p>{zh}</p><div class="practice-en">{en} '
        f'<button class="speak-btn icon-only" type="button" data-audio="{audio_base}/practice-{i}.mp3" aria-label="朗读练习句">'
        '<span aria-hidden="true">▶</span><span>朗读练习句</span></button></div></article>'
        for i, (zh, en) in enumerate(data["practice"])
    )
    practice_section = (
        '<section class="study-section" id="practice"><h2 class="section-heading">今日可练 <small>PRACTICE TODAY</small></h2>'
        f'<div class="study-grid">{practice_items}</div></section>'
    )

    pit_items = "".join(
        f'<article><div class="wrong">✕ {wrong}</div><div class="right">✓ {right}</div><p>{why}</p></article>'
        for wrong, right, why in data["pitfalls"]
    )
    pitfalls_section = (
        '<section class="study-section pitfalls" id="pitfalls"><h2 class="section-heading">避坑 <small>PITFALLS</small></h2>'
        f'<div class="study-grid">{pit_items}</div></section>'
    )

    shift_items = "".join(
        f'<article><span>{a}</span><b aria-hidden="true">→</b><strong>{b}</strong></article>'
        for a, b in data["shifts"]
    )
    shifts_section = (
        '<section class="study-section shifts" id="mindset"><h2 class="section-heading">认知转变 <small>MINDSET SHIFTS</small></h2>'
        f'<div class="study-grid">{shift_items}</div></section>'
    )

    footer = (
        f"<footer>{data.get('footer_notes', '')}"
        " · 场景/句子朗读使用 edge-tts 神经网络语音 · 单词发音使用浏览器 Web Speech API</footer>"
    )

    difficult_words = ", ".join(repr(w) for w in data["difficult_words"])

    js = f"""(() => {{
    let activeAudio = null;
    let activeBtn = null;
    const status = document.getElementById('speech-status');
    const stopBtn = document.getElementById('stop-speech');
    const rateSel = document.getElementById('speech-rate');
    const reset = () => {{ if (activeAudio) {{ activeAudio.pause(); activeAudio = null; }} activeBtn?.classList.remove('playing'); activeBtn = null; stopBtn.classList.remove('visible'); status.textContent = ''; }};
    const playAudio = (url, btn) => {{ reset(); const a = new Audio(url); a.playbackRate = Number(rateSel.value); activeAudio = a; activeBtn = btn; btn.classList.add('playing'); stopBtn.classList.add('visible'); status.textContent = btn.classList.contains('scene-speak') ? '正在朗读整个场景…' : btn.classList.contains('speak-btn') && btn.dataset.audio.includes('narration') ? '正在播放语音讲解…' : '正在朗读…'; a.onended = () => {{ if (activeAudio === a) reset(); }}; a.onerror = () => {{ status.textContent = '音频加载失败'; if (activeAudio === a) reset(); }}; a.play().catch(() => {{ status.textContent = '播放失败'; if (activeAudio === a) reset(); }}); }};
    document.addEventListener('click', e => {{ const btn = e.target.closest('[data-audio]'); if (!btn) return; e.preventDefault(); if (btn === activeBtn && activeAudio) {{ reset(); return; }} playAudio(btn.dataset.audio, btn); }});
    stopBtn.addEventListener('click', reset);
    const synth = window.speechSynthesis;
    const getEnglishVoice = () => {{ const v = synth.getVoices(); return v.find(x => /^en-(US|GB)/i.test(x.lang)) || v.find(x => /^en/i.test(x.lang)) || null; }};
    const difficultWords = new Set([{difficult_words}]);
    const shouldPronounce = w => {{ const n = w.toLowerCase().replace(/^[^a-z]+|[^a-z]+$/g,''); return n.replace(/[^a-z]/g,'').length >= 8 || difficultWords.has(n); }};
    const mark = root => {{ const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT); const ns = []; while (w.nextNode()) ns.push(w.currentNode); ns.forEach(n => {{ if (n.parentElement?.closest('button,script,style')) return; let m,l=0,ch=false; const fg = document.createDocumentFragment(); const re = /[A-Za-z]+(?:[-'’][A-Za-z]+)*/g; while ((m = re.exec(n.nodeValue))) {{ if (!shouldPronounce(m[0])) continue; ch=true; fg.append(n.nodeValue.slice(l,m.index)); const b=document.createElement('button');b.type='button';b.className='pronounce-word';b.dataset.speak=m[0];b.setAttribute('aria-label','朗读单词 '+m[0]);b.title='点击听 '+m[0]+' 发音';b.textContent=m[0];fg.append(b);l=m.index+m[0].length;}} if(!ch)return;fg.append(n.nodeValue.slice(l));n.replaceWith(fg);}}); }};
    document.querySelectorAll('.english,.scene-title-en,.paraphrase li p,.chunks,.practice-en,.wrong,.right').forEach(mark);
    document.addEventListener('click', e => {{ const wb = e.target.closest('.pronounce-word'); if (!wb) return; e.preventDefault(); if (!synth) return; synth.cancel(); if (activeAudio) {{ activeAudio.pause(); activeAudio = null; }} activeBtn?.classList.remove('playing'); activeBtn=wb; wb.classList.add('playing'); const u=new SpeechSynthesisUtterance(wb.dataset.speak);u.lang='en-US';u.rate=0.88;const v=getEnglishVoice();if(v)u.voice=v;u.onend=()=>{{activeBtn?.classList.remove('playing');activeBtn=null;}};u.onerror=()=>{{activeBtn?.classList.remove('playing');activeBtn=null;}};synth.speak(u); }});
  }})();"""

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="{meta['title']}视频场景英译学习卡" />
  <title>{meta['title']}｜场景英译</title>
  <style>{CSS}</style>
</head>
<body>
  {hero}
  <main class="page">
    {sidebar}
    <div class="content">
      {"".join(cards)}
      {practice_section}
      {pitfalls_section}
      {shifts_section}
      {footer}
    </div>
  </main>
  <script>{js}</script>
</body>
</html>"""
    return html


CSS = """:root {
  --teal-950:#073f42; --teal-800:#0d686c; --teal-700:#0f7c80; --teal-600:#14919b;
  --mint-100:#dff4ec; --mint-50:#f0faf6; --ink:#183536; --muted:#607879;
  --line:#d7e8e2; --paper:#fff; --amber:#a85d08; --shadow:0 12px 32px rgba(7,63,66,.08);
}
* { box-sizing:border-box; }
html { scroll-behavior:smooth; scroll-padding-top:24px; }
body { margin:0; color:var(--ink); background:#edf7f2; font-family:Inter,"PingFang SC","Noto Sans SC","Microsoft YaHei",system-ui,sans-serif; line-height:1.65; }
button, select { font:inherit; }
a { color:inherit; }
.hero { color:#fff; background:radial-gradient(circle at 85% 10%,rgba(129,230,196,.24),transparent 30%),linear-gradient(125deg,#073f42,#0d7377 56%,#14919b); }
.hero-inner { width:min(1440px,100%); margin:auto; padding:48px clamp(20px,5vw,72px) 42px; }
.hero-flex { display:flex; gap:clamp(18px,3vw,40px); align-items:flex-start; }
.hero-cover { width:min(240px,42vw); height:auto; max-height:320px; object-fit:contain; object-position:center; border-radius:16px; border:1px solid rgba(255,255,255,.28); box-shadow:0 18px 44px rgba(0,0,0,.32); flex-shrink:0; }
.hero-text { min-width:0; flex:1; }
.eyebrow { margin:0 0 12px; font-size:.78rem; font-weight:800; letter-spacing:.14em; text-transform:uppercase; opacity:.8; }
h1 { max-width:1020px; margin:0; font-size:clamp(1.8rem,3.8vw,3.2rem); line-height:1.13; letter-spacing:-.04em; }
.hero-en { margin:12px 0 24px; font-size:clamp(1rem,2vw,1.3rem); opacity:.82; }
.hero-meta { display:flex; flex-wrap:wrap; gap:9px; align-items:center; }
.chip { border:1px solid rgba(255,255,255,.28); border-radius:99px; padding:5px 11px; font-size:.82rem; background:rgba(255,255,255,.08); }
.source-link { font-weight:750; text-decoration:none; border-bottom:1px solid rgba(255,255,255,.5); }
.lang-switch { margin-left:12px; font-size:.8rem; font-weight:700; }
.toolbar { display:flex; flex-wrap:wrap; gap:10px; align-items:center; margin-top:24px; }
.toolbar label { font-size:.82rem; opacity:.82; }
.toolbar select { color:#fff; background:#0a5d61; border:1px solid rgba(255,255,255,.3); border-radius:8px; padding:7px 9px; }
.stop-btn { display:none; color:#fff; background:#8c3b2a; border:0; border-radius:8px; padding:8px 12px; cursor:pointer; }
.stop-btn.visible { display:inline-flex; }
.speech-status { min-height:1.4em; font-size:.82rem; opacity:.88; }
.narration-player { margin-top:18px; padding:16px 18px; background:rgba(255,255,255,.1); border-radius:12px; border:1px solid rgba(255,255,255,.15); }
.audio-label { color:rgba(255,255,255,.88); font-size:.82rem; font-weight:700; margin:0 0 8px; }
.page { width:min(1440px,100%); margin:auto; padding:28px clamp(16px,3vw,44px) 64px; display:grid; grid-template-columns:minmax(230px,280px) minmax(0,1fr); gap:30px; align-items:start; }
.sidebar { position:sticky; top:20px; min-width:0; }
.sidebar-box { background:rgba(255,255,255,.8); border:1px solid var(--line); border-radius:16px; padding:17px; box-shadow:var(--shadow); backdrop-filter:blur(12px); }
.sidebar h2 { margin:0 0 13px; font-size:.9rem; letter-spacing:.08em; color:var(--teal-800); }
.map-link { display:grid; grid-template-columns:34px minmax(0,1fr); gap:9px; padding:10px 6px; text-decoration:none; border-top:1px solid var(--line); }
.map-link:hover b { color:var(--teal-700); }
.map-id { width:30px; height:30px; display:grid; place-items:center; border-radius:9px; color:#fff; background:var(--teal-700); font-size:.72rem; font-weight:800; }
.map-link b { display:block; font-size:.78rem; line-height:1.4; }
.map-link small { display:block; color:var(--muted); font-size:.67rem; line-height:1.4; margin-top:2px; overflow-wrap:anywhere; }
.content { min-width:0; }
.scene-card { background:var(--paper); border:1px solid var(--line); border-radius:20px; padding:clamp(20px,3vw,34px); margin-bottom:24px; box-shadow:var(--shadow); overflow:hidden; }
.scene-frame { display:block; width:100%; max-height:480px; object-fit:contain; object-position:center; background:rgba(7,63,66,.04); border-radius:14px; margin:16px 0 4px; border:1px solid var(--line); box-shadow:0 10px 28px rgba(7,63,66,.1); }
.scene-topline { display:flex; justify-content:space-between; gap:16px; align-items:center; }
.scene-id { display:inline-grid; place-items:center; min-width:42px; height:30px; padding:0 10px; color:#fff; background:var(--teal-700); border-radius:8px; font-size:.78rem; font-weight:850; }
.time { margin-left:10px; color:var(--muted); font-size:.82rem; font-variant-numeric:tabular-nums; }
.scene-card h2 { margin:18px 0 2px; font-size:clamp(1.35rem,2.4vw,2rem); line-height:1.25; color:var(--teal-950); }
.scene-title-en { margin:0 0 18px; color:var(--teal-600); font-weight:700; font-size:.98rem; }
.context { margin:0 0 20px; padding:12px 15px; color:#496566; background:var(--mint-50); border-left:3px solid var(--teal-600); border-radius:0 10px 10px 0; font-size:.88rem; }
.context b { margin-right:10px; color:var(--teal-800); }
.sentence-list { display:grid; gap:12px; }
.sentence { position:relative; display:grid; grid-template-columns:38px minmax(0,1fr); gap:12px; padding:16px; border:1px solid #e2ece8; border-radius:14px; background:#fcfefd; min-width:0; }
.sentence-no { color:var(--teal-600); font-size:.76rem; font-weight:850; font-variant-numeric:tabular-nums; padding-top:4px; }
.bilingual { min-width:0; display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1fr); gap:clamp(14px,2vw,28px); }
.lang-block { min-width:0; }
.lang-block p { margin:5px 0 0; overflow-wrap:anywhere; }
.en-block { padding-left:clamp(14px,2vw,28px); border-left:1px solid var(--line); }
.en-block p { color:#0b5c60; font-weight:650; }
.lang-tag { display:inline-block; color:var(--muted); font-size:.66rem; font-weight:850; letter-spacing:.12em; }
.en-head { display:flex; justify-content:space-between; gap:10px; align-items:center; min-height:30px; }
.note { grid-column:2; margin:1px 0 0; color:#708182; font-size:.78rem; }
.note span { margin-right:7px; color:var(--amber); font-weight:750; }
.speak-btn { display:inline-flex; align-items:center; gap:7px; border:1px solid #b8d9d1; border-radius:9px; padding:7px 11px; color:var(--teal-800); background:#f5fbf8; cursor:pointer; white-space:nowrap; font-size:.78rem; font-weight:750; transition:.15s ease; }
.speak-btn:hover { color:#fff; background:var(--teal-700); border-color:var(--teal-700); transform:translateY(-1px); }
.speak-btn.playing { color:#fff; background:var(--teal-700); border-color:var(--teal-700); }
.speak-btn.compact { padding:4px 8px; font-size:.7rem; }
.speak-btn.icon-only { padding:3px 7px; margin-left:6px; }
.speak-btn.icon-only span:last-child { display:none; }
.pronounce-word { display:inline; margin:0; padding:0 2px; color:inherit; background:rgba(20,145,155,.08); border:0; border-bottom:1px dashed var(--teal-600); border-radius:3px; font:inherit; font-weight:inherit; line-height:inherit; cursor:pointer; }
.pronounce-word:hover, .pronounce-word:focus { color:var(--teal-950); background:#cceee4; border-bottom-style:solid; outline:3px solid rgba(20,145,155,.42); outline-offset:2px; }
.pronounce-word.playing { color:#fff; background:var(--teal-700); border-bottom-color:var(--teal-700); }
.paraphrase { margin-top:18px; border-top:1px solid var(--line); }
.paraphrase summary { padding:16px 0 3px; color:var(--teal-800); cursor:pointer; font-weight:800; }
.paraphrase summary span { color:var(--muted); font-size:.75rem; font-weight:500; margin-left:8px; }
.paraphrase ol { margin:12px 0 0; padding-left:22px; }
.paraphrase li { padding:7px 0 9px 5px; }
.paraphrase li p { margin:0; font-size:.9rem; font-weight:650; }
.chunks { margin-top:4px; color:var(--teal-700); font-size:.78rem; }
.study-section { margin:38px 0 0; }
.section-heading { display:flex; align-items:baseline; gap:10px; margin:0 0 15px; color:var(--teal-950); font-size:1.35rem; }
.section-heading small { color:var(--teal-600); font-size:.78rem; letter-spacing:.05em; }
.study-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:14px; }
.study-grid article { padding:17px; background:#fff; border:1px solid var(--line); border-radius:14px; box-shadow:0 6px 18px rgba(7,63,66,.05); min-width:0; }
.study-grid p { margin:0; }
.practice-en { margin-top:9px; color:var(--teal-700); font-weight:650; overflow-wrap:anywhere; }
.wrong { color:#a24831; text-decoration:line-through; overflow-wrap:anywhere; }
.right { color:var(--teal-700); font-weight:750; margin:5px 0; overflow-wrap:anywhere; }
.pitfalls p { color:var(--muted); font-size:.82rem; }
.shifts article { display:grid; grid-template-columns:minmax(0,1fr) auto minmax(0,1.5fr); gap:12px; align-items:center; }
.shifts b { color:var(--teal-600); font-size:1.2rem; }
.shifts strong { color:var(--teal-800); }
footer { margin-top:38px; color:var(--muted); font-size:.78rem; text-align:center; }
@media (max-width:900px) { .page { grid-template-columns:1fr; } .sidebar { position:static; } .sidebar-box { overflow-x:auto; padding:12px; } .sidebar h2 { padding-left:5px; } .map-nav { display:flex; width:max-content; gap:8px; } .map-link { width:220px; border:1px solid var(--line); border-radius:10px; padding:8px; } .bilingual { grid-template-columns:1fr; } .en-block { padding:12px 0 0; border-left:0; border-top:1px dashed var(--line); } }
@media (max-width:620px) { .hero-inner { padding-top:32px; } .hero-flex { flex-direction:column; align-items:center; } .hero-cover { width:100%; max-width:360px; } .hero-text { text-align:center; } .page { padding-inline:10px; gap:18px; } .scene-card { border-radius:14px; padding:17px 13px; } .scene-topline { align-items:flex-start; } .scene-speak span:last-child { display:none; } .sentence { grid-template-columns:26px minmax(0,1fr); padding:13px 10px; gap:6px; } .note { grid-column:2; } .study-grid { grid-template-columns:1fr; } .shifts article { grid-template-columns:1fr; gap:5px; } .shifts b { transform:rotate(90deg); justify-self:start; } }
@media (prefers-reduced-motion:reduce) { html { scroll-behavior:auto; } .speak-btn { transition:none; } }"""


def generate_manifest(slug: str, data: dict) -> dict:
    return {
        "slug": slug,
        "scenes": len(data["scenes"]),
        "sentences": sum(len(s["sentences"]) for s in data["scenes"]),
        "scene_audio": [f"audio/{slug}/{s['id']}.mp3" for s in data["scenes"]],
        "sentence_audio": {
            f"{s['id']}-{i+1:02d}": f"audio/{slug}/{s['id']}-{i+1:02d}.mp3"
            for s in data["scenes"] for i in range(len(s["sentences"]))
        },
        "practice_audio": [f"audio/{slug}/practice-{i}.mp3" for i in range(len(data["practice"]))],
        "narration": f"audio/{slug}/narration.mp3",
    }


async def run_all(slug: str, data: dict) -> None:
    total_sents = sum(len(s["sentences"]) for s in data["scenes"])
    print(f"📢 {slug}: 生成英文音频：{len(data['scenes'])} 场景 + {total_sents} 句 + {len(data['practice'])} 练习")

    scene_results = await asyncio.gather(
        *(generate_scene_mp3(slug, s) for s in data["scenes"])
    )
    sent_results = await asyncio.gather(*[
        generate_sentence_mp3(slug, s["id"], i + 1, text)
        for s in data["scenes"] for i, (_, text, _) in enumerate(s["sentences"])
    ])
    practice_results = await asyncio.gather(*[
        generate_practice_mp3(slug, i, text) for i, (_, text) in enumerate(data["practice"])
    ])
    narration_ok = await generate_narration(slug, data)

    print(f"  {slug}: 场景 {sum(scene_results)}/{len(data['scenes'])} | 逐句 {sum(sent_results)}/{total_sents} | 练习 {sum(practice_results)}/{len(data['practice'])} | 旁白 {'✓' if narration_ok else '✗'}")
    manifest = generate_manifest(slug, data)
    (audio_dir(slug) / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    from argparse import ArgumentParser

    parser = ArgumentParser(description="场景英译学习卡生成器")
    parser.add_argument("--slug", type=str, help="视频 slug")
    parser.add_argument("--audio-only", action="store_true", help="仅生成音频")
    parser.add_argument("--html-only", action="store_true", help="仅生成 HTML")
    parser.add_argument("--all", action="store_true", help="处理全部 scene-data 条目")
    args = parser.parse_args()

    if args.all:
        slugs = sorted(p.stem for p in DATA_DIR.glob("*.json"))
    elif args.slug:
        slugs = [args.slug]
    else:
        parser.error("需要 --slug 或 --all")

    for slug in slugs:
        data = load_slug(slug)
        if not args.html_only:
            asyncio.run(run_all(slug, data))
        if not args.audio_only:
            html = build_html(data)
            out = DOCS / f"{slug}-场景英译.html"
            out.write_text(html, encoding="utf-8")
            print(f"  ✓ HTML: {out.name} ({len(html)} bytes)")
        print(f"✓ 完成 {slug}")


if __name__ == "__main__":
    main()
