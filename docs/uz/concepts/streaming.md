---
summary: "22. Streaming + bo‘laklash xatti-harakati (blok javoblar, qoralama streaming, limitlar)"
read_when:
  - 23. Kanallarda streaming yoki bo‘laklash qanday ishlashini tushuntirish
  - 24. Blok streaming yoki kanal bo‘laklash xatti-harakatini o‘zgartirish
  - 25. Takroriy/erta blok javoblari yoki qoralama streamingni nosozlikdan chiqarish
title: "26. Streaming va Bo‘laklash"
---

# 27. Streaming + bo‘laklash

28. OpenClaw da ikkita alohida “streaming” qatlami mavjud:

- 29. **Blok streaming (kanallar):** yordamchi yozayotgan sari yakunlangan **bloklar**ni chiqaradi. 30. Bular oddiy kanal xabarlari (token deltalar emas).
- 31. **Token-ga o‘xshash streaming (faqat Telegram):** generatsiya jarayonida **qoralama pufagi**ni qisman matn bilan yangilaydi; yakuniy xabar oxirida yuboriladi.

32. Bugungi kunda tashqi kanal xabarlariga **haqiqiy token streaming** yo‘q. 33. Telegram qoralama streaming — yagona qisman-stream yuzasi.

## 34. Blok streaming (kanal xabarlari)

35. Blok streaming yordamchi chiqishini mavjud bo‘lishi bilan yirik bo‘laklarda yuboradi.

```
36. Model chiqishi
  └─ text_delta/events
       ├─ (blockStreamingBreak=text_end)
       │    └─ bufer o‘sgan sari chunker bloklarni chiqaradi
       └─ (blockStreamingBreak=message_end)
            └─ message_end da chunker tozalaydi
                   └─ kanalga yuborish (blok javoblar)
```

37. Afsona:

- 38. `text_delta/events`: model streaming hodisalari (streaming bo‘lmagan modellar uchun siyrak bo‘lishi mumkin).
- 39. `chunker`: `EmbeddedBlockChunker` min/maks chegaralarni va uzilish afzalligini qo‘llaydi.
- 40. `channel send`: haqiqiy chiqish xabarlari (blok javoblar).

41. **Boshqaruvlar:**

- 42. `agents.defaults.blockStreamingDefault`: `"on"`/`"off"` (standart: off).
- 43. Kanal bo‘yicha bekor qilishlar: `*.blockStreaming` (va hisob bo‘yicha variantlar) har bir kanal uchun `"on"`/`"off"` ni majburlash uchun.
- 44. `agents.defaults.blockStreamingBreak`: `"text_end"` yoki `"message_end"`.
- 45. `agents.defaults.blockStreamingChunk`: \`{ minChars, maxChars, breakPreference?
  46. }`. 47. `agents.defaults.blockStreamingCoalesce`: `{ minChars?, maxChars?, idleMs?
  47. }\` (yuborishdan oldin stream qilingan bloklarni birlashtirish).
- 49. Kanalning qat’iy chegarasi: `*.textChunkLimit` (masalan, `channels.whatsapp.textChunkLimit`). 50. Kanal bo‘laklash rejimi: `*.chunkMode` (`length` — standart, `newline` — uzunlik bo‘yicha bo‘laklashdan oldin bo‘sh qatorlar (paragraf chegaralari) bo‘yicha ajratadi).
- Channel hard cap: `*.textChunkLimit` (e.g., `channels.whatsapp.textChunkLimit`).
- Channel chunk mode: `*.chunkMode` (`length` default, `newline` splits on blank lines (paragraph boundaries) before length chunking).
- Discord soft cap: `channels.discord.maxLinesPerMessage` (standart 17) baland javoblarni UI kesilib qolishining oldini olish uchun bo‘lib yuboradi.

**Chegara semantikasi:**

- `text_end`: chunker chiqarishi bilanoq oqim bloklari; har bir `text_end` da flush qilinadi.
- `message_end`: assistent xabari tugaguncha kutadi, so‘ng buferlangan chiqishni flush qiladi.

`message_end` buferlangan matn `maxChars` dan oshsa ham chunker’dan foydalanadi, shuning uchun oxirida bir nechta chunk chiqarilishi mumkin.

## Chunklash algoritmi (past/yuqori chegaralar)

Blok bo‘yicha chunklash `EmbeddedBlockChunker` tomonidan amalga oshiriladi:

- **Past chegara:** bufer >= `minChars` bo‘lmaguncha chiqarma (majburiy holatlardan tashqari).
- **Yuqori chegara:** `maxChars` dan oldin bo‘linishni afzal ko‘r; majbur bo‘lsa, `maxChars` da bo‘l.
- **Uzilish ustuvorligi:** `paragraph` → `newline` → `sentence` → `whitespace` → qattiq uzilish.
- **Kod panjaralari:** panjaralar ichida hech qachon bo‘linmaydi; `maxChars` da majbur bo‘linganda, Markdown to‘g‘ri bo‘lishi uchun panjarani yopib + qayta ochadi.

`maxChars` kanalning `textChunkLimit` ga qisiladi, shuning uchun har bir kanal limitidan oshib bo‘lmaydi.

## Birlashtirish (oqimdagi bloklarni qo‘shish)

Blok oqimi yoqilganida, OpenClaw jo‘natishdan oldin **ketma-ket blok chunklarni birlashtirishi** mumkin. Bu progressiv chiqishni saqlagan holda “bir qatorli spam”ni kamaytiradi.

- Birlashtirish flush qilishdan oldin **bo‘sh (idle) tanaffuslar**ni (`idleMs`) kutadi.
- Buferlar `maxChars` bilan cheklanadi va undan oshsa flush qilinadi.
- `minChars` yetarli matn to‘planguncha juda kichik bo‘laklar jo‘natilishini oldini oladi
  (yakuniy flush har doim qolgan matnni yuboradi).
- Birlashtirgich `blockStreamingChunk.breakPreference` dan olinadi
  (`paragraph` → `\n\n`, `newline` → `\n`, `sentence` → bo‘sh joy).
- Kanal bo‘yicha override’lar `*.blockStreamingCoalesce` orqali mavjud (hisob bo‘yicha sozlamalarni ham o‘z ichiga oladi).
- Standart coalesce `minChars` Signal/Slack/Discord uchun override qilinmasa 1500 ga oshiriladi.

## Bloklar orasida odamga o‘xshash tempo

Blok oqimi yoqilganda, birinchi blokdan keyin
blok javoblari orasiga **tasodifiy pauza** qo‘shishingiz mumkin. Bu ko‘p-pufakli javoblarni
yanada tabiiy his qildiradi.

- Sozlama: `agents.defaults.humanDelay` (har bir agent uchun `agents.list[].humanDelay` orqali override qilinadi).
- Rejimlar: `off` (standart), `natural` (800–2500ms), `custom` (`minMs`/`maxMs`).
- Faqat **blok javoblari**ga tatbiq etiladi, yakuniy javoblar yoki vosita xulosalariga emas.

## “Chunklarni oqimda yuborish yoki hammasini biryo‘la”

Bu quyidagiga mos keladi:

- **Chunklarni oqimda yuborish:** `blockStreamingDefault: "on"` + `blockStreamingBreak: "text_end"` (jarayon davomida chiqaradi). Telegram bo‘lmagan kanallar ham `*.blockStreaming: true` ni talab qiladi.
- **Hammasini oxirida yuborish:** `blockStreamingBreak: "message_end"` (bir marta flush, juda uzun bo‘lsa bir nechta chunk bo‘lishi mumkin).
- **Blok oqimi yo‘q:** `blockStreamingDefault: "off"` (faqat yakuniy javob).

**Kanal eslatmasi:** Telegram bo‘lmagan kanallarda blok oqimi **o‘chiq**, agar
`*.blockStreaming` aniq `true` qilib qo‘yilmagan bo‘lsa. Telegram qoralama (draft)larni oqimda yubora oladi
(`channels.telegram.streamMode`) blok javoblarsiz.

Sozlama joylashuvi eslatmasi: `blockStreaming*` standartlari
ildiz konfiguratsiyada emas, `agents.defaults` ostida joylashgan.

## Telegram qoralama oqimi (token’ga o‘xshash)

Telegram qoralama oqimiga ega yagona kanal:

- Bot API `sendMessageDraft` dan **mavzulari bor shaxsiy chatlar**da foydalanadi.
- `channels.telegram.streamMode: "partial" | "block" | "off"`.
  - `partial`: so‘nggi oqim matni bilan qoralama yangilanadi.
  - `block`: qoralama bo‘laklangan bloklarda yangilanadi (xuddi shu chunker qoidalari).
  - `off`: qoralama oqimi yo‘q.
- Qoralama chunk sozlamasi (faqat `streamMode: "block"` uchun): `channels.telegram.draftChunk` (standartlar: `minChars: 200`, `maxChars: 800`).
- Qoralama oqimi blok oqimidan alohida; blok javoblari standart bo‘yicha o‘chiq va Telegram bo‘lmagan kanallarda faqat `*.blockStreaming: true` bilan yoqiladi.
- Yakuniy javob baribir oddiy xabar bo‘ladi.
- `/reasoning stream` mantiqni qoralama pufagiga yozadi (faqat Telegram).

Qoralama oqimi faol bo‘lsa, OpenClaw ikki marta oqim bo‘lishining oldini olish uchun o‘sha javobda blok oqimini o‘chiradi.

```
Telegram (shaxsiy + mavzular)
  └─ sendMessageDraft (qoralama pufagi)
       ├─ streamMode=partial → so‘nggi matnni yangilash
       └─ streamMode=block   → qoralamani chunker bilan yangilash
  └─ yakuniy javob → oddiy xabar
```

Afsona:

- 1. `sendMessageDraft`: Telegram qoralama pufagi (haqiqiy xabar emas).
- 2. `final reply`: oddiy Telegram xabari yuborilishi.
