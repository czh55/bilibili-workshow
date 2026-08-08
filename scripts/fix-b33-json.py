#!/usr/bin/env python3
"""批33：为10篇摄影/修图/脸型JSON补全 practice/pitfalls/shifts/footer_notes。"""
import json
from pathlib import Path

DATA = Path("/Users/chenzhiheng/Projects/bilibili-workshop/scripts/scene-data")

ENRICH = {
"eye-catchlight-tutorial": {
  "practice": [
    ["说眼神光", "The bright spark in the eyes is a catchlight."],
    ["说逆光眩光", "Backlighting adds flare and blown highlights."],
    ["说挡光手法", "Block the lens glare with your hand, keep the catchlights."],
    ["说姿势微调", "Tuck the chin to clean up the facial lines."]
  ],
  "pitfalls": [
    ["Shoot straight into the sun.", "You get flare and lose the catchlights.", "直面太阳会过曝眩光。"],
    ["Use a reflector to create catchlights.", "Real sun in the eyes beats any bounced light.", "眼神光靠真实光源。"],
    ["Forget to pose the subject.", "A slight chin tuck changes everything.", "姿势微调很关键。"],
    ["Expect catchlights without direction.", "The model must face the light first.", "脸要先朝向光源。"]
  ],
  "shifts": [
    ["说眼睛光只说亮", "用 catchlight（眼神光）、spark（光点）、lively（有神）"],
    ["说逆光只说逆光", "用 backlight（逆光）、flare（眩光）、blown highlights（过曝高光）"]
  ],
  "footer": "转录基于图文实录完整口播与图注。已校正：一镜到底教拍眼神光、道具是一片透光枫叶、模特放在阳光下为眼睛受光做准备、太阳在画面一侧逆光带来高光与眩光、用手挡镜头上方强光保留眼神光压住过曝眩光、下巴略收让脸部线条与眼神光更干净、作者连夸漂亮眼神光与秋叶透光同时成立。"
},
"vlog-four-perspectives": {
  "practice": [
    ["说拇指相机", "A thumb-size camera that shoots 4K unlocks creative angles."],
    ["说第一人称", "Magnetic POV mounts free your hands for immersion."],
    ["说第三人称", "Built-in magnets invent third-person shots anywhere."],
    ["说上帝视角", "Ceiling mounts turn a day into a bird's-eye story."]
  ],
  "pitfalls": [
    ["Think creative angles need big gear.", "A thumb-size 4K camera plus mounts does it.", "小相机加支架就够。"],
    ["Forget POV options.", "A magnetic necklace mount gives immersive first-person.", "挂脖磁吸出第一人称。"],
    ["Stick to one perspective.", "First, third, and bird's-eye views enrich the story.", "多视角更有趣。"],
    ["Skip the mounts and clamps.", "Everyday items plus mounts equal new views.", "物品加支架就是新视角。"]
  ],
  "shifts": [
    ["说视角只说视角", "用 POV（第一人称）、third-person（第三人称）、bird's-eye view（上帝视角）"],
    ["说拍摄只说拍摄", "用 mount（支架）、magnetic（磁吸）、necklace（挂脖）"]
  ],
  "footer": "转录基于图文实录完整口播。已校正：新手小白能拍摄哪些有趣视角、用拇指大小能拍4K的相机教拍摄十几种创意镜头、利用转向支架或夹子将生活常用物品和相机固定在一起得到有趣视角、外出时用磁吸挂脖拍摄第一人称视角、机子小小不怕尴尬解放双手拍沉浸式视频、相机自带磁吸帮助发掘很多不一样的第三人称视角丰富Vlog画面、拍摄角度上还可以选择墙壁冰箱门上、高视角利用拓展舱轻松俯瞰画面得到丰富上帝视角、多视角展示一天都干了什么。"
},
"rain-umbrella-no-reflect": {
  "practice": [
    ["说伞面反光问题", "Beaded clear umbrellas throw glare over the face."],
    ["说上撑伞柄", "Push the umbrella up to clear the lens path."],
    ["说光线改道", "Raised, the light path shifts overhead and the face sharpens."]
  ],
  "pitfalls": [
    ["Shoot straight through the umbrella.", "Glare and droplets bury the face.", "俯拍伞面反光盖脸。"],
    ["Keep the umbrella low.", "It must clear the lens-to-face path.", "伞要离开镜头与脸之间。"],
    ["Remove the raindrops for clarity.", "Keep the droplets—the vibe is the point.", "雨滴是氛围不是瑕疵。"],
    ["Wait for the sun to move.", "Just reposition the umbrella instead.", "改伞的位置即可。"]
  ],
  "shifts": [
    ["说反光只说反光", "用 glare（反光）、highlights（高光）、overlap（叠加）"],
    ["说氛围只说氛围", "用 atmosphere（氛围）、droplet（水珠）、mood（情绪感）"]
  ],
  "footer": "转录基于图文实录完整口播与图注。已校正：透过带水珠的透明伞俯拍伞面反光看不清脸、另一角度伞面高光与水珠叠在一起面部细节被压住、手握伞柄把伞上撑、伞抬高后光线路径改到头顶方向、脸部轮廓与表情清晰雨滴氛围仍在、清晰度回来后雨天道具感反而更完整。"
},
"slow-shutter-portrait": {
  "practice": [
    ["说慢门人像差距", "The same slow shutter looks different in skilled hands."],
    ["说追焦拍摄", "Pan smoothly at 1/20s for cinematic motion."],
    ["说闪光流光", "Flash plus camera shake makes light trails."],
    ["说旋焦人像", "Center focus plus body rotation gives swirl blur."]
  ],
  "pitfalls": [
    ["Blame the camera price.", "Technique—panning, shaking, rotating—does the work.", "差距在技法不在器材。"],
    ["Use a slow shutter without motion.", "The blur comes from camera movement, not the number.", "慢门要配合移动。"],
    ["Shake randomly and hope.", "Center focus keeps the subject sharp while lines swirl.", "旋焦需要中心对焦。"],
    ["Forget the flash for trails.", "The flash freezes; the shake draws light.", "闪光灯是流光关键。"],
    ["Pan too fast or too slow.", "Smooth, steady tracking at 1/20s is the sweet spot.", "跟随要平稳。"]
  ],
  "shifts": [
    ["说慢门只说慢门", "用 slow shutter（慢门）、pan（追焦）、motion blur（动态模糊）"],
    ["说人像只说人像", "用 light trail（流光）、swirl blur（旋焦）、freeze（定住）"]
  ],
  "footer": "转录基于图文实录完整口播。已校正：你用慢门拍的照片和摄影师用慢门拍的照片差距大、不是相机更贵而是技法、把快门速度设为20分之1秒、相机平稳跟着模特一起移动就能拍出电影感的追焦照片、让模特静止不动就能拍出时间流逝的效果、准备一个闪光灯在按下快门的同时晃动相机就能拍出绝美流光人像效果、给相机设置中心对焦拍摄时旋转机身就拍出来定格旋焦人像。"
},
"video-clarity-tips": {
  "practice": [
    ["说光的决定性", "Light rules clarity—too little means noise and mush."],
    ["说明暗对比", "Contrast, not brightness, is the real clarity secret."],
    ["说蝴蝶光公式", "Key at 45° down makes a butterfly highlight that slims the face."],
    ["说背景分离", "Back lights separate the subject for depth."],
    ["说色彩对比", "A blue fill against warm light adds cinematic punch."],
    ["说导出参数", "Shoot 4K, export H.264 at max bitrate."]
  ],
  "pitfalls": [
    ["Upgrade the camera first.", "Fix the light and contrast before buying gear.", "先解决光再换设备。"],
    ["Flood the scene with flat light.", "Even lighting removes focus and feels unclear.", "太平的光没有视觉重心。"],
    ["Skip the fill light.", "Dead-black shadows need a softer fill.", "暗部需要补光。"],
    ["Blast the subject with the key.", "Butterfly light at 45° is the classic look.", "主光45度出蝴蝶光。"],
    ["Edit hard but export soft.", "Low bitrate ruins the clarity you created.", "导出参数不对伤画质。"],
    ["Shoot 1080p and crop later.", "4K survives reframing without heavy loss.", "4K抗二次构图。"]
  ],
  "shifts": [
    ["说清晰只说清晰", "用 clarity（清晰度）、contrast（对比）、noise（噪点）"],
    ["说打光只说打光", "用 key light（主光）、fill light（补光）、butterfly lighting（蝴蝶光）"],
    ["说后期只说后期", "用 H.264、bitrate（码率）、saturation（饱和度）"]
  ],
  "footer": "转录基于图文实录完整口播。已校正：相机拍的画面还没手机拍的清晰、并非如此、对画面清晰度起决定性作用的元素是光、光线太暗导致画面噪点严重细节模糊、只用灯把环境打亮光线太平画面没有视觉重心观感不够清晰、当主体从环境中凸显出来画面就清晰多了、所以光是表层原因、光带来的明暗对比才是最底层原因、经典万能打光公式第一步主光放人物正前方从上往下45度角拍摄、人脸上形成蝴蝶形状高光脸颊两侧阴影视觉上更显瘦立体、第二步用灯棒或反光板给阴影补一点光不要让暗部过于死黑但光线要比主光弱一点、这就是早期好莱坞给女演员打的蝴蝶光因为拍人好看也叫美人光、第三步在背景里放一些小灯比如小台灯落地灯、让人物边缘和背景分离开来画面更有氛围感、明暗对比能增加清晰度别的对比也可以、比如色彩对比很多电影让主体颜色和背景形成强烈对比塑造人物形象、拍口播时用灯棒给窗帘打蓝色和屋内暖光形成对比让画面更有质感、大光圈拍人更好看原理类似光圈越大虚实对比越明显主体更突出、后期通过手动拉曝光对比度和饱和度增加画面对比也能提升清晰度、做完这些清晰度已能打到90%的人、导出参数不对容易损伤画质、前期尽量用4K分辨率即便二次构图也不会过度损伤画质、导出编码选择H.264最高码率。"
},
"wedding-retouch-process": {
  "practice": [
    ["说轮廓勾勒", "Trace the crown-to-forehead line to start a retouch."],
    ["说蚂蚁线选区", "Marching ants mark exactly where you'll edit."],
    ["说液化网格", "A mesh and pins shape the body without global warping."],
    ["说黑白检视", "Desaturating exposes tonal problems color hides."],
    ["说前后对照", "Grading side-by-side proves the retouch works."]
  ],
  "pitfalls": [
    ["Jump straight to smoothing.", "Outline, select, and liquify come first.", "先轮廓后磨皮。"],
    ["Liquify the whole body at once.", "Pinned local meshes keep it natural.", "局部液化更自然。"],
    ["Trust the color view.", "A black-and-white pass reveals tonal issues.", "黑白检视查光影。"],
    ["Forget the final comparison.", "Side-by-side grading shows the true result.", "对照才见效果。"],
    ["Retouch without precision zoom.", "100% zoom catches knee creases and seams.", "细节要放大看。"]
  ],
  "shifts": [
    ["说选区只说选区", "用 marching ants（蚂蚁线）、selection（选区）、local edit（局部处理）"],
    ["说修图只说修图", "用 liquify（液化）、mesh（网格）、anchor（锚点）"],
    ["说检视只说检视", "用 desaturate（去色）、black-and-white check（黑白检视）、grade（调色）"]
  ],
  "footer": "转录基于图文实录完整口播与图注。已校正：开场侧脸发顶到额头的勾勒线光标停在发际附近、天空选区不规则蚂蚁线落在蓝天区域准备做局部处理或填充、液化变形网格新娘全身三角网与钉点耳旁显示像素坐标与6.0度、西服选区蚂蚁线贴着夹克下摆与背景交界准备局部处理、肩部变形网格蓝色3×3锚点覆盖西装肩臂水印颜值修图可见、裤线刷修100%缩放下圆形笔刷停在西裤膝后褶皱处、黑白检视去色后回看新娘侧脸与头纱层次光标停在耳饰附近、成片与调色对照左右饱和度色温差异明显画面带修图服务水印。"
},
"retoucher-ends-cleaner": {
  "practice": [
    ["说保洁隐喻", "Retouching is housekeeping—tidy one patch at a time."],
    ["说高低频", "High/low frequency splits texture from color for clean skin."],
    ["说背景清场", "Background clutter gets swept like a floor."],
    ["说细节级别", "Band-aids and plates are cleaning-grade details."],
    ["说验收终帧", "A clean wide shot is the final acceptance."]
  ],
  "pitfalls": [
    ["Smooth everything globally.", "Local, frequency-separated work keeps skin real.", "全局磨皮会失真。"],
    ["Leave background clutter.", "Cars, plates and signs all get swept.", "背景杂物要清场。"],
    ["Miss the tiny stuff.", "A heel band-aid is exactly the point.", "小细节正是重点。"],
    ["Judge only in color.", "Check tonal quality on its own.", "要单独看影调。"],
    ["Stop before the wide shot.", "The clean full frame is the acceptance.", "终帧全景才见成果。"]
  ],
  "shifts": [
    ["说修图只说修图", "用 frequency separation（高低频）、pen path（钢笔路径）、local retouch（局部修图）"],
    ["说清场只说清场", "用 cleanup（清场）、sweep（清扫）、remove clutter（去杂物）"]
  ],
  "footer": "转录基于图文实录完整口播与图注。已校正：开场钢笔点落在腋窝附近对应标题保洁隐喻先打扫皮肤局部、笑口特写标题栏可见变色鱼高低频进入皮肤牙齿细节层、地砖扫地钢笔路径框住斜向路面区域准备清理、中景电瓶车车牌与钢笔路径同框背景清场开始、变换框罩住车牌车轮一带红门福字与颜值修图水印可见、脚后跟创可贴特写典型保洁级细节准备擦掉、中景验收背景更干净人物与红门福成为主体、终帧清场后的彩色全景对应保洁完成的结果。"
},
"wedding-photo-retouch": {
  "practice": [
    ["说高倍检视", "Zoom in hard on creases, moles, and edges first."],
    ["说局部液化", "Liquify the neck creases locally, never globally."],
    ["说轮廓蒙版", "Build a silhouette mask before swapping the background."],
    ["说黑白复查", "Strip color to check the light transitions."]
  ],
  "pitfalls": [
    ["Global skin smoothing.", "Local warping and brushes keep the skin real.", "局部处理更自然。"],
    ["Retouch blind at 100%.", "245% zoom is where the real detail lives.", "高倍缩放下精修。"],
    ["Swap backgrounds without a mask.", "Follow the head-neck-shoulder silhouette first.", "先建立轮廓蒙版。"],
    ["Judge by color alone.", "A black-and-white pass exposes the transitions.", "去色复查光影。"],
    ["Forget the full-body view.", "Posture and garment need a 100% check.", "全身回看体态服装。"]
  ],
  "shifts": [
    ["说修图只说修图", "用 liquify（液化）、mask（蒙版）、retouch brush（修复笔刷）"],
    ["说检视只说检视", "用 245% zoom（高倍缩放）、black-and-white check（黑白检视）、transition（过渡）"]
  ],
  "footer": "转录基于图文实录完整口播与图注。已校正：开场高倍检视皮肤折痕痣点与深色椅面边界钢笔光标停在轮廓线上、液化网格覆盖颈侧针对横纹做局部变形而非全局磨皮、侧光人像工作视图暖光勾勒下颌与颈前蕾丝婚纱细节清晰、轮廓蒙版选区沿头颈肩剪影行进为后续换背景或局部处理做准备、高倍局部润饰笔刷落在颈侧阴影过渡带界面显示约245%缩放、全身回看100%视图下检查体态与服装手臂旁有白色标注线、构图检视台灯圆桌与沙发一并入画确认暖光氛围与整体层次、黑白检视去掉色彩后复查颈肩光影过渡与皮肤干净度。"
},
"cinematic-composition": {
  "practice": [
    ["说黄金分割", "A golden-ratio card finds the visual landing point."],
    ["说普通vs电影感", "Even light reads ordinary; side light reads cinematic."],
    ["说快门与运动", "Faster shutter freezes motion; slower blurs it."],
    ["说曝光三要素", "Shutter stops motion, aperture sets depth, ISO tunes light."]
  ],
  "pitfalls": [
    ["Rely on rule-of-thirds only.", "Golden-ratio placement sharpens the eye.", "黄金分割更精确。"],
    ["Blast flat light and call it clean.", "A side-light panel creates the drama.", "侧光才有戏剧感。"],
    ["Shoot every scene at 1/60s.", "1/1300s freezes; 1/60s blurs—choose the story.", "快门速度是创作工具。"],
    ["Forget the exposure trio.", "Shutter, aperture and ISO divide the work.", "三要素各司其职。"]
  ],
  "shifts": [
    ["说构图只说构图", "用 golden ratio（黄金分割）、focal placement（焦点落点）、composition card（构图卡）"],
    ["说电影感只说电影感", "用 dramatic side light（戏剧性侧光）、cinematic（电影感的）、LED panel（灯板）"]
  ],
  "footer": "转录基于图文实录完整口播与图注。已校正：开场构图工具黄金分割卡对准路锥室外日光下演示焦点落点、对照A同一鞋履题材先给出普通的观感光线相对平均、对照A幕后感地面相机与环境光并存尚未看到强侧光灯板、对照B叠字电影感的下方可见LED灯板制造的戏剧性侧光、快门对比1/60秒糊成圆盘1/160秒见臂影1/1300秒冻帧清晰、收尾总览快门控制运动光圈控制景深ISO控制亮度与噪点。"
},
"face-shape-analysis": {
  "practice": [
    ["说S型轮廓", "The S-curve nose-lip-chin profile is called the ugliest."],
    ["说直面型", "A near-vertical profile reads sculpted and dignified."],
    ["说凸面微凸", "Bulging profiles read bright, classy, or naive."],
    ["说凹面微凹", "Curved-in profiles are common and read sorrowful."]
  ],
  "pitfalls": [
    ["Judge faces by the front view alone.", "The side profile sets the shape category.", "侧轮廓才定面型。"],
    ["Treat labels as facts.", "These are perceptual categories, not verdicts.", "标签是审美分类不是定论。"],
    ["Skip the nose-lip-chin line.", "That dashed line is the whole analysis.", "鼻唇颏起伏是核心。"],
    ["Assume beauty is universal.", "Perception varies by culture and era.", "审美有时代地域差异。"]
  ],
  "shifts": [
    ["说脸型只说脸型", "用 profile（侧轮廓）、S-curve（S型）、straight（直面型）"],
    ["说轮廓只说轮廓", "用 convex（凸面）、concave（凹面）、bulge（外拱）"]
  ],
  "footer": "转录基于图文实录完整口播与图注。已校正：红虚线描出鼻唇颏起伏、黄字这是最丑的面型、黄白叠字S型早期凤姐脸、直面型红虚线更接近竖直轮廓立体端庄标志大气、微凸定名轮廓略向外凸明艳贵气多出港风美女、凸面定名鼻唇颏外拱更明显可爱不足憨态有余、微凹段口号正脸大字东亚人最多的面型容易出现三八纹、凹面定名红虚线向内弯叫月亮脸苦相又土气很难出美女、收束观感大字很难出美女压在胸口位置。"
},
}

for slug, enr in ENRICH.items():
    p = DATA / f"{slug}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["practice"] = enr["practice"]
    d["pitfalls"] = enr["pitfalls"]
    d["shifts"] = enr["shifts"]
    d["footer_notes"] = enr["footer"]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ {slug}: practice {len(enr['practice'])} / pitfalls {len(enr['pitfalls'])} / shifts {len(enr['shifts'])}")
print("完成")
