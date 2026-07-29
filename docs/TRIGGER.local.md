# 本机私有触发提示词（含 Token，勿 push）

```text
请帮我触发 Cursor Automation「Bilibili 视频转文稿 SVG」。

严格按下列步骤执行，不要改 URL / Header / JSON 字段名：

1. 向这个 Webhook 发 POST（先 unset 代理）：
   URL: https://api2.cursor.sh/automations/webhook/4bc55ebc-86f4-11f1-a7d1-d6b4613131ce
   Header:
     Content-Type: application/json
     Authorization: Bearer crsr_60f788a61f65b30e343b1b6cfe4c5d77c497e38383fd92482fc1811cc5688aea
   Body:
   {
     "url": "{B站链接}",
     "date": "{YYYY-MM-DD}"
   }

2. 命令：

unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY all_proxy
curl -sS -w "\nHTTP_CODE:%{http_code}\n" -X POST \
  "https://api2.cursor.sh/automations/webhook/4bc55ebc-86f4-11f1-a7d1-d6b4613131ce" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer crsr_60f788a61f65b30e343b1b6cfe4c5d77c497e38383fd92482fc1811cc5688aea" \
  -d '{"url":"{B站链接}","date":"{YYYY-MM-DD}"}'

3. 解读响应：
   - success=true → 报告 backgroundComposerId
   - is disabled → 提醒开启 Automation
   - 401/403 → Token 失效
   - 其它 → 原样贴响应

4. 只触发 Webhook，不本地下载/转录。

本次视频：{B站链接}
日期：{YYYY-MM-DD}
```

## 极简版

```text
用 curl POST 触发 Cursor Automation（先 unset 代理）：
URL: https://api2.cursor.sh/automations/webhook/4bc55ebc-86f4-11f1-a7d1-d6b4613131ce
Auth: Bearer crsr_60f788a61f65b30e343b1b6cfe4c5d77c497e38383fd92482fc1811cc5688aea
Body: {"url":"这里换成B站链接","date":"2026-07-24"}
把 HTTP 状态码和 JSON 响应贴给我。
```
