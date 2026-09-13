#!/bin/bash
# b57 Whisper：短视频并行，长视频串行
cd /Users/chenzhiheng/Projects/video-notes
PY=/opt/homebrew/Cellar/yt-dlp/2026.7.4/libexec/bin/python
SHORT=(b57a b57b b57c b57d b57e)
LONG=(b57i b57g b57h b57f)  # 约 9→12→13→19 分钟，由短到长

run_one() {
  local k="$1"
  if [ -f "$k.json" ] && [ -s "$k.json" ]; then
    echo "$(date +%H:%M) $k 已转录"
    echo "完成 $k"
    return
  fi
  echo "$(date +%H:%M) 转录 $k ..."
  $PY -m whisper "$k.m4a" --model medium --language Chinese --output_dir . > "/tmp/w_$k.log" 2>&1
  echo "$(date +%H:%M) 完成 $k"
}

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

for k in "${LONG[@]}"; do
  run_one "$k"
done
echo "全部转录结束"
