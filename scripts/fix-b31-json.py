#!/usr/bin/env python3
"""批31：为10篇相机基础知识JSON补全 practice/pitfalls/shifts/footer_notes。"""
import json
from pathlib import Path

DATA = Path("/Users/chenzhiheng/Projects/bilibili-workshop/scripts/scene-data")

ENRICH = {
"camera-dynamic-range": {
  "practice": [
    ["说过曝的本质", "Pixels that pass their full-well capacity just lose the extra photons."],
    ["说动态范围定义", "Dynamic range is the brightest over the darkest you can record."],
    ["说档位换算", "Doubling the light coming in is exactly one stop."],
    ["说高ISO的代价", "Cranking ISO narrows the ADC window, so the dynamic range shrinks."],
    ["说基准ISO读出噪声", "At base ISO the read noise is only a few electrons."]
  ],
  "pitfalls": [
    ["Blame ISO for adding the light.", "ISO only brightens the signal—the aperture and shutter decide the light.", "ISO不改变进光量。"],
    ["Think every stop is fixed forever.", "A stop is always a doubling, but a sensor's range changes with ISO.", "一档永远是加倍，但动态范围随ISO变化。"],
    ["Expect consumer cameras to match cinema.", "Most consumer bodies top out around 13 stops, cinema closer to 17.", "消费级相机一般只有13档左右。"],
    ["Forget read noise exists at base ISO.", "Even with no light the sensor reads a few electrons of floor noise.", "没有光也有底噪。"],
    ["Crank ISO to make a dark shot safe.", "You trade away highlight room—the effective well capacity drops.", "提ISO会压缩高光保留能力。"]
  ],
  "shifts": [
    ["说过曝只说过曝", "用 full-well capacity（满阱容量）、clipping（裁切）、losing highlights（丢失高光）"],
    ["说动态范围只说动态范围", "用 brightest vs darkest（最亮与最暗）、read noise（读出噪声）、stops（档位）"],
    ["说ISO只说ISO", "用 PGA gain（PGA增益）、ADC window（ADC窗口）、base ISO（基准ISO）"]
  ],
  "footer": "转录基于图文实录完整口播。已校正：传感器里几千万个像素用来感光、光子越多像素越亮、单个像素容纳电子最大值为满阱容量、超出部分无法记录就是过曝、没有信号时CMOS也有底噪近似读出噪声、满阱容量与读出噪声的比值就是动态范围、主流消费级相机约13档、电影机能到16.7档、档指曝光指数两倍为一档、1/100秒与1/200秒或F1.4与F2都差一档、ISO改变亮度但不改变进光量、真正决定进光量只有光圈快门、A7M4满阱72000电子基准ISO读出噪声约5个电子、往上推一档10个两档20个直到最大72000差不多13.8档、提高ISO动态范围会降低、ADC能接收最大电压有上限、PGA模拟放大两倍即ISO200、电压放大到两伏但ADC上限还是1伏、超出部分无法记录、等效只接收到36000电子信号、放大倍数越高满阱越小、ISO100接收范围70微伏至1伏、ISO200变成140微伏至1伏、上限不变下限提高整体动态范围被压缩。"
},
"camera-iso-explained": {
  "practice": [
    ["说量子效率", "Only about half of the incoming photons ever become electrons."],
    ["说转换增益", "Base ISO is simply how many microvolts each electron produces."],
    ["说PGA放大", "Higher ISO means the PGA amplifies the voltage signal harder."],
    ["说原生与扩展", "Native ISO ends where the analog gain ends; beyond that is digital."],
    ["说ISO本质", "Modern ISO is really just gain along the readout chain."]
  ],
  "pitfalls": [
    ["Call ISO the camera's sensitivity to light.", "QE is the real light sensitivity, and it never changes with ISO.", "量子效率才是感光能力且固定。"],
    ["Assume every ISO number is native.", "Only the base-ISO-times-analog-gain range counts as native.", "只有模拟增益区间算原生ISO。"],
    ["Think extended ISO beats boosting in post.", "It is digital gain anyway—the same as brightening the file later.", "扩展ISO本质上就是后期提亮。"],
    ["Forget the floating-diffusion capacitor.", "That capacitor sets conversion gain, the anchor of base ISO.", "浮动扩散电容决定基准ISO。"],
    ["Expect PGA gain to go forever.", "Analog gain caps out, often around 32x on many bodies.", "模拟放大有上限。"],
    ["Mix up native and base ISO.", "Base ISO is the floor; native ISO includes all analog-boosted steps.", "基准是最小值，原生包含所有模拟档。"]
  ],
  "shifts": [
    ["说ISO只说感光度", "用 quantum efficiency（量子效率）、conversion gain（转换增益）、PGA（可编程增益放大器）"],
    ["说原生ISO只说原生", "用 base ISO（基准ISO）、native ISO（原生ISO）、extended ISO（扩展ISO）"],
    ["说放大只说放大", "用 analog gain（模拟增益）、digital gain（数字增益）、brightening（提亮）"]
  ],
  "footer": "转录基于图文实录完整口播。已校正：100个光子进入像素约50-60个转成电子、光电转换率叫量子效率QE、量子效率每台相机固定不随ISO改变、所以数码相机ISO指的不是量子效率、电路层面ISO首先体现在电荷到电压的转换、浮动扩散节点电容决定一个电子转成多大电压通常是微伏每电子、电荷电压对应关系叫转换增益conversion gain、也就是基准ISO Base ISO、调整ISO就是改变电压信号强度、通过PGA模拟放大实现、基准ISO100时一个电子转10微伏、ISO200即两倍放大变20微伏、ISO400四倍放大变40微伏、PGA放大倍率有限、以32倍为例即ISO3200、ISO100到3200区间都可叫原生ISO、A7M4原生从ISO100到51200、有人认为只有基准ISO100才是原生有争议、原生ISO定义指不经数字放大用基准ISO乘以PGA模拟放大得到的数值、超出模拟区间都是扩展ISO、是ADC量化后机内数字放大、跟后期提亮画面没差别、数码时代把ISO理解为传感器敏感度不贴切、ISO主要是电荷电压转换和PGA模拟放大、可看作这段电路共同协作的电信号读出、另一个名字叫增益。"
},
"camera-iso-genius": {
  "practice": [
    ["说传感器信号链", "Lens, filter, photodiode, well, and readout—the CMOS chain in one sentence."],
    ["说满阱容量", "A single well can pool tens of thousands of electrons before it's full."],
    ["说ISO与放大", "Dialing in an ISO is just picking the analog gain number."],
    ["说拜耳排列", "Color filters in a Bayer array let each pixel see one color."],
    ["说去马赛克", "Demosaicing borrows the neighbors to rebuild every pixel's true color."]
  ],
  "pitfalls": [
    ["Think the sensor records color directly.", "Sensors only see brightness; filters fake the color.", "传感器只记录亮度。"],
    ["Expect a raw file to look finished.", "A gray-looking frame is just the sensor data before demosaicing.", "RAW灰蒙蒙是正常的。"],
    ["Blame the microlens for focus.", "It gathers light, not focus—focus is the lens's job.", "微透镜只管收光。"],
    ["Skip the ADC in your mental model.", "The whole analog path funnels into the ADC's voltage cap.", "ADC是电压上限的关键。"],
    ["Assume the well is bottomless.", "Hit the full-well capacity and extra light is just clipped.", "满阱后多出的光子被丢弃。"]
  ],
  "shifts": [
    ["说成像只说拍照", "用 photodiode（光电二极管）、full-well capacity（满阱容量）、floating diffusion（浮动扩散）"],
    ["说颜色只说颜色", "用 color filter（滤色片）、Bayer array（拜耳排列）、demosaicing（去马赛克）"],
    ["说ISO只说ISO", "用 PGA gain（PGA增益）、ADC（模数转换器）、signal chain（信号链）"]
  ],
  "footer": "转录基于图文实录完整口播。已校正：主流的背照式CMOS由几部分构成、光线到达传感器先经微透镜汇集到下层的滤色片、滤色片筛选出波长匹配的光进入光电二极管PD、光子被转成电子在特定区域累积叫势阱、一个势阱可容纳几万个电子、最大值为满阱容量FWC、随后电子被浮动扩散节点FD转移捕捉到电容里、电容里的电荷转换成电压信号、源极跟随器缓冲稳定信号后被可编程增益放大器PGA模拟放大、改变ISO数值就是改变模拟放大倍数、最后进入模数转换器ADC把电压转成数字信号、打开文件看到灰蒙蒙画面、因为每个像素只能记录亮度无法直接记录颜色、所以每个像素上放彩色滤色片、常见RGB拜耳排列、每个像素能记录对应颜色的亮度信息、之后图像信号处理器ISP提取每个像素周围的颜色信息补全当前像素、混合出原本颜色的RGB信息、通过每个像素计算还原看到正常照片、这个处理过程叫去马赛克。"
},
"film-how-records": {
  "practice": [
    ["说卤化银", "A silver halide grain is the tiny particle that turns light into an image."],
    ["说潜影", "Light splits the halide into invisible silver specks—the latent image."],
    ["说显影定影", "Developer builds the visible silver; fixer dissolves what never saw light."],
    ["说负片原理", "More light means more dark silver, so the negative comes out inverted."],
    ["说印相还原", "Printing the negative onto paper flips the tones twice back to normal."]
  ],
  "pitfalls": [
    ["Think film records color straight away.", "It only records light; color comes from dyes layered in the emulsion.", "胶片本身只记亮度，颜色靠染料层。"],
    ["Skip the stop bath step.", "Without acid to stop development, the image keeps darkening.", "没有停显液会过显。"],
    ["Assume bright areas are bright on the negative.", "Heavy exposure turns film darkest—that's the negative.", "曝光强的地方反而最黑。"],
    ["Think fixer makes the image appear.", "The developer does that; the fixer just makes it permanent.", "显影让影像出现，定影只是固定。"],
    ["Forget the enlarger in the workflow.", "You need it (and photo paper) to turn a negative back into a photo.", "印相需要放大机和相纸。"]
  ],
  "shifts": [
    ["说胶片只说胶片", "用 silver halide（卤化银）、emulsion（乳剂）、grain（颗粒）"],
    ["说冲洗只说冲洗", "用 latent image（潜影）、developer（显影剂）、stop bath（停显液）、fixer（定影液）"],
    ["说负片只说负片", "用 negative（负片）、enlarger（放大机）、two negatives make a positive（负负得正）"]
  ],
  "footer": "转录基于图文实录完整口播。已校正：把一张胶片放大上千倍能看到很多颗粒状物质、这是感光材料卤化银、卤素与银形成的化合物、是胶片能感光成像的关键物质、胶片通常由很多层构成、最主要的是混合明胶与卤化银的感光乳剂层和承载它们的片基层、光线照射胶片、感光层中卤化银颗粒发生光解反应、感光点位析出微小银原子团簇叫潜影核、此时影像已被记录但光解银量极少无法被肉眼观测处于潜影状态、进入冲洗流程首先用显影剂、受光卤化银进一步反应、具有潜影核的卤化银被还原成金属银颗粒、大量金属银颗粒聚集构成可见影像、接下来停显液弱酸性中和显影液使卤化银停止反应、之后含硫代硫酸铵的定影液把未感光的卤化银溶解使胶片不能再感光、最后清洗残留成分、胶片上的画面黑白颠倒、曝光强的部分反而变黑、因为卤化银感光显影后形成的金属银颗粒本身呈黑色、曝光越多金属银越多画面越黑、曝光少金属银少看上去更亮、黑白颠倒的底片叫负片、用胶片放大机和含感光材料涂层的相纸把负相印到相纸、相纸接受到与实景相反的曝光、再经过一遍冲洗流程、负负得正还原出正常照片。"
},
"film-iso-history": {
  "practice": [
    ["说卤化银种类", "Chloride, bromide and iodide—three halides with rising sensitivity."],
    ["说标准混乱", "Every maker pushed its own scale until one body unified them."],
    ["说ISO组织的来历", "ISO stands for the International Organization for Standardization."],
    ["说ASA与DIN", "The unified standard prints the arithmetic ASA and logarithmic DIN together."],
    ["说数码延续", "Digital kept the ISO label even after the physics changed."]
  ],
  "pitfalls": [
    ["Translate ISO as if it were a word.", "It's an organization's acronym that became a byword.", "ISO是组织缩写。"],
    ["Think one halide fits all.", "Bromide dominates film, but chloride and iodide have roles too.", "溴化银最常用但不是唯一。"],
    ["Assume speed ratings predate 1987.", "Standards existed—many of them—before ISO unified things.", "1987年前已有多套标准。"],
    ["Forget DIN used logarithms.", "DIN numbers are logarithmic, so the marks look very different.", "DIN是对数制。"],
    ["Expect digital ISO to mean film speed.", "The label survived, but the mechanism is readout gain now.", "数码ISO的含义已改变。"]
  ],
  "shifts": [
    ["说感光度只说感光度", "用 ASA（美标算术值）、DIN（德标对数值）、GOST（苏联标准）"],
    ["说标准只说标准", "用 International Organization for Standardization（国际标准化组织）、unify（统一）"],
    ["说历史只说历史", "用 byword（代名词）、inherited label（沿用的标注）"]
  ],
  "footer": "转录基于图文实录完整口播。已校正：制作感光材料的卤化银有氯化银、溴化银和碘化银、感光效率由低到高、其中溴化银在胶片上应用最广泛、用不同卤化银和辅助材料混合能制作感光度高低不同的胶片、如何区分和标注成为问题、许多厂商组织先后制定标准、主流有德标DIN制、以柯达为首的美标ASA制、苏联的OCT等、标准太多反而困扰用户不利于传播普及、国际标准化组织International Organization for Standardization简称ISO、这个组织在1987年制定胶片通用感光度标准、规定在胶片上标出感光度的算数值ASA和对数值DIN、实际上就是把美标和德标相结合、随时间推移标注逐渐简化变成我们所熟知的样式、ISO并不是感光度的文本翻译而是一个组织简称、这个组织规范了胶片感光度的测定原理方法标准以及标注形式、ISO顺其自然成为感光度的代名词、时至今日胶片退出主流数码崛起、ISO的标注依然沿用、但数码和胶片无论感光材料还是成像原理都发生很大变化、数码时代的ISO含义已不同。"
},
"photo-why-blur": {
  "practice": [
    ["说清晰成像", "When nothing moves, light lands on the same spots and the photo is sharp."],
    ["说动态模糊两大因素", "Blur is exposure time times the relative motion in the frame."],
    ["说用快门控制", "Shorter exposure shrinks the distance a subject moves on the sensor."],
    ["说光绘创作", "Long exposures let you paint with light as your brush."]
  ],
  "pitfalls": [
    ["Think blur is always a mistake.", "Motion blur is a tool—light painters lean on it.", "动态模糊也可以是创作手段。"],
    ["Blame a soft lens for motion blur.", "Subject movement and slow shutter are the real causes.", "糊更常来自运动和慢快门。"],
    ["Crank ISO instead of shortening the shutter.", "A faster shutter freezes the motion; ISO only adds noise.", "加快快门才能真正防糊。"],
    ["Expect stillness to save you.", "Even a still subject blurs if the camera itself moves.", "相机自身晃动一样会糊。"]
  ],
  "shifts": [
    ["说糊只说糊", "用 motion blur（动态模糊）、exposure time（曝光时长）、relative motion（相对运动）"],
    ["说快门只说快门", "用 freeze（凝固）、long exposure（长曝光）、shutter speed（快门速度）"],
    ["说创作只说创作", "用 light painting（光绘）、creative tool（创作手段）"]
  ],
  "footer": "转录基于图文实录完整口播。已校正：相对完全静止的拍摄中按下快门、场景中所有物体反射的光线由镜头进入传感器在固定位置累积、得到清晰画面、一旦空间内有运动产生、运动物体反射的光会随之发生位移、得到带运动轨迹的模糊画面、这种由相对运动位移产生的模糊就是动态模糊、影响动态模糊最大的两个因素、一个是曝光时长一个是相对运动、大部分拍摄很难改变被摄物体的运动、只能通过改变快门控制模糊、运动恒定时曝光时间越短运动物体空间位移越小画面越清晰、反之曝光时间越长位移越大图像更模糊、动态模糊并不是成像缺陷、很多人利用这个特性创作、比如光绘、平面摄影中多数情况还是会规避这种模糊获得清晰图像。"
},
"leaf-shutter": {
  "practice": [
    ["说镜间快门结构", "The leaf shutter lives inside the lens, right next to the aperture blades."],
    ["说没有果冻效应", "The whole sensor exposes at once, so there's no rolling shutter."],
    ["说快门本质", "Every shutter is just a switch that controls how long light gets in."]
  ],
  "pitfalls": [
    ["Confuse the leaf shutter with the focal plane.", "A leaf shutter is in the lens; the focal plane one sits at the sensor.", "镜间快门在镜头里，焦平面快门在机身。"],
    ["Expect it in every camera.", "Its cost and light trade-offs keep it rare on modern bodies.", "成本高影响进光，应用不常见。"],
    ["Think it avoids all blur.", "It avoids rolling distortion, but motion blur still depends on time.", "免的是果冻效应，不是运动模糊。"],
    ["Forget its aperture side effects.", "It steals a bit of depth-of-field control and max light.", "它会影响进光量和景深。"]
  ],
  "shifts": [
    ["说快门只说快门", "用 leaf shutter（镜间快门）、focal plane shutter（焦平面快门）、rolling shutter（果冻效应）"],
    ["说结构只说结构", "用 aperture blades（光圈叶片）、open fully（整体开启）、no time gap（无时间差）"]
  ],
  "footer": "转录基于图文实录完整口播。已校正：镜间快门在镜头中间光圈旁、结构和光圈有些相似、由于在镜头内部开合过程中CMOS可以整体感光不存在时间差、因此不会产生果冻效应、开合速度通常也更快、缺点是对进光量和景深有影响、对硬件要求很高、结构复杂、应用并不常见、所有类型的快门本质上都是一个开关、一个控制时间的开关、目的是让相机更精确地还原我们按下快门那一刻、这个世界最真实的模样。"
},
"animation-science-howto": {
  "practice": [
    ["说MG动画本质", "Motion graphics just make shapes move, frame after frame."],
    ["说关键帧", "A keyframe stores a state, and the app tweens between them."],
    ["说速度曲线", "F9 eases the frames, turning a flat line into a smooth curve."],
    ["说核心动机", "Start from one core idea and sketch it with the simplest shapes."],
    ["说脚本与插件", "Scripts automate AE; plugins stretch what AE can do."]
  ],
  "pitfalls": [
    ["Jump straight into effects.", "Anchor the idea in shapes and keyframes before decorating.", "先搭结构和运动，再上效果。"],
    ["Leave every motion linear.", "Linear keyframes look robotic—ease them to feel alive.", "线性运动很生硬。"],
    ["Click the 3D switch and expect CGI.", "AE is a 2D app; convincing 3D needs tricks and plugins.", "AE本质是2D软件。"],
    ["Confuse scripts with plugins.", "Scripts drive existing features; plugins add new ones.", "脚本控制现有功能，插件扩展边界。"],
    ["Let one comp swallow everything.", "Split work across compositions to stay organized.", "分开制作便于管理。"],
    ["Polish before the idea is clear.", "Without a core motivation, more effects just add noise.", "没有核心动机就无从下手。"]
  ],
  "shifts": [
    ["说动画只说动画", "用 keyframe（关键帧）、tween（补间）、linear motion（线性运动）、speed curve（速度曲线）"],
    ["说操作只说操作", "用 stopwatch（码表）、trim paths（修剪路径）、pen tool（钢笔工具）、graph editor（图表编辑器）"],
    ["说流程只说流程", "用 core idea（核心动机）、comp（合成）、script vs plugin（脚本vs插件）"]
  ],
  "footer": "转录基于图文实录完整口播。已校正：动画类型属于MG动画、可简单理解为让图形动起来、无论什么形状单一元素还是复合形态都可看作图形、图形能动起来靠关键帧、关键帧是动画最基础运行逻辑也是最容易劝退的部分、AE界面左侧项目面板管理所有文件也能导入素材、右侧实时监看面板叫合成窗口、上面是工具栏、最下面合成的时间线窗口是主要操作区域、点击右键可新建文字形状图层、新建形状展开变换参数有五个选项、其中位置缩放旋转是影响运动的三个关键参数、做位移动画把图形放左侧、时间线拖到起始处点位置属性前码表图标记录关键帧、拖到两秒处改变位置自动生成第二个关键帧、预览就是一个简单位移动画、关键帧记录画面元素在不同时间下的不同状态、一个合成几十个图层几百上千关键帧、一个工程少则几个多则几十个合成、为不让工程混乱会分开制作、动画不流畅是因为还是线性运动、选出两个关键帧打开图表编辑器选择编辑速度图表、横向时间纵向速率、是直线说明速度一致、按F9键菱形关键帧变沙漏形状、直线变曲线、高的部分运动更快低的部分更慢、由快到慢左高右低、由慢变快左低右高、调整速度曲线实现想要的运动效果、关键帧只是让画面动起来、调整好运动曲线让画面丝滑流畅、会操作不会创作是因为没找到核心动机、以快门这期为例核心动机就是快门形态、先想象快门组成部分用基础形状描绘、长方形CMOS圆形卡口四个长方形拼出快门叶片、关键帧记录每个叶片起始和结束位置、预合成复制一份再翻转就有快门开合效果、粗糙画面还要说到AE最重要部分效果、给CMOS形状加四色渐变效果调整颜色分布、再添加网格效果调整参数得到更符合直觉的CMOS画面、通过一个或多个效果叠加实现更丰富视觉表现、还能添加更多细节、完成核心画面确立视频基调、相机生长动画先找图片参考用钢笔工具绘制、再添加修剪路径效果打上关键帧、让图形线条路径从0%到最后100%依次展现、就是路径生长动画、打开3D开关旋转一下、AE本质还是2D软件、想在二维实现3D效果可以耍点小心机、相机旋转到不同形态时做出对应轮廓线条、在轮廓变化起始中间和结束状态分别打上关键帧、适当调整一个障眼法的3D效果就出来了、实现一个动画效果可以有很多种途径方法、学会举一反三永远保持寻找更好方法的思维模式、AE拓展工具就是常听到的插件脚本、脚本通常体积小巧通过代码控制AE现有功能让操作更便捷、比如脚本点击图标自动生成动画、把常用效果以图标形式摆放、点击图标就OK省去反复查找时间、插件更复杂是为了拓展AE的边界、让原本实现不了或很难实现的效果更容易制作、比如粒子插件和3D插件、用动画做科普的目的就是让晦涩难懂的文字表述以可视化形态展现、优势直观明了、归根结底只是一种表现形式、科普内容本身才是核心、要做锦上添花而非纸上添花。"
},
"electronic-front-curtain": {
  "practice": [
    ["说电子前帘组合", "EFCS opens electronically and closes with a mechanical curtain."],
    ["说它的优点", "It dodges readout limits and avoids the shake of a front curtain."],
    ["说光斑裁切", "At high speeds the two shutters clip bokeh circles off-center."]
  ],
  "pitfalls": [
    ["Think EFCS is fully electronic.", "It's a hybrid—electronic to open, mechanical to close.", "电子前帘是电子加机械的组合。"],
    ["Use it at high speeds and blame the lens.", "Fast speeds make the out-of-focus bokeh get sliced.", "高速下焦外光斑会被裁切。"],
    ["Expect it to cure all shake.", "It removes front-curtain shake, not camera movement.", "它只消除前帘震动。"],
    ["Assume front and back curtains share a plane.", "They sit apart, which is exactly what causes the clipping.", "机械后帘与CMOS不在同一平面。"]
  ],
  "shifts": [
    ["说快门只说快门", "用 EFCS（电子前帘快门）、mechanical rear curtain（机械后帘）、hybrid（混合式）"],
    ["说问题只说问题", "用 bokeh clipping（光斑裁切）、uneven exposure（曝光不均）、curtain shake（快门震动）"]
  ],
  "footer": "转录基于图文实录完整口播。已校正：电子前帘快门是电子加机械的组合、开启时用电子快门、关闭时使用机械后帘快门、由于机械后帘的介入这种曝光方式不受读出速度影响、同时还能避免前帘开合产生的震动、缺点是由于机械后帘与控制电子快门的CMOS不在一个平面上、快门速度过高时会出现曝光不均匀现象、最常见的就是焦外的光斑被裁切、原理是高速快门使曝光间隔变小、两种快门又不在一个平面上、焦外的弥散圆被机械快门遮挡后、导致后面CMOS无法均匀曝光、因此出现前景的光斑上半部分被裁切、而后景的光斑下半部分被裁切的现象。"
},
"electronic-shutter-framerate": {
  "practice": [
    ["说帧率与卡顿", "Low frame rates spread motion wide, so the image stutters."],
    ["说动态模糊的作用", "Motion blur records the trajectory, making motion look continuous."],
    ["说快门速度上限", "Shutter speed can never beat the reciprocal of the frame rate."],
    ["说180度规则", "At 180 degrees each frame gets half the time of one frame."],
    ["说快门角度换算", "172.8 degrees at 24fps is exactly a 1/50s exposure."],
    ["说频闪原因", "Shutter speeds mismatched with AC power cause flicker."]
  ],
  "pitfalls": [
    ["Set shutter speed faster than the frame allows.", "At 25fps you can't beat 1/25s per frame—it's the ceiling.", "帧率决定快门速度上限。"],
    ["Shoot 24fps at 180° under 50Hz lights.", "That's 1/48s and it flickers—use 1/50s instead.", "24帧180度在50Hz下会频闪。"],
    ["Treat odd angles like typos.", "172.8° and 144° are the cinema standard at 24fps.", "奇怪角度来自电影24帧。"],
    ["Skip motion blur in low frame rates.", "Sharp frames at low fps feel stuttery without it.", "低帧率需要动态模糊。"],
    ["Think the angle disc is still in cameras.", "It's legacy from film cameras; modern bodies borrow the label.", "快门角度是胶片时代的标注。"],
    ["Blame the camera for flicker.", "Mismatched AC frequency and shutter speed cause it.", "频闪源于快门与交流电频率不匹配。"]
  ],
  "shifts": [
    ["说帧率只说帧率", "用 frame rate（帧率）、stutter（卡顿）、per-frame motion（每帧运动）"],
    ["说快门只说快门", "用 180° rule（180度规则）、shutter angle（快门角度）、reciprocal（倒数）"],
    ["说频闪只说频闪", "用 flicker（频闪）、AC frequency（交流电频率）、1/50s vs 1/60s（两种市电快门）"]
  ],
  "footer": "转录基于图文实录完整口播。已校正：视频实际上是连续播放的静止帧、一帧就是一张图片、不同帧率决定一秒钟内小球运动路径上有多少个画面、连续播放变成视频、帧率较低时物体每帧之间运动跨度很大、过于清晰的画面使人一眼产生明显卡顿、加入适当动态模糊实际上就是增加运动轨迹的记录、画面更连贯流畅、模糊太大会影响观看体验、帧率决定快门速度上限、视频拍摄中快门速度最大只能是帧率的倒数、每秒25帧时每帧最长25分之一秒、用圆形分布对应打开360度就是100%曝光为单帧曝光上限、时间减半变50%曝光量即50分之一秒角度180度、每帧曝光一半时长产生的动态模糊比较符合人眼视觉感知、以角度控制曝光的快门早期用在胶片摄影机、金属圆盘转速匹配帧率、通过控制打开角度让光线穿过改变每帧胶片曝光时长、快门角度大小决定每帧画面曝光多少、通常说的180度对应单帧一半曝光时长即帧率倒数的一半、如今一些电影机还沿用快门角度标注、172.8度和144度来自电影24帧拍摄帧率、172.8度开角对应24分之一秒的48%即50分之一秒快门速度、144度对应24分之一秒的40%即60分之一秒、用50分之一秒和60分之一秒是为了匹配不同国家和地区的交流电频率避免频闪、频闪通常是快门速度设定与人造光源交流电频率不匹配导致、我国交流电频率50Hz、拍摄24帧按180度曝光快门48分之一秒、每帧记录的电压周期不一致画面亮度不同、连续播放可能出现闪烁、用50分之一秒快门正好与周期匹配亮度一致避免频闪。"
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
