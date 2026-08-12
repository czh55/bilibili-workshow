#!/usr/bin/env python3
"""b45：为 9 篇新视频追加 index.json 条目，并在图文实录加入 English Version 链接。"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
INDEX = DOCS / "index.json"

ENTRIES = [
    {
        "slug": "mask-tutorial",
        "title": "我今天必须教会你，蒙版！",
        "date": "2026-08-12",
        "duration": "1分51秒",
        "tags": ["摄影", "修图", "剪辑", "蒙版"],
        "url": "http://xhslink.cn/o/2NnOyOfdlo3",
        "summary": "核心判断：蒙版之所以是修图与剪辑的核心功能，是因为它把「修改」与「原图」解耦——白加黑减控制显示与隐藏，从换天、局部提亮到视频过渡，一个原理贯穿照片、调色、视频三种场景。",
        "shots": 10, "segs": 72, "height": 7304,
    },
    {
        "slug": "camera-movement-apple",
        "title": "什么是运镜？我用一颗苹果告诉你",
        "date": "2026-08-12",
        "duration": "1分07秒",
        "tags": ["摄影", "运镜", "镜头语言", "短视频"],
        "url": "http://xhslink.cn/o/8nlFEp6PEU9",
        "summary": "核心判断：运镜不是耍帅的炫技，而是有明确叙事功能的镜头语言——摇镜头交代关系、下降镜头开场、上升镜头结尾、推镜头放大情绪、拉镜头转向环境。一颗苹果的冒险故事，让五种运镜各就各位。",
        "shots": 8, "segs": 45, "height": 7185,
    },
    {
        "slug": "flower-shooting",
        "title": "这么拍花，包出片的～",
        "date": "2026-08-12",
        "duration": "1分43秒",
        "tags": ["摄影", "拍花", "道具", "氛围感"],
        "url": "http://xhslink.cn/o/61osLfkUpoT",
        "summary": "核心判断：拍花出片的关键不是器材，而是给静态花朵制造「动态氛围」——喷壶造水珠、塑料板做朦胧、卡纸压杂乱、碎花瓣玩创意、纱巾出梦幻，五个随手可得的道具构成一套可复现的出片流程。",
        "shots": 10, "segs": 33, "height": 7329,
    },
    {
        "slug": "travel-shoot",
        "title": "假期旅游，就这么拍～",
        "date": "2026-08-12",
        "duration": "2分09秒",
        "tags": ["摄影", "旅游", "人像", "构图"],
        "url": "http://xhslink.cn/o/520YpUSJNKL",
        "summary": "核心判断：假期人多也能高效出片，靠四件事——手机端平打好构图基础、退后五步用长焦避开人群、同一姿势不超过三秒保持生动、转瞬即逝的风景用横屏视频抓拍再挑帧拼图。技巧之外，旅程本身比照片更值得珍视。",
        "shots": 10, "segs": 83, "height": 7415,
    },
    {
        "slug": "harmony-shooting",
        "title": "这样拍，更和谐～",
        "date": "2026-08-12",
        "duration": "1分43秒",
        "tags": ["摄影", "审美", "构图", "思想"],
        "url": "http://xhslink.cn/o/2k1fCkClN7q",
        "summary": "核心判断：审美不是天赋，而是「找重点」的能力——人天生会看最突出的事物（黄豆），相机却会把一切全拍进去；所以拍照的第一步，是帮相机找到那颗黄豆。从拍照延伸到穿搭、化妆、海报设计，最后落脚到基本功。",
        "shots": 11, "segs": 52, "height": 7242,
    },
    {
        "slug": "light-and-shadow",
        "title": "找光是为了看清楚，那影呢？",
        "date": "2026-08-12",
        "duration": "1分33秒",
        "tags": ["摄影", "灯光", "光影", "氛围"],
        "url": "http://xhslink.cn/o/cOwg6z2hk0",
        "summary": "核心判断：照片显乱往往不是杂物多，而是光太匀导致没有主次——直射大灯均匀照亮一切、也消灭所有影子；换成氛围小灯，让影子吞没多余细节，有光的地方才格外突出。同一原理从布光延伸到修图，可以拯救手机里的废片。",
        "shots": 10, "segs": 34, "height": 7217,
    },
    {
        "slug": "curve-color-grade",
        "title": "小小曲线调色，拿捏啦🫴！！",
        "date": "2026-08-12",
        "duration": "1分44秒",
        "tags": ["摄影", "调色", "曲线", "后期"],
        "url": "http://xhslink.cn/o/8KywZvpaNFR",
        "summary": "核心判断：曲线调色并不玄，它建立在直方图之上——左暗右亮读明暗，打点拉曲线提亮与加对比，四根曲线（亮度+红绿蓝）分工明确，再用相反色校准偏色。一张直方图，就是读懂曲线全部用法的钥匙。",
        "shots": 10, "segs": 69, "height": 7443,
    },
    {
        "slug": "color-grade-basics",
        "title": "小小调色，拿捏啦🫴！！",
        "date": "2026-08-12",
        "duration": "1分47秒",
        "tags": ["摄影", "调色", "三原色", "原理"],
        "url": "http://xhslink.cn/o/7K4F5QCUxGV",
        "summary": "核心判断：调色反复翻车的根源是「颜色不够就加色」的直觉错了——光学三原色两两叠加出三对对立色，对立色混合反而变白；照片发灰不显色是混进了对立色。所以调色做减法：减去对立色，目标颜色自然透出；按「近少远多」控制增减量，就能把世界调成任意颜色。",
        "shots": 11, "segs": 64, "height": 7550,
    },
    {
        "slug": "photo-clarity",
        "title": "照片通透是由什么决定的呢？通透只需两点",
        "date": "2026-08-12",
        "duration": "36秒",
        "tags": ["摄影", "调色", "通透", "后期"],
        "url": "http://xhslink.cn/o/3bZGd47sE3f",
        "summary": "核心判断：36 秒讲透「照片通透」的本质——两点：一去灰，二颜色干净。去灰靠直方图两端：缺少暗部亮部、信息堆在灰部就不通透，压暗暗部增亮亮部即可；画面显脏则查暗部与中性色：可选颜色里调中性色，脏灰就变干净。",
        "shots": 6, "segs": 29, "height": 6605,
    },
]


def main() -> None:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    existing = {
        e.get("outputs", {}).get("html", ""): e
        for e in data
        if isinstance(e.get("outputs"), dict)
    }

    added = 0
    for e in ENTRIES:
        slug = e["slug"]
        html_name = f"{slug}-图文实录.html"
        if html_name in existing:
            print(f"  ~ {slug} 已存在，跳过")
            continue
        entry = {
            "date": e["date"],
            "title": e["title"],
            "summary": e["summary"],
            "tags": e["tags"],
            "platform": "xiaohongshu",
            "url": e["url"],
            "duration": e["duration"],
            "outputs": {
                "html": html_name,
                "svg": f"{slug}-理性分析.svg",
                "html_en": f"{slug}-场景英译.html",
                "html_en_type": "scene-english",
            },
            "screenshot_count": e["shots"],
            "transcript_segments": e["segs"],
            "svg_height": e["height"],
        }
        data.append(entry)
        added += 1
        print(f"  ✓ 新增 {slug}")

    json.dump(data, open(INDEX, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"新增 {added} 条，index.json 共 {len(data)} 条")

    # 加入 English Version 链接
    for e in ENTRIES:
        slug = e["slug"]
        zh_file = DOCS / f"{slug}-图文实录.html"
        en_file = f"{slug}-场景英译.html"
        if not zh_file.exists():
            print(f"  ✗ 缺中文页 {zh_file.name}")
            continue
        html = zh_file.read_text(encoding="utf-8")
        if f'href="{en_file}"' in html:
            print(f"  ~ {slug}: 链接已存在")
            continue
        if "lang-switch" not in html:
            link = f'\n<a class="source-link lang-switch" href="{en_file}" hreflang="en">English Version</a>'
            html = re.sub(r"</header>", link + "</header>", html, count=1)
            zh_file.write_text(html, encoding="utf-8")
            print(f"  ✓ {slug}: 加入 English Version 链接")
        else:
            html = re.sub(
                r'href="[^"]*场景英译\.html"', f'href="{en_file}"', html, count=1
            )
            zh_file.write_text(html, encoding="utf-8")
            print(f"  ~ {slug}: 更新已有链接")

    print("完成")


if __name__ == "__main__":
    main()
