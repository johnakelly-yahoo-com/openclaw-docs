---
summary: "6. Kengaytirilgan exec rejimi va /elevated direktivalari"
read_when:
  - 7. Kengaytirilgan rejim standartlarini, ruxsat ro‘yxatlarini yoki slash-buyruqlar xatti-harakatini sozlash
title: "8. Kengaytirilgan rejim"
---

# 9. Kengaytirilgan rejim (/elevated direktivalari)

## 10. U nima qiladi

- 11. `/elevated on` gateway xostda ishlaydi va exec tasdiqlarini saqlab qoladi ( `/elevated ask` bilan bir xil).
- 12. `/elevated full` gateway xostda ishlaydi **va** exec’ni avtomatik tasdiqlaydi (exec tasdiqlarini o‘tkazib yuboradi).
- 13. `/elevated ask` gateway xostda ishlaydi, lekin exec tasdiqlarini saqlab qoladi ( `/elevated on` bilan bir xil).
- 14. `on`/`ask` `exec.security=full` ni **majburiy** qilmaydi; sozlangan security/ask siyosati baribir amal qiladi.
- 15. Faqat agent **sandboxed** bo‘lganda xatti-harakatni o‘zgartiradi (aks holda exec allaqachon xostda ishlaydi).
- 16. Direktiva shakllari: `/elevated on|off|ask|full`, `/elev on|off|ask|full`.
- 17. Faqat `on|off|ask|full` qabul qilinadi; boshqa har qanday qiymat maslahat qaytaradi va holatni o‘zgartirmaydi.

## 18. U nimani boshqaradi (va nimani boshqarmaydi)

- 19. **Mavjudlik to‘siqlari**: `tools.elevated` — global asosiy daraja. 20. `agents.list[].tools.elevated` har bir agent bo‘yicha kengaytirilganni yanada cheklashi mumkin (ikkalasi ham ruxsat berishi kerak).
- 21. **Sessiya bo‘yicha holat**: `/elevated on|off|ask|full` joriy sessiya kaliti uchun kengaytirilgan darajani o‘rnatadi.
- 22. **Inline direktiva**: Xabar ichidagi `/elevated on|ask|full` faqat shu xabarga tatbiq etiladi.
- 23. **Guruhlar**: Guruh chatlarida kengaytirilgan direktivalar faqat agent tilga olinganda bajariladi. 24. Tilga olish talablarini chetlab o‘tadigan faqat-buyruq xabarlari tilga olingan deb hisoblanadi.
- 25. **Xostda bajarish**: kengaytirilgan rejim `exec` ni gateway xostga majburiy o‘tkazadi; `full` esa `security=full` ni ham o‘rnatadi.
- 26. **Tasdiqlar**: `full` exec tasdiqlarini o‘tkazib yuboradi; `on`/`ask` esa ruxsat ro‘yxati/ask qoidalari talab qilganda ularni hurmat qiladi.
- 27. **Sandbox bo‘lmagan agentlar**: joylashuv uchun hech narsa qilmaydi; faqat gating, loglash va holatga ta’sir qiladi.
- 28. **Asbob siyosati baribir amal qiladi**: agar `exec` asbob siyosati tomonidan rad etilgan bo‘lsa, kengaytirilgandan foydalanib bo‘lmaydi.
- 29. **`/exec` dan alohida**: `/exec` ruxsat etilgan jo‘natuvchilar uchun sessiya bo‘yicha standartlarni sozlaydi va kengaytirilganni talab qilmaydi.

## 30. Hal qilish tartibi

1. 31. Xabardagi inline direktiva (faqat shu xabarga tatbiq etiladi).
2. 32. Sessiya override’i (faqat-direktiva xabar yuborish orqali o‘rnatiladi).
3. 33. Global standart (`agents.defaults.elevatedDefault` konfiguratsiyada).

## 34) Sessiya standartini o‘rnatish

- 35. **Faqat** direktivadan iborat xabar yuboring (bo‘shliqlarga ruxsat beriladi), masalan, `/elevated full`.
- 36. Tasdiqlovchi javob yuboriladi (`Elevated mode set to full...` / `Elevated mode disabled.`).
- 37. Agar kengaytirilgan kirish o‘chirilgan bo‘lsa yoki jo‘natuvchi tasdiqlangan ruxsat ro‘yxatida bo‘lmasa, direktiva amaliy xato bilan javob qaytaradi va sessiya holatini o‘zgartirmaydi.
- 38. Joriy kengaytirilgan darajani ko‘rish uchun argumentlarsiz `/elevated` (yoki `/elevated:`) yuboring.

## 39. Mavjudlik + ruxsat ro‘yxatlari

- 40. Funksiya to‘sig‘i: `tools.elevated.enabled` (kod qo‘llab-quvvatlasa ham, konfiguratsiya orqali sukut bo‘yicha o‘chiq bo‘lishi mumkin).
- 41. Jo‘natuvchi ruxsat ro‘yxati: `tools.elevated.allowFrom` provayderlar bo‘yicha ruxsat ro‘yxatlari bilan (masalan, `discord`, `whatsapp`).
- 42. Agent bo‘yicha to‘siq: `agents.list[].tools.elevated.enabled` (ixtiyoriy; faqat yanada cheklashi mumkin).
- 43. Agent bo‘yicha ruxsat ro‘yxati: `agents.list[].tools.elevated.allowFrom` (ixtiyoriy; o‘rnatilganda, jo‘natuvchi **ikkala** global + agent bo‘yicha ruxsat ro‘yxatlariga mos kelishi kerak).
- 44. Discord fallback: agar `tools.elevated.allowFrom.discord` ko‘rsatilmagan bo‘lsa, `channels.discord.dm.allowFrom` ro‘yxati fallback sifatida ishlatiladi. 45. Override qilish uchun `tools.elevated.allowFrom.discord` ni (hatto `[]` bo‘lsa ham) o‘rnating. 46. Agent bo‘yicha ruxsat ro‘yxatlari fallback’dan **foydalanmaydi**.
- 47. Barcha to‘siqlar o‘tishi kerak; aks holda kengaytirilgan rejim mavjud emas deb hisoblanadi.

## 48. Loglash + holat

- 49. Kengaytirilgan exec chaqiruvlari info darajasida loglanadi.
- 50. Sessiya holati kengaytirilgan rejimni o‘z ichiga oladi (masalan, `elevated=ask`, `elevated=full`).
