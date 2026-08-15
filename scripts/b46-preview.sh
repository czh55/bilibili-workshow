#!/bin/bash
# b46 预览抽帧：对每个视频每 N 秒抽一帧低分辨率，供图像审阅选图
cd /Users/chenzhiheng/Projects/bilibili-workshop
FF=/opt/homebrew/bin/ffmpeg
mkdir -p _work/b46-preview
# key|间隔秒
PAIRS=(
  "f01|15"
  "f02|5"
  "f03|15"
  "f04|15"
  "f05|15"
  "f06|15"
  "f07|4"
  "f08|10"
  "f09|8"
  "f10|10"
  "f11|4"
  "f12|8"
  "f13|5"
  "f14|15"
)
for pair in "${PAIRS[@]}"; do
  k="${pair%%|*}"; step="${pair#*|}"
  dur=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$k.source.mp4")
  n=0
  for (( t=0; t<${dur%.*}; t+=step )); do
    out="_work/b46-preview/${k}_$(printf '%03d' $t).jpg"
    $FF -y -v error -ss "$t" -i "$k.source.mp4" -frames:v 1 -vf "scale=320:-2" -q:v 5 "$out" 2>/dev/null
    n=$((n+1))
  done
  echo "$k: $n 帧"
done
echo "预览完成"
