---
summary: "Background exec execution and process management"
read_when:
  - Adding or modifying background exec behavior
  - Debugging long-running exec tasks
title: "Background Exec and Process Tool"
---

# boshqa kontekstlardan qayta foydalanish (mahalliy skriptlar, kelajakdagi desktop ilova va h.k.)

OpenClaw runs shell commands through the `exec` tool and keeps long‑running tasks in memory. The `process` tool manages those background sessions.

## exec tool

Key parameters:

- `command` (required)
- `yieldMs` (default 10000): auto‑background after this delay
- `background` (bool): background immediately
- `timeout` (seconds, default 1800): kill the process after this timeout
- `elevated` (bool): run on host if elevated mode is enabled/allowed
- Fon ijrosi + Jarayon asbobi Set `pty: true`.
- Haqiqiy TTY kerakmi?

Behavior:

- Foreground runs return output directly.
- When backgrounded (explicit or timeout), the tool returns `status: "running"` + `sessionId` and a short tail.
- Output is kept in memory until the session is polled or cleared.
- If the `process` tool is disallowed, `exec` runs synchronously and ignores `yieldMs`/`background`.

## Child process bridging

When spawning long-running child processes outside the exec/process tools (for example, CLI respawns or gateway helpers), attach the child-process bridge helper so termination signals are forwarded and listeners are detached on exit/error. This avoids orphaned processes on systemd and keeps shutdown behavior consistent across platforms.

Environment overrides:

- `PI_BASH_YIELD_MS`: default yield (ms)
- `PI_BASH_MAX_OUTPUT_CHARS`: in‑memory output cap (chars)
- `OPENCLAW_BASH_PENDING_MAX_OUTPUT_CHARS`: pending stdout/stderr cap per stream (chars)
- 1. `PI_BASH_JOB_TTL_MS`: yakunlangan sessiyalar uchun TTL (ms, 1 daqiqa–3 soat oralig‘ida cheklangan)

2. Konfiguratsiya (tavsiya etiladi):

- 3. `tools.exec.backgroundMs` (standart 10000)
- 4. `tools.exec.timeoutSec` (standart 1800)
- 5. `tools.exec.cleanupMs` (standart 1800000)
- 6. `tools.exec.notifyOnExit` (standart true): fon rejimidagi exec yakunlanganda tizim hodisasini navbatga qo‘shadi va heartbeat so‘raydi.

## 7. process vositasi

8. Amallar:

- 9. `list`: ishlayotgan + yakunlangan sessiyalar
- 10. `poll`: sessiya uchun yangi chiqishni chiqarib tashlash (shuningdek chiqish holatini bildiradi)
- 11. `log`: yig‘ilgan chiqishni o‘qish (`offset` + `limit` qo‘llab-quvvatlanadi)
- 12. `write`: stdin yuborish (`data`, ixtiyoriy `eof`)
- 13. `kill`: fon sessiyasini to‘xtatish
- 14. `clear`: yakunlangan sessiyani xotiradan olib tashlash
- 15. `remove`: agar ishlayotgan bo‘lsa o‘ldiradi, aks holda yakunlangan bo‘lsa tozalaydi

16. Eslatmalar:

- 17. Faqat fon rejimidagi sessiyalar ro‘yxatga olinadi va xotirada saqlanadi.
- 18. Jarayon qayta ishga tushirilganda sessiyalar yo‘qoladi (diskda saqlanmaydi).
- 19. Sessiya jurnallari faqat `process poll/log` ishga tushirilganda va vosita natijasi yozib olinganda chat tarixiga saqlanadi.
- 20. `process` agent bo‘yicha cheklangan; u faqat shu agent boshlagan sessiyalarni ko‘radi.
- 21. `process list` tez ko‘zdan kechirish uchun hosila `name` (buyruq fe’li + maqsad) ni o‘z ichiga oladi.
- 22. `process log` qatorlarga asoslangan `offset`/`limit` dan foydalanadi (`offset`ni qoldirsangiz, oxirgi N qator olinadi).

## 23. Misollar

24. Uzoq vazifani ishga tushiring va keyinroq so‘rov qiling:

```json
25. { "tool": "exec", "command": "sleep 5 && echo done", "yieldMs": 1000 }
```

```json
26. { "tool": "process", "action": "poll", "sessionId": "<id>" }
```

27. Darhol fon rejimida boshlash:

```json
28. { "tool": "exec", "command": "npm run build", "background": true }
```

29. stdin yuborish:

```json
30. { "tool": "process", "action": "write", "sessionId": "<id>", "data": "y\n" }
```
