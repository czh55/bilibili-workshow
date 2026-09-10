#!/bin/bash
# b54 短优先转录：j01–j46，有 m4a 即 Whisper medium 中文
cd /Users/chenzhiheng/Projects/bilibili-workshop
FFMPEG=$(command -v ffmpeg)
[ -z "$FFMPEG" ] && FFMPEG=/opt/homebrew/bin/ffmpeg
LOCKDIR=_work/b54-logs/whisper-locks
mkdir -p "$LOCKDIR" _work/b54-logs

while true; do
  for n in $(seq 1 46); do
    k=$(printf 'j%02d' "$n")
    src=$(ls "$k".source.* 2>/dev/null | head -1)
    if [ -n "$src" ] && [ ! -f "$k.m4a" ]; then
      "$FFMPEG" -y -i "$src" -vn -acodec aac -b:a 128k "$k.m4a" 2>/dev/null \
        && echo "=== 音频 $k 完成 ==="
    fi
    # 损坏的 m4a（ffprobe 失败）→ 重抽
    if [ -f "$k.m4a" ] && [ -n "$src" ]; then
      if ! ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$k.m4a" >/dev/null 2>&1; then
        echo "=== $k.m4a 损坏，重抽 ==="
        rm -f "$k.m4a"
        "$FFMPEG" -y -i "$src" -vn -acodec aac -b:a 128k "$k.m4a" 2>/dev/null \
          && echo "=== 音频 $k 重抽完成 ==="
      fi
    fi
  done

  next=""; next_dur=999999
  for n in $(seq 1 46); do
    k=$(printf 'j%02d' "$n")
    [ -f "$k.m4a" ] || continue
    [ -f "$k.json" ] && continue
    [ -f "$LOCKDIR/$k.lock" ] && continue
    dur=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$k.m4a" 2>/dev/null | cut -d. -f1)
    # 无法探测时长则跳过，避免短优先死循环卡在 0s 坏文件
    [ -n "$dur" ] || continue
    dur=${dur:-0}
    if [ "$dur" -lt 1 ]; then continue; fi
    if [ "$dur" -lt "$next_dur" ]; then next=$k; next_dur=$dur; fi
  done

  if [ -z "$next" ]; then
    done_count=$(ls j[0-9][0-9].json 2>/dev/null | wc -l | tr -d ' ')
    dl_count=$(ls j*.source.mp4 2>/dev/null | wc -l | tr -d ' ')
    echo "=== 暂无可转：转录 $done_count/46，已下载 $dl_count/46 ==="
    if ! pgrep -f 'b54-download.sh' >/dev/null 2>&1; then
      pending=0
      for n in $(seq 1 46); do
        k=$(printf 'j%02d' "$n")
        if [ -f "$k.m4a" ] && [ ! -f "$k.json" ]; then pending=$((pending+1)); fi
      done
      if [ "$pending" -eq 0 ] && [ "$done_count" -ge 1 ]; then
        echo "=== b54 转录结束（$done_count）==="
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
  [ -f "$next.json" ] && echo "=== $next 转录完成 ===" || echo "=== $next 转录可能失败 ==="
done
