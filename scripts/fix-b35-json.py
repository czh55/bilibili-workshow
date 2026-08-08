#!/usr/bin/env python3
"""b35 补全脚本：为 scene-data 添加 practice/pitfalls/shifts/difficult_words/footer_notes"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "scripts" / "scene-data"

def practice_for(slug):
    P = {
"sony-rx1riii-hands-on": [
 ["这台相机在35mm焦段画质顶级，怎么说？", "At 35mm, the quality is class-leading."],
 ["传感器越大进光越多。", "Bigger sensors gather more light."],
 ["裁切到70mm依然可用。", "Cropped to 70mm, it still holds up."],
 ["出门要带三块电池。", "You need three batteries to feel safe."],
],
"desk-product-filming": [
 ["拍上手展示时拉高手机，怎么说？", "Raise the phone when showing the product."],
 ["不要用手机画圈。", "Don't circle the phone around."],
 ["学会翻转产品来拍。", "Learn to flip the product over."],
 ["指点要有节奏。", "Point with rhythm, not randomly."],
],
"cotton-25l-photo-backpack": [
 ["相机装进去自动上锁。", "It locks into place automatically."],
 ["25升不是特别大。", "25 liters isn't a huge size."],
 ["背板是悬浮型的。", "The back panel floats off the pack."],
 ["悬浮背框散热更好。", "The floating frame ventilates better."],
],
"lighting-texture-layers": [
 ["基础照明是空间底色。", "Base lighting is the room's backdrop."],
 ["功能照明精准解决需求。", "Task lighting solves specific needs."],
 ["点位越低光线越柔和。", "Lower light points feel softer."],
 ["高显色光源还原真实颜色。", "High-CRI light renders true colors."],
],
"face-type-midline": [
 ["三停比例约1比1比0.8。", "The thirds are about 1:1:0.8."],
 ["标准脸耐看又不出错。", "A balanced face is pleasant and never off."],
 ["中庭偏长是成熟脸。", "A longer mid-face reads mature."],
 ["看三停比例判断脸型。", "Your thirds reveal your face type."],
],
"lumix-l10-vs-x100": [
 ["传感器越大进光越多。", "Bigger sensors gather more light."],
 ["富士是固定焦段。", "The Fuji is fixed at 35mm."],
 ["高像素可裁切换焦段。", "High resolution allows cropping to other focal lengths."],
 ["Lumix对焦又快又稳。", "The Lumix autofocus is fast and steady."],
],
"feel-not-pretty-reason": [
 ["把嘴抿上测法令纹。", "Press your lips together to test the folds."],
 ["眼睛睁大往上看。", "Open the eyes wide and look up."],
 ["戴眼镜不好看说明山根塌。", "Looking bad in glasses shows a low nasal bridge."],
 ["侧脸比正脸好看是比例问题。", "Better in profile means a proportion issue."],
],
"photo-smile-looks-good": [
 ["让法令纹变得合理。", "Make the folds look intentional."],
 ["用嘴角把苹果肌顶出来。", "Push the cheek apples up with the mouth corners."],
 ["牙齿不能咬紧要分开。", "Keep your teeth apart, not clenched."],
 ["先笑嘴巴再展眼睛。", "Smile first, then open the eyes."],
],
"fangyuan-23-face-angle": [
 ["方圆脸拍照不难。", "Round faces are not hard to shoot."],
 ["录一段视频看自己的真实效果。", "Record a video to see how you really look."],
 ["鼻梁不高别拍纯侧脸。", "A low nose flattens in a pure profile."],
 ["手机垂直于地面拍。", "Keep the phone perpendicular to the ground."],
],
"ai-photo-real-3-tips": [
 ["提示词太干净是主因。", "Overly clean prompts are the culprit."],
 ["提示词加光影描述。", "Add light-and-shadow words to the prompt."],
 ["加轻微瑕疵更真实。", "Minor imperfections add realism."],
 ["前景遮挡让画面更真实。", "Foreground occlusion makes the shot feel real."],
],
    }
    return P[slug]

def pitfalls_for(slug):
    P = {
"sony-rx1riii-hands-on": [
 ["以为固定镜头相机只能拍一个焦段", "利用高像素裁切模拟35-70mm", "裁切后仍保留可用画质"],
 ["忽略续航问题就出门", "出门带三块备用电池", "高画质模式下续航顶不住"],
 ["认为画质旗舰一定要可换镜头", "固定镜头也能达到顶级画质", "这台机器追求体积与画质的极限"],
 ["只看像素不看处理器", "关注BIONZ XR和AI芯片", "性能决定对焦与运行速度"],
],
"desk-product-filming": [
 ["拿着相机原地不动拍", "让镜头有活动感地转动", "画面太死板没有活力"],
 ["拍上手展示时手机拿太低", "拉高手机找画面延伸", "低角度会把产品拍得粗大"],
 ["用手机画圈制造动感", "先放再后推、节奏分明", "画圈很生硬观感差"],
 ["产品平铺着干拍", "翻转产品展示不同面", "翻转能展示更多细节"],
],
"cotton-25l-photo-backpack": [
 ["只看容量不看背负系统", "留意悬浮背板和背长调节", "背负决定长途舒适度"],
 ["以为软腰带就是缺点", "软腰带无硬框架反而灵活", "没有硬框架塑形更适合日常"],
 ["忽略金属框架", "检查框架支撑和底部支撑", "框架决定包体承重"],
 ["买包不看散热", "选悬浮背框设计", "悬浮设计通风散热更好"],
],
"lighting-texture-layers": [
 ["只装主灯就让全屋亮", "用基础光做底色、别过亮", "均匀白光盖过一切质感"],
 ["沙发看书暗就怪主灯", "补一盏落地灯做功能照明", "功能光精准解决局部需求"],
 ["认为氛围灯可有可无", "氛围光是高级感核心", "低点位柔和光才有层次"],
 ["固定一个色温用到底", "选可调色温的灯具", "不同时段需要不同色温"],
],
"face-type-midline": [
 ["只凭感觉说好看不好看", "用三停比例客观判断", "三停比例决定脸型类型"],
 ["认为中庭长就不好看", "中庭长是成熟御姐范", "成熟脸有自己的魅力"],
 ["只看正面判断脸型", "结合上中下庭比例", "三停是量化标准"],
 ["觉得比例好就一劳永逸", "不同比例对应不同风格", "每种脸型都有适配风格"],
],
"lumix-l10-vs-x100": [
 ["只看像素数比较相机", "结合画幅、镜头和处理器", "像素不是画质唯一指标"],
 ["认为定焦就是不方便", "定焦逼你移动构图更走心", "定焦有创作意义"],
 ["忽略对焦差异", "测试连续人像对焦表现", "对焦稳定性差异明显"],
 ["只看硬件不看色彩系统", "比较胶片模拟与实时LUT", "色彩自由度影响后期"],
],
"feel-not-pretty-reason": [
 ["觉得自己丑就否定自己", "先做几个自测动作找原因", "很多「丑」是具体可修的面部特征"],
 ["法令纹深就直接医美", "先测是不是鼻基底凹陷", "对症才能有效改善"],
 ["戴眼镜不好看就换眼镜", "可能是山根塌导致", "山根问题换眼镜也难解决"],
 ["侧脸正脸都无所谓", "对比正侧脸找比例问题", "比例问题可通过角度缓解"],
],
"photo-smile-looks-good": [
 ["拍照不敢露脸怕笑纹", "让法令纹因笑容变得合理", "笑起来法令纹反而好看"],
 ["僵硬的假笑", "用嘴角顶起苹果肌", "苹果肌上提改善内沟法令纹"],
 ["笑的时候咬紧牙关", "牙齿分开、下颌放松", "咬紧会让下巴显短"],
 ["只笑嘴不展眼睛", "先笑嘴巴再展开眼睛", "完整笑容需要眼嘴配合"],
],
"fangyuan-23-face-angle": [
 ["听别人说拍侧脸就拍侧脸", "先录视频找自己真正好看的角度", "每个人的最佳角度都不同"],
 ["左脸不好看就放弃", "左脸抬头就很好看", "换角度激活好看的一面"],
 ["鼻梁不高硬拍纯侧脸", "用2/3侧脸修饰", "2/3侧脸让鼻子不显矮"],
 ["朋友拍仰拍角就低头", "侧脸抬头不看镜头", "仰拍配侧脸抬头更好看"],
],
"ai-photo-real-3-tips": [
 ["以为AI假是模型不行", "先改提示词加光影", "太干净的光是塑料感来源"],
 ["提示词只写高清真实", "具体描述光的方向和明暗", "具体描述才有真实光影"],
 ["追求皮肤完美无瑕", "加轻微瑕疵", "完美皮肤反而塑料感"],
 ["人物直接站背景前", "加前景遮挡和中景虚化", "遮挡关系像真实街拍"],
],
    }
    return P[slug]

def shifts_for(slug):
    P = {
"sony-rx1riii-hands-on": [["认为顶配画质必须可换镜头", "固定镜头也能顶级画质"], ["只看像素", "看处理器与对焦性能"], ["忽略续航", "出门备三块电池"]],
"desk-product-filming": [["原地不动拍", "让镜头有活动感"], ["手机拿太低", "拉高手机找延伸"], ["干拍平铺产品", "翻转产品展示"]],
"cotton-25l-photo-backpack": [["只看容量大小", "看背负系统与散热"], ["忽略背长调节", "按身型调背长"], ["买包只看外型", "检查框架与快装"]],
"lighting-texture-layers": [["一开灯全亮", "分层照明有重点"], ["怪主灯不够亮", "补功能照明"], ["固定色温", "选可调色温"]],
"face-type-midline": [["凭感觉评价颜值", "用三停比例分析"], ["中庭长=丑", "中庭长=成熟御姐"], ["只问好不好看", "问属于哪种脸型"]],
"lumix-l10-vs-x100": [["只看像素对比", "综合画幅镜头处理器"], ["定焦=不方便", "定焦=更有创作意识"], ["只看硬件参数", "比较色彩与对焦体验"]],
"feel-not-pretty-reason": [["觉得自己丑就自卑", "用自测动作找具体原因"], ["法令纹深就焦虑", "先测鼻基底"], ["盲目换眼镜", "先看山根条件"]],
"photo-smile-looks-good": [["怕笑纹不敢笑", "让法令纹因笑变合理"], ["僵硬假笑", "嘴角发力顶苹果肌"], ["咬紧牙关笑", "牙齿分开下颌放松"]],
"fangyuan-23-face-angle": [["听博主说拍侧脸", "自己录视频找角度"], ["拍不好怪搭子", "学会自己找角度"], ["纯侧脸硬拍", "改用2/3侧脸"]],
"ai-photo-real-3-tips": [["AI假怪模型", "先改提示词"], ["只写高清真实", "具体写光影"], ["追求完美皮肤", "加瑕疵加前景"]],
    }
    return P[slug]

def main():
    slugs = ["sony-rx1riii-hands-on","desk-product-filming","cotton-25l-photo-backpack","lighting-texture-layers","face-type-midline","lumix-l10-vs-x100","feel-not-pretty-reason","photo-smile-looks-good","fangyuan-23-face-angle","ai-photo-real-3-tips"]
    for slug in slugs:
        p = OUT / f"{slug}.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        d["practice"] = practice_for(slug)
        d["pitfalls"] = pitfalls_for(slug)
        d["shifts"] = shifts_for(slug)
        words = []
        for s in d["scenes"]:
            for zh, en, note in s["sentences"]:
                w = note.split("（")[0].strip()
                if w and w not in words:
                    words.append(w)
        d["difficult_words"] = words
        d["footer_notes"] = f"来源：{d['meta']['title']}（小红书，时长{d['meta']['duration']}）· 本页为场景英译学习卡，中文逐句来自原视频转录，英文为口语化译写，适合跟读练习。"
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"✓ 补全 {slug}: practice={len(d['practice'])} pitfalls={len(d['pitfalls'])} shifts={len(d['shifts'])} words={len(words)}")

if __name__ == "__main__":
    main()
