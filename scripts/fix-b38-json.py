#!/usr/bin/env python3
"""b38 补全脚本：为 scene-data 添加 practice/pitfalls/shifts/difficult_words/footer_notes"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "scripts" / "scene-data"

def practice_for(slug):
    P = {
"clothes-wearable-check": [
 ["好看不一定能穿。", "Pretty doesn't mean wearable."],
 ["真丝弹性大易变形。", "Silk is stretchy and deforms."],
 ["收腰款活动量小。", "Fitted tops have little give."],
 ["别只看好看。", "Don't only look at looks."],
],
"clothes-thinking-not-rote": [
 ["看视频觉得会了。", "You feel you've learned it all."],
 ["挑衣服要学思路。", "Learn the logic behind choosing."],
 ["锁边是最基础的。", "Overlocked edges are the basics."],
 ["桑蚕丝是顶级里布。", "Silk is the premium lining."],
],
"clothes-look-cheap-details": [
 ["衣领后的小绳叫挂耳。", "The little loop is a hanger loop."],
 ["细节决定品质。", "Details define quality."],
 ["对齐自然显贵。", "Alignment reads as expensive."],
 ["领贴要有固定线。", "The stay needs a fixing stitch."],
],
"uniqlo-wireless-bra-fit": [
 ["看支撑性设计够不够。", "Check the support structure."],
 ["空杯与杯侧网有关。", "Gapping ties to the side mesh."],
 ["背网轻薄不透痕。", "The back mesh stays invisible."],
 ["杯垫上下固定防移位。", "Pads are locked top and bottom."],
],
"wool-real-fake-check": [
 ["教一招辨别真假。", "One trick to tell real from fake."],
 ["正品写绵羊毛或羊毛。", "Real ones say sheep's wool."],
 ["吊牌看执行标准。", "Check the standard number."],
 ["安全类别必须有。", "The safety class is a must."],
],
"clothes-one-detail-quality": [
 ["袖口斜度影响显瘦。", "Sleeve angle affects slimming."],
 ["双省带看中间缝。", "Check the center seam."],
 ["洗水衣服看拉头。", "Check the pull on washed clothes."],
 ["包好的拉头不变色。", "Protected pulls keep their color."],
],
"cheap-luxury-knitwear": [
 ["首选棉混纺。", "Blends are the first pick."],
 ["莫代尔吸湿排汗好。", "Modal wicks moisture well."],
 ["边缘要做密织。", "Edges need compaction."],
 ["领脚用收针工艺。", "Collars use a gradual decrease."],
],
"clothes-price-quality": [
 ["只谈做工不谈价是耍流氓。", "Talking craft without price is silly."],
 ["领口翘起不要选。", "Skip collars that pop up."],
 ["买前要撑两下试回弹。", "Stretch it to test the rebound."],
 ["选秒回弹的。", "Choose instant snap-back."],
],
"zara-efficient-shopping": [
 ["ZARA分四个档位。", "ZARA has four tiers."],
 ["三角形是入门款。", "A triangle marks entry tier."],
 ["圆圈是质感款。", "A circle marks quality pieces."],
 ["STUDIO是高端线标志。", "STUDIO marks the high-end line."],
],
"weipang-pants-selection": [
 ["裤腿塞裤腿侧面看。", "Fold one leg into the other, view the side."],
 ["大U裆空间更足。", "A U-crotch leaves room."],
 ["面料选软不选硬。", "Choose soft over stiff."],
 ["高腰款显瘦。", "High-rise waists slim."],
],
    }
    return P[slug]

def pitfalls_for(slug):
    P = {
"clothes-wearable-check": [
 ["只看模特上身好看", "考虑自己能不能穿出去", "实穿性决定利用率"],
 ["真丝看起来高级就买", "注意真丝易变形", "弹性大后期必变形"],
 ["BM风短裙跟风买", "前怕走光后怕走光先想", "短裙穿着压力大"],
 ["亚麻收腰款贴身穿", "看活动量和开线风险", "无弹力面料坐下就开线"],
],
"clothes-thinking-not-rote": [
 ["看视频收藏就完事", "到店用思路判断", "死记硬背到店全忘"],
 ["只记某一类衣服技巧", "学判断逻辑举一反三", "思路能迁移到所有衣服"],
 ["不挂里布只看正面", "看侧缝处理工艺", "锁边包边握手缝三档"],
 ["挂里布只看外层面料", "看里布成分", "里布决定舒适与档次"],
],
"clothes-look-cheap-details": [
 ["只看正面样子", "翻看领后挂耳等细节", "细节决定品质观感"],
 ["条纹错位不当事", "选左右对齐的", "错位一眼显廉价"],
 ["领贴尖尖不在乎", "选领贴平整内扣的", "露尖位移破坏领形"],
 ["领贴无固定线也买", "掀开看有没有固定线", "没固定线穿就外翻"],
],
"uniqlo-wireless-bra-fit": [
 ["无钢圈内衣都差不多", "重点看支撑性设计", "支撑不足必空杯跑杯"],
 ["空杯怪自己胸型", "看杯侧网格设计", "网格收拢防空杯"],
 ["只关注罩杯大小", "看侧比张力网收副乳", "张力网支撑决定贴合"],
 ["抬手就卷边不当事", "选压胶设计背网", "压胶防抬手卷边"],
],
"wool-real-fake-check": [
 ["标了羊毛就放心", "看成分是否规范", "加产地支数就是假"],
 ["名字越长越高级", "澳洲羊毛等花哨命名要警惕", "不规范命名按假处理"],
 ["只认品牌不认标准", "认执行标准号", "标准号决定真假"],
 ["忽略安全类别", "认准GB18401-2010", "没标安全类别是次品"],
],
"clothes-one-detail-quality": [
 ["短袖随便买", "看袖口斜度", "斜度大暴露手臂显壮"],
 ["双省带缝不拢无所谓", "选上下闭合的", "张着缝就是返工货"],
 ["洗水衣服只注意颜色", "检查拉头是否包好", "拉头锈旧是洗坏的"],
 ["看不出工艺就看感觉", "用拉头和缝口判断", "细节工艺是品质入口"],
],
"cheap-luxury-knitwear": [
 ["纯棉就买", "选棉混纺", "纯棉排汗差易缩水"],
 ["莫代尔越多越好", "跟棉混纺互补", "纯莫代尔没板型"],
 ["袖口下摆不管", "选密织工艺", "密织防变形"],
 ["穿针织衫老气怪自己", "看领脚收针工艺", "细节工艺决定精致度"],
],
"clothes-price-quality": [
 ["看价格就觉得值", "结合做工判断", "做工差再便宜不值"],
 ["领口翘起看不见", "看领口是否趴在衣架", "翘领上身也翘"],
 ["抽褶堆领显时尚", "夏天避开", "视觉增胖20斤"],
 ["螺纹变形洗洗就好", "买前撑两下试回弹", "回弹差洗几次必变形"],
],
"zara-efficient-shopping": [
 ["在ZARA盲目逛", "先翻领标定档位", "领标秒分四档"],
 ["看到好看就买", "分清入门款质量", "三角标质量一般"],
 ["同一价格都差不多", "认准圆圈质感款", "圆圈款版型做工好"],
 ["高端款犹豫不决", "收完不补看到就买", "STUDIO量少不补货"],
],
"weipang-pants-selection": [
 ["只看模特图", "裤腿塞裤腿看裆部", "裆型暴露卡裆风险"],
 ["牛仔硬挺显型", "微胖避开硬面料", "硬面料显厚重卡裆"],
 ["面料软就行", "软垂弹三个字", "垂弹才不贴肉不勒"],
 ["低腰显腿长", "避入高腰款", "高腰拉长纵向比例"],
],
    }
    return P[slug]

def shifts_for(slug):
    P = {
"clothes-wearable-check": [["只看好看", "考虑实穿性"], ["真丝高级就买", "先想变形风险"], ["设计感堆叠", "款式面料配套"]],
"clothes-thinking-not-rote": [["死记硬背技巧", "学判断思路"], ["只记某一类", "思路举一反三"], ["看正面", "看侧缝和里布"]],
"clothes-look-cheap-details": [["只看正面", "翻细节看品质"], ["条纹错位无所谓", "对齐显贵"], ["领贴外翻将就", "选有固定线"]],
"uniqlo-wireless-bra-fit": [["无钢圈=不贴合", "看支撑设计选"], ["空杯怪胸型", "看杯侧网格"], ["只挑罩杯", "看张力网压胶"]],
"wool-real-fake-check": [["标羊毛就信", "看成分标准"], ["名字越长越高级", "规范命名才真"], ["只看品牌", "认执行标准号"]],
"clothes-one-detail-quality": [["凭感觉挑", "看一个细节"], ["双省带缝口不管", "看是否闭合"], ["洗水衣服只看颜色", "查拉头包好没"]],
"cheap-luxury-knitwear": [["纯棉最安全", "混纺互补更佳"], ["好看就行", "查边缘密织"], ["穿针织老气", "看收针工艺"]],
"clothes-price-quality": [["看价签判断值不值", "结合做工看"], ["领口翘着买", "趴衣架才选"], ["变形洗洗就行", "买前试回弹"]],
"zara-efficient-shopping": [["在ZARA盲逛", "翻领标定档"], ["好看就买", "分清四档质量"], ["高端款犹豫", "收完不补快下手"]],
"weipang-pants-selection": [["只信模特图", "裤腿塞裤腿测裆"], ["硬面料显型", "软垂弹才适合"], ["低腰显腿长", "高腰拉比例"]],
    }
    return P[slug]

def main():
    slugs = ["clothes-wearable-check","clothes-thinking-not-rote","clothes-look-cheap-details","uniqlo-wireless-bra-fit","wool-real-fake-check","clothes-one-detail-quality","cheap-luxury-knitwear","clothes-price-quality","zara-efficient-shopping","weipang-pants-selection"]
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
