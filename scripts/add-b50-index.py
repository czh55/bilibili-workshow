#!/usr/bin/env python3
"""b50：为批内新视频追加 index.json 条目（幂等，已存在跳过）。"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
INDEX = DOCS / "index.json"

DATE = "2026-08-25"

ENTRIES = [
    {
        "slug": "la-la-land-colorist", "title": "《爱乐之城》调色师，带你调色：从一级校色开始建立色彩分离",
        "duration": "10分42秒", "tags": ["调色", "达芬奇", "爱乐之城", "一级校色", "教学"],
        "url": "https://xhslink.cn/o/9MqPNKA33FQ",
        "summary": "核心判断：所有优秀调色的秘密都在一级校色（primaries）——它决定高光/中间调/暗部的颜色选择、对比曲线与细节取舍，是全片基调的地基。Offset 复刻胶片实验室配光控制，线性一级校色适合快速工作，二者可单独或组合使用。判断画面是否干净，先看色彩分离与肤色平衡；Parade 波形是验证白平衡的可靠工具。",
        "shots": 9, "segs": 32, "height": 6993,
    },
    {
        "slug": "lut-placement-tips", "title": "LUT使用的小秘诀：放链路开头还是结尾？",
        "duration": "2分08秒", "tags": ["调色", "LUT", "色域", "教学"],
        "url": "https://xhslink.cn/o/6DWfzldxlgw",
        "summary": "核心判断：LUT 在调色链路中放开头还是结尾，取决于是否保护了交付色域——放开头可以，但必须用 DCI P3 limiter 兜底（否则显示器上看不到的色可能在 P3 投影色域里显形）；放链路末尾、先校色后套 LUT，则全程在已知调色板内工作，更可控也更省时。",
        "shots": 4, "segs": 10, "height": 5598,
    },
    {
        "slug": "alibaba-465b-share-sale", "title": "阿里账上465亿美金，为什么还要卖股票",
        "duration": "5分58秒", "tags": ["阿里巴巴", "配股", "港股", "AI", "财经分析"],
        "url": "https://xhslink.cn/o/AevRrQbFItb",
        "summary": "核心判断：阿里不缺钱，缺的是确定的未来现金流——现金是用来活的不是烧的（3800 亿投资计划还有一半要花），募资买的是 AI 窗口期；选股权而非发债，是因为债有硬性还本付息约束而 AI 回报周期不确定，本质是用电商时代的信用对换 AI 时代的所有权。800 亿只稀释约 3.8%，其余跌幅来自估值语言从现金牛到增长股的切换，股东结构正在换血。",
        "shots": 8, "segs": 193, "height": 7016,
    },
    {
        "slug": "finalcut-auto-edit-workflow", "title": "终于😭 FinalCut也能用的自动剪辑工作流",
        "duration": "3分47秒", "tags": ["Final Cut Pro", "AI剪辑", "ChadCut", "效率工具", "教程"],
        "url": "https://xhslink.cn/o/874xMKvHEdF",
        "summary": "核心判断：Chad Cut + AI Agent（Codex/Claude Code）+ 自制 skill 构成一条能在 Final Cut Pro 上跑的自动剪辑链——Agent 一句话配置与指挥，Chad Cut 做口播粗剪、B-roll、字幕与动画，skill 打通工程导入 Final Cut 二次创作。AI 剪辑仍需人工纠错，但脏活已省下；真正让它越来越懂你的机制是剪辑习惯文档 + 每次项目后复盘。",
        "shots": 6, "segs": 35, "height": 6926,
    },
    {
        "slug": "tree-vs-wall-crash", "title": "为啥\"更软\"的树，反而更危险？刹车坏了，如何自救？",
        "duration": "8分31秒", "tags": ["汽车安全", "碰撞测试", "刹车失灵", "自救", "科普"],
        "url": "https://xhslink.cn/o/947KAfQ6d2o",
        "summary": "核心判断：刹车失灵时选树更危险——判断碰撞危险不取决于障碍物硬度，而看防撞梁、吸能盒、前纵梁有没有接住撞击；细窄的树能绕开关键结构直接伤及成员舱，宽墙反而让整个车头一起吸能。刹车失灵后决定后果的第一因素是车速（动能与速度平方成正比），第二是车辆是否失控，第三才是撞树还是撞墙；正确处置是全力减速并稳住车辆，而非最后一刻猛打方向找墙。",
        "shots": 9, "segs": 270, "height": 7254,
    },
    {
        "slug": "latte-art-integration", "title": "咖啡拉花入门要看：融合做不好，液面怎么干净？",
        "duration": "2分31秒", "tags": ["咖啡", "拉花", "融合", "教学"],
        "url": "https://xhslink.cn/o/470wpG6zFLv",
        "summary": "核心判断：拉花液面干净取决于融合四口诀——折杯融合（咖啡液面变深防翻滚）、高融合（杯缸距 5-10cm 避免白奶纹）、椭圆形融合（流量稳不浇杯底）、大面积快速融合（液面流动、减缓奶泡分层）。融合要高出图贴面，两者高度要求不同。",
        "shots": 4, "segs": 20, "height": 6290,
    },
    {
        "slug": "top-beauty-nose-design", "title": "这才是有效设计：怎么驾驭顶级美鼻",
        "duration": "3分35秒", "tags": ["面部美学", "鼻子", "医美设计", "美学"],
        "url": "https://xhslink.cn/o/8b4HbiFni3b",
        "summary": "核心判断：驾驭顶级美鼻需要整套面部骨像配合而非单点追鼻子——山根高且有好看转折、眉骨包眼眶并眼头留白、鼻走势有攻击性、鼻翼光影下压、OG 线该薄则薄该厚则厚、下巴往前而非往下。设计的本质是比例与光影的混合感；原图驾驭不了顶鼻，需结合混合感元素，且不可盲目跟风。",
        "shots": 6, "segs": 30, "height": 6990,
    },
    {
        "slug": "liquify-beats-colorgrade", "title": "调色再好也没用！高手差距藏在人像液化里",
        "duration": "1分49秒", "tags": ["人像修图", "液化", "PS", "后期", "教学"],
        "url": "https://xhslink.cn/o/7CwyoYiyoib",
        "summary": "核心判断：调色没问题成片还不好看，毛病全在液化——正确顺序先头发（抬高颅顶显脸小）、再体态（头肩比与线条）、后面部（微调保留辨识度+中性灰光影）。关键是留住面部原生高光与皮肤肌理，只去暗沉疲惫，杜绝塑料假磨皮；片子廉价不是技术不足，而是修得过于完美失去人像灵魂。",
        "shots": 4, "segs": 24, "height": 6173,
    },
    {
        "slug": "bright-skin-one-minute", "title": "高级白亮透｜1分钟拯救废片，这样调色太绝了",
        "duration": "1分26秒", "tags": ["人像修图", "调色", "CameraRaw", "PS", "教学"],
        "url": "https://xhslink.cn/o/1dcUcoV877r",
        "summary": "核心判断：白亮透调色四步——先诊断（光线杂乱/背景抢主体/肤色蜡黄），Camera Raw 提黑降对比控回画面信息，RGB S 曲线加强对比+蓝通道中部定点提亮去黄，最后背景/人物蒙版分区处理建立层次、颜色分级给高光加少量蓝色。核心是让主体突出、肤色干净、层次分明。",
        "shots": 4, "segs": 30, "height": 6359,
    },
    {
        "slug": "liquify-bone-structure", "title": "人像高不高级，主要看液化！",
        "duration": "2分14秒", "tags": ["人像修图", "液化", "骨相", "后期", "科普"],
        "url": "https://xhslink.cn/o/7wttcbBXnW",
        "summary": "核心判断：人像高级感主要看液化——调色只是摆盘，液化才是雕刻骨像的刻刀；液化靠骨像和肌肉审美，分寸差一点气质全垮。核心三字是骨像感，最怕的不是推多而是不知道哪里该收。正确顺序是先整体后局部、先轮廓后色调、五官不乱动；液化不是换头，高手知道何时该收手。",
        "shots": 4, "segs": 46, "height": 6197,
    },
    {
        "slug": "chin-aesthetics-code", "title": "下巴的美学密码",
        "duration": "0分16秒", "tags": ["面部美学", "下巴", "医美", "美学"],
        "url": "https://xhslink.cn/o/4K2ablmHHbj",
        "summary": "核心判断：下巴美学看比例不看绝对长短——短不丑（后缩才显嘴凸）、方要有度（宽度不超瞳距）、长要连贯（下颌圆崎断层显假面）、翘要克制（超鼻孔显脸长）。四条边界构成下巴审美的基本框架。",
        "shots": 2, "segs": 9, "height": 4430,
    },
    {
        "slug": "forehead-aesthetics-design", "title": "额头美学设计",
        "duration": "0分13秒", "tags": ["面部美学", "额头", "眉骨", "美学"],
        "url": "https://xhslink.cn/o/2XIklA1WYa6",
        "summary": "核心判断：额头美学是比例游戏——宽窄与下颌呼应、高低与眉毛联动、后倾靠额肌结节过渡、前凸靠眉骨承接。设计的关键是让额头与下半脸形成连贯的比例关系。",
        "shots": 2, "segs": 5, "height": 4499,
    },
    {
        "slug": "facial-balance-features", "title": "有辨识度的面部平衡",
        "duration": "0分26秒", "tags": ["面部美学", "骨相", "眉眼", "医美", "美学"],
        "url": "https://xhslink.cn/o/85o21bnOryy",
        "summary": "核心判断：面部平衡的美学判断——每个部位都有边界：眉毛低可以但不能短（短显老局促）、中庭长可以但鬓区不能窄（窄显脸长头大）、下颌方可以但嘴巴不能太小（显小气）、颧骨高是骨相优势但要有眉毛包裹颧弓才有高级感。辨识度来自比例平衡而非单点极致。",
        "shots": 3, "segs": 16, "height": 4535,
    },
    {
        "slug": "latte-no-crema", "title": "没有油脂，怎么拉花？",
        "duration": "0分47秒", "tags": ["咖啡", "拉花", "油脂", "萃取", "教学"],
        "url": "https://xhslink.cn/o/95ranq8YKok",
        "summary": "核心判断：萃取油脂少也能拉花，关键在预融合——先倒打发好的牛奶预融合并旋转，让液面不再清汤寡水；预融合后液面支撑性变弱、牛奶流动性变强，融合时控制好奶量与注入速度。预融合还有两点好处：口感减少苦味、液面颜色更浅更干净、减少深色胶感。",
        "shots": 3, "segs": 16, "height": 5157,
    },
]


def main() -> None:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    existing = {
        e["outputs"]["html"]
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
