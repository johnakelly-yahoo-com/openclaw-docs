---
summary: "`openclaw agent` uchun CLI ma’lumotnomasi (Gateway orqali bitta agent navbatini yuborish)"
read_when:
  - Skriptlardan bitta agent navbatini ishga tushirmoqchisiz (ixtiyoriy ravishda javobni yetkazish)
title: "agent"
---

# `openclaw agent`

Gateway orqali agent navbatini ishga tushiring (ichiga o‘rnatilgan rejim uchun `--local` dan foydalaning).
Sozlangan agentni to‘g‘ridan-to‘g‘ri nishonga olish uchun `--agent <id>` dan foydalaning.

Bog‘liq:

- Agent yuborish vositasi: [Agent send](/tools/agent-send)

## Misollar

```bash
openclaw agent --to +15555550123 --message "status update" --deliver
openclaw agent --agent ops --message "Summarize logs"
openclaw agent --session-id 1234 --message "Summarize inbox" --thinking medium
openclaw agent --agent ops --message "Generate report" --deliver --reply-channel slack --reply-to "#reports"
```
