---
summary: "32. Kiruvchi auto-reply ishlarini ketma-ketlashtiradigan buyruqlar navbati dizayni"
read_when:
  - 33. Auto-reply bajarilishi yoki parallelizmini o‘zgartirish
title: "34. Buyruqlar navbati"
---

# 35. Buyruqlar navbati (2026-01-16)

36. Bir nechta agent ishlarining to‘qnashuvini oldini olish uchun barcha kanallar bo‘yicha kiruvchi auto-reply ishlarini kichik, jarayon ichidagi navbat orqali ketma-ketlashtiramiz, shu bilan birga sessiyalar bo‘yicha xavfsiz parallelizmga ruxsat beramiz.

## 37. Nega

- 38. Auto-reply ishlar qimmat bo‘lishi mumkin (LLM chaqiruvlari) va bir nechta kiruvchi xabarlar bir-biriga yaqin kelganda to‘qnashishi mumkin.
- 39. Ketma-ketlashtirish umumiy resurslar (sessiya fayllari, loglar, CLI stdin) uchun raqobatni kamaytiradi va yuqori oqimdagi rate limitlar ehtimolini pasaytiradi.

## 40. Qanday ishlaydi

- 41. Yo‘laklarga sezgir FIFO navbat har bir yo‘lakni sozlanadigan parallelizm chegarasi bilan bo‘shatadi (sozlanmagan yo‘laklar uchun standart 1; main uchun 4, subagent uchun 8).
- 42. `runEmbeddedPiAgent` **sessiya kaliti** bo‘yicha navbatga qo‘shadi (yo‘lak `session:<key>`) va har bir sessiya uchun faqat bitta faol ishni kafolatlaydi.
- 43. Har bir sessiya ishi so‘ngra **global yo‘lak** ga (standart bo‘yicha `main`) navbatga qo‘shiladi, shuning uchun umumiy parallelizm `agents.defaults.maxConcurrent` bilan cheklanadi.
- 44. Batafsil loglash yoqilganda, navbatdagi ishlar boshlanishidan oldin ~2 soniyadan ko‘proq kutgan bo‘lsa, qisqa bildirishnoma chiqaradi.
- 45. Navbatga qo‘shish paytida (kanal tomonidan qo‘llab-quvvatlanganda) typing indikatorlari darhol ishga tushadi, shuning uchun navbatimizni kutayotganimizda ham foydalanuvchi tajribasi o‘zgarmaydi.

## 46. Navbat rejimlari (har bir kanal bo‘yicha)

47. Kiruvchi xabarlar joriy ishni yo‘naltirishi, keyingi navbatdagi burilishni kutishi yoki ikkalasini ham qilishi mumkin:

- `steer`: joriy ishga darhol kiritadi (keyingi tool chegarasidan keyin kutilayotgan tool chaqiruvlarini bekor qiladi). 49. Agar streaming bo‘lmasa, `followup` ga qaytadi.
- 50. `followup`: joriy ish tugagach, keyingi agent burilishi uchun navbatga qo‘shadi.
- 1. `collect`: navbatga olingan barcha xabarlarni **bitta** keyingi javobga birlashtiradi (standart). 2. Agar xabarlar turli kanallar/ipliklarga yo‘naltirilgan bo‘lsa, marshrutlashni saqlash uchun ular alohida-alohida chiqariladi.
- 3. `steer-backlog` (ya’ni `steer+backlog`): hozir yo‘naltiradi **va** xabarni keyingi javob uchun saqlab qoladi.
- 4. `interrupt` (eskirgan): shu sessiya uchun faol ishni to‘xtatadi, so‘ng eng yangi xabarni ishga tushiradi.
- 5. `queue` (eskirgan sinonim): `steer` bilan bir xil.

6. Steer-backlog shuni anglatadiki, yo‘naltirilgan ish tugagach yana keyingi javob olishingiz mumkin, shuning uchun oqimli interfeyslar dublikatga o‘xshab ko‘rinishi mumkin. 7. Agar har bir kiruvchi xabar uchun bitta javob xohlasangiz, `collect`/`steer` ni afzal ko‘ring.
7. Mustaqil buyruq sifatida `/queue collect` yuboring (har sessiya uchun) yoki `messages.queue.byChannel.discord: "collect"` ni o‘rnating.

9. Standartlar (konfiguratsiyada o‘rnatilmagan bo‘lsa):

- 10. Barcha interfeyslar → `collect`

11. Global yoki kanal bo‘yicha `messages.queue` orqali sozlang:

```json5
12. {
  messages: {
    queue: {
      mode: "collect",
      debounceMs: 1000,
      cap: 20,
      drop: "summarize",
      byChannel: { discord: "collect" },
    },
  },
}
```

## 13. Navbat parametrlari

14. Parametrlar `followup`, `collect` va `steer-backlog` ga qo‘llanadi (hamda `steer` keyingi javobga qaytganda):

- 15. `debounceMs`: keyingi javobni boshlashdan oldin sukunatni kutish (“continue, continue” ni oldini oladi).
- 16. `cap`: har bir sessiya uchun navbatdagi maksimal xabarlar soni.
- 17. `drop`: to‘lib ketganda siyosat (`old`, `new`, `summarize`).

18. Summarize tashlab yuborilgan xabarlarning qisqa punktlar ro‘yxatini saqlaydi va uni sun’iy keyingi so‘rov sifatida kiritadi.
19. Standartlar: `debounceMs: 1000`, `cap: 20`, `drop: summarize`.

## 20. Sessiya bo‘yicha alohida sozlamalar

- 21. Joriy sessiya uchun rejimni saqlash uchun mustaqil buyruq sifatida `/queue <mode>` yuboring.
- 22. Parametrlarni birlashtirish mumkin: `/queue collect debounce:2s cap:25 drop:summarize`
- 23. `/queue default` yoki `/queue reset` sessiya bo‘yicha o‘rnatilgan sozlamani tozalaydi.

## 24. Qamrov va kafolatlar

- 25. Javob shlyuzi quvuridan foydalanadigan barcha kiruvchi kanallarda avtomatik javob agenti ishlariga tatbiq etiladi (WhatsApp web, Telegram, Slack, Discord, Signal, iMessage, webchat va boshqalar).
- 26. Standart yo‘lak (`main`) kiruvchi xabarlar va asosiy yurak urishlari uchun butun jarayon bo‘yicha umumiy; bir vaqtning o‘zida bir nechta sessiyaga ruxsat berish uchun `agents.defaults.maxConcurrent` ni o‘rnating.
- 27. Qo‘shimcha yo‘laklar mavjud bo‘lishi mumkin (masalan, `cron`, `subagent`), shunda fon ishlar kiruvchi javoblarni bloklamasdan parallel ishlaydi.
- 28. Sessiya bo‘yicha yo‘laklar bir vaqtning o‘zida faqat bitta agent ishi berilgan sessiyaga tegishini kafolatlaydi.
- 29. Tashqi bog‘liqliklar yoki fon ishchi oqimlari yo‘q; sof TypeScript + promises.

## 30. Muammolarni bartaraf etish

- 31. Agar buyruqlar tiqilib qolgandek ko‘rinsa, batafsil loglarni yoqing va navbat bo‘shayotganini tasdiqlash uchun “queued for …ms” qatorlarini qidiring.
- 32. Agar navbat chuqurligi kerak bo‘lsa, batafsil loglarni yoqing va navbat vaqtlariga oid qatorlarni kuzating.
