#!/usr/bin/env python3
"""给所有图文实录 HTML 的 figcaption 增加英文翻译 + 朗读按钮 + 音频。

- 读取 translations.json（中文 caption → 英文翻译）
- 扫描 docs/*-图文实录.html
- 对每个 figcaption 解析中文，查英文翻译，重写为中英对照结构：
    <figcaption class="cap-bilingual">
      <div class="cap-zh">[00:00] 原理说明相关画面。</div>
      <div class="cap-en"><button class="cap-speak" data-audio="audio/xxxx.mp3">🔊</button><span>English...</span></div>
      <audio class="cap-audio" src="audio/xxxx.mp3" preload="none"></audio>
    </figcaption>
- 注入全局 CSS 与 JS（含哨兵标记，幂等）
"""
from __future__ import annotations

import hashlib
import html as html_mod
import json
import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
TRANSLATIONS = json.loads(
    (Path(__file__).resolve().parent.parent / "translations.json").read_text(encoding="utf-8")
)

TIME_RE = re.compile(r"\[(\d{1,2}:\d{2}(?::\d{2})?)\]")
CAP_RE = re.compile(r"<figcaption>(.*?)</figcaption>", re.S)
FIGURE_RE = re.compile(r"<figure>.*?</figure>", re.S)

CSS_BLOCK = """<style id="cap-en-style">
.cap-bilingual{padding:14px 18px}.cap-bilingual .cap-zh{color:#57534e;font-size:14px;line-height:1.7}.cap-bilingual .cap-zh .time-badge{font-weight:700;color:#b45309;margin-right:6px}.cap-bilingual .cap-en{display:flex;align-items:flex-start;gap:10px;margin-top:8px;padding-top:8px;border-top:1px dashed #e7e5e4;color:#0f766e;font-size:14px;line-height:1.7}.cap-speak{flex:none;width:34px;height:34px;border:none;border-radius:50%;background:#0f766e;color:#fff;font-size:14px;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;transition:transform .15s,background .2s}.cap-speak:hover{background:#115e59;transform:scale(1.08)}.cap-speak.playing{background:#b45309;animation:capPulse 1s infinite}@keyframes capPulse{0%,100%{opacity:1}50%{opacity:.55}}
</style>
"""

JS_BLOCK = """<script id="cap-en-script">
(function(){
  function stopOthers(except){
    document.querySelectorAll('.cap-audio').forEach(function(a){
      if(a!==except){a.pause();a.currentTime=0;}
    });
    document.querySelectorAll('.cap-speak.playing').forEach(function(b){
      if(!except||b.dataset.audio!==except.dataset.audio){b.classList.remove('playing');}
    });
  }
  document.addEventListener('click',function(e){
    var btn=e.target.closest('.cap-speak');
    if(!btn)return;
    var cap=btn.closest('.cap-bilingual');
    if(!cap)return;
    var au=cap.querySelector('.cap-audio');
    if(!au)return;
    if(au.paused){
      stopOthers(au);
      btn.classList.add('playing');
      au.play();
    }else{
      au.pause();au.currentTime=0;btn.classList.remove('playing');
    }
  });
  ['pause','ended'].forEach(function(ev){
    document.addEventListener(ev,function(e){
      if(e.target.classList&&e.target.classList.contains('cap-audio')){
        var cap=e.target.closest('.cap-bilingual');
        if(cap){var b=cap.querySelector('.cap-speak');if(b)b.classList.remove('playing');}
      }
    },true);
  });
})();
</script>
"""


def strip_html(s: str) -> str:
    return (
        re.sub(r"<[^>]+>", "", s)
        .replace("&quot;", '"')
        .replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .strip()
    )


def extract_zh(cap_html: str) -> str:
    text = strip_html(cap_html)
    time_m = TIME_RE.search(text)
    zh = text[time_m.end():].strip(" ：: ") if time_m else text
    return zh.strip()


def audio_url(zh: str) -> str:
    h = hashlib.md5(zh.encode("utf-8")).hexdigest()[:12]
    return f"audio/{h}.mp3"


def rewrite_figcaption(fig: str) -> tuple[str, int]:
    """返回 (重写后的 figure, 处理数)。未命中翻译则保持原样。"""
    cap_m = CAP_RE.search(fig)
    if not cap_m:
        return fig, 0
    cap_html = cap_m.group(1)
    if "cap-bilingual" in cap_html:
        return fig, 0
    zh = extract_zh(cap_html)
    en = TRANSLATIONS.get(zh, "")
    if not en:
        return fig, 0
    src = audio_url(zh)
    new_cap = (
        '<figcaption class="cap-bilingual">\n'
        f'<div class="cap-zh">{cap_html}</div>\n'
        f'<div class="cap-en"><button class="cap-speak" data-audio="{src}" type="button" aria-label="Play English audio">🔊</button>'
        f"<span>{html_mod.escape(en)}</span></div>\n"
        f'<audio class="cap-audio" src="{src}" preload="none"></audio>\n'
        "</figcaption>"
    )
    new_fig = fig[: cap_m.start()] + new_cap + fig[cap_m.end():]
    return new_fig, 1


def process_file(path: Path) -> tuple[int, int]:
    html = path.read_text(encoding="utf-8")
    count = 0

    def repl(m: re.Match) -> str:
        nonlocal count
        new_fig, n = rewrite_figcaption(m.group(0))
        count += n
        return new_fig

    html2 = FIGURE_RE.sub(repl, html)
    all_n = len(FIGURE_RE.findall(html))

    if "id=\"cap-en-style\"" not in html2:
        html2 = html2.replace("</head>", CSS_BLOCK + "</head>", 1)
    if "id=\"cap-en-script\"" not in html2:
        html2 = html2.replace("</body>", JS_BLOCK + "</body>", 1)

    if html2 != html:
        path.write_text(html2, encoding="utf-8")
    return count, all_n


def main() -> None:
    files = sorted(DOCS.glob("*-图文实录.html"))
    total_done = total_all = 0
    for f in files:
        done, all_n = process_file(f)
        total_done += done
        total_all += all_n
        if done:
            print(f"  {f.name}: {done}/{all_n}")
    print(f"\n完成: {total_done}/{total_all} captions 增强")
    sys.exit(0)


if __name__ == "__main__":
    main()
