#!/usr/bin/env python3
"""b46 预览帧拼网格：把每篇的预览帧拼成 4 列网格图供审阅。"""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
PREV = ROOT / "_work/b46-preview"
FF = "/opt/homebrew/bin/ffmpeg"

keys = [f"f{i:02d}" for i in range(1, 15)]
for k in keys:
    files = sorted(PREV.glob(f"{k}_[0-9]*.jpg"), key=lambda p: int(p.stem.split("_")[1]))
    if not files:
        continue
    cols = 4
    rows = (len(files) + cols - 1) // cols
    row_paths = []
    for r in range(rows):
        chunk = files[r * cols:(r + 1) * cols]
        args = []
        for f in chunk:
            args += ["-i", str(f)]
        row_path = PREV / f"{k}_row{r}.jpg"
        n = len(chunk)
        args = []
        for f in chunk:
            args += ["-i", str(f)]
        subprocess.run(
            [FF, "-y", "-v", "error", *args,
             "-filter_complex", f"hstack=inputs={n},scale=-2:480,pad=width=1280:height=480:x=0:y=0", str(row_path)],
            check=True, capture_output=True)
        row_paths.append(row_path)
    grid = PREV / f"{k}_grid.jpg"
    if len(row_paths) == 1:
        subprocess.run(["cp", str(row_paths[0]), str(grid)], check=True)
    else:
        args = []
        for f in row_paths:
            args += ["-i", str(f)]
        subprocess.run(
            [FF, "-y", "-v", "error", *args,
             "-filter_complex", f"vstack=inputs={len(row_paths)},scale=-2:800", str(grid)],
            check=True, capture_output=True)
    print(f"{k}: {len(files)} 帧 -> {grid.name}")
print("完成")
