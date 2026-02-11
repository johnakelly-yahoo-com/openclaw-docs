---
summary: "How OpenClaw builds prompt context and reports token usage + costs"
read_when:
  - Explaining token usage, costs, or context windows
  - Debugging context growth or compaction behavior
title: "Token Use and Costs"
---

# Token use & costs

OpenClaw tracks **tokens**, not characters. Tokens are model-specific, but most
OpenAI-style models average ~4 characters per token for English text.

## How the system prompt is built

OpenClaw assembles its own system prompt on every run. It includes:

- Asboblar roʻyxati + qisqa tavsiflar
- Skills list (only metadata; instructions are loaded on demand with `read`)
- Oʻzini-oʻzi yangilash boʻyicha koʻrsatmalar
- Workspace + bootstrap fayllari (`AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`, yangi boʻlsa `BOOTSTRAP.md`). Katta fayllar `agents.defaults.bootstrapMaxChars` (standart: 20000) orqali qisqartiriladi.
- Vaqt (UTC + foydalanuvchi vaqt zonasi)
- Javob teglar + heartbeat xatti-harakati
- Runtime metamaʼlumotlari (host/OS/model/thinking)

[System Prompt](/concepts/system-prompt) ichida toʻliq tafsilotni koʻring.

## Kontekst oynasida nimalar hisobga olinadi

Model oladigan hamma narsa kontekst limitiga hisoblanadi:

- System prompt (yuqorida sanab oʻtilgan barcha boʻlimlar)
- Suhbat tarixi (foydalanuvchi + yordamchi xabarlari)
- Asbob chaqiruvlari va asbob natijalari
- Ilovalar/transkriptlar (rasmlar, audio, fayllar)
- Siqish xulosalari va kesib tashlangan artefaktlar
- Provayder o‘ramlari yoki xavfsizlik sarlavhalari (ko‘rinmaydi, ammo baribir hisobga olinadi)

Amaliy tafsilotlar (har bir kiritilgan fayl, tool, skill va system prompt hajmi boʻyicha) uchun `/context list` yoki `/context detail` dan foydalaning. [Context](/concepts/context) ni ko‘ring.

## Joriy token sarfini qanday koʻrish

Bularni chatda ishlating:

- `/status` → sessiya modeli, kontekst sarfi, oxirgi javobning input/output tokenlari va **taxminiy narx**ni (faqat API kalitida) koʻrsatadigan **emoji‑ga boy status kartasi**.
- `/usage off|tokens|full` → har bir javobga **har‑javob uchun usage footer** qoʻshadi.
  - Sessiya boʻyicha saqlanadi ( `responseUsage` sifatida ).
  - OAuth autentifikatsiyasi **narxni yashiradi** (faqat tokenlar).
- `/usage cost` → OpenClaw sessiya loglaridan olingan mahalliy narx xulosasini koʻrsatadi.

Boshqa interfeyslar:

- **TUI/Web TUI:** `/status` + `/usage` qoʻllab‑quvvatlanadi.
- **CLI:** `openclaw status --usage` va `openclaw channels list` provayder kvota oynalarini koʻrsatadi (har‑javob narxlari emas).

## Narxni baholash (koʻrsatilganda)

Narxlar modelingizning pricing konfiguratsiyasidan baholanadi:

```
models.providers.<provider>.models[].cost
```

Bular `input`, `output`, `cacheRead` va `cacheWrite` uchun **1M token uchun USD** hisoblanadi. Agar pricing mavjud boʻlmasa, OpenClaw faqat tokenlarni koʻrsatadi. OAuth tokenlari hech qachon dollar narxini koʻrsatmaydi.

## Cache TTL va pruning taʼsiri

Provayder prompt cacheʼlash faqat cache TTL oynasi ichida amal qiladi. OpenClaw ixtiyoriy ravishda **cache‑ttl pruning**ni ishga tushirishi mumkin: cache TTL muddati tugagach sessiyani qisqartiradi, soʻng cache oynasini qayta oʻrnatadi, shunda keyingi soʻrovlar butun tarixni qayta cacheʼlash oʻrniga yangi cacheʼlangan kontekstdan foydalana oladi. Bu sessiya TTL dan keyin bekor turganda cache write xarajatlarini pastroq ushlab turadi.

[Gateway configuration](/gateway/configuration) da sozlang va xatti‑harakat tafsilotlarini [Session pruning](/concepts/session-pruning) da koʻring.

Heartbeat bekor turish oraligʻida cacheʼni **iliq** saqlab turishi mumkin. Agar modelingiz cache TTL `1h` boʻlsa, heartbeat intervalini undan biroz kamroq (masalan, `55m`) qilib belgilash butun promptni qayta cacheʼlashdan qochib, cache write xarajatlarini kamaytiradi.

Anthropic API pricingʼda cache readʼlar input tokenlarga qaraganda ancha arzon, cache writeʼlar esa yuqoriroq multiplikator bilan hisoblanadi. Eng soʻnggi stavkalar va TTL multiplikatorlari uchun Anthropicʼning prompt caching pricingʼini koʻring:
[https://docs.anthropic.com/docs/build-with-claude/prompt-caching](https://docs.anthropic.com/docs/build-with-claude/prompt-caching)

### Misol: heartbeat bilan 1 soatlik cacheʼni iliq saqlash

```yaml
agents:
  defaults:
    model:
      primary: "anthropic/claude-opus-4-6"
    models:
      "anthropic/claude-opus-4-6":
        params:
          cacheRetention: "long"
    heartbeat:
      every: "55m"
```

## Token bosimini kamaytirish bo‘yicha maslahatlar

- Uzoq sessiyalarni qisqartirish uchun `/compact` dan foydalaning.
- Ish jarayonlaringizda katta tool chiqishlarini qisqartiring.
- Skill tavsiflarini qisqa saqlang (skill roʻyxati promptga kiritiladi).
- Keng qamrovli, izlanishli ishlar uchun kichikroq modellarni afzal ko‘ring.

Aniq skill roʻyxati ustama formulasi uchun [Skills](/tools/skills) ni koʻring.
