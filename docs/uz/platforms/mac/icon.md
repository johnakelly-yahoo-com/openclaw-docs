---
summary: "10. macOS’da OpenClaw uchun menyu paneli ikonka holatlari va animatsiyalari"
read_when:
  - 11. Meniu paneli ikonka xatti-harakatini o‘zgartirish
title: "12. Meniu paneli ikonka"
---

# 13. Meniu paneli ikonka holatlari

14. Muallif: steipete · Yangilangan: 2025-12-06 · Qamrov: macOS ilovasi (`apps/macos`)

- 15. **Idle:** Oddiy ikonka animatsiyasi (miltillash, vaqti-vaqti bilan qimir).
- 16. **Paused:** Status elementi `appearsDisabled` dan foydalanadi; harakat yo‘q.
- 17. **Ovozli trigger (katta quloqlar):** Ovoz uyg‘otish detektori uyg‘otuvchi so‘z eshitilganda `AppState.triggerVoiceEars(ttl: nil)` ni chaqiradi va nutq yozib olinayotgan paytda `earBoostActive=true` ni saqlab turadi. 18. Quloqlar 1.9x ga kattalashadi, o‘qiluvchanlik uchun dumaloq quloq teshiklari paydo bo‘ladi, so‘ng 1 soniya sukunatdan keyin `stopVoiceEars()` orqali tushiriladi. 19. Faqat ilova ichidagi ovoz pipeline’idan ishga tushiriladi.
- 20. **Working (agent ishlayapti):** `AppState.isWorking=true` “dum/oyoqlar yugurishi” mikro-harakatini boshqaradi: ish jarayoni davomida tezroq oyoq qimirlatish va yengil siljish. 21. Hozirda WebChat agent ishga tushirilishi atrofida yoqib/o‘chiriladi; ularni ulaganingizda boshqa uzoq vazifalar atrofida ham xuddi shunday toggle qo‘shing.

22. Ulash nuqtalari

- 23. Ovoz uyg‘otish: runtime/tester trigger paytida `AppState.triggerVoiceEars(ttl: nil)` ni chaqiring va yozib olish oynasiga mos kelishi uchun 1 soniya sukunatdan keyin `stopVoiceEars()` ni chaqiring.
- 24. Agent faolligi: ish oralig‘ida `AppStateStore.shared.setWorking(true/false)` ni o‘rnating (WebChat agent chaqiruvida allaqachon qilingan). 25. Animatsiyalar tiqilib qolmasligi uchun oraliqlarni qisqa tuting va `defer` bloklarida reset qiling.

26. Shakllar va o‘lchamlar

- 27. Asosiy ikonka `CritterIconRenderer.makeIcon(blink:legWiggle:earWiggle:earScale:earHoles:)` da chiziladi.
- 28. Quloq masshtabi sukut bo‘yicha `1.0`; ovozli boost `earScale=1.9` ni o‘rnatadi va umumiy freymni o‘zgartirmasdan `earHoles=true` ni yoqadi (18×18 pt shablon tasvir 36×36 px Retina backing store’ga render qilinadi).
- 29. Scurry oyoq qimirlatishni ~1.0 gacha va kichik gorizontal tebranishni ishlatadi; u mavjud idle wiggle’ga qo‘shimcha bo‘ladi.

30. Xulq-atvor eslatmalari

- 31. Quloqlar/working uchun tashqi CLI/broker toggle yo‘q; tasodifiy tebranishlarni oldini olish uchun buni ilovaning o‘z signallari ichida saqlang.
- 32. Agar vazifa osilib qolsa, ikonka tezda bazaviy holatga qaytishi uchun TTL’larni qisqa (&lt;10s) tuting.
