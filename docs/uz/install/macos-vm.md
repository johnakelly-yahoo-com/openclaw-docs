---
summary: "Izolyatsiya yoki iMessage kerak bo‘lganda OpenClaw’ni sandboxlangan macOS VM’da (mahalliy yoki hosted) ishga tushiring."
read_when:
  - Siz OpenClaw’ni asosiy macOS muhitingizdan ajratib qo‘ymoqchisiz.
  - Siz sandbox ichida iMessage integratsiyasini (BlueBubbles) xohlaysiz.
  - Siz klonlash mumkin bo‘lgan, qayta tiklanadigan macOS muhitini xohlaysiz.
  - Siz mahalliy va hosted macOS VM variantlarini solishtirmoqchisiz.
title: "macOS VM’lar"
---

# macOS VM’larda OpenClaw (Sandboxing)

## Tavsiya etilgan standart (ko‘pchilik foydalanuvchilar uchun).

- Doim yoqilgan Gateway va past xarajat uchun **kichik Linux VPS**. [VPS hosting](/vps) ga qarang.
- Brauzer avtomatlashtirish uchun to‘liq nazorat va **rezident IP** xohlasangiz **maxsus apparat** (Mac mini yoki Linux qurilma). Ko‘plab saytlar data-markaz IP’larini bloklaydi, shuning uchun mahalliy brauzer ko‘pincha yaxshiroq ishlaydi.
- **Gibrid:** Gateway’ni arzon VPS’da saqlang va brauzer/UI avtomatlashtirish kerak bo‘lganda Mac’ingizni **node** sifatida ulang. [Nodes](/nodes) va [Gateway remote](/gateway/remote) ga qarang.

Agar sizga faqat macOS’ga xos imkoniyatlar (iMessage/BlueBubbles) kerak bo‘lsa yoki kundalik Mac’ingizdan qat’iy izolyatsiya xohlasangiz, macOS VM’dan foydalaning.

## macOS VM variantlari

### Apple Silicon Mac’ingizda (Lume) mahalliy VM

Mavjud Apple Silicon Mac’ingizda [Lume](https://cua.ai/docs/lume) yordamida sandboxlangan macOS VM’da OpenClaw’ni ishga tushiring.

Bu sizga quyidagilarni beradi:

- Izolyatsiyadagi to‘liq macOS muhiti (hostingiz toza qoladi)
- BlueBubbles orqali iMessage qo‘llab-quvvatlashi (Linux/Windows’da imkonsiz)
- VM’larni klonlash orqali darhol reset
- Qo‘shimcha apparat yoki bulut xarajatlari yo‘q

### Hosted Mac provayderlari (bulut)

Agar sizga bulutda macOS kerak bo‘lsa, hosted Mac provayderlari ham mos keladi:

- [MacStadium](https://www.macstadium.com/) (hosted Mac’lar)
- Boshqa hosted Mac sotuvchilari ham ishlaydi; ularning VM + SSH hujjatlariga amal qiling.

macOS VM’ga SSH orqali kirish imkoniga ega bo‘lgach, quyidagi 6-qadamdan davom eting.

---

## Tezkor yo‘l (Lume, tajribali foydalanuvchilar)

1. Lume’ni o‘rnating
2. `lume create openclaw --os macos --ipsw latest`
3. Setup Assistant’ni yakunlang, Remote Login (SSH) ni yoqing
4. `lume run openclaw --no-display`
5. SSH orqali kiring, OpenClaw’ni o‘rnating, kanallarni sozlang
6. Tayyor

---

## Kerakli narsalar (Lume)

- Apple Silicon Mac (M1/M2/M3/M4)
- Host’da macOS Sequoia yoki undan keyingi versiya
- Har bir VM uchun ~60 GB bo‘sh disk joyi
- ~20 daqiqa

---

## 1. Lume’ni o‘rnating

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/trycua/cua/main/libs/lume/scripts/install.sh)"
```

Agar `~/.local/bin` PATH’ingizda bo‘lmasa:

```bash
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.zshrc && source ~/.zshrc
```

Tekshiring:

```bash
lume --version
```

Hujjatlar: [Lume Installation](https://cua.ai/docs/lume/guide/getting-started/installation)

---

## 2. macOS VM’ni yarating

```bash
lume create openclaw --os macos --ipsw latest
```

Bu macOS’ni yuklab oladi va VM’ni yaratadi. VNC oynasi avtomatik ravishda ochiladi.

Eslatma: Yuklab olish ulanish tezligingizga qarab biroz vaqt olishi mumkin.

---

## 3. Setup Assistant’ni yakunlang

VNC oynasida:

1. Til va mintaqani tanlang
2. Apple ID’ni o‘tkazib yuboring (yoki keyin iMessage ishlatmoqchi bo‘lsangiz, tizimga kiring)
3. Foydalanuvchi hisobini yarating (foydalanuvchi nomi va parolni eslab qoling)
4. Barcha ixtiyoriy funksiyalarni o‘tkazib yuboring

Sozlash tugagach, SSH’ni yoqing:

1. System Settings → General → Sharing’ni oching
2. "Remote Login"’ni yoqing

---

## 4. VM’ning IP manzilini oling

```bash
lume get openclaw
```

IP manzilni toping (odatda `192.168.64.x`).

---

## 5. VM’ga SSH orqali kiring

```bash
ssh youruser@192.168.64.X
```

`youruser` o‘rniga yaratgan hisobingizni, IP o‘rniga esa VM’ingizning IP manzilini qo‘ying.

---

## 6. OpenClaw’ni o‘rnating

VM ichida:

```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

Model provayderingizni (Anthropic, OpenAI va boshqalar) sozlash uchun onboarding ko‘rsatmalariga amal qiling.

---

## 7. Kanallarni sozlash

Konfiguratsiya faylini tahrirlang:

```bash
nano ~/.openclaw/openclaw.json
```

Kanallaringizni qo‘shing:

```json
{
  "channels": {
    "whatsapp": {
      "dmPolicy": "allowlist",
      "allowFrom": ["+15551234567"]
    },
    "telegram": {
      "botToken": "YOUR_BOT_TOKEN"
    }
  }
}
```

So‘ng WhatsApp’ga kiring (QR’ni skaner qiling):

```bash
openclaw channels login
```

---

## 8. VM’ni headless rejimda ishga tushiring

VM’ni to‘xtatib, displeysiz qayta ishga tushiring:

```bash
lume stop openclaw
lume run openclaw --no-display
```

VM fon rejimida ishlaydi. OpenClaw’ning demoni gateway’ni ishlashda ushlab turadi.

Holatni tekshirish uchun:

```bash
ssh youruser@192.168.64.X "openclaw status"
```

---

## Bonus: iMessage integratsiyasi

Bu macOS’da ishlashning eng kuchli funksiyasidir. OpenClaw’ga iMessage qo‘shish uchun [BlueBubbles](https://bluebubbles.app) dan foydalaning.

VM ichida:

1. BlueBubbles’ni bluebubbles.app’dan yuklab oling
2. Apple ID’ingiz bilan tizimga kiring
3. Web API’ni yoqing va parol o‘rnating
4. BlueBubbles webhook’larini gateway’ingizga yo‘naltiring (misol: `https://your-gateway-host:3000/bluebubbles-webhook?password=<password>`)

OpenClaw konfiguratsiyangizga qo‘shing:

```json
{
  "channels": {
    "bluebubbles": {
      "serverUrl": "http://localhost:1234",
      "password": "your-api-password",
      "webhookPath": "/bluebubbles-webhook"
    }
  }
}
```

Gateway’ni qayta ishga tushiring. Endi agentingiz iMessage’larni yuborishi va qabul qilishi mumkin.

To‘liq sozlash tafsilotlari: [BlueBubbles channel](/channels/bluebubbles)

---

## Golden image’ni saqlang

Keyingi moslashtirishlardan oldin toza holatingizni snapshot qiling:

```bash
lume stop openclaw
lume clone openclaw openclaw-golden
```

Istalgan vaqtda tiklash:

```bash
lume stop openclaw && lume delete openclaw
lume clone openclaw-golden openclaw
lume run openclaw --no-display
```

---

## 24/7 ishlash

VM’ni doimiy ishlashda saqlash uchun:

- Mac’ingizni quvvatga ulangan holda saqlang
- System Settings → Energy Saver bo‘limida uyqu rejimini o‘chiring
- Agar kerak bo‘lsa, `caffeinate` dan foydalaning

Haqiqiy doimiy ishlash uchun maxsus Mac mini yoki kichik VPS’ni ko‘rib chiqing. Qarang: [VPS hosting](/vps).

---

## Nosozliklarni bartaraf etish

| Muammo                           | Yechim                                                                                                                        |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| VM’ga SSH orqali kira olmayapman | VM’ning System Settings bo‘limida "Remote Login" yoqilganligini tekshiring                                                    |
| VM IP ko‘rinmayapti              | VM to‘liq yuklanishini kuting, so‘ng `lume get openclaw` ni yana ishga tushiring                                              |
| Lume buyrug‘i topilmadi          | `~/.local/bin` ni PATH’ingizga qo‘shing                                                                                       |
| WhatsApp QR skan qilinmayapti    | `openclaw channels login` ni ishga tushirayotganda VM’ga (host’ga emas) kirganingizga ishonch hosil qiling |

---

## Tegishli hujjatlar

- [VPS hosting](/vps)
- [Nodes](/nodes)
- [Gateway remote](/gateway/remote)
- [BlueBubbles channel](/channels/bluebubbles)
- [Lume Quickstart](https://cua.ai/docs/lume/guide/getting-started/quickstart)
- [Lume CLI Reference](https://cua.ai/docs/lume/reference/cli-reference)
- [Unattended VM Setup](https://cua.ai/docs/lume/guide/fundamentals/unattended-setup) (ilg‘or)
- [Docker Sandboxing](/install/docker) (muqobil izolyatsiya yondashuvi)
