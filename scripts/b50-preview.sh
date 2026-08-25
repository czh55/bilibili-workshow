#!/bin/bash
# b50 预览抽帧：对每个视频每 N 秒抽一帧低分辨率，供图像审阅选图
cd /Users/chenzhiheng/Projects/bilibili-workshop
FF=/opt/homebrew/bin/ffmpeg
mkdir -p _work/b50-preview
# key|间隔秒
PAIRS=(
  "d01|20"
  "d02|10"
  "d03|15"
  "d04|15"
  "d05|20"
  "d06|10"
  "d07|15"
  "d08|8"
  "d09|8"
  "d10|10"
  "d11|2"
  "d12|2"
  "d13|3"
  "d14|4"
)
for pair in "${PAIRS[@]}"; do
  k="${pair%%|*}"; step="${pair#*|}"
  dur=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$k.source.mp4")
  n=0
  for (( t=0; t<${dur%.*}; t+=step )); do
    out="_work/b50-preview/${k}_$(printf '%03d' $t).jpg"
    $FF -y -v error -ss "$t" -i "$k.source.mp4" -frames:v 1 -vf "scale=320:-2" -q:v 5 "$out" 2>/dev/null
    n=$((n+1))
  done
  echo "$k: $n 帧"
done
echo "预览完成"
