---
summary: "SSH orqali masofadagi OpenClaw gateway’ni boshqarish uchun macOS ilova oqimi"
read_when:
  - Masofaviy mac boshqaruvini sozlash yoki nosozliklarni tuzatish
title: "Masofadan boshqarish"
---

# Masofaviy OpenClaw (macOS ⇄ masofaviy host)

Ushbu oqim macOS ilovasiga boshqa hostda (desktop/server) ishlayotgan OpenClaw gateway uchun to‘liq masofaviy boshqaruv sifatida ishlash imkonini beradi. Bu ilovaning **Remote over SSH** (masofadan ishga tushirish) funksiyasidir. Barcha funksiyalar — sog‘liq tekshiruvlari, Voice Wake forwarding va Web Chat — _Settings → General_ dagi bir xil masofaviy SSH konfiguratsiyasidan foydalanadi.

## Rejimlar

- **Local (this Mac)**: Hammasi noutbukda ishlaydi. SSH ishlatilmaydi.
- **Remote over SSH (default)**: OpenClaw buyruqlari masofaviy hostda bajariladi. Mac ilova `-o BatchMode` bilan, tanlangan identifikatsiya/kalit va lokal port-forward bilan SSH ulanishini ochadi.
- **Remote direct (ws/wss)**: SSH tunneli yo‘q. Mac ilova gateway URL’iga to‘g‘ridan-to‘g‘ri ulanadi (masalan, Tailscale Serve yoki ommaviy HTTPS reverse proxy orqali).

## Masofaviy transportlar

Masofaviy rejim ikki xil transportni qo‘llab-quvvatlaydi:

- **SSH tunnel** (standart): Gateway portini localhost’ga yo‘naltirish uchun `ssh -N -L ...` dan foydalanadi. Tunnel loopback bo‘lgani uchun gateway node IP’ni `127.0.0.1` sifatida ko‘radi.
- **Direct (ws/wss)**: Gateway URL’iga bevosita ulanadi. Gateway haqiqiy mijoz IP’ni ko‘radi.

## Masofaviy hostdagi talablar

1. Node + pnpm ni o‘rnating va OpenClaw CLI’ni build/o‘rnating (`pnpm install && pnpm build && pnpm link --global`).
2. Interaktiv bo‘lmagan shelllar uchun `openclaw` PATH’da ekanini ta’minlang (zarur bo‘lsa `/usr/local/bin` yoki `/opt/homebrew/bin` ga symlink qiling).
3. Kalit autentifikatsiyasi bilan SSH’ni oching. LAN’dan tashqarida barqaror ulanish uchun **Tailscale** IP’larini tavsiya qilamiz.

## macOS ilovasini sozlash

1. Open _Settings → General_.
2. Under **OpenClaw runs**, pick **Remote over SSH** and set:
   - **Transport**: **SSH tunnel** or **Direct (ws/wss)**.
   - **SSH target**: `user@host` (optional `:port`).
     - If the gateway is on the same LAN and advertises Bonjour, pick it from the discovered list to auto-fill this field.
   - **Gateway URL** (Direct only): `wss://gateway.example.ts.net` (or `ws://...` for local/LAN).
   - **Identity file** (advanced): path to your key.
   - **Project root** (advanced): remote checkout path used for commands.
   - **CLI path** (advanced): optional path to a runnable `openclaw` entrypoint/binary (auto-filled when advertised).
3. Hit **Test remote**. Success indicates the remote `openclaw status --json` runs correctly. Failures usually mean PATH/CLI issues; exit 127 means the CLI isn’t found remotely.
4. Health checks and Web Chat will now run through this SSH tunnel automatically.

## Web Chat

- **SSH tunnel**: Web Chat connects to the gateway over the forwarded WebSocket control port (default 18789).
- **Direct (ws/wss)**: Web Chat connects straight to the configured gateway URL.
- There is no separate WebChat HTTP server anymore.

## Permissions

- The remote host needs the same TCC approvals as local (Automation, Accessibility, Screen Recording, Microphone, Speech Recognition, Notifications). Run onboarding on that machine to grant them once.
- Nodes advertise their permission state via `node.list` / `node.describe` so agents know what’s available.

## Security notes

- Prefer loopback binds on the remote host and connect via SSH or Tailscale.
- If you bind the Gateway to a non-loopback interface, require token/password auth.
- See [Security](/gateway/security) and [Tailscale](/gateway/tailscale).

## WhatsApp login flow (remote)

- Run `openclaw channels login --verbose` **on the remote host**. Scan the QR with WhatsApp on your phone.
- Re-run login on that host if auth expires. Health check will surface link problems.

## Troubleshooting

- **exit 127 / not found**: `openclaw` isn’t on PATH for non-login shells. Add it to `/etc/paths`, your shell rc, or symlink into `/usr/local/bin`/`/opt/homebrew/bin`.
- **Health probe failed**: check SSH reachability, PATH, and that Baileys is logged in (`openclaw status --json`).
- **Web Chat stuck**: confirm the gateway is running on the remote host and the forwarded port matches the gateway WS port; the UI requires a healthy WS connection.
- **Node IP shows 127.0.0.1**: expected with the SSH tunnel. Switch **Transport** to **Direct (ws/wss)** if you want the gateway to see the real client IP.
- **Voice Wake**: trigger phrases are forwarded automatically in remote mode; no separate forwarder is needed.

## Notification sounds

Pick sounds per notification from scripts with `openclaw` and `node.invoke`, e.g.:

```bash
openclaw nodes notify --node <id> --title "Ping" --body "Remote gateway ready" --sound Glass
```

There is no global “default sound” toggle in the app anymore; callers choose a sound (or none) per request.
