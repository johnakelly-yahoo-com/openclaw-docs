---
summary: "OpenClaw typing indikatorlarini qachon ko‘rsatadi va ularni qanday sozlash mumkin"
read_when:
  - Typing indikatorlari xatti-harakatini yoki sukut bo‘yicha sozlamalarni o‘zgartirish
title: "Typing indikatorlari"
---

# Typing indikatorlari

Typing indikatorlari run faol bo‘lganida chat kanaliga yuboriladi. **Qachon** typing boshlanishini boshqarish uchun `agents.defaults.typingMode` dan va **qanchalik tez-tez** yangilanishini boshqarish uchun `typingIntervalSeconds` dan foydalaning.

## Sukut bo‘yicha sozlamalar

`agents.defaults.typingMode` **o‘rnatilmagan** bo‘lsa, OpenClaw eski xatti-harakatni saqlaydi:

- **To‘g‘ridan-to‘g‘ri chatlar**: model sikli boshlanishi bilan typing darhol boshlanadi.
- **Mention bilan guruh chatlari**: typing darhol boshlanadi.
- **Mentionsiz guruh chatlari**: typing faqat xabar matni stream bo‘la boshlaganda boshlanadi.
- **Heartbeat runlari**: typing o‘chirilgan.

## Rejimlar

`agents.defaults.typingMode` ni quyidagilardan biriga o‘rnating:

- `never` — hech qachon typing indikatori yo‘q.
- `instant` — model sikli boshlanishi bilan **darhol** typing boshlanadi, hatto run
  keyinroq faqat jim javob tokenini qaytarsa ham.
- `thinking` — **birinchi reasoning delta** da typing boshlanadi (run uchun
  `reasoningLevel: "stream"` talab qilinadi).
- `message` — **birinchi jim bo‘lmagan matn delta** da typing boshlanadi (`NO_REPLY` jim tokenini e’tiborsiz qoldiradi).

“Qanchalik erta ishga tushishi” tartibi:
`never` → `message` → `thinking` → `instant`

## Konfiguratsiya

```json5
{
  agent: {
    typingMode: "thinking",
    typingIntervalSeconds: 6,
  },
}
```

Har bir sessiya uchun rejim yoki chastotani alohida o‘zgartirishingiz mumkin:

```json5
{
  session: {
    typingMode: "message",
    typingIntervalSeconds: 4,
  },
}
```

## Eslatmalar

- `message` rejimi faqat jim javoblar (masalan, chiqishni bostirish uchun ishlatiladigan `NO_REPLY`
  tokeni) uchun typing ko‘rsatmaydi.
- `thinking` faqat ish reasoning oqimini uzatayotganda ishga tushadi (`reasoningLevel: "stream"`).
  Agar model reasoning deltalarni chiqarmasa, yozish boshlanmaydi.
- Heartbeats rejimdan qat’i nazar, hech qachon yozishni ko‘rsatmaydi.
- `typingIntervalSeconds` boshlanish vaqtini emas, **yangilanish tezligini** boshqaradi.
  Standart qiymat — 6 soniya.
