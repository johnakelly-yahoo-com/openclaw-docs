---
summary: "20. Matrix qo‘llab-quvvatlash holati, imkoniyatlar va konfiguratsiya"
read_when:
  - 21. Matrix kanal imkoniyatlari ustida ish olib borilmoqda
title: "22. Matrix"
---

# 23. Matrix (plagin)

24. Matrix — ochiq, markazlashtirilmagan xabar almashish protokoli. 25. OpenClaw Matrix **foydalanuvchisi** sifatida istalgan homeserverda ulanadi, shuning uchun bot uchun Matrix hisobi kerak. 26. Tizimga kirgach, botga bevosita DM yuborishingiz yoki uni xonalarga (Matrix "guruhlar") taklif qilishingiz mumkin. 27. Beeper ham yaroqli mijoz variantidir, ammo u E2EE yoqilgan bo‘lishini talab qiladi.

28. Holat: plagin orqali qo‘llab-quvvatlanadi (@vector-im/matrix-bot-sdk). 29. To‘g‘ridan-to‘g‘ri xabarlar, xonalar, mavzular (threads), media, reaksiyalar, so‘rovlar (yuborish + poll-start matn sifatida), joylashuv va E2EE (kriptografik qo‘llab-quvvatlash bilan).

## 30. Plagin talab qilinadi

31. Matrix plagin sifatida yetkazib beriladi va asosiy o‘rnatmaga kiritilmagan.

32. CLI orqali o‘rnating (npm registri):

```bash
33. openclaw plugins install @openclaw/matrix
```

34. Lokal checkout (git repodan ishga tushirilganda):

```bash
35. openclaw plugins install ./extensions/matrix
```

36. Agar konfiguratsiya/onboarding vaqtida Matrix’ni tanlasangiz va git checkout aniqlansa, OpenClaw lokal o‘rnatish yo‘lini avtomatik taklif qiladi.

37. Tafsilotlar: [Plugins](/tools/plugin)

## 38. Sozlash

1. 39. Matrix plaginini o‘rnating:
   - 40. npm’dan: `openclaw plugins install @openclaw/matrix`
   - 41. Lokal checkout’dan: `openclaw plugins install ./extensions/matrix`

2. 42. Homeserverda Matrix hisobini yarating:
   - 43. Hosting variantlarini ko‘rib chiqing: [https://matrix.org/ecosystem/hosting/](https://matrix.org/ecosystem/hosting/)
   - 44. Yoki uni o‘zingiz joylashtiring.

3. 45. Bot hisobi uchun access token oling:

   - 46. O‘z homeserveringizda `curl` orqali Matrix login API’dan foydalaning:

   ```bash
   47. curl --request POST \
     --url https://matrix.example.org/_matrix/client/v3/login \
     --header 'Content-Type: application/json' \
     --data '{
     "type": "m.login.password",
     "identifier": {
       "type": "m.id.user",
       "user": "your-user-name"
     },
     "password": "your-password"
   }'
   ```

   - 48. `matrix.example.org` ni homeserver URL’ingiz bilan almashtiring.
   - 49. Yoki `channels.matrix.userId` + `channels.matrix.password` ni sozlang: OpenClaw xuddi shu login endpoint’ini chaqiradi, access token’ni `~/.openclaw/credentials/matrix/credentials.json` ga saqlaydi va keyingi ishga tushirishda undan qayta foydalanadi.

4. 50. Hisob ma’lumotlarini sozlash:
   - Env: `MATRIX_HOMESERVER`, `MATRIX_ACCESS_TOKEN` (or `MATRIX_USER_ID` + `MATRIX_PASSWORD`)
   - Or config: `channels.matrix.*`
   - If both are set, config takes precedence.
   - With access token: user ID is fetched automatically via `/whoami`.
   - When set, `channels.matrix.userId` should be the full Matrix ID (example: `@bot:example.org`).

5. Restart the gateway (or finish onboarding).

6. Start a DM with the bot or invite it to a room from any Matrix client
   (Element, Beeper, etc.; see [https://matrix.org/ecosystem/clients/](https://matrix.org/ecosystem/clients/)). Beeper requires E2EE,
   so set `channels.matrix.encryption: true` and verify the device.

Minimal config (access token, user ID auto-fetched):

```json5
{
  channels: {
    matrix: {
      enabled: true,
      homeserver: "https://matrix.example.org",
      accessToken: "syt_***",
      dm: { policy: "pairing" },
    },
  },
}
```

E2EE config (end to end encryption enabled):

```json5
{
  channels: {
    matrix: {
      enabled: true,
      homeserver: "https://matrix.example.org",
      accessToken: "syt_***",
      encryption: true,
      dm: { policy: "pairing" },
    },
  },
}
```

## Encryption (E2EE)

End-to-end encryption is **supported** via the Rust crypto SDK.

Enable with `channels.matrix.encryption: true`:

- If the crypto module loads, encrypted rooms are decrypted automatically.
- Outbound media is encrypted when sending to encrypted rooms.
- On first connection, OpenClaw requests device verification from your other sessions.
- Verify the device in another Matrix client (Element, etc.) to enable key sharing.
- If the crypto module cannot be loaded, E2EE is disabled and encrypted rooms will not decrypt;
  OpenClaw logs a warning.
- If you see missing crypto module errors (for example, `@matrix-org/matrix-sdk-crypto-nodejs-*`),
  allow build scripts for `@matrix-org/matrix-sdk-crypto-nodejs` and run
  `pnpm rebuild @matrix-org/matrix-sdk-crypto-nodejs` or fetch the binary with
  `node node_modules/@matrix-org/matrix-sdk-crypto-nodejs/download-lib.js`.

Crypto state is stored per account + access token in
`~/.openclaw/matrix/accounts/<account>/<homeserver>__<user>/<token-hash>/crypto/`
(SQLite database). Sync state lives alongside it in `bot-storage.json`.
If the access token (device) changes, a new store is created and the bot must be
re-verified for encrypted rooms.

**Device verification:**
When E2EE is enabled, the bot will request verification from your other sessions on startup.
Open Element (or another client) and approve the verification request to establish trust.
Once verified, the bot can decrypt messages in encrypted rooms.

## Routing model

- Replies always go back to Matrix.
- DMs share the agent's main session; rooms map to group sessions.

## Access control (DMs)

- Default: `channels.matrix.dm.policy = "pairing"`. Unknown senders get a pairing code.
- Approve via:
  - `openclaw pairing list matrix`
  - `openclaw pairing approve matrix <CODE>`
- Public DMs: `channels.matrix.dm.policy="open"` plus `channels.matrix.dm.allowFrom=["*"]`.
- `channels.matrix.dm.allowFrom` accepts full Matrix user IDs (example: `@user:server`). The wizard resolves display names to user IDs when directory search finds a single exact match.

## Rooms (groups)

- Default: `channels.matrix.groupPolicy = "allowlist"` (mention-gated). Use `channels.defaults.groupPolicy` to override the default when unset.
- Allowlist rooms with `channels.matrix.groups` (room IDs or aliases; names are resolved to IDs when directory search finds a single exact match):

```json5
{
  channels: {
    matrix: {
      groupPolicy: "allowlist",
      groups: {
        "!roomId:example.org": { allow: true },
        "#alias:example.org": { allow: true },
      },
      groupAllowFrom: ["@owner:example.org"],
    },
  },
}
```

- `requireMention: false` enables auto-reply in that room.
- `groups."*"` can set defaults for mention gating across rooms.
- `groupAllowFrom` restricts which senders can trigger the bot in rooms (full Matrix user IDs).
- Per-room `users` allowlists can further restrict senders inside a specific room (use full Matrix user IDs).
- The configure wizard prompts for room allowlists (room IDs, aliases, or names) and resolves names only on an exact, unique match.
- 1. Ishga tushishda OpenClaw allowlistlardagi xona/foydalanuvchi nomlarini IDlarga moslaydi va moslikni logga yozadi; aniqlanmagan yozuvlar allowlist moslashtirishida e’tiborga olinmaydi.
- 2. Takliflar odatda avtomatik qo‘shiladi; `channels.matrix.autoJoin` va `channels.matrix.autoJoinAllowlist` orqali boshqariladi.
- 3. **Hech qanday xona**ga ruxsat bermaslik uchun `channels.matrix.groupPolicy: "disabled"` qilib qo‘ying (yoki allowlistni bo‘sh qoldiring).
- 4. Meros kalit: `channels.matrix.rooms` (`groups` bilan bir xil tuzilma).

## 5. Tredlar

- Reply threading is supported.
- 7. `channels.matrix.threadReplies` javoblar tredlarda qolishini boshqaradi:
  - `off`, `inbound` (default), `always`
- `channels.matrix.replyToMode` controls reply-to metadata when not replying in a thread:
  - 10. `off` (standart), `first`, `all`

## 11. Imkoniyatlar

| 12. Funksiya           | 13. Holat                                                                                                                                               |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 14. Shaxsiy xabarlar   | 15. ✅ Qo‘llab-quvvatlanadi                                                                                                                              |
| Rooms                                         | 17. ✅ Qo‘llab-quvvatlanadi                                                                                                                              |
| Threads                                       | 19. ✅ Qo‘llab-quvvatlanadi                                                                                                                              |
| 20. Media              | 21. ✅ Qo‘llab-quvvatlanadi                                                                                                                              |
| 22. E2EE               | 23. ✅ Qo‘llab-quvvatlanadi (kripto modul talab qilinadi)                                                                             |
| 24. Reaksiyalar        | 25. ✅ Qo‘llab-quvvatlanadi (vositalar orqali yuborish/o‘qish)                                                                        |
| 26. So‘rovnomalar      | 27. ✅ Yuborish qo‘llab-quvvatlanadi; kiruvchi so‘rovnoma boshlanishlari matnga aylantiriladi (javoblar/yakunlar e’tiborga olinmaydi) |
| 28. Joylashuv          | 29. ✅ Qo‘llab-quvvatlanadi (geo URI; balandlik e’tiborga olinmaydi)                                                                  |
| 30. Mahalliy buyruqlar | ✅ Supported                                                                                                                                                                    |

## 32. Nosozliklarni bartaraf etish

33. Avval ushbu ketma-ketlikni ishga tushiring:

```bash
34. openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
openclaw channels status --probe
```

35. So‘ng zarur bo‘lsa DM juftlash holatini tasdiqlang:

```bash
36. openclaw pairing list matrix
```

37. Keng tarqalgan xatolar:

- 38. Tizimga kirilgan, ammo xona xabarlari e’tiborsiz: xona `groupPolicy` yoki xona allowlisti tomonidan bloklangan.
- 39. DMlar e’tiborsiz: `channels.matrix.dm.policy="pairing"` bo‘lganda jo‘natuvchi tasdiqlanishni kutmoqda.
- 40. Shifrlangan xonalar ishlamaydi: kripto qo‘llab-quvvatlashi yoki shifrlash sozlamalari mos kelmaydi.

For triage flow: [/channels/troubleshooting](/channels/troubleshooting).

## 42. Konfiguratsiya ma’lumotnomasi (Matrix)

Full configuration: [Configuration](/gateway/configuration)

44. Provayder parametrlari:

- 45. `channels.matrix.enabled`: kanal ishga tushishini yoqish/o‘chirish.
- 46. `channels.matrix.homeserver`: homeserver URL manzili.
- 47. `channels.matrix.userId`: Matrix foydalanuvchi IDsi (access token bilan ixtiyoriy).
- 48. `channels.matrix.accessToken`: access token.
- 49. `channels.matrix.password`: tizimga kirish paroli (token saqlanadi).
- 50. `channels.matrix.deviceName`: qurilma ko‘rinadigan nomi.
- `channels.matrix.encryption`: enable E2EE (default: false).
- `channels.matrix.initialSyncLimit`: initial sync limit.
- `channels.matrix.threadReplies`: `off | inbound | always` (default: inbound).
- `channels.matrix.textChunkLimit`: outbound text chunk size (chars).
- `channels.matrix.chunkMode`: `length` (default) or `newline` to split on blank lines (paragraph boundaries) before length chunking.
- `channels.matrix.dm.policy`: `pairing | allowlist | open | disabled` (default: pairing).
- `channels.matrix.dm.allowFrom`: DM allowlist (full Matrix user IDs). `open` requires `"*"`. The wizard resolves names to IDs when possible.
- `channels.matrix.groupPolicy`: `allowlist | open | disabled` (default: allowlist).
- `channels.matrix.groupAllowFrom`: allowlisted senders for group messages (full Matrix user IDs).
- `channels.matrix.allowlistOnly`: force allowlist rules for DMs + rooms.
- `channels.matrix.groups`: group allowlist + per-room settings map.
- `channels.matrix.rooms`: legacy group allowlist/config.
- `channels.matrix.replyToMode`: reply-to mode for threads/tags.
- `channels.matrix.mediaMaxMb`: inbound/outbound media cap (MB).
- `channels.matrix.autoJoin`: invite handling (`always | allowlist | off`, default: always).
- `channels.matrix.autoJoinAllowlist`: allowed room IDs/aliases for auto-join.
- `channels.matrix.actions`: per-action tool gating (reactions/messages/pins/memberInfo/channelInfo).
