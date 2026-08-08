#!/usr/bin/env python3
"""批30：为10篇跑步/徒步/摄影/相机JSON补全 practice/pitfalls/shifts/footer_notes。"""
import json
from pathlib import Path

DATA = Path("/Users/chenzhiheng/Projects/bilibili-workshop/scripts/scene-data")

ENRICH = {
"paobu-songkuan-tips": {
 "practice": [
   ["说跑步是走路的延伸", "Running is walking, extended."],
   ["说重心提起不下沉", "Lift your center and never let it sink."],
   ["说撑起来就送髋", "Stay tall and you're already driving the hip."],
   ["说推臀前进感", "Feel a hand always pushing your hip forward."]
 ],
 "pitfalls": [
   ["Swinging the hips like ballroom", "Staying tall to drive the hip", "把送髋理解成扭胯是最大误区"],
   ["Caving in at the waist", "Lifting the center of gravity", "塌腰跑重心下沉，送髋全丢"],
   ["Forcing hip movement", "Letting posture create it", "送髋是撑起来自然带出的"],
   ["Sinking at the hips", "Feeling the forward push", "感觉不到有人推着臀就没送髋"]
 ],
 "shifts": [
   ["以前以为送髋是扭屁股", "现在撑起来重心提起就是送髋"],
   ["以前一跑就塌腰", "现在跑步是走路的延伸，重心保持"],
   ["以前追求大腿摆动", "现在感觉有人推着臀往前"]
 ],
 "footer": "送髋不是扭胯，是撑起重心后的自然结果。跑步=走路延伸，重心提起不下沉，感觉有人推着臀往前走就对了。"
},
"quanma-posan-baibi": {
 "practice": [
   ["说准备姿势", "Stagger your stance with weight on the front leg."],
   ["说前摆最高点", "At the top of the forward swing, the thumb reaches the nose."],
   ["说后摆肩肘带动", "In the backswing, keep wrist and elbow still and drive from the shoulder."],
   ["说长跑摆臂", "Marathons use the same swing, just smaller."]
 ],
 "pitfalls": [
   ["Swinging past the nose", "Stopping the thumb at the nose", "摆过鼻尖会让身体后仰"],
   ["Elbow drifting from the waist", "Keeping the elbow close", "肘离腰远，上身就会晃动"],
   ["Moving wrist and elbow", "Driving from the shoulder", "后摆靠肩肘带动，腕肘不动"],
   ["Same big swing for marathons", "Smaller amplitude on long runs", "马拉松也大摆臂会浪费体力"]
 ],
 "shifts": [
   ["以前跑步手臂乱甩", "现在虎口到鼻尖、肘贴腰的标准摆臂"],
   ["以前摆臂幅度一成不变", "现在短跑大摆臂、长跑小摆臂"],
   ["以前躯干乱晃", "现在以躯干为轴，前不露肘后不露手"]
 ],
 "footer": "摆臂四要素：空拳90度、虎口到鼻尖、肩肘带动后摆、肘贴腰。短跑大摆臂、长跑小摆臂，以躯干为轴减少晃动。"
},
"hike-route-difficulty": {
 "practice": [
   ["说公里数会骗人", "Judging a trail is about three numbers, not distance."],
   ["说累计爬升的体感", "100m per kilometer equals ten floors every kilometer."],
   ["说爬升判断标准", "Under 500m of climb, a daily-walking habit is enough."],
   ["说高海拔的代价", "The same slope costs 30-50% more effort up high."],
   ["说路况的影响", "Stairs repeat the same knee bend and build patella pressure."]
 ],
 "pitfalls": [
   ["Judging by kilometers alone", "Checking climb, altitude and surface", "只看公里数会被难度骗到"],
   ["Reading only the peak altitude", "Checking start elevation and rise speed", "只看最高海拔，不看起点与上升速度"],
   ["Ignoring the trail surface", "Asking about stairs, scree or mud", "忽略路况，体力消耗远超预期"],
   ["Climbing too fast at altitude", "Gaining under 500m per day", "高海拔每天爬升太快会高反"]
 ],
 "shifts": [
   ["以前看路线只看公里数", "现在先看累计爬升三档标准"],
   ["以前只看最高海拔", "现在看起点海拔和上升速度"],
   ["以前忽略路面", "现在先问台阶碎石还是泥路"]
 ],
 "footer": "徒步难度三数字：累计爬升（<500/500-1000/1000+三档）、海拔变化速度（日升≤500m安全）、路况（台阶/碎石/泥路）。装备是加分项，体能与认知才是基础。"
},
"huanjing-yuecha-weimei": {
 "practice": [
   ["说普通环境出片", "Ordinary spots can still deliver epic, painterly shots."],
   ["说别只盯器材", "Don't pin great work on the camera and lens."],
   ["说真正要学的", "Light, weather, composition and timing are the real lessons."]
 ],
 "pitfalls": [
   ["Chasing camera specs", "Learning light, weather and timing", "纠结参数不如学光线构图"],
   ["Waiting for perfect scenery", "Working with the plain environment", "等完美环境不如把眼前拍好"],
   ["Ignoring clothing and styling", "Dressing the model for the scene", "服装是画面的一部分"],
   ["Forgetting post-processing", "Planning editing from the start", "后期思维要从拍摄前就开始"]
 ],
 "shifts": [
   ["以前纠结相机品牌参数", "现在关注光线天气构图时机"],
   ["以前等完美环境", "现在普通环境红框定点就能出片"],
   ["以前以为设备决定一切", "现在思维模式+引导模特才是关键"]
 ],
 "footer": "环境越差照片越美的秘密：不是环境，是取景思路。红框定点放人，光线/天气/服装/环境/后期/构图/时机才是真正该学的。"
},
"rope-face-tracking-mobile7p": {
 "practice": [
   ["说跟随感镜头", "A rope plus a tracking gimbal creates the follow shot."],
   ["说构图稳定", "Side tracking mirrors the top view—framing stays stable."],
   ["说幕后布置", "The crew and the crossing rope reveal the trick."]
 ],
 "pitfalls": [
   ["Shooting handheld for the shot", "Rigging the gimbal on a rope path", "手持拍不出这种跟随轨迹"],
   ["Revealing the rig early", "Hiding the rope until the wide shot", "绳子进画要留到广角才露"],
   ["Shaky tracking", "Steady side and top views", "追踪不稳构图就散"]
 ],
 "shifts": [
   ["以前跟拍靠手持", "现在一根绳子+稳定器追踪拍出机关感"],
   ["以前只会正对拍", "现在侧面/俯视同构，构图更稳"],
   ["以前幕后穿帮", "现在把机关藏到广角才揭晓"]
 ],
 "footer": "绳子+稳定器人脸追踪：用绳子和高机位布置稳定轨迹，侧面/俯视同构保证构图稳定，广角才揭晓幕后机关。"
},
"buguang-guangwei-tips": {
 "practice": [
   ["说逆光表现通透", "Looks flat? Use backlight to bring out layers."],
   ["说双灯切高光", "Two lights: one keys the highlight, one backlights for depth."],
   ["说轮廓光抠暗色", "Rim light cuts the dark object out of the dark."],
   ["说裸灯打光影", "Flat and dull? Go with a bare light."]
 ],
 "pitfalls": [
   ["Using front light only", "Adding backlight for translucency", "单打前光是照片不通透的主因"],
   ["One light for everything", "Splitting key and backlight", "一个灯又想切高光又补层次会两头空"],
   ["Ignoring stray light", "Diffusing and blocking stray light", "杂光不处理，高光形状就脏"],
   ["Afraid of bare lights", "Using bare light for hard shadows", "光影太平时恰恰要裸灯"]
 ],
 "shifts": [
   ["以前布光东拼西凑", "现在就几个光位来回用：逆光/双灯/轮廓光/裸灯"],
   ["以前高光一塌糊涂", "现在先切高光再补层次"],
   ["以前怕器材复杂", "现在单灯+反光板也能拍大部分产品"]
 ],
 "footer": "布光就几个光位来回用：不通透打逆光、玻璃切双灯、黑中有黑用轮廓光、太平用裸灯、少器材用单灯+反光板。"
},
"chekuai-renman-tutorial": {
 "practice": [
   ["说拍两段素材", "Fix the phone and film the person walking toward you."],
   ["说画中画变速", "Drop the speed to about 0.3 and enable frame interpolation."],
   ["说蒙版融合", "Add a linear mask with the line between the person and the traffic."]
 ],
 "pitfalls": [
   ["Moving the camera between clips", "Keeping the camera fixed", "两段素材机位不一致会穿帮"],
   ["Skipping frame interpolation", "Enabling smart frame interpolation", "0.3倍速不补帧画面会卡顿"],
   ["Hard mask edges", "Feathering the mask line", "蒙版不羽化，接缝明显"],
   ["Keeping the long tail", "Trimming the extra ending", "结尾多余画面要删掉"]
 ],
 "shifts": [
   ["以前以为车快人慢要复杂合成", "现在延时车流+0.3倍人物+线性蒙版三步搞定"],
   ["以前蒙版生硬", "现在羽化让两画面自然融合"],
   ["以前机位随手移", "现在机位固定两段各拍"]
 ],
 "footer": "车快人慢=延时车流（快）+ 0.3倍速人物（慢）+ 线性蒙版羽化融合。机位固定、智能补帧、删尾导出。"
},
"dual-native-iso": {
 "practice": [
   ["说两大技术", "The two big ones: DCG dual-conversion gain and DGO dual-gain output."],
   ["说DCG两个电容", "Dual conversion gain means two capacitors, one big, one small."],
   ["说暗光画质提升", "Front-end read noise stays put, so low-light quality rises."],
   ["说DGO融合", "Low gain keeps highlights; high gain saves shadows."]
 ],
 "pitfalls": [
   ["Confusing DCG with DGO", "Separating conversion vs fusion paths", "DCG是电容切换，DGO是双路融合"],
   ["Thinking ISO gain is free", "Noting read noise amplifies too", "PGA放大会连噪声一起放大"],
   ["Judging only by dynamic range", "Choosing DCG for dark scenes", "动态范围选DGO，暗光选DCG"],
   ["Mixing up the terms", "Using technical names in depth", "双增益/双原生ISO两种技术路径不同"]
 ],
 "shifts": [
   ["以前以为ISO只是调亮度", "现在知道ISO本质是增益"],
   ["以前双原生ISO是玄学", "现在DCG双电容+第二基准ISO让暗光更干净"],
   ["以前动态范围就靠HDR", "现在DGO双路读出融合更聪明"]
 ],
 "footer": "双原生ISO的两种路径：DCG双转换增益（大小电容两档基准ISO，暗光压制前端噪声）与DGO双增益融合（双路读出后期融合，大幅提升动态范围）。ISO本质是增益。"
},
"huoren-yunjing-3tips": {
 "practice": [
   ["说推镜头", "The push-in closes both physical and emotional distance."],
   ["说拉镜头", "The pull-back opens up a wider world."],
   ["说环绕秘诀", "The trick: the subject's gaze follows the camera."],
   ["说追踪模块", "Box the subject on screen to start tracking."]
 ],
 "pitfalls": [
   ["Shooting static shots", "Adding push or pull to every scene", "固定机位拍再多也缺活人感"],
   ["Orbiting with a wandering subject", "Keeping the gaze following the camera", "环绕时目光不跟镜头就散"],
   ["Using the wrong gimbal mode", "Picking PF or PTF for the move", "档位不对画面就晃"],
   ["Ignoring frame drift", "Letting tracking lock the subject", "大幅度运镜不追踪容易跑偏"]
 ],
 "shifts": [
   ["以前一条固定机位拍到底", "现在推/拉/环绕三种运镜讲活人感"],
   ["以前运镜全靠手稳", "现在追踪模块框选即可闭眼运镜"],
   ["以前不知道档位", "现在水平线用PF、摇镜头用PTF"]
 ],
 "footer": "活人感三运镜：推（靠近期待）、拉（展开氛围）、环绕（不挑场景）。大运镜靠追踪模块锁人，档位选对画面就稳。"
},
"travel-10-transitions-2": {
 "practice": [
   ["说遮挡物转场", "Cover the lens with anything and you have a transition."],
   ["说自己造遮挡", "No obstacle around? Create one yourself."],
   ["说敲击转场", "Tap the lens and you get the knock cut."],
   ["说甩镜转场", "At the end of clip one, whip the camera to one side."],
   ["说脑补原理", "A hint of connection and the brain fills in the rest."]
 ],
 "pitfalls": [
   ["Cutting without a cover", "Blocking the lens for one beat", "硬切没有遮挡物会跳"],
   ["Whip-panning the same direction", "Starting the next clip opposite", "甩镜两段同方向拼不起来"],
   ["Chasing fancy effects", "Relying on similarity and motion", "转场本质是画面联系感"],
   ["Forgetting the brain-fill trick", "Trusting the viewer's imagination", "忘了观众会脑补，转场就会生硬"]
 ],
 "shifts": [
   ["以前转场靠特效模板", "现在遮挡物+甩镜+相似动作三招通用"],
   ["以前找不到遮挡物就放弃", "现在用手臂手指自己造遮挡"],
   ["以前以为转场玄学", "现在知道靠画面联系感让大脑脑补"]
 ],
 "footer": "转场底层逻辑=画面间的联系感。遮挡物一遮、甩镜反向拼接、相似动作衔接，大脑会自动脑补过渡——这就是丝滑的秘密。"
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
