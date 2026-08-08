#!/usr/bin/env python3
"""b36 补全脚本：为 scene-data 添加 practice/pitfalls/shifts/difficult_words/footer_notes"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "scripts" / "scene-data"

def practice_for(slug):
    P = {
"facial-stereo-beauty": [
 ["双眼皮不是好看的关键，怎么说？", "Double eyelids aren't what makes you pretty."],
 ["把重点放到眶缘体积。", "Put the focus on the orbital rim."],
 ["鼻梁高度不是核心。", "Nose-bridge height isn't the core."],
 ["口周整体饱满才好看。", "Overall fullness around the mouth reads as pretty."],
],
"color-explained-clearly": [
 ["色彩描述曾长期停留在主观层面。", "Color description was subjective for ages."],
 ["色调决定是什么颜色。", "Hue decides what color it is."],
 ["涂料混合是减色法。", "Paint mixing is subtractive."],
 ["人眼靠三种锥细胞看颜色。", "The eye uses three cones to see color."],
],
"shot-thinking-from-zero": [
 ["把文字语言转化成镜头语言。", "Turn words into camera language."],
 ["先远一点看他在干嘛。", "First shoot wide to see what he's doing."],
 ["让观众自行脑补。", "Let the audience fill in the gaps."],
 ["焦点从人转到衣服。", "Shift focus from person to clothes."],
],
"on-camera-fat-lens": [
 ["显胖不是镜头的错。", "Looking fat isn't the lens's fault."],
 ["距离重塑面部比例。", "Distance reshapes facial proportions."],
 ["压缩不属于任何焦段。", "Compression belongs to no lens."],
 ["答案只有三个字：拍侧脸。", "The answer is three words: shoot the profile."],
],
"sony-a6700-four-features": [
 ["对焦包围自动拍多张。", "Focus bracketing shoots multiple frames."],
 ["增量设到4起步。", "Start with an increment of 4."],
 ["峰值让手动对焦精准。", "Peaking makes manual focus precise."],
 ["创意外观直出电影感。", "Creative Looks give a film look out of camera."],
],
"fangyuan-makeup-frame": [
 ["用后置镜头看清真实的自己。", "The rear camera shows your true face."],
 ["眉毛要画到外轮廓。", "Extend the brow to the outer contour."],
 ["用收缩式腮红。", "Use a contouring blush."],
 ["模糊唇线边界。", "Blur the lip line."],
],
"round-face-angle-tips": [
 ["方圆脸拍照不难。", "Round faces aren't hard to photograph."],
 ["后置把脸拍宽。", "The rear camera widens your face."],
 ["脸平就拍2/3侧脸。", "A flat face looks better at the 2/3 angle."],
 ["舌头抵住上颚。", "Press your tongue to the roof of the mouth."],
],
"square-face-hair-frame": [
 ["头包脸轮廓圆润饱满。", "A hair-wrap gives a round, full outline."],
 ["选窄板的烫发工具。", "Pick a narrow straightener plate."],
 ["顶点在耳尖往上。", "The crown sits above the ear tip."],
 ["冷却后才能定型。", "Let it cool to set the curl."],
],
"joker-film-pull-part1": [
 ["导演是质量第一责任人。", "The director owns the film's quality."],
 ["用特写吊起胃口。", "Close-ups build the suspense."],
 ["未见其人先闻其声。", "Hear the person before seeing them."],
 ["拉片拆解技术细节。", "Break the film down shot by shot."],
],
"native-camera-slim-tips": [
 ["靠着拍别缩着。", "Lean, don't hunch."],
 ["向后打开成三角形。", "Open back into a triangle."],
 ["剪刀手别贴脸。", "Don't press the peace sign to your face."],
 ["记住这四招。", "Remember these four tricks."],
],
    }
    return P[slug]

def pitfalls_for(slug):
    P = {
"facial-stereo-beauty": [
 ["以为好看=单一生理特征", "看眶缘、上颌骨等整体结构", "美是整体结构而非单一五官"],
 ["只关注双眼皮", "先看眼眶骨体积", "眼眶骨决定上半脸立体度"],
 ["把鼻梁高度当核心", "看中面部饱满度", "上颌骨饱满比鼻梁更关键"],
 ["只看局部嘴唇", "看口周整体饱满", "局部细节不如整体协调重要"],
],
"color-explained-clearly": [
 ["以为颜色是物体固有属性", "知道颜色是人眼的感知", "光谱决定反射但感知在人眼"],
 ["把色彩只当直觉经验", "理解三个维度可量化", "色调亮度饱和度是基础框架"],
 ["混用加色减色概念", "分清涂料减色、光加色", "两种体系混合规则不同"],
 ["看完就忘没有抓手", "记住三刺激理论", "三锥细胞原理是色彩科学地基"],
],
"shot-thinking-from-zero": [
 ["想拍大片就先学软件", "先学文字转镜头的分镜", "镜头语言才是短片灵魂"],
 ["以为分镜一定要画出来", "在脑子里完成规划", "分镜思维重于分镜画稿"],
 ["直接拍完整流程", "用放大和还原降低思考成本", "两技巧极大提升拍摄效率"],
 ["每个动作都拍全", "用动作延续让观众脑补", "省略让剪辑更有节奏感"],
],
"on-camera-fat-lens": [
 ["显胖就怪镜头畸变", "理解是距离透视造成的", "畸变不背显胖的锅"],
 ["以为长焦压缩背景", "压缩属于距离而非焦段", "长焦只是放大远景"],
 ["用数码裁切换取焦段", "用光学放大保持画质", "数码裁切放大噪点"],
 ["上镜显胖换镜头", "调整距离改拍侧脸", "拍侧脸比换器材有效"],
],
"sony-a6700-four-features": [
 ["以为对焦包围要手动合成", "机身自动拍序列后期堆叠", "自动拍摄省时省力"],
 ["参数随便设", "增量4、张数9起步", "合理起步参数更容易成功"],
 ["手动对焦全靠手感", "打开峰值对焦显示", "峰值让手动对焦可依赖"],
 ["后期调色才出片", "用创意外观直出", "S3Tone直出电影感"],
],
"fangyuan-makeup-frame": [
 ["用前置自拍判断脸型", "用后置镜头看清真实脸型", "前置会扭曲真实轮廓"],
 ["眉毛画在眉骨正上方", "画到外轮廓中间带弧度", "外轮廓修饰才显脸窄"],
 ["腮红打在苹果肌", "用收缩式腮红修饰外边缘", "收缩色能收缩脸型"],
 ["唇线画得清晰", "模糊唇线边界", "硬唇线把视线引到下半脸"],
],
"round-face-angle-tips": [
 ["只用后置拍照", "换前置自拍显脸小", "后置会放大面部宽度"],
 ["正脸对着镜头", "拍2/3侧脸", "侧脸角度突出骨相"],
 ["头发全部别到耳后", "用头发遮挡一边脸", "遮挡让脸型线条流畅"],
 ["拍照牙关咬紧", "放松下颌、舌头抵上颚", "咬紧会让双下巴明显"],
],
"square-face-hair-frame": [
 ["全头都烫一遍", "只烫该烫的分区", "乱烫反而显头大"],
 ["烫发板越宽越好", "选窄板贴合发根", "窄板更贴合易定型"],
 ["枕骨最扁处也烫", "避开两个骨头区域", "骨头处烫不出蓬松"],
 ["烫完立刻拨弄", "冷却后再定型", "未冷却头发定不住型"],
],
"joker-film-pull-part1": [
 ["以为导演只要喊开始卡", "内容层面还有很多工作", "导演对最终质量全责"],
 ["主角出场就给正脸", "先背影特写吊胃口", "渐进亮相让观众记住角色"],
 ["平铺直叙介绍人物", "先闻其声先见其行", "悬念式引入更抓人"],
 ["骂烂片只图爽", "拆解镜头语言找原因", "基础叙事都没做到才被骂"],
],
"native-camera-slim-tips": [
 ["靠着拍就缩着肩膀", "侧面伸展手肘内扣", "缩着显得虎背熊腰"],
 ["回眸时抱臂", "向后打开成三角形", "前臂横在身前显厚"],
 ["剪刀手贴着脸", "往前伸进对角线", "贴脸显脸大"],
 ["撩头发抱成团", "撑腰挑肩抬起另一手", "打开轮廓才显瘦"],
],
    }
    return P[slug]

def shifts_for(slug):
    P = {
"facial-stereo-beauty": [["以为好看=单一生理特征", "好看=整体结构协调"], ["只盯五官局部", "看眶缘体积与饱满度"], ["迷信鼻梁高度", "看中面部饱满度"]],
"color-explained-clearly": [["颜色靠主观描述", "颜色用三维度量化"], ["混用加色减色", "分清两种混合体系"], ["颜色是物体属性", "颜色是人眼的感知"]],
"shot-thinking-from-zero": [["想拍大片先学软件", "先学文字转镜头"], ["一定要画分镜脚本", "分镜思维在脑内完成"], ["每个动作拍全", "动作延续让观众脑补"]],
"on-camera-fat-lens": [["显胖怪镜头畸变", "看清是距离透视"], ["压缩属于长焦", "压缩属于距离"], ["上镜显胖换器材", "改距离改侧脸"]],
"sony-a6700-four-features": [["用基础模式拍照", "解锁进阶功能提效率"], ["手动对焦靠手感", "峰值对焦可视化"], ["后期才能出片", "创意外观直出"]],
"fangyuan-makeup-frame": [["前置自拍看脸型", "后置看清真实脸型"], ["腮红打苹果肌", "收缩腮红修饰外缘"], ["唇线清晰", "唇线模糊边界"]],
"round-face-angle-tips": [["后置硬拍正脸", "前置自拍找角度"], ["正脸对镜头", "2/3侧脸出骨相"], ["牙关咬紧", "下颌放松"]],
"square-face-hair-frame": [["全头乱烫", "按分区精准烫"], ["脸包头就认命", "头包脸可以烫出来"], ["烫完立刻拨", "冷却后再定型"]],
"joker-film-pull-part1": [["看烂片只骂不拆", "拆镜头语言找原因"], ["主角上来给正脸", "渐进亮相拉悬念"], ["导演只喊开始", "导演对内容全责"]],
"native-camera-slim-tips": [["上镜胖就节食", "用姿势显瘦"], ["缩着靠着拍", "伸展撑开拍"], ["贴脸剪刀手", "往前伸进对角线"]],
    }
    return P[slug]

def main():
    slugs = ["facial-stereo-beauty","color-explained-clearly","shot-thinking-from-zero","on-camera-fat-lens","sony-a6700-four-features","fangyuan-makeup-frame","round-face-angle-tips","square-face-hair-frame","joker-film-pull-part1","native-camera-slim-tips"]
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
