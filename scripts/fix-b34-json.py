#!/usr/bin/env python3
"""b34 补全脚本：为 scene-data 添加 practice/pitfalls/shifts/difficult_words/footer_notes"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "scripts" / "scene-data"

def practice_for(slug):
    P = {
"original-vs-retouch": [
 ["看到颈部横纹，你要怎么圈选出来？", "Select the neck's horizontal lines to clean them up."],
 ["修图前先整体看一遍画面，用英语怎么说？", "Take an overall look at the shot before you start."],
 ["用笔刷修复肤质，怎么说？", "Use a round brush to repair the skin texture."],
 ["检查轮廓边缘是否干净。", "Check if the outline edges are clean."],
],
"uniqlo-airism-sweat-tips": [
 ["夏天选衣服想避免汗湿尴尬，怎么说？", "Pick summer clothes that avoid sweat stains and odor."],
 ["铜氨纤维又吸湿又排汗，怎么说？", "Cupro fiber absorbs moisture and wicks sweat away."],
 ["这种面料摸起来很丝滑，怎么说？", "This fabric feels cool and silky to the touch."],
 ["纤维自带消臭功能。", "The fiber has built-in deodorizing."],
],
"tight-vs-loose-slim": [
 ["紧身显胖，宽松显瘦，怎么说？", "Tight looks bigger; loose looks slimmer."],
 ["这种面料洗多了会鼓包。", "This fabric puckers after many washes."],
 ["选纱向一致的布料。", "Choose fabric with a consistent grain."],
 ["一出汗它就变得透色。", "Once you sweat, it becomes see-through."],
],
"linen-ramie-hemp-diff": [
 ["亚麻缩水率最高，怎么说？", "Linen shrinks the most of all hemp fabrics."],
 ["苎麻是三种麻里最便宜的。", "Ramie is the cheapest of the three."],
 ["汉麻上身最舒适。", "Hemp is the most comfortable to wear."],
 ["买亚麻衣服要买大不买小。", "Size up rather than down when buying linen."],
],
"clothes-quality-simple": [
 ["判断半裙版型先看臀围，怎么说？", "Judge a skirt by its hip area."],
 ["好版型靠省道撑起来。", "Good fit comes from bust and waist darts."],
 ["下摆久穿也不外翘。", "The hem never flares out even after wear."],
 ["多片结构让腰显得更细。", "Multi-panel construction makes the waist look small."],
],
"bust-size-outfit-tips": [
 ["这种带胸背包容性很小。", "This chest panel leaves little room."],
 ["大胸要选对折量充足的。", "Bigger busts need plenty of ease on both sides."],
 ["小胸穿大胸款是空的。", "A small bust leaves this area empty."],
 ["碎折设计大小胸都能穿。", "Gathered darts work for both bust sizes."],
],
"clothing-luxury-details": [
 ["看到凤尾针就知道衣服不便宜。", "Feather stitching signals a higher price."],
 ["长裙要选斜裁面料。", "Choose bias-cut fabric for long gowns."],
 ["这种面料抗皱性很好。", "This fabric has excellent wrinkle resistance."],
 ["细节决定衣服显不显贵。", "Details are what make clothes look expensive."],
],
"clothing-quality-myths": [
 ["后开衩的堆叠是故意留的放量。", "That fold is deliberately added ease."],
 ["真正的牛角扣纹理都不同。", "Real horn buttons each have a unique grain."],
 ["麻结千万不要剪。", "Never cut the slubs off."],
 ["省道处的格子不对齐是正常的。", "Misalignment at darts is actually correct."],
],
"big-face-bazi-bangs": [
 ["先找到头发露白的地方。", "First find the thin spot."],
 ["把发束往前梳盖住露白。", "Comb it forward to cover the spot."],
 ["刀刃立起来往前划。", "Keep the blade upright and glide forward."],
 ["把发束拉到鼻子定位长度。", "Pull the section down to the nose to set length."],
],
"clothes-quality-details": [
 ["插肩袖最能看出版型好坏。", "Set-in sleeves reveal the pattern quality."],
 ["好版型在肩位捏省。", "Good patterns dart at the shoulder."],
 ["无袖T恤认准内里有贴衬的。", "Look for a lined inner finish on sleeveless tees."],
 ["分辨衣服好坏要细心。", "Judging quality takes a keen eye."],
],
    }
    return P[slug]

def pitfalls_for(slug):
    P = {
"original-vs-retouch": [
 ["看到颈部横纹就直接磨皮整片处理", "只圈选横纹局部、用生成式修补", "局部处理保留肤质，整片磨皮会失真"],
 ["液化时大幅度推动下颌", "液化网格轻推、幅度要小", "大幅度推动会让脸型失真不自然"],
 ["直接修脸不看整体", "先3D模式整体审视画面再动手", "从整体出发才不会顾此失彼"],
 ["跳过边缘检查直接导出", "用「选择并遮住」检查边缘", "边缘不干净会穿帮"],
],
"uniqlo-airism-sweat-tips": [
 ["夏天只追求好看，不看面料", "优先选吸汗速干的面料", "好看但闷汗会带来社交尴尬"],
 ["觉得真丝最好就咬牙买真丝", "性价比选铜氨纤维", "真丝贵且排汗不如铜氨"],
 ["只买最薄的一款", "按场景选经典款、网眼款或棉混款", "不同场景需要不同的厚度与挺阔度"],
 ["内裤只看款式不看工艺", "选压胶无痕工艺", "有走线会勒、会卷边"],
],
"tight-vs-loose-slim": [
 ["认为越紧越显瘦", "宽松版型反而显瘦", "紧身会勾勒赘肉，宽松更有余量"],
 ["看面料只看正面", "检查上下纱向是否一致", "纱向不同水洗后会鼓包"],
 ["小圆领显端庄", "正肩大领型更显瘦", "小圆领露肤度低又显得脖子粗"],
 ["薄如纸的面料显得轻盈", "轻薄但要选不透色的", "一出汗透色非常尴尬"],
],
"linen-ramie-hemp-diff": [
 ["第一次买麻直接买汉麻", "先从亚麻入门", "汉麻最贵，亚麻性价比最高"],
 ["亚麻买正码", "亚麻买大不买小", "亚麻缩水率是所有麻里最高的"],
 ["以为苎麻纤维细就柔软", "苎麻实际最硬挺扎人", "细长纤维反而更硬"],
 ["麻料洗完暴晒", "通风阴干、卷起来存放", "暴晒会损伤纤维、起皱"],
],
"clothes-quality-simple": [
 ["只看前面，不看侧面", "侧面看臀围是否外凸", "侧面的版型问题最多"],
 ["以为平整就是好版型", "看有没有胸省腰省", "人体凹凸不平，没省道就压不住"],
 ["看到松紧腰就当半裙", "腰头松紧一收是腰围放大器", "多片结构才能显腰细"],
 ["觉得越厚越高级", "看缝线颜色是否与面料呼应", "细节呼应才是高级感"],
],
"bust-size-outfit-tips": [
 ["看到喜欢的就买", "先看对折量是否匹配罩杯", "对折量决定能不能穿"],
 ["小胸也硬穿大胸款", "小胸选带碎折的设计", "大胸款小胸穿是空的"],
 ["大胸不敢穿贴身的", "选对折量充足的版型", "充足放量既美观又舒适"],
 ["只看胸围不看结构", "看胸省和背折设计", "结构决定包裹与舒适"],
],
"clothing-luxury-details": [
 ["以为贵的标志是面料厚", "看工艺细节如凤尾针", "工艺复杂度才是显贵关键"],
 ["长裙随意买直裁的", "长裙要选斜裁面料", "斜裁包容性好、垂坠感强"],
 ["看花纹只看颜色", "分辨是否浮雕立体", "立体花纹工艺复杂价格更高"],
 ["觉得白裙子单调就放弃", "选带流苏工艺的", "流苏增加立体度和层次感"],
],
"clothing-quality-myths": [
 ["看到堆叠量以为是瑕疵", "那是故意留的活动量", "方便穿脱和抬手臂"],
 ["看到麻结就剪掉", "麻结是天然特征，别剪", "剪了会纤维断裂破洞"],
 ["格子没对齐就是差", "合体省道处不对齐是正常的", "剪开缝进去必然歪斜"],
 ["里布有放量以为没烫好", "后中隐藏放量是必须工艺", "没有放量抬手会受限"],
],
"big-face-bazi-bangs": [
 ["想盖露白就直接剪短", "先找露白处、抠出前发盖住", "盲目剪短会越修越秃"],
 ["刮头发压着头皮刮", "刀刃立起来往前划", "压头皮刮会损伤发根"],
 ["长度凭感觉定", "拉到鼻子处定位", "鼻翼附近的长度最修饰脸型"],
 ["只修前面不管分区", "中分后分三角往前梳", "分区决定刘海整体走向"],
],
"clothes-quality-details": [
 ["以为插肩袖都差不多", "看省位是否在肩臂转折点", "省位不对肩部就松垮"],
 ["只挑好看的款式", "认内里有贴衬的无袖T恤", "没贴衬洗几次就变形"],
 ["看到锁边觉得工整", "折回锁边压线要避开", "这种工艺一撑就变形"],
 ["好坏凭感觉", "看版型、内衬、锁边三处", "细心分辨才能避雷"],
],
    }
    return P[slug]

def shifts_for(slug):
    P = {
"original-vs-retouch": [["一上来就磨皮", "先圈选、做局部生成式修补"], ["只修脸不看整体", "先整体审视再动手"], ["大力度液化", "小幅度网格微调"]],
"uniqlo-airism-sweat-tips": [["夏天只买好看的", "按面料性能选衣"], ["以为真丝是唯一选择", "铜氨纤维性价比更高"], ["只穿一季就淘汰", "选久洗久穿依然消臭的"]],
"tight-vs-loose-slim": [["越紧越显瘦", "宽松才显瘦"], ["只看正面效果", "检查纱向与洗后形态"], ["买到薄的就以为透气", "透气还要防透色"]],
"linen-ramie-hemp-diff": [["凭感觉买麻", "先看纤维特性和产地"], ["同一种麻买到底", "按舒适度/透气/性价比分场景选"], ["麻料乱洗乱晒", "简单过水、通风晾干、卷放"]],
"clothes-quality-simple": [["只看花色", "先看版型和结构"], ["平整就是好", "有省道才贴合身体"], ["凭厚度判断", "看做工细节"]],
"bust-size-outfit-tips": [["喜欢的就买", "先看对折量"], ["胸大就穿宽松", "选对折量充足的版型"], ["胸小就穿紧身", "选碎折设计显大"]],
"clothing-luxury-details": [["贵=厚面料", "贵=工艺细节"], ["直裁长裙也行", "长裙要斜裁"], ["花纹看颜色", "花纹看立体度"]],
"clothing-quality-myths": [["堆叠量=瑕疵", "堆叠量=活动量"], ["麻结=残次", "麻结=天然特征"], ["格子歪=差", "省道处歪=正常"]],
"big-face-bazi-bangs": [["露白就拼命剪短", "抠前发盖住露白"], ["凭手感刮头发", "刀刃立起往前划"], ["长度靠猜", "拉到鼻子定位"]],
"clothes-quality-details": [["插肩袖都差不多", "看省位位置"], ["无袖T恤随便买", "认内里贴衬"], ["看锁边觉得工整", "折回锁边是雷"]],
    }
    return P[slug]

def main():
    slugs = ["original-vs-retouch","uniqlo-airism-sweat-tips","tight-vs-loose-slim","linen-ramie-hemp-diff","clothes-quality-simple","bust-size-outfit-tips","clothing-luxury-details","clothing-quality-myths","big-face-bazi-bangs","clothes-quality-details"]
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
