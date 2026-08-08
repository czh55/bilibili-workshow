#!/usr/bin/env python3
"""批32：为10篇光圈/快门/构图/收音JSON补全 practice/pitfalls/shifts/footer_notes。"""
import json
from pathlib import Path

DATA = Path("/Users/chenzhiheng/Projects/bilibili-workshop/scripts/scene-data")

ENRICH = {
"electronic-shutter": {
  "practice": [
    ["说电子快门读出", "The sensor reads rows one at a time, not all at once."],
    ["说果冻效应", "Staggered row timing bends fast-moving subjects."],
    ["说机械快门的优势", "A rear curtain blocks light while rows read out."],
    ["说全域快门", "Electrons park in storage cells before readout."]
  ],
  "pitfalls": [
    ["Think all sensors read at once.", "Readout is row by row—that's the root of rolling shutter.", "读出只能逐行进行。"],
    ["Blame every distortion on the lens.", "At 20ms readout, a 33MP frame lags 4.3µs per row.", "果冻效应来自逐行读出时差。"],
    ["Assume mechanical shutters never distort.", "They do roll, just far less than electronic ones.", "机械快门也有果冻效应，只是更轻。"],
    ["Buy a global shutter and expect no trade-off.", "Extra storage cells cut light capture and raise the price.", "全域快门牺牲进光和画质，还贵。"]
  ],
  "shifts": [
    ["说电子快门只说电子快门", "用 row-by-row readout（逐行读出）、readout speed（读出速度）、time gap（时间差）"],
    ["说果冻只说果冻", "用 rolling shutter（果冻效应）、distortion（变形）、skew（倾斜扭曲）"],
    ["说快门只说快门", "用 mechanical curtain（机械帘幕）、global shutter（全域快门）、storage cell（存储单元）"]
  ],
  "footer": "转录基于图文实录完整口播。已校正：CMOS每个像素都有开关、打开接收光线关闭则重置、按下快门后CMOS清空电荷信息开始接收光线、光子进入传感器被光电二极管转化成电子、再由电容转化成电压、之后通过PGA放大电路放大、再经由模数转换器ADC转化成数字信号、从电压到数字信号的整个读出过程只能依次逐行进行、绝大多数CMOS由于性能制约读出速度受限动辄2、3、10毫秒、以20毫秒读出速度为例对应到每行像素在图表上是一条斜线、想做到每行像素曝光结束时同步读出、电子快门只能严格按照这条斜线即读出速度来控制每行像素的开启、无论快门如何调整时间差都是20毫秒远大于机械快门的4毫秒、较高时间差会出现严重问题果冻效应、由于每行像素记录时间不同存在时差、导致运动物体在空间位移中发生形变、直线变斜的旋转的变扭曲、3300万像素CMOS拍摄一张照片需要读出4672行、按20毫秒读出速度每行像素时间差约等于4.3微秒、听上去几乎不可感知但对高速运动物体足以产生明显变形、机械快门同样会出现果冻效应只是比电子快门好很多、控制果冻效应只有两种方法、减少相对运动或提高读出速度、机械前帘物理结构决定CMOS可以先曝光后逐行读出、中间读出期间后帘遮盖没有光线进入因此不受影响、电子快门可以同时开启感光但会导致后读出像素感光时间更长曝光不均匀、同时曝光后同时关闭也不行关闭后没被读出的信息都会重置、全域快门可以同时控制电路开启、曝光后把电子先转移到存储单元再读出数据、不存在曝光时间差完全避免果冻效应、代价是给每个像素增加额外存储单元降低接收光线能力、对信噪比和画质产生影响、当然最大的影响还是贵。"
},
"aperture-definition-part1": {
  "practice": [
    ["说相对光圈值", "F1.4 and F2.8 are relative apertures, not sizes."],
    ["说F值公式", "The F-number is focal length divided by the entrance pupil."],
    ["说入瞳径", "It's the opening you see from the front of the lens."]
  ],
  "pitfalls": [
    ["Think F16 is a bigger hole.", "A larger f-number means a smaller physical opening.", "数值越大物理光圈越小。"],
    ["Mistake the blades for the pupil.", "The pupil is the apparent opening, shaped by front glass too.", "入瞳径是视觉开孔直径。"],
    ["Expect small f-numbers to always mean huge pupils.", "The pupil also depends on focal length and front optics.", "入瞳径还受焦距和前组镜片影响。"]
  ],
  "shifts": [
    ["说F值只说数字", "用 relative aperture（相对光圈）、focal length（焦距）、ratio（比值）"],
    ["说光圈只说光圈", "用 entrance pupil（入瞳）、physical aperture（物理光圈）、apparent opening（视觉开孔）"]
  ],
  "footer": "转录基于图文实录完整口播。已校正：常听到的光圈F1.4、F2.8、F4、F8、F16是镜头的相对光圈值、数值越小实际物理光圈越大、数值越大实际物理光圈越小、很多人被这个相反概念搞混、光圈F值等于焦距除以入瞳径即焦距与入瞳径的比值、入瞳径很大程度上由物理光圈控制、入瞳径可以理解为从镜头前看向其内部的视觉开孔直径、不是真实的光圈叶片所控制的物理孔径、很多大光圈镜头前镜组采用高曲率或高折射率的镜片、其作用就是把入瞳径放大。"
},
"mechanical-shutter": {
  "practice": [
    ["说双帘结构", "Front and rear curtains open and close to control the light."],
    ["说快门速度真相", "Shutter speed is exposure time, not curtain speed."],
    ["说帘幕间隔", "A wider curtain gap means more light reaches the sensor."],
    ["说闪光同步", "Below 4ms the sensor can't fully open, capping sync at 1/250s."]
  ],
  "pitfalls": [
    ["Assume shutter speed is curtain speed.", "Curtains stay constant; the speed number is exposure time.", "快门速度是曝光时长。"],
    ["Think all curtains run horizontally.", "Most modern cameras use vertical-traveling curtains.", "主流是纵走前后双帘。"],
    ["Use flash past 1/250s and blame the flash.", "The slit-shaped curtains can't expose the whole sensor in time.", "超过同步速度会拍到黑边。"],
    ["Expect the front and rear to move in sync.", "They move sequentially, defining exposure via their gap.", "前后帘按顺序运动。"]
  ],
  "shifts": [
    ["说快门只说快门", "用 front/rear curtain（前帘/后帘）、curtain gap（帘幕间隔）、slit（夹缝）"],
    ["说速度只说速度", "用 exposure time（曝光时长）、flash sync（闪光同步）、1/250s（同步上限）"]
  ],
  "footer": "转录基于图文实录完整口播。已校正：大多数机械快门采用纵走前后双帘结构、不同相机帘幕运动次序有差别、先打开让传感器感光的叫前帘、之后关闭结束感光的叫后帘、按下快门后前帘落下相机清空CMOS中的电荷并开始感光、之后前帘抬起传感器从下至上依次接触光线、到达设定时间后后帘抬起此时CMOS仍处感光状态、等所有信号逐行读出完毕后帘复位一次拍摄完成、常说的100分之1秒1000分之1秒快门速度、惯性思维会让人误以为指机械帘幕的运动速度、实则不然、通常为了方便控制曝光时长机械帘幕运动速度大多是恒定的一般为250分之1秒即4毫秒、所以准确来说快门速度通常指曝光时长而非机械快门运动速度、帘幕运动速度恒定如何精确控制曝光、很简单间隔、前后帘开合间隔越大CMOS接受光线时间越长、其他参数不变整体进光量越多画面更亮、反之间隔越小进光量更少画面更暗、机械快门依靠帘幕开合遮挡控制曝光、帘幕运动速度恒定为4毫秒、当曝光时间小于这个值帘幕以夹缝形态滚动、CMOS没有机会同时露出、当曝光时间大于或等于4毫秒CMOS会有一定时间同时露出、这个时间内外界施加的光能被整个CMOS均匀捕获、这也是多数闪光灯同步速度上限为250分之1秒的原因、无论快门如何调整CMOS上下行两端都会有4毫秒时间差、这个时间差在电子快门中尤为明显。"
},
"aperture-dof-formula": {
  "practice": [
    ["说容许弥散圆", "A blur circle small enough to look sharp is the circle of confusion."],
    ["说0.029毫米", "On full frame the accepted blur is just 0.029mm across."],
    ["说景深公式", "Plug in CoC, aperture, focal length, and focus distance."]
  ],
  "pitfalls": [
    ["Treat sharpness as absolute.", "It's defined by how small the blur looks to the eye.", "清晰是相对人眼的感知。"],
    ["Assume CoC is the same for every sensor.", "Full frame uses ~0.029mm, but smaller sensors differ.", "不同画幅的容许弥散圆不同。"],
    ["Skip the formula and guess.", "The numbers—5.034m total—come straight from the math.", "用公式才能算准景深。"],
    ["Confuse depth of focus with depth of field.", "One lives at the sensor, the other in the scene.", "焦深在传感器侧，景深在场景侧。"]
  ],
  "shifts": [
    ["说模糊只说模糊", "用 circle of confusion（弥散圆）、acceptable blur（可接受的模糊）、CoC（容许弥散圆）"],
    ["说景深只说景深", "用 depth of field（景深）、front/back depth（前/后景深）、total（总景深）"]
  ],
  "footer": "转录基于图文实录完整口播。已校正：前后移动焦点成像焦点脱离传感器、传感器上接收到的便是焦点之外逐渐扩大的弥散圆、物体点的成像慢慢变模糊、只要弥散圆足够小人眼无法辨别模糊自然认为清晰、这个足够小的弥散圆叫容许弥散圆、以36毫米×24毫米全画幅相机来说通常定义的容许弥散圆大小、直径约为0.029毫米只比发丝直径稍微大一点、为方便演示把容许弥散圆放大一些、放到焦点两侧与光线夹角大小吻合的位置、这个区间就是无法辨认出模糊的范围称之为焦深、前后移动被摄主体只要移动范围不超过容许弥散圆区间就认为是清晰的、与焦深对应镜头之外物体前后相对清晰的范围就是景深、准确计算景深范围需要引入公式、delta是容许弥散圆直径0.029毫米、光圈设定F8焦距35毫米对焦距离3米即3000毫米、带入这些设定参数用景深公式计算得出整个景深范围5.034米即5034毫米、前景深约1.087米后景深3.947米。"
},
"aperture-affect-dof-6": {
  "practice": [
    ["说入瞳径影响景深", "The entrance pupil's size sets the light cone, which sets depth."],
    ["说光圈与景深的关系", "Stop down for deeper focus; open up for creamy shallow depth."],
    ["说拍摄距离", "Closer subjects get shallower depth of field."],
    ["说光圈的另类影响", "Blade shape rounds bokeh; tiny apertures diffract and star."]
  ],
  "pitfalls": [
    ["Blame the blades for depth of field.", "It's the entrance pupil and light cone that really rule.", "本质是入瞳径决定景深。"],
    ["Forget subject distance.", "Distance shifts the light cone, so depth changes too.", "距离也会改变景深。"],
    ["Expect a perfectly round bokeh from every lens.", "Blade count and shape decide whether circles stay round.", "叶片数量形状决定光斑圆润度。"],
    ["Assume smaller is always sharper.", "Diffraction softens the image past a certain point.", "过小光圈会因衍射变软。"]
  ],
  "shifts": [
    ["说景深只说景深", "用 entrance pupil（入瞳径）、light cone（光锥）、angle（夹角）"],
    ["说光圈效果只说光圈", "用 bokeh（焦外）、diffraction（衍射）、starburst（星芒）"]
  ],
  "footer": "转录基于图文实录完整口播。已校正：控制其他变量只缩小光圈、入瞳径随之变小、光线夹角也变小、原来的光束变窄、但容许弥散圆直径固定不变、想要对应在光束上就要把容许弥散圆向两侧延伸、焦深明显增大景深自然变大、本质上影响景深变化的是入瞳径而非物理光圈、但从另一面来说入瞳径很大程度上受物理光圈控制、所以大家通常也说光圈影响景深、调小光圈入瞳直径缩短光线夹角变小景深范围增大景深更深、光圈放大入瞳直径增长光线夹角变大景深范围减小景深更浅、另一个影响景深很重要的因素是被摄物体与相机距离、原因是距离改变影响入射光线夹角大小、自然也会改变容许弥散圆所定义的区间景深随之变化、光圈除了曝光和景深还有一些别的影响、光圈叶片数量和形状影响着焦外光斑是否圆润、光圈缩小到一定程度由于光路狭小造成的衍射对成像质量有所限制、也有人专门利用这些特性制作镜头拍摄例如星芒效果的风格化影像、整期视频围绕着一个元素原来讨论的、影像从来都没有标准答案、就如同算不尽的圆周率、了解这些知识未必会提高拍摄水平、但就像科学家对圆的执念一样、了解的更深一点才能走的更远一些。"
},
"aperture-coc-part4": {
  "practice": [
    ["说弥散圆的视觉极限", "A blur circle small enough to look sharp is the circle of confusion."],
    ["说镜头本质", "Complex lenses still boil down to a simple convex lens."],
    ["说焦点与像素", "Only the focal point is perfectly sharp; pixels are the floor."]
  ],
  "pitfalls": [
    ["Think blur is absolute.", "Sharpness is judged against viewing distance and size.", "清晰与否取决于观看尺寸和距离。"],
    ["Mistake the light cone for a real cone.", "It's an abstraction of how rays spread past focus.", "光束扩散是几何概念。"],
    ["Forget the pixel floor.", "Even a perfect point can't image finer than one pixel.", "成像最小单位是一个像素。"],
    ["Assume every lens element is a lens.", "Complex groups correct aberrations but use the same math.", "多组镜片是为修正像差。"]
  ],
  "shifts": [
    ["说模糊只说模糊", "用 circle of confusion（弥散圆）、blur circle（模糊圆）、focal point（焦点）"],
    ["说镜头只说镜头", "用 convex lens（凸透镜）、refract（折射）、converge（汇聚）"]
  ],
  "footer": "转录基于图文实录完整口播。已校正：这是一个圆形看上去有些模糊、暂且称它为弥散圆、如果观看设备是6英寸手机观看距离差不多30厘米、把这个弥散圆缩小再缩小到一定尺寸、很多人就察觉不到它的模糊、从视觉上便是可接受的清晰的圆、这个可接受的弥散圆称之为容许弥散圆、镜头通常由多组多枚镜片构成、目的是更好汇聚光线优化成像品质、但根本还是利用了凸透镜的成像原理、为方便演示简化一下、一个凸透镜用于成像一个光圈用于控制通光孔径、一个面可以由无数个点组成、取其中一个把焦点对在上面、理论上这个点可以无限小、由于传感器物理限制可以成像的最小单位是一个像素点、从这一点反射出的光会有一部分进入镜头、经凸透镜折射后再汇聚到成像光屏即相机传感器、理想状态经过凸透镜折射的光线会如同一束光束完美汇聚到一个交叉点之后再分散开来、这个交叉点称之为焦点、如果焦点和传感器重合物体面的那个点便能清晰呈现在画面上、物体平面上的多个点都会一一对应投射在传感器上、此时能看到一个清晰倒立的像、严格来说只有光线汇聚的交叉点即焦点上成像最清晰、在这个汇聚点之外的光束上可以想象成有无数个扩散且模糊的圆即弥散圆。"
},
"aperture-depth-of-field": {
  "practice": [
    ["说景深的直觉定义", "Depth of field is the sharp zone around your focus point."],
    ["说光圈与景深方向", "Wide open for shallow depth; stopped down for deep focus."],
    ["说引出弥散圆", "The real ruler is the entrance pupil and circle of confusion."]
  ],
  "pitfalls": [
    ["Think only the focus plane is sharp.", "There's a whole zone of acceptable sharpness.", "对焦点前后都有一段清晰区间。"],
    ["Assume the physical aperture rules.", "The entrance pupil is what actually changes depth.", "直接起作用的是入瞳径。"],
    ["Forget that blur is perceptual.", "Sharp means indistinguishable from sharp to the eye.", "清晰是人眼的判断。"],
    ["Crank aperture without a reason.", "Depth control is a creative choice, not an accident.", "景深是创作选择。"]
  ],
  "shifts": [
    ["说虚化只说虚化", "用 background blur（背景虚化）、bokeh（虚化效果）、sharp zone（清晰区间）"],
    ["说景深只说景深", "用 deep/shallow depth（深/浅景深）、focus point（对焦点）、entrance pupil（入瞳径）"]
  ],
  "footer": "转录基于图文实录完整口播。已校正：就算不了解景深的朋友也一定听过背景虚化、通常一个场景中人物主体清晰而背景虚化模糊、想象人物和相机之间有一条纵向轴线、把焦点设定在人物主体上、人物前后会有一段相对清晰的区间、把相对清晰的这一区间称作景深、增加一个视图就能分辨出人物主体前景以及背景、把焦点对着人物主体调大光圈、除了焦点前后一段范围相对清晰其他地方开始逐渐模糊、这一段相对清晰的范围就是常说的景深、光圈越小清晰范围越大一般称深景深或大景深、反之光圈越大清晰范围越小称之为浅景深、简单来说景深就是对焦点前后能被人眼识别为清晰的范围、实际上直接影响景深的是入瞳径而非物理光圈、那么为什么大家会说光圈影响景深、以及该如何定义这个景深的范围、这里就要涉及到另一个概念容许弥散圆。"
},
"aperture-calc-part2": {
  "practice": [
    ["说入瞳直径计算", "At f/1.2 the 50mm lens opens to a 42mm entrance pupil."],
    ["说光圈控光原理", "A wider pupil admits more light, brightening the image."],
    ["说平方反比规律", "Each 1.4x in f-number doubles or halves the light."]
  ],
  "pitfalls": [
    ["Think f-number equals aperture size.", "It's a ratio of focal length to entrance pupil.", "F值是焦距与入瞳径的比值。"],
    ["Forget the inverse-square law.", "Illuminance follows the square, not the number.", "照度是平方反比关系。"],
    ["Expect doubling the f-number to halve brightness.", "A 1.4x change in f-number is one stop.", "F值变1.4倍才是一档。"],
    ["Assume the pupil is the blade opening.", "Front optics can enlarge the apparent pupil.", "前组镜片能放大入瞳径。"]
  ],
  "shifts": [
    ["说光圈只说光圈", "用 entrance pupil（入瞳）、illuminance（照度）、light area（光通面积）"],
    ["说档位只说档位", "用 inverse square（平方反比）、1.4x（1.4倍）、one stop（一档）"]
  ],
  "footer": "转录基于图文实录完整口播。已校正：这是一颗50毫米定焦镜头、光圈值最大F1.2时根据公式算出此时的入瞳直径大约是42毫米、把光圈值调到F16此时的入瞳直径仅约为3毫米、明白了这些就不难理解光圈如何控制曝光、调大光圈入瞳径随之变大光通面积自然更大、相机传感器接收到的光线照度变强、呈现出来的画面看起来更亮、把光圈调小入瞳径变小光通面积更小、传感器接收到的光线照度变弱、画面就会更暗、实际上光圈F值与成像面照度近似平方反比关系、F值每改变1.4倍成像面照度便相应成两倍变化、成像面照度跟光通面积不能混为一谈、但在不同F值下得出的入瞳直径按算术看光通面积同样符合这个规律、光圈除了能控制曝光还会影响一个非常重要的成像特性景深。"
},
"photo-composition-aesthetics": {
  "practice": [
    ["说构图美学", "Composition is about aesthetics, not just rule-of-thirds."],
    ["说视线引导", "Leave space ahead of the subject to guide the eye."],
    ["说视觉平衡", "Counterweight elements on the other side to balance the frame."]
  ],
  "pitfalls": [
    ["Rely only on the rule of thirds.", "Real composition is built on aesthetics and psychology.", "构图不只是三分法。"],
    ["Place the subject facing the edge.", "Tight edges block the gaze; leave room in view direction.", "视线方向要留白。"],
    ["Forget the frame's weight.", "A lone subject on one side tips the whole image.", "元素偏移会失衡。"],
    ["Think balance means symmetry.", "Balance comes from counterweights, not mirrors.", "平衡靠配重不是对称。"]
  ],
  "shifts": [
    ["说构图只说三分法", "用 visual weight（视觉重量）、Gestalt（格式塔）、visual tension（视觉张力）"],
    ["说平衡只说平衡", "用 counterweight（配重）、seesaw（跷跷板）、lead the eye（引导视线）"]
  ],
  "footer": "转录基于图文实录完整口播。已校正：真正懂构图的人不仅停留在三分线黄金分割线这些基础公式上、而是懂得构图背后的审美法则、比如这个箭头箭头靠右就会觉得压抑箭头靠左就会舒服很多、所以在拍这个画面时不会把人放在右边导致视线轨迹受阻、而是放在左边为视线方向留白引导视觉空间、把这个箭头换成一个方块移到左边就会左重右轻造成构图失衡、想要恢复平衡就需要在右边增加一个元素、如同在跷跷板的另一端放上重物、这本书最厉害的地方就是它让你通过本质了解构图、它不是讲三分法九宫格这种基础构图、而是深入到美学数学和观众心理学、帮你构建牢固的审美体系、不管是审美的视觉重量还是抽象的格式塔理论、包括色彩对构图的影响等等都讲得特别透彻、每个术语都会配专业的摄影作品以及几个对比图片、让你知道什么画面是好的而且能说出好在哪里、哪怕是新手小白也能看懂、这本书除了教你构图的方法还能提升你的审美、增强你对场景布置光线色彩情绪的感知、帮你拍出更有美感更有故事的好作品。"
},
"audio-channel-select": {
  "practice": [
    ["说单声道", "Mono puts one mic into both left and right speakers."],
    ["说立体声陷阱", "Choosing stereo with one mic lands it in a single ear."],
    ["说软件修复", "Fill the empty channel from the live one in your editor."],
    ["说双人双声道", "Give each guest a channel so you can mix them separately."],
    ["说四轨多轨", "One-to-four rigs give four independent tracks to mix."],
    ["说内录双保险", "On-board recordings back up the camera audio."]
  ],
  "pitfalls": [
    ["Pick stereo with a single mic.", "One mic in stereo fills just one ear.", "单麦选立体声会只有一边有声。"],
    ["Mix two mics into mono and lose control.", "You can't fix levels after they're mixed together.", "混在一起后期无法单独调。"],
    ["Ignore channel settings until post.", "Check the recorder's channel mode before you hit record.", "录制前就该设好声道。"],
    ["Use four mics without a four-track camera.", "The camera must support four tracks to keep them separate.", "相机要支持四轨才行。"],
    ["Skip the safety recording.", "Transmitter internal audio is your backup if the camera fails.", "内录是双保险。"]
  ],
  "shifts": [
    ["说声道只说声道", "用 mono（单声道）、stereo（立体声）、channel（声道）"],
    ["说后期只说后期", "用 fill left to right（左填右）、route（路由）、multi-track（多轨）"],
    ["说收音只说收音", "用 transmitter（发射器）、on-board recording（内录）、safety net（双保险）"]
  ],
  "footer": "转录基于图文实录完整口播。已校正：音频时不同声道是什么意思怎么设置不翻车、一个视频弄懂单声道立体声双声道录音、最简单的录音一个人别一个发射器一个接收器、接收器里选择单声道相当于把一个麦克风的声音同时录进左右两声道、这是平时听到最多的声音、录音时声音只有左耳或只有右耳、耳机没坏多半是录音时选择了双声道有时候也叫立体声、选择双声道相当于一个麦克风的声音只录制在左右声道中的一个、不用急在软件里复制到另外一个声道就可以、素材只有左声道有声音右声道没有、剪映音频最后一项声道配置打开把左声道填充至右声道、两声道都有声音了、Premiere里选择素材右键片段属性里面有一个音频、把没有声音的选择有声音的这个声道点OK、单人录音没问题、双人录音俩嘉宾一人一个发射器一个接收器、选单声道俩嘉宾声音不分左右直接混到这个音频里、但俩嘉宾声音大小不一样或声线不一样后期想单独调、单声道模式下没法调它是混在一起的、这个时候建议选择双声道一个嘉宾一个声道、处理这种素材分两步、剪映专业版选中素材分离音频、把分离的音频再复制一份、选择其中一个音频在声道配置把左声道填充到右声道、另外一个音频把右声道复制到左声道、俩嘉宾声音就正常了可以单独控制、达芬奇操作差不多选中素材取消它们的关联、Alt再复制一段音频、选择其中一段的片段属性音频然后选择一样、另外一个也是片段属性、一拖四多轨需要特定麦克风和相机、大疆Mic三默认一拖二、再准备两个发射器长按链接按钮红蓝闪烁、接收器里设备配对选择TX、TX3配对TX4配对、配对完成后主界面看到四个麦克风图标、RX设置把声道选择四声道、索尼相机搭配大疆Mic三热靴转接、进菜单录制录音MI音频设置选择四轨、左上角已经是四个音轨了、拖到达芬奇里四条音轨每一条可以单独控制、剪映专业版拖进去只有一条音轨、选中素材分离音频把音频复制三份、第二段切换多音轨音轨二、第三段切音轨三、第四段切音轨四、每一段可以单独控制、一拖多声音很适合多个嘉宾或多个声源录制、四个轨道每个都能单独调后期自由度更大、录音过程建议结合发射器内录使用、文件类型可以选择原文件和处理文件、发射器能同步录一条原始音频和处理过的音频、即使相机录制出现问题发射器内录文件也给录制过程加了双保险。"
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
