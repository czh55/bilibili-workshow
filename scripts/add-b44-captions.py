#!/usr/bin/env python3
"""b44：向 translations.json 追加 5 个视频的图注英文翻译（幂等）。"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATH = ROOT / "translations.json"

NEW = {
    # no-many-clothes
    "作者身穿白色基础款T恤出镜，介绍第一个穿搭思路": "The creator appears in a white basic tee, introducing the first styling idea.",
    "无袖蛋糕领白T，是白T的第一种替换款": "A sleeveless cake-neck white tee, the first alternative to a plain white tee.",
    "牛仔裤、短裙等基础款下装，说明下半身全带基础款": "Denim jeans and skirts as basic bottoms, showing that all lower half items are basics.",
    "裸色包臀裙外搭彩色条纹衬衫的罩衫造型": "A nude bodycon skirt styled with a colorful striped shirt worn as an overlay.",
    "白色上衣叠穿黑色小罩衫当披肩，层次感穿搭": "A white top layered with a black mini cardigan worn like a shawl for depth.",
    "油画感鱼骨衣配白色短裙的亮色设计款搭配": "An artistic corset top paired with a white skirt as a bright statement piece.",
    "粉色纯棉T恤与缎面短裙的统一色调、不同材质搭配": "A pink cotton tee with a satin skirt — same tone, different textures.",
    "纯色基础款套装，强调成套省心不用搭配": "A solid-color basic set, emphasizing how easy it is to wear as-is.",
    "民族风大包、双肩包等配饰，说明用配饰撑起整套 look": "Ethnic-style bags and backpacks as accessories to elevate a whole look.",
    "黑色背心搭配糖果色饺子包的造型": "A black vest styled with a candy-colored hobo bag.",
    # wulingshan-aranya
    "博主开场介绍两天一夜的雾灵山阿那亚山居之旅": "The creator introduces a two-day mountain retreat at Wulingshan Aranya.",
    "蓝椰酒店外景与自驾到达的画面": "The exterior of Lanye Hotel and the arrival by car.",
    "酒店门前的小花园，适合遛狗拍照": "The little garden in front of the hotel, great for walking dogs and photos.",
    "第一食堂的用餐环境与菜品": "The dining hall and dishes at the first canteen.",
    "房间的榻榻米设计，简洁干净": "The tatami-style room, simple and clean.",
    "适合拍照的酒店大堂与旁边的杂货商店": "The photogenic hotel lobby with a lifestyle store next door.",
    "山间小路与周边小景点": "The mountain trails and nearby scenic spots.",
    "山泉旁的小瀑布": "The small waterfall beside the mountain spring.",
    "适合带小朋友玩的灯塔自然乐园": "The Lighthouse Nature Park, perfect for families with kids.",
    "去温泉路上被绿植包围、沿台阶而上的山景": "The path to the hot spring, surrounded by greenery and stone steps.",
    "温泉入口处，工作人员讲解冲洗换泳衣的流程": "At the hot spring entrance, staff explain the rinse-and-change process.",
    # easy-pose-simple
    "博主在实景中开场，介绍「交叉」与「支点」两个知识点": "The creator opens on location, introducing the two tips: crossing and a pivot point.",
    "站姿腿交叉、手交叉的示范": "A standing demo of crossing legs and arms.",
    "坐姿交叉与插兜姿势的示范": "A sitting demo with crossed limbs and hands in pockets.",
    "以板凳、马路牙子为例演示坐姿交叉": "Crossing while sitting on a bench or curb.",
    "叉腰、搭头等「三角形」姿势": "Triangle poses such as hands on hips or a hand on the head.",
    "单手、双手靠桌子的倚靠姿势": "Leaning poses with one hand or both hands on a table.",
    "靠墙、靠门窗等环境元素的倚靠姿势": "Leaning against a wall, door, or window as environmental elements.",
    "结尾总结「交叉、支点」两个关键词": "The closing summary of the two keywords: crossing and a pivot point.",
    # urban-village-answer
    "东京市中心密集的握手楼群，引出「像中国城中村」的对比": "Dense handshake buildings in central Tokyo, sparking the comparison to China's urban villages.",
    "深圳城中村停满电动车的道路，说明只留不到 60% 空间": "A street in a Shenzhen urban village packed with e-bikes, leaving less than 60% of the road.",
    "日本电动车法案对宽度、时速的限制说明": "Japan's e-bike regulations limiting width and speed.",
    "清水市摩天轮俯瞰握手楼，色彩低饱和协调": "A ferris wheel view of handshake buildings in Shimizu, low-saturation and harmonious.",
    "深圳大芬油画村街道，材质配色混搭略显杂乱": "A street in Shenzhen's Dafen Oil Painting Village, where mixed materials look cluttered.",
    "城中村外立面的不锈钢防盗网": "Stainless steel security bars on urban village facades.",
    "东京中央区握手楼酒店的窗外绿植与柜本状窗户": "Greenery outside the window and cabinet-like windows at a Tokyo hotel in handshake buildings.",
    "深圳城中村分布图，显示城中村大面积覆盖": "A distribution map showing urban villages covering most of Shenzhen.",
    "改造后的南头古城街道": "The renovated streets of Nantou Ancient Town.",
    "南头古城城市微更新后的特色街景": "Distinctive streetscapes of Nantou Ancient Town after micro-regeneration.",
    # one-house-vs-zijian
    "动漫房子的下大上小结构，说明降低重心更温馨": "The anime house's wider-base, narrower-top structure that lowers the center of gravity.",
    "想象「小新家在中国」的上下一样厚重建造": "An imagined Chinese version of Shin-chan's house, heavy and boxy.",
    "自建房的反光不锈钢、彩色窗户等不协调外墙": "Clashing facades on self-built houses: reflective steel and colorful windows.",
    "一户建材质统一、低饱和色调的协调外墙": "A coordinated facade on a Japanese detached house with unified materials and muted tones.",
    "呆板房子与凹凸设计的对比": "A flat, boring house versus one with recessed and projecting details.",
    "工地板房与建筑设计师家的错落感对比": "A construction site hut versus an architect's home — the contrast in layering.",
    "多层次的错落感让建筑更灵动": "Multi-level layering makes a building feel more dynamic.",
    "总结演示：上小下大结构+色调相近颜色+绿植": "Summary demo: a tapered structure, harmonious colors, and greenery.",
}

data = json.loads(PATH.read_text(encoding="utf-8"))
added = 0
for zh, en in NEW.items():
    if zh not in data:
        data[zh] = en
        added += 1
    elif data[zh] != en:
        data[zh] = en
        added += 1
PATH.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"新增/更新 {added} 条，共 {len(data)} 条")
