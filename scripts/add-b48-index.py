#!/usr/bin/env python3
"""b48：为 11 篇新视频追加 index.json 条目（v09 documentary-color-tone 已存在跳过）。"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
INDEX = DOCS / "index.json"

DATE = "2026-08-17"

ENTRIES = [
    {
        "slug": "light-ratio-texture", "title": "光比决定质感！布光万能公式 + 直出调色分享",
        "duration": "6分41秒", "tags": ["摄影", "布光", "口播", "调色"],
        "url": "https://xhslink.cn/o/1gqVKXOrNVY",
        "summary": "核心判断：高质感口播画面不靠昂贵设备，而靠一条可控的光线逻辑——侧光制造立体感，一盏可控主灯实现明暗分离，按空间选焦段，再叠加反光板、色温差、轮廓光、造型光四招进阶，最后前机 S-Log3 + 定制 LUT 直出。",
        "shots": 10, "segs": 226, "height": 6522,
    },
    {
        "slug": "street-style-fashion", "title": "如何让你的街拍充满时尚感？",
        "duration": "53秒", "tags": ["摄影", "街拍", "构图", "姿势"],
        "url": "https://xhslink.cn/o/8TsYSymGw4o",
        "summary": "核心判断：街拍时尚感不是靠环境或设备，而是三个可执行的口令层——机位与站位（举高+侧位）、构图（头顶空间、一分为二、纯背景）、姿势与情绪（倒肩伸手、半身右上角、松弛不盯镜头）。每个口令都能独立复制到下一次拍摄。",
        "shots": 7, "segs": 29, "height": 6474,
    },
    {
        "slug": "stairs-atmosphere-shot", "title": "遇见楼梯一定要试试这样拍🎬氛围感十足",
        "duration": "39秒", "tags": ["摄影", "楼梯拍照", "构图", "氛围感"],
        "url": "https://xhslink.cn/o/6lkYQliTehU",
        "summary": "核心判断：同一个楼梯，氛围感来自机位与视角的选择——抬高手机拍纵深感、俯拍裙摆、侧前低机位三分线、侧面三角形构图。每个技巧都是一组可复制的动作口令（抬高/后退/倍率/站位），翻车与出片的差别就在这几个动作上。",
        "shots": 5, "segs": 26, "height": 5907,
    },
    {
        "slug": "purple-gray-advanced", "title": "为什么紫色和灰色，普通人总穿不出高级感",
        "duration": "2分03秒", "tags": ["穿搭", "色彩", "紫色", "灰色"],
        "url": "https://xhslink.cn/o/75VSx2Jf71c",
        "summary": "核心判断：紫与灰是最难穿的两个颜色，但它们不是「穿上就赢」，而是「人成就颜色」——紫色要求内在精神属性（烟火气不足、身型纤弱），灰色要求五官立体与风格鲜明（否则灰扑扑无存在感）。灰色尤其极端：要么金字塔尖的最高级，要么毫无态度主张的最低级。",
        "shots": 7, "segs": 58, "height": 6119,
    },
    {
        "slug": "daily-expression-possession", "title": "你绝对没注意过自己日常生活中的表情，原来",
        "duration": "3分23秒", "tags": ["形体", "表情管理", "眼神", "气质"],
        "url": "https://xhslink.cn/o/8lHE9mjVYTv",
        "summary": "核心判断：气质的差距不在五官而在「控制力」——眼神的定力（十秒不眨眼、三秒换视点）和表情管理（面无表情是克制无意识表情的结果），加上肩开、腹收、颈立、背挺的行走姿态。这套方法把抽象的「气质」拆成可训练、可验收的具体口令。",
        "shots": 9, "segs": 139, "height": 6491,
    },
    {
        "slug": "jewelry-black-photo", "title": "珠宝拍摄死黑不是灯越多越好，方法很重要！",
        "duration": "36秒", "tags": ["摄影", "珠宝", "静物", "布光"],
        "url": "https://xhslink.cn/o/8wSI0L4wwFP",
        "summary": "核心判断：珠宝金属面死黑的根因不是灯不够亮，而是光源方向与柔化方式不对。专业解法三步走：关掉侧灯减少干扰光、主光移到正后方统一方向、硫酸纸做天幕柔化硬光；剩余局部死黑用左右银卡纸反射补光即可。灯的数量不重要，方法才重要。",
        "shots": 8, "segs": 15, "height": 5973,
    },
    {
        "slug": "new-rule-content-power", "title": "原来新规内容力是这样的",
        "duration": "1分48秒", "tags": ["直播", "内容力", "电商", "话术"],
        "url": "https://xhslink.cn/o/37FdIdE1s6i",
        "summary": "核心判断：平台内容力新规的实质是「去营销化、要活人感」——画质画面去同质化（不能绿幕/AI/不清晰）、话术去营销化（卖点场景化情绪化）、内容做成自然流属性（教知识/测评/故事）。直播结构从「直接卖」转向「先做围观内容再转化」，全域流量（A1-A5）下多数观众只有意向没有购买行为，先给价值才能留人。",
        "shots": 8, "segs": 79, "height": 6290,
    },
    {
        "slug": "worst-talent-2026", "title": "原来这就是26年最差的达人！",
        "duration": "34秒", "tags": ["直播", "达人", "主播", "话术"],
        "url": "https://xhslink.cn/o/9Ak8T6Ytfaf",
        "summary": "核心判断：26 年最差达人的三个标签——状态平尬无控场（直播与短视频的控场需求不同）、话术像说明书没人情味（转化差）、逼单生硬不会来事（最后两单最后三单是典型反面）。三个问题共同指向同一件事：直播能力没有拎起来。",
        "shots": 5, "segs": 26, "height": 5865,
    },
    {
        "slug": "stir-fry-water-mistake", "title": "你炒的菜全是水？因为从开火第一步就错了",
        "duration": "5分34秒", "tags": ["美食", "炒菜", "调料", "烹饪科学"],
        "url": "https://xhslink.cn/o/AhYuW8cvrKR",
        "summary": "核心判断：在家炒不出饭店味不是手艺差，而是调料下锅时机全反了。一切建立在两个物理化学现象上——美拉德反应（蛋白质+糖，140 度以上锁香）与莱顿弗洛斯特效应（200 度锅面蒸汽膜不粘不糊）。每样调料按化学性质选择时机：盐分肉菜汤三条铁律、生抽高温激发、老抽管色、蚝油怕热、姜蒜葱有序、醋分烹与点、淀粉临出锅。",
        "shots": 13, "segs": 53, "height": 7545,
    },
    {
        "slug": "knowledge-base-depreciation", "title": "小心，你刚建的知识库可能正在贬值",
        "duration": "3分33秒", "tags": ["知识库", "笔记", "AI", "第二大脑"],
        "url": "https://xhslink.cn/o/Ab8mwlYPLOp",
        "summary": "核心判断：知识库贬值的根因不是存储量，而是「燃料」质量——被动记录产出的流水账是死语料，AI 检索再强也点不燃。解法是转向苏格拉底式引导：取消文件记录与手动整理，只保留对话（人天生擅长说话），让 AI 像心理教练一样反问追问，把模糊情绪拆解成具体归因，从而产出可用燃料。结果是知识库自组织长成树，价值从「存了多少」转向「认知被加工到什么密度」。",
        "shots": 9, "segs": 95, "height": 7049,
    },
    {
        "slug": "valentine-rose-tutorial", "title": "七夕“压纹玫瑰”🌹详细拆解教学",
        "duration": "2分21秒", "tags": ["咖啡", "拉花", "压纹玫瑰", "教学"],
        "url": "https://xhslink.cn/o/424nLiPriOE",
        "summary": "核心判断：压纹玫瑰的灵魂是「流量节奏 + 液面轨迹控制」。四步流程：①融合（低流距小流量、注入点在杯底距液面最高点、防砸气泡）；②画椭圆搅拌（拉高流距、轨迹必须在液面内不碰杯壁）；③开底+二段（四分满后液面中心偏上注入、持续增流量边摆边回杯、半圆时缸子前推两厘米、深V底纹、二段更大流量回包）；④八字收尾+推花瓣（钢嘴贴近液面速度快、左右交替推瓣、花蕊加大流量包裹）。每一步都在解决同一件事：让奶泡稳定停留在液面、纹路干净成型。",
        "shots": 10, "segs": 20, "height": 6701,
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
            "date": DATE,
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


if __name__ == "__main__":
    main()
