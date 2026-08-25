#!/usr/bin/env python3
"""b50：按 slugs 生成关键截图。

用法：
  python3 scripts/b50-make-shots.py {slug} [{slug} ...]

每个 slug 需要存在 shots-{slug}.json，格式：
{
  "key": "d01",
  "shots": [{"file": "shot-01.jpg", "time": "00:20", "chapter": 1, "scene": "..."}]
}
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
FF = "/opt/homebrew/bin/ffmpeg"


def parse_time(t: str) -> float:
    parts = t.split(":")
    if len(parts) == 2:
        return int(parts[0]) * 60 + float(parts[1])
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    return float(t)


def extract(slug: str, shots_file: Path) -> int:
    data = json.loads(shots_file.read_text(encoding="utf-8"))
    shots = data["shots"]
    if not shots:
        print(f"✗ {slug}: shots 为空")
        return 0
    key = data.get("key")
    if not key:
        print(f"✗ {slug}: shots JSON 缺少 key")
        return 0
    src = ROOT / f"{key}.source.mp4"
    if not src.exists():
        # 兼容 .mp4/.mkv 等其它扩展名
        cands = list(ROOT.glob(f"{key}.source.*"))
        if not cands:
            print(f"✗ {slug}: 找不到 {key}.source.*")
            return 0
        src = cands[0]
    outdir = ROOT / "docs" / "assets" / slug
    outdir.mkdir(parents=True, exist_ok=True)
    n = 0
    for s in shots:
        t = parse_time(s["time"])
        out = outdir / s["file"]
        if out.exists():
            n += 1
            continue
        r = subprocess.run(
            [FF, "-y", "-v", "error", "-ss", str(max(0, t - 0.2)), "-i", str(src),
             "-frames:v", "1", "-vf", "scale='min(1280,iw)':-2", "-q:v", "2", str(out)],
            capture_output=True, text=True)
        if r.returncode != 0:
            print(f"  ✗ {slug}/{s['file']} @{s['time']}: {r.stderr.strip()[:120]}")
        else:
            n += 1
    print(f"✓ {slug}: {n}/{len(shots)} 截图")
    return n


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    for slug in args:
        shots_file = ROOT / f"shots-{slug}.json"
        if not shots_file.exists():
            print(f"✗ {slug}: 无 shots JSON")
            continue
        extract(slug, shots_file)


if __name__ == "__main__":
    main()
