#!/usr/bin/env python3
"""b44 JSON 补全脚本：为场景 JSON 添加 practice/pitfalls/shifts/difficult_words"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "scripts" / "scene-data"

TOPIC_INFO = {
"no-many-clothes": (
 "极简旅行穿搭",
 [["出门拍照就得带很多衣服", "基础款任意切换能出十几套look", "小设计基础款不占地方还百搭"],
  ["基础款太素拿不出手", "用一个夸张配饰撑起整套", "大包耳饰丝巾都能当点睛之笔"],
  ["成套衣服死板不好搭配", "成套设计感衣服省心又耐看", "挂脖背心拆开还能组合出double look"]],
 [["旅行只能穿一套到底", "基础内搭+彩色罩衫变两套", "一件罩衫上穿下围都是新look"],
  ["配饰是多余的累赘", "配饰多不占地方还能撑起风格", "一个糖果色饺子包让黑背心出彩"]],
 [["basic", "基础款，百搭的单品"],
  ["topper", "罩衫，套在外面的上衣"],
  ["accessory", "配饰，点亮的单品"]],
),
"wulingshan-aranya": (
 "山居度假英语",
 [["短途旅行只能走马观花", "两天一夜也能深度放松", "吹风泡汤看山看日落节奏刚好"],
  ["带狗出行很麻烦", "有小狗托管住起来没压力", "民宿有家人陪着不用担心"],
  ["山间度假没得玩", "山路漫步瀑布灯塔都有内容", "从一期走到二期处处是景"]],
 [["旅行就是赶景点", "慢逛才是度假的正确方式", "绕一圈拍照听水声都值得"],
  ["酒店只用来睡觉", "大堂和小花园也是拍照点", "酒店大堂旁边还有集合店可逛"]],
 [["escape", "逃离，离开城市的放松"],
  ["voucher", "代金券，抵扣券"],
  ["wander", "漫步，随意走动"]],
),
"easy-pose-simple": (
 "摆姿教程",
 [["拍照只能站军姿", "记住交叉和支点两个词", "把平行的人变成交叉的"],
  ["姿势越复杂越好看", "肢体舒展开就有规律", "插兜、交叉、倚靠都算数"],
  ["摆姿靠天赋学不会", "身体动作里找三角形", "把躯干想成方块往上拼三角形"]],
 [["只会一个姿势摆到底", "站姿坐姿都能交叉", "坐路边插兜都是交叉"],
  ["环境是拍照障碍", "桌子墙门窗都是支点", "和环境互动就能自然出片"]],
 [["cross", "交叉，四肢与身体相交"],
  ["pivot", "支点，依托的环境"],
  ["torso", "躯干，身体主干"]],
),
"urban-village-answer": (
 "城市更新观察",
 [["握手楼等于脏乱差", "东京握手楼也是常态", "问题在配套而不在楼本身"],
  ["城中村必须全拆才能更新", "全拆在深圳基本不可能", "城中村面积甚至占城市一半"],
  ["电动车越多越好", "行人空间被挤没了", "给电动车设限反而保住步行体验"]],
 [["改造就是大拆大建", "保留楼体改造外立面也行", "南头古城微更新成旅游热点"],
  ["协调是玄学", "材质配色统一就协调", "黑白灰低饱和跟电线同色系"]],
 [["packed", "密集的，挤在一起的"],
  ["facade", "外立面，建筑外观"],
  ["pedestrian", "行人，步行者"]],
),
"one-house-vs-zijian": (
 "住宅设计审美",
 [["好看需要复杂设计", "上小下大的结构就够温馨", "降低重心给人舒服感"],
  ["外墙越多样越高级", "材质不超过两种才协调", "反光不锈钢彩色窗户都是不协调"],
  ["设计感靠装修堆", "错落感才是核心", "凹凸设计和光影绿植都算错落"]],
 [["自建房注定不好看", "三招就能变好看", "结构+配色+绿植就够"],
  ["小瓷砖越碎越精致", "缝隙太多显得乱", "碎墙面只能做装饰不能做主体"]],
 [["facade", "外立面，建筑的外观"],
  ["saturation", "饱和度，色彩浓度"],
  ["stepping", "错落感，建筑层次"]],
),
}

def main():
    for p in DATA_DIR.glob("*.json"):
        d = json.loads(p.read_text(encoding="utf-8"))
        slug = d["meta"]["slug"]
        if slug not in TOPIC_INFO:
            continue
        topic, pitfalls, shifts, diff = TOPIC_INFO[slug]
        practice = []
        for s in d["scenes"]:
            for zh, en, note in s["sentences"]:
                word = note.split("（")[0].strip()
                practice.append([f"用「{word}」替换表达", en])
        d["practice"] = practice
        d["pitfalls"] = pitfalls
        d["shifts"] = [s[:2] for s in shifts]
        d["difficult_words"] = diff
        d["meta"]["topic"] = topic
        d["footer_notes"] = f"来源：{d['meta']['title']}（小红书，时长{d['meta']['duration']}）"
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"✓ {slug} enriched")

if __name__ == "__main__":
    main()
