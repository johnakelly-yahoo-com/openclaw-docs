---
summary: "Terminal UI (TUI): connect to the Gateway from any machine"
read_when:
  - You want a beginner-friendly walkthrough of the TUI
  - You need the complete list of TUI features, commands, and shortcuts
title: "TUI"
---

# TUI (Terminal UI)

## Quick start

1. Start the Gateway.

```bash
openclaw gateway
```

2. Open the TUI.

```bash
openclaw tui
```

3. Type a message and press Enter.

Remote Gateway:

```bash
openclaw tui --url ws://<host>:<port> --token <gateway-token>
```

Use `--password` if your Gateway uses password auth.

## What you see

- Header: connection URL, current agent, current session.
- Chat log: user messages, assistant replies, system notices, tool cards.
- Status line: connection/run state (connecting, running, streaming, idle, error).
- Footer: connection state + agent + session + model + think/verbose/reasoning + token counts + deliver.
- Input: text editor with autocomplete.

## Mental model: agents + sessions

- Agents are unique slugs (e.g. `main`, `research`). The Gateway exposes the list.
- Sessions belong to the current agent.
- Session keys are stored as `agent:<agentId>:<sessionKey>`.
  - If you type `/session main`, the TUI expands it to `agent:<currentAgent>:main`.
  - If you type `/session agent:other:main`, you switch to that agent session explicitly.
- Session scope:
  - `per-sender` (default): each agent has many sessions.
  - `global`: the TUI always uses the `global` session (the picker may be empty).
- The current agent + session are always visible in the footer.

## Sending + delivery

- Messages are sent to the Gateway; delivery to providers is off by default.
- Turn delivery on:
  - `/deliver on`
  - 1. yoki Sozlamalar paneli
  - 2. yoki `openclaw tui --deliver` bilan boshlang

## 3. Tanlagichlar + qoplamalar

- 4. Model tanlagichi: mavjud modellarni roʻyxatlaydi va sessiya uchun ustuvor sozlamani oʻrnatadi.
- 5. Agent tanlagichi: boshqa agentni tanlang.
- 6. Sessiya tanlagichi: faqat joriy agent uchun sessiyalarni koʻrsatadi.
- 7. Sozlamalar: yetkazib berishni, asbob chiqishini kengaytirishni va fikrlash koʻrinishini yoqib/oʻchirish.

## Keyboard shortcuts

- 9. Enter: xabar yuborish
- 10. Esc: faol ishga tushirishni bekor qilish
- 11. Ctrl+C: kiritmani tozalash (chiqish uchun ikki marta bosing)
- 12. Ctrl+D: chiqish
- 13. Ctrl+L: model tanlagichi
- 14. Ctrl+G: agent tanlagichi
- 15. Ctrl+P: sessiya tanlagichi
- 16. Ctrl+O: asbob chiqishini kengaytirishni yoqib/oʻchirish
- 17. Ctrl+T: fikrlash koʻrinishini yoqib/oʻchirish (tarix qayta yuklanadi)

## 18. Slash buyruqlar

19. Asosiy:

- `/help`
- `/status`
- 22. `/agent <id>` (yoki `/agents`)
- 23. `/session <key>` (yoki `/sessions`)
- 24. `/model <provider/model>` (yoki `/models`)

25. Sessiya boshqaruvlari:

- 26. `/think <off|minimal|low|medium|high>`
- 27. `/verbose <on|full|off>`
- `/reasoning <on|off|stream>`
- 29. `/usage <off|tokens|full>`
- 30. `/elevated <on|off|ask|full>` (alias: `/elev`)
- 31. `/activation <mention|always>`
- 32. `/deliver <on|off>`

33. Sessiya hayotiy sikli:

- 34. `/new` yoki `/reset` (sessiyani tiklash)
- 35. `/abort` (faol ishga tushirishni bekor qilish)
- 36. `/settings`
- 37. `/exit`

38. Boshqa Gateway slash buyruqlari (masalan, `/context`) Gateway’ga uzatiladi va tizim chiqishi sifatida ko‘rsatiladi. 39. [Slash commands](/tools/slash-commands) ni ko‘ring.

## 40. Mahalliy shell buyruqlari

- 41. TUI xostida mahalliy shell buyrug‘ini ishga tushirish uchun qator boshiga `!` qo‘ying.
- 42. TUI har bir sessiyada bir marta mahalliy bajarishga ruxsat so‘raydi; rad etilsa, sessiya davomida `!` o‘chirilgan bo‘lib qoladi.
- 43. Buyruqlar TUI ishchi katalogida yangi, interaktiv bo‘lmagan shellda bajariladi (doimiy `cd`/muhit yo‘q).
- 44. Yolg‘iz `!` oddiy xabar sifatida yuboriladi; boshidagi bo‘shliqlar mahalliy bajarishni ishga tushirmaydi.

## 45. Asbob chiqishi

- 46. Asbob chaqiruvlari argumentlar va natijalar bilan kartochkalar ko‘rinishida ko‘rsatiladi.
- 47. Ctrl+O yig‘ilgan/kengaytirilgan ko‘rinishlar o‘rtasida almashadi.
- 48. Asboblar ishlayotganida, qisman yangilanishlar shu kartochkaga oqim sifatida keladi.

## 49. Tarix + oqim

- 50. Ulanishda TUI eng so‘nggi tarixni yuklaydi (standart 200 ta xabar).
- Streaming responses update in place until finalized.
- The TUI also listens to agent tool events for richer tool cards.

## Connection details

- The TUI registers with the Gateway as `mode: "tui"`.
- Reconnects show a system message; event gaps are surfaced in the log.

## Options

- `--url <url>`: Gateway WebSocket URL (defaults to config or `ws://127.0.0.1:<port>`)
- `--token <token>`: Gateway token (if required)
- `--password <password>`: Gateway password (if required)
- `--session <key>`: Session key (default: `main`, or `global` when scope is global)
- `--deliver`: Deliver assistant replies to the provider (default off)
- `--thinking <level>`: Override thinking level for sends
- `--timeout-ms <ms>`: Agent timeout in ms (defaults to `agents.defaults.timeoutSeconds`)

Note: when you set `--url`, the TUI does not fall back to config or environment credentials.
Pass `--token` or `--password` explicitly. Missing explicit credentials is an error.

## Troubleshooting

No output after sending a message:

- Run `/status` in the TUI to confirm the Gateway is connected and idle/busy.
- Check the Gateway logs: `openclaw logs --follow`.
- Confirm the agent can run: `openclaw status` and `openclaw models status`.
- If you expect messages in a chat channel, enable delivery (`/deliver on` or `--deliver`).
- `--history-limit <n>`: History entries to load (default 200)

## Connection troubleshooting

- `disconnected`: ensure the Gateway is running and your `--url/--token/--password` are correct.
- No agents in picker: check `openclaw agents list` and your routing config.
- Empty session picker: you might be in global scope or have no sessions yet.
