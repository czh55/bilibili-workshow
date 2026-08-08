#!/usr/bin/env python3
"""批29：为10篇游泳技术JSON补全 practice/pitfalls/shifts/footer_notes。"""
import json
from pathlib import Path

DATA = Path("/Users/chenzhiheng/Projects/bilibili-workshop/scripts/scene-data")

ENRICH = {
"ziyouyong-qingsong-changyou": {
 "practice": [
   ["说检查腿的位置", "Check whether your leg sinks or floats."],
   ["说划水行程要长", "A long stroke beats a short dog-paddle."],
   ["说侧向换气", "Breathing sideways never means lifting the head."],
   ["说前伸拉长行程", "Reach forward to lengthen every stroke."]
 ],
 "pitfalls": [
   ["Lifting the head to breathe", "Rolling the head sideways", "抬头换气会扯断身体流线"],
   ["Short floppy pulls", "Long steady extension", "行程太短会越游越累"],
   ["Kicking with straight legs", "Kicking from a floating position", "腿沉在水下会拖慢速度"],
   ["Gasping on every breath", "Relaxing the exhale", "像救命一样换气会消耗过多氧气"]
 ],
 "shifts": [
   ["以前换气就抬头", "现在侧头滚转，身体保持流线"],
   ["以前只关注速度", "现在先检查腿的位置与划程"],
   ["以前游25米就累", "现在靠前伸和侧呼吸把距离拉长"]
 ],
 "footer": "轻松长游三件套：腿飘在水面（少阻力）+ 划程拉长（少次数）+ 侧向换气（不破坏流线）。先检查腿位再谈提速。"
},
"ziyouyong-tisu-tips": {
 "practice": [
   ["说转胯提高效率", "Rotating the hips lets your arm pull longer."],
   ["说转胯减少水阻", "Sideways swimming with the shoulder up cuts drag."],
   ["说转胯帮助呼吸", "Hip rotation rolls the head out for a breath."],
   ["说自然转胯", "Reach high like picking fruit and the hip turns naturally."]
 ],
 "pitfalls": [
   ["Twisting the hips deliberately", "Letting the reach turn the hips", "刻意扭胯反而破坏节奏"],
   ["Rotating the whole torso", "Rotating around the long axis", "转胯不是整条脊柱乱转"],
   ["Forgetting the reach", "Reaching long first, then rotating", "手不先伸够，转胯无意义"],
   ["Swimming flat as a board", "Letting the hips roll side to side", "一点不转胯会阻力大增"]
 ],
 "shifts": [
   ["以前自由泳身体不动", "现在靠转胯让划水更远更省力"],
   ["以前发力全靠手臂", "现在用核心+身体合力推水"],
   ["以前转胯靠扭", "现在靠够高摘桃的天然动作"]
 ],
 "footer": "转胯不是扭屁股，是前伸够高时身体的自然反应。转胯带来四重收益：划程更长、水阻更小、呼吸更顺、发力更大。"
},
"mosike-dieyong-huanqi": {
 "practice": [
   ["说推水换气同步", "Sync the kick with the pull at the breath."],
   ["说颈肩背一条线", "Keep neck, shoulders and back in one line."],
   ["说身体平直推进", "Keep the body flat and drive forward."],
   ["说屈肘移臂", "Bending the elbow helps the recovery."]
 ],
 "pitfalls": [
   ["Lifting the chin to breathe", "Rotating the whole body like a plank", "抬头换气会让身体断成两截"],
   ["Scooping water shallowly", "Pushing through the full stroke", "推水不到位，换气就顶不上去"],
   ["Stiff straight-arm recovery", "Bent-elbow low recovery", "直臂甩臂会累到肩膀"],
   ["Kicking without rhythm", "Syncing kick with the pull", "换气时不打腿，动作断节"]
 ],
 "shifts": [
   ["以前蝶泳换气靠抬头", "现在推水+打腿+颈肩背一条线整体转"],
   ["以前手臂乱划", "现在比数字3和4记住发力与移臂"],
   ["以前身体起伏大", "现在保持平直向前推进"]
 ],
 "footer": "蝶泳换气口诀：推水时打腿、颈肩背成一线、身体平直推进、屈肘移臂。俄教练的三字诀：推、线、平。"
},
"youyong-zhuanshen-duibi": {
 "practice": [
   ["说紧凑团身", "A tighter tuck spins you faster."],
   ["说蹬壁时机", "Hug the wall longer for a solid push."],
   ["说冲刺后团身", "Sprint in sync, then tuck tight."],
   ["说翻滚中段保持", "Stay compact throughout the flip."]
 ],
 "pitfalls": [
   ["Tucking loose and upright", "Tucking tight and close", "团身松会拉长半径转不快"],
   ["Pushing off too early", "Pressing both feet against the wall", "离墙远蹬壁会泄力"],
   ["Opening up mid-flip", "Staying curled until feet touch", "翻滚中展开会损失角速度"],
   ["Looking behind you", "Spotting the wall with your eyes", "回头张望会破坏团身"]
 ],
 "shifts": [
   ["以前翻滚像慢放", "现在团身紧、贴墙久，一滚一带"],
   ["以前蹬壁靠冲劲", "现在等脚贴稳再发力"],
   ["以前只求转过去", "现在追求滚翻速度+蹬壁质量"]
 ],
 "footer": "转身对比的本质：松散团身 vs 紧凑团身。团身越紧滚翻越快、贴墙越久蹬壁越有力——差的就是这两点。"
},
"chigun-zhuanjian-lianxi": {
 "practice": [
   ["说仰泳棍身一字", "The pole lies flat, passing the mid-shoulder line."],
   ["说自由泳前伸下探", "Lean forward, the pole reaching down."],
   ["说高肘移臂", "The pole sweeps back with the elbow raised."],
   ["说弧线闭环", "Each arc closes its own loop."]
 ],
 "pitfalls": [
   ["Bending the elbow too much", "Letting the pole stay level", "持棍时屈肘就失去轨迹参照"],
   ["Rotating at the waist", "Rotating at the shoulder", "转肩练习动腰就白练了"],
   ["Rushing the cycle", "Tracing the full arc slowly", "赶速度会丢失肩线轨迹"],
   ["Dropping the leading hand", "Keeping the pole aligned", "棍身歪斜说明转肩不完整"]
 ],
 "shifts": [
   ["以前转肩靠感觉", "现在一根棍画出标准弧线"],
   ["以前水陆脱节", "现在陆上轨迹直接对应水中划臂"],
   ["以前仰泳自由泳分开练", "现在一棍两用，一套动作练两泳"]
 ],
 "footer": "持棍转肩=把水中看不见的划臂路径搬到陆上可视化。仰泳走一字、自由泳走下探+高肘，弧线闭环才算完整。"
},
"qimeng-jibengong-shangxian": {
 "practice": [
   ["说鞭状腿无抬腿", "The whip kick has no lifting motion."],
   ["说直棍腿的代价", "Straight-stick kicking hurts countless swimmers."],
   ["说展开小腹发力", "The whip kick expands the lower abs."],
   ["说鞭状腿起频率", "Only the whip kick can hit high tempo."]
 ],
 "pitfalls": [
   ["Lifting the whole leg", "Expanding the lower abs", "抬腿是直棍腿，不是鞭状腿"],
   ["Expecting a quick fix", "Accumulating swim volume", "速成班教不出舒展的自由泳"],
   ["Training kicks on land", "Learning them in the water", "自由泳腿本质只能水中练"],
   ["Forcing a transition", "Rebuilding the mechanics", "发力方式不同，直棍转鞭状是扯淡"]
 ],
 "shifts": [
   ["以前以为打腿=抬腿", "现在知道是展开小腹的鞭状发力"],
   ["以前相信速成班", "现在明白需要量的堆积"],
   ["以前追求直上直下", "现在明白只有鞭状腿才能起频率"]
 ],
 "footer": "鞭状腿不是抬腿，是展开小腹的波浪发力。直棍腿是商业速成的坑，真正的自由泳腿只能靠水中量的积累。"
},
"hexin-shoujin-fangfa": {
 "practice": [
   ["说核心肌群组成", "The core includes the abs, back and pelvis."],
   ["说收紧与吸肚子的区别", "Bracing can take a punch; sucking in stays soft."],
   ["说保护脊柱", "Firing together, they shield the spine."],
   ["说吹蜡烛技巧", "Blowing engages the transverse abs."]
 ],
 "pitfalls": [
   ["Sucking in your belly", "Bracing the whole core", "吸肚子是软的，扛不住冲击"],
   ["Only training the abs", "Training abs, back and pelvis", "只练肚子不是核心训练"],
   ["Holding your breath", "Exhaling while bracing", "憋气收紧会缺氧眩晕"],
   ["Bracing only mid-exercise", "Bracing before every rep", "发力瞬间才收核心容易受伤"]
 ],
 "shifts": [
   ["以前收紧=吸肚子", "现在一锤一圈能抵挡才是核心收紧"],
   ["以前只练腹肌", "现在练腹部背部骨盆整个核心"],
   ["以前找不到感觉", "现在上大号/吹蜡烛/大笑三招秒会"]
 ],
 "footer": "核心=腹部+背部+骨盆。收紧是硬如铜墙、能扛冲击，吸肚子是软趴趴。三招生活技巧：上大号、吹蜡烛、笑出腹肌。"
},
"dieyong-huashou-jiaoxue": {
 "practice": [
   ["说四段划手", "The pull has four phases: reach, catch, pull, pinky-out."],
   ["说拇指入水", "Enter the water thumbs first."],
   ["说压胸提臀", "Press the chest down, lift the hips up."],
   ["说身体同拍", "Chest press and hip lift sync with the pull."]
 ],
 "pitfalls": [
   ["Entering pinky first", "Entering thumbs first", "小拇指先入水会阻水乱向"],
   ["Pulling only with arms", "Driving with chest and hips", "光靠手臂推水，蝶泳会很累"],
   ["Straight-arm recovery", "Low bent-elbow recovery", "直臂移臂容易拉伤肩膀"],
   ["Rushing the phases", "Completing each phase fully", "四段划水跳步会丢推力"]
 ],
 "shifts": [
   ["以前蝶泳全靠手臂", "现在压胸提臀用身体推进"],
   ["以前入水随手甩", "现在大拇指先入水、双手回前伸"],
   ["以前移臂乱甩", "现在低平屈肘、指向拇指入水"]
 ],
 "footer": "蝶泳划手四段：划手→抱水→推水→小拇指出水；入水拇指先行；身体压胸提臀与划手同拍。"
},
"dietui-jiebie-juepigu": {
 "practice": [
   ["说蝶腿误区", "Thinking the dolphin kick is a butt-up is a myth."],
   ["说手负责导向", "The hands steer you as you rise or dive."],
   ["说发力顺序", "Push the chest, then the belly, then flick the legs."],
   ["说循环节奏", "Finish the kick and flow into the next round."]
 ],
 "pitfalls": [
   ["Kicking from the hips", "Pushing the chest first", "只甩屁股，上半身会僵"],
   ["Freezing the torso", "Letting the wave travel through", "上半身不动就丢掉了波动"],
   ["Stopping after one kick", "Flowing into the next cycle", "打完腿停住，节奏就断了"],
   ["Forgetting the hands", "Using the hands to guide", "手不用，方向就会乱"]
 ],
 "shifts": [
   ["以前蝶腿=撅屁股", "现在顶胸-顶肚-甩腿的全身波动"],
   ["以前下半身硬甩", "现在手负责导向，波动贯穿全身"],
   ["以前出水乱游", "现在出水向上/前游垂直向前"]
 ],
 "footer": "蝶腿不是撅屁股，是顶胸-顶肚-甩腿的全身波动。手负责方向，腿是最后一步的自然甩动，节奏连续不断。"
},
"ziyouyong-datui-zoushui": {
 "practice": [
   ["说脚背推水", "Use the instep to push down and the sole to push up."],
   ["说膝踝放松", "Relaxed joints make the leg wave like a flag."],
   ["说微弯膝控方向", "Slightly bend the knees to control the kick's direction."],
   ["说沿腿全长推进", "Thrust builds along the entire leg."]
 ],
 "pitfalls": [
   ["Toes-down vertical cutting", "Pushing with the instep", "脚尖垂直切水只制造阻力"],
   ["Pulling knees to the chest", "Keeping a long bodyline", "收膝会向后推自己"],
   ["Stiff knees and ankles", "Relaxing into a wave", "膝踝僵硬就没有振荡推进"],
   ["Kicking straight up-down", "Guiding water from knee to toes", "直上直下打腿没有后推力"]
 ],
 "shifts": [
   ["以前以为打腿靠甩", "现在知道是靠脚面引导水流"],
   ["以前腿越硬越用力", "现在膝踝放松，波状如旗"],
   ["以前只求快打", "现在追求每一下都在产生后推力"]
 ],
 "footer": "自由泳打腿走水=用脚背向下、脚底向上引导水流向后。膝踝放松产生波浪，推力沿整条腿分布；僵硬垂直只会制造阻力。"
}
}

for p in sorted(DATA.glob("*.json")):
    slug = p.stem
    if slug not in ENRICH:
        continue
    d = json.loads(p.read_text(encoding="utf-8"))
    d["practice"] = ENRICH[slug]["practice"]
    d["pitfalls"] = ENRICH[slug]["pitfalls"]
    d["shifts"] = ENRICH[slug]["shifts"]
    d["footer_notes"] = ENRICH[slug]["footer"]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ {slug}")
print("完成")
