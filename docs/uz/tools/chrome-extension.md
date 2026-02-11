---
summary: "12. Chrome kengaytmasi: OpenClaw’ga mavjud Chrome tabingizni boshqarishga ruxsat bering"
read_when:
  - 13. Siz agent mavjud Chrome tabini (asboblar paneli tugmasi) boshqarishini xohlaysiz
  - 14. Sizga masofaviy Gateway + Tailscale orqali mahalliy brauzer avtomatlashtirish kerak
  - 15. Siz brauzerni egallab olishning xavfsizlik oqibatlarini tushunmoqchisiz
title: "16. Chrome kengaytmasi"
---

# 17. Chrome kengaytmasi (brauzer relay)

18. OpenClaw Chrome kengaytmasi agentga alohida openclaw-boshqariladigan Chrome profilini ishga tushirmasdan, **mavjud Chrome tablaringizni** (oddiy Chrome oynangizni) boshqarish imkonini beradi.

19. Ulanish/uzilish **bitta Chrome asboblar paneli tugmasi** orqali amalga oshiriladi.

## 20. Bu nima (kontseptsiya)

21. Uchta qism mavjud:

- 22. **Brauzerni boshqarish xizmati** (Gateway yoki node): agent/asbob chaqiradigan API (Gateway orqali)
- 23. **Mahalliy relay serveri** (loopback CDP): boshqaruv serveri va kengaytma o‘rtasida ko‘prik bo‘ladi (sukut bo‘yicha `http://127.0.0.1:18792`)
- 24. **Chrome MV3 kengaytmasi**: `chrome.debugger` yordamida faol tabga ulanadi va CDP xabarlarini relay’ga uzatadi

25. So‘ng OpenClaw biriktirilgan tabni odatiy `browser` asbob interfeysi orqali (to‘g‘ri profilni tanlab) boshqaradi.

## 26. O‘rnatish / yuklash (unpacked)

1. 27. Kengaytmani barqaror mahalliy yo‘lga o‘rnating:

```bash
28. openclaw browser extension install
```

2. 29. O‘rnatilgan kengaytma katalogi yo‘lini chiqaring:

```bash
30. openclaw browser extension path
```

3. 31. Chrome → `chrome://extensions`

- 32) “Developer mode” ni yoqing
- 33. “Load unpacked” → yuqorida chiqarilgan katalogni tanlang

4. 34. Kengaytmani pin qiling.

## 35) Yangilanishlar (build bosqichisiz)

36. Kengaytma OpenClaw relizi (npm paketi) ichida statik fayllar sifatida yetkaziladi. 37. Alohida “build” bosqichi yo‘q.

38. OpenClaw yangilangandan so‘ng:

- 39. OpenClaw holat katalogi ostidagi o‘rnatilgan fayllarni yangilash uchun `openclaw browser extension install` ni qayta ishga tushiring.
- 40. Chrome → `chrome://extensions` → kengaytmada “Reload” ni bosing.

## 41. Foydalanish (qo‘shimcha sozlamalarsiz)

42. OpenClaw sukut bo‘yicha `chrome` nomli ichki brauzer profili bilan keladi, u standart portdagi kengaytma relay’iga yo‘naltirilgan.

43. Undan foydalaning:

- 44. CLI: `openclaw browser --browser-profile chrome tabs`
- 45. Agent asbobi: `browser` va `profile="chrome"`

46. Agar boshqa nom yoki boshqa relay porti kerak bo‘lsa, o‘zingiz profilingizni yarating:

```bash
47. openclaw browser create-profile \
  --name my-chrome \
  --driver extension \
  --cdp-url http://127.0.0.1:18792 \
  --color "#00AA00"
```

## 48. Ulanish / uzilish (asboblar paneli tugmasi)

- 49. OpenClaw boshqarishini xohlagan tabni oching.
- 50. Kengaytma belgisini bosing.
  - Beydj biriktirilganda `ON` ni ko‘rsatadi.
- Ajratish uchun yana bir marta bosing.

## Qaysi tabni boshqaradi?

- U avtomatik ravishda “siz hozir qarab turgan tabni” boshqarmaydi.
- U **faqat siz asboblar paneli tugmasini bosib aniq biriktirgan tab(lar)ni** boshqaradi.
- Almashtirish uchun: boshqa tabni oching va u yerda kengaytma ikonkasini bosing.

## Beydj + keng tarqalgan xatolar

- `ON`: biriktirilgan; OpenClaw o‘sha tabni boshqara oladi.
- `…`: lokal relayga ulanmoqda.
- `!`: relayga ulanib bo‘lmadi (eng ko‘p uchraydigani: brauzer relay serveri bu kompyuterda ishga tushmagan).

Agar `!` ni ko‘rsangiz:

- Gateway lokal ishlayotganiga ishonch hosil qiling (standart sozlama), yoki Gateway boshqa joyda ishlasa, bu mashinada node host ishga tushiring.
- Kengaytma Options sahifasini oching; u relayga ulanish mumkinligini ko‘rsatadi.

## Masofaviy Gateway (node hostdan foydalaning)

### Lokal Gateway (Chrome bilan bir xil mashina) — odatda **qo‘shimcha qadamlar yo‘q**

Agar Gateway Chrome bilan bir xil mashinada ishlasa, u loopback’da brauzer boshqaruv xizmatini ishga tushiradi va relay serverini avtomatik boshlaydi. Kengaytma lokal relay bilan gaplashadi; CLI/asbob chaqiriqlari Gateway’ga boradi.

### Masofaviy Gateway (Gateway boshqa joyda ishlaydi) — **node hostni ishga tushiring**

Agar Gateway boshqa mashinada ishlasa, Chrome ishlayotgan mashinada node hostni ishga tushiring.
Gateway brauzer harakatlarini o‘sha node’ga proksi qiladi; kengaytma + relay brauzer mashinasida lokal qoladi.

Agar bir nechta node ulangan bo‘lsa, bittasini `gateway.nodes.browser.node` bilan pin qiling yoki `gateway.nodes.browser.mode` ni sozlang.

## Sandboxing (asbob konteynerlari)

Agar agent sessiyangiz sandbox qilingan bo‘lsa (`agents.defaults.sandbox.mode != "off"`), `browser` asbobi cheklanishi mumkin:

- Standart holatda, sandbox qilingan sessiyalar ko‘pincha **sandbox brauzer**ni (`target="sandbox"`) nishonga oladi, xost Chrome’ni emas.
- Chrome kengaytmasi orqali relay takeover **xost** brauzer boshqaruv serverini nazorat qilishni talab qiladi.

Variantlar:

- Eng osoni: kengaytmadan **sandbox qilinmagan** sessiya/agentdan foydalanish.
- Yoki sandbox qilingan sessiyalar uchun xost brauzer boshqaruviga ruxsat bering:

```json5
{
  agents: {
    defaults: {
      sandbox: {
        browser: {
          allowHostControl: true,
        },
      },
    },
  },
}
```

So‘ng asbob siyosat bilan rad etilmaganiga ishonch hosil qiling va (kerak bo‘lsa) `browser` ni `target="host"` bilan chaqiring.

Diagnostika: `openclaw sandbox explain`

## Masofaviy kirish bo‘yicha maslahatlar

- Gateway va node hostni bir xil tailnet’da saqlang; relay portlarini LAN yoki ommaviy Internetga ochishdan qoching.
- Node’larni ongli ravishda juftlang; masofadan boshqarishni istamasangiz brauzer proksi marshrutlashni o‘chiring (`gateway.nodes.browser.mode="off"`).

## “Extension path” qanday ishlaydi

`openclaw browser extension path` kengaytma fayllari joylashgan **o‘rnatilgan** diskdagi katalogni chiqaradi.

CLI ataylab `node_modules` yo‘lini chiqarmaydi. Har doim avval `openclaw browser extension install` ni ishga tushiring — bu kengaytmani OpenClaw holat katalogingiz ostidagi barqaror joyga ko‘chiradi.

Agar o‘sha o‘rnatish katalogini ko‘chirsangiz yoki o‘chirsangiz, Chrome uni yaroqsiz deb belgilaydi va to‘g‘ri yo‘ldan qayta yuklamaguningizcha kengaytma buzilgan bo‘lib qoladi.

## Xavfsizlik oqibatlari (buni o‘qing)

Bu juda kuchli va xavfli. Buni modelga “brauzeringizda qo‘llar” berishdek qabul qiling.

- Kengaytma Chrome’ning debugger API’sidan foydalanadi (`chrome.debugger`). Biriktirilganda, model quyidagilarni qila oladi:
  - tabda bosish/yozish/navigatsiya qilish
  - sahifa mazmunini o‘qish
  - tab’dagi login qilingan sessiya kira oladigan hamma narsaga kirish
- **Bu ajratilgan emas** — maxsus openclaw tomonidan boshqariladigan profil kabi emas.
  - Agar kundalik foydalaniladigan profilingiz/tab’ingizga biriktirsangiz, o‘sha akkaunt holatiga kirish huquqini berasiz.

Tavsiyalar:

- Kengaytma relayidan foydalanish uchun shaxsiy brauzeringizdan alohida, maxsus Chrome profilini afzal ko‘ring.
- Gateway va barcha node xostlarni faqat tailnet ichida saqlang; Gateway autentifikatsiyasi va node juftlashuviga tayaning.
- Relay portlarini LAN orqali (`0.0.0.0`) ochishdan saqlaning va Funnel (ommaviy)dan foydalanmang.
- Relay kengaytma bo‘lmagan manbalarni bloklaydi va CDP mijozlari uchun ichki autentifikatsiya tokenini talab qiladi.

Tegishli:

- Brauzer vositasi sharhi: [Browser](/tools/browser)
- Xavfsizlik auditi: [Security](/gateway/security)
- Tailscale sozlamalari: [Tailscale](/gateway/tailscale)
