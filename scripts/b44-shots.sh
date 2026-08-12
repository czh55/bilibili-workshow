#!/bin/bash
# b44 提取关键截图：slug -> 视频键|时间点列表
cd /Users/chenzhiheng/Projects/bilibili-workshop
FF=/opt/homebrew/bin/ffmpeg
SLUGS=(no-many-clothes wulingshan-aranya easy-pose-simple urban-village-answer one-house-vs-zijian)
VALS=(
  "d01|10 16 28 44 56 72 86 100 128 148"
  "d02|8 24 36 48 64 76 85 100 112 130 144 200 260"
  "d03|12 26 40 55 66 84 92 100"
  "d04|4 48 69 115 137 150 180 219 239 260"
  "d05|18 32 47 59 75 82 87 110"
)
for i in "${!SLUGS[@]}"; do
  s="${SLUGS[$i]}"; val="${VALS[$i]}"
  k="${val%%|*}"; times="${val#*|}"
  mkdir -p "docs/assets/$s"
  n=1
  for t in $times; do
    out="docs/assets/$s/shot-$(printf '%02d' $n).jpg"
    $FF -y -v error -ss "$t" -i "$k.source.mp4" -frames:v 1 -vf "scale='min(1280,iw)':-2" -q:v 2 "$out" 2>/dev/null
    n=$((n+1))
  done
  echo "$s: $(ls docs/assets/$s | wc -l | tr -d ' ') 截图"
done