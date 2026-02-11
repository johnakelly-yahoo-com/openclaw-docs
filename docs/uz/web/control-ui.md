---
summary: "Browser-based control UI for the Gateway (chat, nodes, config)"
read_when:
  - You want to operate the Gateway from a browser
  - You want Tailnet access without SSH tunnels
title: "Control UI"
---

# Control UI (browser)

The Control UI is a small **Vite + Lit** single-page app served by the Gateway:

- default: `http://<host>:18789/`
- optional prefix: set `gateway.controlUi.basePath` (e.g. `/openclaw`)

It speaks **directly to the Gateway WebSocket** on the same port.

## Quick open (local)

If the Gateway is running on the same computer, open:

- [http://127.0.0.1:18789/](http://127.0.0.1:18789/) (or [http://localhost:18789/](http://localhost:18789/))

If the page fails to load, start the Gateway first: `openclaw gateway`.

Auth is supplied during the WebSocket handshake via:

- `connect.params.auth.token`
- `connect.params.auth.password`
  The dashboard settings panel lets you store a token; passwords are not persisted.
  The onboarding wizard generates a gateway token by default, so paste it here on first connect.

## Device pairing (first connection)

When you connect to the Control UI from a new browser or device, the Gateway
requires a **one-time pairing approval** — even if you're on the same Tailnet
with `gateway.auth.allowTailscale: true`. This is a security measure to prevent
unauthorized access.

**What you'll see:** "disconnected (1008): pairing required"

**To approve the device:**

```bash
# List pending requests
openclaw devices list

# Approve by request ID
openclaw devices approve <requestId>
```

Once approved, the device is remembered and won't require re-approval unless
you revoke it with `openclaw devices revoke --device <id> --role <role>`. See
[Devices CLI](/cli/devices) for token rotation and revocation.

**Notes:**

- 1. Mahalliy ulanishlar (`127.0.0.1`) avtomatik tasdiqlanadi.
- 2. Masofaviy ulanishlar (LAN, Tailnet va boshqalar) 3. aniq tasdiqlashni talab qiladi.
- Each browser profile generates a unique device ID, so switching browsers or
  clearing browser data will require re-pairing.

## 5. Nimalar qila oladi (bugun)

- Chat with the model via Gateway WS (`chat.history`, `chat.send`, `chat.abort`, `chat.inject`)
- 7. Chat’da tool chaqiruvlarini oqimda uzatish + jonli tool chiqish kartalari (agent hodisalari)
- 8. Kanallar: WhatsApp/Telegram/Discord/Slack + plagin kanallari (Mattermost va boshqalar) 9. holat + QR login + har bir kanal uchun sozlamalar (`channels.status`, `web.login.*`, `config.patch`)
- 10. Instansiyalar: mavjudlik ro‘yxati + yangilash (`system-presence`)
- Sessions: list + per-session thinking/verbose overrides (`sessions.list`, `sessions.patch`)
- Cron jobs: list/add/run/enable/disable + run history (`cron.*`)
- Skills: status, enable/disable, install, API key updates (`skills.*`)
- Nodes: list + caps (`node.list`)
- 15. Exec tasdiqlari: gateway yoki node allowlist’larini tahrirlash + `exec host=gateway/node` uchun siyosat so‘rash (`exec.approvals.*`)
- 16. Config: `~/.openclaw/openclaw.json` ni ko‘rish/tahrirlash (`config.get`, `config.set`)
- 17. Config: tekshiruv bilan qo‘llash + qayta ishga tushirish (`config.apply`) va oxirgi faol sessiyani uyg‘otish
- 18. Config yozuvlari bir vaqtning o‘zida tahrirlarni bosib ketmaslik uchun base-hash himoyasini o‘z ichiga oladi
- Config schema + form rendering (`config.schema`, including plugin + channel schemas); Raw JSON editor remains available
- Debug: status/health/models snapshots + event log + manual RPC calls (`status`, `health`, `models.list`)
- 21. Loglar: gateway fayl loglarini filtr/eksport bilan jonli kuzatish (`logs.tail`)
- 22. Yangilash: paket/git yangilashni ishga tushirish + qayta ishga tushirish (`update.run`) va qayta ishga tushirish hisobotini olish

23. Cron vazifalar paneli eslatmalari:

- 24. Izolyatsiyalangan vazifalar uchun yetkazib berish sukut bo‘yicha qisqa xulosa e’lon qilishga sozlangan. 25. Agar faqat ichki ishga tushirishlarni xohlasangiz, none’ga o‘zgartirishingiz mumkin.
- 26. Announce tanlanganda kanal/maqsad maydonlari paydo bo‘ladi.

## 27. Chat xatti-harakati

- 28. `chat.send` **bloklamaydi**: darhol `{ runId, status: "started" }` bilan tasdiqlaydi va javob `chat` hodisalari orqali oqimda keladi.
- 29. Xuddi shu `idempotencyKey` bilan qayta yuborish ish jarayonida `{ status: "in_flight" }`, yakunlangandan so‘ng esa `{ status: "ok" }` ni qaytaradi.
- 30. `chat.inject` sessiya transkriptiga assistent eslatmasini qo‘shadi va faqat UI yangilanishlari uchun `chat` hodisasini tarqatadi (agent ishga tushirilmaydi, kanalga yetkazilmaydi).
- 31. To‘xtatish:
  - 32. **Stop** tugmasini bosing ( `chat.abort` ni chaqiradi)
  - 33. `/stop` yozing (yoki `stop|esc|abort|wait|exit|interrupt`) — out-of-band bekor qilish uchun
  - 34. `chat.abort` `{ sessionKey }` ( `runId` siz) ni qo‘llab-quvvatlaydi va shu sessiya uchun barcha faol ishga tushirishlarni bekor qiladi

## 35. Tailnet orqali kirish (tavsiya etiladi)

### 36. Integratsiyalashgan Tailscale Serve (afzal)

37. Gateway’ni loopback’da qoldiring va Tailscale Serve orqali HTTPS bilan proksi qiling:

```bash
38. openclaw gateway --tailscale serve
```

39. Ochish:

- 40. `https://<magicdns>/` (yoki sozlangan `gateway.controlUi.basePath`)

41. Sukut bo‘yicha, Serve so‘rovlari `gateway.auth.allowTailscale` `true` bo‘lganda Tailscale identity header’lari (`tailscale-user-login`) orqali autentifikatsiyadan o‘ta oladi. 42. OpenClaw
    identifikatsiyani `x-forwarded-for` manzilini `tailscale whois` orqali aniqlab, header bilan moslashtirish orqali tekshiradi va faqat so‘rov loopback’ga Tailscale’ning `x-forwarded-*` header’lari bilan kelgandagina qabul qiladi. 43. Agar Serve trafigi uchun ham token/parol talab qilmoqchi bo‘lsangiz,
    `gateway.auth.allowTailscale: false` qilib qo‘ying (yoki `gateway.auth.mode: "password"` ni majburiy qiling).

### 44. Tailnet’ga bog‘lash + token

```bash
45. openclaw gateway --bind tailnet --token "$(openssl rand -hex 32)"
```

46. So‘ng oching:

- 47. `http://<tailscale-ip>:18789/` (yoki sozlangan `gateway.controlUi.basePath`)

48. Token’ni UI sozlamalariga joylang ( `connect.params.auth.token` sifatida yuboriladi).

## 49. Xavfsiz bo‘lmagan HTTP

50. Agar panelni oddiy HTTP orqali ochsangiz (`http://<lan-ip>` yoki `http://<tailscale-ip>`),
    brauzer **xavfsiz bo‘lmagan kontekst**da ishlaydi va WebCrypto’ni bloklaydi. By default,
    OpenClaw **blocks** Control UI connections without device identity.

**Recommended fix:** use HTTPS (Tailscale Serve) or open the UI locally:

- `https://<magicdns>/` (Serve)
- `http://127.0.0.1:18789/` (on the gateway host)

**Downgrade example (token-only over HTTP):**

```json5
{
  gateway: {
    controlUi: { allowInsecureAuth: true },
    bind: "tailnet",
    auth: { mode: "token", token: "replace-me" },
  },
}
```

This disables device identity + pairing for the Control UI (even on HTTPS). Use
only if you trust the network.

See [Tailscale](/gateway/tailscale) for HTTPS setup guidance.

## Building the UI

The Gateway serves static files from `dist/control-ui`. Build them with:

```bash
pnpm ui:build # auto-installs UI deps on first run
```

Optional absolute base (when you want fixed asset URLs):

```bash
OPENCLAW_CONTROL_UI_BASE_PATH=/openclaw/ pnpm ui:build
```

For local development (separate dev server):

```bash
pnpm ui:dev # auto-installs UI deps on first run
```

Then point the UI at your Gateway WS URL (e.g. `ws://127.0.0.1:18789`).

## Debugging/testing: dev server + remote Gateway

The Control UI is static files; the WebSocket target is configurable and can be
different from the HTTP origin. This is handy when you want the Vite dev server
locally but the Gateway runs elsewhere.

1. Start the UI dev server: `pnpm ui:dev`
2. Open a URL like:

```text
http://localhost:5173/?gatewayUrl=ws://<gateway-host>:18789
```

Optional one-time auth (if needed):

```text
http://localhost:5173/?gatewayUrl=wss://<gateway-host>:18789&token=<gateway-token>
```

Notes:

- `gatewayUrl` is stored in localStorage after load and removed from the URL.
- `token` is stored in localStorage; `password` is kept in memory only.
- When `gatewayUrl` is set, the UI does not fall back to config or environment credentials.
  Provide `token` (or `password`) explicitly. Missing explicit credentials is an error.
- Use `wss://` when the Gateway is behind TLS (Tailscale Serve, HTTPS proxy, etc.).
- `gatewayUrl` is only accepted in a top-level window (not embedded) to prevent clickjacking.
- For cross-origin dev setups (e.g. `pnpm ui:dev` to a remote Gateway), add the UI
  origin to `gateway.controlUi.allowedOrigins`.

Example:

```json5
{
  gateway: {
    controlUi: {
      allowedOrigins: ["http://localhost:5173"],
    },
  },
}
```

Remote access setup details: [Remote access](/gateway/remote).
