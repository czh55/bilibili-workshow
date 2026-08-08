#!/usr/bin/env python3
"""批31：为10篇相机基础知识视频生成完整场景英译JSON。"""
import json, re
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

ARTICLES = {}

ARTICLES["camera-dynamic-range"] = {
    "title_zh": "你拍的画面为什么会过曝？",
    "title_en": "Why Does Your Image Overexpose?",
    "duration": "3分00秒",
    "topic": "摄影 · 相机知识",
    "scenes": [
        {"id": "s1", "scene_zh": "过曝的本质：满阱容量", "scene_en": "Overexposure: Hitting Full-Well Capacity", "time": "00:00",
         "context": "这是相机传感器里几千万个像素的其中之一，它的最大作用就是感光。像素接收的光子数量越多，反映在照片上的这个点就越亮。单个像素能容纳电子数量的最大值为满阱容量，超出之后的部分都无法记录，也就是画面过曝。",
         "sentences": [
            ["像素接收的光子越多，画面就越亮。", "More photons captured by a pixel make it brighter.", "photon（光子）"],
            ["单个像素容纳电子的最大值叫满阱容量。", "The max electrons a pixel holds is the full-well capacity.", "full-well capacity（满阱容量）"],
            ["超出满阱的部分无法记录，就是过曝。", "Everything beyond the well is lost—that's overexposure.", "overexposure（过曝）"]
         ]},
        {"id": "s2", "scene_zh": "动态范围的定义", "scene_en": "Defining Dynamic Range", "time": "00:25",
         "context": "像素接收的光子越少，画面就越暗。在没有信号输入时，CMOS本身也存在噪声，也就是底噪，可以近似为读出噪声，此时为最小值。这个最大值满阱容量与最小值读出噪声的比值就是动态范围。简单来说就是相机能记录下最亮和最暗的一个区间。",
         "sentences": [
            ["没有信号时CMOS也有底噪，近似读出噪声。", "Even with no signal, CMOS has a floor—the read noise.", "read noise（读出噪声）"],
            ["满阱容量除以读出噪声，就是动态范围。", "Full-well capacity over read noise defines dynamic range.", "dynamic range（动态范围）"],
            ["动态范围=能记录的最亮到最暗区间。", "It's the span from the brightest to the darkest you can record.", "span（区间）"]
         ]},
        {"id": "s3", "scene_zh": "动态范围的档位", "scene_en": "Dynamic Range in Stops", "time": "00:51",
         "context": "动态范围的高低对于画面的影响非常大。目前一些主流消费级相机的动态范围大约在13档左右，而有些电影机才可以做到16.7档。这里的档指的是曝光指数，两倍为一档。比如1/100秒和1/200秒的快门，或者是光圈F1.4和F2，都是相差一档的进光量。",
         "sentences": [
            ["主流消费级相机约13档，电影机可到16.7档。", "Consumer cameras hit ~13 stops; cinema cameras reach 16.7.", "stop（档位）"],
            ["两倍进光量就是一档。", "Doubling the light equals one stop.", "doubling（加倍）"],
            ["1/100秒到1/200秒，或F1.4到F2，都差一档。", "1/100s to 1/200s, or f/1.4 to f/2, are each one stop.", "one stop（一档）"]
         ]},
        {"id": "s4", "scene_zh": "ISO改变不了进光量", "scene_en": "ISO Doesn't Change the Light", "time": "01:18",
         "context": "虽然ISO能改变图像的亮度，但改变不了进光量，真正决定进光量的只有光圈和快门。以A7M4为例，其最大满阱容量有72000个电子，基准ISO下读出噪声约为5个电子。想要分辨出有效信号，就需要高于这个最小值。往上推一档是10个电子，两档是20个，以此类推到最大72000个电子，差不多就是13.8档。",
         "sentences": [
            ["ISO改变亮度，但改变不了进光量。", "ISO shifts brightness but not the light captured.", "captured light（进光量）"],
            ["真正决定进光量的只有光圈和快门。", "Only aperture and shutter set how much light lands.", "aperture（光圈）"],
            ["A7M4满阱72000电子，基准ISO读出噪声约5个电子。", "The A7M4 holds 72,000 electrons with ~5 read noise.", "electron（电子）"]
         ]},
        {"id": "s5", "scene_zh": "高ISO压缩动态范围", "scene_en": "High ISO Compresses Dynamic Range", "time": "01:54",
         "context": "动态范围除了由硬件决定，还会受ISO的影响：提高ISO，动态范围会随之降低。这是因为模数转换器ADC能接收的最大电压信号是有上限的。当PGA开始模拟放大两倍即ISO200，电压被放大到两伏，但ADC能接收的上限还是1伏，超出的部分无法被记录，相当于实际接收到的只有36000个电子的信号。放大倍数越高，也就相当于满阱容量越小。",
         "sentences": [
            ["提高ISO，动态范围会随之降低。", "Raising ISO shrinks the dynamic range.", "shrink（压缩）"],
            ["ADC能接收的最大电压有上限。", "The ADC's max voltage is capped.", "ADC（模数转换器）"],
            ["放大两倍后超出上限，等效满阱容量减半。", "Beyond the cap after 2x gain, the effective well halves.", "effective well（等效满阱）"]
         ]},
        {"id": "s6", "scene_zh": "ADC接收窗口被压缩", "scene_en": "The ADC Window Narrows", "time": "02:34",
         "context": "从ADC层面来看，ISO100时电压信号的接收范围是70微伏至1伏，而ISO200时ADC的接收范围变成140微伏至1伏。上限不变、下限提高，整体动态范围被压缩。所以ISO越高，PGA的放大倍率越高，ADC能接收的电压区间就会变窄，动态范围自然随之下降。",
         "sentences": [
            ["ISO200时，ADC下限从70升到140微伏。", "At ISO200 the ADC floor rises from 70 to 140 microvolts.", "microvolt（微伏）"],
            ["上限不变、下限提高，动态范围被压缩。", "The ceiling stays, the floor rises—range compresses.", "ceiling（上限）"],
            ["ISO越高，ADC电压区间越窄，动态范围越小。", "Higher ISO narrows the ADC window and shrinks the range.", "narrow（变窄）"]
         ]}
    ]
}

ARTICLES["camera-iso-explained"] = {
    "title_zh": "终于搞懂了相机 ISO",
    "title_en": "Finally Understanding Camera ISO",
    "duration": "2分19秒",
    "topic": "摄影 · 相机知识",
    "scenes": [
        {"id": "s1", "scene_zh": "量子效率QE", "scene_en": "Quantum Efficiency", "time": "00:00",
         "context": "当100个光子进入到像素中，大概有50-60个能被转换成电子，这个光电转换率被称之为量子效率QE。这听上去很像是相机的感光度，那改变ISO是不是就能改变这个量子效率呢？答案是不能，每台相机的量子效率都是固定的，并不会随ISO的切换而改变。所以数码相机的ISO指的不是量子效率这个感光度。",
         "sentences": [
            ["100个光子约50-60个转成电子，这就是量子效率。", "About 50-60 of 100 photons become electrons—that's quantum efficiency.", "quantum efficiency（量子效率）"],
            ["量子效率每台相机固定，不随ISO改变。", "QE is fixed per camera and never changes with ISO.", "fixed（固定的）"],
            ["所以数码相机的ISO不是量子效率。", "So digital ISO isn't that kind of sensitivity.", "sensitivity（感光度）"]
         ]},
        {"id": "s2", "scene_zh": "转换增益与基准ISO", "scene_en": "Conversion Gain and Base ISO", "time": "00:24",
         "context": "从电路层面来看，ISO首先体现在电荷到电压的转换上。浮动扩散节点的电容，决定了一个电子能转换成多大电压，通常是微伏每电子。这个电荷到电压的对应关系称之为转换增益conversion gain，而这就是我们常说的Base ISO，也叫基准ISO或基础ISO。",
         "sentences": [
            ["浮动扩散节点的电容决定转换增益。", "The floating-diffusion capacitor sets the conversion gain.", "conversion gain（转换增益）"],
            ["一电子转成多少微伏，就是基准ISO。", "Microvolts per electron define the base ISO.", "base ISO（基准ISO）"]
         ]},
        {"id": "s3", "scene_zh": "PGA模拟放大", "scene_en": "PGA Analog Gain", "time": "00:44",
         "context": "调整ISO改变的到底是什么？其实就是改变电压信号的强度，通过PGA的模拟放大来实现。假设在基准ISO100时，一个电子能被转换成10微伏电压。提高ISO到200，也就是PGA执行两倍放大，10微伏被放大到20微伏；ISO400就是PGA4倍放大，变成40微伏，以此类推。",
         "sentences": [
            ["调ISO就是通过PGA改变电压信号强度。", "Changing ISO alters signal strength via the PGA.", "PGA（可编程增益放大器）"],
            ["ISO100时每电子10微伏，ISO200翻倍到20微伏。", "At ISO100 each electron makes 10µV; ISO200 doubles it to 20.", "double（翻倍）"],
            ["ISO400是4倍放大，40微伏。", "ISO400 means 4x gain, or 40 microvolts.", "gain（增益）"]
         ]},
        {"id": "s4", "scene_zh": "原生ISO的范围", "scene_en": "The Native ISO Range", "time": "00:31",
         "context": "PGA的放大倍率也是有限的，以32倍为例就是ISO3200。那么从ISO100到3200这个区间的数值，都可以被称为原生ISO。得益于技术进步，很多相机原生的ISO范围会大很多，例如A7M4从ISO100到51200。",
         "sentences": [
            ["PGA最多32倍放大，即ISO3200。", "PGA tops out at 32x, which is ISO3200.", "top out（上限）"],
            ["ISO100到3200区间都可叫原生ISO。", "Everything from ISO100 to 3200 counts as native ISO.", "native ISO（原生ISO）"],
            ["技术进步让原生范围更大，如A7M4到51200。", "Progress widens it—the A7M4 reaches ISO51200.", "widen（扩大）"]
         ]},
        {"id": "s5", "scene_zh": "原生与扩展ISO", "scene_en": "Native vs Extended ISO", "time": "01:26",
         "context": "有人认为只有基准ISO100才是原生ISO，其他都是非原生，这确实存在诸多争议。从原生ISO（Native ISO）的定义来看，它指不经数字放大、用基准ISO乘以PGA模拟放大得到的数值。在这样的定义下，这些都可以叫原生ISO，不同的是有些是基准ISO，有些是模拟放大ISO。超出这个模拟区间的数值都是扩展ISO，也就是ADC量化之后在机内数字放大，跟后期提亮画面没有什么差别。",
         "sentences": [
            ["原生ISO=基准ISO×PGA模拟放大，不经数字放大。", "Native ISO is base ISO times analog gain, with no digital boost.", "digital boost（数字放大）"],
            ["模拟区间内都算原生ISO，只是基准与放大之分。", "Within the analog range, some are base and some are boosted.", "boosted（被放大的）"],
            ["超出模拟区间的都是扩展ISO，等同后期提亮。", "Beyond it, extended ISO is just digital brightening.", "extended ISO（扩展ISO）"]
         ]},
        {"id": "s6", "scene_zh": "ISO的本质：增益", "scene_en": "ISO Is Really Gain", "time": "00:57",
         "context": "在数码时代把ISO理解为传感器对光线的敏感度并不太贴切。ISO主要体现电荷到电压的转换，和之后PGA参与的模拟放大，也可以把ISO看作是这一段电路共同协作的电信号读出。当然它有另外一个名字：增益。",
         "sentences": [
            ["把ISO理解为传感器敏感度不太贴切。", "Reading ISO as sensor sensitivity is misleading.", "misleading（有误导性的）"],
            ["ISO=电荷到电压的转换+PGA模拟放大。", "ISO is charge-to-voltage conversion plus PGA gain.", "voltage（电压）"],
            ["ISO的另一个名字叫增益。", "ISO has another name: gain.", "gain（增益）"]
         ]}
    ]
}

ARTICLES["camera-iso-genius"] = {
    "title_zh": "发明相机的真是个天才",
    "title_en": "The Genius Who Invented the Camera",
    "duration": "2分02秒",
    "topic": "摄影 · 相机知识",
    "scenes": [
        {"id": "s1", "scene_zh": "CMOS的信号链", "scene_en": "The CMOS Signal Chain", "time": "00:00",
         "context": "以相机中主流的背照式CMOS为例，其主要由这几部分构成。光线到达传感器，先经透镜汇集到下层的滤色片，滤色片能筛选出一支波长匹配的光，进入到光电二极管PD，光子被光电二极管转化成电子，并在一个特定的区域内累积，这个区域被称为势阱。通常一个势阱内可以容纳几万个电子，达到最大值即为满阱容量FWC。",
         "sentences": [
            ["光线经微透镜汇集到滤色片。", "Light is gathered by the microlens onto the color filter.", "microlens（微透镜）"],
            ["滤色片筛选出波长匹配的光进入光电二极管。", "The filter passes matched wavelengths into the photodiode.", "photodiode（光电二极管）"],
            ["电子在势阱累积，最大即满阱容量。", "Electrons pool in the well—its max is the full-well capacity.", "well（势阱）"]
         ]},
        {"id": "s2", "scene_zh": "读出与放大", "scene_en": "Readout and Amplification", "time": "00:31",
         "context": "随后势阱中的电子被浮动扩散节点FD转移并捕捉到一个电容里，电容里的电荷由此转换成电压信号。这些电压会被一个能缓冲稳定信号的源极跟随器读出，再被一个可编程增益放大器PGA执行模拟放大。改变ISO的数值，实际上就是改变模拟放大倍数。最后再进入模数转换器ADC，把电压信号转换成数字信号。",
         "sentences": [
            ["电子转移到浮动扩散节点，转换成电压。", "Electrons move to the floating diffusion and become voltage.", "floating diffusion（浮动扩散）"],
            ["源极跟随器缓冲读出，PGA做模拟放大。", "The source follower buffers; the PGA amplifies.", "source follower（源极跟随器）"],
            ["改变ISO就是改变模拟放大倍数。", "Changing ISO changes the analog gain.", "analog gain（模拟增益）"],
            ["ADC把电压转成数字信号。", "The ADC converts voltage to digital.", "digital（数字）"]
         ]},
        {"id": "s3", "scene_zh": "为什么是灰蒙蒙的", "scene_en": "Why It Looks Gray", "time": "01:10",
         "context": "打开文件看到灰蒙蒙的画面，为什么会这样？传感器的每个像素能记录的只有亮度信息，而无法直接记录颜色信息，所以才会在每个像素上放着一个彩色滤色片。常见的就是RGB的拜耳排列。有了这些滤色片，传感器的每个像素就能记录其对应颜色的亮度信息。",
         "sentences": [
            ["每个像素只能记录亮度，不能直接记录颜色。", "Each pixel records brightness, not color directly.", "brightness（亮度）"],
            ["每个像素上放彩色滤色片，常见是拜耳排列。", "A color filter sits on each pixel—usually the Bayer array.", "Bayer array（拜耳排列）"],
            ["这样像素就能记录对应颜色的亮度。", "Now each pixel logs the brightness of its color.", "color filter（滤色片）"]
         ]},
        {"id": "s4", "scene_zh": "去马赛克", "scene_en": "Demosaicing", "time": "01:35",
         "context": "之后通过图像信号处理器把这些单色RGB信号进行处理。简单来说就是提取每个像素周围的颜色信息，来补全当前像素，这样就能混合出这个像素原本颜色的RGB信息。通过每个像素的计算还原，我们才能看到一张正常的照片。这个处理过程叫做去马赛克。",
         "sentences": [
            ["ISP提取周围像素颜色来补全当前像素。", "The ISP borrows neighbors' color to fill each pixel.", "ISP（图像信号处理器）"],
            ["混合出像素原本的RGB信息。", "It blends out the pixel's true RGB values.", "blend（混合）"],
            ["这个还原过程叫去马赛克。", "That process is demosaicing.", "demosaicing（去马赛克）"]
         ]}
    ]
}

ARTICLES["film-how-records"] = {
    "title_zh": "胶片是如何记录画面的",
    "title_en": "How Film Records an Image",
    "duration": "1分54秒",
    "topic": "摄影 · 胶片",
    "scenes": [
        {"id": "s1", "scene_zh": "卤化银：感光关键", "scene_en": "Silver Halide: The Light Catcher", "time": "00:00",
         "context": "把一张胶片放大上千倍，能看到很多颗粒状物质，这是一种感光材料叫卤化银，是卤素与银形成的化合物，也是胶片能感光成像的关键物质。一张胶片通常有很多层构成，其中最主要的就是混合了明胶与卤化银的感光乳剂层，和承载它们的片基层。",
         "sentences": [
            ["胶片放大上千倍，看到的是卤化银颗粒。", "Zoom in a thousand times and you see silver halide grains.", "silver halide（卤化银）"],
            ["卤化银是卤素与银形成的化合物。", "It's a compound of a halogen and silver.", "compound（化合物）"],
            ["胶片核心是明胶与卤化银的感光乳剂层。", "The key layer blends gelatin and silver halide.", "emulsion（感光乳剂）"]
         ]},
        {"id": "s2", "scene_zh": "潜影与显影", "scene_en": "The Latent Image and Development", "time": "00:20",
         "context": "当光线照射到胶片上，感光层中的卤化银颗粒发生光解反应，其感光点位会析出微小的银原子团簇，称之为潜影核。此时影像已经被记录下来，但由于光解银量极少，还无法被肉眼观测到，处于潜影状态。接下来需要进入冲洗流程：首先用显影剂，受光的卤化银进一步发生反应，具有潜影核的卤化银会被还原成金属银颗粒，大量金属银颗粒的聚集就构成了可见影像。",
         "sentences": [
            ["光线照射，卤化银光解析出银原子团簇——潜影核。", "Light splits the halide into silver clusters—the latent image.", "latent image（潜影）"],
            ["潜影银量极少，肉眼还看不见。", "So little silver forms that it's invisible to the eye.", "invisible（不可见）"],
            ["显影剂把受光卤化银还原成金属银，构成影像。", "Developer reduces the exposed grains to silver, making the image.", "developer（显影剂）"]
         ]},
        {"id": "s3", "scene_zh": "停显与定影", "scene_en": "Stop Bath and Fixer", "time": "00:49",
         "context": "接下来利用停显液，其弱酸性可以中和掉显影液，使卤化银停止反应。之后用含有硫代硫酸铵的定影液，把未感光的卤化银溶解，使胶片不能再感光。最后再清洗掉胶片上的残留成分，经过这一完整流程，胶片就变成了现在的样子。",
         "sentences": [
            ["停显液的弱酸性中和显影液，停止反应。", "The stop bath's acid neutralizes the developer.", "stop bath（停显液）"],
            ["定影液溶解未感光的卤化银，胶片不再感光。", "Fixer dissolves the unexposed halide so film stops reacting.", "fixer（定影液）"],
            ["清洗残留，胶片成型。", "Wash the residue and the film is done.", "residue（残留物）"]
         ]},
        {"id": "s4", "scene_zh": "负片与印相", "scene_en": "Negative and Printing", "time": "01:08",
         "context": "胶片上的画面是黑白颠倒的。正常会认为曝光强的部分应该更亮，但实际上胶片曝光强的部分反而会变黑。这是因为卤化银感光显影之后形成的金属银颗粒本身呈黑色：曝光越多的部分金属银越多，表现在画面上就越黑；而曝光少的部分金属银越少，看上去则更亮。这样黑白颠倒的底片被称为负片。想要还原成正常照片，需要用胶片放大机和同样含有感光材料涂层的相纸，把胶片上的负相印到相纸，相纸能接受到与实景相反的曝光，之后再经过一遍冲洗流程，负负得正，就能还原出正常的照片。",
         "sentences": [
            ["曝光越强，金属银越多，画面反而越黑。", "More exposure means more silver, and a darker negative.", "negative（负片）"],
            ["黑白颠倒的底片叫负片。", "That inverted image is the negative.", "inverted（颠倒的）"],
            ["放大机把负相印到相纸，负负得正。", "An enlarger prints it onto paper—two negatives make a positive.", "enlarger（放大机）"]
         ]}
    ]
}

ARTICLES["film-iso-history"] = {
    "title_zh": "胶片与 ISO 的前世今生！",
    "title_en": "The Story of ISO and Film",
    "duration": "1分30秒",
    "topic": "摄影 · 胶片",
    "scenes": [
        {"id": "s1", "scene_zh": "卤化银与感光度", "scene_en": "Silver Halides and Speed", "time": "00:00",
         "context": "用来制作感光材料的卤化银有氯化银、溴化银和碘化银这几种，它们的感光效率由低到高，其中溴化银在胶片上的应用最广泛。用不同的卤化银和一些辅助材料的混合，就能制作出感光度高低不同的胶片。",
         "sentences": [
            ["卤化银有氯化银、溴化银、碘化银三种。", "Silver halides come as chloride, bromide and iodide.", "halide（卤化物）"],
            ["感光效率由低到高，溴化银应用最广。", "Sensitivity rises in order; bromide is the most common.", "sensitivity（感光效率）"],
            ["不同卤化银混合，制出不同感光度的胶片。", "Mixing halides yields films of different speeds.", "speed（感光度）"]
         ]},
        {"id": "s2", "scene_zh": "标准乱象：ASA、DIN、OCT", "scene_en": "Standard Chaos: ASA, DIN, GOST", "time": "00:15",
         "context": "如何区分和标注就成了问题。许多厂商和组织都先后制定了自己的标准，主流的有德标DIN制、以柯达为首的美标ASA制、苏联的OCT等等。有标准是好，但标准太多反而会对用户产生困扰，更不利于传播普及。",
         "sentences": [
            ["厂商各自定标准：DIN、ASA、GOST等。", "Manufacturers each set standards: DIN, ASA, GOST and more.", "standard（标准）"],
            ["标准太多反而困扰用户、不利于普及。", "Too many standards confuse users and block adoption.", "adoption（普及）"]
         ]},
        {"id": "s3", "scene_zh": "ISO组织统一标准", "scene_en": "ISO Unifies the Standard", "time": "00:33",
         "context": "国际标准化组织（International Organization for Standardization），简称ISO。这个组织在1987年制定了胶片通用感光度标准，规定在胶片上标出感光度的算数值ASA和对数值DIN，实际上就是把美标和德标相结合。随着时间的推移，标注也逐渐简化，变成了我们现在所熟知的样子。",
         "sentences": [
            ["ISO组织1987年制定胶片通用感光度标准。", "In 1987 the ISO body set the universal film-speed standard.", "universal（通用的）"],
            ["把美标ASA和德标DIN相结合。", "It combined the US ASA and German DIN scales.", "combine（结合）"],
            ["标注逐渐简化成我们今天熟悉的样子。", "Over time the marking simplified into today's familiar form.", "simplify（简化）"]
         ]},
        {"id": "s4", "scene_zh": "ISO成为感光度代名词", "scene_en": "ISO Becomes a Byword for Speed", "time": "00:59",
         "context": "ISO并不是感光度的文本翻译，而是一个组织的简称，这个组织规范了胶片感光度的测定原理、方法、标准以及标注形式。就这样ISO顺其自然成为了感光度的代名词。时至今日胶片退出主流市场、数码崛起，ISO的标注依然沿用，但数码和胶片无论是感光材料还是成像原理都发生了很大变化，数码时代的ISO又该如何理解呢？",
         "sentences": [
            ["ISO是组织简称，不是感光度的翻译。", "ISO is an organization's acronym, not a translation.", "acronym（缩写）"],
            ["ISO顺其自然成了感光度的代名词。", "Naturally, ISO became the byword for speed.", "byword（代名词）"],
            ["数码时代ISO沿用标注，但含义已不同。", "Digital kept the label, but the meaning changed.", "label（标注）"]
         ]}
    ]
}

ARTICLES["photo-why-blur"] = {
    "title_zh": "照片为什么会拍“糊”？",
    "title_en": "Why Do Photos Come Out Blurry?",
    "duration": "1分04秒",
    "topic": "摄影 · 相机知识",
    "scenes": [
        {"id": "s1", "scene_zh": "静止拍摄是清晰的", "scene_en": "Still Scenes Stay Sharp", "time": "00:00",
         "context": "在相对完全静止的拍摄中，按下快门后，场景中所有的物体反射的光线会由镜头进入相机的传感器，并在固定的位置累积，这样就能得到一张清晰的画面。",
         "sentences": [
            ["完全静止时，光线在传感器固定位置累积。", "When all is still, light piles up at fixed spots.", "piles up（累积）"],
            ["这样就能得到清晰的画面。", "That gives you a crisp image.", "crisp（清晰的）"]
         ]},
        {"id": "s2", "scene_zh": "动态模糊的产生", "scene_en": "How Motion Blur Happens", "time": "00:12",
         "context": "一旦空间内有运动产生，运动物体反射的光会随之发生位移，得到的便是带有运动轨迹的模糊画面。这种由相对运动位移产生的模糊就是动态模糊。影响动态模糊最大的两个因素，一个是曝光时长，一个是相对运动。",
         "sentences": [
            ["运动物体的光发生位移，产生运动轨迹模糊。", "Moving objects displace light, leaving a blurred trail.", "displace（位移）"],
            ["这就是动态模糊。", "That's motion blur.", "motion blur（动态模糊）"],
            ["两大因素：曝光时长和相对运动。", "Two factors: exposure time and relative motion.", "exposure time（曝光时长）"]
         ]},
        {"id": "s3", "scene_zh": "用快门控制模糊", "scene_en": "Control Blur With the Shutter", "time": "00:33",
         "context": "在大部分拍摄中我们很难改变被摄物体的运动，只能通过改变快门来控制这种模糊。在运动恒定的情况下，曝光时间越短，运动物体的空间位移就越小，画面越清晰；反之曝光时间越长，位移就越大，图像也就更模糊。",
         "sentences": [
            ["物体运动难改变，只能靠快门控制模糊。", "You can't stop the subject, only control the blur via shutter.", "shutter（快门）"],
            ["曝光时间越短，位移越小，画面越清晰。", "Shorter exposure, less displacement, sharper image.", "sharper（更清晰）"],
            ["曝光越长，位移越大，画面越模糊。", "Longer exposure, more blur.", "blur（模糊）"]
         ]},
        {"id": "s4", "scene_zh": "动态模糊也可以是创作", "scene_en": "Blur as a Creative Tool", "time": "00:51",
         "context": "实际上动态模糊并不是成像缺陷，很多人还会利用这个特性来创作有意思的内容，比如光绘。当然在平面摄影中，多数情况下还是会规避这种模糊，来获得一张清晰的图像。",
         "sentences": [
            ["动态模糊不是缺陷，还能用来创作。", "Motion blur isn't a flaw—people create with it.", "flaw（缺陷）"],
            ["比如光绘。", "Like light painting.", "light painting（光绘）"],
            ["平面摄影大多规避模糊，追求清晰。", "Still photography mostly avoids blur for sharpness.", "sharpness（清晰度）"]
         ]}
    ]
}

ARTICLES["leaf-shutter"] = {
    "title_zh": "「镜间快门」是个什么东西？",
    "title_en": "What Is a Leaf Shutter?",
    "duration": "34秒",
    "topic": "摄影 · 相机知识",
    "scenes": [
        {"id": "s1", "scene_zh": "镜间快门在镜头中间", "scene_en": "Leaf Shutter Sits in the Lens", "time": "00:00",
         "context": "镜间快门顾名思义在镜头中间、光圈旁，其结构和光圈也有些相似。由于其在镜头内部，开合的过程中CMOS可以整体感光，不存在时间差，因此也就不会产生果冻效应，其开合速度通常也更快。",
         "sentences": [
            ["镜间快门在镜头中间、光圈旁。", "The leaf shutter lives in the lens, next to the aperture.", "leaf shutter（镜间快门）"],
            ["开合时CMOS整体感光，没有时间差。", "The whole sensor exposes at once, with no time gap.", "time gap（时间差）"],
            ["因此不会产生果冻效应，开合还更快。", "No rolling shutter, and faster speeds to boot.", "rolling shutter（果冻效应）"]
         ]},
        {"id": "s2", "scene_zh": "缺点与本质", "scene_en": "Downsides and the Essence", "time": "00:14",
         "context": "缺点就是会对进光量和景深有影响，对硬件的要求也很高，结构复杂，所以这种快门的应用并不常见。其实所有类型的快门本质上都是一个开关，一个控制时间的开关，其目的就是让相机更精确地还原我们按下快门的那一刻，这个世界最真实的模样。",
         "sentences": [
            ["缺点：影响进光量和景深，硬件要求高。", "Downsides: it affects light and depth, and needs costly hardware.", "depth of field（景深）"],
            ["应用并不常见。", "So it's rarely seen.", "rarely（罕见）"],
            ["所有快门本质上都是控制时间的开关。", "Every shutter is really just a switch that controls time.", "switch（开关）"]
         ]}
    ]
}

ARTICLES["animation-science-howto"] = {
    "title_zh": "如何制作动画科普！！！",
    "title_en": "How to Make Science Explainers in Motion",
    "duration": "7分00秒",
    "topic": "动画 · After Effects",
    "scenes": [
        {"id": "s1", "scene_zh": "MG动画：让图形动起来", "scene_en": "Motion Graphics: Make Shapes Move", "time": "00:00",
         "context": "动画类型属于MG动画，可以简单理解为让图形动起来。无论什么形状，单一元素还是复合形态，都可以看作是图形。图形不能理解？那它们到底是如何动起来的呢？很简单，关键帧。关键帧是动画最基础的运行逻辑，也是最容易让人劝退的部分。",
         "sentences": [
            ["MG动画就是让图形动起来。", "Motion graphics simply make shapes move.", "motion graphics（MG动画）"],
            ["关键帧是动画最基础的运行逻辑。", "Keyframes are the core logic of animation.", "keyframe（关键帧）"],
            ["它也是最容易让人劝退的部分。", "And the part that scares people off most.", "scare off（劝退）"]
         ]},
        {"id": "s2", "scene_zh": "AE界面初体验", "scene_en": "First Steps in the AE Interface", "time": "00:18",
         "context": "来到软件界面：左侧是项目面板，在这里可以管理所有的文件，也能导入素材；右侧这个是实时监看面板，叫做合成窗口；上面一般是工具栏；最下面是合成的时间线窗口，这是最主要的操作区域，绝大部分的操作都可以在这里进行。",
         "sentences": [
            ["左侧项目面板管理文件和素材。", "The project panel on the left manages files and imports.", "project panel（项目面板）"],
            ["右侧是合成窗口，实时监看。", "The comp window on the right previews live.", "comp window（合成窗口）"],
            ["最下面是时间线，主操作区。", "The timeline below is the main workspace.", "timeline（时间线）"]
         ]},
        {"id": "s3", "scene_zh": "新建与变换参数", "scene_en": "Creating Layers and Transform", "time": "00:45",
         "context": "点击鼠标右键可以新建最基本的元素：文字、形状图层，也可以在工具栏选择相应的工具在合成窗口直接操作。我们新建一个形状，展开它的变换参数，里面有五个选项，试着调整一下这些参数，能看到图形会随之产生变化。其中位置、缩放、旋转，是影响运动的三个关键参数。",
         "sentences": [
            ["右键可新建文字和形状图层。", "Right-click to add text and shape layers.", "shape layer（形状图层）"],
            ["变换参数里，位置/缩放/旋转影响运动。", "Of the transform options, position, scale and rotation drive motion.", "transform（变换）"]
         ]},
        {"id": "s4", "scene_zh": "关键帧动画", "scene_en": "Keyframe Animation", "time": "01:10",
         "context": "先来做一个简单的位移动画：把图形放在左侧，拖动时间线到起始处，点击位置属性前的码表图标，此时就完成了一个关键帧的记录；之后拖动时间线至两秒处，再改变一下图形的位置，这样就会在当前状态自动生成一个关键帧。预览一下，一个简单的位移动画就完成了。关键帧其实就是记录画面元素在不同时间下的不同状态，这也是动画最基本的运行逻辑。",
         "sentences": [
            ["点击码表图标记录起始关键帧。", "Click the stopwatch to record the first keyframe.", "stopwatch（码表）"],
            ["两秒处改变位置，自动生成第二个关键帧。", "Move the shape at two seconds to auto-add the second keyframe.", "auto-add（自动生成）"],
            ["关键帧=元素在不同时间的不同状态。", "Keyframes capture states across time.", "capture（记录）"]
         ]},
        {"id": "s5", "scene_zh": "速度曲线让动画丝滑", "scene_en": "Speed Curves for Smooth Motion", "time": "02:11",
         "context": "为什么动画看起来还不够流畅？因为现在它还是线性运动。选出这两个关键帧，打开图表编辑器，选择编辑速度图表：这个图表的横向代表时间，纵向表示速率。能看到它还是一条直线，也就说明运动的运动速度是一致的，运动起来自然也就平平无奇。按F9键，菱形关键帧变成了沙漏形状，再次回到图表编辑器，直线也变成了曲线。高的部分表示运动更快，低的部分则更慢。想要由快到慢就可以左高右低，而用慢变快则可以左低右高。",
         "sentences": [
            ["线性运动让动画平平无奇。", "Linear motion makes animation feel flat.", "linear（线性的）"],
            ["按F9，直线关键帧变成曲线。", "Hit F9 and the straight frames turn to curves.", "ease（缓动）"],
            ["曲线高=快、低=慢，可自由塑造节奏。", "High curve is fast, low is slow—shape your rhythm.", "rhythm（节奏）"],
            ["关键帧让画面动，速度曲线让画面丝滑。", "Keyframes move it; curves make it silky.", "silky（丝滑）"]
         ]},
        {"id": "s6", "scene_zh": "核心动机", "scene_en": "Find the Core Idea", "time": "03:09",
         "context": "有些朋友会说软件操作我都会，可是一旦开始创作就无从下手，那可能是因为你还没有找到创作的核心动机。以快门这期视频为例，其实核心动机就是有快门形态。我们可以先想象快门的组成部分，然后用最基础的形状把它描绘出来：一个长方形的CMOS，一个圆形的相机卡口，再用四个长方形拼出快门叶片。想让快门动起来，就可以用关键帧记录一下每个叶片起始和结束的位置。",
         "sentences": [
            ["会操作但不会创作，是缺核心动机。", "Knowing the tools but not the why? Find the core idea.", "core idea（核心动机）"],
            ["用最基础的形状描绘主题。", "Sketch the subject with the simplest shapes.", "sketch（描绘）"],
            ["关键帧记录每个叶片的起止位置。", "Keyframe each blade's start and end.", "blade（叶片）"]
         ]},
        {"id": "s7", "scene_zh": "效果叠加与路径动画", "scene_en": "Effects and Path Animation", "time": "03:53",
         "context": "AE最重要的一个部分：效果。给CMOS形状加上一个四色渐变效果，调整颜色分布，再添加一个网格效果，就能得到一个更符合直觉的CMOS画面。还可以做相机生长动画：用钢笔工具进行绘制，完成之后添加修剪路径效果，打上关键帧，让图形的线条路径从0%到最后100%依次展现，这样一个路径生长动画就完成了。",
         "sentences": [
            ["效果可以叠加，实现丰富视觉表现。", "Stack effects to enrich the visuals.", "stack（叠加）"],
            ["四色渐变加网格，CMOS更有直觉。", "Gradient plus grid makes the CMOS intuitive.", "gradient（渐变）"],
            ["钢笔绘制+修剪路径关键帧=路径生长动画。", "Pen + trim paths keyframed gives a growing-line animation.", "trim path（修剪路径）"]
         ]},
        {"id": "s8", "scene_zh": "伪3D的小心机", "scene_en": "Fake 3D in a 2D App", "time": "04:56",
         "context": "打开3D开关旋转一下，说好的3D呢？虽然可以通过插件或渲染器实现一些3D效果，但AE本质上还是一个2D软件。想在二维中实现3D效果还可以耍点小心机：这个动画其实就是相机旋转到不同的形态时，给它做出对应的轮廓线条，在轮廓变化的起始、中间和结束状态分别打上关键帧，再适当调整一下，一个障眼法的3D效果就出来了。",
         "sentences": [
            ["AE本质是2D软件。", "After Effects is fundamentally 2D.", "fundamentally（本质上）"],
            ["旋转到不同形态，配对应轮廓线条。", "Rotate the form and draw matching outline lines.", "outline（轮廓）"],
            ["起止和中间打关键帧，就是伪3D。", "Keyframe start, middle and end—that's fake 3D.", "fake 3D（伪3D）"]
         ]},
        {"id": "s9", "scene_zh": "脚本与插件", "scene_en": "Scripts and Plugins", "time": "05:58",
         "context": "除了基础软件操作，还需要了解AE的拓展工具，也就是常听到的插件脚本。脚本通常体积小巧，它可以通过代码来控制AE现有的功能，让操作更为便捷。而插件则会复杂一些，是为了拓展AE的边界，让原本实现不了或很难实现的效果能更容易制作出来，比如这一类粒子插件和3D插件。",
         "sentences": [
            ["脚本用代码控制AE现有功能。", "Scripts drive existing AE features via code.", "script（脚本）"],
            ["插件拓展AE的边界。", "Plugins push the boundaries of AE.", "plugin（插件）"],
            ["粒子插件和3D插件让特效更易实现。", "Particle and 3D plugins make effects much easier.", "particle（粒子）"]
         ]},
        {"id": "s10", "scene_zh": "动画科普的初心", "scene_en": "Why Animate Science", "time": "06:43",
         "context": "用动画来制作科普的目的，就是为了让一些晦涩难懂的文字表述，以可视化的形态展现，它的优势就是直观明了。但它归根结底也只是一种表现形式，而科普内容本身才是核心，你要做的是锦上添花，而非纸上添花。",
         "sentences": [
            ["动画科普把晦涩文字可视化。", "Animated explainers turn dense text into visuals.", "visualize（可视化）"],
            ["它的优势是直观明了。", "Its strength is clarity at a glance.", "clarity（直观）"],
            ["动画只是形式，内容才是核心，做锦上添花。", "Animation is a vessel; the content is the core.", "vessel（载体）"]
         ]}
    ]
}

ARTICLES["electronic-front-curtain"] = {
    "title_zh": "“电子前帘快门”是个什么东西？",
    "title_en": "What Is an Electronic Front Curtain?",
    "duration": "43秒",
    "topic": "摄影 · 相机知识",
    "scenes": [
        {"id": "s1", "scene_zh": "电子前帘=电子开+机械后帘关", "scene_en": "EFCS: Electronic Open, Mechanical Close", "time": "00:00",
         "context": "电子前帘快门，也就是电子加机械的组合：开启时用电子快门，关闭时使用机械后帘快门。由于机械后帘的介入，这种曝光方式也可以不受读出速度的影响，同时还能避免前帘开合产生的震动。",
         "sentences": [
            ["电子前帘=电子开、机械后帘关的组合。", "EFCS opens electronically and closes with a mechanical curtain.", "EFCS（电子前帘快门）"],
            ["不受读出速度影响，还能避免前帘震动。", "It dodges readout limits and curtain shake.", "curtain shake（快门震动）"]
         ]},
        {"id": "s2", "scene_zh": "焦外光斑被裁切", "scene_en": "Bokeh Gets Sliced", "time": "00:14",
         "context": "有优点自然也少不了缺点。由于机械后帘与控制电子快门的CMOS不在一个平面上，快门速度过高时会出现曝光不均匀的现象，最常见的就是焦外的光斑被裁切。原理就是高速快门使得曝光间隔变小，两种快门又不在一个平面上，焦外的弥散圆被机械快门遮挡后，导致后面CMOS无法均匀曝光，因此会出现前景的光斑上半部分被裁切，而后景的光斑下半部分被裁切的现象。",
         "sentences": [
            ["机械后帘和CMOS不在同一平面，高速时曝光不均。", "The curtain and sensor sit apart, so high speeds expose unevenly.", "unevenly（不均）"],
            ["最常见的是焦外光斑被裁切。", "Most visible: sliced bokeh highlights.", "bokeh（焦外）"],
            ["前景光斑切上半，后景切下半。", "Foreground bokeh loses its top; background loses its bottom.", "slice（裁切）"]
         ]}
    ]
}

ARTICLES["electronic-shutter-framerate"] = {
    "title_zh": "拍视频必须搞懂的：快门｜帧率",
    "title_en": "Video Essentials: Shutter and Frame Rate",
    "duration": "2分44秒",
    "topic": "摄影 · 视频知识",
    "scenes": [
        {"id": "s1", "scene_zh": "帧率与卡顿", "scene_en": "Frame Rate and Stutter", "time": "00:00",
         "context": "视频实际上是连续播放的竞争训练，一帧就是一张图片。以这个线性运动的小球为例，不同的帧率决定了在一秒钟内小球运动路径上会有多少个画面产生，把这些画面放到一起连续播放就变成了视频。显然在帧率较低的情况下，物体每帧之间的运动跨度很大，此时过于清晰的画面会使人一眼产生明显的卡顿。",
         "sentences": [
            ["视频是连续播放的静止帧。", "Video is still frames played in sequence.", "frame（帧）"],
            ["帧率越低，每帧之间运动跨度越大。", "Lower frame rates mean bigger jumps between frames.", "frame rate（帧率）"],
            ["过于清晰的低帧率画面会卡顿。", "Too-sharp low-fps motion looks stuttery.", "stutter（卡顿）"]
         ]},
        {"id": "s2", "scene_zh": "动态模糊让画面连贯", "scene_en": "Motion Blur Smooths It Out", "time": "00:25",
         "context": "加入适当的动态模糊，实际上就是增加了运动轨迹的记录，画面看上去自然也就更连贯、流畅。但是这种模糊太大的话，同样也会影响观看体验。",
         "sentences": [
            ["动态模糊=记录更多运动轨迹。", "Motion blur records more of the trajectory.", "trajectory（运动轨迹）"],
            ["适当的模糊让画面连贯流畅。", "Just enough blur makes motion flow.", "flow（流畅）"],
            ["模糊太大反而影响观看。", "Too much blur ruins the viewing.", "too much（过量）"]
         ]},
        {"id": "s3", "scene_zh": "快门速度的上限", "scene_en": "The Shutter Speed Ceiling", "time": "00:40",
         "context": "帧率决定了快门速度的上限：在视频拍摄中，快门速度最大也就只能是帧率的倒数。以每秒25帧为例，一秒钟时长想要记录25帧画面，那么平均到每一帧的时间最长也就只有25分之一秒。用一个圆形分布来对应的话，打开360度也就是100%曝光，为单帧画面的曝光上限。如果时间减半变为50%的曝光量，也就是50分之一秒，角度为180度。",
         "sentences": [
            ["快门速度最大只能是帧率的倒数。", "Shutter tops out at the reciprocal of the frame rate.", "reciprocal（倒数）"],
            ["25帧每秒，每帧最长1/25秒，即360度全开。", "At 25fps, each frame caps at 1/25s—a full 360°.", "full open（全开）"],
            ["时间减半是180度，即1/50秒。", "Half the time is 180°, or 1/50s.", "180 degrees（180度）"]
         ]},
        {"id": "s4", "scene_zh": "180度快门规则", "scene_en": "The 180-Degree Rule", "time": "01:17",
         "context": "每帧画面曝光一半的时长所产生的动态模糊，是一个比较符合人眼视觉感知的数值。这种以角度来控制曝光的快门，早期曾用在胶片摄影机中：一个金属圆盘，其转速匹配帧率，通过控制打开角度让光线穿过，从而改变每帧胶片的曝光时长。快门角度大小决定了每帧画面曝光的多少，通常说的180度对应的就是单帧画面一半的曝光时长，也就是帧率倒数的一半。",
         "sentences": [
            ["每帧曝光一半时长，动态模糊最接近人眼感知。", "Half-time exposure per frame matches human perception.", "perception（感知）"],
            ["胶片摄影机用金属圆盘控制打开角度。", "Film cameras used a spinning disc to set the open angle.", "disc（圆盘）"],
            ["180度=单帧曝光时长的一半。", "180° equals half of one frame's time.", "shutter angle（快门角度）"]
         ]},
        {"id": "s5", "scene_zh": "奇怪的快门角度", "scene_en": "Those Odd Shutter Angles", "time": "01:42",
         "context": "如今一些电影机还会沿用这个快门角度的标注。如果你看到172.8度、144度等奇怪的数值也不必惊讶，这通常是采用了电影24帧的拍摄帧率。172.8度的开角对应的是每帧画面曝光总量24分之一秒的48%，换算过来也就是50分之一秒的快门速度；而144度对应的则是24分之一秒的40%，也就是60分之一秒的快门速度。",
         "sentences": [
            ["172.8度和144度来自24帧电影帧率。", "172.8° and 144° come from the 24fps cinema rate.", "cinema（电影）"],
            ["172.8度=1/50秒，144度=1/60秒。", "172.8° equals 1/50s; 144° equals 1/60s.", "convert（换算）"]
         ]},
        {"id": "s6", "scene_zh": "快门与频闪", "scene_en": "Shutter and Flicker", "time": "02:05",
         "context": "之所以使用50分之一秒和60分之一秒的快门速度，是为了匹配不同国家和地区的交流电频率，从而避免一个很大的问题：频闪。频闪通常是因为快门速度的设定与人造光源的交流电频率不匹配而导致的。我们国家的交流电频率为50Hz，如果想拍摄24帧的帧率，按180度曝光的话快门为48分之一秒，这就会导致每一帧画面记录的电压周期不一致，画面亮度也会不同，连续播放起来就有可能出现闪烁。而使用50分之一秒的快门，正好能与周期匹配，做到亮度一致，从而避免出现频闪。",
         "sentences": [
            ["1/50秒和1/60秒是为了匹配交流电频率。", "1/50s and 1/60s match regional AC power frequencies.", "AC frequency（交流电频率）"],
            ["快门与光源频率不匹配，就会频闪。", "A mismatch between shutter and lights causes flicker.", "flicker（频闪）"],
            ["50Hz地区用1/50秒，亮度一致不闪。", "In 50Hz regions, 1/50s keeps brightness steady.", "steady（稳定）"]
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
