#!/usr/bin/env python3
"""为 b42 的 15 篇新视频创建 index.json 条目并加入 English Version 链接。"""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
INDEX = DOCS / "index.json"

ENTRIES = [
 {"slug": "white-balance-offset", "title": "终于有人把白平衡偏移说清楚了！", "duration": "45分钟", "date": "2026-08-09",
  "summary": "45分钟相机白平衡系统课：从AWB自动白平衡到色温定义、光色温与相机色温的差值逻辑（相机色温大于光线色温偏暖、小于偏冷）、白平衡把白色还原成白色、色调偏移决定画面氛围，讲清原片直出的色彩控制秘密。",
  "tags": ["白平衡", "色温", "相机设置", "摄影教学", "小红书"],
  "url": "http://xhslink.cn/o/8bnTzqVAMvT", "shots": 8, "segs": 1361, "height": 2520},
 {"slug": "guide-pose-model", "title": "如何引导摆姿摆姿呢？一个视频教会你。", "duration": "43分钟", "date": "2026-08-09",
  "summary": "43分钟人像美姿系统课：从站姿不稳纠正、摆姿引导话术、手部美字逻辑配竖构图，到蹲姿脚法、靠姿第四脚、道具互动与抓拍，把抽象美姿拆成可执行口令。",
  "tags": ["人像摄影", "摆姿", "美姿教学", "模特引导", "小红书"],
  "url": "http://xhslink.cn/o/4J6bjUXtIsl", "shots": 6, "segs": 1398, "height": 2480},
 {"slug": "dance-move-tutorial", "title": "这套动作教程来啦！", "duration": "23秒", "date": "2026-08-09",
  "summary": "23秒舞蹈动作快教学：从起式手位、抛头发、扶墙甩手抬腿转到侧身抬腿转，8个动作按固定顺序衔接，每个动作附口头口令方便跟练。",
  "tags": ["舞蹈", "动作教学", "跟练", "小红书"],
  "url": "http://xhslink.cn/o/1zBETKHZTC6", "shots": 6, "segs": 10, "height": 2240},
 {"slug": "lingdong-move-tutorial", "title": "灵动小师妹动作教学来啦！", "duration": "43秒", "date": "2026-08-09",
  "summary": "43秒灵动舞蹈教学：以「你以为的vs灵动版」对比拆解8组动作，转圈手伸出去斜肩歪头笑、遮太阳转身祈福迂回、提裙子侧身顶胯斜肩、坐姿重心前倾等。",
  "tags": ["舞蹈", "灵动", "动作教学", "小师妹", "小红书"],
  "url": "http://xhslink.cn/o/kpR88JaAih", "shots": 7, "segs": 23, "height": 2280},
 {"slug": "yaqi-lighting-trick", "title": "1分钟get雅琪同款打光秘籍", "duration": "1分32秒", "date": "2026-08-09",
  "summary": "92秒视频打光三件套：面光（双主光+下巴反光板）打立体消法令纹泪沟、背景光暖色打氛围、发丝光打精致，冷光显白暖光显温柔。",
  "tags": ["打光", "视频教程", "面光", "氛围感", "小红书"],
  "url": "http://xhslink.cn/o/24f7rAJOsDK", "shots": 6, "segs": 47, "height": 2520},
 {"slug": "outdoor-light-control", "title": "哪怕是在户外，也要学会控光哦。", "duration": "3分04秒", "date": "2026-08-09",
  "summary": "户外柔光四法：阴凉处避直射、背光+反光板、柔光屏、树影下补灯；白天补光要100W级，RGB全彩灯可还原电影场景。",
  "tags": ["打光", "户外", "vlog", "补光灯", "柔光", "小红书"],
  "url": "http://xhslink.cn/o/2m3URy7Jyox", "shots": 7, "segs": 84, "height": 2880},
 {"slug": "light-distance-guide", "title": "灯离人的最佳距离？一个视频给你答案", "duration": "1分24秒", "date": "2026-08-09",
  "summary": "八角柔光箱1米2米3米距离对比实验：1米光线充足柔和背景暗、2米扩散照亮背景、3米光变硬阴影锐利；实战推荐1.2-1.8米兼顾品质与可控。",
  "tags": ["闪光灯", "布光", "人像摄影", "柔光箱", "小红书"],
  "url": "http://xhslink.cn/o/2c438JwDNNG", "shots": 5, "segs": 52, "height": 2480},
 {"slug": "restaurant-toplight-fix", "title": "一学就会的餐厅顶光爆改氛围光拍照", "duration": "47秒", "date": "2026-08-09",
  "summary": "餐厅顶光三招：向光侧头发放前面接光、盘子当反光板补脸光、紫色图片调亮屏幕当氛围灯，低成本把灾难顶光变成氛围感神器。",
  "tags": ["拍照技巧", "顶光", "氛围感", "餐厅", "小红书"],
  "url": "http://xhslink.cn/o/7QAxf2iYJP6", "shots": 5, "segs": 44, "height": 2200},
 {"slug": "home-lighting-gap", "title": "手机在家拍出博主感：¥0→¥1000打光差距多大？", "duration": "2分00秒", "date": "2026-08-09",
  "summary": "手机拍视频灯光四档预算：¥0关顶灯开窗柔光、¥68反光板补阴影、¥500面光灯+氛围灯、¥1000双口袋灯打立体与发丝，逐级叠加出专业效果。",
  "tags": ["手机摄影", "打光", "省钱", "布光方案", "小红书"],
  "url": "http://xhslink.cn/o/2H7qD1cvv1c", "shots": 5, "segs": 56, "height": 2800},
 {"slug": "sofa-portrait", "title": "沙发人像怎么拍？一条视频教会你", "duration": "34秒", "date": "2026-08-09",
  "summary": "34秒沙发人像系列第六个动作：坐姿剪刀腿手前伸，双腿交叉成剪刀状、手向前自然延伸，姿态舒展显腿长。",
  "tags": ["人像摄影", "沙发人像", "拍照姿势", "小红书"],
  "url": "http://xhslink.cn/o/7LTACoUc8e3", "shots": 5, "segs": 4, "height": 1840},
 {"slug": "petite-longleg-poses", "title": "小个子秒变大长腿拍照姿势", "duration": "29秒", "date": "2026-08-09",
  "summary": "小个子显高五式：三脚前伸松手伸腰、后插腰提包单抬腿、侧身向后走背头看镜头、侧身抬腿伸腰提鞋跟、发包往前走抓拍，用延伸与动感拉长视觉。",
  "tags": ["拍照姿势", "显高", "小个子", "全身照", "小红书"],
  "url": "http://xhslink.cn/o/APxuTRL0nik", "shots": 5, "segs": 8, "height": 2840},
 {"slug": "summer-skirt-slim", "title": "夏天穿短裙这样拍超级显瘦！", "duration": "52秒", "date": "2026-08-09",
  "summary": "短裙显瘦姿势库：坐姿腿前伸不往里放、架腿藏肉、蹲姿遮肉、翘腿侧伸面向镜头、侧前方45度伸腿绷脚背，五类动作显瘦显长。",
  "tags": ["拍照姿势", "显瘦", "短裙", "腿部", "小红书"],
  "url": "http://xhslink.cn/o/6I0Gsupwsyf", "shots": 5, "segs": 20, "height": 2520},
 {"slug": "june-sales-fuel-cars", "title": "6月销量分析 燃油车篇", "duration": "29分钟", "date": "2026-08-09",
  "summary": "6月燃油车销量全景：行业下行定调、BBA减量保价（A6仅7000台）、丰田大众强势、二线豪华艰难、国产吉利长安奇瑞推荐，燃油车占比降至40%，抄底看8月底问价9-10月出手。",
  "tags": ["汽车", "销量分析", "燃油车", "购车建议", "小红书"],
  "url": "http://xhslink.cn/o/qjE7KV6b46", "shots": 6, "segs": 711, "height": 2920},
 {"slug": "photo-course-14", "title": "从0开始学摄影｜第十四期", "duration": "3分41秒", "date": "2026-08-09",
  "summary": "街头人像「随地大小拍」实拍教学：贩卖机停车场都能拍、重点在人物本身、构图避干扰、长条顶光专注眼神、侧面营造侧光立体感。",
  "tags": ["摄影教程", "人像", "街头摄影", "构图", "小红书"],
  "url": "http://xhslink.cn/o/4dCILnS6h6J", "shots": 6, "segs": 114, "height": 2520},
 {"slug": "beach-pose-machine", "title": "海边pose机 | 7个姿势拿捏夏日氛围感", "duration": "18秒", "date": "2026-08-09",
  "summary": "18秒海边pose快闪（纯音乐）：背影看海开场营造意境、侧身回头撩发借海风、回眸看镜头定格收尾，三段式拿捏夏日氛围感。",
  "tags": ["海边", "拍照姿势", "氛围感", "夏日", "小红书"],
  "url": "http://xhslink.cn/o/12eJ5bjRLUB", "shots": 4, "segs": 1, "height": 2160},
]

def main():
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    existing = {e.get("outputs", {}).get("html", ""): e for e in data if isinstance(e.get("outputs"), dict)}

    added = 0
    for e in ENTRIES:
        slug = e["slug"]
        html = f"{slug}-图文实录.html"
        if html in existing:
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
                "html": html,
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
            html = re.sub(r'href="[^"]*场景英译\.html"', f'href="{en_file}"', html, count=1)
            zh_file.write_text(html, encoding="utf-8")
            print(f"  ~ {slug}: 更新已有链接")

    print("完成")


if __name__ == "__main__":
    main()
