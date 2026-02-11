---
summary: "iOS va boshqa masofaviy tugunlar uchun shlyuzga tegishli tugun juftlashuvi (Variant B)"
read_when:
  - macOS UI bo‘lmasdan tugun juftlashuvini tasdiqlashni amalga oshirish
  - Masofaviy tugunlarni tasdiqlash uchun CLI oqimlarini qo‘shish
  - Tugunlarni boshqarish bilan shlyuz protokolini kengaytirish
title: "Shlyuzga tegishli juftlashuv"
---

# Shlyuzga tegishli juftlashuv (Variant B)

Shlyuzga tegishli juftlashuvda, qaysi tugunlarga qo‘shilish ruxsat etilishini belgilovchi yagona haqiqat manbai **Shlyuz** hisoblanadi. UI’lar (macOS ilovasi, kelajakdagi mijozlar) faqat kutilayotgan so‘rovlarni tasdiqlash yoki rad etish uchun frontend vazifasini bajaradi.

**Muhim:** WS tugunlari `connect` vaqtida **qurilma juftlashuvi** (rol `node`) dan foydalanadi.
`node.pair.*` alohida juftlashuv ombori bo‘lib, WS handshake’ni **cheklamaydi**.
Faqatgina aniq `node.pair.*` ni chaqirgan mijozlargina ushbu oqimdan foydalanadi.

## Tushunchalar

- **Kutilayotgan so‘rov**: tugun qo‘shilishni so‘radi; tasdiqlash talab etiladi.
- **Juftlangan tugun**: tasdiqlangan va autentifikatsiya tokeni berilgan tugun.
- **Transport**: Shlyuz WS endpoint’i so‘rovlarni uzatadi, ammo a’zolikni hal qilmaydi. (Meros TCP ko‘prigi qo‘llab-quvvatlashi eskirgan/olib tashlangan.)

## Juftlashuv qanday ishlaydi

1. Tugun Shlyuz WS ga ulanadi va juftlashuvni so‘raydi.
2. Shlyuz **kutilayotgan so‘rov**ni saqlaydi va `node.pair.requested` hodisasini chiqaradi.
3. Siz so‘rovni tasdiqlaysiz yoki rad etasiz (CLI yoki UI orqali).
4. Tasdiqlanganda, Shlyuz **yangi token** chiqaradi (qayta juftlashuvda tokenlar aylantiriladi).
5. Tugun token yordamida qayta ulanadi va endi “juftlangan” bo‘ladi.

Kutilayotgan so‘rovlar **5 daqiqa**dan so‘ng avtomatik ravishda muddati o‘tadi.

## CLI ish jarayoni (headless uchun qulay)

```bash
openclaw nodes pending
openclaw nodes approve <requestId>
openclaw nodes reject <requestId>
openclaw nodes status
openclaw nodes rename --node <id|name|ip> --name "Living Room iPad"
```

`nodes status` juftlangan/ulangan tugunlar va ularning imkoniyatlarini ko‘rsatadi.

## API yuzasi (shlyuz protokoli)

Hodisalar:

- `node.pair.requested` — yangi kutilayotgan so‘rov yaratilganda chiqariladi.
- `node.pair.resolved` — so‘rov tasdiqlanganda/rad etilganda/muddati o‘tganda chiqariladi.

Metodlar:

- `node.pair.request` — kutilayotgan so‘rovni yaratish yoki qayta ishlatish.
- `node.pair.list` — kutilayotgan + juftlangan tugunlarni ro‘yxatlash.
- `node.pair.approve` — kutilayotgan so‘rovni tasdiqlash (token chiqaradi).
- `node.pair.reject` — kutilayotgan so‘rovni rad etish.
- `node.pair.verify` — `{ nodeId, token }` ni tekshirish.

Eslatmalar:

- `node.pair.request` har bir tugun uchun idempotent: takroriy chaqiruvlar bir xil kutilayotgan so‘rovni qaytaradi.
- Tasdiqlash **har doim** yangi token yaratadi; `node.pair.request` dan hech qachon token qaytarilmaydi.
- So‘rovlar avtomatik tasdiqlash oqimlari uchun ishora sifatida `silent: true` ni o‘z ichiga olishi mumkin.

## Avtomatik tasdiqlash (macOS ilovasi)

macOS ilovasi quyidagi hollarda ixtiyoriy ravishda **jim tasdiqlash**ga urinishi mumkin:

- so‘rov `silent` deb belgilangan bo‘lsa va
- 1. ilova xuddi shu foydalanuvchi yordamida shlyuz xostiga SSH ulanishini tekshirishi mumkin.

2. Agar jim tasdiqlash muvaffaqiyatsiz bo‘lsa, u odatiy “Approve/Reject” so‘roviga qaytadi.

## 3. Saqlash (mahalliy, xususiy)

4. Juftlash holati Gateway holat katalogida saqlanadi (standart `~/.openclaw`):

- 5. `~/.openclaw/nodes/paired.json`
- 6. `~/.openclaw/nodes/pending.json`

7. Agar `OPENCLAW_STATE_DIR` ni qayta belgilasangiz, `nodes/` papkasi ham u bilan birga ko‘chadi.

8. Xavfsizlik eslatmalari:

- 9. Tokenlar maxfiy hisoblanadi; `paired.json` ni sezgir ma’lumot sifatida ko‘ring.
- 10. Tokenni aylantirish qayta tasdiqlashni talab qiladi (yoki tugun yozuvini o‘chirishni).

## 11. Transport xatti-harakati

- 12. Transport **holatsiz**; u a’zolikni saqlamaydi.
- 13. Agar Gateway oflayn bo‘lsa yoki juftlash o‘chirilgan bo‘lsa, tugunlar juftlasha olmaydi.
- 14. Agar Gateway masofaviy rejimda bo‘lsa, juftlash baribir masofaviy Gateway omboriga qarshi amalga oshiriladi.
