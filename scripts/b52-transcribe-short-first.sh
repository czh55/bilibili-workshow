#!/bin/bash
# b52 并行转录：按音频时长升序处理，避免长视频阻塞短视频
# 可与 b52-auto-process.sh / b52-download.sh 并存；已有 .json 则跳过
cd /Users/chenzhiheng/Projects/video-notes

FFMPEG=$(command -v ffmpeg)
[ -z "$FFMPEG" ] && FFMPEG=/opt/homebrew/bin/ffmpeg
LOCKDIR=_work/b52-logs/whisper-locks
mkdir -p "$LOCKDIR"

# 抽出尚未转录的音频
while true; do
  # 兜底抽音频
  for n in $(seq 1 106); do
    k=$(printf 'h%02d' "$n")
    src=$(ls "$k".source.* 2>/dev/null | head -1)
    if [ -n "$src" ] && [ ! -f "$k.m4a" ]; then
      "$FFMPEG" -y -i "$src" -vn -acodec aac -b:a 128k "$k.m4a" 2>/dev/null \
        && echo "=== 音频 $k 完成 ==="
    fi
  done

  # 按时长升序选下一个待转录（跳过已有 json / 正被锁定）
  next=""
  next_dur=999999
  for n in $(seq 1 106); do
    k=$(printf 'h%02d' "$n")
    [ -f "$k.m4a" ] || continue
    [ -f "$k.json" ] && continue
    [ -f "$LOCKDIR/$k.lock" ] && continue
    dur=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$k.m4a" 2>/dev/null | cut -d. -f1)
    dur=${dur:-0}
    if [ "$dur" -lt "$next_dur" ]; then
      next=$k
      next_dur=$dur
    fi
  done

  if [ -z "$next" ]; then
    done_count=$(ls h*.json 2>/dev/null | grep -E '^h[0-9]+\.json$' | wc -l | tr -d ' ')
    dl_count=$(ls h*.source.mp4 2>/dev/null | wc -l | tr -d ' ')
    echo "=== 暂无可转：转录 $done_count/106，已下载 $dl_count ==="
    # 下载结束且全部转完则退出
    if ! pgrep -f 'b52-download.sh' >/dev/null 2>&1; then
      pending=0
      for n in $(seq 1 106); do
        k=$(printf 'h%02d' "$n")
        if [ -f "$k.m4a" ] && [ ! -f "$k.json" ]; then pending=$((pending+1)); fi
      done
      if [ "$pending" -eq 0 ] && [ "$done_count" -ge 1 ]; then
        echo "=== 短优先转录结束（$done_count）==="
        break
      fi
    fi
    sleep 20
    continue
  fi

  echo "=== 转录 $next (${next_dur}s) [短优先] ==="
  touch "$LOCKDIR/$next.lock"
  python3 -m whisper "$next.m4a" --model medium --language Chinese --output_dir . 2>&1 | tail -5
  rm -f "$LOCKDIR/$next.lock"
  if [ -f "$next.json" ]; then
    echo "=== $next 转录完成 ==="
  else
    echo "=== $next 转录可能失败 ==="
  fi
done
