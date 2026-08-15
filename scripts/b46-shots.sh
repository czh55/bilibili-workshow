#!/bin/bash
# b46 批量抽高清截图：slug|视频键|时间点列表
cd /Users/chenzhiheng/Projects/bilibili-workshop
FF=/opt/homebrew/bin/ffmpeg
S=(
  "latte-3-moves|f01|10 40 85 130 170 240 300 370"
  "latte-correction-share|f02|3 12 22 30 40 50 62"
  "round-face-makeup|f03|6 15 35 60 90 115 145 220 290"
  "ai-talking-edit|f04|8 45 60 90 150 200 250 300 360"
  "documentary-color-tone|f05|8 50 100 135 170 200 240 300 335"
  "latte-big-heart|f06|10 30 50 70 120 160 200 270"
  "round-face-adjust|f07|3 10 16 24 32 37"
  "rgb-curve-basics|f08|12 25 40 55 75 95 130 160 200 240"
  "skirt-photo-poses|f09|4 25 35 55 70 90 110 145"
  "ai-love-shortfilm|f10|6 20 35 60 90 120 150 180 210"
  "couple-quarrel|f11|3 10 20 30 38 42"
  "promotion-interview|f12|6 25 40 60 90 120 150 180"
  "inner-drain-reason|f13|4 12 20 30 42 52"
  "new-leader-team|f14|8 25 40 55 75 95 120 160 210 270 310"
)
for item in "${S[@]}"; do
  slug="${item%%|*}"; rest="${item#*|}"; k="${rest%%|*}"; times="${rest#*|}"
  mkdir -p "docs/assets/$slug"
  n=1
  for t in $times; do
    out="docs/assets/$slug/shot-$(printf '%02d' $n).jpg"
    $FF -y -v error -ss "$t" -i "$k.source.mp4" -frames:v 1 -vf "scale='min(1280,iw)':-2" -q:v 2 "$out" 2>/dev/null
    n=$((n+1))
  done
  echo "$slug: $((n-1)) 张截图"
done
echo "全部截图完成"
