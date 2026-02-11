---
summary: "`openclaw webhooks` uchun CLI ma’lumotnomasi (webhook yordamchilari + Gmail Pub/Sub)"
read_when:
  - Siz Gmail Pub/Sub hodisalarini OpenClaw’ga ulashni xohlaysiz
  - Siz webhook yordamchi buyruqlarini xohlaysiz
title: "Gateway RPC: `agent` va `agent.wait`."
---

# `openclaw webhooks`

Webhook yordamchilari va integratsiyalar (Gmail Pub/Sub, webhook yordamchilari).

Bog‘liq:

- Webhooklar: [Webhook](/automation/webhook)
- Gmail Pub/Sub: [Gmail Pub/Sub](/automation/gmail-pubsub)

## Gmail

```bash
openclaw webhooks gmail setup --account you@example.com
openclaw webhooks gmail run
```

Batafsil ma’lumot uchun [Gmail Pub/Sub hujjatlari](/automation/gmail-pubsub) ga qarang.
