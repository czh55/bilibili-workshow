#!/bin/bash
# b49 转录：串行跑 24 个视频
cd /Users/chenzhiheng/Projects/bilibili-workshop
KEYS=(c01 c02 c03 c04 c05 c06 c07 c08 c09 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24)
for k in "${KEYS[@]}"; do
  if [ -f "$k.json" ]; then
    echo "=== $k 已转录，跳过 ==="
    continue
  fi
  if [ ! -f "$k.m4a" ]; then
    echo "=== $k 无音频，跳过 ==="
    continue
  fi
  dur=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $k.m4a 2>/dev/null)
  echo "=== 转录 $k (${dur}s) ==="
  python3 -m whisper "$k.m4a" --model medium --language Chinese --output_dir . 2>&1 | tail -2
  echo "=== $k 完成 ==="
done
echo "全部转录结束"
