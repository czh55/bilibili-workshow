# 个人专栏生成脚本

`platform: personal` 条目的可复用生成器。

## 本篇

```bash
# 仓库根目录执行
node scripts/personal/generate-a6700-slog-sunrise-practice-html.mjs
node scripts/personal/generate-a6700-slog-sunrise-practice-svg.mjs
node scripts/personal/generate-log-color-grading-notes-svg.mjs
python3 scripts/build-search-index.py
```

规范见 `docs/WORKFLOW.md` →「个人专栏（platform: personal）」。

## 类目总结

```bash
# 根据 docs/category-summaries/content.json + index.json 生成 12 篇类目导读，并写入 topics.json
python3 scripts/generate-category-summaries.py
```
