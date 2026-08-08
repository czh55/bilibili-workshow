#!/usr/bin/env python3
"""b37 补全脚本：为 scene-data 添加 practice/pitfalls/shifts/difficult_words/footer_notes"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "scripts" / "scene-data"

def practice_for(slug):
    P = {
"beauty-voiceover-editing": [
 ["拉片是提升剪辑水平最快的方式。", "Breaking down edits is the fastest way to improve."],
 ["开篇要设计一个钩子。", "Open with a clear hook."],
 ["写文案时就要构思剪辑。", "The script pre-plans the edit."],
 ["把握本质效果自来。", "Hold the essence and effects follow."],
],
"travel-telephoto-diff": [
 ["想把背景拍大一些。", "You want the background bigger."],
 ["退到十米开外。", "Back up past ten meters."],
 ["再切到长焦焦段。", "Now switch to the telephoto setting."],
 ["长焦让背景更近。", "Telephoto brings the background closer."],
],
"joker-film-pull-mid": [
 ["导演用画面操控情绪。", "Directors steer emotion through images."],
 ["音效不只是配音。", "Sound is more than dubbing."],
 ["把下一场音效提前。", "Play the next scene's sound early."],
 ["轴线帮观众记住位置。", "The axis helps viewers track positions."],
],
"focal-length-photo-story": [
 ["单张好看组照平淡。", "Each photo is fine, but the set feels flat."],
 ["第一张拍环境。", "First, capture the environment."],
 ["再近一点拍表情。", "Closer still, shoot the expression."],
 ["细节最能勾起回忆。", "Details bring back memories best."],
],
"cinematic-font-free": [
 ["输入文字生成动态字体。", "Type text, get animated fonts."],
 ["用色度抠图去掉底色。", "Key out the background color."],
 ["别只用一个字体。", "Don't settle on one font."],
 ["字体颜色取自主色调。", "Pick the frame's dominant hue."],
],
"winter-fabric-quality": [
 ["德绒靠空气保暖。", "Decron traps air for warmth."],
 ["三种绒本质相同。", "The three fleeces are the same thing."],
 ["抓绒毛短做内衣。", "Short-pile sherpa lines underwear."],
 ["选带防静电处理的。", "Choose anti-static treatments."],
],
"stitch-quality-clothes": [
 ["袖口翻开看里面。", "Flip the cuff and check inside."],
 ["两条明线叫二本针。", "Two lines make double-stitch."],
 ["衬衣三厘米十四五针。", "Shirts run 14-15 stitches per 3cm."],
 ["受力处要套结加固。", "Stress points get bar-tacked."],
],
"hoodie-buying-details": [
 ["本布领口会变形。", "Self-fabric collars stretch out."],
 ["螺纹要弹性好。", "Choose stretchy ribbing."],
 ["领贴条必不可少。", "Neck tape is a must."],
 ["三百到四百克最合适。", "300-400 grams is the sweet spot."],
],
"shirt-buying-details": [
 ["扣眼方向有讲究。", "Buttonholes face different ways."],
 ["领子应该内扣。", "Collars should roll inward."],
 ["贝壳扣天然加分。", "Shell buttons are a natural bonus."],
 ["四对齐是优秀格调。", "Four-way alignment marks quality."],
],
"clothes-avoid-awkward": [
 ["门襟长坐下会鼓包。", "Long flies bunch when you sit."],
 ["里布中间要有线泡。", "Loops between layers hold the lining."],
 ["选接近肤色的内衣。", "Choose skin-toned underwear."],
 ["选平缓弧线的胸省。", "Choose smooth, gentle curves."],
],
    }
    return P[slug]

def pitfalls_for(slug):
    P = {
"beauty-voiceover-editing": [
 ["口播开头直接自我介绍", "先设计钩子留住观众", "钩子决定前几秒的留存率"],
 ["文案和剪辑分开想", "写文案时构思剪辑", "文案即剪辑蓝图"],
 ["账号背书越啰嗦越好", "背书要简洁有双作用", "自我介绍+召唤老粉即可"],
 ["效果堆得越花越好", "把握本质效果自然出", "花字音效可换本质不变"],
],
"travel-telephoto-diff": [
 ["合影往前站挤进画面", "请摄影师往后退", "后退让背景进入画面"],
 ["退一点点就想拍", "退到十米开外", "距离决定背景大小"],
 ["退远后人变小", "切换长焦拉近人物", "长焦保持人物大小放大背景"],
 ["长焦运镜乱晃", "沿平行方向缓慢运镜", "平行运镜才有推进感"],
],
"joker-film-pull-mid": [
 ["以为音效只是配音", "音效可独立制造情绪", "听与视并列非附属"],
 ["情绪爆发靠演员表演", "用声效提前手法", "声音前置预告内心怒火"],
 ["镜头随意切换", "遵守轴线规则", "越轴会让观众混乱"],
 ["看不懂就骂烂片", "拆解视听语言找原因", "画面声音共同传递情绪"],
],
"focal-length-photo-story": [
 ["站一个位置狂按快门", "每张都换焦段视角", "视角单一照片全一样"],
 ["只会拍人物正脸", "远中近加细节四步", "四步公式讲完整故事"],
 ["以为好看要姿势会摆", "每张补充新内容", "有故事的照片不重复"],
 ["出门带一堆镜头", "一个焦段也能拍四步", "手机相机都能做到"],
],
"cinematic-font-free": [
 ["开头用系统默认字体", "用动态字体网站生成", "默认字体没有质感"],
 ["透明底导出失败就放弃", "设黑底白底导出再抠图", "色度抠图一秒去底"],
 ["一种字体用到底", "两个字体混搭", "混搭才有独特性"],
 ["字体颜色随手选", "取画面主色调或互补色", "取色才有一眼层次"],
],
"winter-fabric-quality": [
 ["看名字以为德绒都高级", "注意真德绒已停产", "市面德绒多为概念复用"],
 ["把所有绒当不同东西", "记住抓摇珊瑚是一家", "只是绒毛长短不同"],
 ["只挑最贵的买", "看用途选绒", "内衣选抓绒睡衣选珊瑚绒"],
 ["化纤绒直接买", "选防静电处理", "化纤绒极易起静电"],
],
"stitch-quality-clothes": [
 ["只看正面好看", "翻开袖口看里侧", "内侧线迹暴露品质"],
 ["线头剪掉就行", "看虚线会不会拖线", "虚线后期必拖线"],
 ["以为针数越少越好", "厚料10针薄料14针", "针距跟着面料厚度走"],
 ["忽略内里锁边", "锁边越密实越好", "内里线迹同样重要"],
],
"hoodie-buying-details": [
 ["领口选本布最舒服", "避开本布领口", "本布领穿两次就变形"],
 ["螺纹越粗越耐用", "选氨纶多秒回弹", "回弹性决定变形程度"],
 ["单层帽轻便", "选双层帽立体挺阔", "单层帽软趴无型"],
 ["克重越重越好", "选300-400克", "太重显胖太轻贴身"],
],
"shirt-buying-details": [
 ["所有扣眼同方向", "腰部扣眼横开", "横开抗拉力更强"],
 ["袖口开叉无所谓", "认准宝剑头开叉", "简单包条易变形"],
 ["塑料扣也没关系", "贝壳扣是加分项", "天然贝壳扣更显品质"],
 ["混纺就是廉价", "少量纤维补缺点", "混纺抗皱不牺牲质感"],
],
"clothes-avoid-awkward": [
 ["牛仔裤随便买", "选门襟短的", "门襟长坐下鼓包"],
 ["里布不固定也没事", "选带线泡的里布", "线泡固定里布不乱跑"],
 ["浅色裙不试穿", "透光看一下里布", "无里布浅色全透色"],
 ["胸省越尖越显胸", "选平缓弧线省道", "尖省上身突兀"],
],
    }
    return P[slug]

def shifts_for(slug):
    P = {
"beauty-voiceover-editing": [["口播直接开讲", "先设计钩子留人"], ["文案剪辑分开想", "文案即剪辑蓝图"], ["堆效果", "把握本质"]],
"travel-telephoto-diff": [["合影往前站", "后退十米再长焦"], ["怕退远人变小", "长焦拉近保人放背景"], ["乱晃运镜", "平行缓慢运镜"]],
"joker-film-pull-mid": [["音效只是配音", "音效独立造情绪"], ["情绪靠表演", "声效提前手法"], ["镜头随意切", "遵守轴线"]],
"focal-length-photo-story": [["原地狂按快门", "每张换焦段"], ["只拍正脸", "远中近加细节"], ["照片追求张张精彩", "每张补充新内容"]],
"cinematic-font-free": [["默认字体开场", "动态字体网站"], ["不会抠图就放弃", "黑底导出色度抠图"], ["一种字体", "混搭字体取画面色"]],
"winter-fabric-quality": [["看名字买绒", "看本质和用途"], ["所有绒混为一谈", "分清长短绒"], ["贵就买", "看保暖和静电处理"]],
"stitch-quality-clothes": [["只看正面", "翻内里看针迹"], ["线头随手剪", "看虚线风险"], ["凭手感猜品质", "用针距标准判断"]],
"hoodie-buying-details": [["领口选软的", "选回弹螺纹"], ["单层帽轻便", "双层帽挺阔"], ["克重越重越好", "300-400克刚好"]],
"shirt-buying-details": [["扣眼随便", "腰部横开抗拉"], ["领子歪就扔", "看领口内扣"], ["塑料扣无妨", "贝壳扣加分"]],
"clothes-avoid-awkward": [["买到手才发现尴尬", "买前检查小细节"], ["里布不管", "选带线泡固定"], ["胸省越尖越显胸", "平缓弧线更高级"]],
    }
    return P[slug]

def main():
    slugs = ["beauty-voiceover-editing","travel-telephoto-diff","joker-film-pull-mid","focal-length-photo-story","cinematic-font-free","winter-fabric-quality","stitch-quality-clothes","hoodie-buying-details","shirt-buying-details","clothes-avoid-awkward"]
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
