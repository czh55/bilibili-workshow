#!/bin/bash
# b48 转录：串行跑 11 个视频（v09 已存在跳过）
cd /Users/chenzhiheng/Projects/bilibili-workshop
KEYS=(v01 v02 v03 v04 v05 v06 v07 v08 v10 v11 v12)
for k in "${KEYS[@]}"; do
  if [ -f "$k.json" ]; then
    echo "=== $k 已转录，跳过 ==="
    continue
  fi
  echo "=== 转录 $k ($(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $k.m4a 2>/dev/null)s) ==="
  python3 -m whisper "$k.m4a" --model medium --language Chinese --output_dir . 2>&1 | tail -3
  echo "=== $k 完成 ==="
done
echo "全部转录结束"
