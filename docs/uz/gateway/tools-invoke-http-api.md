---
summary: "Gateway HTTP endpoint’i orqali bitta asbobni to‘g‘ridan-to‘g‘ri chaqirish"
read_when:
  - To‘liq agent aylanishini ishga tushirmasdan asboblarni chaqirish
  - Asbob siyosati nazoratini talab qiladigan avtomatlasiyalarni yaratish
title: "Tools Invoke API"
---

# Tools Invoke (HTTP)

OpenClaw Gateway bitta asbobni to‘g‘ridan-to‘g‘ri chaqirish uchun oddiy HTTP endpoint taqdim etadi. U har doim yoqilgan, biroq Gateway autentifikatsiyasi va asbob siyosati bilan cheklangan.

- `POST /tools/invoke`
- Gateway bilan bir xil port (WS + HTTP multiplex): `http://<gateway-host>:<port>/tools/invoke`

Standart maksimal payload hajmi 2 MB.

## Autentifikatsiya

Gateway autentifikatsiya konfiguratsiyasidan foydalanadi. Bearer token yuboring:

- `Authorization: Bearer <token>`

Eslatmalar:

- When `gateway.auth.mode="token"`, use `gateway.auth.token` (or `OPENCLAW_GATEWAY_TOKEN`).
- When `gateway.auth.mode="password"`, use `gateway.auth.password` (or `OPENCLAW_GATEWAY_PASSWORD`).

## 11. So‘rov tanasi

```json
{
  "tool": "sessions_list",
  "action": "json",
  "args": {},
  "sessionKey": "main",
  "dryRun": false
}
```

Fields:

- `tool` (string, required): tool name to invoke.
- `action` (string, optional): mapped into args if the tool schema supports `action` and the args payload omitted it.
- `args` (object, optional): tool-specific arguments.
- 12. `sessionKey` (string, ixtiyoriy): maqsadli sessiya kaliti. If omitted or `"main"`, the Gateway uses the configured main session key (honors `session.mainKey` and default agent, or `global` in global scope).
- `dryRun` (boolean, optional): reserved for future use; currently ignored.

## Policy + routing behavior

13. Asboblar mavjudligi Gateway agentlari ishlatadigan xuddi shu siyosat zanjiri orqali filtrlanadi:

- `tools.profile` / `tools.byProvider.profile`
- `tools.allow` / `tools.byProvider.allow`
- `agents.<id>.tools.allow` / `agents.<id>.tools.byProvider.allow`
- group policies (if the session key maps to a group or channel)
- subagent policy (when invoking with a subagent session key)

If a tool is not allowed by policy, the endpoint returns **404**.

To help group policies resolve context, you can optionally set:

- `x-openclaw-message-channel: <channel>` (example: `slack`, `telegram`)
- `x-openclaw-account-id: <accountId>` (when multiple accounts exist)

## 14. Javoblar

- `200` → `{ ok: true, result }`
- `400` → `{ ok: false, error: { type, message } }` (invalid request or tool error)
- `401` → unauthorized
- `404` → tool not available (not found or not allowlisted)
- `405` → method not allowed

## Example

```bash
curl -sS http://127.0.0.1:18789/tools/invoke \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "tool": "sessions_list",
    "action": "json",
    "args": {}
  }'
```
