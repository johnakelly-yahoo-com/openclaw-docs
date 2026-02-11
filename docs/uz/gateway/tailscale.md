---
summary: "Tailnet yoki ommaviy dashboard kirishini avtomatlashtirish"
read_when:
  - 10. Gateway Control UI’ni localhost’dan tashqarida ochish
  - Tailscale (Gateway dashboard)
title: "OpenClaw Gateway dashboard’i va WebSocket porti uchun Tailscale **Serve** (tailnet) yoki **Funnel** (ommaviy) ni avtomatik sozlashi mumkin."
---

Bu Gateway’ni loopback’ga bog‘langan holda saqlaydi,
Tailscale esa HTTPS, marshrutlash va (Serve uchun) identifikatsiya header’larini ta’minlaydi.
================================================================================================================================

Rejimlar `serve`: `tailscale serve` orqali faqat tailnet uchun Serve.

## Gateway `127.0.0.1` da qoladi.

- `funnel`: `tailscale funnel` orqali ommaviy HTTPS. OpenClaw umumiy parolni talab qiladi.
- `off`: Sukut bo‘yicha (Tailscale avtomatlashtirilmagan). Autentifikatsiya
- Handshake’ni boshqarish uchun `gateway.auth.mode` ni sozlang:

## `token` (`OPENCLAW_GATEWAY_TOKEN` o‘rnatilgan bo‘lsa, sukut bo‘yicha)

`password` (`OPENCLAW_GATEWAY_PASSWORD` yoki konfiguratsiya orqali umumiy sir)

- `tailscale.mode = "serve"` va `gateway.auth.allowTailscale` `true` bo‘lganda,
  yaroqli Serve proxy so‘rovlari token/parol taqdim etmasdan
  Tailscale identifikatsiya header’lari (`tailscale-user-login`) orqali autentifikatsiya qilinishi mumkin.
- OpenClaw identifikatsiyani `x-forwarded-for` manzilini lokal Tailscale daemon’i
  (`tailscale whois`) orqali aniqlab va uni header bilan moslashtirib, qabul qilishdan oldin tekshiradi.

OpenClaw so‘rovni faqat loopback’dan kelib,
Tailscale’ning `x-forwarded-for`, `x-forwarded-proto` va `x-forwarded-host`
header’lari mavjud bo‘lsa Serve deb hisoblaydi. Aniq credential’larni talab qilish uchun `gateway.auth.allowTailscale: false` ni o‘rnating yoki
`gateway.auth.mode: "password"` ni majburiy qiling.
Konfiguratsiya misollari
Faqat tailnet (Serve)

{
gateway: {
bind: "loopback",
tailscale: { mode: "serve" },
},
}
-

### Ochish: `https://<magicdns>/` (yoki sozlangan `gateway.controlUi.basePath`)

```json5
{
  gateway: {
    bind: "loopback",
    tailscale: { mode: "serve" },
  },
}
```

Open: `https://<magicdns>/` (or your configured `gateway.controlUi.basePath`)

### Faqat Tailnet (Tailnet IP’ga bog‘lash)

Gateway’ni to‘g‘ridan-to‘g‘ri Tailnet IP’da tinglashi uchun ishlating (Serve/Funnel yo‘q).

```json5
{
  gateway: {
    bind: "tailnet",
    auth: { mode: "token", token: "your-token" },
  },
}
```

Boshqa Tailnet qurilmasidan ulaning:

- Boshqaruv UI: `http://<tailscale-ip>:18789/`
- WebSocket: `ws://<tailscale-ip>:18789`

Eslatma: loopback (`http://127.0.0.1:18789`) bu rejimda **ishlamaydi**.

### Ochiq internet (Funnel + umumiy parol)

```json5
{
  gateway: {
    bind: "loopback",
    tailscale: { mode: "funnel" },
    auth: { mode: "password", password: "replace-me" },
  },
}
```

Parolni diskka yozib qo‘yishdan ko‘ra `OPENCLAW_GATEWAY_PASSWORD` dan foydalanishni afzal ko‘ring.

## CLI misollar

```bash
openclaw gateway --tailscale serve
openclaw gateway --tailscale funnel --auth password
```

## Eslatmalar

- Tailscale Serve/Funnel ishlashi uchun `tailscale` CLI o‘rnatilgan va tizimga kirilgan bo‘lishi kerak.
- `tailscale.mode: "funnel"` auth rejimi `password` bo‘lmasa, ochiq ekspozitsiyani oldini olish uchun ishga tushmaydi.
- Agar OpenClaw yopilishda `tailscale serve`
  yoki `tailscale funnel` sozlamalarini bekor qilishi kerak bo‘lsa, `gateway.tailscale.resetOnExit` ni sozlang.
- `gateway.bind: "tailnet"` — to‘g‘ridan-to‘g‘ri Tailnet’ga bog‘lash (HTTPS yo‘q, Serve/Funnel yo‘q).
- `gateway.bind: "auto"` loopback’ni afzal ko‘radi; faqat Tailnet bo‘lsin desangiz `tailnet` dan foydalaning.
- Serve/Funnel faqat **Gateway boshqaruv UI + WS** ni ochib beradi. Tugunlar (nodes) bir xil Gateway WS endpoint orqali ulanadi, shuning uchun Serve tugunlarga kirish uchun ham ishlashi mumkin.

## Brauzer boshqaruvi (masofaviy Gateway + lokal brauzer)

Agar Gateway’ni bitta mashinada ishga tushirib, brauzerni boshqa mashinada boshqarmoqchi bo‘lsangiz,
brauzer joylashgan mashinada **node host** ni ishga tushiring va ikkisini ham bir xil tailnet’da saqlang.
Gateway brauzer harakatlarini tugunga proksi qiladi; alohida boshqaruv serveri yoki Serve URL kerak emas.

Brauzer boshqaruvi uchun Funnel’dan qoching; tugun juftlashuvini operator kirishi kabi ko‘ring.

## Tailscale talablar + cheklovlar

- Serve tailnet’ingizda HTTPS yoqilgan bo‘lishini talab qiladi; agar yo‘q bo‘lsa, CLI ogohlantiradi.
- Serve Tailscale identifikatsiya sarlavhalarini qo‘shadi; Funnel esa qo‘shmaydi.
- Funnel uchun Tailscale v1.38.3+, MagicDNS, HTTPS yoqilgan bo‘lishi va funnel node atributi talab qilinadi.
- Funnel TLS orqali faqat `443`, `8443` va `10000` portlarini qo‘llab-quvvatlaydi.
- macOS’da Funnel ishlashi uchun ochiq manbali Tailscale ilovasi varianti talab qilinadi.

## Batafsil ma’lumot

- Tailscale Serve sharhi: [https://tailscale.com/kb/1312/serve](https://tailscale.com/kb/1312/serve)
- `tailscale serve` buyrug‘i: [https://tailscale.com/kb/1242/tailscale-serve](https://tailscale.com/kb/1242/tailscale-serve)
- Tailscale Funnel sharhi: [https://tailscale.com/kb/1223/tailscale-funnel](https://tailscale.com/kb/1223/tailscale-funnel)
- `tailscale funnel` buyrug‘i: [https://tailscale.com/kb/1311/tailscale-funnel](https://tailscale.com/kb/1311/tailscale-funnel)
