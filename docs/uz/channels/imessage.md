---
summary: "imsg orqali legacy iMessage qo‘llab-quvvatlovi (stdio orqali JSON-RPC). Yangi sozlamalar BlueBubbles dan foydalanishi kerak."
read_when:
  - iMessage qo‘llab-quvvatlovini sozlash
  - Debugging iMessage send/receive
title: iMessage
---

# iMessage (legacy: imsg)

> **Tavsiya etiladi:** yangi iMessage sozlamalari uchun [BlueBubbles](/channels/bluebubbles) dan foydalaning.
>
> `imsg` kanali — legacy tashqi CLI integratsiyasi bo‘lib, kelajakdagi relizda olib tashlanishi mumkin.

Holat: legacy tashqi CLI integratsiyasi. Gateway `imsg rpc` ni ishga tushiradi (stdio orqali JSON-RPC).

## Tezkor sozlash (boshlovchilar uchun)

1. Ensure Messages is signed in on this Mac.
2. `imsg` ni o‘rnating:
   - `brew install steipete/tap/imsg`
3. OpenClaw ni `channels.imessage.cliPath` va `channels.imessage.dbPath` bilan sozlang.
4. Gateway’ni ishga tushiring va macOS so‘rovlarini tasdiqlang (Automation + Full Disk Access).

Minimal konfiguratsiya:

```json5
{
  channels: {
    imessage: {
      enabled: true,
      cliPath: "/usr/local/bin/imsg",
      dbPath: "/Users/<you>/Library/Messages/chat.db",
    },
  },
}
```

## Bu nima

- macOS’da `imsg` ga asoslangan iMessage kanali.
- Deterministik yo‘naltirish: javoblar har doim iMessage’ga qaytadi.
- DM’lar agentning asosiy sessiyasini ulashadi; guruhlar esa izolyatsiyalangan (`agent:<agentId>:imessage:group:<chat_id>`).
- Agar ko‘p ishtirokchili thread `is_group=false` bilan kelsa ham, uni `channels.imessage.groups` orqali `chat_id` bo‘yicha izolyatsiya qilishingiz mumkin (quyidagi “Group-ish threads” ga qarang).

## Konfiguratsiya yozuvlari

Standart bo‘yicha iMessage `/config set|unset` orqali ishga tushirilgan konfiguratsiya yangilanishlarini yozishga ruxsat etilgan (`commands.config: true` talab etiladi).

O‘chirish:

```json5
{
  channels: { imessage: { configWrites: false } },
}
```

## Talablar

- Messages akkauntiga kirilgan macOS.
- OpenClaw + `imsg` uchun Full Disk Access (Messages DB’ga kirish).
- Automation permission when sending.
- `channels.imessage.cliPath` can point to any command that proxies stdin/stdout (for example, a wrapper script that SSHes to another Mac and runs `imsg rpc`).

## Troubleshooting macOS Privacy and Security TCC

If sending/receiving fails (for example, `imsg rpc` exits non-zero, times out, or the gateway appears to hang), a common cause is a macOS permission prompt that was never approved.

macOS grants TCC permissions per app/process context. Approve prompts in the same context that runs `imsg` (for example, Terminal/iTerm, a LaunchAgent session, or an SSH-launched process).

Checklist:

- **Full Disk Access**: allow access for the process running OpenClaw (and any shell/SSH wrapper that executes `imsg`). This is required to read the Messages database (`chat.db`).
- **Automation → Messages**: allow the process running OpenClaw (and/or your terminal) to control **Messages.app** for outbound sends.
- **`imsg` CLI health**: verify `imsg` is installed and supports RPC (`imsg rpc --help`).

Tip: If OpenClaw is running headless (LaunchAgent/systemd/SSH) the macOS prompt can be easy to miss. Run a one-time interactive command in a GUI terminal to force the prompt, then retry:

```bash
imsg chats --limit 1
# or
imsg send <handle> "test"
```

Related macOS folder permissions (Desktop/Documents/Downloads): [/platforms/mac/permissions](/platforms/mac/permissions).

## Setup (fast path)

1. Ensure Messages is signed in on this Mac.
2. Configure iMessage and start the gateway.

### Dedicated bot macOS user (for isolated identity)

If you want the bot to send from a **separate iMessage identity** (and keep your personal Messages clean), use a dedicated Apple ID + a dedicated macOS user.

1. Create a dedicated Apple ID (example: `my-cool-bot@icloud.com`).
   - Apple may require a phone number for verification / 2FA.
2. Create a macOS user (example: `openclawhome`) and sign into it.
3. Open Messages in that macOS user and sign into iMessage using the bot Apple ID.
4. Enable Remote Login (System Settings → General → Sharing → Remote Login).
5. Install `imsg`:
   - `brew install steipete/tap/imsg`
6. Set up SSH so `ssh <bot-macos-user>@localhost true` works without a password.
7. Point `channels.imessage.accounts.bot.cliPath` at an SSH wrapper that runs `imsg` as the bot user.

First-run note: sending/receiving may require GUI approvals (Automation + Full Disk Access) in the _bot macOS user_. If `imsg rpc` looks stuck or exits, log into that user (Screen Sharing helps), run a one-time `imsg chats --limit 1` / `imsg send ...`, approve prompts, then retry. See [Troubleshooting macOS Privacy and Security TCC](#troubleshooting-macos-privacy-and-security-tcc).

Example wrapper (`chmod +x`). Replace `<bot-macos-user>` with your actual macOS username:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Run an interactive SSH once first to accept host keys:
#   ssh <bot-macos-user>@localhost true
exec /usr/bin/ssh -o BatchMode=yes -o ConnectTimeout=5 -T <bot-macos-user>@localhost \
  "/usr/local/bin/imsg" "$@"
```

Example config:

```json5
{
  channels: {
    imessage: {
      enabled: true,
      accounts: {
        bot: {
          name: "Bot",
          enabled: true,
          cliPath: "/path/to/imsg-bot",
          dbPath: "/Users/<bot-macos-user>/Library/Messages/chat.db",
        },
      },
    },
  },
}
```

For single-account setups, use flat options (`channels.imessage.cliPath`, `channels.imessage.dbPath`) instead of the `accounts` map.

### Remote/SSH variant (optional)

If you want iMessage on another Mac, set `channels.imessage.cliPath` to a wrapper that runs `imsg` on the remote macOS host over SSH. OpenClaw only needs stdio.

Example wrapper:

```bash
#!/usr/bin/env bash
exec ssh -T gateway-host imsg "$@"
```

**Remote attachments:** When `cliPath` points to a remote host via SSH, attachment paths in the Messages database reference files on the remote machine. OpenClaw can automatically fetch these over SCP by setting `channels.imessage.remoteHost`:

```json5
{
  channels: {
    imessage: {
      cliPath: "~/imsg-ssh", // SSH wrapper to remote Mac
      remoteHost: "user@gateway-host", // for SCP file transfer
      includeAttachments: true,
    },
  },
}
```

If `remoteHost` is not set, OpenClaw attempts to auto-detect it by parsing the SSH command in your wrapper script. Explicit configuration is recommended for reliability.

#### Remote Mac via Tailscale (example)

If the Gateway runs on a Linux host/VM but iMessage must run on a Mac, Tailscale is the simplest bridge: the Gateway talks to the Mac over the tailnet, runs `imsg` via SSH, and SCPs attachments back.

1. Arxitektura:

```mermaid
12. Telegram orqali juftlash (iOS uchun tavsiya etiladi)
```

2. Aniq konfiguratsiya misoli (Tailscale hostname):

```json5
3. {
  channels: {
    imessage: {
      enabled: true,
      cliPath: "~/.openclaw/scripts/imsg-ssh",
      remoteHost: "bot@mac-mini.tailnet-1234.ts.net",
      includeAttachments: true,
      dbPath: "/Users/bot/Library/Messages/chat.db",
    },
  },
}
```

4. Wrapper misoli (`~/.openclaw/scripts/imsg-ssh`):

```bash
5. #!/usr/bin/env bash
exec ssh -T bot@mac-mini.tailnet-1234.ts.net imsg "$@"
```

6. Eslatmalar:

- 7. Mac Messages’ga tizimga kirgan bo‘lishi va Remote Login yoqilgan bo‘lishi kerak.
- 8. SSH kalitlaridan foydalaning, shunda `ssh bot@mac-mini.tailnet-1234.ts.net` buyruqi so‘rovlarsiz ishlaydi.
- 9. `remoteHost` ilovalarni SCP orqali yuklab olish uchun SSH manziliga mos bo‘lishi kerak.

10. Ko‘p akkauntli qo‘llab-quvvatlash: har bir akkaunt uchun alohida konfiguratsiya va ixtiyoriy `name` bilan `channels.imessage.accounts` dan foydalaning. 11. Umumiy naqsh uchun [`gateway/configuration`](/gateway/configuration#telegramaccounts--discordaccounts--slackaccounts--signalaccounts--imessageaccounts) ga qarang. 12. `~/.openclaw/openclaw.json` ni commit qilmang (unda ko‘pincha tokenlar bo‘ladi).

## 13. Kirish nazorati (DMlar + guruhlar)

14. DMlar:

- 15. Standart: `channels.imessage.dmPolicy = "pairing"`.
- 16. Noma’lum jo‘natuvchilar pairing kodi oladi; tasdiqlanmaguncha xabarlar e’tiborga olinmaydi (kodlar 1 soatdan keyin eskiradi).
- 17. Tasdiqlash:
  - 18. `openclaw pairing list imessage`
  - 19. `openclaw pairing approve imessage <CODE>`
- 20. Pairing iMessage DMlar uchun standart token almashinuvidir. 21. Tafsilotlar: [Pairing](/channels/pairing)

22. Guruhlar:

- 23. `channels.imessage.groupPolicy = open | allowlist | disabled`.
- 24. `allowlist` o‘rnatilganda, guruhlarda kim ishga tushira olishini `channels.imessage.groupAllowFrom` boshqaradi.
- 25. Mention gating `agents.list[].groupChat.mentionPatterns` (yoki `messages.groupChat.mentionPatterns`) dan foydalanadi, chunki iMessage’da native mention metama’lumotlari yo‘q.
- 26. Ko‘p-agent override: har bir agent uchun `agents.list[].groupChat.mentionPatterns` da alohida patternlar o‘rnating.

## 27. Qanday ishlaydi (xatti-harakat)

- 28. `imsg` xabar hodisalarini stream qiladi; gateway ularni umumiy kanal konvertiga normallashtiradi.
- 29. Javoblar har doim o‘sha chat id yoki handle’ga qaytariladi.

## 30. Guruhga o‘xshash threadlar (`is_group=false`)

31. Ba’zi iMessage threadlarida bir nechta ishtirokchi bo‘lishi mumkin, ammo Messages chat identifikatorni qanday saqlashiga qarab `is_group=false` bilan keladi.

32. Agar `channels.imessage.groups` ostida `chat_id` ni aniq sozlasangiz, OpenClaw ushbu threadni “guruh” sifatida ko‘radi:

- 33. sessiya izolyatsiyasi (alohida `agent:<agentId>:imessage:group:<chat_id>` sessiya kaliti)
- 34. guruh allowlisting / mention gating xatti-harakati

35. Misol:

```json5
36. {
  channels: {
    imessage: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15555550123"],
      groups: {
        "42": { requireMention: false },
      },
    },
  },
}
```

37. Bu muayyan thread uchun alohida shaxsiyat/model kerak bo‘lganda foydalidir (qarang: [Multi-agent routing](/concepts/multi-agent)). 38. Fayl tizimi izolyatsiyasi uchun [Sandboxing](/gateway/sandboxing) ga qarang.

## 39. Media + cheklovlar

- 40. `channels.imessage.includeAttachments` orqali ixtiyoriy ilova (attachment) qabul qilish.
- 41. Media limiti `channels.imessage.mediaMaxMb` orqali belgilanadi.

## 42. Cheklovlar

- 43. Chiqishdagi matn `channels.imessage.textChunkLimit` ga bo‘linadi (standart 4000).
- 44. Ixtiyoriy yangi qator bo‘yicha bo‘lish: uzunlik bo‘yicha bo‘lishdan oldin bo‘sh qatorlar (paragraf chegaralari) bo‘yicha ajratish uchun `channels.imessage.chunkMode="newline"` ni o‘rnating.
- 45. Media yuklashlari `channels.imessage.mediaMaxMb` bilan cheklanadi (standart 16).

## 46. Manzillash / yetkazib berish nishonlari

47. Barqaror marshrutlash uchun `chat_id` ni afzal ko‘ring:

- 48. `chat_id:123` (afzal)
- 49. `chat_guid:...`
- 50. `chat_identifier:...`
- direct handles: `imessage:+1555` / `sms:+1555` / `user@example.com`

List chats:

```
imsg chats --limit 20
```

## Configuration reference (iMessage)

Full configuration: [Configuration](/gateway/configuration)

Provider options:

- `channels.imessage.enabled`: enable/disable channel startup.
- `channels.imessage.cliPath`: path to `imsg`.
- `channels.imessage.dbPath`: Messages DB path.
- `channels.imessage.remoteHost`: SSH host for SCP attachment transfer when `cliPath` points to a remote Mac (e.g., `user@gateway-host`). Auto-detected from SSH wrapper if not set.
- `channels.imessage.service`: `imessage | sms | auto`.
- `channels.imessage.region`: SMS region.
- `channels.imessage.dmPolicy`: `pairing | allowlist | open | disabled` (default: pairing).
- `channels.imessage.allowFrom`: DM allowlist (handles, emails, E.164 numbers, or `chat_id:*`). `open` requires `"*"`. iMessage has no usernames; use handles or chat targets.
- `channels.imessage.groupPolicy`: `open | allowlist | disabled` (default: allowlist).
- `channels.imessage.groupAllowFrom`: group sender allowlist.
- `channels.imessage.historyLimit` / `channels.imessage.accounts.*.historyLimit`: max group messages to include as context (0 disables).
- `channels.imessage.dmHistoryLimit`: DM history limit in user turns. Per-user overrides: `channels.imessage.dms["<handle>"].historyLimit`.
- `channels.imessage.groups`: per-group defaults + allowlist (use `"*"` for global defaults).
- `channels.imessage.includeAttachments`: ingest attachments into context.
- `channels.imessage.mediaMaxMb`: inbound/outbound media cap (MB).
- `channels.imessage.textChunkLimit`: outbound chunk size (chars).
- `channels.imessage.chunkMode`: `length` (default) or `newline` to split on blank lines (paragraph boundaries) before length chunking.

Related global options:

- `agents.list[].groupChat.mentionPatterns` (or `messages.groupChat.mentionPatterns`).
- `messages.responsePrefix`.
