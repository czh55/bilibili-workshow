#!/usr/bin/env python3
"""b45：向 translations.json 追加 9 个视频的图注英文翻译（幂等）。"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATH = ROOT / "translations.json"

NEW = {
    # ===== mask-tutorial =====
    "演示一张照片，指出不想要天空时需要把天空擦掉": "A photo is shown, noting that if you don't want the sky, you erase it away.",
    "讲解蒙版相当于给照片叠加一块板子，可控制显示与隐藏": "A mask is like layering a board over the photo, controlling what shows and what hides.",
    "在白板上演示「想显示哪儿涂白、想隐藏哪儿涂黑」": "Demonstrating on the board: paint white where you want to show, black where you want to hide.",
    "展示换天效果：用蒙版把新天空替换到照片上": "Showing a sky-replacement result: a mask swaps a new sky onto the photo.",
    "背景正常但人脸太暗的照片，直接调亮度会让整个画面变亮": "A photo with a normal background but a too-dark face; brightening directly lights up the whole frame.",
    "在亮度涂层上添加蒙版，只把脸部涂白、其余涂黑": "Adding a mask on the brightness layer, painting only the face white and the rest black.",
    "展示一段视频，提问它是如何做到的": "A video clip is shown, asking how the effect was made.",
    "分析视频画面，随电线杆边界逐渐隐藏露出下一层": "Analyzing the shot: it gradually hides along the utility pole, revealing the layer beneath.",
    "展示线性蒙版：直线的一边显示、另一边隐藏": "Showing a linear mask: one side of the line shows, the other hides.",
    "总结：蒙版贴合电线杆向左移动即可实现过渡": "Summary: slide the mask left along the pole to complete the transition.",
    # ===== camera-movement-apple =====
    "苹果特写，引出用不同运镜能拍出不同感觉": "An apple close-up introduces how different camera moves create different feelings.",
    "手持镜头追逐苹果，展示甩镜头交代场景": "A handheld shot chases the apple, using a whip pan to reveal the scene.",
    "「摇镜头」：渲染激烈氛围并交代人物关系": "The pan: builds an intense atmosphere and establishes character relationships.",
    "「下降镜头」：画面从全局到主角，是电影开场常用方式": "The crane down: moves from the wide scene to the main character, a classic movie opening.",
    "「上升镜头」：适合作为结尾": "The crane up: works well as an ending.",
    "明亮温馨的厨房环境，衬托故事氛围": "A bright, cozy kitchen setting that supports the story's mood.",
    "「推镜头」：交代环境的同时放大人物情绪": "The push-in: establishes the setting while magnifying the character's emotion.",
    "「拉镜头」：情绪淡化、环境成为重点": "The pull-back: the emotion fades and the setting becomes the focus.",
    # ===== flower-shooting =====
    "准备一个喷壶，把风的形状具象化、用水珠表达花朵鲜嫩": "Prepare a spray bottle to make the wind visible and express freshness with water drops.",
    "多雨春季的朦胧浪漫，取出透明塑料板": "The hazy romance of a rainy spring — take out a transparent plastic sheet.",
    "把水喷到塑料板上，透过塑料板去拍花": "Spray water onto the plastic sheet and shoot the flowers through it.",
    "背景杂乱时采用国画处理方式：平面化、乱中取静": "When the background is messy, use the ink-painting approach: flatten it and find calm within the chaos.",
    "拿出彩色卡纸，模仿画作装裱效果": "Bring out colorful cardstock to mimic a framed artwork.",
    "捡起一地碎花瓣，装进带水的碗中": "Pick up fallen petals and drop them into a bowl of water.",
    "利用 Live 图特性，得到更生动的春天": "Use the Live Photo feature to capture a livelier spring.",
    "用轻盈细孔纱巾，调慢快门拍出梦幻感": "Use a light, fine-mesh scarf with a slow shutter for a dreamy feel.",
    "把纱巾盖在镜头前，显出光的形状": "Drape the scarf over the lens to reveal the shape of the light.",
    "总结：不要错过每一个花期的到来": "Summary: don't miss a single flower season.",
    # ===== travel-shoot =====
    "讲解「手机永远要平」，屏幕水平线要平行于地面": "Explaining to keep the phone level, with the horizon parallel to the ground.",
    "演示转动手机的方向：永远是这样转而不是那样转": "Demonstrating which way to rotate the phone — this way, never that way.",
    "九宫格构图：脚永远在九宫格这条线以下才显腿长": "Rule-of-thirds composition: feet below the bottom line make legs look longer.",
    "「人太多用长焦」：先退后五步再用长焦放大": "Crowded? Use the telephoto: take five steps back, then zoom in.",
    "让摄影师微微蹲下仰拍，完全避开人群": "Have the photographer squat down and shoot from below to avoid the crowd entirely.",
    "演示「一个姿势不要超过三秒」：不断重复动作": "Demonstrating the three-second rule: keep repeating the motion.",
    "华为 Pura90 Pro Max 的 X-MAGE 智拍功能推荐姿势": "Huawei Pura90 Pro Max's X-MAGE smart-shoot feature suggests poses.",
    "X-MAGE 智能识别场景一键构图，路人帮拍也出片": "X-MAGE detects the scene and composes the shot; even a stranger can nail the photo.",
    "遇到转瞬即逝的风景用横屏无脑拍视频": "For fleeting scenery, just shoot landscape video without overthinking.",
    "从视频中调出最好看的三帧拼成长图，电影感氛围感故事感同时拥有": "Pick the three best frames and stitch them into one long image — cinematic, moody, and story-driven at once.",
    # ===== harmony-shooting =====
    "红豆中只有一颗黄豆，人的视线总是看向最突出的黄豆": "One yellow bean among red ones — the eye always lands on the most striking bean.",
    "提问：明明红豆这么多，你看到的却总是那颗黄豆": "Asking: with so many red beans, why do your eyes always land on that yellow one?",
    "「一个画面只有红豆就没有重点」：观众不知道该看哪里": "A frame with only red beans has no focal point — viewers don't know where to look.",
    "「黄豆太多又很杂乱」：观众不知道该看谁": "Too many yellow beans make it cluttered — viewers don't know who to look at.",
    "「只有一颗黄豆」：既有重点又很舒服": "Just one yellow bean: focused and comfortable.",
    "举例拍照：眼睛会找黄豆但相机不会，它把看到的一切全拍进去": "Photo example: your eyes find the focal point, but the camera shoots everything it sees.",
    "第一步就是帮相机找到那颗黄豆": "The first step is helping the camera find that focal point.",
    "生活处处有黄豆：穿搭中也有重点": "Focal points exist everywhere in life — even outfits have one.",
    "化妆、海报设计中同样存在黄豆": "Makeup and poster design have focal points too.",
    "「只有先拍好一颗黄豆，才可能拍好更多颗黄豆」": "Only after mastering one focal point can you master many.",
    "创造的自由建立在扎实的基本功上": "Creative freedom is built on solid fundamentals.",
    # ===== light-and-shadow =====
    "精心布置的场景，拍出来却还是乱乱的": "A carefully styled scene still comes out looking messy.",
    "关闭直直照射下来的大灯": "Turning off the big lamp shining straight down.",
    "换成两个更有氛围的小灯，画面就好多了": "Swap in two cozier accent lights — much better already.",
    "大灯均匀照亮每一样东西，同时让影子全部消失": "The big lamp lights everything evenly but also wipes out every shadow.",
    "需要用影去吞没多余的细节，有光的地方才格外突出": "Shadow is needed to swallow extra details so the lit areas stand out.",
    "对比效果：有影吞没细节后画面更有主次": "The contrast: with shadow swallowing details, the frame gains hierarchy.",
    "很多电影场景看似打乱却一点也不显脏、很耐看": "Many movie scenes look cluttered yet never dirty — they're pleasing to watch.",
    "手机里的废片可以在修图时通过重塑光影来拯救": "Rejected phone photos can be saved in editing by reshaping light and shadow.",
    "既然黑色影子有吞没细节的功能": "Since black shadows can swallow details...",
    "干脆把不要的细节都涂成纯黑色": "Just paint the unwanted details pure black.",
    # ===== curve-color-grade =====
    "把一张照片扔进修图软件": "Drop a photo into the photo editor.",
    "得到一张直方图": "Up pops a histogram.",
    "直方图从左到右代表照片从暗到亮": "The histogram maps dark to bright from left to right.",
    "判断：直方图靠右面积大说明整体偏亮": "Judging: more mass on the right means the photo is brighter overall.",
    "在曲线上打三个点，把右侧（亮部）往上拉提高天空亮度": "Set three points and pull the right side (highlights) up to brighten the sky.",
    "效果演示：天空变亮": "The result: the sky becomes brighter.",
    "提高对比度：亮部拉高暗部拉低形成S形曲线": "Boost contrast: lift highlights, lower shadows, forming an S-shaped curve.",
    "曲线调色共四根：亮度+红绿蓝三根色彩曲线": "There are four curves: brightness plus red, green, and blue.",
    "总结版示意图：色彩曲线控制画面中三色多少": "Summary chart: each color curve controls the amount of its color.",
    "演练：照片偏黄，往黄色相反色调、加蓝色再降红色": "Practice: a yellowish photo — move toward yellow's opposite, add blue, then lower red.",
    # ===== color-grade-basics =====
    "把红色拉到最高，画面特别怪异": "Crank the red all the way up — the shot looks so weird.",
    "再把绿色和蓝色也拉到最高，反而白了": "Max out green and blue too — now it turns white instead.",
    "光学三原色讲解": "Explaining the optical primary colors.",
    "三原色两两叠加得到三个颜色，共六个互为对立的颜色": "Pairing the primaries yields three more colors — six that oppose one another.",
    "对立色混在一块反而变成白色": "Opposing colors mixed together turn white.",
    "照片发白发灰不显色，是它的对立色混进来了": "A washed-out photo means its opposite color has mixed in.",
    "调色不是做加法而是做减法": "Grading is about subtraction, not addition.",
    "夕阳想更红：减去对立色青色（蓝+绿混合得到）": "Want a redder sunset: subtract cyan, its opposite, made from blue plus green.",
    "比起加红更重要的是减去蓝和绿": "More important than adding red is cutting the blue and green.",
    "想调橙色看距离：离红色最近、离蓝色最远": "Want orange? It's about distance: closest to red, farthest from blue.",
    "「近少远多」：以橙色为原点，减红最少、减蓝最多": "Near, less; far, more: from orange's origin, cut red least and blue most.",
    # ===== photo-clarity =====
    "讲解通透的本质：一去灰、二颜色干净": "Explaining the essence of clarity: remove the haze and keep colors clean.",
    "照片直方图缺少暗部和亮部，信息集中在灰部": "The histogram lacks shadows and highlights — data bunches in the midtones.",
    "压暗暗部、增亮亮部，画面就通透了": "Deepen the shadows and lift the highlights — the image becomes clear.",
    "换个场景用同样办法，照片看起来还是显脏": "The same trick in another scene still leaves the photo looking dirty.",
    "可选颜色中不是调红色而是中性色，加夕阳的红和邻近色黄色": "In selective color, adjust the neutrals — not red — adding the sunset's red and adjacent yellow.",
    "水面颜色脏：选择中性色加青色和邻近色蓝色，颜色就变纯了": "Dirty water tones: add cyan and adjacent blue to the neutrals until the colors turn clean.",
}


def main() -> None:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    added = 0
    for zh, en in NEW.items():
        if zh not in data:
            data[zh] = en
            added += 1
    PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    print(f"新增 {added} 条翻译，总条目 {len(data)}")


if __name__ == "__main__":
    main()
