---
summary: "Android app (node): connection runbook + Canvas/Chat/Camera"
read_when:
  - Pairing or reconnecting the Android node
  - Debugging Android gateway discovery or auth
  - Verifying chat history parity across clients
title: "Android App"
---

# Android App (Node)

## Snapshotni qo‘llab-quvvatlash

- Rol: hamroh tugun ilovasi (Android Gateway’ni xost qilmaydi).
- Gateway talab qilinadi: ha (uni macOS, Linux yoki Windows’da WSL2 orqali ishga tushiring).
- O‘rnatish: [Getting Started](/start/getting-started) + [Pairing](/gateway/pairing).
- Gateway: [Runbook](/gateway) + [Configuration](/gateway/configuration).
  - Protokollar: [Gateway protocol](/gateway/protocol) (tugunlar + boshqaruv tekisligi).

## Tizim boshqaruvi

Tizim boshqaruvi (launchd/systemd) Gateway xostida joylashgan. Qarang: [Gateway](/gateway).

## Ulanish bo‘yicha Runbook

Android tugun ilovasi ⇄ (mDNS/NSD + WebSocket) ⇄ **Gateway**

Android to‘g‘ridan-to‘g‘ri Gateway WebSocket’iga ulanadi (standart `ws://<host>:18789`) va Gateway’ga tegishli pairing’dan foydalanadi.

### Talablar

- Gateway’ni “master” mashinada ishga tushirishingiz mumkin.
- Android qurilma/emulyator gateway WebSocket’iga yetib bora olishi kerak:
  - mDNS/NSD bilan bir xil LAN’da, **yoki**
  - Wide-Area Bonjour / unicast DNS-SD’dan foydalangan holda bir xil Tailscale tailnet’da (quyida qarang), **yoki**
  - Gateway xosti/portini qo‘lda kiritish (zaxira usul)
- CLI’ni (`openclaw`) gateway mashinasida (yoki SSH orqali) ishga tushira olishingiz mumkin.

### 1. Gateway’ni ishga tushiring

```bash
openclaw gateway --port 18789 --verbose
```

Loglarda quyidagiga o‘xshash yozuvni ko‘rganingizni tasdiqlang:

- `listening on ws://0.0.0.0:18789`

Faqat tailnet uchun sozlamalar (Vienna ⇄ London uchun tavsiya etiladi) da gateway’ni tailnet IP’iga bog‘lang:

- Gateway xostidagi `~/.openclaw/openclaw.json` faylida `gateway.bind: "tailnet"` ni o‘rnating.
- Gateway’ni / macOS menyu paneli ilovasini qayta ishga tushiring.

### 2. Discovery’ni tekshiring (ixtiyoriy)

Gateway mashinasidan:

```bash
dns-sd -B _openclaw-gw._tcp local.
```

Qo‘shimcha nosozliklarni aniqlash eslatmalari: [Bonjour](/gateway/bonjour).

#### Tailnet (Vienna ⇄ London) orqali unicast DNS-SD yordamida discovery

Android NSD/mDNS discovery tarmoqlar orasidan o‘tmaydi. Agar Android tuguningiz va gateway turli tarmoqlarda bo‘lsa, lekin Tailscale orqali ulangan bo‘lsa, Wide-Area Bonjour / unicast DNS-SD’dan foydalaning:

1. Gateway xostida DNS-SD zonani (masalan, `openclaw.internal.`) sozlang va `_openclaw-gw._tcp` yozuvlarini e’lon qiling.
2. Tanlangan domen uchun Tailscale split DNS’ni sozlab, uni o‘sha DNS serverga yo‘naltiring.

Batafsil ma’lumotlar va CoreDNS konfiguratsiyasi namunasi: [Bonjour](/gateway/bonjour).

### 3. Android’dan ulaning

Android ilovasida:

- Ilova gateway ulanishini **foreground service** (doimiy bildirishnoma) orqali faol holda saqlaydi.
- **Settings**’ni oching.
- **Discovered Gateways** bo‘limida gateway’ingizni tanlab, **Connect** ni bosing.
- Agar mDNS bloklangan bo‘lsa, **Advanced → Manual Gateway** (xost + port) dan foydalanib, **Connect (Manual)** ni bosing.

Birinchi muvaffaqiyatli pairing’dan so‘ng, Android ishga tushganda avtomatik qayta ulanadi:

- Agar yoqilgan bo‘lsa, qo‘lda kiritilgan endpoint, aks holda
- Oxirgi topilgan gateway (imkon qadar).

### 4. Pairing’ni tasdiqlang (CLI)

Gateway mashinasida:

```bash
openclaw nodes pending
openclaw nodes approve <requestId>
```

Pairing tafsilotlari: [Gateway pairing](/gateway/pairing).

### 5. Tugun ulanganini tekshiring

- 1. Via tugunlar holati:

  ```bash
  2. openclaw tugunlar holati
  ```

- 3. Via Gateway:

  ```bash
  4. openclaw gateway call node.list --params "{}"
  ```

### 5. 6. Chat + tarix

6. Android tugunining Chat oynasi gateway’ning **asosiy sessiya kaliti** (`main`) dan foydalanadi, shuning uchun tarix va javoblar WebChat va boshqa mijozlar bilan bo‘lishiladi:

- 7. Tarix: `chat.history`
- 8. Yuborish: `chat.send`
- 9. Push yangilanishlar (best-effort): `chat.subscribe` → `event:"chat"`

### 10. 7. Canvas + kamera

#### 11. Gateway Canvas Host (veb kontent uchun tavsiya etiladi)

12. Agar tugun agent diskda tahrirlashi mumkin bo‘lgan haqiqiy HTML/CSS/JS ni ko‘rsatsin desangiz, tugunni Gateway canvas host’ga yo‘naltiring.

13. Eslatma: tugunlar `canvasHost.port` (`standart` `18793`) dagi mustaqil canvas host’dan foydalanadi.

1. 14. Gateway host’da `~/.openclaw/workspace/canvas/index.html` yarating.

2. 15. Tugunni unga yo‘naltiring (LAN):

```bash
16. openclaw nodes invoke --node "<Android Node>" --command canvas.navigate --params '{"url":"http://<gateway-hostname>.local:18793/__openclaw__/canvas/"}'
```

17. Tailnet (ixtiyoriy): agar ikkala qurilma ham Tailscale’da bo‘lsa, `.local` o‘rniga MagicDNS nomi yoki tailnet IP’dan foydalaning, masalan: `http://<gateway-magicdns>:18793/__openclaw__/canvas/`.

18. Bu server HTML ichiga live-reload mijozini qo‘shadi va fayllar o‘zgarganda qayta yuklaydi.
19. A2UI host `http://<gateway-host>:18793/__openclaw__/a2ui/` da joylashgan.

20. Canvas buyruqlari (faqat oldingi rejim):

- 21. `canvas.eval`, `canvas.snapshot`, `canvas.navigate` (standart scaffold’ga qaytish uchun `{"url":""}` yoki `{"url":"/"}` dan foydalaning). 22. `canvas.snapshot` `{ format, base64 }` ni qaytaradi (`standart` `format="jpeg"`).
- 23. A2UI: `canvas.a2ui.push`, `canvas.a2ui.reset` (`canvas.a2ui.pushJSONL` eski alias)

24. Kamera buyruqlari (faqat oldingi rejim; ruxsat bilan cheklangan):

- 25. `camera.snap` (jpg)
- 26. `camera.clip` (mp4)

27. Parametrlar va CLI yordamchilari uchun [Camera node](/nodes/camera) ga qarang.
