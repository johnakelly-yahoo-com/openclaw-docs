---
summary: "Tadqiqot qaydlari: Clawd ish joylari uchun oflayn xotira tizimi (Markdown — manba-haqiqat + hosila indeks)"
read_when:
  - Kundalik Markdown jurnallaridan tashqarida ish joyi xotirasini loyihalash (~/.openclaw/workspace)
  - Deciding: mustaqil CLI va chuqur OpenClaw integratsiyasi
  - Oflayn eslab qolish + refleksiya qo‘shish (saqlash/eslash/refleksiya)
title: "Workspace Memory tadqiqoti"
---

# Workspace Memory v2 (oflayn): tadqiqot qaydlari

Maqsad: Clawd uslubidagi ish joyi (`agents.defaults.workspace`, standart `~/.openclaw/workspace`), bu yerda “xotira” har bir kun uchun bitta Markdown faylida (`memory/YYYY-MM-DD.md`) hamda bir nechta barqaror fayllarda (masalan, `memory.md`, `SOUL.md`) saqlanadi.

Ushbu hujjat Markdown’ni ko‘rib chiqiladigan, kanonik manba-haqiqat sifatida saqlab qoladigan, biroq hosila indeks orqali **tuzilmali eslash** (qidiruv, entitet xulosalari, ishonch yangilanishlari) ni qo‘shadigan **oflayn-birinchi** xotira arxitekturasini taklif qiladi.

## Nega o‘zgartirish kerak?

Joriy sozlama (kuniga bitta fayl) quyidagilar uchun juda yaxshi:

- “faqat qo‘shib boriladigan” jurnal yuritish
- inson tomonidan tahrirlash
- git asosidagi barqarorlik + audit qilinuvchanlik
- kam ishqalanishli qayd etish (“shunchaki yozib qo‘yish”)

U quyidagilar uchun zaif:

- yuqori darajadagi qayta chaqirish (“X haqida nimaga kelishgandik?”, “oxirgi marta Y ni qachon sinab ko‘rdik?”)
- ko‘p fayllarni qayta o‘qimasdan entitetga yo‘naltirilgan javoblar (“Alice / The Castle / warelay haqida aytib ber”)
- fikr/afzalliklar barqarorligi (va u o‘zgarganda dalillar)
- vaqt cheklovlari (“2025-yil noyabrida nima to‘g‘ri edi?”) va ziddiyatlarni hal qilish

## Dizayn maqsadlari

- **Oflayn**: tarmoqsiz ishlaydi; noutbukda/Castle’da ishga tushadi; bulutga bog‘liqlik yo‘q.
- **Tushuntiriladigan**: qaytarib olingan elementlar manbaga bog‘lanishi (fayl + joylashuv) va inferensiyadan ajratilishi kerak.
- **Kam marosim**: kundalik yozuvlar Markdown bo‘lib qoladi, og‘ir sxema ishlari yo‘q.
- **Incremental**: v1 is useful with FTS only; semantic/vector and graphs are optional upgrades.
- **Agent-friendly**: makes “recall within token budgets” easy (return small bundles of facts).

## North star model (Hindsight × Letta)

Two pieces to blend:

1. **Letta/MemGPT-style control loop**

- keep a small “core” always in context (persona + key user facts)
- everything else is out-of-context and retrieved via tools
- memory writes are explicit tool calls (append/replace/insert), persisted, then re-injected next turn

2. **Hindsight-style memory substrate**

- separate what’s observed vs what’s believed vs what’s summarized
- support retain/recall/reflect
- confidence-bearing opinions that can evolve with evidence
- entity-aware retrieval + temporal queries (even without full knowledge graphs)

## Proposed architecture (Markdown source-of-truth + derived index)

### Canonical store (git-friendly)

Keep `~/.openclaw/workspace` as canonical human-readable memory.

Suggested workspace layout:

```
~/.openclaw/workspace/
  memory.md                    # small: durable facts + preferences (core-ish)
  memory/
    YYYY-MM-DD.md              # daily log (append; narrative)
  bank/                        # “typed” memory pages (stable, reviewable)
    world.md                   # objective facts about the world
    experience.md              # what the agent did (first-person)
    opinions.md                # subjective prefs/judgments + confidence + evidence pointers
    entities/
      Peter.md
      The-Castle.md
      warelay.md
      ...
```

Notes:

- **Daily log stays daily log**. No need to turn it into JSON.
- The `bank/` files are **curated**, produced by reflection jobs, and can still be edited by hand.
- `memory.md` remains “small + core-ish”: the things you want Clawd to see every session.

### Derived store (machine recall)

Add a derived index under the workspace (not necessarily git tracked):

```
~/.openclaw/workspace/.memory/index.sqlite
```

Back it with:

- SQLite schema for facts + entity links + opinion metadata
- SQLite **FTS5** for lexical recall (fast, tiny, offline)
- Loglar JSONL formatida (har bir qatorda bitta JSON obyekt).

Semantik eslab qolish uchun ixtiyoriy embeddinglar jadvali (hali oflayn).

## Retain / Recall / Reflect (operational loop)

### Retain: normalize daily logs into “facts”

Hindsight’s key insight that matters here: store **narrative, self-contained facts**, not tiny snippets.

Practical rule for `memory/YYYY-MM-DD.md`:

- at end of day (or during), add a `## Retain` section with 2–5 bullets that are:
  - narrative (cross-turn context preserved)
  - self-contained (standalone makes sense later)
  - tagged with type + entity mentions

Example:

```
## Retain
- W @Peter: Currently in Marrakech (Nov 27–Dec 1, 2025) for Andy’s birthday.
- B @warelay: I fixed the Baileys WS crash by wrapping connection.update handlers in try/catch (see memory/2025-11-27.md).
- O(c=0.95) @Peter: Prefers concise replies (&lt;1500 chars) on WhatsApp; long content goes into files.
```

Minimal parsing:

- Type prefix: `W` (world), `B` (experience/biographical), `O` (opinion), `S` (observation/summary; usually generated)
- Entities: `@Peter`, `@warelay`, etc (slugs map to `bank/entities/*.md`)
- Opinion confidence: `O(c=0.0..1.0)` optional

Indeks har doim **Markdown’dan qayta qurilishi mumkin**.

### Recall: queries over the derived index

Recall should support:

- **lexical**: “find exact terms / names / commands” (FTS5)
- **entity**: “tell me about X” (entity pages + entity-linked facts)
- 1. **temporal**: “11-noyabr 27 atrofida nima bo‘ldi” / “o‘tgan haftadan beri”
- 2. **opinion**: “Peter nimani afzal ko‘radi?” 3. (ishonch + dalillar bilan)

4. Qaytarish formati agentlar uchun qulay bo‘lishi va manbalarni keltirishi kerak:

- 5. `kind` (`world|experience|opinion|observation`)
- Agar mualliflar bu haqda o‘ylashini istamasangiz: reflect vazifasi bu punktlarni jurnalning qolgan qismidan chiqarib olishi mumkin, ammo aniq `## Retain` bo‘limiga ega bo‘lish eng oson “sifat richagi”dir.
- 7. `entities` (`["Peter","warelay"]`)
- 8. `content` (bayon qilingan fakt)
- 9. `source` (`memory/2025-11-27.md#L12` va h.k.)

### 10. Refleksiya: barqaror sahifalarni yaratish + e’tiqodlarni yangilash

11. Refleksiya — rejalashtirilgan ish (kunlik yoki heartbeat `ultrathink`) bo‘lib, u:

- 12. so‘nggi faktlar asosida `bank/entities/*.md` ni yangilaydi (entity xulosalari)
- 13. mustahkamlash/qarama-qarshilikka qarab `bank/opinions.md` dagi ishonchni yangilaydi
- 14. ixtiyoriy ravishda `memory.md` ga tahrirlarni taklif qiladi (“core-ish” barqaror faktlar)

15. Fikr evolyutsiyasi (oddiy, tushuntiriladigan):

- 16. har bir fikrda quyidagilar bo‘ladi:
  - 17. bayonot
  - 18. ishonch `c ∈ [0,1]`
  - 19. last_updated
  - `timestamp` (manba kuni yoki mavjud bo‘lsa, ajratib olingan vaqt oralig‘i)
- 21. yangi faktlar kelganda:
  - 22. entity ustma-ustligi + o‘xshashlik bo‘yicha nomzod fikrlarni topish (avval FTS, keyin embeddinglar)
  - 23. ishonchni kichik deltalar bilan yangilash; katta sakrashlar kuchli qarama-qarshilik + takroriy dalillarni talab qiladi

## 24. CLI integratsiyasi: mustaqil vs chuqur integratsiya

25. Tavsiya: **OpenClaw ichida chuqur integratsiya**, lekin ajratiladigan yadro kutubxonasini saqlash.

### 26. Nega OpenClaw ga integratsiya qilish kerak?

- 27. OpenClaw allaqachon biladi:
  - 28. ish joyi yo‘li (`agents.defaults.workspace`)
  - 29. sessiya modeli + heartbeats
  - 30. loglash + nosozliklarni bartaraf etish andozalari
- 31. Asboblarni agentning o‘zi chaqirishini xohlaysiz:
  - 32. `openclaw memory recall "…" --k 25 --since 30d`
  - 33. `openclaw memory reflect --since 7d`

### 34. Nega baribir kutubxonani ajratish kerak?

- 35. xotira mantiğini gateway/runtime bo‘lmasdan testlanadigan saqlash
- dalil havolalari (tasdiqlovchi + qarama-qarshi fakt identifikatorlari)

37. Tuzilishi:

## Xotira asboblari kichik CLI + kutubxona qatlamidan iborat bo‘lishi mo‘ljallangan, ammo bu hozircha faqat tadqiqotdir.

38. “S-Collide” / SuCo: qachon ishlatish (tadqiqot)

39. Agar “S-Collide” **SuCo (Subspace Collision)** ni anglatadigan bo‘lsa: bu kuchli recall/kechikish muvozanatini maqsad qilgan ANN qidiruv yondashuvi bo‘lib, subfazolardagi o‘rganilgan/tuzilmaviy to‘qnashuvlardan foydalanadi (maqola: arXiv 2411.14754, 2024).

- 40. `~/.openclaw/workspace` uchun amaliy yondashuv:
- 41. **boshlamang** SuCo bilan.
- 42. SQLite FTS + (ixtiyoriy) oddiy embeddinglardan boshlang; darhol UX yutuqlarining aksariga erishasiz.
  - 43. SuCo/HNSW/ScaNN turidagi yechimlarni faqat shunda ko‘rib chiqing:
  - 44. korpus katta bo‘lganda (o‘nlab/yuz minglab bo‘laklar)
  - 45. embeddinglarni qo‘pol kuch bilan qidirish juda sekinlashganda

46. recall sifati leksik qidiruv bilan sezilarli darajada cheklanib qolganda

- 47. Offline-ga qulay muqobillar (murakkablik ortib borish tartibida):
- 48. SQLite FTS5 + metadata filtrlari (nol ML)
- 49. Embeddinglar + brute force (bo‘laklar soni kam bo‘lsa, hayratlanarli darajada uzoq ishlaydi)
- SuCo (tadqiqot darajasida; agar ichiga joylashtira oladigan mustahkam implementatsiya bo‘lsa, jozibali)

Ochiq savol:

- sizning qurilmalaringizda (noutbuk + desktop) “shaxsiy yordamchi xotirasi” uchun **eng yaxshi** oflayn embedding modeli qaysi?
  - agar sizda allaqachon Ollama bo‘lsa: lokal model bilan embedding qiling; aks holda toolchain ichiga kichik embedding modelini yuboring.

## Eng kichik foydali pilot

Agar minimal, lekin baribir foydali versiyani xohlasangiz:

- `bank/` entity sahifalarini va kundalik loglarda `## Retain` bo‘limini qo‘shing.
- Iqtiboslar bilan eslab qolish uchun SQLite FTS’dan foydalaning (yo‘l + qator raqamlari).
- Faqatgina recall sifati yoki masshtab talab qilgandagina embedding qo‘shing.

## Manbalar

- Letta / MemGPT tushunchalari: “asosiy xotira bloklari” + “arxiv xotira” + vositalar orqali o‘zini tahrirlovchi xotira.
- Hindsight Texnik Hisoboti: “retain / recall / reflect”, to‘rtta tarmoqli xotira, narrativ faktlarni ajratib olish, fikr ishonchliligining evolyutsiyasi.
- SuCo: arXiv 2411.14754 (2024): “Subspace Collision” taxminiy eng yaqin qo‘shnilarni topish (ANN) orqali retrieval.
