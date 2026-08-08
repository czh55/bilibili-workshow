#!/usr/bin/env python3
"""批30：为10篇小红书视频生成完整场景英译JSON（跑步送髋/摆臂/徒步难度/摄影/双原生ISO/运镜转场）。"""
import json, re
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

ARTICLES = {}

ARTICLES["paobu-songkuan-tips"] = {
    "title_zh": "新手跑者必须要知道跑步如何送髋",
    "title_en": "Hip Drive Every New Runner Must Know",
    "duration": "43秒",
    "topic": "跑步 · 跑姿",
    "scenes": [
        {"id": "s1", "scene_zh": "跑步是走路的延伸", "scene_en": "Running Is Walking, Extended", "time": "00:00",
         "context": "很多人在走路的时候很挺拔，但是一跑就塌。为什么？因为不知道送髋的正确姿势。跑步是走路的延伸：走路时沿髋部水平线往前移动，跑的时候仍然是这样跑的，重心提起来，这个地方绝对没有向下下沉。",
         "sentences": [
            ["走路很挺拔，一跑就塌，是不知道送髋。", "You walk tall but cave in while running—that's missing hip drive.", "hip drive（送髋）"],
            ["跑步是走路的延伸。", "Running is walking, extended.", "extended（延伸）"],
            ["重心提起来，绝对不向下下沉。", "Lift your center and never let it sink.", "center of gravity（重心）"]
         ]},
        {"id": "s2", "scene_zh": "送髋不是跳国标", "scene_en": "Hip Drive Isn't Ballroom Hips", "time": "00:19",
         "context": "很多人认为送髋像跳国标那样送。不是的。现在我就送髋了，这样没送髋，这样送髋了，没送髋。听懂了吗？跑的时候撑起来就已经送髋了。",
         "sentences": [
            ["送髋不是像跳国标那样扭。", "Hip drive isn't ballroom-style hip swing.", "ballroom（国标舞）"],
            ["跑的时候撑起来，就已经送髋了。", "Stay tall and you're already driving the hip.", "stay tall（撑起来）"],
            ["一撑就送髋，一塌就丢失。", "Tall means drive; slumping loses it.", "slump（塌陷）"]
         ]},
        {"id": "s3", "scene_zh": "感觉有人推着你的臀", "scene_en": "Feel a Hand Pushing Your Hip", "time": "00:30",
         "context": "没有撑起来，一跑就这样塌。感觉有人用手时刻推着你的臀，再往前走。这里再往前走。千万不要这样塌腰的模式。",
         "sentences": [
            ["感觉有人时刻推着你的臀往前走。", "Feel a hand always pushing your hip forward.", "push forward（向前推）"],
            ["千万不要塌腰的跑步模式。", "Never run in the slumped-waist mode.", "slumped waist（塌腰）"]
         ]}
    ]
}

ARTICLES["quanma-posan-baibi"] = {
    "title_zh": "全马破三选手应该怎么跑步摆臂",
    "title_en": "Arm Swing for a Sub-3 Marathoner",
    "duration": "1分32秒",
    "topic": "跑步 · 摆臂",
    "scenes": [
        {"id": "s1", "scene_zh": "摆臂：跑步稳定的关键", "scene_en": "Arm Swing: The Key to Stability", "time": "00:00",
         "context": "我们跑的时候要稳定，所以摆臂就很重要了。没有一个人讲到摆臂的，所以我很重视这个摆臂。摆臂非常非常重要。",
         "sentences": [
            ["跑步要稳定，摆臂很关键。", "Stable running starts with the arm swing.", "arm swing（摆臂）"],
            ["很少有人讲摆臂，但它极其重要。", "Few teach the arm swing, yet it matters most.", "matter most（最重要）"]
         ]},
        {"id": "s2", "scene_zh": "准备姿势", "scene_en": "The Setup", "time": "00:08",
         "context": "一前一后站好，重心在前腿上，脚踝、膝关节、头部在一条垂直线。小臂和大臂成90度。大拇指扣在食指和中指之上，手握空拳，拳心朝上。",
         "sentences": [
            ["一前一后站好，重心在前腿上。", "Stagger your stance with weight on the front leg.", "stagger（前后错开）"],
            ["脚踝、膝关节、头在一条垂直线上。", "Keep ankle, knee and head on one vertical line.", "vertical line（垂直线）"],
            ["小臂和大臂成90度，手握空拳。", "Keep the forearm at 90 degrees with a loose fist.", "loose fist（空拳）"]
         ]},
        {"id": "s3", "scene_zh": "前摆最高：虎口到鼻尖", "scene_en": "Forward Swing: Thumb to Nose", "time": "00:20",
         "context": "找到人体的中间线，双手合十下来到鼻尖。前摆最高，虎口摆到鼻尖。小臂在胸前是倾斜的，肘在肚子前面，紧跟腰对一条直线。",
         "sentences": [
            ["前摆最高，虎口摆到鼻尖。", "At the top of the forward swing, the thumb reaches the nose.", "thumb（虎口）"],
            ["小臂在胸前是倾斜的，肘在肚子前面。", "The forearm tilts across the chest with the elbow ahead of the belly.", "tilt（倾斜）"],
            ["肘紧跟腰，保持一条直线。", "Keep the elbow close to the waist, in one line.", "close to the waist（贴近腰）"]
         ]},
        {"id": "s4", "scene_zh": "后摆：肩肘带动", "scene_en": "The Backswing: Driven by the Shoulder", "time": "00:36",
         "context": "后摆的时候，手腕不动、肘不动，肩肘带动。90度不变，肘贴近腰向后提起，前后大摆臂。",
         "sentences": [
            ["后摆时手腕和肘不动，肩肘带动。", "In the backswing, keep wrist and elbow still and drive from the shoulder.", "drive from the shoulder（肩肘带动）"],
            ["90度不变，肘贴近腰向后提起。", "Hold 90 degrees and pull the elbow back near the waist.", "pull back（向后提）"]
         ]},
        {"id": "s5", "scene_zh": "别摆过鼻尖", "scene_en": "Don't Swing Past the Nose", "time": "00:44",
         "context": "不要摆过鼻尖，摆过了就会后仰。肘贴近腰就会没有晃动；离腰一远，就会晃了。紧跟腰对立起来，一看就是打乒乓球的模式。",
         "sentences": [
            ["摆过鼻尖就会后仰。", "Swinging past the nose makes you lean back.", "lean back（后仰）"],
            ["肘贴近腰就没晃动，离腰远就晃。", "Elbow close to the waist kills the wobble; away from it, you wobble.", "wobble（晃动）"]
         ]},
        {"id": "s6", "scene_zh": "大摆臂与长跑摆臂", "scene_en": "Big Swings vs Marathon Swings", "time": "01:04",
         "context": "大摆臂用到哪里呢？用到短跑、间歇跑和上坡跑、冲刺跑。在马拉松长跑当中也是同样的摆臂，只是幅度小了一点。以身体躯干为轴，前不露肘、后不露手，肘不超过肚皮、肘不超过后背，也是贴近腰，前后自然摆动。",
         "sentences": [
            ["大摆臂用于短跑、间歇跑和冲刺跑。", "Big swings suit sprints, intervals and finishing kicks.", "sprint（冲刺）"],
            ["马拉松同样摆臂，只是幅度更小。", "Marathons use the same swing, just smaller.", "smaller amplitude（更小幅度）"],
            ["以躯干为轴，前不露肘后不露手。", "Pivot on the torso—no elbow forward, no hand back.", "pivot（轴心）"]
         ]}
    ]
}

ARTICLES["hike-route-difficulty"] = {
    "title_zh": "徒步路线难度怎么看？别再只看公里数",
    "title_en": "How to Judge Trail Difficulty—Not Just Kilometers",
    "duration": "3分17秒",
    "topic": "户外 · 徒步",
    "scenes": [
        {"id": "s1", "scene_zh": "公里数会骗人", "scene_en": "Kilometers Can Lie", "time": "00:00",
         "context": "看别人推荐路线最常见的描述是15公里、中等难度。但同样的15公里，累计爬升300和累计爬升1500，是天差地别的两种体验。判断一条路线关键不在公里，而是另外三个数字。",
         "sentences": [
            ["同样15公里，爬升300和1500是天差地别。", "The same 15km with 300 vs 1500 meters of climb feels worlds apart.", "climb（爬升）"],
            ["判断路线关键不在公里，而是三个数字。", "Judging a trail is about three numbers, not distance.", "trail（路线）"]
         ]},
        {"id": "s2", "scene_zh": "数字一：累计爬升", "scene_en": "Number 1: Total Climb", "time": "00:29",
         "context": "累计爬升比公里数更直接影响你的体力。公里数告诉你走多远，累计爬升告诉你每走一步要花多少力气。300爬升摊到15公里，平均每公里爬升20米，几乎感觉不到坡度；800爬升摊到8公里，每公里100米，相当于1公里爬10层楼。",
         "sentences": [
            ["公里数说走多远，爬升说每步花多大力。", "Distance says how far; climb says how hard each step is.", "distance（距离）"],
            ["每公里爬升20米，几乎感觉不到坡度。", "20m per kilometer feels almost flat.", "flat（平坦）"],
            ["每公里爬升100米，相当于1公里爬10层楼。", "100m per kilometer equals ten floors every kilometer.", "ten floors（10层楼）"]
         ]},
        {"id": "s3", "scene_zh": "爬升判断标准", "scene_en": "Climb Benchmarks", "time": "00:53",
         "context": "一个简单的判断方法：累计爬升小于500米一天，只要平时有走路习惯基本能走完；500到1000米一天，需要规律的日常运动，走完会累但可以应对；1000米一天，需要提前做体能准备，不是临时起意就能走的。",
         "sentences": [
            ["爬升小于500米，有走路习惯就能走完。", "Under 500m of climb, a daily-walking habit is enough.", "daily-walking habit（走路习惯）"],
            ["500到1000米，需要规律运动。", "500 to 1000m needs regular exercise.", "regular exercise（规律运动）"],
            ["1000米以上，要提前做体能准备。", "Beyond 1000m, prepare your fitness in advance.", "prepare（准备）"]
         ]},
        {"id": "s4", "scene_zh": "数字二：海拔变化速度", "scene_en": "Number 2: Altitude and Its Pace", "time": "00:35",
         "context": "很多人看海拔只看最高点，比如最高海拔4000，这个信息其实没什么用。关键看两个东西：起点海拔和海拔上升的速度。从500米出发走到4000米，和从3000米出发走到4000米，虽然最高点一样，身体感受完全不同。",
         "sentences": [
            ["只看最高海拔4000，其实没什么用。", "Looking only at a 4000m peak tells you little.", "peak（最高点）"],
            ["关键看起点海拔和上升速度。", "What matters is the start elevation and how fast you rise.", "start elevation（起点海拔）"],
            ["从500米和从3000米到4000米，感受完全不同。", "Starting at 500 vs 3000m to reach 4000m feels totally different.", "totally different（完全不同）"]
         ]},
        {"id": "s5", "scene_zh": "高海拔的代价", "scene_en": "The Cost of Altitude", "time": "00:41",
         "context": "海拔升高，血液氧气含量下降，肌肉在缺氧环境下的力量会打折。走同样的坡度，在高海拔要多花30%到50%的力气。而且缺氧会让判断力和协调性也下降，这就是为什么有些人3000米以下走得飞快，一过3500就慢了下来。",
         "sentences": [
            ["海拔升高，血液氧含量下降。", "Higher altitude drops the oxygen in your blood.", "oxygen（氧气）"],
            ["同样的坡度，高海拔多花30%到50%力气。", "The same slope costs 30-50% more effort up high.", "effort（力气）"],
            ["缺氧连判断力和协调性都会下降。", "Low oxygen even dulls judgment and coordination.", "judgment（判断力）"]
         ]},
        {"id": "s6", "scene_zh": "海拔适应节奏", "scene_en": "Acclimatization Pace", "time": "00:58",
         "context": "给自己一个参考：3000米以下，大部分人适应几天就能正常走；3000到4000米，给身体一两天的适应时间，慢一点没有关系；4000米以上，适应时间就会更长。每天上升不超过500米海拔是比较安全的节奏。",
         "sentences": [
            ["3000米以下，适应几天就能正常走。", "Below 3000m, a few days of acclimatization works.", "acclimatization（适应）"],
            ["3000到4000米，给身体一两天适应。", "3000-4000m needs a day or two to adjust.", "adjust（调整）"],
            ["每天上升不超过500米，比较安全。", "Gaining no more than 500m a day is the safe pace.", "safe pace（安全节奏）"]
         ]},
        {"id": "s7", "scene_zh": "数字三：路况", "scene_en": "Number 3: Trail Surface", "time": "00:13",
         "context": "路况是最容易被新手忽略、但对体力影响不亚于爬升的维度。同样10公里：走台阶路，膝盖反复做同一角度的屈伸，3公里之后髌骨压力开始累积；走碎石路，每一步脚踝都在调整，小腿小肌群一直工作；走泥路或湿滑路面，摩擦力不稳定，核心肌群会比你预想地累得更快。",
         "sentences": [
            ["走台阶路，膝盖反复屈伸，髌骨压力累积。", "Stairs repeat the same knee bend and build patella pressure.", "patella（髌骨）"],
            ["走碎石路，每一步脚踝都在调整。", "Scree keeps your ankles adjusting every step.", "scree（碎石）"],
            ["走泥路，核心比预想更快累。", "Mud tires out your core faster than expected.", "tire out（累垮）"]
         ]},
        {"id": "s8", "scene_zh": "看路线问三个问题", "scene_en": "Ask Three Questions", "time": "00:55",
         "context": "我在出凤东坡暴雪时，雪深到膝盖，体力消耗是平时的两到三倍，每一步都要先把脚从雪里拔出来。所以下次看路线要问自己：累计爬升是多少，有没有超过平时运动量？起点海拔多少，一天之内要上升多少？路面是什么，台阶、碎石还是泥路？三个数字都对得上自己的体能，才是一条真正适合你的路线。",
         "sentences": [
            ["暴雪中每一步都要把脚从雪里拔出来。", "In deep snow every step means pulling your foot free.", "pull free（拔出）"],
            ["问自己：累计爬升多少？", "Ask: how much total climb?", "total climb（累计爬升）"],
            ["起点海拔多少，一天上升多少？", "What's the start elevation and daily gain?", "daily gain（每日上升）"],
            ["路面是台阶、碎石还是泥路？", "Is the surface stairs, scree or mud?", "surface（路面）"],
            ["装备是加分项，体能与认知才是基础。", "Gear is a bonus; fitness and awareness are the base.", "bonus（加分项）"]
         ]}
    ]
}

ARTICLES["huanjing-yuecha-weimei"] = {
    "title_zh": "环境越差，照片越唯美~",
    "title_en": "The Worse the Spot, the Prettier the Photo",
    "duration": "2分02秒",
    "topic": "摄影 · 拍摄环境",
    "scenes": [
        {"id": "s1", "scene_zh": "看似无料的荒草地", "scene_en": "The Seemingly Empty Field", "time": "00:02",
         "context": "这是我的拍摄环境，在这个位置放一个美女。开场取景：看似无料的荒草地，红框标出「放一个美女」的站位。普通甚至被忽视的环境，也能成为拍摄场地。",
         "sentences": [
            ["这是我的拍摄环境，在这个位置放一个美女。", "This is my shooting spot—place a model right here.", "shooting spot（拍摄场地）"],
            ["看似无料的荒草地，红框标出站位。", "A seemingly empty field, with the model's spot marked.", "mark（标出）"]
         ]},
        {"id": "s2", "scene_zh": "园林·海边·羊圈", "scene_en": "Gardens, Shores and Barns", "time": "00:07",
         "context": "切到园林现场：石桥与柳枝遮住的亭阁，仍叠同一句提示。海边礁石浅滩，环境朴素，仍被标为拍摄场地。更「土」的现场：棚下羊圈、塑料桶与摩托车，作者蹲低取景。",
         "sentences": [
            ["园林里石桥亭阁，也标为拍摄场地。", "A garden bridge and pavilion also make the list.", "pavilion（亭阁）"],
            ["海边礁石浅滩，环境朴素也出片。", "A plain rocky shore still works as a set.", "set（场地）"],
            ["羊圈、塑料桶、摩托车，蹲低取景。", "A barn with barrels and a bike—crouch low and shoot.", "crouch（蹲低）"]
         ]},
        {"id": "s3", "scene_zh": "村路茅棚与花树木桥", "scene_en": "Village Shacks and Blossoms", "time": "00:28",
         "context": "村路茅棚：开口处被当作模特站位，环境简陋但构图方向明确。花树与木桥：景更好看，方法仍是红框定点加同一句口播。方法不变，效果照旧。",
         "sentences": [
            ["茅棚开口处当站位，简陋但构图明确。", "A shack's opening frames the model—rough yet clear.", "frame（构图）"],
            ["景更好看，方法仍是红框定点。", "Prettier scenery, same marked-spot method.", "marked-spot（定点）"]
         ]},
        {"id": "s4", "scene_zh": "普通环境也能出大片", "scene_en": "Ordinary Places, Great Shots", "time": "01:22",
         "context": "总结起句叠在成片上：普通环境也能走出「江山美人」式画面。这些拍摄环境看起来非常普通，甚至很容易被忽视，如果你想拍出好作品，不要过分关注相机和镜头。",
         "sentences": [
            ["普通环境也能走出「江山美人」式画面。", "Ordinary spots can still deliver epic, painterly shots.", "painterly（唯美的）"],
            ["别把好作品寄托在相机和镜头上。", "Don't pin great work on the camera and lens.", "pin on（寄托）"]
         ]},
        {"id": "s5", "scene_zh": "新手纠结器材，高手关注什么", "scene_en": "Rookies Chase Gear; Pros Watch This", "time": "01:30",
         "context": "很多新手入门时浪费大量时间讨论相机品牌、做工、参数、型号、手感、对焦、像素、锐度、色彩——这些本来是相机厂家应该研究的。并不是有了高档相机就能拍出好照片。光线、天气、服装、环境、后期、思维模式、构图、拍摄时机、引导模特——这些才是我们真正应该关注的。",
         "sentences": [
            ["新手浪费时间讨论相机品牌和参数。", "Rookies burn hours on camera brands and specs.", "specs（参数）"],
            ["不是有了高档相机就能拍出好照片。", "A fancy camera alone won't make good photos.", "fancy（高档的）"],
            ["光线、天气、构图、时机，才是真正要学的。", "Light, weather, composition and timing are the real lessons.", "composition（构图）"]
         ]}
    ]
}

ARTICLES["rope-face-tracking-mobile7p"] = {
    "title_zh": "一根绳子+手机稳定器人脸追踪还能这样玩",
    "title_en": "A Rope + Phone Gimbal Face Tracking? Try This",
    "duration": "17秒",
    "topic": "摄影 · 创意拍摄",
    "scenes": [
        {"id": "s1", "scene_zh": "成片效果与幕后布置", "scene_en": "The Shot and the Rig", "time": "00:01",
         "context": "开场对比：成片举手特写（上）与树旁稳定器实拍（下），先交代「拍什么」和「怎么架」。用一根绳子加手机稳定器的人脸追踪，拍出跟随感十足的镜头。",
         "sentences": [
            ["上为成片举手特写，下为树旁实拍。", "Top: the finished close-up. Bottom: the gimbal rig by the tree.", "rig（布置）"],
            ["一根绳子加稳定器追踪，拍出跟随感。", "A rope plus a tracking gimbal creates the follow shot.", "follow shot（跟随镜头）"]
         ]},
        {"id": "s2", "scene_zh": "远去与侧面跟随", "scene_en": "Receding and Side Tracking", "time": "00:04",
         "context": "远去段落：上为跟随背影，下为高机位路径，展示追踪下的景别切换。侧面跟随与俯视同构，强调主体移动时构图仍稳定。",
         "sentences": [
            ["跟随背影远去，景别随追踪切换。", "The receding back view shifts with the tracking.", "recede（远去）"],
            ["侧面跟随与俯视同构，构图稳定。", "Side tracking mirrors the top view—framing stays stable.", "stable framing（稳定构图）"]
         ]},
        {"id": "s3", "scene_zh": "绳子轨迹与幕后机关", "scene_en": "The Rope's Trail and the Crew", "time": "00:12",
         "context": "广角下露出斜向细线：绳子轨迹第一次清楚进画。下方橙衣人员与横穿绳索，印证「绳子+稳定器」的幕后布置。收尾用近景迎面与含绳线的宽景，把氛围感与幕后机关收在同一帧。",
         "sentences": [
            ["广角下，绳子的斜向细线终于入画。", "At wide angle, the rope's diagonal line finally appears.", "diagonal（斜向）"],
            ["橙衣人员和横穿绳索，暴露了幕后机关。", "The crew and the crossing rope reveal the trick.", "reveal（揭穿）"],
            ["收尾把氛围感和幕后机关收在同一帧。", "The ending blends mood and the rig in one frame.", "mood（氛围感）"]
         ]}
    ]
}

ARTICLES["buguang-guangwei-tips"] = {
    "title_zh": "布光很难？其实就这几个光位来回用！",
    "title_en": "Lighting Isn't Hard—Just These Positions",
    "duration": "38秒",
    "topic": "摄影 · 布光",
    "scenes": [
        {"id": "s1", "scene_zh": "逆光表现通透", "scene_en": "Backlight for Translucency", "time": "00:01",
         "context": "不通透，打逆光，表现层次。逆光穿过瓶身，液体与瓶壁开始显出通透层次。逆光是让透明材质发光的关键光位。",
         "sentences": [
            ["不通透？打逆光表现层次。", "Looks flat? Use backlight to bring out layers.", "backlight（逆光）"],
            ["逆光穿过瓶身，液体显出通透。", "Light passing through the bottle makes the liquid glow.", "translucent（通透的）"]
         ]},
        {"id": "s2", "scene_zh": "双灯切高光", "scene_en": "Two Lights, Sharp Highlights", "time": "00:03",
         "context": "玻璃质感，切高光。现场双灯布置：一盏主控高光，一盏从后方透射补充层次。成片示意「单边锋利有过渡」：瓶肩高光窄而干净，边缘仍有柔和过渡。",
         "sentences": [
            ["双灯布置：一盏主控高光，一盏后方透射。", "Two lights: one keys the highlight, one backlights for depth.", "key（主光）"],
            ["单边锋利有过渡：高光窄而干净。", "Sharp on one edge with a soft falloff—clean, narrow highlights.", "falloff（过渡）"]
         ]},
        {"id": "s3", "scene_zh": "硫酸纸闭杂光", "scene_en": "Diffusion Paper Cleans Stray Light", "time": "00:09",
         "context": "反光强用硫酸纸，表面光洁，闭杂光。布光现场强调表面干净、少杂光，为高光形状做准备。",
         "sentences": [
            ["反光强，用硫酸纸柔化。", "Strong reflections call for diffusion paper.", "diffusion（柔光）"],
            ["表面光洁，杂光越少越好。", "Keep the surface clean with as little stray light as possible.", "stray light（杂光）"]
         ]},
        {"id": "s4", "scene_zh": "轮廓光抠出黑中有黑", "scene_en": "Rim Light Cuts Out of the Dark", "time": "00:14",
         "context": "黑中有黑，用轮廓光，两边各一个。轮廓光把深色手电筒从暗背景里「抠」出来。窄高光，边缘发灰。",
         "sentences": [
            ["黑中有黑，用轮廓光，两边各一个。", "For black-on-black, add rim lights on both sides.", "rim light（轮廓光）"],
            ["轮廓光把深色物体从暗背景里抠出来。", "Rim light cuts the dark object out of the dark.", "cut out（抠出）"]
         ]},
        {"id": "s5", "scene_zh": "黑卡纸描黑边", "scene_en": "Black Cards Add Edge Lines", "time": "00:20",
         "context": "用黑卡纸给产品两侧描黑边。黑卡纸辅助后，透明瓶两侧出现更清晰的黑边轮廓，勾勒出立体感。",
         "sentences": [
            ["用黑卡纸给产品两侧描黑边。", "Black cards trace dark edges along both sides.", "trace（描边）"],
            ["透明瓶两侧出现清晰黑边，立体感更强。", "The clear bottle gains cleaner edges for more depth.", "depth（立体感）"]
         ]},
        {"id": "s6", "scene_zh": "裸灯打光影", "scene_en": "Bare Light for Hard Shadows", "time": "00:23",
         "context": "光影太平没层次，用裸灯打光影。裸灯近距离打光，阴影更硬、对比更强，明暗强烈有冲击力。",
         "sentences": [
            ["光影太平没层次？用裸灯。", "Flat and dull? Go with a bare light.", "bare light（裸灯）"],
            ["裸灯近距离，阴影更硬、对比更强。", "A bare light up close makes harder shadows and stronger contrast.", "contrast（对比）"]
         ]},
        {"id": "s7", "scene_zh": "单灯+反光板", "scene_en": "One Light Plus Reflectors", "time": "00:30",
         "context": "单灯拍，用天目光，操作反而更简单。目光就用反光板，大部分产品都能拍。单灯加两侧反光板：少器材也能控亮暗与反光。",
         "sentences": [
            ["单灯加天目光，操作反而更简单。", "One light plus a fill—simpler than you think.", "fill（补光）"],
            ["反光板就能控亮暗，大部分产品都能拍。", "Reflectors control the tones—works for most products.", "reflector（反光板）"]
         ]}
    ]
}

ARTICLES["chekuai-renman-tutorial"] = {
    "title_zh": "车快人慢教程",
    "title_en": "Car-Fast, Person-Slow Tutorial",
    "duration": "44秒",
    "topic": "摄影 · 拍摄技巧",
    "scenes": [
        {"id": "s1", "scene_zh": "拍两段素材", "scene_en": "Shoot Two Clips", "time": "00:02",
         "context": "像这样的车快人慢视频是怎么拍的？很简单，固定手机，先拍一段人物迎面走来的视频，保持机位不动，用延时摄影功能再拍一段10分钟左右的车流视频。",
         "sentences": [
            ["固定手机，先拍人物迎面走来的视频。", "Fix the phone and film the person walking toward you.", "walk toward（迎面走来）"],
            ["保持机位不动，用延时摄影拍10分钟车流。", "Keep the camera still and time-lapse 10 minutes of traffic.", "time-lapse（延时摄影）"]
         ]},
        {"id": "s2", "scene_zh": "画中画+变速", "scene_en": "Picture-in-Picture and Speed", "time": "00:11",
         "context": "依次导入两段视频，将人物视频切画中画，再点变速，将速度调至0.3左右，并勾选智能补帧。车流是延时快放，人物是0.3倍慢放，形成快慢对比。",
         "sentences": [
            ["人物视频切画中画。", "Turn the person clip into picture-in-picture.", "picture-in-picture（画中画）"],
            ["速度调到0.3左右，勾选智能补帧。", "Drop the speed to about 0.3 and enable frame interpolation.", "frame interpolation（智能补帧）"]
         ]},
        {"id": "s3", "scene_zh": "蒙版融合", "scene_en": "Mask It Together", "time": "00:18",
         "context": "再给画中画视频添加蒙版，选择线性，调整蒙版线放在人物与车流中间，轻按羽化让画面融合。最后添加音乐，删除结尾多余视频，导出看成品。",
         "sentences": [
            ["添加线性蒙版，把线放在人物与车流中间。", "Add a linear mask with the line between the person and the traffic.", "linear mask（线性蒙版）"],
            ["轻按羽化，让画面自然融合。", "Feather it softly to blend the frames.", "feather（羽化）"],
            ["加音乐，删掉结尾多余画面，导出。", "Add music, trim the tail and export.", "export（导出）"]
         ]}
    ]
}

ARTICLES["dual-native-iso"] = {
    "title_zh": "一个视频告诉你什么是双原生ISO",
    "title_en": "Dual Native ISO Explained in One Video",
    "duration": "2分15秒",
    "topic": "摄影 · 相机知识",
    "scenes": [
        {"id": "s1", "scene_zh": "两大技术：DCG与DGO", "scene_en": "Two Technologies: DCG and DGO", "time": "00:00",
         "context": "与ISO相关的名词有很多，一些名词的混用以及定义模糊造成了诸多奇异。其中争论最多的可能就是这两个：DCG双转换增益，和DGO双增益融合输出。",
         "sentences": [
            ["ISO相关名词混用，引发很多争议。", "Loose ISO terms cause plenty of confusion.", "confusion（混淆）"],
            ["两大技术：DCG双转换增益，DGO双增益融合输出。", "The two big ones: DCG dual-conversion gain and DGO dual-gain output.", "dual-conversion gain（双转换增益）"]
         ]},
        {"id": "s2", "scene_zh": "DCG：两个电容，两个基准ISO", "scene_en": "DCG: Two Capacitors, Two Base ISOs", "time": "00:17",
         "context": "电容CFD决定电荷到电压的转换增益。双转换增益其实就是设计两个电容，一大一小，这样就有了两个基准ISO。光线充足时用大电容，能接收更多的电子，电荷转换的电压小，也就是低转换增益，既保证了动态范围又能提升画质。",
         "sentences": [
            ["双转换增益=设计一大一小两个电容。", "Dual conversion gain means two capacitors, one big, one small.", "capacitor（电容）"],
            ["光线充足用大电容，接收更多电子。", "In bright light the big capacitor holds more electrons.", "hold（容纳）"],
            ["低转换增益，保证动态范围还提升画质。", "Low gain keeps dynamic range and lifts image quality.", "dynamic range（动态范围）"]
         ]},
        {"id": "s3", "scene_zh": "暗光切换小电容", "scene_en": "Low Light: Switch to the Small Cap", "time": "00:37",
         "context": "光线不足时切换小电容，由于能接收的电子很少，小电容可以让电荷直接转换成更高的电压，也就是高转换增益。",
         "sentences": [
            ["光线不足切小电容，直接转成更高电压。", "In dim light, the small capacitor converts charge to higher voltage.", "convert（转换）"],
            ["这就是高转换增益。", "That's the high conversion gain.", "high gain（高增益）"]
         ]},
        {"id": "s4", "scene_zh": "为什么暗光画质更好", "scene_en": "Why Low Light Gets Cleaner", "time": "00:46",
         "context": "假设ISO100，大电容把每个电子转换成10W的电压；提升到ISO800，只需要PGA放大8倍，电压变成80W每电子，这会造成前端电路的读出噪声也放大了8倍。如果在ISO800时切换到DCG的小电容，也就是第二档基准ISO，则能利用高转换增益，让每个电子直接转换成80W的电压，不需要PGA再执行放大，这样前端读出噪声也就不会放大，可以有效提升暗光画质。",
         "sentences": [
            ["ISO100升到800要PGA放大8倍，噪声也放大8倍。", "Going ISO100 to 800 needs 8x PGA gain—and 8x read noise.", "PGA（可编程增益放大器）"],
            ["切到第二档基准ISO，利用高转换增益。", "Switching to the second base ISO uses high conversion gain.", "base ISO（基准ISO）"],
            ["前端读出噪声不放大，暗光画质提升。", "Front-end read noise stays put, so low-light quality rises.", "read noise（读出噪声）"]
         ]},
        {"id": "s5", "scene_zh": "DGO：双路读出融合", "scene_en": "DGO: Dual-Path Readout Fusion", "time": "01:16",
         "context": "DGO与DCG有些不同，它是在电容之后分成两条读出电路，把同一批电荷转换出两路电压信号。例如ISO800时，一路信号做8倍模拟放大，一路不放大用低增益，再分别有两个ADC读出，后期这两路信号会做融合处理。",
         "sentences": [
            ["DGO在电容后分成两条读出电路。", "DGO splits into two readout paths after the capacitor.", "readout path（读出电路）"],
            ["同一批电荷转换出两路电压信号。", "One batch of charge becomes two voltage signals.", "signal（信号）"],
            ["一路8倍放大，一路低增益，双ADC读出。", "One path at 8x, one at low gain, read by two ADCs.", "ADC（模数转换器）"]
         ]},
        {"id": "s6", "scene_zh": "融合保高光加暗部", "scene_en": "Fusion: Highlights Plus Shadows", "time": "01:32",
         "context": "低增益下保证了高光细节，而高增益则能记录更多的暗部信息，以此来有效提升动态范围。DGO的优势在于能够大幅提升动态范围，但是对比暗光场景则是DCG更有优势。",
         "sentences": [
            ["低增益保高光，高增益记暗部。", "Low gain keeps highlights; high gain saves shadows.", "highlight（高光）"],
            ["融合后有效提升动态范围。", "The fusion effectively widens the dynamic range.", "widen（拓宽）"],
            ["DGO强在动态范围，DCG强在暗光。", "DGO excels at range; DCG wins in low light.", "excel（擅长）"]
         ]},
        {"id": "s7", "scene_zh": "命名与使用建议", "scene_en": "Naming and Practical Advice", "time": "01:47",
         "context": "DCG和DGO翻译过来都可以叫双增益，只是技术路径有所不同。ISO的本质又是增益，所以称两者为双原生ISO也合乎逻辑。具体讨论可以用技术名称，泛制则沿用ISO，毕竟ISO这个符号的诞生就是为了统一标准、易于传播。",
         "sentences": [
            ["DCG和DGO都可以叫双增益。", "Both DCG and DGO translate as dual gain.", "dual gain（双增益）"],
            ["称两者为双原生ISO也合乎逻辑。", "Calling either “dual native ISO” is logical.", "dual native ISO（双原生ISO）"],
            ["具体讨论用技术名，泛制沿用ISO。", "Use technical names in depth; keep ISO in general talk.", "technical name（技术名称）"]
         ]}
    ]
}

ARTICLES["huoren-yunjing-3tips"] = {
    "title_zh": "3个活人感运镜，1招拯救你的坏视频",
    "title_en": "3 Camera Moves That Make Videos Feel Alive",
    "duration": "3分48秒",
    "topic": "摄影 · 运镜",
    "scenes": [
        {"id": "s1", "scene_zh": "要人、要景、要活人感", "scene_en": "People, Place and Life", "time": "00:00",
         "context": "旅行第三天，女朋友不理我了，因为出片。她要的既有背脚拍进去，又要有人又有景，还有活人感。先找到运镜思路：从人物开始运镜，自然过渡到身后的场景，就同时展现了人物和景色。",
         "sentences": [
            ["既要有人物，又要有景色，还要活人感。", "She wants the person, the place and a sense of life.", "sense of life（活人感）"],
            ["从人物开始运镜，自然过渡到身后场景。", "Start on the person and glide to the scene behind.", "glide（滑动）"]
         ]},
        {"id": "s2", "scene_zh": "推镜头", "scene_en": "The Push-In", "time": "00:42",
         "context": "这些画面都是简单的推镜头。推镜头可以拉近你和人物之间物理和内心的距离，同时也增强一种期待的感觉。旅行的时候就应该多拍些推镜头，它是一个很符合视觉逻辑的简单运镜。当镜头不断往前推的时候，就有一种很自然的去靠近人物的感觉，而且拍起来根本不需要技巧，只需要把相机拿稳然后慢慢往前走。",
         "sentences": [
            ["推镜头拉近物理和内心的距离。", "The push-in closes both physical and emotional distance.", "push-in（推镜头）"],
            ["它增强期待感，符合视觉逻辑。", "It builds anticipation and fits visual logic.", "anticipation（期待感）"],
            ["只需要拿稳相机慢慢往前走。", "Just hold the camera steady and walk forward.", "steady（稳）"]
         ]},
        {"id": "s3", "scene_zh": "拉镜头", "scene_en": "The Pull-Back", "time": "00:13",
         "context": "和推镜头完全相反的就是拉镜头。镜头在向后拉的过程中，画面变得越来越广阔。旅拍时用拉镜头，随着景别变化，观众可以看到的信息越来越多。人物虽然没有做特别有趣的动作，但因为镜头一直在移动，整个画面也变得有趣了。",
         "sentences": [
            ["拉镜头让画面越来越广阔。", "The pull-back opens up a wider world.", "pull-back（拉镜头）"],
            ["景别变化，观众看到的信息越来越多。", "As the shot widens, viewers absorb more and more.", "absorb（接收）"],
            ["镜头在动，画面就变有趣。", "A moving camera alone makes the shot engaging.", "engaging（有趣的）"]
         ]},
        {"id": "s4", "scene_zh": "拉镜头的氛围感与结尾", "scene_en": "The Pull-Back as Mood and Ending", "time": "00:45",
         "context": "来到一个特别好看的场景，第一个反应是让人站进去拍。如果用拉镜头来拍，从细节开始再过渡到整个场景，就更能体现氛围感。这个时候再让人物离开画面，就是一个很好的vlog结尾。",
         "sentences": [
            ["从细节开始，再过渡到整个场景。", "Start on a detail, then open to the whole scene.", "open to（展开到）"],
            ["拉镜头更能体现氛围感。", "The pull-back brings out the atmosphere.", "atmosphere（氛围感）"],
            ["人物离开画面，就是很好的vlog结尾。", "The person leaving the frame makes a great vlog closer.", "closer（结尾）"]
         ]},
        {"id": "s5", "scene_zh": "环绕运镜", "scene_en": "The Orbit", "time": "00:03",
         "context": "还有一种更特别的运镜：环绕运镜。让人物保持一定距离，先从远景开始拍，然后慢慢环绕运镜去拍它的侧脸。这个镜头的秘诀就是环绕的时候，人物目光能一点跟着镜头的方向一起移动。这个运镜完全不挑场景，而且拍出来就有氛围感。",
         "sentences": [
            ["从远景开始，慢慢环绕拍侧脸。", "Start wide, then orbit in toward the profile.", "orbit（环绕）"],
            ["秘诀：人物的目光跟着镜头方向移动。", "The trick: the subject's gaze follows the camera.", "gaze（目光）"],
            ["完全不挑场景，拍出来就有氛围感。", "It fits any scene and instantly feels cinematic.", "fit any scene（不挑场景）"]
         ]},
        {"id": "s6", "scene_zh": "环绕的优点", "scene_en": "Why Orbit Wins", "time": "00:19",
         "context": "环绕拍摄比起推进来说还有一个好处：它不需要特别大范围的移动。像在展露上，或者随意切换到比较空旷的场地，都是可以去无脑拍的一个简单运镜。",
         "sentences": [
            ["环绕不需要大范围移动。", "Orbiting needs no large-scale movement.", "large-scale（大范围）"],
            ["在展台或空旷场地，都能无脑拍。", "On a stage or an open field, it's a foolproof shot.", "foolproof（无脑）"]
         ]},
        {"id": "s7", "scene_zh": "追踪模块救场", "scene_en": "The Tracking Module Saves You", "time": "00:45",
         "context": "大幅度运镜时画面容易跑偏。如果不想花时间去练习稳定器运镜，可以利用追踪模块帮助运镜。比如R45的增强智能追踪模块，只需要在屏幕上框选一下就可以开启追踪，不仅可以追踪人，还可以追踪物体包括小动物。现在就不需要什么技巧，几乎可以闭着眼睛运镜。",
         "sentences": [
            ["大幅度运镜画面容易跑偏。", "Big moves tend to drift off frame.", "drift（跑偏）"],
            ["屏幕框选一下，即可开启追踪。", "Box the subject on screen to start tracking.", "box（框选）"],
            ["不仅能追踪人，还能追踪物体和小动物。", "It tracks people, objects and even pets.", "track（追踪）"]
         ]},
        {"id": "s8", "scene_zh": "档位选择", "scene_en": "Choosing the Right Mode", "time": "00:10",
         "context": "稳定器的模式比较重要。无论手机稳定器还是专业稳定器，只有把档位调对，拍摄时画面才会更稳定。环绕运镜或跟随人物，只要在同一个水平线上，可以调整PF模式；想拍摇镜头，比如先跟随人物再上摇或下摇，可以调整PTF模式。",
         "sentences": [
            ["档位调对，画面才稳定。", "The right mode keeps the shot stable.", "mode（档位）"],
            ["同一水平线用PF，环绕跟随都行。", "PF mode handles orbits and follows on one level.", "PF mode（PF模式）"],
            ["拍摇镜头上摇下摇，用PTF。", "For pans and tilts, switch to PTF.", "PTF mode（PTF模式）"]
         ]},
        {"id": "s9", "scene_zh": "Z轴稳定指示器", "scene_en": "The Z-Axis Stability Meter", "time": "00:33",
         "context": "R45还有Z轴稳定指示器的功能。如果你上架抖动比较厉害，它就会变成红色；如果你的步伐比较稳定，它就会变成绿色。这个小功能很有意思：运镜的时候就会不自觉想走得更稳定一些。",
         "sentences": [
            ["抖动厉害时，指示器变红。", "Heavy shake turns the indicator red.", "indicator（指示器）"],
            ["步伐稳定时，指示器变绿。", "A steady gait turns it green.", "gait（步伐）"],
            ["看着颜色，就会不自觉走得更稳。", "Watching the color makes you walk steadier by habit.", "by habit（不自觉地）"]
         ]}
    ]
}

ARTICLES["travel-10-transitions-2"] = {
    "title_zh": "1分钟学会10种旅行神级转场！",
    "title_en": "10 Pro Travel Transitions in 1 Minute",
    "duration": "1分22秒",
    "topic": "摄影 · 运镜转场",
    "scenes": [
        {"id": "s1", "scene_zh": "擦身而过转场", "scene_en": "The Brush-Past Cut", "time": "00:00",
         "context": "第一种可以在擦身而过时变换任何场景的神器转场。秘诀就在于用身体挡住镜头的一瞬间切换画面。恭喜你，现在你学会了利用遮挡物进行转场。",
         "sentences": [
            ["擦身而过，用身体挡住镜头的一瞬间切换。", "Brush past and switch shots the instant your body blocks the lens.", "block（遮挡）"],
            ["这是利用遮挡物进行转场。", "That's a transition using an obstacle.", "obstacle（遮挡物）"]
         ]},
        {"id": "s2", "scene_zh": "遮挡物的底层逻辑", "scene_en": "The Logic of Obstacles", "time": "00:11",
         "context": "你知道遮挡物有多重要？只需要随便找一个东西遮一下，你就可以轻松做出一个转场。现在你已经完全搞懂转场的底层逻辑了。",
         "sentences": [
            ["随便找一个东西遮一下，就能转场。", "Cover the lens with anything and you have a transition.", "cover（遮挡）"],
            ["这就是转场的底层逻辑。", "That's the underlying logic of transitions.", "underlying logic（底层逻辑）"]
         ]},
        {"id": "s3", "scene_zh": "没有遮挡物？自己造", "scene_en": "No Obstacle? Make One", "time": "00:18",
         "context": "如果身边没有合适的遮挡物该怎么办？就是自己造一个遮挡。在必要的时候，你就是遮挡物本身。比如用手机靠近电梯门，下一个画面用手指模仿电梯打开的样子，这样你就能一秒钟穿越到户外。或者直接用手臂做遮挡物，就可以从下班直接转场到你想去的地方。",
         "sentences": [
            ["没有遮挡物，就自己造一个。", "No obstacle around? Create one yourself.", "create（制造）"],
            ["必要的时候，你就是遮挡物本身。", "When needed, you are the obstacle.", "you are the obstacle（你是遮挡物）"],
            ["手机靠近电梯门，用手模仿电梯打开。", "Bring the phone to the elevator door, then mimic it with your hand.", "mimic（模仿）"],
            ["用手臂做遮挡，从下班转到任何地方。", "Your arm blocks the shot to jump anywhere.", "jump（转场）"]
         ]},
        {"id": "s4", "scene_zh": "敲击转场", "scene_en": "The Knock Cut", "time": "00:36",
         "context": "轻敲镜头，这样不就得到了一个敲击转场？敲击镜头的瞬间衔接两个场景，配合音效就是一个干净利落的转场。",
         "sentences": [
            ["敲击镜头，得到敲击转场。", "Tap the lens and you get the knock cut.", "tap（敲击）"]
         ]},
        {"id": "s5", "scene_zh": "甩镜头转场", "scene_en": "The Whip-Pan Cut", "time": "00:44",
         "context": "不用遮挡物的话还能拍转场吗？当然可以，我们可以用运镜来转场。像这样的甩镜头转场真的巨简单：只需要在第一个片段结尾，镜头甩向一边，然后再拍摄下一个片段时，从相反方向继续运镜，再把它们剪辑起来就可以了。",
         "sentences": [
            ["第一个片段结尾，镜头甩向一边。", "At the end of clip one, whip the camera to one side.", "whip（甩）"],
            ["下一个片段从相反方向继续运镜。", "Start the next clip moving from the opposite side.", "opposite（相反方向）"],
            ["剪辑拼接，就是一个转场。", "Cut them together and you have the transition.", "cut together（拼接）"]
         ]},
        {"id": "s6", "scene_zh": "相似动作转场", "scene_en": "The Match-Action Cut", "time": "00:55",
         "context": "还有一个更简单的方法：只需要在向后运镜的同时，让人物走进画面，在它回头看你的时候，转到下一个画面，继续向前走。",
         "sentences": [
            ["向后运镜的同时，让人物走进画面。", "Dolly back as the person walks into frame.", "dolly back（向后运镜）"],
            ["在它回头看你的时候切到下一个画面。", "Cut to the next shot the moment they turn to look.", "turn to look（回头）"]
         ]},
        {"id": "s7", "scene_zh": "转场的秘密：脑补", "scene_en": "The Secret: Your Brain Fills the Gap", "time": "01:03",
         "context": "明明是不同场景的两个画面，究竟如何做到完美衔接？我发现就是靠脑补。只要画面稍微有点联系感，人的大脑就会不自觉脑补接下来的内容。所以我们只需要做的就是画面之间的共多年：可以是通过相似动作、相似物体，甚至同一种运镜，都可以丝滑地转场。",
         "sentences": [
            ["只要画面有联系感，大脑就会脑补。", "A hint of connection and the brain fills in the rest.", "fill in（脑补）"],
            ["相似动作、相似物体、同一种运镜，都能转场。", "Similar moves, similar objects, even the same camera move work.", "similar（相似的）"],
            ["关于转场的秘密你都知道了。", "Now you know the secret of transitions.", "secret（秘密）"]
         ]}
    ]
}


def build(slug, art):
    full_scenes = []
    for s in art["scenes"]:
        sentences = s["sentences"]
        speak = " ".join(t[1] for t in sentences)
        paraphrase = []
        seen = set()
        for t in sentences:
            note = t[2]
            parts = [x.strip() for x in re.split(r"[（(]/", note) if x.strip()]
            if parts:
                key = parts[0].rstrip("）)")
                if key not in seen and len(key) <= 24:
                    paraphrase.append([key, key])
                    seen.add(key)
        if not paraphrase:
            paraphrase.append([sentences[0][2], sentences[0][2]])
        full_scenes.append({
            "id": s["id"],
            "title_cn": s["scene_zh"][:18] + ("…" if len(s["scene_zh"]) > 18 else ""),
            "title_en": s["scene_en"][:42] + ("…" if len(s["scene_en"]) > 42 else ""),
            "time": s["time"],
            "context": s["context"],
            "sentences": sentences,
            "paraphrase": paraphrase[:2],
            "speak": speak,
        })

    total_sents = sum(len(sc["sentences"]) for sc in full_scenes)
    words = []
    for sc in full_scenes:
        for t in sc["sentences"]:
            for m in re.findall(r"[A-Za-z]+(?:[-'][A-Za-z]+)*", t[1]):
                n = m.lower()
                if len(n) >= 6 and n not in words:
                    words.append(n)
    words = words[:30]
    if len(words) < 20:
        words = words + ["camera", "lighting", "composition", "transition", "moment", "swing", "tracking", "stability", "balance", "practice"][: 20 - len(words)]

    out = {
        "meta": {
            "slug": slug,
            "title": art["title_zh"],
            "title_en": art["title_en"],
            "duration": art["duration"],
            "scenes": len(full_scenes),
            "sentences": total_sents,
            "date": "2026-08-08",
            "platform": "xiaohongshu",
            "source_url": f"http://xhslink.cn/o/{slug}",
            "topic": art["topic"],
        },
        "scene_imgs": [f"shot-{i:02d}" for i in range(1, len(full_scenes) + 1)],
        "scenes": full_scenes,
        "practice": art.get("practice", []),
        "pitfalls": art.get("pitfalls", []),
        "shifts": art.get("shifts", []),
        "difficult_words": words,
        "footer_notes": art.get("footer", ""),
    }
    p = DATA / f"{slug}.json"
    p.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ {slug}: {len(full_scenes)} scenes, {total_sents} sents, {len(words)} words")


for slug, art in ARTICLES.items():
    build(slug, art)
print("完成")
