#!/bin/bash
# b55 短优先转录：k01–k05
cd /Users/chenzhiheng/Projects/video-notes
FFMPEG=$(command -v ffmpeg)
[ -z "$FFMPEG" ] && FFMPEG=/opt/homebrew/bin/ffmpeg
LOCKDIR=_work/b55-logs/whisper-locks
mkdir -p "$LOCKDIR" _work/b55-logs

while true; do
  for n in $(seq 1 5); do
    k=$(printf 'k%02d' "$n")
    src=$(ls "$k".source.* 2>/dev/null | head -1)
    if [ -n "$src" ] && [ ! -f "$k.m4a" ]; then
      "$FFMPEG" -y -i "$src" -vn -acodec aac -b:a 128k "$k.m4a" 2>/dev/null \
        && echo "=== 音频 $k 完成 ==="
    fi
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
  for n in $(seq 1 5); do
    k=$(printf 'k%02d' "$n")
    [ -f "$k.m4a" ] || continue
    [ -f "$k.json" ] && continue
    [ -f "$LOCKDIR/$k.lock" ] && continue
    dur=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$k.m4a" 2>/dev/null | cut -d. -f1)
    [ -n "$dur" ] || continue
    dur=${dur:-0}
    if [ "$dur" -lt 1 ]; then continue; fi
    if [ "$dur" -lt "$next_dur" ]; then next=$k; next_dur=$dur; fi
  done

  if [ -z "$next" ]; then
    done_count=$(ls k0[1-5].json 2>/dev/null | wc -l | tr -d ' ')
    dl_count=$(ls k0[1-5].source.mp4 2>/dev/null | wc -l | tr -d ' ')
    echo "=== 暂无可转：转录 $done_count/5，已下载 $dl_count/5 ==="
    if ! pgrep -f 'b55-download.sh' >/dev/null 2>&1; then
      pending=0
      for n in $(seq 1 5); do
        k=$(printf 'k%02d' "$n")
        if [ -f "$k.m4a" ] && [ ! -f "$k.json" ]; then pending=$((pending+1)); fi
      done
      if [ "$pending" -eq 0 ] && [ "$done_count" -ge 5 ]; then
        echo "=== b55 转录结束（$done_count）==="
        break
      fi
      if [ "$dl_count" -ge 5 ] && [ "$pending" -eq 0 ] && [ "$done_count" -lt 5 ]; then
        echo "=== 下载齐但转录不足，继续等待 ==="
      fi
      if [ "$dl_count" -ge 5 ] && [ "$done_count" -ge 5 ]; then
        echo "=== b55 转录结束（$done_count）==="
        break
      fi
    fi
    sleep 15
    continue
  fi

  echo "=== 转录 $next (${next_dur}s) [短优先] ==="
  touch "$LOCKDIR/$next.lock"
  python3 -m whisper "$next.m4a" --model medium --language Chinese --output_dir . 2>&1 | tail -8
  rm -f "$LOCKDIR/$next.lock"
  [ -f "$next.json" ] && echo "=== $next 转录完成 ===" || echo "=== $next 转录可能失败 ==="
done
