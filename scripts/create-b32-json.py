#!/usr/bin/env python3
"""批32：为10篇相机光圈/快门/构图/收音视频生成完整场景英译JSON。"""
import json, re
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

ARTICLES = {}

ARTICLES["electronic-shutter"] = {
    "title_zh": "学摄影需要知道的——电子快门",
    "title_en": "The Electronic Shutter, Explained",
    "duration": "2分48秒",
    "topic": "摄影 · 相机知识",
    "scenes": [
        {"id": "s1", "scene_zh": "电子快门的基础", "scene_en": "Electronic Shutter Basics", "time": "00:00",
         "context": "可以想象CMOS的每个像素都有个开关：打开可以接收光线，关闭则重置。当按下快门后，CMOS清空电荷信息，并开始接收光线，光子进入到传感器，被光电二极管转化成电子，再由电容转化成电压，之后通过PGA放大电路放大，再经由模数转换器ADC转化成数字信号。从电压到数字信号的整个读出过程，只能依次逐行进行。",
         "sentences": [
            ["CMOS的每个像素都有个开关，打开接收光线。", "Every CMOS pixel is a switch: open to catch light.", "pixel（像素）"],
            ["光子被光电二极管转化成电子，再变成电压。", "Photons become electrons, then voltage, then digital.", "photodiode（光电二极管）"],
            ["读出过程只能依次逐行进行。", "Readout can only happen row by row.", "readout（读出）"]
         ]},
        {"id": "s2", "scene_zh": "读出速度与时间差", "scene_en": "Readout Speed and Time Gap", "time": "00:35",
         "context": "绝大多数CMOS由于性能制约，读出速度受限，动辄2、3、10毫秒。以20毫秒的读出速度为例，对应到每行像素，在图表上是一条斜线。想要做到每行像素曝光结束时可以同步读出，电子快门就只能严格按照这条斜线也就是读出速度，来控制每行像素的开启。无论快门如何调整，时间差都是20毫秒，远大于机械快门的4毫秒。",
         "sentences": [
            ["读出速度受限，动辄2、3、10毫秒。", "Readout often takes 2, 3, or 10 milliseconds.", "millisecond（毫秒）"],
            ["电子快门按读出速度的斜线逐行控制曝光。", "It follows that diagonal to expose row by row.", "diagonal（斜线）"],
            ["时间差固定20毫秒，远大于机械快门的4毫秒。", "The gap stays 20ms—far worse than the 4ms mechanical.", "time gap（时间差）"]
         ]},
        {"id": "s3", "scene_zh": "果冻效应", "scene_en": "Rolling Shutter Distortion", "time": "01:01",
         "context": "较高的时间差会出现一个严重的问题——果冻效应。由于每行像素记录的时间不同、存在时差，从而导致运动物体在空间位移中发生形变：直线变成斜的、旋转的变扭曲。以这个3300万像素的CMOS来看，拍摄一张照片需要读出4672行，按照20毫秒的读出速度计算，那么每行像素的时间差约等于4.3微秒。这听上去几乎不可感知，但对于拍摄高速运动的物体来说，这个时间差足以让画面产生明显的变形。面对高速运动的物体，使用机械快门同样会出现果冻效应，只是相比电子快门要好很多。",
         "sentences": [
            ["每行像素记录时间不同，运动物体会变形。", "Rows record at different times, so motion distorts.", "distort（变形）"],
            ["3300万像素按20毫秒读出，每行差4.3微秒。", "At 33MP and 20ms, each row lags ~4.3 microseconds.", "microsecond（微秒）"],
            ["拍高速物体时，机械快门果冻效应好很多。", "For fast subjects, mechanical rolling is far milder.", "milder（更轻微）"]
         ]},
        {"id": "s4", "scene_zh": "为什么机械快门不读出受影响", "scene_en": "Why Mechanical Readout Is Safe", "time": "01:42",
         "context": "控制果冻效应只有两种方法：一个是减少相对运动，一个是提高读出速度。有人会疑问，同样需要读出为什么机械快门不受影响。机械前帘的物理结构决定了CMOS可以先曝光、后逐行读出，而中间这部分读出期间，由于后帘的遮盖，CMOS虽然处在感光状态，但不会有光线进入，因此不受影响。",
         "sentences": [
            ["控制果冻效应：减少相对运动或提高读出速度。", "Fight rolling shutter by slowing motion or speeding readout.", "reduce（减少）"],
            ["机械快门先曝光、后逐行读出。", "Mechanical shutters expose first, read out later.", "expose first（先曝光）"],
            ["读出期间后帘遮盖，没有光线进入。", "The rear curtain blocks light during readout.", "rear curtain（后帘）"]
         ]},
        {"id": "s5", "scene_zh": "全域快门", "scene_en": "Global Shutter", "time": "02:06",
         "context": "电子快门可以做到同时开启并感光，但这样会导致后读出的像素因为感光时间更长，从而让画面整体曝光不均匀。同时曝光之后同时关闭也不行，关闭后意味着没有被读出的信息都会被重置。有没有办法做到同时曝光呢？有——全域快门。全域快门可以同时控制电路开启，曝光之后把电子先转移到存储单元，之后再读出数据，这样就不存在曝光时间差，也就能完全避免果冻效应。代价就是由于给每个像素增加了额外的存储单元，会降低像素接收光线的能力，进而对信噪比和画质产生影响。当然最大的影响还是——贵。",
         "sentences": [
            ["同时开但逐行读，会曝光不均匀。", "Expose all at once and late rows overexpose.", "uneven（不均匀）"],
            ["全域快门把电子先转移到存储单元再读出。", "A global shutter stores electrons first, then reads out.", "global shutter（全域快门）"],
            ["代价：像素接收光线能力下降，影响画质。", "The cost: reduced light capture, worse signal and image quality.", "signal-to-noise（信噪比）"]
         ]}
    ]
}

ARTICLES["aperture-definition-part1"] = {
    "title_zh": "相机“光圈” 底层逻辑科普，光圈如何定义（一）",
    "title_en": "Aperture Decoded, Part 1: The Definition",
    "duration": "53秒",
    "topic": "摄影 · 光圈",
    "scenes": [
        {"id": "s1", "scene_zh": "F值的反直觉", "scene_en": "F-Numbers Are Counterintuitive", "time": "00:00",
         "context": "我们常听到的光圈F1.4、F2.8、F4、F8、F16等等，这些说的其实是镜头的相对光圈值。这个数值越小代表实际的物理光圈越大，而数值越大则表示实际物理光圈越小。很多人可能会被这个相反的概念搞混，那我们不妨先看一下光圈的F值是如何定义的。",
         "sentences": [
            ["F1.4、F2.8这些是镜头的相对光圈值。", "F1.4, F2.8 and friends are relative aperture values.", "relative aperture（相对光圈）"],
            ["数值越小物理光圈越大，越大越小。", "Smaller numbers mean a bigger physical opening.", "physical opening（物理孔径）"],
            ["这个相反的概念常常把人搞混。", "That inversion confuses a lot of people.", "inversion（反转）"]
         ]},
        {"id": "s2", "scene_zh": "F值等于焦距除以入瞳径", "scene_en": "F = Focal Length / Entrance Pupil", "time": "00:18",
         "context": "光圈F值等于焦距除以入瞳径，也就是焦距与入瞳径的比值。而入瞳径很大程度上正是由这个物理光圈所控制的。什么是入瞳径？我们可以理解为从镜头前看向其内部的视觉开孔直径。它并不是真实的光圈叶片所控制的物理孔径。很多大光圈镜头前镜组采用高曲率或高折射率的镜片，其作用就是把入瞳径放大。",
         "sentences": [
            ["光圈F值等于焦距除以入瞳径。", "The F-number equals focal length over the entrance pupil.", "entrance pupil（入瞳）"],
            ["入瞳径是从镜头前看向内部的视觉开孔直径。", "The entrance pupil is the opening you see from the front.", "visual opening（视觉开孔）"],
            ["大光圈镜头用高折射率镜片放大入瞳径。", "Fast lenses use high-curvature elements to enlarge the pupil.", "refractive（折射率）"]
         ]}
    ]
}

ARTICLES["mechanical-shutter"] = {
    "title_zh": "学摄影需要知道的——机械快门",
    "title_en": "The Mechanical Shutter, Explained",
    "duration": "2分33秒",
    "topic": "摄影 · 相机知识",
    "scenes": [
        {"id": "s1", "scene_zh": "纵走前后双帘", "scene_en": "Vertical Front and Rear Curtains", "time": "00:00",
         "context": "目前大多数机械快门采用的都是纵走前后双帘的结构，不同相机的帘幕运动次序会有差别。通常先打开让传感器感光的叫做前帘，之后关闭结束感光的叫做后帘。当按下快门后前帘落下，相机清空CMOS中的电荷并开始感光；之后前帘抬起，传感器从下至上依次接触光线；到达设定时间后后帘抬起，此时CMOS仍处在感光状态，等所有信号逐行读出完毕，后帘复位，一次拍摄完成。",
         "sentences": [
            ["机械快门是纵走前后双帘结构。", "Most mechanical shutters use vertical front and rear curtains.", "curtain（帘幕）"],
            ["前帘打开让传感器开始感光。", "The front curtain opens to start exposing.", "front curtain（前帘）"],
            ["后帘关闭，逐行读出后复位。", "The rear curtain ends it, then resets after readout.", "rear curtain（后帘）"]
         ]},
        {"id": "s2", "scene_zh": "快门速度其实是曝光时长", "scene_en": "Shutter Speed Means Exposure Time", "time": "00:32",
         "context": "我们常说的100分之1秒、1000分之1秒等等的快门速度，惯性思维会让一些人误以为指的是机械帘幕的运动速度，这听上去很合理，实则不然。通常为了方便控制曝光时长，机械帘幕的运动速度大多是恒定的，一般为250分之1秒，也就是4毫秒。所以准确来说，快门速度通常指的是曝光时长，而非机械快门的运动速度。",
         "sentences": [
            ["有人误以为快门速度是帘幕的运动速度。", "Some assume shutter speed is the curtain's travel speed.", "travel speed（运动速度）"],
            ["帘幕运动速度恒定，一般是250分之1秒。", "The curtains always travel at 1/250s—about 4ms.", "constant（恒定的）"],
            ["快门速度通常指的是曝光时长。", "Shutter speed actually means exposure time.", "exposure time（曝光时长）"]
         ]},
        {"id": "s3", "scene_zh": "帘幕间隔控制曝光", "scene_en": "The Gap Controls Exposure", "time": "01:00",
         "context": "既然帘幕运动速度恒定，那它如何做到精确控制曝光呢？很简单，间隔。当前后帘开合的间隔越大，CMOS接受光线的时间也就越长，其他参数不变，整体进光量也就越多，画面更亮；反之，帘幕开合间隔越小，CMOS接收光线的时间也就越短，进光量更少，画面更暗。",
         "sentences": [
            ["帘幕间隔越大，CMOS接受光线越久，画面更亮。", "A wider gap means more light and a brighter frame.", "gap（间隔）"],
            ["间隔越小，进光越少，画面更暗。", "A narrower gap darkens the image.", "darker（更暗）"]
         ]},
        {"id": "s4", "scene_zh": "闪光同步速度", "scene_en": "Flash Sync Speed", "time": "01:55",
         "context": "机械快门依靠帘幕的开合遮挡来控制曝光，帘幕的运动速度恒定为4毫秒，这意味着：当曝光时间小于这个值时，帘幕会以夹缝的形态滚动，CMOS也就没有机会同时露出；当曝光时间大于或等于4毫秒时，CMOS则会有一定的时间同时露出，而在这个时间内，外界所施加的光就能被整个CMOS均匀捕获。这也是为什么多数闪光灯同步速度上限为250分之1秒的原因。",
         "sentences": [
            ["曝光小于4毫秒时，帘幕以夹缝形态滚动。", "Below 4ms the curtains roll as a slit.", "slit（夹缝）"],
            ["曝光≥4毫秒时，CMOS能同时整体露出。", "At 4ms or more the whole sensor gets fully exposed.", "fully exposed（整体露出）"],
            ["这就是闪光灯同步速度上限1/250秒的原因。", "That's why flash sync tops out at 1/250s.", "flash sync（闪光同步）"]
         ]}
    ]
}

ARTICLES["aperture-dof-formula"] = {
    "title_zh": "相机“光圈”底层逻辑科普，景深公式（五）",
    "title_en": "Aperture Decoded, Part 5: The DoF Formula",
    "duration": "1分48秒",
    "topic": "摄影 · 光圈",
    "scenes": [
        {"id": "s1", "scene_zh": "容许弥散圆定义景深", "scene_en": "The Circle of Confusion Sets Depth", "time": "00:00",
         "context": "前后移动焦点，能看到成像焦点脱离传感器，此时传感器上接收到的便是焦点之外逐渐扩大的弥散圆，因此这个物体点的成像就会慢慢变模糊。当然只要这个弥散圆足够小，人眼就无法辨别出模糊，自然也就认为是清晰的。这个足够小的弥散圆，就是我们前面说的容许弥散圆。",
         "sentences": [
            ["焦点脱离传感器，成像开始变模糊。", "As focus slips off the sensor, the image blurs.", "slip off（脱离）"],
            ["弥散圆足够小，人眼就无法辨别模糊。", "Small enough, the blur becomes invisible to the eye.", "indistinguishable（无法辨别）"],
            ["这个可接受的弥散圆叫容许弥散圆。", "That acceptable blur is the circle of confusion.", "circle of confusion（容许弥散圆）"]
         ]},
        {"id": "s2", "scene_zh": "0.029毫米", "scene_en": "0.029 Millimeters", "time": "00:22",
         "context": "以传感器大小36毫米×24毫米的全画幅相机来说，通常对其定义的容许弥散圆大小，放在手机上看差不多是这样。它的直径约为0.029毫米，只比发丝直径稍微大一点。为了方便演示，我们把这个容许弥散圆放大一些，再放到焦点的两侧与光线夹角大小吻合的位置，那么这个区间就是我们无法辨认出模糊的范围，称之为焦深。",
         "sentences": [
            ["全画幅的容许弥散圆直径约0.029毫米。", "On full frame, the circle of confusion is about 0.029mm.", "full frame（全画幅）"],
            ["它只比发丝直径稍微大一点。", "That's barely wider than a hair.", "hair（发丝）"],
            ["焦点两侧无法辨认模糊的区间叫焦深。", "The blur-free span around focus is the depth of focus.", "depth of focus（焦深）"]
         ]},
        {"id": "s3", "scene_zh": "景深公式计算", "scene_en": "Computing Depth of Field", "time": "00:52",
         "context": "与焦深对应，镜头之外物体前后相对清晰的范围，就是我们说的景深。想要准确计算出景深范围需要引入一个公式：这里的delta是容许弥散圆的直径0.029毫米，光圈设定到F8，焦距为35毫米，对焦距离是3米也就是3000毫米。带入这些设定的参数，再用景深公式计算就可以得出，此时画面的整个景深范围是5.034米也就是5034毫米，其中前景深约为1.087米，后景深为3.947米。",
         "sentences": [
            ["景深是镜头外物体前后相对清晰的范围。", "Depth of field is the acceptably sharp span beyond the lens.", "depth of field（景深）"],
            ["公式带入容许弥散圆0.029毫米、F8、35mm、3米。", "Plug in 0.029mm CoC, f/8, 35mm, and 3 meters.", "plug in（代入）"],
            ["算得总景深5.034米，前景深1.087米、后景深3.947米。", "That yields 5.034m total—1.087m front, 3.947m back.", "total（总）"]
         ]}
    ]
}

ARTICLES["aperture-affect-dof-6"] = {
    "title_zh": "相机“光圈”底层逻辑科普，如何影响景深（六）",
    "title_en": "Aperture Decoded, Part 6: What Shapes DoF",
    "duration": "2分19秒",
    "topic": "摄影 · 光圈",
    "scenes": [
        {"id": "s1", "scene_zh": "入瞳径决定景深", "scene_en": "The Entrance Pupil Decides", "time": "00:00",
         "context": "在控制其他变量的前提下，我们只缩小光圈，这时会发现入瞳径随之变小，光线夹角也同样变小，原来的光束变窄了，但容许弥散圆的直径是固定不变的。此时想要对应在光束上，就要把容许弥散圆向两侧延伸，这样一来焦深明显增大，对应的景深自然也就变大了。本质上影响景深变化的是入瞳径，而非物理光圈，但从另一面来说，入瞳径很大程度上受物理光圈的控制，所以大家通常也都会说光圈影响景深。",
         "sentences": [
            ["缩小光圈，入瞳径和光线夹角变小。", "Stopping down shrinks the pupil and the light cone.", "light cone（光锥）"],
            ["容许弥散圆固定，向两侧延伸焦深变大。", "The fixed CoC stretches out, widening the depth of focus.", "stretch（延伸）"],
            ["本质上是入瞳径影响景深，不是物理光圈。", "It's the entrance pupil, not the blades, that rules DoF.", "essentially（本质上）"]
         ]},
        {"id": "s2", "scene_zh": "光圈大小与景深", "scene_en": "Aperture Size vs Depth", "time": "00:36",
         "context": "当调小光圈，入瞳直径缩短，光线夹角随之变小，景深范围相应增大，景深更深；当光圈放大，入瞳直径增长，光线夹角随之变大，景深范围也就会减小，因此景深更浅。另一个影响景深很重要的因素，就是被摄物体与相机的距离，其原因同样是距离的改变影响了入射光线夹角的大小，那自然也会改变容许弥散圆所定义的区间，景深便随之产生变化。",
         "sentences": [
            ["光圈小、景深深；光圈大、景深浅。", "Small aperture, deep field; large aperture, shallow field.", "shallow（浅）"],
            ["拍摄距离也影响景深，因为它改变光线夹角。", "Subject distance matters too—it changes the light cone.", "subject distance（拍摄距离）"]
         ]},
        {"id": "s3", "scene_zh": "光圈的别的影响", "scene_en": "Aperture's Other Effects", "time": "01:33",
         "context": "除了曝光和景深之外，光圈还会有一些别的影响：例如光圈叶片的数量和形状影响着焦外光斑是否圆润；还有光圈缩小到一定程度，由于光路狭小造成的衍射，会对成像质量有所限制。当然也会有人专门利用这些特性去制作镜头，来拍摄例如星芒效果的风格化影像。",
         "sentences": [
            ["叶片数量和形状影响焦外光斑是否圆润。", "Blade count and shape round out the bokeh.", "bokeh（焦外）"],
            ["光圈过小产生衍射，限制成像质量。", "Tiny apertures diffract and soften the image.", "diffraction（衍射）"],
            ["也有人利用衍射特性拍星芒。", "Some use it on purpose to shoot starbursts.", "starburst（星芒）"]
         ]}
    ]
}

ARTICLES["aperture-coc-part4"] = {
    "title_zh": "相机“光圈”底层逻辑科普，弥散圆（四）",
    "title_en": "Aperture Decoded, Part 4: The Circle of Confusion",
    "duration": "1分51秒",
    "topic": "摄影 · 光圈",
    "scenes": [
        {"id": "s1", "scene_zh": "可接受的弥散圆", "scene_en": "The Acceptable Blur", "time": "00:00",
         "context": "这是一个圆形，看上去有些模糊，我们暂且称它为弥散圆。如果此时你的观看设备是6英寸大小的手机，并且观看距离差不多是30厘米的话，那么当把这个弥散圆缩小再缩小，缩小到一定的尺寸，此时很多人应该就察觉不到它的模糊，从视觉上它便是一个可接受的清晰的圆。而这个可接受的弥散圆，我们就可以称之为容许弥散圆。",
         "sentences": [
            ["模糊的圆形光斑叫弥散圆。", "The blurred circle of light is a circle of confusion.", "blurred（模糊的）"],
            ["缩小到一定尺寸，人眼就察觉不到模糊。", "Shrink it enough and the blur becomes invisible.", "shrink（缩小）"],
            ["可接受的弥散圆叫容许弥散圆。", "That acceptable size is the circle of confusion.", "acceptable（可接受的）"]
         ]},
        {"id": "s2", "scene_zh": "凸透镜成像", "scene_en": "Imaging With a Simple Lens", "time": "00:26",
         "context": "众所周知，镜头通常由多组多枚镜片构成，其目的是为了更好的汇聚光线、优化成像品质，但其实根本还是利用了凸透镜的成像原理。这里为了方便演示，我们不妨把它简化一下：一个凸透镜用于成像，一个光圈用于控制通光孔径。学过小学几何的肯定都知道，一个面可以由无数个点组成，取其中一个把焦点对在上面，理论上这个点可以无限小，不过由于传感器的物理限制，可以成像的最小单位也就是一个像素点。",
         "sentences": [
            ["镜头再复杂，根本还是凸透镜成像原理。", "Even complex lenses still rely on a simple convex lens.", "convex lens（凸透镜）"],
            ["一个凸透镜成像，一个光圈控光。", "One lens to image, one aperture to control light.", "aperture（光圈）"],
            ["传感器的成像最小单位是一个像素点。", "The sensor's smallest image unit is one pixel.", "pixel（像素）"]
         ]},
        {"id": "s3", "scene_zh": "焦点与弥散圆", "scene_en": "Focus and the Blur Circle", "time": "00:51",
         "context": "从这一点反射出的光会有一部分进入镜头，经由凸透镜折射之后再汇聚到成像光屏，也就是相机的传感器。理想状态下，经过凸透镜折射的光线会如同一束光束，完美汇聚到一个交叉点之后再分散开来，这个交叉点称之为焦点。如果焦点和传感器重合，此时物体面的那个点便能清晰地呈现在画面上；严格来说只有光线汇聚的交叉点也就是焦点上成像才是最清晰的，而在这个汇聚点之外的光束上，我们可以想象成有无数个扩散且模糊的圆，也就是我们前面提到的弥散圆。",
         "sentences": [
            ["光线经凸透镜折射后汇聚到一个焦点。", "Refracted rays meet at one focal point.", "focal point（焦点）"],
            ["焦点与传感器重合，画面就清晰。", "When focus hits the sensor, the image is sharp.", "coincide（重合）"],
            ["焦点之外的光束上是无数扩散的弥散圆。", "Away from focus, the beam fans into spreading blur circles.", "spreading（扩散的）"]
         ]}
    ]
}

ARTICLES["aperture-depth-of-field"] = {
    "title_zh": "相机“光圈”底层逻辑科普，景深是什么？（三）",
    "title_en": "Aperture Decoded, Part 3: What Is Depth of Field",
    "duration": "1分12秒",
    "topic": "摄影 · 光圈",
    "scenes": [
        {"id": "s1", "scene_zh": "背景虚化与景深", "scene_en": "Bokeh and Depth of Field", "time": "00:00",
         "context": "就算不了解景深的朋友，也一定听过另一个词：背景虚化。通常在一个场景中，人物主体清晰，而背景是虚化模糊的。我们想象一下，人物和相机之间有一条纵向轴线，当我们把焦点设定在人物主体上，此时人物前后会有一段相对清晰的区间，我们把相对清晰的这一区间称作景深。",
         "sentences": [
            ["背景虚化是大家最熟悉的摄影效果。", "Background blur is photography's most familiar look.", "background blur（背景虚化）"],
            ["人物前后有一段相对清晰的区间。", "In front of and behind the subject lies a sharp zone.", "sharp zone（清晰区间）"],
            ["这段相对清晰的区间就叫景深。", "That relatively sharp zone is the depth of field.", "depth of field（景深）"]
         ]},
        {"id": "s2", "scene_zh": "光圈大小决定清晰范围", "scene_en": "Aperture Sets the Sharp Zone", "time": "00:28",
         "context": "把焦点对着人物主体调大光圈，此时除了焦点前后一段范围相对清晰，其他地方开始逐渐模糊。光圈越小，清晰的范围越大，一般称之为深景深或者大景深；反之光圈越大，这个清晰的范围就越小，称之为浅景深。简单来说，景深就是对焦点前后能被人眼识别为清晰的范围。实际上直接影响景深的是入瞳径，而非物理光圈，那么为什么大家会说光圈影响景深，以及该如何定义这个景深的范围，这里就要涉及到另一个概念：容许弥散圆。",
         "sentences": [
            ["调大光圈，只有焦点前后一小段清晰。", "Wide open, only a sliver around focus stays sharp.", "sliver（一小段）"],
            ["光圈越小景深越深，越大景深越浅。", "Smaller aperture deepens it; larger makes it shallow.", "deep vs shallow（深与浅）"],
            ["直接影响景深的是入瞳径，引出容许弥散圆。", "The pupil really rules DoF—enter the circle of confusion.", "circle of confusion（容许弥散圆）"]
         ]}
    ]
}

ARTICLES["aperture-calc-part2"] = {
    "title_zh": "相机“光圈” 底层逻辑科普，光圈计算（二）",
    "title_en": "Aperture Decoded, Part 2: The Math",
    "duration": "1分08秒",
    "topic": "摄影 · 光圈",
    "scenes": [
        {"id": "s1", "scene_zh": "入瞳直径计算", "scene_en": "Computing the Pupil Diameter", "time": "00:00",
         "context": "这是一颗50毫米的定焦镜头，当光圈值为最大的F1.2，根据公式我们可以算出此时的入瞳直径大约是42毫米；而把光圈值调到F16，此时的入瞳直径仅约为3毫米。明白了这些我们就不难理解，光圈是如何控制曝光的：当调大光圈，入瞳径随之变大，光通面积自然也就更大，相应的相机传感器接收到的光线照度就会变强，因此呈现出来的画面看起来更亮；如果光圈调小，画面就会更暗。",
         "sentences": [
            ["50mm镜头F1.2时，入瞳直径约42毫米。", "At f/1.2 the 50mm lens has a 42mm entrance pupil.", "entrance pupil（入瞳）"],
            ["F16时入瞳直径只剩约3毫米。", "At f/16 it shrinks to about 3mm.", "shrink（缩小）"],
            ["入瞳径越大，进光越多，画面越亮。", "Bigger pupil, more light, brighter image.", "brighter（更亮）"]
         ]},
        {"id": "s2", "scene_zh": "F值与照度的平方反比", "scene_en": "Inverse-Square Law of f-Numbers", "time": "00:41",
         "context": "实际上光圈的F值与成像面照度是近似平方反比的关系，也就是F值每改变1.4倍，成像面照度便会相应的成两倍变化。虽然成像面照度跟光通面积不能混为一谈，但在不同的F值下得出的入瞳直径，既然按算术来看其光通面积，同样也是符合这个规律的。光圈除了能控制曝光，还会影响一个非常重要的成像特性：景深。",
         "sentences": [
            ["F值与成像面照度近似平方反比。", "Illuminance is roughly the inverse square of the f-number.", "inverse square（平方反比）"],
            ["F值每改变1.4倍，照度变化2倍。", "Each 1.4x in f-number doubles or halves the light.", "double（加倍）"],
            ["光圈还影响另一个重要特性：景深。", "Aperture also shapes depth of field.", "depth of field（景深）"]
         ]}
    ]
}

ARTICLES["photo-composition-aesthetics"] = {
    "title_zh": "构图对一张照片来说有多重要？",
    "title_en": "Why Composition Matters",
    "duration": "1分07秒",
    "topic": "摄影 · 构图",
    "scenes": [
        {"id": "s1", "scene_zh": "构图背后的美学法则", "scene_en": "The Aesthetics Behind Composition", "time": "00:00",
         "context": "你以为你很懂构图吗？真正懂构图的人不仅停留在三分线、黄金分割线这些基础的公式上，而是懂得构图背后的审美法则。比如这个箭头：箭头靠右就会觉得压抑，箭头靠左就会舒服很多。所以在拍这个画面时，就不会把人放在右边导致视线轨迹受阻，而是放在左边，为视线方向留白，引导视觉空间。",
         "sentences": [
            ["懂构图的人不停留在三分线和黄金分割。", "Real composition isn't just rule-of-thirds or golden ratio.", "rule of thirds（三分法）"],
            ["箭头靠右压抑，靠左舒服。", "An arrow on the right feels tight; on the left, relaxed.", "visual tension（视觉张力）"],
            ["为视线方向留白，引导视觉空间。", "Leave space in the viewing direction to lead the eye.", "lead the eye（引导视线）"]
         ]},
        {"id": "s2", "scene_zh": "视觉重量与平衡", "scene_en": "Visual Weight and Balance", "time": "00:19",
         "context": "现在把这个箭头换成一个方块，把它移到左边就会左重右轻，造成构图失衡。想要恢复平衡，就需要在右边增加一个元素，如同在跷跷板的另一端放上重物。所以是这样构图，而不是这样构图。",
         "sentences": [
            ["元素偏左会左重右轻、构图失衡。", "A block on the left tips the frame—unbalanced.", "unbalanced（失衡）"],
            ["在另一端加元素，像跷跷板一样找平衡。", "Add weight opposite, like a seesaw.", "seesaw（跷跷板）"],
            ["平衡靠对比和呼应，不是平均。", "Balance comes from counterweights, not symmetry.", "counterweight（配重）"]
         ]},
        {"id": "s3", "scene_zh": "从本质了解构图", "scene_en": "Learn Composition From First Principles", "time": "00:31",
         "context": "这本书最厉害的地方，就是它让你通过本质了解构图。它不是讲三分法、九宫格这种基础构图，而是深入到美学、数学和观众心理学，帮你构建牢固的审美体系。不管是审美的视觉重量，还是抽象的格式塔理论，包括色彩对构图的影响等等，都讲得特别透彻。每个术语都会配专业的摄影作品以及几个对比图片，让你知道什么画面是好的，而且能说出好在哪里，哪怕是新手小白也能看懂。",
         "sentences": [
            ["从美学、数学和观众心理学理解构图。", "Understand composition through aesthetics, math, and viewer psychology.", "viewer psychology（观众心理学）"],
            ["视觉重量和格式塔理论都讲得很透彻。", "Visual weight and Gestalt theory get deep coverage.", "Gestalt（格式塔）"],
            ["配专业作品和对比图，能说出好在哪里。", "Paired with masterworks and comparisons, you can say why it works.", "comparison（对比）"]
         ]}
    ]
}

ARTICLES["audio-channel-select"] = {
    "title_zh": "收藏！一个视频弄懂收音时的声道选择",
    "title_en": "Channel Selection for Recording Audio",
    "duration": "5分01秒",
    "topic": "音频 · 收音",
    "scenes": [
        {"id": "s1", "scene_zh": "单声道与立体声", "scene_en": "Mono vs Stereo", "time": "00:00",
         "context": "音频时不同声道究竟是什么意思，怎么设置才能不翻车？一个视频弄懂录音时的单声道、立体声和双声道录音。最简单的录音就是一个人、别一个发射器一个接收器。这时候该怎么设置呢？接收器里边咱们选择单声道，它相当于把一个麦克风的声音同时录进了左右两声道，这是咱们平时听到最多的声音。",
         "sentences": [
            ["单声道把一个麦克风的声音同时录进左右两声道。", "Mono records one mic into both left and right.", "mono（单声道）"],
            ["这是平时听到最多的声音。", "It's the sound we hear most often.", "most common（最常见）"]
         ]},
        {"id": "s2", "scene_zh": "只有一边有声音", "scene_en": "Sound Only on One Side", "time": "00:27",
         "context": "你在录音时有没有遇到这种情况：声音只有左边耳朵有，或者只有右边耳朵有，耳机也没坏。这种情况多半是你在录音时选择了双声道，有时候也叫立体声。只要选择双声道，相当于你一个麦克风的声音只录制在了左右声道中的一个。这个时候也不用急，咱们在软件里复制到另外一个声道就可以。",
         "sentences": [
            ["只有一只耳朵有声，多半是选了双声道。", "Sound in one ear usually means you picked stereo.", "stereo（立体声）"],
            ["一个麦克风的声音只进了左右中的一个。", "The single mic landed in only one channel.", "channel（声道）"],
            ["在软件里复制到另一个声道就行。", "Fix it by copying into the other channel.", "copy（复制）"]
         ]},
        {"id": "s3", "scene_zh": "软件里修复声道", "scene_en": "Fixing Channels in Software", "time": "00:44",
         "context": "这段素材就是只有左声道有声音，右声道没有。在剪映里，音频最后一项声道配置打开，把左声道填充至右声道，这时两声道都有声音了。在Premiere里面是这样：选择素材右键片段属性里面有一个音频，然后把没有声音的选成有声音的这个声道，然后点OK，两声道都有声音了。",
         "sentences": [
            ["剪映：声道配置里把左声道填充至右声道。", "In CapCut, fill the right channel from the left.", "fill（填充）"],
            ["PR：片段属性里把无声声道改成有声的。", "In Premiere, route the silent channel to the live one.", "route（路由）"]
         ]},
        {"id": "s4", "scene_zh": "双人录音的声道选择", "scene_en": "Channels for Two Speakers", "time": "01:20",
         "context": "单人录音没有问题的。如果你是双人录音，那么俩嘉宾一人一个发射器、一个接收器。现在还是俩选择：选单声道，俩嘉宾的声音不分左右，直接混到这个音频里面，没啥说的。但是俩嘉宾如果说声音大小不一样、或者声线不一样，后期你想单独调他的或者调她的，单声道模式下就没法调，它是混在一起的。这个时候建议选择双声道，一个嘉宾一个声道。",
         "sentences": [
            ["双人录音选单声道，声音会混在一起。", "Mono mixes both guests into one track.", "mix（混合）"],
            ["两人音量声线不同，后期没法单独调。", "If their levels differ, you can't fix them separately.", "separately（单独地）"],
            ["建议双声道：一个嘉宾一个声道。", "Choose stereo—one guest per channel.", "per channel（每声道）"]
         ]},
        {"id": "s5", "scene_zh": "双声道素材的处理", "scene_en": "Handling Stereo Clips", "time": "01:49",
         "context": "处理这种素材分两步。剪映专业版：咱们选中素材，分离音频，然后把刚才分离的音频再复制一份，选择一个音频，在声道配置里跟刚才一样把左声道填充到右声道，另外一个音频呢，还是一样，把右声道复制到左声道，这样的话俩嘉宾的声音就正常了，咱们可以单独控制。达芬奇里面的操作差不多：选中素材取消它们的关联，Alt再复制一段音频，选择其中一段的片段属性，音频然后选择一样，另外一个也是片段属性。",
         "sentences": [
            ["分离音频后复制一份，分别填充左右。", "Split the audio, duplicate it, fill each side.", "duplicate（复制）"],
            ["左填右、右填左，两人声音就正常了。", "Left to right, right to left—both voices come alive.", "come alive（恢复正常）"],
            ["达芬奇取消关联后再复制，操作类似。", "In Resolve, unlink, duplicate, then reroute.", "unlink（取消关联）"]
         ]},
        {"id": "s6", "scene_zh": "一拖四多轨录音", "scene_en": "Four-Channel Multi-Track", "time": "02:34",
         "context": "我已经听到有小伙伴说，嘉宾练多、四个人，咋设置单独的音频轨道呢？这稍微有点进阶，需要特定的麦克风和相机。大疆Mic三默认是一拖二，咱们再准备两个发射器，长按链接按钮配对，接收器里设备配对选择TX。配对完成后在主界面可以看到四个麦克风的图标，RX设置里把声道选择四声道。相机部分：索尼相机搭配大疆Mic三的热靴转接，装上之后进到菜单，录制-录音-MI音频设置，选择四轨。拖到达芬奇里看，四条音轨现在可以单独控制。",
         "sentences": [
            ["四个人就要用一拖四和多轨麦克风。", "Four people need a one-to-four rig and multi-track.", "multi-track（多轨）"],
            ["大疆Mic三默认一拖二，再配两个发射器。", "The DJI Mic 3 ships 1-to-2; add two more transmitters.", "transmitter（发射器）"],
            ["RX设四声道，相机MI音频设四轨。", "Set RX to four channels and the camera to four tracks.", "four tracks（四轨）"]
         ]},
        {"id": "s7", "scene_zh": "四轨后期与内录双保险", "scene_en": "Post on Four Tracks, Plus Safety Recs", "time": "03:55",
         "context": "达芬奇里四条音轨每一条现在可以单独控制。剪映专业版拖进去以后只有一条音轨，不用慌，咱们选中素材分离音频，然后把音频复制三份，选择第二段切换多音轨音轨二，第三段切音轨三，第四段切音轨四，每一段可以单独控制。一拖多的声音很适合多个嘉宾或多个声源的录制场景，四个轨道每个都能单独调，后期的自由度更大。另外录音过程还是建议结合发射器的内录来使用，文件类型可以选择原文件和处理文件，发射器能同步录一条三脚架位的原始音频和处理过的音频，即使相机录制出现问题，发射器内录的文件也给录制过程加了双保险。",
         "sentences": [
            ["剪映拖入只有一条音轨，分离后复制三份切换多音轨。", "CapCut shows one track—split, copy three times, switch tracks.", "switch tracks（切换音轨）"],
            ["一拖四适合多嘉宾，后期自由度大。", "Multi-track suits many guests and gives post freedom.", "freedom（自由度）"],
            ["配合发射器内录，等于加了双保险。", "Pair with on-board recording as a safety net.", "safety net（双保险）"]
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
        words = words + ["exposure", "sensor", "pixel", "shutter", "signal", "noise", "dynamic", "range", "gain", "digital"][: 20 - len(words)]

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
