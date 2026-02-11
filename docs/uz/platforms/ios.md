---
summary: "iOS node ilovasi: Gateway’ga ulanish, pairing, canvas va muammolarni bartaraf etish"
read_when:
  - iOS node’ni pairing qilish yoki qayta ulash
  - iOS ilovasini manbadan ishga tushirish
  - Gateway’ni aniqlash yoki canvas buyruqlarini disk raskadrovka qilish
title: "iOS ilova"
---

# iOS ilova (Node)

Mavjudligi: ichki preview. iOS ilovasi hali ommaga tarqatilmagan.

## Nima qiladi

- Gateway’ga WebSocket orqali ulanadi (LAN yoki tailnet).
- Node imkoniyatlarini ochadi: Canvas, Screen snapshot, Camera capture, Location, Talk mode, Voice wake.
- `node.invoke` buyruqlarini qabul qiladi va node holati hodisalarini xabar qiladi.

## Talablar

- Gateway boshqa qurilmada ishlayotgan bo‘lishi kerak (macOS, Linux yoki WSL2 orqali Windows).
- Tarmoq yo‘li:
  - Bonjour orqali bir xil LAN, **yoki**
  - Unicast DNS-SD orqali tailnet (misol domen: `openclaw.internal.`), **yoki**
  - Qo‘lda host/port (zaxira variant).

## Tezkor boshlash (pair + connect)

1. Gateway’ni ishga tushiring:

```bash
openclaw gateway --port 18789
```

2. iOS ilovasida Settings’ni oching va aniqlangan gateway’ni tanlang (yoki Manual Host’ni yoqing va host/port kiriting).

3. Gateway joylashgan hostda pairing so‘rovini tasdiqlang:

```bash
openclaw nodes pending
openclaw nodes approve <requestId>
```

4. Ulanishni tekshirish:

```bash
openclaw nodes status
openclaw gateway call node.list --params "{}"
```

## Aniqlash yo‘llari

### Bonjour (LAN)

Gateway `local.` da `_openclaw-gw._tcp` ni e’lon qiladi. iOS ilovasi bularni avtomatik ravishda ro‘yxatlaydi.

### Tailnet (tarmoqlararo)

Agar mDNS bloklangan bo‘lsa, unicast DNS-SD zonadan foydalaning (domen tanlang; misol: `openclaw.internal.`) va Tailscale split DNS.
[Bonjour](/gateway/bonjour) sahifasida CoreDNS misolini ko‘ring.

### Qo‘lda host/port

Settings’da **Manual Host** ni yoqing va gateway host + portini kiriting (standart `18789`).

## Canvas + A2UI

iOS node WKWebView canvas’ni render qiladi. Uni boshqarish uchun `node.invoke` dan foydalaning:

```bash
openclaw nodes invoke --node "iOS Node" --command canvas.navigate --params '{"url":"http://<gateway-host>:18793/__openclaw__/canvas/"}'
```

Eslatmalar:

- Gateway canvas host’i `/__openclaw__/canvas/` va `/__openclaw__/a2ui/` ni xizmat qiladi.
- iOS node canvas host URL reklama qilinganda ulanishda avtomatik ravishda A2UI’ga o‘tadi.
- `canvas.navigate` va `{"url":""}` bilan ichki scaffold’ga qayting.

### Canvas eval / snapshot

```bash
openclaw nodes invoke --node "iOS Node" --command canvas.eval --params '{"javaScript":"(() => { const {ctx} = window.__openclaw; ctx.clearRect(0,0,innerWidth,innerHeight); ctx.lineWidth=6; ctx.strokeStyle=\"#ff2d55\"; ctx.beginPath(); ctx.moveTo(40,40); ctx.lineTo(innerWidth-40, innerHeight-40); ctx.stroke(); return \"ok\"; })()"}'
```

```bash
openclaw nodes invoke --node "iOS Node" --command canvas.snapshot --params '{"maxWidth":900,"format":"jpeg"}'
```

## Voice wake + talk mode

- Voice wake va talk mode Settings’da mavjud.
- iOS fon audioni to‘xtatib qo‘yishi mumkin; ilova faol bo‘lmaganda ovozli funksiyalarni best-effort sifatida ko‘ring.

## Keng tarqalgan xatolar

- `NODE_BACKGROUND_UNAVAILABLE`: iOS ilovasini oldingi rejimga olib chiqing (canvas/kamera/ekran buyruqlari bunga muhtoj).
- `A2UI_HOST_NOT_CONFIGURED`: Gateway canvas host URL’ini e’lon qilmagan; [Gateway configuration](/gateway/configuration) dagi `canvasHost` ni tekshiring.
- Juftlash oynasi hech qachon chiqmaydi: `openclaw nodes pending` ni ishga tushiring va qo‘lda tasdiqlang.
- Qayta o‘rnatgandan keyin qayta ulanish ishlamaydi: Keychain’dagi juftlash tokeni tozalangan; nodeni qayta juftlang.

## Tegishli hujjatlar

- [Pairing](/gateway/pairing)
- [Discovery](/gateway/discovery)
- [Bonjour](/gateway/bonjour)
