#!/bin/bash
# 批量创建正式截图 docs/assets/{slug}/shot-XX.jpg（纯 bash）
cd /Users/chenzhiheng/Projects/bilibili-workshop
KEYS=(v04 v05 v06 v07 v08 v09 v10 v11 v12 v14 v15)
SLUGS=(lingdong-move-tutorial yaqi-lighting-trick outdoor-light-control light-distance-guide restaurant-toplight-fix home-lighting-gap sofa-portrait petite-longleg-poses summer-skirt-slim photo-course-14 beach-pose-machine)
TIMES=(
  "2 8 14 20 26 32 38"
  "5 20 40 55 70 85"
  "5 30 60 90 120 150 175"
  "5 20 40 60 75"
  "5 15 25 35 45"
  "10 30 55 80 105"
  "2 8 15 22 30"
  "2 8 14 20 26"
  "5 15 25 35 45"
  "10 40 80 120 160 200"
  "2 6 10 14"
)
for i in "${!KEYS[@]}"; do
  k="${KEYS[$i]}"; s="${SLUGS[$i]}"
  mkdir -p "docs/assets/$s"
  n=1
  for t in ${TIMES[$i]}; do
    out="docs/assets/$s/shot-$(printf '%02d' $n).jpg"
    [ -f "$out" ] || ffmpeg -y -v error -ss "$t" -i "$k.source.mp4" -frames:v 1 -vf "scale='min(1280,iw)':-2" -q:v 2 "$out" 2>/dev/null
    n=$((n+1))
  done
  echo "$k -> $s: $(ls docs/assets/$s 2>/dev/null | wc -l) 截图"
done
