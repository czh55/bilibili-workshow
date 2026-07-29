# B 站视频转 SVG · Webhook 触发提示词

把下面整段复制到任意模型，把 `{B站链接}` 换成真实链接；Token 填你自己的（或见本机 `docs/TRIGGER.local.md`）。

---

## 可直接粘贴的 Prompt

```text
请帮我触发 Cursor Automation「Bilibili 视频转文稿 SVG」。

严格按下列步骤执行，不要改 URL / Header / JSON 字段名：

1. 向这个 Webhook 发 POST 请求（关掉系统代理后再请求，避免连不上）：
   URL: https://api2.cursor.sh/automations/webhook/4bc55ebc-86f4-11f1-a7d1-d6b4613131ce
   Header:
     Content-Type: application/json
     Authorization: Bearer {你的_crsr_Token}
   Body (JSON):
   {
     "url": "{B站链接}",
     "date": "{YYYY-MM-DD，可选；不填则用今天}"
   }

2. 推荐命令（macOS / Linux）：

unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY all_proxy
curl -sS -w "\nHTTP_CODE:%{http_code}\n" -X POST \
  "https://api2.cursor.sh/automations/webhook/4bc55ebc-86f4-11f1-a7d1-d6b4613131ce" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {你的_crsr_Token}" \
  -d '{"url":"{B站链接}","date":"{YYYY-MM-DD}"}'

3. 根据返回结果告诉我：
   - success=true → 读出 backgroundComposerId，说明已排队
   - "is disabled" → 提醒我去 Automations 打开开关
   - 401/403 → Token 失效，需在 Automations 里重新复制
   - 其它错误 → 原样贴出响应体

4. 不要修改仓库代码，不要本地下载/转录视频；本任务只负责触发 Webhook。

本次要处理的视频：
{B站链接}
日期（可选）：{YYYY-MM-DD}
```

---

## 极简版

```text
用 curl POST 触发这个 Cursor Automation Webhook（先 unset 代理）：
URL: https://api2.cursor.sh/automations/webhook/4bc55ebc-86f4-11f1-a7d1-d6b4613131ce
Auth: Bearer {你的_crsr_Token}
Body: {"url":"这里换成B站链接","date":"2026-07-24"}
跑完把 HTTP 状态码和 JSON 响应贴给我。
```

---

## Payload

| 字段 | 必填 | 说明 |
|------|------|------|
| `url` | 是 | bilibili.com / b23.tv |
| `date` | 否 | 展示日期 YYYY-MM-DD |

成功：`{"success":true,"backgroundComposerId":"bc-..."}`
