#!/bin/bash
# 批量抽帧（纯 bash）：从 v0X.source.mp4 抽取候选帧到 _work/{k}/
cd /Users/chenzhiheng/Projects/bilibili-workshop
mkdir -p _work
KEYS=(v03 v04 v05 v06 v07 v08 v09 v10 v11 v12 v14 v15)
TIMES=(
  "0 4 8 12 16 20"
  "0 5 10 15 20 25 30 35 40"
  "5 15 25 35 45 55 65 75 85"
  "5 15 30 50 70 90 110 130 150 170"
  "3 10 20 30 40 50 60 70 80"
  "3 8 13 18 23 28 33 38 43"
  "5 15 30 45 60 75 90 105"
  "0 5 10 15 20 25 30"
  "0 4 8 12 16 20 24 28"
  "3 8 13 18 23 28 33 38 43 48"
  "5 20 40 60 80 100 120 140 160 180 200"
  "0 3 6 9 12 15"
)
for i in "${!KEYS[@]}"; do
  k="${KEYS[$i]}"
  mkdir -p "_work/$k"
  for t in ${TIMES[$i]}; do
    out="_work/$k/f-$t.jpg"
    [ -f "$out" ] || ffmpeg -y -v error -ss "$t" -i "$k.source.mp4" -frames:v 1 -q:v 3 "$out" 2>/dev/null
  done
  echo "$k: $(ls _work/$k 2>/dev/null | wc -l) 帧"
done
