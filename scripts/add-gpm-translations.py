#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为 guide-pose-model 完整版的 18 个图注追加英文翻译到 translations.json（幂等）。"""
import json
from pathlib import Path

P = Path(__file__).resolve().parent.parent / "translations.json"
t = json.loads(P.read_text(encoding="utf-8"))

NEW = {
    "画圈圈原则：一只脚站稳，另一只脚画圈圈": "The circle principle: plant one foot firmly while the other draws a circle around it",
    "六个脚法点位的实拍参考：脚位一到脚位六": "Real-shot reference of the six foot positions, from position one to six",
    "单手美姿：固定手 + 功能手": "One-hand posing: a fixed hand plus a functional hand",
    "功能手自上而下：挡太阳→抓头发→揉眼睛→揉鼻子→咬嘴巴→放下巴→放胸口→交叉": "The functional hand moves top-down: shield the sun, touch the hair, rub the eyes, rub the nose, bite the lip, rest on the chin, on the chest, then fold the arms",
    "双手美姿：抱胸八字起式 + 功能手变化": "Two-hand posing: arms crossed in a figure-eight start, then functional-hand variations",
    "坐姿：135° + 前方脚伸长、后方脚漏半鞋": "Seated pose: 135° leg angle, front foot extended and back foot showing half a shoe",
    "坐姿手法：前方手固定，后方手自上而下抓": "Seated hand technique: front hand fixed, back hand grabbing from top to bottom",
    "平行蹲：两脚并拢 + 提气头朝上": "Parallel squat: feet together, lift your energy and keep your head up",
    "后方重心腿蹲：后方腿支撑，前方腿往前伸约 110°": "Rear-weight squat: back leg supports, front leg extends forward at about 110°",
    "前方腿重心蹲：前方脚着地，后方腿往前伸约 110°": "Front-weight squat: front foot grounded, back leg extends forward at about 110°",
    "通用手法：固定手不变，功能手画圈圈自上而下抓": "Universal hand method: keep the fixed hand still while the functional hand sweeps top-down in a circle",
    "反面教材：头、肩、手三个部位同时靠墙，人像电线杆没有曲线": "Bad example: head, shoulder and hand all lean on the wall, making the body stiff like a pole with no curves",
    "手靠墙：反手搭或直接支撑": "Hand leaning on the wall: backhand hook or direct support",
    "肩膀靠墙：侧面用肩靠，头尽量不靠": "Shoulder leaning on the wall: lean sideways with the shoulder, keep the head off the wall",
    "臀部靠墙：上半身往前压，线条感更好": "Hip leaning on the wall: press the upper body forward for better lines",
    "单脚靠墙：脚勾起来，洒脱感": "One-foot lean: hook one foot up on the wall for a free-spirited look",
    "墨镜道具：垂下 → 腹部 → 锁骨 → 嘴 → 眼睛 → 头顶": "Sunglasses prop: hang down, to the waist, collarbone, mouth, eyes, then top of the head",
    "背包道具：垂下 → 放上一点 → 腹部 → 侧面 → 肩": "Backpack prop: hang down, raise it a bit, to the waist, to the side, then onto the shoulder",
}

added = skipped = 0
for zh, en in NEW.items():
    if zh in t:
        skipped += 1
    else:
        t[zh] = en
        added += 1

P.write_text(json.dumps(t, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"added={added} skipped={skipped} total={len(t)}")
