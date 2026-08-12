#!/usr/bin/env python3
"""b45：生成 9 篇小红书图文实录 HTML（含转录注入、术语校正、简体转换）。

用法：
  python3 scripts/b45-html.py {slug} [{slug} ...]
  python3 scripts/b45-html.py          # 全部 9 篇

说明：先运行 gen-caption-audio.py 生成图注英文音频，再运行 enhance-captions-html.py
将单语 figcaption 增强为中英对照（顺序不可颠倒）。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import opencc

    _T2S = opencc.OpenCC("t2s")
except ImportError:
    _T2S = None

try:
    from zhconv import convert as _zh_convert
except ImportError:
    _zh_convert = None

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"


def to_simplified(s: str) -> str:
    if _T2S:
        return _T2S.convert(s)
    if _zh_convert:
        return _zh_convert(s, "zh-cn")
    return s


def fmt(t: float) -> str:
    t = max(0, int(t))
    return f"{t // 60:02d}:{t % 60:02d}"


# whisper JSON 文件名映射：slug -> 音频前缀
SLUG_TO_AUDIO = {
    "mask-tutorial": "e01",
    "camera-movement-apple": "e02",
    "flower-shooting": "e03",
    "travel-shoot": "e04",
    "harmony-shooting": "e05",
    "light-and-shadow": "e06",
    "curve-color-grade": "e07",
    "color-grade-basics": "e08",
    "photo-clarity": "e09",
}

# 元数据：slug -> (标题, 时长秒, 标签, 原视频URL, 开场导语, 知识结构 rows, 总结)
DATA = {
    "mask-tutorial": {
        "title": "我今天必须教会你，蒙版！",
        "title_display": "蒙版到底怎么用？白加黑减，五步讲透",
        "duration": "1:51",
        "tags": "摄影 修图 剪辑 蒙版",
        "url": "http://xhslink.cn/o/2NnOyOfdlo3",
        "intro": "一支 1 分 51 秒的对话式教学：两位主角以「蒙版到底是啥」开场，从一张照片讲起，把修图和剪辑里最重要的蒙版功能拆成五个递进的知识点——白加黑减原理、不破坏原图的换天操作、亮度涂层局部提亮、视频过渡里的隐藏蒙版，最后落到线性蒙版的实际应用。全程用画面演示，看完就能上手。",
        "summary_rows": [
            ("00:00→00:07", "开场引入", "「蒙版到底是啥」——这个功能在修图和剪辑中都特别重要，值得专门学一次。"),
            ("00:07→00:32", "原理说明", "用「不想要天空却擦多了」的例子对比：有蒙版就不用重来。蒙版相当于给照片叠一块板子，想显示哪儿涂白、想隐藏哪儿涂黑，口诀是「白加黑减」。"),
            ("00:32→00:43", "操作演示", "蒙版在蒙版上操作，不破坏照片本身，可随意修改。换天、改变画面形状都是这么做的。"),
            ("00:43→00:67", "局部调整", "蒙版不只用于照片：调色、文字、视频都可以。人脸太暗时，在亮度涂层上加蒙版，只把脸部涂白，亮度调整就只作用于脸部。"),
            ("00:67→00:95", "视频过渡", "一段「两层视频」的过渡演示：A 段后半部分随电线杆边界逐渐隐藏，下一层的 B 段随之露出。"),
            ("00:95→01:50", "线性蒙版", "线性蒙版的效果是直线的一边显示、另一边隐藏。在 A 段视频上加上它，调整位置贴合电线杆向左移动，过渡就轻松实现。"),
        ],
        "takeaway": "蒙版的核心是「白加黑减」：在蒙版上用白色显示、黑色隐藏，从而在不破坏原图的前提下完成换天、局部调整、视频过渡等操作。从照片到视频，一个原理贯穿始终。",
        "chapters": [
            {
                "id": "ch1", "time": "00:00-00:07", "title": "蒙版到底是啥",
                "paras": [
                    "视频用一段轻松的对话开场。一个声音带着困惑发问：「这个蒙版到底是啥呀？」另一个声音立刻接上：「这个很有用了，在修图和剪辑中都特别重要。」被问「难不难」，对方打包票：「不难，我教你。」",
                ],
                "figs": [1],
            },
            {
                "id": "ch2", "time": "00:07-00:32", "title": "从擦掉天空说起：白加黑减",
                "paras": [
                    "教学从一张照片开始。主讲人指着照片：「如果我们不想要这个天空，把它擦掉了。」但难点出现了——「不小心擦多了，怎么办？」在没有蒙版的思路里，只能重来，下次仔细一点。",
                    "「但是有蒙版就不用这么麻烦了。」主讲人引出核心概念：蒙版相当于给照片上叠加一块板子，这块板子可以控制画面中哪里显示、哪里隐藏。规则很简单：「想显示哪儿，就在蒙版上涂上白色；想隐藏哪儿呢，就涂黑色。」一句话总结——「白加黑减」。",
                ],
                "figs": [2, 3],
            },
            {
                "id": "ch3", "time": "00:32-00:43", "title": "不破坏照片本身的换天操作",
                "paras": [
                    "听者总结自己的理解：「也就是在蒙版上操作，不破坏照片本身，可以随意修改。」主讲人肯定道：「对，那像换天、改变画面形状，都是这么做的。」蒙版的价值在这一刻体现出来：所有修改都在蒙版上完成，原图始终完好。",
                ],
                "figs": [4],
            },
            {
                "id": "ch4", "time": "00:43-00:67", "title": "从照片到调色：蒙版的局部调整",
                "paras": [
                    "听者以为蒙版「不常用」，主讲人立刻纠正：「那如果蒙版不只能用在照片上，调色、文字、视频都可以呢。」",
                    "他用一张照片演示：背景正常，但人脸太暗。「直接调亮度呢，整个画面都变亮了。」这不是想要的效果。办法是：在亮度涂层上加上一个蒙版，把其他部分涂黑、只把脸部涂白——「那这个亮度调整，就只在脸部才有了。甚至想要哪儿亮都可以。」这被总结为蒙版的另一个用途：局部调整。",
                ],
                "figs": [5, 6],
            },
            {
                "id": "ch5", "time": "00:67-00:95", "title": "视频过渡：一层一层分析",
                "paras": [
                    "「咱们再稍微难一点点。」主讲人放出一段视频，让听者猜它是怎么做的。听者觉得「太难了」，跟蒙版有什么关系？",
                    "主讲人带着观众一层一层拆解：「你看这个画面，其实它只有两段视频，A 段是这样，B 段是这样。重点在 A 段的后半部分——随着电线杆的边界，逐渐隐藏了。」下一层的视频，就会随着露出来。",
                ],
                "figs": [7, 8],
            },
            {
                "id": "ch6", "time": "00:95-01:50", "title": "线性蒙版：让过渡贴合画面",
                "paras": [
                    "揭晓答案：「你看这有一个线性蒙版，它的效果是直线的一边显示、另一边隐藏。」那么只需要在 A 段视频上加上它，调整位置，让蒙版贴合电线杆向左移动——「就轻松实现了。」",
                    "「我觉得我行了。」听者信心满满地收尾。从一张照片到一段视频，蒙版的原理始终一致：白显示、黑隐藏，板子移动到哪里，哪里就发生变化。",
                ],
                "figs": [9, 10],
            },
        ],
    },
    "camera-movement-apple": {
        "title": "什么是运镜？我用一颗苹果告诉你",
        "title_display": "用一颗苹果讲清五种运镜",
        "duration": "1:07",
        "tags": "摄影 运镜 镜头语言 短视频",
        "url": "http://xhslink.cn/o/8nlFEp6PEU9",
        "intro": "一支 1 分 07 秒的运镜科普：用一个苹果的冒险故事，把镜头语言讲得既有画面又易记。摇镜头渲染氛围、下降镜头开启故事、上升镜头收束结尾、推镜头放大情绪、拉镜头转向环境——每种运镜都有明确的叙事功能。",
        "summary_rows": [
            ("00:00→00:10", "开场引入", "以「我练运镜呢」开场，点出运镜除了耍帅还能讲故事。"),
            ("00:10→00:27", "摇镜头", "同一个苹果用不同运镜能拍出不同感觉。摇镜头可以渲染激烈的氛围，同时交代人物关系。"),
            ("00:27→00:42", "升降镜头", "下降镜头画面从全局到主角，是电影里常用的开场方式；上升镜头则适合作为结尾。"),
            ("00:42→00:51", "环境叙事", "明亮温馨的厨房是故事舞台——但都是假象，苹果决定离开。"),
            ("00:51→01:07", "推拉镜头", "推镜头在交代环境的同时放大人物情绪；向后拉镜头则情绪淡化、环境成为重点。"),
        ],
        "takeaway": "运镜不是炫技，而是叙事工具：摇镜头交代关系、下降镜头开场、上升镜头结尾、推镜头放大情绪、拉镜头转向环境。学会运镜，视频就能讲出不同感觉。",
        "chapters": [
            {
                "id": "ch1", "time": "00:00-00:10", "title": "运镜还能讲故事",
                "paras": [
                    "视频从一个疑问开场：「你干嘛呢？」「我练运镜呢。」随后立刻给出结论：「其实除了耍帅，运镜还能讲故事。」这句话奠定了全片的基调：运镜是服务于叙事的镜头语言，而不是单纯的炫技。",
                ],
                "figs": [1],
            },
            {
                "id": "ch2", "time": "00:10-00:27", "title": "摇镜头：渲染氛围，交代关系",
                "paras": [
                    "「你看啊，这颗苹果，用不同的运镜，能拍出不同的感觉。」主讲人举起苹果，用一段追跑戏演示。苹果要逃，镜头紧随其后。",
                    "「这是一颗苹果的宿命。」画风一转，进入正式的镜头讲解。第一种是摇镜头：「可以渲染激烈的氛围，同时交代人物关系。」在追跑中，镜头摇动带出的画面位置变化，让观众自然理解了苹果与「追捕者」的空间关系。",
                ],
                "figs": [2, 3],
            },
            {
                "id": "ch3", "time": "00:27-00:42", "title": "升降镜头：开场与结尾",
                "paras": [
                    "镜头落在一个「普通的厨房」，一段苹果的冒险故事即将上演。「这是下降镜头，画面从全局到主角，是电影里常用的开场方式。」全景先交代环境，镜头下降让主角苹果进入画面中心。",
                    "「反之呢，上升镜头则适合作为结尾。」主角（苹果）说完自己的宣言，镜头上升、画面拉开，为故事收束。听者恍然大悟：「有点意思，确实感觉不一样。」",
                ],
                "figs": [4, 5],
            },
            {
                "id": "ch4", "time": "00:42-00:51", "title": "环境叙事：明亮温馨是假象",
                "paras": [
                    "「这里很好，明亮又温馨。」但旁白随即揭穿：「但那都是假象，我必须离开这。」这段用环境本身推动叙事——明亮的厨房是苹果生活的舒适区，也暗示着它必须逃离的现状。镜头语言在此刻完成了「环境即情绪」的表达。",
                ],
                "figs": [6],
            },
            {
                "id": "ch5", "time": "00:51-01:07", "title": "推拉镜头：情绪与环境的博弈",
                "paras": [
                    "「推镜头，在交代环境的同时，放大人物情绪。」镜头缓缓推进，观众被拉近到苹果的决心之中。「同理向后拉镜头，情绪会淡化，环境变成重点。」镜头一退，视角重新回到厨房这个空间。",
                    "「原来这么多说法，以前我还真没注意过。」听者感慨。结尾点题：「总之你看，一颗苹果都能拍出不同感觉。学会运镜，你的视频也可以。」",
                ],
                "figs": [7, 8],
            },
        ],
    },
    "flower-shooting": {
        "title": "这么拍花，包出片的～",
        "title_display": "五个道具，把花拍出氛围感",
        "duration": "1:43",
        "tags": "摄影 拍花 道具 氛围感",
        "url": "http://xhslink.cn/o/61osLfkUpoT",
        "intro": "一支 1 分 43 秒的拍花教程：针对「拍多了千篇一律」的困扰，用五个随手可得的小道具——喷壶、透明塑料板、彩色卡纸、碎花瓣、纱巾——把静态的花拍出动态的氛围感。每步都有成品画面对照，跟着做就能出片。",
        "summary_rows": [
            ("00:00→00:20", "道具一：喷壶", "花大多是静态的，氛围感来自动态时刻。用喷壶把风的形状具象化，用水珠表达花朵的鲜嫩。"),
            ("00:20→00:40", "道具二：透明塑料板", "多雨春季有朦胧浪漫。把水喷到塑料板上，透过它去拍花。"),
            ("00:40→00:56", "道具三：彩色卡纸", "花的背景杂乱时，想到国画处理方式：平面化、乱中取静。拿出彩色卡纸，还能模仿画作装裱。"),
            ("00:56→00:71", "道具四：碎花瓣", "花一定要长在地上树上吗？捡起一地碎花瓣装进带水的碗，再用 Live 图特性，得到更生动的春天。"),
            ("00:71→00:91", "道具五：纱巾", "材质轻盈、有细密小孔的纱巾，调慢快门拍出梦幻感；盖在镜头前，显出光的形状。"),
            ("00:91→01:43", "结尾寄语", "生活日复一日，但祝我们都不要错过每一个花期的到来。"),
        ],
        "takeaway": "拍花出片的关键是给静态花朵制造动态氛围：喷壶造水珠、塑料板做朦胧、卡纸压杂乱、碎花瓣玩创意、纱巾出梦幻。五个道具五种氛围，全片可复现。",
        "chapters": [
            {
                "id": "ch1", "time": "00:00-00:20", "title": "喷壶：把风的形状具象化",
                "paras": [
                    "「最近花开得好好啊，但是我拍多了感觉都千篇一律的。」视频从真实的困扰出发。解法是什么？「没关系，我教你一些不那么路人的方式。」",
                    "核心观察：「花嘛，大多是静态的，而氛围感呢，常来源于那些动态的时刻。」于是第一个道具登场：喷壶。「不如准备一个喷壶，把风的形状具象化，用水珠表达花朵的鲜嫩。」喷水的一瞬，水珠在花瓣间飞散，静态的花立刻有了呼吸感。",
                ],
                "figs": [1],
            },
            {
                "id": "ch2", "time": "00:20-00:40", "title": "透明塑料板：多雨的朦胧浪漫",
                "paras": [
                    "「而除了阳光明媚，多雨的春季又有独属于它朦胧的浪漫。」第二个道具是透明塑料板：「将水喷到塑料板上，透过它去拍花，你就得到了……」画面中的花被水雾虚化，色彩变得柔润，仿佛隔着雨帘看花。",
                ],
                "figs": [2, 3],
            },
            {
                "id": "ch3", "time": "00:40-00:56", "title": "彩色卡纸：乱中取静",
                "paras": [
                    "「可很多时候你发现花的背景很杂乱。」面对杂乱背景，视频提出国画的处理方式：「平面化，乱中取静。」具体操作是拿出彩色卡纸——「所以你拿出了一张彩色卡纸。」把花与卡纸同框，背景的杂乱被卡纸的色块压住，画面瞬间安静。",
                    "「举一反三，模仿画作的装裱也可以。」同样的思路还可以玩出更多花样。",
                ],
                "figs": [4, 5],
            },
            {
                "id": "ch4", "time": "00:56-00:71", "title": "碎花瓣：换个载体玩创意",
                "paras": [
                    "「你又想，花一定要拍在地上树上的吗？」第四个道具打破常规。「你捡起了一地的碎花瓣，把它们装进了带水的碗中。」花瓣漂浮在水面，色彩在水中晕开。",
                    "「再充分利用 Live 图的特性，你就得到了更生动的春天。」Live 图记录的一小段动态，让花瓣的漂浮成为流动的画面。",
                ],
                "figs": [6, 7],
            },
            {
                "id": "ch5", "time": "00:71-00:91", "title": "纱巾：慢门与光的形状",
                "paras": [
                    "最后一个道具是纱巾：「手边有一条很适合春天的纱巾，它材质轻盈，还有细密的小孔。」「于是你调慢快门，就得到了……」慢门下纱巾在花间飘动，画面变得梦幻。",
                    "「你甚至学会了把它盖在镜头前，显出光的形状。」纱巾遮住镜头，光线透过小孔形成光斑——「于是你就拍出了很有梦幻感的春天。」",
                ],
                "figs": [8, 9],
            },
            {
                "id": "ch6", "time": "00:91-01:43", "title": "结尾：不要错过花期",
                "paras": [
                    "「生活虽然日复一日，年复一年，但祝你我都不要错过每一个花期的到来。」画面回到盛开的花景——「一切重新开始，一切生机盎然。」道具带来的不仅是技巧，更是提醒人去留意季节流转中的美。",
                ],
                "figs": [10],
            },
        ],
    },
    "travel-shoot": {
        "title": "假期旅游，就这么拍～",
        "title_display": "假期旅游高效出片四技巧",
        "duration": "2:09",
        "tags": "摄影 旅游 人像 构图",
        "url": "http://xhslink.cn/o/520YpUSJNKL",
        "intro": "一支 2 分 09 秒的旅游拍照指南：针对假期人多、出片慢的痛点，给出四个实用技巧——手机永远要平的构图基础、人多用长焦避开人群、同一姿势不超过三秒保持生动、用横屏视频抓拍转瞬即逝的风景再挑帧拼图。最后提醒：旅程不只有出片，愉快的经历才让旅途更美好。",
        "summary_rows": [
            ("00:00→00:40", "技巧一：构图基础", "手机永远要平（水平线平行地面）；脚永远在九宫格这条线以下才显腿长；人放在区域内、上方留白，为后期裁剪留空间。"),
            ("00:40→00:59", "技巧二：人多用长焦", "先退后五步，再用长焦放大；让摄影师微微蹲下仰拍，基本完全避开人群，还能把远处山和建筑拉到眼前。"),
            ("00:59→00:96", "技巧三：姿势不超三秒", "同一姿势不要超过三秒，不断重复动作，即使简单的比耶也能生动；华为 Pura90 Pro Max 的 X-MAGE 智拍还能按场景推荐姿势、一键构图。"),
            ("00:96→01:29", "技巧四：横屏拍视频", "遇到转瞬即逝的风景，用横屏无脑拍视频，再挑出最好看的三帧拼成长图，电影感、氛围感、故事感同时拥有。"),
        ],
        "takeaway": "旅游高效出片四技巧：手机端平、长焦避人群、姿势多变化、视频里挑帧。技巧之外，旅程的愉快经历和融洽氛围，才是照片背后真正值得留下的东西。",
        "chapters": [
            {
                "id": "ch1", "time": "00:00-00:40", "title": "技巧一：打好构图基础",
                "paras": [
                    "视频以「马上出去旅游，真想拍点人生照片」的真实诉求开场，但假期人多、出片慢是共同的痛点。「那我教你四个技巧，只要学会了，就能在旅游中高效出片。」",
                    "第一点，「务必打好以下基础，出片率立刻提升 90%」。首先是「手机永远要平」，即屏幕上的水平线要平行于地面；「可以转动手机，但永远是这样转，而不是这样转」——转的方向有讲究。其次是「脚永远在九宫格这条线以下，才会显得腿更长」。最后是「人永远放在这个区域内，上方要留白」，这样不仅直出好看，还能为后期裁剪提供更多空间。",
                ],
                "figs": [1, 2, 3],
            },
            {
                "id": "ch2", "time": "00:40-00:59", "title": "技巧二：人太多，用长焦",
                "paras": [
                    "「人太多，用长焦。」第二点的操作非常具体：「先退后五步，再用长焦放大，再让你的摄影师微微蹲下仰拍，就能基本完全避开人群，留下最干净的画面。」",
                    "长焦的另一个价值是拉近远景：「长焦还很适合跟远处的景点合拍，远处的山啊、建筑，就能够立刻被拉到眼前。」",
                ],
                "figs": [4, 5],
            },
            {
                "id": "ch3", "time": "00:59-00:96", "title": "技巧三：姿势不超过三秒",
                "paras": [
                    "「同一个姿势，不要超过三秒。用一个动作超过三秒钟，就会变得尴尬。」第三点是关于动态：「要不断的重复这个动作，这样呢，即使是简单的比耶，也能很生动。」",
                    "视频还展示了华为 Pura90 Pro Max 的 X-MAGE 智拍功能：「它可以根据场合、道具和人物智能识别，为你推荐当下最合适的姿势。有它当你的随身 Pose 机，再也不怕姿势尴尬。」它还能「智能识别身边场景，为我们一键构图、推荐合适的个性色卡，即使让路人帮拍，也能轻松拍出好看的照片。」",
                ],
                "figs": [6, 7, 8],
            },
            {
                "id": "ch4", "time": "00:96-01:29", "title": "技巧四：横屏无脑拍视频",
                "paras": [
                    "「在里头呢，我们常会遇到很多转瞬即逝的风景，来不及多说了。」第四点最省力：「我们直接用横屏无脑拍视频。」",
                    "「最后只需要在这些视频里调出最好看的那三帧，拼成长图——电影感、氛围感、故事感，同时拥有。不再浪费时间在打卡照上，因为每一帧都是最后的出片素材。」",
                    "结尾回归初心：「最后最重要的是，旅程不只有出片。愉快的经历、融洽的氛围、眼中的风景，是这些才使这些旅途更加美好。」",
                ],
                "figs": [9, 10],
            },
        ],
    },
    "harmony-shooting": {
        "title": "这样拍，更和谐～",
        "title_display": "审美的第一课：帮相机找到那颗黄豆",
        "duration": "1:43",
        "tags": "摄影 审美 构图 思想",
        "url": "http://xhslink.cn/o/2k1fCkClN7q",
        "intro": "一支 1 分 43 秒的审美启蒙课：用「红豆配黄豆」的比喻，讲清摄影构图的底层逻辑。人天生会看最突出的事物，而相机不会——所以拍照的第一步，是帮相机找到那颗「黄豆」。从拍照延伸到穿搭、化妆、海报设计，最后落脚到基本功的重要性。",
        "summary_rows": [
            ("00:00→00:25", "开场比喻", "红豆这么多，你却总是看那颗黄豆——能轻易看到最突出的事物，就是你天生就有的审美。"),
            ("00:25→00:42", "构图原理", "一个画面只有红豆就没有重点，观众不知道该看哪里；黄豆太多又杂乱，不知道该看谁；只有一颗黄豆，既有重点又舒服。"),
            ("00:42→00:65", "拍照应用", "明明很美的风景拍出来很丑，因为眼睛会找黄豆而相机不会——第一步就是帮相机找到那颗黄豆。"),
            ("00:65→00:84", "生活延伸", "生活处处有黄豆：穿搭、化妆、海报设计，都需要一个突出的重点。"),
            ("00:84→01:43", "总结升华", "只有先能拍好一颗黄豆，才可能拍好更多颗黄豆。创造的自由，建立在扎实的基本功上。"),
        ],
        "takeaway": "审美的第一课是「找黄豆」：画面里要有一个让观众视线落脚的重点。先帮相机找到那一颗黄豆，再谈更多更宏大的构图。",
        "chapters": [
            {
                "id": "ch1", "time": "00:00-00:25", "title": "你天生就有审美",
                "paras": [
                    "视频从一个自我怀疑开始：「怎么办，我总觉得我审美太差了。」对方的回应出人意料：「你信吗？其实你天生就有审美。」",
                    "他用一个现场实验证明：「比如此刻，你在看什么？嗯，这颗黄豆啊。」画面里红豆很多，黄豆只有一颗，「可你看的却总是这颗黄豆」。「能轻易看到最突出的事物，这不就是你天生就有的审美吗？」",
                ],
                "figs": [1, 2],
            },
            {
                "id": "ch2", "time": "00:25-00:42", "title": "找黄豆：审美的第一课",
                "paras": [
                    "「来，今天讲审美的第一课：找黄豆。」主讲人给出三种画面的对比。「一个画面如果只有红豆，就没有重点，观众不知道该看哪里。」「而黄豆太多呢，又变得很杂乱，观众不知道该看谁。」",
                    "「那如果只有一颗黄豆呢？既有重点又很舒服，对吧。」红豆象征背景、黄豆象征焦点——一颗黄豆，就是画面里的视觉重心。",
                ],
                "figs": [3, 4, 5],
            },
            {
                "id": "ch3", "time": "00:42-00:65", "title": "为什么好风景拍出来很丑",
                "paras": [
                    "「比如拍照。为什么明明很美的风景，但拍出来就很丑？」主讲人给出解释：「是因为你的眼睛会找黄豆，但相机不会。它只是一台机器，它不懂美，于是只能把它看到的一切全拍进去。」",
                    "「所以我们要做的第一步，就是帮相机找到那颗黄豆。」拍摄前先想清楚画面里的焦点在哪——这就是把「眼睛里的美」翻译给相机的过程。",
                ],
                "figs": [6, 7],
            },
            {
                "id": "ch4", "time": "00:65-00:84", "title": "生活处处有黄豆",
                "paras": [
                    "「而且不止拍照，生活其实处处有黄豆。」主讲人把概念延伸到穿搭、化妆、海报设计——每一处都有一个「让视线落脚」的重点。一个造型需要一个亮点，一张海报需要一行主标题，道理相通。",
                ],
                "figs": [8, 9],
            },
            {
                "id": "ch5", "time": "00:84-01:43", "title": "先拍好一颗黄豆",
                "paras": [
                    "「那我如果不想只拍一颗黄豆呢？拍多了也太无聊了。」面对想拍「更宏大、更复杂世界」的想法，主讲人提醒：「只有先能拍好一颗黄豆，你才有可能能拍好更多颗黄豆。」",
                    "结尾是一句意味深长的总结：「创造的自由，建立在扎实的基本功上。这些以后我慢慢跟你讲。」审美没有捷径，先掌握最基础的「找黄豆」，才有资格谈复杂构图。",
                ],
                "figs": [10, 11],
            },
        ],
    },
    "light-and-shadow": {
        "title": "找光是为了看清楚，那影呢？",
        "title_display": "让照片变乱的不是杂物，是灯",
        "duration": "1:33",
        "tags": "摄影 灯光 光影 氛围",
        "url": "http://xhslink.cn/o/cOwg6z2hk0",
        "intro": "一支 1 分 33 秒的光影课：精心布置的场景拍出来还是乱，问题不在杂物，而在那盏直射大灯。大灯均匀照亮一切，也让影子全部消失；换成氛围小灯，影回来吞没多余细节，画面就有了主次。视频还把原理延伸到修图：用黑色吞没不要的细节，可以拯救手机里的废片。",
        "summary_rows": [
            ("00:00→00:07", "问题提出", "精心布置了半天，拍出来还是乱乱的——问题出在灯。"),
            ("00:07→00:33", "换灯对比", "关掉直射大灯、换成两个氛围小灯，画面立刻好多了。大灯均匀照亮每一样东西，同时让影子全部消失。"),
            ("00:33→00:58", "影子作用", "需要让影去吞没多余的细节，有光的地方才格外突出。照片看着乱，不是因为环境乱，而是因为光太匀、没有主次。"),
            ("00:58→01:33", "延伸应用", "很多电影场景看似打乱却一点也不显脏、很耐看。手机里的废片也可以在修图时通过重塑光影拯救，甚至把不要的细节涂成纯黑色。"),
        ],
        "takeaway": "照片乱不是杂物多，而是光太匀导致没有主次。让影子去吞没多余细节，光所及之处才格外突出——这一原理既适用于布灯，也适用于修图。",
        "chapters": [
            {
                "id": "ch1", "time": "00:00-00:07", "title": "精心布置，还是乱",
                "paras": [
                    "视频开头，一位主角情绪低落：「你看，我精心布置了半天，可为啥拍出来还是乱乱的？」另一位没有急着安慰，而是让他先看一样东西：「可能是因为……它。」",
                ],
                "figs": [1],
            },
            {
                "id": "ch2", "time": "00:07-00:33", "title": "关掉大灯，换小灯",
                "paras": [
                    "「你看，我们关掉这盏大灯，换成两个更有氛围的小灯。」镜头切到改造后的画面，「哎，这就好多了。」",
                    "原理随即点破：「因为让照片乱的，也许从来都不是你扔掉的那些垃圾，而是这盏灯。一盏直直照射下来的大灯，能均匀地照亮每一样东西，但同时它也让影子全部消失。」均匀的光消灭了影子，也就消灭了画面的层次与主次。",
                ],
                "figs": [2, 3, 4],
            },
            {
                "id": "ch3", "time": "00:33-00:58", "title": "用影去吞没细节",
                "paras": [
                    "「可往往呢，我们需要用影去吞没多余的细节，这样，那些有光的地方才会格外突出。」小灯的光影让桌面形成明暗分区，杂物被影子的暗部吞掉，视觉自然聚焦在受光的区域。",
                    "「所以有些照片看着乱，不是因为环境乱，而是因为光太匀了，所以显得没有主次。」这句点题直接颠覆了「乱=东西多」的直觉。",
                ],
                "figs": [5, 6],
            },
            {
                "id": "ch4", "time": "00:58-01:33", "title": "电影为何耐看，废片如何拯救",
                "paras": [
                    "「没错，这也是很多电影场景看似打乱、却一点也不显脏、反而很耐看的原因。」主讲人把原理从布景延伸到电影美学——耐看的画面不是没有杂物，而是光替它做好了取舍。",
                    "「那换个思路，我们手机里存的很多废片，也可以在修图时通过重塑光影来拯救。」既然黑色的影子有吞没细节的功能，「那我要是干脆把不要的细节都涂成纯黑色呢？」——把布光思维搬到修图软件里，废片也能焕然一新。",
                ],
                "figs": [7, 8, 9, 10],
            },
        ],
    },
    "curve-color-grade": {
        "title": "小小曲线调色，拿捏啦🫴！！",
        "title_display": "曲线调色从直方图讲起",
        "duration": "1:44",
        "tags": "摄影 调色 曲线 后期",
        "url": "http://xhslink.cn/o/8KywZvpaNFR",
        "intro": "一支 1 分 44 秒的曲线调色入门课：从一张照片扔进软件得到的直方图讲起，教你看懂暗部亮部、用打点拉曲线提亮天空、用 S 曲线提高对比度；再延伸到四根曲线（亮度 + 红绿蓝），最后演示如何用相反色把偏黄照片调回来。",
        "summary_rows": [
            ("00:00→00:14", "引入直方图", "照片扔进修图软件，会得到一个直方图。"),
            ("00:14→00:37", "读懂直方图", "从左到右分别代表照片从暗到亮。左边面积大说明整体偏暗，靠右面积大则偏亮。"),
            ("00:37→00:59", "曲线操作", "曲线调色基于直方图：想提高天空亮度就把右侧亮部往上拉；想提高对比度就把亮部拉高、暗部拉低，形成 S 形曲线。"),
            ("00:59→00:78", "四根曲线", "曲线调色一共四根：亮度曲线，加上红、绿、蓝三根色彩曲线，可单独控制画面中三个颜色的多少。"),
            ("00:78→01:44", "调色演练", "照片偏黄就往黄色的相反色调——加蓝色，再降低红色，颜色就调过来了。还能控制亮暗部颜色、拯救偏色、还原肤色。"),
        ],
        "takeaway": "曲线调色的基础是看懂直方图：左暗右亮。亮度曲线调明暗（S 曲线加对比度），红绿蓝三根色彩曲线调颜色，相反色相加减即可校准偏色。",
        "chapters": [
            {
                "id": "ch1", "time": "00:00-00:14", "title": "曲线调色是啥",
                "paras": [
                    "视频以常见的困惑开场：「修图软件里这个曲线调色是啥呀？」主讲人回应：「这个功能可好用了，我看好多软件里都有。」",
                    "「来，我教你。」他从一张照片讲起：「这是一张照片，把它扔到修图软件里，我们就会得到一个直方图。」看着复杂的一堆图形，听者想溜：「这个图一看就好复杂，我先走了。」主讲人拦住他：「别跑呀，不难。」",
                ],
                "figs": [1, 2],
            },
            {
                "id": "ch2", "time": "00:14-00:37", "title": "看懂直方图：左暗右亮",
                "paras": [
                    "「其实就是从左到右呢，分别代表着照片从暗到亮。」主讲人用一个直观的例子讲解：「比如你看这个直方图，它左边的面积更大，就说明这个照片整体偏暗。」",
                    "「同样啊，再给你一个直方图，先不给你看照片，你猜它大概是个什么亮度？」听者回答：「靠右的面积大，整体偏亮吧。」「你看这不会了吗？」——读懂直方图的分布，就等于读懂了照片的明暗构成。",
                ],
                "figs": [3, 4],
            },
            {
                "id": "ch3", "time": "00:37-00:59", "title": "打点拉曲线：提亮与对比度",
                "paras": [
                    "「曲线调色其实就是基于这个直方图做调整。」主讲人演示第一个操作：「咱们先在这个直线上打三个点，比如说现在你想提高天空的亮度——天空是照片中的亮部，亮部在直方图的右侧，所以我们要把右侧往上拉一点。」画面中天空随即变亮。",
                    "「那如果你想提高对比度，就把照片的亮部拉高，同时把暗部拉低，形成一个 S 形的曲线。」效果立竿见影，「你看效果明显吧」。",
                ],
                "figs": [5, 6, 7],
            },
            {
                "id": "ch4", "time": "00:59-00:78", "title": "四根曲线：亮度加三色",
                "paras": [
                    "「那曲线能调颜色吗？」「可以啊。」主讲人引出完整体系：「曲线调色一共有四根曲线，刚才讲的是亮度曲线，另外呢，还有三根色彩曲线，分别代表红色、绿色和蓝色。」",
                    "「简单来说呢，它们可以单独地去控制画面当中这三个颜色的多少。刚开始用的时候，看这张图就够了，这是总结版本。」一张色彩关系图，成了入门的全部捷径。",
                ],
                "figs": [8, 9],
            },
            {
                "id": "ch5", "time": "00:78-01:44", "title": "演练：把偏黄的照片调回来",
                "paras": [
                    "「那咱们来演练一下，这张照片不想让它这么黄，怎么办？」主讲人给出调色方向：「应该往黄色的相反色去调，从这个图片上看，我们应该加蓝色。」",
                    "「加蓝色之后画面偏红，我们再去降低红色，颜色就调过来了。」听者感叹「这很方便啊」。「是啊，它还有很多用法，比如分别控制亮部和暗部的颜色、拯救偏色的照片还原肤色，或者这种戏剧性的海报风格。」最后留下一句：「行了，先讲这么多，不懂的再问我。」",
                ],
                "figs": [10],
            },
        ],
    },
    "color-grade-basics": {
        "title": "小小调色，拿捏啦🫴！！",
        "title_display": "调色不是做加法，是做减法",
        "duration": "1:47",
        "tags": "摄影 调色 三原色 原理",
        "url": "http://xhslink.cn/o/7K4F5QCUxGV",
        "intro": "一支 1 分 47 秒的调色原理课：从「夕阳想调更红却越调越怪」的困惑出发，用光学三原色讲清对立色（互补色）的关系。核心是颠覆直觉的一句话——调色不是做加法而是做减法：照片发灰不是颜色不够，而是对立色混进来了，把对立色抽走，你要的颜色自然透出来。最后用「近少远多」教你把世界调成任意颜色。",
        "summary_rows": [
            ("00:00→00:17", "问题演示", "夕阳想调更红，直接把红色拉到最高特别怪异；再把绿色蓝色也拉到最高，反而白了。"),
            ("00:17→00:35", "三原色原理", "光学三原色两两叠加得到三个颜色，共六个互为对立的颜色。神奇的是对立色混在一起反而变成白色。"),
            ("00:35→00:51", "减法原理", "照片发白发灰不显色，不是你想要的颜色不够，而是它的对立色混进来了。调色不是做加法，而是做减法。"),
            ("00:51→00:66", "夕阳应用", "夕阳想更红，其实不是加红色，而是减去它的对立色——青色（蓝和绿混合得到）。比起加红，更重要的是减去蓝和绿。"),
            ("00:66→01:47", "近少远多", "调橙色看距离：离红色最近少减，离蓝色最远多减。明白这一点，就能把世界调成任意想要的颜色，甚至还原被舞台灯干扰的肤色。"),
        ],
        "takeaway": "调色的底层是颜色对立关系：对立色混合变白。所以调色做减法而非加法——照片发灰是混进了对立色，抽走它，目标颜色自然显现；按「近少远多」控制各色增减量。",
        "chapters": [
            {
                "id": "ch1", "time": "00:00-00:17", "title": "越调越怪的红色",
                "paras": [
                    "视频从一个调色困境开始：「我想把这个夕阳调得更红，可是调完红色咋这么怪啊？」",
                    "「那我给你看个神奇的。」主讲人现场演示：「我们直接把红色拉到最高——特别怪异，对吧？但这个时候我们把绿色和蓝色也拉到最高——啊，怎么反而白了？」这个反直觉的现象，正是整堂课的引子。",
                ],
                "figs": [1, 2],
            },
            {
                "id": "ch2", "time": "00:17-00:35", "title": "光学三原色与对立色",
                "paras": [
                    "「来，今天我给你讲讲调色原理。这是光学三原色，把它们两两叠加，我们又得到了三个颜色。」听者嫌复杂：「你别闹了，我就想调个图，这也太复杂了。」",
                    "「哎，不难。你看，其实不就是六个互为对立的颜色吗？」主讲人把图简化，「神奇之处在于，当对立色混在一块的时候，反而变成了白色。」三对颜色：红对青、绿对品红、蓝对黄——对立色混合，彼此抵消归于白。",
                ],
                "figs": [3, 4, 5],
            },
            {
                "id": "ch3", "time": "00:35-00:51", "title": "调色是做减法",
                "paras": [
                    "「这代表啥？」主讲人讲透关键：「有的时候我们的照片发白发灰不显色，并不是因为你想要的那种颜色不够多，而是它的对立色混进来了。」",
                    "「把这个对立色抽走，你要的颜色自然而然就会透出来。意思就是，调色不是做加法，而是做减法。」一句话颠覆了「颜色不够就加颜色」的直觉。",
                ],
                "figs": [6, 7],
            },
            {
                "id": "ch4", "time": "00:51-00:66", "title": "夕阳更红：减去蓝和绿",
                "paras": [
                    "「比如我想把夕阳调得更红，其实不是要加红色，而是要减去它的对立色。」「红色的对立色是青色，而青色是蓝和绿混合得到的。」",
                    "「所以比起加红，更重要的是减去蓝和绿。」听者夸「聪明」——看似是在增加红色，真正的做法反而是把混进来的蓝绿抽掉，让红自己透出来。",
                ],
                "figs": [8, 9],
            },
            {
                "id": "ch5", "time": "00:66-01:47", "title": "近少远多：调出任意颜色",
                "paras": [
                    "「哎，可是如果我想调的是橙色，而不是那种纯红的颜色呢？」「好问题，就看距离。你看这张图——橙色离红色最近，离绿色稍微远点，离蓝色最远。」",
                    "「你就记住：近少远多。」主讲人给出实操：「比如你想调橙色，咱们就以橙色为原点，把离得最近的红色稍微减去一点点，绿色稍远就多减去一点，而蓝色最远，减去的最多。这样调出来就是橙色。」",
                    "「明白了这一点，你就可以把世界调成任意一种你想要的颜色，甚至可以还原被舞台灯干扰的肤色、把照片调成电影海报。」收尾依旧轻松：「好，今天先讲这么多，不懂的再问我。」",
                ],
                "figs": [10, 11],
            },
        ],
    },
    "photo-clarity": {
        "title": "照片通透是由什么决定的呢？通透只需两点",
        "title_display": "照片通透只需两点：去灰 + 颜色干净",
        "duration": "0:36",
        "tags": "摄影 调色 通透 后期",
        "url": "http://xhslink.cn/o/3bZGd47sE3f",
        "intro": "一支 36 秒的极简调色课：一句话点透「照片通透」的本质——去灰、颜色干净。先看直方图：缺少暗部和亮部、信息集中在灰部就会不通透，压暗暗部、增亮亮部即可解决；再讲第二种情况：信息集中在暗部画面显脏，是颜色不够纯，需要在可选颜色中调中性色，水面脏就加青和蓝。",
        "summary_rows": [
            ("00:00→00:05", "点出本质", "通透的本质就两点：一去灰，二颜色干净。"),
            ("00:05→00:14", "去灰操作", "直方图缺少暗部和亮部、信息集中在灰部，看起来就不通透。压暗暗部、增亮亮部，画面就通透了。"),
            ("00:14→00:36", "颜色修正", "换个场景用同样办法还显脏，是信息集中在暗部、颜色不够纯。在可选颜色中不调红色而调中性色，灰就变干净；水面脏就选中性色加青色和邻近色蓝色。"),
        ],
        "takeaway": "照片通透只两点：去灰（压暗增亮拉开直方图两端）和颜色干净（在可选颜色中修中性色）。遇到画面显脏，先查直方图信息集中在哪，再对症调整。",
        "chapters": [
            {
                "id": "ch1", "time": "00:00-00:05", "title": "通透的本质就两点",
                "paras": [
                    "「怎么让照片变通透？」视频直接给出答案：「通透的本质就两点：一，去灰；二，颜色干净。」36 秒的篇幅，围绕这两个词展开，没有多余的铺垫。",
                ],
                "figs": [1],
            },
            {
                "id": "ch2", "time": "00:05-00:14", "title": "去灰：拉开直方图两端",
                "paras": [
                    "「聪明的你会发现，照片的直方图缺少暗部和亮部，信息主要集中在灰部，所以看起来不通透。」直方图的两端（纯黑、纯白）没有信息，中间堆满灰——画面自然发闷。",
                    "「只需要压暗暗部、增亮亮部，画面就通透了。」把灰部的信息向两端推开，对比度随之建立，通透感立刻出现。",
                ],
                "figs": [2, 3],
            },
            {
                "id": "ch3", "time": "00:14-00:36", "title": "颜色干净：修中性色",
                "paras": [
                    "「但是当我换个场景，用同样的办法，发现照片看起来还是显脏。」同样的压暗增亮，这次失灵了。「这个时候看直方图可以发现，信息主要集中在暗部，所以画面脏。」",
                    "「还有可能是颜色不够纯。」主讲人给出第二种解法：「在可选颜色中，不是调红色，而是中性色——也就是灰色加夕阳的红，和邻近色黄色，颜色中的灰就变干净了。」",
                    "「同理，水面颜色脏，选择中性色加青色和邻近色蓝色，颜色就变纯了，画面也就干净了。」一个场景对应一组中性色修正，通透感的第二块拼图就此补全。",
                ],
                "figs": [4, 5, 6],
            },
        ],
    },
}


def build_transcript(slug: str) -> str:
    audio = SLUG_TO_AUDIO[slug]
    whisper = json.loads((ROOT / f"{audio}.json").read_text(encoding="utf-8"))
    terms_path = ROOT / f"terms-{slug}.json"
    replacements: dict[str, str] = {}
    if terms_path.exists():
        terms = json.loads(terms_path.read_text(encoding="utf-8"))["terms"]
        for t in terms:
            if t.get("adopted"):
                corr = t.get("correct")
                if corr and corr != "无法确认" and corr != t.get("original"):
                    replacements[to_simplified(t["original"])] = to_simplified(corr)
    rows = []
    for seg in whisper.get("segments", []):
        text = (seg.get("text") or "").strip()
        if not text:
            continue
        text = to_simplified(text)
        for orig, corr in replacements.items():
            text = text.replace(orig, corr)
        rows.append(
            f'<div class="transcript-row"><time>{fmt(seg["start"])}</time>'
            f"<p>{text}</p></div>"
        )
    return "\n".join(rows)


def build_html(slug: str) -> str:
    d = DATA[slug]
    shots = json.loads((ROOT / f"shots-{slug}.json").read_text(encoding="utf-8"))["shots"]
    # 截图编号 -> scene 描述
    fig_desc: dict[int, str] = {}
    for s in shots:
        fig_desc[int(s["file"].replace("shot-", "").replace(".jpg", ""))] = s["scene"]

    transcript = build_transcript(slug)
    n_seg = transcript.count("transcript-row")

    summary_rows = "\n".join(
        f'<div class="summary-row"><span class="time-marker">[{tr}]</span>'
        f"<div><strong>{label}</strong><p>{txt}</p></div></div>"
        for tr, label, txt in d["summary_rows"]
    )

    # 章节渲染：每个章节生成 h2 + 段落 + 配图
    toc_links = "".join(
        f'<a href="#{c["id"]}">{c["title"]}</a>' for c in d.get("chapters", [])
    )
    toc_links += '<a href="#transcript">完整转录</a>'

    story = []
    for c in d.get("chapters", []):
        paras = "".join(f"<p>{p}</p>" for p in c["paras"])
        figs = ""
        for num in c.get("figs", []):
            desc = fig_desc.get(num, "")
            badge = ""
            for s in shots:
                if s["file"] == f"shot-{num:02d}.jpg":
                    badge = s.get("time", "")
                    break
            figs += f'<figure><img src="assets/{slug}/shot-{num:02d}.jpg" alt="{desc}" loading="lazy"><figcaption><span class="time-badge">[{badge}]</span>{desc}</figcaption></figure>'
        story.append(
            f'<section class="story-section" id="{c["id"]}">'
            f'<h2><span class="time-marker">{c["time"]}</span>{c["title"]}</h2>{paras}{figs}'
            f"</section>"
        )
    story_html = "\n".join(story)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="{d['intro'][:140]}">
<title>{d['title']}｜图文实录</title>
<style>*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}
body{{margin:0;font-family:"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.8;color:#292524;background:#fafaf9}}
.container{{width:min(960px,100%);margin:0 auto;padding:48px 32px 80px}}header{{margin-bottom:40px}}
header h1{{font-size:32px;font-weight:900;color:#1c1917;margin:0 0 12px;line-height:1.3}}
.meta-row{{display:flex;gap:16px;flex-wrap:wrap;align-items:center;margin-bottom:16px}}
.meta-tag{{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600}}
.tag-platform{{background:#ff2442;color:#fff}}.tag-duration{{background:#f1f5f9;color:#64748b}}.tag-topic{{background:#dbeafe;color:#1e40af}}
.source-link{{color:#3b82f6;font-size:14px;text-decoration:none}}.source-link:hover{{text-decoration:underline}}
.toc{{background:#fff;border-radius:16px;padding:20px 24px;margin-bottom:32px;box-shadow:0 2px 12px rgba(0,0,0,.04)}}
.toc h3{{font-size:16px;color:#1e40af;margin:0 0 12px}}.toc a{{display:block;color:#475569;font-size:14px;text-decoration:none;padding:4px 0;border-bottom:1px solid #f1f5f9}}.toc a:hover{{color:#3b82f6}}
.documentary{{font-size:17px}}.story-section{{margin:48px 0}}
.story-section h2{{font-size:24px;font-weight:700;color:#1c1917;margin:0 0 16px;padding-bottom:8px;border-bottom:2px solid #e7e5e4}}
.story-section p{{margin:0 0 14px;color:#44403c}}
.time-marker{{display:inline-block;padding:2px 8px;background:#fef3c7;border-radius:6px;font-size:13px;font-weight:700;color:#b45309;margin-right:6px;font-variant-numeric:tabular-nums}}
.quote-block{{background:#f0fdf4;border-left:4px solid #10b981;padding:12px 16px;border-radius:8px;margin:14px 0;font-size:15px;color:#166534;font-style:italic}}
img{{display:block;max-width:100%;height:auto}}figure{{margin:28px 0;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(41,37,36,.1)}}
figcaption{{padding:14px 18px;color:#57534e;font-size:14px}}figcaption .time-badge{{font-weight:700;color:#b45309;margin-right:6px}}
.transcript-section{{margin-top:48px}}.transcript-section h2{{font-size:24px;font-weight:700;color:#1c1917}}
.transcript-note{{font-size:14px;color:#78716c;margin-bottom:24px}}.transcript-list{{list-style:none;padding:0}}
.transcript-row{{display:grid;grid-template-columns:72px 1fr;gap:16px;padding:14px 0;border-bottom:1px solid #e7e5e4}}
.transcript-row time{{font-variant-numeric:tabular-nums;color:#b45309;font-weight:700}}.transcript-row p{{margin:0}}
@media(max-width:640px){{.container{{padding:28px 18px 56px}}header h1{{font-size:24px}}.transcript-row{{grid-template-columns:56px 1fr;gap:10px}}}}
.transcript-collapsible{{border:none;margin:0;padding:0}}.transcript-collapsible summary{{display:flex;align-items:center;gap:10px;cursor:pointer;list-style:none;user-select:none;font-size:24px;font-weight:700;color:#1c1917;margin:0;padding-bottom:8px;border-bottom:2px solid #e7e5e4}}
.transcript-collapsible summary::-webkit-details-marker,.transcript-collapsible summary::marker{{display:none}}
.transcript-collapsible summary::before{{content:"▶";font-size:12px;color:#b45309;transition:transform .2s;flex-shrink:0}}
.transcript-collapsible[open] summary::before{{transform:rotate(90deg)}}.transcript-collapsible[open] summary{{margin-bottom:16px}}.transcript-collapsible .transcript-body{{margin-top:0}}
.summary-row{{display:flex;gap:12px;padding:16px 20px;background:#fff;border-radius:12px;margin-bottom:12px;box-shadow:0 2px 12px rgba(0,0,0,.04);align-items:flex-start}}
.summary-row .time-marker{{flex-shrink:0;margin-top:2px}}
.summary-row strong{{display:block;font-size:16px;color:#1c1917;margin-bottom:4px}}
.summary-row p{{color:#57534e;margin:0;font-size:15px}}
.takeaway-box{{background:#eff6ff;border-left:4px solid #3b82f6;border-radius:12px;padding:16px 20px;margin-top:20px}}
.takeaway-box strong{{display:block;font-size:16px;color:#1e40af;margin-bottom:6px}}
.takeaway-box p{{color:#3b82f6;margin:0;font-size:15px}}
.content-points h2{{font-size:24px;font-weight:700;color:#1c1917;margin:0 0 14px;padding-bottom:8px;border-bottom:2px solid #e7e5e4}}
.content-points h3{{font-size:20px;font-weight:700;color:#1c1917;margin:22px 0 14px}}
</style>
</head>
<body><main class="container">
<header><h1>{d['title_display']}</h1>
<div class="meta-row"><span class="meta-tag tag-platform">小红书</span><span class="meta-tag tag-duration">{d['duration']}</span><span class="meta-tag tag-topic">{d['tags']}</span></div>
<a class="source-link" href="{d['url']}" target="_blank" rel="noopener">→ 原视频链接</a></header>
<nav class="toc"><h3>内容导航</h3>
{toc_links}</nav>
<article class="documentary"><div class="content-points"><h2>内容要点</h2><p>{d['intro']}</p><h3>知识结构</h3>
{summary_rows}
<div class="takeaway-box"><strong>总结</strong><p>{d['takeaway']}</p></div></div>
{story_html}
<section class="transcript-section" id="transcript"><details class="transcript-collapsible"><summary>完整转录（{n_seg}段）</summary>
<div class="transcript-body"><p class="transcript-note">以下文本由 Whisper medium 模型自动转录，可能存在少量识别误差，已尽可能修正。</p>
<div class="transcript-list">
{transcript}
</div></div></details></section>
</article>
</main>
</body></html>
"""


def generate(slug: str) -> None:
    html = build_html(slug)
    out = DOCS / f"{slug}-图文实录.html"
    out.write_text(html, encoding="utf-8")
    print(f"✓ {slug}: {out.name} 生成")


if __name__ == "__main__":
    args = sys.argv[1:]
    for s in args or list(DATA.keys()):
        generate(s)
    print("完成")
