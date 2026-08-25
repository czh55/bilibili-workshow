#!/usr/bin/env python3
"""b50：建立 14 篇 shots JSON（基于转录内容节点的截图规划）。"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")

PLAN = {
    "la-la-land-colorist": {
        "key": "d01",
        "title": "《爱乐之城》调色师，带你调色",
        "duration": 642,
        "shots": [
            {"file": "shot-01.jpg", "time": "00:20", "chapter": 1, "scene": "开场立题：一级校色 primaries 是建立色彩分离与肤色平衡的起点"},
            {"file": "shot-02.jpg", "time": "01:40", "chapter": 2, "scene": "Offset 控制：达芬奇对胶片时代 lab 配光控制的复刻，位于一级校色面板"},
            {"file": "shot-03.jpg", "time": "02:20", "chapter": 2, "scene": "线性一级校色与 Offset 并排显示，可单独用也可组合使用"},
            {"file": "shot-04.jpg", "time": "04:58", "chapter": 3, "scene": "第一组对比素材：男士胡子偏中性、衬衫偏冷，观察色彩分离"},
            {"file": "shot-05.jpg", "time": "05:40", "chapter": 3, "scene": "暖冷两套一级校色对比：金色光晕覆盖 vs 更白更冷，肤色调随之改变"},
            {"file": "shot-06.jpg", "time": "07:00", "chapter": 4, "scene": "肤色局部对比：鼻梁处一张偏暖一张偏冷，仅用 primaries 实现"},
            {"file": "shot-07.jpg", "time": "08:00", "chapter": 4, "scene": "Parade 波形检查白平衡：蓝通道高低决定白色偏蓝还是偏黄"},
            {"file": "shot-08.jpg", "time": "09:30", "chapter": 5, "scene": "压暗阴影案例：为保证人物对比牺牲阴影细节，即 crushing the shadows"},
            {"file": "shot-09.jpg", "time": "10:20", "chapter": 5, "scene": "四人镜头暖冷双版本：Offset 与线性一级校色共同作用的最终对比"}
        ]
    },
    "lut-placement-tips": {
        "key": "d02",
        "title": "LUT使用的小秘诀",
        "duration": 128,
        "shots": [
            {"file": "shot-01.jpg", "time": "00:12", "chapter": 1, "scene": "问题提出：LUT 放在调色链路开头，随后再校色"},
            {"file": "shot-02.jpg", "time": "00:45", "chapter": 2, "scene": "建议在链路末尾加 DCI P3 limiter，把色彩限制在交付色域内"},
            {"file": "shot-03.jpg", "time": "01:20", "chapter": 3, "scene": "个人偏好：LUT 放在链路末尾，先校色后套 LUT，全程在已知色域内工作"},
            {"file": "shot-04.jpg", "time": "01:45", "chapter": 3, "scene": "结尾总结：两种 LUT 用法都成立，关键是与交付色域匹配"}
        ]
    },
    "alibaba-465b-share-sale": {
        "key": "d03",
        "title": "阿里账上465亿美金，为什么还要卖股票",
        "duration": 358,
        "shots": [
            {"file": "shot-01.jpg", "time": "00:05", "chapter": 1, "scene": "核心数字开场：800 亿港元配股，香港上市公司史上最大一级市场增发"},
            {"file": "shot-02.jpg", "time": "00:45", "chapter": 1, "scene": "募资用途白纸黑字：100% 投向 AI 与 AI 基础设施，无电商并购回购"},
            {"file": "shot-03.jpg", "time": "01:14", "chapter": 2, "scene": "机构层反应：一小时内超额认购，最终需求 280 亿美元，接近募资三倍"},
            {"file": "shot-04.jpg", "time": "01:30", "chapter": 2, "scene": "二级市场反应：港股开盘一度暴跌 10%，最低 110.4 港元跌破配售价"},
            {"file": "shot-05.jpg", "time": "02:05", "chapter": 3, "scene": "现金流视角：465 亿美元现金不是用来烧的，3800 亿投资计划已投一半"},
            {"file": "shot-06.jpg", "time": "03:20", "chapter": 4, "scene": "为什么选股权而非发债：债有还本付息约束，AI 回本周期无法确定"},
            {"file": "shot-07.jpg", "time": "04:30", "chapter": 5, "scene": "反直觉点：2024 年回购 125 亿美元股票，配售 ADS 约 115 美元，高卖低买"},
            {"file": "shot-08.jpg", "time": "05:05", "chapter": 5, "scene": "估值语言切换：从现金牛到增长股，股东结构换血带来的波动"}
        ]
    },
    "finalcut-auto-edit-workflow": {
        "key": "d04",
        "title": "终于😭 FinalCut也能用的自动剪辑工作流",
        "duration": 227,
        "shots": [
            {"file": "shot-01.jpg", "time": "00:12", "chapter": 1, "scene": "开头动画演示：AI 自动剪辑的口播粗剪，一刀未动的成片效果"},
            {"file": "shot-02.jpg", "time": "00:30", "chapter": 1, "scene": "半年使用 Chad Cut 的复盘：动画效果很好但没省下剪辑时间"},
            {"file": "shot-03.jpg", "time": "01:15", "chapter": 2, "scene": "第一步：对 Codex（ChatGPT 桌面端）下一句话，自动配置 Chad Cut"},
            {"file": "shot-04.jpg", "time": "01:55", "chapter": 3, "scene": "提示词展示：素材丢进对话，提出剪辑要求，可截图保存"},
            {"file": "shot-05.jpg", "time": "02:20", "chapter": 3, "scene": "Chad Cut 网页端剪辑界面：与主流剪辑软件相似的界面，AI 与人共同操控"},
            {"file": "shot-06.jpg", "time": "03:10", "chapter": 4, "scene": "关键经验：建一个自己的剪辑习惯文档，让 AI 每次执行后复盘"}
        ]
    },
    "tree-vs-wall-crash": {
        "key": "d05",
        "title": "为啥\"更软\"的树，反而更危险？刹车坏了，如何自救？",
        "duration": 511,
        "shots": [
            {"file": "shot-01.jpg", "time": "00:15", "chapter": 1, "scene": "极限二选一：左侧树右侧墙，一秒钟要选哪个避险目标"},
            {"file": "shot-02.jpg", "time": "00:40", "chapter": 1, "scene": "碰撞吸能结构：防撞梁摊开力，吸能盒与前纵梁压溃折叠吸收能量"},
            {"file": "shot-03.jpg", "time": "01:30", "chapter": 2, "scene": "25% 偏置碰撞测试：64km/h 车头一侧撞刚性物体，考验单纵梁受力"},
            {"file": "shot-04.jpg", "time": "02:05", "chapter": 2, "scene": "撞宽墙对比：平整宽墙让更多吸能结构同时参与，近似 100% 正面碰撞"},
            {"file": "shot-05.jpg", "time": "03:10", "chapter": 3, "scene": "拳套比喻：金属拳套打水泥墙手会断，车太硬则人就要变形"},
            {"file": "shot-06.jpg", "time": "04:30", "chapter": 4, "scene": "防撞梁设计：抗弯能力、材料与截面结构，口子越多结构稳定性越好"},
            {"file": "shot-07.jpg", "time": "05:30", "chapter": 4, "scene": "前纵梁三段工作：前端被撞折、中间折叠耗能、末端把力分给车身"},
            {"file": "shot-08.jpg", "time": "06:45", "chapter": 5, "scene": "刹车失灵处置：松油门扶稳方向开双闪，继续尝试刹车，逐步降挡"},
            {"file": "shot-09.jpg", "time": "08:10", "chapter": 5, "scene": "结论：决定事故后果的是撞击速度、车辆是否失控，其次才是目标选择"}
        ]
    },
    "latte-art-integration": {
        "key": "d06",
        "title": "咖啡拉花入门要看：融合做不好，液面怎么干净？",
        "duration": 151,
        "shots": [
            {"file": "shot-01.jpg", "time": "00:12", "chapter": 1, "scene": "折杯融合：杯子微微倾斜让咖啡液面变深，倒入牛奶时不易剧烈翻滚"},
            {"file": "shot-02.jpg", "time": "00:45", "chapter": 2, "scene": "高融合：杯与缸距离 5-10 厘米，液面才不会有白色奶纹"},
            {"file": "shot-03.jpg", "time": "01:12", "chapter": 2, "scene": "椭圆形融合示范：避免圆形融合导致流量忽大忽小、牛奶浇杯底"},
            {"file": "shot-04.jpg", "time": "01:50", "chapter": 3, "scene": "大面积快速融合：让液面流动起来，减缓奶泡分层，避免拉花一坨"}
        ]
    },
    "top-beauty-nose-design": {
        "key": "d07",
        "title": "这才是有效设计：怎么驾驭顶级美鼻",
        "duration": 215,
        "shots": [
            {"file": "shot-01.jpg", "time": "00:20", "chapter": 1, "scene": "山根高低落差：混合感的关键区域必须高，且要有好看的转折"},
            {"file": "shot-02.jpg", "time": "01:00", "chapter": 1, "scene": "眉弓包住眼眶：眉骨不一定要往上做，但要包裹眼眶、塑造眼窝"},
            {"file": "shot-03.jpg", "time": "01:40", "chapter": 2, "scene": "鼻走势向下向上起抬：真正的顶级鼻有攻击性气势，很多人驾驭不了"},
            {"file": "shot-04.jpg", "time": "02:10", "chapter": 3, "scene": "面部骨像打造：OG 线原理，该薄的地方薄、该厚的地方加厚"},
            {"file": "shot-05.jpg", "time": "02:55", "chapter": 3, "scene": "下巴要往前而非往下：这是脸上扎的东西达不到效果的原因"},
            {"file": "shot-06.jpg", "time": "03:25", "chapter": 3, "scene": "最终变化对比：方案包含美术与美学知识，需了解自己脸型再决策"}
        ]
    },
    "liquify-beats-colorgrade": {
        "key": "d08",
        "title": "调色再好也没用！高手差距藏在人像液化里",
        "duration": 109,
        "shots": [
            {"file": "shot-01.jpg", "time": "00:20", "chapter": 1, "scene": "第一步头发：抬高颅顶拉蓬松发丝，视觉上脸自然缩小"},
            {"file": "shot-02.jpg", "time": "00:40", "chapter": 2, "scene": "第二步体态：肩膀打开标准头肩比，手臂收窄修瘦不修细"},
            {"file": "shot-03.jpg", "time": "01:00", "chapter": 2, "scene": "第三步面部：脸型流畅微调，保留个人辨识度，校准五官比例"},
            {"file": "shot-04.jpg", "time": "01:25", "chapter": 3, "scene": "行业真话：片子廉价不是技术不足，而是修得过于完美失去灵魂"}
        ]
    },
    "bright-skin-one-minute": {
        "key": "d09",
        "title": "高级白亮透｜1分钟拯救废片，这样调色太绝了",
        "duration": 86,
        "shots": [
            {"file": "shot-01.jpg", "time": "00:12", "chapter": 1, "scene": "底片问题分析：光线杂乱无主次，背景抢主体，肤色蜡黄不均"},
            {"file": "shot-02.jpg", "time": "00:36", "chapter": 1, "scene": "Camera Raw 基础：提高黑色降对比和阴影，稍加高光与白色"},
            {"file": "shot-03.jpg", "time": "00:50", "chapter": 2, "scene": "曲线调整：RGB 拉 S 型曲线，蓝色曲线中部定点提亮去黄"},
            {"file": "shot-04.jpg", "time": "01:10", "chapter": 2, "scene": "蒙版分区：背景镜像蒙版反向控制空间层次，人物蒙版统一肤色"}
        ]
    },
    "liquify-bone-structure": {
        "key": "d10",
        "title": "人像高不高级，主要看液化！",
        "duration": 134,
        "shots": [
            {"file": "shot-01.jpg", "time": "00:22", "chapter": 1, "scene": "核心观点：调色只是摆盘，液化才是雕刻骨像的刻刀"},
            {"file": "shot-02.jpg", "time": "00:58", "chapter": 2, "scene": "液化核心三字：骨像感。最怕的不是推多，是不知道哪里该收"},
            {"file": "shot-03.jpg", "time": "01:15", "chapter": 2, "scene": "客户案例：收颧骨、顺下颌、调整颈部肌肉，微调三处保留辨识度"},
            {"file": "shot-04.jpg", "time": "01:40", "chapter": 3, "scene": "修图顺序：先观察整体比例找别扭处，先整体后局部，五官不乱动"}
        ]
    },
    "chin-aesthetics-code": {
        "key": "d11",
        "title": "下巴的美学密码",
        "duration": 16,
        "shots": [
            {"file": "shot-01.jpg", "time": "00:03", "chapter": 1, "scene": "下巴短不显丑，后缩才会比例失调显嘴凸"},
            {"file": "shot-02.jpg", "time": "00:10", "chapter": 1, "scene": "下巴方有气场但宽度超瞳距会奇怪，翘一点精致但超鼻孔显脸长"}
        ]
    },
    "forehead-aesthetics-design": {
        "key": "d12",
        "title": "额头美学设计",
        "duration": 13,
        "shots": [
            {"file": "shot-01.jpg", "time": "00:03", "chapter": 1, "scene": "上下平衡：额头宽下颌就宽，额头窄下颌就窄"},
            {"file": "shot-02.jpg", "time": "00:09", "chapter": 1, "scene": "比例呼应：额头高眉毛就高，额头前凸眉骨就要出来"}
        ]
    },
    "facial-balance-features": {
        "key": "d13",
        "title": "有辨识度的面部平衡",
        "duration": 26,
        "shots": [
            {"file": "shot-01.jpg", "time": "00:04", "chapter": 1, "scene": "眉毛可以低但不可以短：眉型短显老显局促"},
            {"file": "shot-02.jpg", "time": "00:16", "chapter": 1, "scene": "比例关系：中庭长鬓区不能窄，下颌方但嘴巴不能太小"},
            {"file": "shot-03.jpg", "time": "00:22", "chapter": 1, "scene": "颧骨高是骨相优势：前提是眉毛包裹住颧弓才有高级感"}
        ]
    },
    "latte-no-crema": {
        "key": "d14",
        "title": "没有油脂，怎么拉花？",
        "duration": 47,
        "shots": [
            {"file": "shot-01.jpg", "time": "00:08", "chapter": 1, "scene": "预融合：油脂少时先倒打发好的牛奶预融合，旋转让液面不再清汤寡水"},
            {"file": "shot-02.jpg", "time": "00:22", "chapter": 2, "scene": "控制奶量：预融合后液面支撑性变弱，牛奶流动性变强，需控注入速度"},
            {"file": "shot-03.jpg", "time": "00:40", "chapter": 2, "scene": "预融合两点好处：口感减少苦味，液面颜色浅一些更干净"}
        ]
    }
}

for slug, data in PLAN.items():
    out = ROOT / f"shots-{slug}.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"✓ {slug}: {len(data['shots'])} shots")
print(f"完成 {len(PLAN)} 篇")
