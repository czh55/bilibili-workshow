#!/bin/bash
# 批量 Whisper 转录：短视频 3 路并行，长视频随后串行
# 用法: bash scripts/xhs-transcribe.sh
cd /Users/chenzhiheng/Projects/bilibili-workshop
PY=/opt/homebrew/Cellar/yt-dlp/2026.7.4/libexec/bin/python
SHORT=(v03 v04 v05 v06 v07 v08 v09 v10 v11 v12 v14 v15)
LONG=(v01 v02 v13)

run_one() {
  local k="$1"
  if [ -f "$k.json" ]; then echo "$(date +%H:%M) $k 已转录"; return; fi
  echo "$(date +%H:%M) 转录 $k ..."
  $PY -m whisper "$k.m4a" --model medium --language Chinese --output_dir . > "/tmp/w_$k.log" 2>&1
  echo "$(date +%H:%M) 完成 $k"
}

# 短视频 3 路并行
BATCH=3
i=0
PIDS=()
for k in "${SHORT[@]}"; do
  run_one "$k" &
  PIDS+=($!)
  i=$((i+1))
  if [ $i -ge $BATCH ]; then
    for p in "${PIDS[@]}"; do wait "$p"; done
    i=0
    PIDS=()
  fi
done
for p in "${PIDS[@]}"; do wait "$p"; done

# 长视频串行
for k in "${LONG[@]}"; do
  if [ -f "$k.json" ]; then echo "$k 已转录"; continue; fi
  echo "$(date +%H:%M) 长视频转录 $k ..."
  $PY -m whisper "$k.m4a" --model medium --language Chinese --output_dir . > "/tmp/w_$k.log" 2>&1
  echo "$(date +%H:%M) 完成 $k"
done
echo "全部转录结束"
