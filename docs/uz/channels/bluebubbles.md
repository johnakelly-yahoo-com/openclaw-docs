---
summary: "iMessage via BlueBubbles macOS server (REST send/receive, typing, reactions, pairing, advanced actions)."
read_when:
  - Setting up BlueBubbles channel
  - Troubleshooting webhook pairing
  - Configuring iMessage on macOS
title: "BlueBubbles"
---

# BlueBubbles (macOS REST)

Status: bundled plugin that talks to the BlueBubbles macOS server over HTTP. **Recommended for iMessage integration** due to its richer API and easier setup compared to the legacy imsg channel.

## Overview

- Runs on macOS via the BlueBubbles helper app ([bluebubbles.app](https://bluebubbles.app)).
- Recommended/tested: macOS Sequoia (15). macOS Tahoe (26) works; edit is currently broken on Tahoe, and group icon updates may report success but not sync.
- OpenClaw talks to it through its REST API (`GET /api/v1/ping`, `POST /message/text`, `POST /chat/:id/*`).
- Incoming messages arrive via webhooks; outgoing replies, typing indicators, read receipts, and tapbacks are REST calls.
- Attachments and stickers are ingested as inbound media (and surfaced to the agent when possible).
- Pairing/allowlist works the same way as other channels (`/channels/pairing` etc) with `channels.bluebubbles.allowFrom` + pairing codes.
- Reactions are surfaced as system events just like Slack/Telegram so agents can "mention" them before replying.
- Advanced features: edit, unsend, reply threading, message effects, group management.

## Quick start

1. Install the BlueBubbles server on your Mac (follow the instructions at [bluebubbles.app/install](https://bluebubbles.app/install)).

2. In the BlueBubbles config, enable the web API and set a password.

3. Run `openclaw onboard` and select BlueBubbles, or configure manually:

   ```json5
   {
     channels: {
       bluebubbles: {
         enabled: true,
         serverUrl: "http://192.168.1.100:1234",
         password: "example-password",
         webhookPath: "/bluebubbles-webhook",
       },
     },
   }
   ```

4. Point BlueBubbles webhooks to your gateway (example: `https://your-gateway-host:3000/bluebubbles-webhook?password=<password>`).

5. Start the gateway; it will register the webhook handler and start pairing.

## Keeping Messages.app alive (VM / headless setups)

Some macOS VM / always-on setups can end up with Messages.app going “idle” (incoming events stop until the app is opened/foregrounded). A simple workaround is to **poke Messages every 5 minutes** using an AppleScript + LaunchAgent.

### 1. Save the AppleScript

Save this as:

- `~/Scripts/poke-messages.scpt`

Example script (non-interactive; does not steal focus):

```applescript
try
  tell application "Messages"
    if not running then
      launch
    end if

    -- Touch the scripting interface to keep the process responsive.
    set _chatCount to (count of chats)
  end tell
on error
  -- Ignore transient failures (first-run prompts, locked session, etc).
end try
```

### 2. Install a LaunchAgent

Save this as:

- `~/Library/LaunchAgents/com.user.poke-messages.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>com.user.poke-messages</string>

    <key>ProgramArguments</key>
    <array>
      <string>/bin/bash</string>
      <string>-lc</string>
      <string>/usr/bin/osascript &quot;$HOME/Scripts/poke-messages.scpt&quot;</string>
    </array>

    <key>RunAtLoad</key>
    <true/>

    <key>StartInterval</key>
    <integer>300</integer>

    <key>StandardOutPath</key>
    <string>/tmp/poke-messages.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/poke-messages.err</string>
  </dict>
</plist>
```

Notes:

- This runs **every 300 seconds** and **on login**.
- The first run may trigger macOS **Automation** prompts (`osascript` → Messages). Approve them in the same user session that runs the LaunchAgent.

Load it:

```bash
launchctl unload ~/Library/LaunchAgents/com.user.poke-messages.plist 2>/dev/null || true
launchctl load ~/Library/LaunchAgents/com.user.poke-messages.plist
```

## Onboarding

BlueBubbles is available in the interactive setup wizard:

```
openclaw onboard
```

The wizard prompts for:

- **Server URL** (required): BlueBubbles server address (e.g., `http://192.168.1.100:1234`)
- **Password** (required): API password from BlueBubbles Server settings
- **Webhook path** (optional): Defaults to `/bluebubbles-webhook`
- **DM policy**: pairing, allowlist, open, or disabled
- **Allow list**: Phone numbers, emails, or chat targets

You can also add BlueBubbles via CLI:

```
openclaw channels add bluebubbles --http-url http://192.168.1.100:1234 --password <password>
```

## Access control (DMs + groups)

DMs:

- Default: `channels.bluebubbles.dmPolicy = "pairing"`.
- Unknown senders receive a pairing code; messages are ignored until approved (codes expire after 1 hour).
- Approve via:
  - `openclaw pairing list bluebubbles`
  - `openclaw pairing approve bluebubbles <CODE>`
- Pairing is the default token exchange. Details: [Pairing](/channels/pairing)

Groups:

- `channels.bluebubbles.groupPolicy = open | allowlist | disabled` (default: `allowlist`).
- `channels.bluebubbles.groupAllowFrom` controls who can trigger in groups when `allowlist` is set.

### Mention gating (groups)

BlueBubbles supports mention gating for group chats, matching iMessage/WhatsApp behavior:

- Uses `agents.list[].groupChat.mentionPatterns` (or `messages.groupChat.mentionPatterns`) to detect mentions.
- When `requireMention` is enabled for a group, the agent only responds when mentioned.
- Control commands from authorized senders bypass mention gating.

Per-group configuration:

```json5
{
  channels: {
    bluebubbles: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15555550123"],
      groups: {
        "*": { requireMention: true }, // default for all groups
        "iMessage;-;chat123": { requireMention: false }, // override for specific group
      },
    },
  },
}
```

### Command gating

- Control commands (e.g., `/config`, `/model`) require authorization.
- Uses `allowFrom` and `groupAllowFrom` to determine command authorization.
- Authorized senders can run control commands even without mentioning in groups.

## Typing + read receipts

- **Typing indicators**: Sent automatically before and during response generation.
- **Read receipts**: Controlled by `channels.bluebubbles.sendReadReceipts` (default: `true`).
- **Typing indicators**: OpenClaw sends typing start events; BlueBubbles clears typing automatically on send or timeout (manual stop via DELETE is unreliable).

```json5
{
  channels: {
    bluebubbles: {
      sendReadReceipts: false, // disable read receipts
    },
  },
}
```

## Advanced actions

BlueBubbles supports advanced message actions when enabled in config:

```json5
{
  channels: {
    bluebubbles: {
      actions: {
        reactions: true, // tapbacks (default: true)
        edit: true, // edit sent messages (macOS 13+, broken on macOS 26 Tahoe)
        unsend: true, // unsend messages (macOS 13+)
        reply: true, // reply threading by message GUID
        sendWithEffect: true, // message effects (slam, loud, etc.)
        renameGroup: true, // rename group chats
        setGroupIcon: true, // set group chat icon/photo (flaky on macOS 26 Tahoe)
        addParticipant: true, // add participants to groups
        removeParticipant: true, // remove participants from groups
        leaveGroup: true, // leave group chats
        sendAttachment: true, // send attachments/media
      },
    },
  },
}
```

Available actions:

- **react**: Add/remove tapback reactions (`messageId`, `emoji`, `remove`)
- **edit**: Edit a sent message (`messageId`, `text`)
- **unsend**: Unsend a message (`messageId`)
- **reply**: Reply to a specific message (`messageId`, `text`, `to`)
- **sendWithEffect**: Send with iMessage effect (`text`, `to`, `effectId`)
- **renameGroup**: Rename a group chat (`chatGuid`, `displayName`)
- **setGroupIcon**: Set a group chat's icon/photo (`chatGuid`, `media`) — flaky on macOS 26 Tahoe (API may return success but the icon does not sync).
- **addParticipant**: Add someone to a group (`chatGuid`, `address`)
- **removeParticipant**: Remove someone from a group (`chatGuid`, `address`)
- 25. **leaveGroup**: Guruh chatini tark etish (`chatGuid`)
- **sendAttachment**: Send media/files (`to`, `buffer`, `filename`, `asVoice`)
  - Voice memos: set `asVoice: true` with **MP3** or **CAF** audio to send as an iMessage voice message. BlueBubbles converts MP3 → CAF when sending voice memos.

### Message IDs (short vs full)

OpenClaw may surface _short_ message IDs (e.g., `1`, `2`) to save tokens.

- `MessageSid` / `ReplyToId` can be short IDs.
- `MessageSidFull` / `ReplyToIdFull` contain the provider full IDs.
- Short IDs are in-memory; they can expire on restart or cache eviction.
- Actions accept short or full `messageId`, but short IDs will error if no longer available.

Use full IDs for durable automations and storage:

- Templates: `{{MessageSidFull}}`, `{{ReplyToIdFull}}`
- Context: `MessageSidFull` / `ReplyToIdFull` in inbound payloads

See [Configuration](/gateway/configuration) for template variables.

## Block streaming

Control whether responses are sent as a single message or streamed in blocks:

```json5
{
  channels: {
    bluebubbles: {
      blockStreaming: true, // enable block streaming (off by default)
    },
  },
}
```

## Media + limits

- Inbound attachments are downloaded and stored in the media cache.
- Media cap via `channels.bluebubbles.mediaMaxMb` (default: 8 MB).
- Outbound text is chunked to `channels.bluebubbles.textChunkLimit` (default: 4000 chars).

## Configuration reference

Full configuration: [Configuration](/gateway/configuration)

Provider options:

- `channels.bluebubbles.enabled`: Enable/disable the channel.
- `channels.bluebubbles.serverUrl`: BlueBubbles REST API base URL.
- `channels.bluebubbles.password`: API password.
- `channels.bluebubbles.webhookPath`: Webhook endpoint path (default: `/bluebubbles-webhook`).
- `channels.bluebubbles.dmPolicy`: `pairing | allowlist | open | disabled` (default: `pairing`).
- `channels.bluebubbles.allowFrom`: DM allowlist (handles, emails, E.164 numbers, `chat_id:*`, `chat_guid:*`).
- `channels.bluebubbles.groupPolicy`: `open | allowlist | disabled` (default: `allowlist`).
- `channels.bluebubbles.groupAllowFrom`: Group sender allowlist.
- `channels.bluebubbles.groups`: Per-group config (`requireMention`, etc.).
- `channels.bluebubbles.sendReadReceipts`: Send read receipts (default: `true`).
- `channels.bluebubbles.blockStreaming`: Enable block streaming (default: `false`; required for streaming replies).
- `channels.bluebubbles.textChunkLimit`: Chiquvchi bo‘lak hajmi (belgilar soni bo‘yicha) (standart: 4000).
- `channels.bluebubbles.chunkMode`: `length` (standart) faqat `textChunkLimit` oshirilganda bo‘ladi; `newline` esa uzunlik bo‘yicha bo‘lishdan oldin bo‘sh qatorlar (paragraf chegaralari) bo‘yicha bo‘ladi.
- `channels.bluebubbles.mediaMaxMb`: Kiruvchi media uchun MB dagi maksimal limit (standart: 8).
- `channels.bluebubbles.historyLimit`: Kontekst uchun maksimal guruh xabarlari (0 — o‘chiriladi).
- `channels.bluebubbles.dmHistoryLimit`: DM tarix limiti.
- `channels.bluebubbles.actions`: Muayyan amallarni yoqish/o‘chirish.
- `channels.bluebubbles.accounts`: Ko‘p akkauntli konfiguratsiya.

Bog‘liq global sozlamalar:

- `agents.list[].groupChat.mentionPatterns` (yoki `messages.groupChat.mentionPatterns`).
- `messages.responsePrefix`.

## Manzillash / yetkazib berish nishonlari

Barqaror marshrutlash uchun `chat_guid` ni afzal ko‘ring:

- `chat_guid:iMessage;-;+15555550123` (guruhlar uchun afzal).
- `chat_id:123`
- `chat_identifier:...`
- To‘g‘ridan-to‘g‘ri identifikatorlar: `+15555550123`, `user@example.com`
  - Agar to‘g‘ridan-to‘g‘ri identifikator uchun mavjud DM chat bo‘lmasa, OpenClaw uni `POST /api/v1/chat/new` orqali yaratadi. Buning uchun BlueBubbles Private API yoqilgan bo‘lishi kerak.

## Xavfsizlik

- Webhook so‘rovlari `guid`/`password` query parametrlari yoki sarlavhalarini `channels.bluebubbles.password` bilan solishtirish orqali autentifikatsiya qilinadi. `localhost` dan kelgan so‘rovlar ham qabul qilinadi.
- API paroli va webhook endpointini maxfiy saqlang (ularni hisob ma’lumotlari kabi ko‘ring).
- Localhost ishonchi bir xil xostdagi reverse proxy parolni bilmasdan aylanib o‘tishiga olib kelishi mumkin. Agar gateway’ni proksi qilsangiz, proksida autentifikatsiyani talab qiling va `gateway.trustedProxies` ni sozlang. [Gateway security](/gateway/security#reverse-proxy-configuration) ga qarang.
- Agar BlueBubbles serverini LAN tashqarisiga ochsangiz, HTTPS va firewall qoidalarini yoqing.

## Nosozliklarni bartaraf etish

- Agar yozish/o‘qilgan hodisalari ishlamay qolsa, BlueBubbles webhook loglarini tekshiring va gateway yo‘li `channels.bluebubbles.webhookPath` bilan mos kelishini tasdiqlang.
- Juftlash kodlari bir soatdan keyin muddati tugaydi; `openclaw pairing list bluebubbles` va `openclaw pairing approve bluebubbles <code>` dan foydalaning.
- Reaksiyalar BlueBubbles private API’ni talab qiladi (`POST /api/v1/message/react`); server versiyasi uni taqdim etishini tekshiring.
- Tahrirlash/o‘chirish macOS 13+ va mos BlueBubbles server versiyasini talab qiladi. macOS 26 (Tahoe) da tahrirlash hozircha private API o‘zgarishlari sababli ishlamaydi.
- Guruh ikonkasini yangilash macOS 26 (Tahoe) da beqaror bo‘lishi mumkin: API muvaffaqiyat qaytarishi mumkin, ammo yangi ikonka sinxronlanmaydi.
- OpenClaw BlueBubbles serverining macOS versiyasiga qarab ma’lum buzilgan amallarni avtomatik yashiradi. Agar macOS 26 (Tahoe) da tahrirlash hanuz ko‘rinsa, uni `channels.bluebubbles.actions.edit=false` bilan qo‘lda o‘chiring.
- Holat/sog‘liq ma’lumotlari uchun: `openclaw status --all` yoki `openclaw status --deep`.

Kanal ish jarayoni bo‘yicha umumiy ma’lumot uchun [Channels](/channels) va [Plugins](/tools/plugin) qo‘llanmasiga qarang.
