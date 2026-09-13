#!/bin/bash
# b57 抽帧：按时长均匀取 5 张（长视频 8 张）
cd /Users/chenzhiheng/Projects/bilibili-workshop
# key slug times(seconds space-separated)
declare -a ROWS=(
  "b57a|host-pop-professional-feel|20 55 95 140 190"
  "b57b|host-speak-visual-sense|10 30 50 70 95"
  "b57c|host-express-day3-ai|15 40 70 105 140"
  "b57d|host-express-day2-logic|15 40 70 105 140"
  "b57e|host-express-system-intro|10 25 40 55 75"
  "b57f|pour-over-fundamentals|60 180 360 540 720 900 1020 1100"
  "b57g|espresso-machine-grind-dial|40 120 240 360 480 600 700"
  "b57h|homemade-americano-guide|40 120 240 400 560 700"
  "b57i|homemade-instant-coffee|30 100 200 320 450 520"
)
for row in "${ROWS[@]}"; do
  IFS='|' read -r k s times <<< "$row"
  mkdir -p "docs/assets/$s"
  n=1
  for t in $times; do
    out="docs/assets/$s/shot-$(printf '%02d' $n).jpg"
    if [ ! -f "$out" ]; then
      ffmpeg -y -v error -ss "$t" -i "$k.source.mp4" -frames:v 1 -vf "scale='min(1280,iw)':-2" -q:v 2 "$out" 2>/dev/null || true
    fi
    n=$((n+1))
  done
  echo "$k -> $s: $(ls docs/assets/$s/shot-*.jpg 2>/dev/null | wc -l | tr -d ' ') shots"
done
echo "全部抽帧结束"
