---
summary: "OpenClaw Gateway CLI (`openclaw gateway`) — run, query, and discover gateways"
read_when:
  - Running the Gateway from the CLI (dev or servers)
  - Debugging Gateway auth, bind modes, and connectivity
  - Discovering gateways via Bonjour (LAN + tailnet)
title: "gateway"
---

# Gateway CLI

The Gateway is OpenClaw’s WebSocket server (channels, nodes, sessions, hooks).

Subcommands in this page live under `openclaw gateway …`.

Related docs:

- [/gateway/bonjour](/gateway/bonjour)
- [/gateway/discovery](/gateway/discovery)
- [/gateway/configuration](/gateway/configuration)

## Run the Gateway

Run a local Gateway process:

```bash
openclaw gateway
```

Foreground alias:

```bash
openclaw gateway run
```

Notes:

- By default, the Gateway refuses to start unless `gateway.mode=local` is set in `~/.openclaw/openclaw.json`. Use `--allow-unconfigured` for ad-hoc/dev runs.
- Binding beyond loopback without auth is blocked (safety guardrail).
- `SIGUSR1` triggers an in-process restart when authorized (enable `commands.restart` or use the gateway tool/config apply/update).
- `SIGINT`/`SIGTERM` handlers stop the gateway process, but they don’t restore any custom terminal state. If you wrap the CLI with a TUI or raw-mode input, restore the terminal before exit.

### Options

- `--port <port>`: WebSocket port (default comes from config/env; usually `18789`).
- `--bind <loopback|lan|tailnet|auto|custom>`: listener bind mode.
- `--auth <token|password>`: auth mode override.
- `--token <token>`: token override (also sets `OPENCLAW_GATEWAY_TOKEN` for the process).
- `--password <password>`: password override (also sets `OPENCLAW_GATEWAY_PASSWORD` for the process).
- `--tailscale <off|serve|funnel>`: expose the Gateway via Tailscale.
- `--tailscale-reset-on-exit`: reset Tailscale serve/funnel config on shutdown.
- `--allow-unconfigured`: allow gateway start without `gateway.mode=local` in config.
- `--dev`: agar yo‘q bo‘lsa, dev config + workspace yaratadi (BOOTSTRAP.md o‘tkazib yuboriladi).
- `--reset`: dev config + hisob ma’lumotlari + sessiyalar + workspace’ni tiklaydi ( `--dev` talab qilinadi).
- `--force`: ishga tushirishdan oldin tanlangan portdagi mavjud tinglovchini majburan to‘xtatadi.
- `--verbose`: batafsil loglar.
- `--claude-cli-logs`: konsolda faqat claude-cli loglarini ko‘rsatadi (va uning stdout/stderr’ini yoqadi).
- `--ws-log <auto|full|compact>`: websocket log uslubi (standart `auto`).
- `--compact`: `--ws-log compact` uchun alias.
- `--raw-stream`: xom model stream hodisalarini jsonl formatida log qiladi.
- `--raw-stream-path <path>`: xom stream jsonl yo‘li.

## Ishlayotgan Gateway’ga so‘rov yuborish

Barcha so‘rov buyruqlari WebSocket RPC’dan foydalanadi.

Chiqish rejimlari:

- Standart: inson uchun o‘qilishi qulay (TTY’da rangli).
- `--json`: mashina uchun o‘qilishi qulay JSON (bezaksiz/spinnersiz).
- `--no-color` (yoki `NO_COLOR=1`): insoniy joylashuvni saqlagan holda ANSI’ni o‘chiradi.

Umumiy parametrlar (qo‘llab-quvvatlangan joylarda):

- `--url <url>`: Gateway WebSocket URL’i.
- `--token <token>`: Gateway tokeni.
- `--password <password>`: Gateway paroli.
- `--timeout <ms>`: timeout/budjet (buyruqqa qarab farq qiladi).
- `--expect-final`: “final” javobni kutadi (agent chaqiruvlari).

Eslatma: `--url` o‘rnatilganda, CLI konfiguratsiya yoki muhit credentiallariga qaytmaydi.
`--token` yoki `--password` ni aniq ko‘rsating. Aniq ko‘rsatilgan hisob ma’lumotlarining yo‘qligi xato hisoblanadi.

### `gateway health`

```bash
openclaw gateway health --url ws://127.0.0.1:18789
```

### `gateway status`

`gateway status` Gateway servisining holatini (launchd/systemd/schtasks) hamda ixtiyoriy RPC tekshiruvini ko‘rsatadi.

```bash
openclaw gateway status
openclaw gateway status --json
```

Parametrlar:

- `--url <url>`: probe URL’ini almashtiradi.
- `--token <token>`: probe uchun token autentifikatsiyasi.
- `--password <password>`: probe uchun parol autentifikatsiyasi.
- `--timeout <ms>`: probe timeout’i (standart `10000`).
- `--no-probe`: RPC probe’ni o‘tkazib yuboradi (faqat servis ko‘rinishi).
- `--deep`: tizim darajasidagi servislarni ham skanerlaydi.

### `gateway probe`

`gateway probe` — “hammasini debug qilish” buyrug‘i. U har doim tekshiradi:

- sozlangan masofaviy gateway’ni (agar o‘rnatilgan bo‘lsa), va
- localhost’ni (loopback) **masofaviy sozlangan bo‘lsa ham**.

Agar bir nechta gateway mavjud bo‘lsa, ularning barchasini chiqaradi. Izolyatsiyalangan profillar/portlardan foydalanganda (masalan, qutqaruv bot), bir nechta gateway qo‘llab-quvvatlanadi, ammo ko‘pchilik o‘rnatmalarda hali ham bitta gateway ishlaydi.

```bash
openclaw gateway probe
openclaw gateway probe --json
```

#### SSH orqali masofaviy (Mac ilovasi bilan moslik)

macOS ilovasidagi “Remote over SSH” rejimi lokal port-forward’dan foydalanadi, shunda masofaviy gateway (faqat loopback’ga bog‘langan bo‘lishi mumkin) `ws://127.0.0.1:<port>` orqali yetib boriladigan bo‘ladi.

CLI’dagi ekvivalenti:

```bash
openclaw gateway probe --ssh user@gateway-host
```

Parametrlar:

- `--ssh <target>`: `user@host` yoki `user@host:port` (port standart bo‘yicha `22`).
- 1. `--ssh-identity <path>`: identifikatsiya fayli.
- 2. `--ssh-auto`: aniqlangan birinchi shlyuz xostini SSH maqsadi sifatida tanlaydi (faqat LAN/WAB).

3. Konfiguratsiya (ixtiyoriy, sukut bo‘yicha qiymatlar sifatida ishlatiladi):

- 4. `gateway.remote.sshTarget`
- 5. `gateway.remote.sshIdentity`

### 6. `gateway call <method>`

7. Past darajadagi RPC yordamchisi.

```bash
8. openclaw gateway call status
openclaw gateway call logs.tail --params '{"sinceMs": 60000}'
```

## 9. Gateway xizmatini boshqarish

```bash
10. openclaw gateway install
openclaw gateway start
openclaw gateway stop
openclaw gateway restart
openclaw gateway uninstall
```

Notes:

- 12. `gateway install` `--port`, `--runtime`, `--token`, `--force`, `--json` ni qo‘llab-quvvatlaydi.
- 13. Hayotiy sikl buyruqlari skriptlash uchun `--json` ni qabul qiladi.

## 14. Shlyuzlarni aniqlash (Bonjour)

15. `gateway discover` Gateway mayoqchalarini (`_openclaw-gw._tcp`) qidiradi.

- Multicast DNS-SD: `local.`
- 17. Unicast DNS-SD (Wide-Area Bonjour): domenni tanlang (masalan: `openclaw.internal.`) va split DNS + DNS serverni sozlang; qarang [/gateway/bonjour](/gateway/bonjour)

18. Faqat Bonjour aniqlashi yoqilgan (sukut bo‘yicha) shlyuzlar mayoqchani e’lon qiladi.

19. Wide-Area aniqlash yozuvlari (TXT) quyidagilarni o‘z ichiga oladi:

- 20. `role` (shlyuz roli uchun ishora)
- 21. `transport` (transport ishorasi, masalan `gateway`)
- 22. `gatewayPort` (WebSocket porti, odatda `18789`)
- 23. `sshPort` (SSH porti; mavjud bo‘lmasa, sukut bo‘yicha `22`)
- 24. `tailnetDns` (mavjud bo‘lsa, MagicDNS xost nomi)
- 25. `gatewayTls` / `gatewayTlsSha256` (TLS yoqilgan + sertifikat barmoq izi)
- 26. `cliPath` (masofaviy o‘rnatishlar uchun ixtiyoriy ishora)

### 27. `gateway discover`

```bash
28. openclaw gateway discover
```

Options:

- `--timeout <ms>`: per-command timeout (browse/resolve); default `2000`.
- 31. `--json`: mashina o‘qiy oladigan chiqish (shuningdek, bezak/spinnerni o‘chiradi).

32. Misollar:

```bash
33. openclaw gateway discover --timeout 4000
openclaw gateway discover --json | jq '.beacons[].wsUrl'
```
