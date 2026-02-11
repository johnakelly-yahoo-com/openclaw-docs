---
summary: "5. OpenClaw xotirasi qanday ishlaydi (workspace fayllari + avtomatik xotira flush)"
read_when:
  - 6. Siz xotira fayllari joylashuvi va ish jarayonini xohlaysiz
  - 7. Siz avtomatik pre-kompaktsiya xotira flush’ini sozlamoqchisiz
---

# 8. Xotira

OpenClaw memory is **plain Markdown in the agent workspace**. Fayllar — haqiqatning yagona manbai; model faqat diskka yozilgan narsalarnigina "eslab qoladi".

11. Xotira qidiruv vositalari faol xotira plagini tomonidan taqdim etiladi (standart: `memory-core`). 12. Xotira plaginlarini `plugins.slots.memory = "none"` bilan o‘chiring.

## 13. Xotira fayllari (Markdown)

Standart ish muhiti joylashuvi ikki xotira qatlamidan foydalanadi:

- 15. `memory/YYYY-MM-DD.md`
  - 16. Kundalik jurnal (faqat qo‘shib boriladi).
  - 17. Sessiya boshida bugun + kecha o‘qiladi.
- 18. `MEMORY.md` (ixtiyoriy)
  - Saralangan uzoq muddatli xotira.
  - 20. **Faqat asosiy, shaxsiy sessiyada yuklanadi** (hech qachon guruh kontekstlarida emas).

21. Bu fayllar workspace ostida joylashgan (`agents.defaults.workspace`, standart `~/.openclaw/workspace`). 22. To‘liq tuzilma uchun [Agent workspace](/concepts/agent-workspace) ga qarang.

## 23. Qachon xotiraga yozish

- 24. Qarorlar, afzalliklar va barqaror faktlar `MEMORY.md` ga yoziladi.
- 25. Kundalik eslatmalar va davomiy kontekst `memory/YYYY-MM-DD.md` ga yoziladi.
- 26. Agar kimdir “buni eslab qol” desa, uni yozib qo‘ying (RAM’da saqlamang).
- 27. Bu soha hali ham rivojlanmoqda. 28. Modelga xotirani saqlashni eslatib turish foydali; u nima qilishni biladi.
- 29. Agar biror narsa mustahkam saqlanishini istasangiz, **botdan uni xotiraga yozishni so‘rang**.

## 30. Avtomatik xotira flush (pre-kompaktsiya ping)

31. Sessiya **avto-kompaktsiyaga yaqinlashganda**, OpenClaw **jim, agentlik burilishi**ni ishga tushiradi va kontekst ixchamlashtirilishidan **oldin** barqaror xotirani yozishni eslatadi. 32. Standart promptlar model _javob berishi mumkin_ligini aniq aytadi, ammo odatda `NO_REPLY` to‘g‘ri javob bo‘ladi, shunda foydalanuvchi bu burilishni ko‘rmaydi.

33. Bu `agents.defaults.compaction.memoryFlush` orqali boshqariladi:

```json5
34. {
  agents: {
    defaults: {
      compaction: {
        reserveTokensFloor: 20000,
        memoryFlush: {
          enabled: true,
          softThresholdTokens: 4000,
          systemPrompt: "Session nearing compaction. Store durable memories now.",
          prompt: "Write any lasting notes to memory/YYYY-MM-DD.md; reply with NO_REPLY if nothing to store.",
        },
      },
    },
  },
}
```

35. Tafsilotlar:

- 36. **Yumshoq chegarasi**: flush sessiya tokenlar taxmini `contextWindow - reserveTokensFloor - softThresholdTokens` dan oshganda ishga tushadi.
- 37. **Jim** standart holatda: promptlar `NO_REPLY` ni o‘z ichiga oladi, shuning uchun hech narsa yetkazilmaydi.
- 38. **Ikki prompt**: foydalanuvchi prompti va tizim prompti eslatmani qo‘shib yuboradi.
- 39. **Har bir kompaktsiya sikliga bitta flush** (`sessions.json` da kuzatiladi).
- 40. **Workspace yoziladigan bo‘lishi kerak**: agar sessiya `workspaceAccess: "ro"` yoki `"none"` bilan sandbox’da ishlasa, flush o‘tkazib yuboriladi.

To‘liq siqish hayotiy sikli uchun qarang:

## 42. Vektorli xotira qidiruvi

43. OpenClaw `MEMORY.md` va `memory/*.md` ustida kichik vektor indeksini qurishi mumkin, shunda semantik so‘rovlar ifoda boshqacha bo‘lsa ham bog‘liq yozuvlarni topa oladi.

44. Standart sozlamalar:

- 45. Standart holatda yoqilgan.
- 46. Xotira fayllaridagi o‘zgarishlarni kuzatadi (debounced).
- 47. Standart holatda masofaviy embeddinglardan foydalanadi. 48. Agar `memorySearch.provider` o‘rnatilmagan bo‘lsa, OpenClaw avtomatik tanlaydi:
  1. 49. `local` — agar `memorySearch.local.modelPath` sozlangan bo‘lsa va fayl mavjud bo‘lsa.
  2. 50. `openai` — agar OpenAI kalitini aniqlash mumkin bo‘lsa.
  3. `gemini`, agar Gemini kalitini aniqlash mumkin bo‘lsa.
  4. `voyage`, agar Voyage kalitini aniqlash mumkin bo‘lsa.
  5. Aks holda, sozlanmaguncha xotira qidiruvi o‘chirilgan holatda qoladi.
- Mahalliy rejim node-llama-cpp’dan foydalanadi va `pnpm approve-builds` talab qilinishi mumkin.
- SQLite ichida vektor qidiruvini tezlashtirish uchun (mavjud bo‘lsa) sqlite-vec’dan foydalanadi.

Masofaviy embeddinglar **majburiy ravishda** embedding provayderi uchun API kalitini talab qiladi. OpenClaw
kalitlarni auth profillari, `models.providers.*.apiKey` yoki muhit o‘zgaruvchilaridan aniqlaydi. Codex OAuth faqat chat/completions’ni qamrab oladi va xotira qidiruvi uchun embedding talablarini **qondirmaydi**. Gemini uchun `GEMINI_API_KEY` yoki
`models.providers.google.apiKey` dan foydalaning. Voyage uchun `VOYAGE_API_KEY` yoki
`models.providers.voyage.apiKey` dan foydalaning. Maxsus OpenAI-mos endpoint’dan foydalanganda,
`memorySearch.remote.apiKey` (va ixtiyoriy `memorySearch.remote.headers`) ni sozlang.

### QMD backend (eksperimental)

O‘rnatilgan SQLite indeksatorini [QMD](https://github.com/tobi/qmd) bilan almashtirish uchun
`memory.backend = "qmd"` ni sozlang: bu BM25 + vektorlar + qayta reytinglashni birlashtiruvchi
mahalliy-first qidiruv sidecar’idir. Markdown haqiqatning yagona manbai bo‘lib qoladi; OpenClaw
qidiruv uchun QMD’ga murojaat qiladi. Asosiy nuqtalar:

**Talablar**

- Standart holatda o‘chirilgan. Har bir konfiguratsiya bo‘yicha yoqiladi (`memory.backend = "qmd"`).
- QMD CLI’ni alohida o‘rnating (`bun install -g https://github.com/tobi/qmd` yoki
  relizni yuklab oling) va `qmd` binari gateway’ning `PATH`’ida ekanligiga ishonch hosil qiling.
- QMD kengaytmalarga ruxsat beruvchi SQLite build’ini talab qiladi (macOS’da `brew install sqlite`).
- QMD to‘liq mahalliy tarzda Bun + `node-llama-cpp` orqali ishlaydi va birinchi ishga tushishda
  HuggingFace’dan GGUF modellarini avtomatik yuklab oladi (alohida Ollama demoni talab qilinmaydi).
- Gateway QMD’ni o‘zini-o‘zi ta’minlovchi XDG home’da
  `~/.openclaw/agents/<agentId>/qmd/` ostida ishga tushiradi, buning uchun `XDG_CONFIG_HOME` va
  `XDG_CACHE_HOME` ni sozlaydi.
- OS qo‘llab-quvvatlashi: Bun + SQLite o‘rnatilgach, macOS va Linux darhol ishlaydi. Windows eng yaxshi WSL2 orqali qo‘llab-quvvatlanadi.

**Sidecar qanday ishlaydi**

- Gateway o‘zini-o‘zi ta’minlovchi QMD home’ni
  `~/.openclaw/agents/<agentId>/qmd/` ostida yozadi (konfiguratsiya + kesh + sqlite DB).
- Kolleksiyalar `memory.qmd.paths` dan `qmd collection add` orqali yaratiladi
  (hamda standart ish maydoni xotira fayllari), so‘ng `qmd update` + `qmd embed`
  ishga tushishda va sozlanadigan intervalda (`memory.qmd.update.interval`,
  standart 5 daq) bajariladi.
- Endi ishga tushishdagi yangilash standart bo‘yicha fon rejimida ishlaydi, shunda chat ishga tushishi bloklanmaydi;
  oldingi bloklovchi xatti-harakatni saqlash uchun `memory.qmd.update.waitForBootSync = true` ni sozlang.
- Qidiruvlar `qmd query --json` orqali bajariladi. Agar QMD ishlamay qolsa yoki binar yo‘q bo‘lsa,
  OpenClaw avtomatik ravishda o‘rnatilgan SQLite menejeriga qaytadi, shunda xotira vositalari ishlashda davom etadi.
- OpenClaw hozircha QMD embedding batch-size sozlamalarini ochib bermaydi; batch xatti-harakati
  QMD’ning o‘zi tomonidan boshqariladi.
- **Birinchi qidiruv sekin bo‘lishi mumkin**: birinchi `qmd query` ishga tushirilganda
  QMD mahalliy GGUF modellarini (reranker/query expansion) yuklab olishi mumkin.
  - OpenClaw QMD’ni ishga tushirganda `XDG_CONFIG_HOME`/`XDG_CACHE_HOME` ni avtomatik sozlaydi.
  - Agar modellarni qo‘lda oldindan yuklab olishni xohlasangiz (va OpenClaw ishlatadigan ayni indeksni qizdirsangiz),
    agentning XDG kataloglari bilan bir martalik so‘rovni ishga tushiring.

    OpenClaw’ning QMD holati **state dir** ostida joylashadi (standart `~/.openclaw`).
    Xuddi shu indeksga `qmd` ni yo‘naltirish uchun OpenClaw ishlatadigan XDG o‘zgaruvchilarini eksport qilishingiz mumkin:

    ```bash
    # Pick the same state dir OpenClaw uses
    STATE_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
    if [ -d "$HOME/.moltbot" ] && [ ! -d "$HOME/.openclaw" ] \
      && [ -z "${OPENCLAW_STATE_DIR:-}" ]; then
      STATE_DIR="$HOME/.moltbot"
    fi

    export XDG_CONFIG_HOME="$STATE_DIR/agents/main/qmd/xdg-config"
    export XDG_CACHE_HOME="$STATE_DIR/agents/main/qmd/xdg-cache"

    # (Optional) force an index refresh + embeddings
    qmd update
    qmd embed

    # Warm up / trigger first-time model downloads
    qmd query "test" -c memory-root --json >/dev/null 2>&1
    ```

**Konfiguratsiya sathi (`memory.qmd.*`)**

- `command` (standart `qmd`): bajariladigan fayl yo‘lini almashtirish.
- `includeDefaultMemory` (standart `true`): `MEMORY.md` + `memory/**/*.md` ni avtomatik indekslash.
- `paths[]`: qo‘shimcha kataloglar/fayllarni qo‘shish (`path`, ixtiyoriy `pattern`, ixtiyoriy
  barqaror `name`).
- `sessions`: sessiya JSONL indekslashiga qo‘shilish (`enabled`, `retentionDays`,
  `exportDir`).
- `update`: yangilash davriyligi va texnik xizmat bajarilishini boshqaradi:
  (`interval`, `debounceMs`, `onBoot`, `waitForBootSync`, `embedInterval`,
  `commandTimeoutMs`, `updateTimeoutMs`, `embedTimeoutMs`).
- `limits`: recall yuklamasini cheklash (`maxResults`, `maxSnippetChars`,
  `maxInjectedChars`, `timeoutMs`).
- `scope`: [`session.sendPolicy`](/gateway/configuration#session) bilan bir xil sxema.
  Standart holatda faqat DM (`deny` hammasi, `allow` to‘g‘ridan-to‘g‘ri chatlar);
  guruhlar/kanallarda QMD natijalarini ko‘rsatish uchun uni bo‘shating.
- 43. Jo‘natuvchi E.164 (masalan `+15551234567`) bo‘yicha `peer.kind: "direct"` bilan moslang.
- Ish maydonidan tashqaridan olingan snippet’lar `memory_search` natijalarida
  `qmd/<collection>/<relative-path>` ko‘rinishida paydo bo‘ladi; `memory_get`
  bu prefiksni tushunadi va sozlangan QMD kolleksiya ildizidan o‘qiydi.
- `memory.qmd.sessions.enabled = true` bo‘lganda, OpenClaw tozalangan sessiya
  transkriptlarini (User/Assistant navbatlari) alohida QMD kolleksiyasiga
  `~/.openclaw/agents/<id>/qmd/sessions/` ostiga eksport qiladi, shunda `memory_search`
  o‘rnatilgan SQLite indeksiga tegmasdan yaqinda bo‘lgan suhbatlarni eslab qolishi mumkin.
- `memory_search` snippet’lari endi `memory.citations` `auto`/`on` bo‘lganda
  `Source: <path#line>` pastki izohini o‘z ichiga oladi; yo‘l metama’lumotini ichki
  saqlab qolish uchun `memory.citations = "off"` ni sozlang (agent baribir
  `memory_get` uchun yo‘lni oladi, ammo snippet matni pastki izohsiz bo‘ladi va tizim prompti
  agentni uni keltirmaslik haqida ogohlantiradi).

**Misol**

```json5
memory: {
  backend: "qmd",
  citations: "auto",
  qmd: {
    includeDefaultMemory: true,
    update: { interval: "5m", debounceMs: 15000 },
    limits: { maxResults: 6, timeoutMs: 4000 },
    scope: {
      default: "deny",
      rules: [{ action: "allow", match: { chatType: "direct" } }]
    },
    paths: [
      { name: "docs", path: "~/notes", pattern: "**/*.md" }
    ]
  }
}
```

**Iqtiboslar va zaxira (fallback)**

- `memory.citations` backend’dan qat’i nazar qo‘llanadi (`auto`/`on`/`off`).
- `qmd` ishga tushganda, diagnostika natijalarni qaysi dvigatel berganini ko‘rsatishi uchun `status().backend = "qmd"` deb belgilaymiz. Agar QMD subprocessi to‘xtasa yoki JSON chiqishini tahlil qilib bo‘lmasa, qidiruv menejeri ogohlantirishni logga yozadi va QMD tiklanguncha o‘rnatilgan provayderni (mavjud Markdown embeddinglari) qaytaradi.

### Qo‘shimcha xotira yo‘llari

Agar standart ish maydoni tuzilmasidan tashqaridagi Markdown fayllarni indekslashni istasangiz, aniq yo‘llarni qo‘shing:

```json5
agents: {
  defaults: {
    memorySearch: {
      extraPaths: ["../team-docs", "/srv/shared-notes/overview.md"]
    }
  }
}
```

Eslatmalar:

- Yo‘llar mutlaq yoki ish maydoniga nisbatan bo‘lishi mumkin.
- Kataloglar `.md` fayllar uchun rekursiv tarzda skan qilinadi.
- Faqat Markdown fayllari indekslanadi.
- Symlinklar (fayl yoki kataloglar) e’tiborga olinmaydi.

### Gemini embeddinglari (mahalliy)

Gemini embeddinglari API’sidan bevosita foydalanish uchun provayderni `gemini` ga sozlang:

```json5
agents: {
  defaults: {
    memorySearch: {
      provider: "gemini",
      model: "gemini-embedding-001",
      remote: {
        apiKey: "YOUR_GEMINI_API_KEY"
      }
    }
  }
}
```

Eslatmalar:

- `remote.baseUrl` ixtiyoriy (standart bo‘yicha Gemini API bazaviy URL’i).
- `remote.headers` kerak bo‘lsa qo‘shimcha sarlavhalarni qo‘shish imkonini beradi.
- Standart model: `gemini-embedding-001`.

Agar **OpenAI-ga mos maxsus endpoint** (OpenRouter, vLLM yoki proksi) dan foydalanmoqchi bo‘lsangiz, OpenAI provayderi bilan `remote` konfiguratsiyasidan foydalanishingiz mumkin:

```json5
agents: {
  defaults: {
    memorySearch: {
      provider: "openai",
      model: "text-embedding-3-small",
      remote: {
        baseUrl: "https://api.example.com/v1/",
        apiKey: "YOUR_OPENAI_COMPAT_API_KEY",
        headers: { "X-Custom-Header": "value" }
      }
    }
  }
}
```

Agar API kalitini sozlashni istamasangiz, `memorySearch.provider = "local"` dan foydalaning yoki `memorySearch.fallback = "none"` qilib qo‘ying.

Zaxira (fallback)lar:

- `memorySearch.fallback` `openai`, `gemini`, `local` yoki `none` bo‘lishi mumkin.
- Zaxira provayder faqat asosiy embedding provayderi ishlamay qolganda qo‘llanadi.

Paketli indekslash (OpenAI + Gemini):

- OpenAI va Gemini embeddinglari uchun standart bo‘yicha yoqilgan. O‘chirish uchun `agents.defaults.memorySearch.remote.batch.enabled = false` ni sozlang.
- Standart xatti-harakat paket yakunlanishini kutadi; kerak bo‘lsa `remote.batch.wait`, `remote.batch.pollIntervalMs` va `remote.batch.timeoutMinutes` ni sozlang.
- Bir vaqtda nechta paketli ish yuborilishini boshqarish uchun `remote.batch.concurrency` ni sozlang (standart: 2).
- Paket rejimi `memorySearch.provider = "openai"` yoki `"gemini"` bo‘lganda qo‘llanadi va mos API kalitidan foydalanadi.
- Gemini paketli ishlar async embedding batch endpoint’dan foydalanadi va Gemini Batch API mavjud bo‘lishini talab qiladi.

Nega OpenAI paketi tez va arzon:

- Katta hajmdagi backfilllar uchun OpenAI odatda biz qo‘llab-quvvatlaydigan eng tez variant, chunki ko‘plab embedding so‘rovlarini bitta paketli ishda yuborib, ularni OpenAI tomonidan asinxron qayta ishlashga topshira olamiz.
- OpenAI Batch API ish yuklamalari uchun chegirmali narxlarni taklif qiladi, shuning uchun katta indekslash ishlarida bir xil so‘rovlarni sinxron yuborishga qaraganda odatda arzonroq bo‘ladi.
- Batafsil ma’lumot uchun OpenAI Batch API hujjatlari va narxlariga qarang:
  - https://platform.openai.com/docs/api-reference/batch
  - https://platform.openai.com/pricing

Konfiguratsiya namunasi:

```json5
agents: {
  defaults: {
    memorySearch: {
      provider: "openai",
      model: "text-embedding-3-small",
      fallback: "openai",
      remote: {
        batch: { enabled: true, concurrency: 2 }
      },
      sync: { watch: true }
    }
  }
}
```

Asboblar:

- `memory_search` — fayl va satr diapazonlari bilan snippetlarni qaytaradi.
- `memory_get` — yo‘l bo‘yicha xotira fayli mazmunini o‘qish.

Mahalliy rejim:

- `agents.defaults.memorySearch.provider = "local"` qilib sozlang.
- `agents.defaults.memorySearch.local.modelPath` ni taqdim eting (GGUF yoki `hf:` URI).
- Ixtiyoriy: masofaviy zaxiraga o‘tishni oldini olish uchun `agents.defaults.memorySearch.fallback = "none"` ni sozlang.

### Xotira asboblari qanday ishlaydi

- `memory_search` `MEMORY.md` + `memory/**/*.md` dan Markdown bo‘laklarini (~400 token maqsad, 80-token overlap) semantik qidiradi. 1. U parcha matnini (taxminan ~700 belgigacha cheklangan), fayl yo‘li, qatorlar oralig‘i, ball, provayder/model va lokal → masofaviy embeddinglarga qaytish bo‘lgan-bo‘lmaganini qaytaradi. 2. To‘liq fayl yuklamasi qaytarilmaydi.
- 3. `memory_get` ma’lum bir xotira Markdown faylini (workspace-ga nisbiy) o‘qiydi, ixtiyoriy ravishda boshlang‘ich qatordan va N qator uchun. [Session management + compaction](/reference/session-management-compaction).
- 5. Ikkala vosita ham faqat `memorySearch.enabled` agent uchun true bo‘lib hal bo‘lganda yoqiladi.

### 6. Nimalar indekslanadi (va qachon)

- 7. Fayl turi: faqat Markdown (`MEMORY.md`, `memory/**/*.md`).
- 8. Indeks saqlanishi: har bir agent uchun SQLite `~/.openclaw/memory/<agentId>.sqlite` da ( `agents.defaults.memorySearch.store.path` orqali sozlanadi, `{agentId}` tokenini qo‘llab-quvvatlaydi).
- 9. Yangilanish: `MEMORY.md` + `memory/` uchun kuzatuvchi indeksni “iflos” deb belgilaydi (debounce 1.5s). 10. Sinxronlash sessiya boshlanishida, qidiruvda yoki interval bo‘yicha rejalashtiriladi va asinxron ishlaydi. 11. Sessiya transkriptlari fon sinxronlashni ishga tushirish uchun delta chegaralaridan foydalanadi.
- 12. Qayta indekslash triggerlari: indeks embedding **provayder/model + endpoint fingerprint + bo‘laklash (chunking) parametrlari** ni saqlaydi. `MEMORY.md` / `memory/` tashqarisidagi yo‘llar rad etiladi.

### Agar ulardan birortasi o‘zgarsa, OpenClaw avtomatik ravishda butun omborni qayta tiklaydi va qayta indekslaydi.

15. Yoqilganda, OpenClaw quyidagilarni birlashtiradi:

- Gibrid qidiruv (BM25 + vektor)
- 17. **BM25 kalit-so‘z dolzarbligi** (IDlar, muhit o‘zgaruvchilari, kod belgilariga o‘xshash aniq tokenlar)

18. Agar platformangizda to‘liq matnli qidiruv mavjud bo‘lmasa, OpenClaw faqat vektorli qidiruvga qaytadi.

#### 19. Nega gibrid?

20. Vektorli qidiruv “bu xuddi shu ma’noni anglatadi” holatlarida juda zo‘r:

- 21. “Mac Studio gateway host” va “gateway’ni ishga tushirayotgan mashina”
- 22. “debounce file updates” va “har bir yozishda indekslashdan qochish”

23. Ammo u aniq, yuqori signalga ega tokenlarda kuchsiz bo‘lishi mumkin:

- 24. IDlar (`a828e60`, `b3b9895a…`)
- 25. kod belgilari (`memorySearch.query.hybrid`)
- 26. xato satrlari (“sqlite-vec unavailable”)

27. BM25 (to‘liq matn) buning teskarisi: aniq tokenlarda kuchli, parafrazalarda kuchsizroq.
28. Gibrid qidiruv — amaliy o‘rtacha yechim: **ikkala retrieval signalidan foydalanish**, shunda ham “tabiiy til” so‘rovlari, ham “pichan ichidagi igna” so‘rovlari uchun yaxshi natijalar olinadi.

#### 29. Natijalarni qanday birlashtiramiz (joriy dizayn)

30. Amalga oshirish eskizi:

1. 31. Har ikki tomondan nomzodlar havzasini olish:

- 32) **Vektor**: kosinus o‘xshashligi bo‘yicha `maxResults * candidateMultiplier` ta eng yuqori natija.
- 33. **BM25**: FTS5 BM25 reytingi bo‘yicha `maxResults * candidateMultiplier` ta eng yuqori natija (kichikroq — yaxshiroq).

2. 34. BM25 reytingini 0..1 ga o‘xshash ballga aylantirish:

- 35) `textScore = 1 / (1 + max(0, bm25Rank))`

3. 36. Nomzodlarni bo‘lak (chunk) ID bo‘yicha birlashtirib, og‘irliklangan ballni hisoblash:

- 37) `finalScore = vectorWeight * vectorScore + textWeight * textScore`

38. Izohlar:

- 39. `vectorWeight` + `textWeight` konfiguratsiyani hal qilishda 1.0 ga normallashtiriladi, shuning uchun og‘irliklar foiz sifatida ishlaydi.
- 40. Agar embeddinglar mavjud bo‘lmasa (yoki provayder nol-vektor qaytarsa), biz baribir BM25 ni ishga tushiramiz va kalit-so‘z mosliklarini qaytaramiz.
- 41. Agar FTS5 yaratilmasa, vektor-only qidiruvni saqlab qolamiz (qat’iy xato yo‘q).

42. Bu “IR-nazariya bo‘yicha mukammal” emas, lekin sodda, tez va real yozuvlarda eslab qolish/aniqlikni yaxshilashga moyil.
43. Keyinroq yanada murakkablashtirmoqchi bo‘lsak, odatiy keyingi qadamlar — Reciprocal Rank Fusion (RRF) yoki aralashtirishdan oldin ballarni normallashtirish (min/max yoki z-score).

44. Konfiguratsiya:

````json5
45. ```
agents: {
  defaults: {
    memorySearch: {
      query: {
        hybrid: {
          enabled: true,
          vectorWeight: 0.7,
          textWeight: 0.3,
          candidateMultiplier: 4
        }
      }
    }
  }
}
```
````

### 46. Embedding keshi

47. OpenClaw **bo‘lak embeddinglari**ni SQLite’da keshlashi mumkin, shunda qayta indekslash va tez-tez yangilanishlar (ayniqsa sessiya transkriptlari) o‘zgarmagan matnni qayta embedding qilmaydi.

48. Konfiguratsiya:

````json5
49. ```
agents: {
  defaults: {
    memorySearch: {
      cache: {
        enabled: true,
        maxEntries: 50000
      }
    }
  }
}
```
````

### 50. Sessiya xotirasi bo‘yicha qidiruv (eksperimental)

1. Ixtiyoriy ravishda **sessiya transkriptlari**ni indekslashingiz va ularni `memory_search` orqali ko‘rsatishingiz mumkin.
2. Bu tajriba (experimental) flagi ortida yashiringan.

```json5
3. agents: {
  defaults: {
    memorySearch: {
      experimental: { sessionMemory: true },
      sources: ["memory", "sessions"]
    }
  }
}
```

4. Eslatmalar:

- 5. Sessiyani indekslash **ixtiyoriy** (sukut bo‘yicha o‘chiq).
- 6. Sessiya yangilanishlari debounce qilinadi va delta chegaralaridan oshgach **asinxron tarzda indekslanadi** (best-effort).
- 7. `memory_search` hech qachon indekslashni kutib turmaydi; fon sinxronlash tugaguncha natijalar biroz eskirgan bo‘lishi mumkin.
- 8. Natijalar hanuz faqat parchalarni (snippets) o‘z ichiga oladi; `memory_get` faqat xotira fayllari bilan cheklangan.
- 9. Sessiya indekslash har bir agent uchun alohida (faqat o‘sha agentning sessiya jurnallari indekslanadi).
- 10. Sessiya jurnallari diskda joylashadi (`~/.openclaw/agents/<agentId>/sessions/*.jsonl`). 11. Fayl tizimiga kirish huquqiga ega bo‘lgan har qanday jarayon/foydalanuvchi ularni o‘qishi mumkin, shuning uchun diskka kirishni ishonch chegarasi sifatida ko‘ring. 12. Qattiqroq izolyatsiya uchun agentlarni alohida OS foydalanuvchilari yoki xostlar ostida ishga tushiring.

13. Delta chegaralari (ko‘rsatilgan sukut bo‘yicha qiymatlar):

```json5
14. agents: {
  defaults: {
    memorySearch: {
      sync: {
        sessions: {
          deltaBytes: 100000,   // ~100 KB
          deltaMessages: 50     // JSONL lines
        }
      }
    }
  }
}
```

### 15. SQLite vektor tezlatilishi (sqlite-vec)

16. sqlite-vec kengaytmasi mavjud bo‘lganda, OpenClaw embeddinglarni
    SQLite virtual jadvalida (`vec0`) saqlaydi va vektor masofa so‘rovlarini
    ma’lumotlar bazasida bajaradi. 17. Bu barcha embeddinglarni JS ichiga yuklamasdan qidiruvni tez saqlaydi.

18. Konfiguratsiya (ixtiyoriy):

```json5
19. agents: {
  defaults: {
    memorySearch: {
      store: {
        vector: {
          enabled: true,
          extensionPath: "/path/to/sqlite-vec"
        }
      }
    }
  }
}
```

20. Eslatmalar:

- 21. `enabled` sukut bo‘yicha true; o‘chirilganda qidiruv saqlangan embeddinglar ustida jarayon ichidagi kosinus o‘xshashligiga qaytadi.
- 22. Agar sqlite-vec kengaytmasi yo‘q bo‘lsa yoki yuklanmasa, OpenClaw xatoni logga yozadi va JS fallback bilan davom etadi (vektor jadvalsiz).
- 23. `extensionPath` biriktirilgan sqlite-vec yo‘lini bekor qiladi (maxsus buildlar yoki noodatiy o‘rnatish joylari uchun foydali).

### 24. Mahalliy embeddingni avtomatik yuklab olish

- 25. Sukut bo‘yicha mahalliy embedding modeli: `hf:ggml-org/embeddinggemma-300M-GGUF/embeddinggemma-300M-Q8_0.gguf` (~0.6 GB).
- 26. `memorySearch.provider = "local"` bo‘lganda, `node-llama-cpp` `modelPath`ni aniqlaydi; agar GGUF yo‘q bo‘lsa, u **avtomatik yuklab olinadi** (keshga yoki `local.modelCacheDir` o‘rnatilgan bo‘lsa o‘sha joyga), so‘ng yuklanadi. 27. Yuklab olishlar qayta urinishda davom ettiriladi.
- 28. Native build talabi: `pnpm approve-builds`ni ishga tushiring, `node-llama-cpp`ni tanlang, so‘ng `pnpm rebuild node-llama-cpp`.
- 29. Fallback: agar mahalliy sozlama muvaffaqiyatsiz bo‘lsa va `memorySearch.fallback = "openai"` bo‘lsa, biz avtomatik ravishda masofaviy embeddinglarga o‘tamiz (`openai/text-embedding-3-small`, agar o‘zgartirilmagan bo‘lsa) va sababini qayd etamiz.

### 30. Maxsus OpenAI-mos endpoint misoli

```json5
31. agents: {
  defaults: {
    memorySearch: {
      provider: "openai",
      model: "text-embedding-3-small",
      remote: {
        baseUrl: "https://api.example.com/v1/",
        apiKey: "YOUR_REMOTE_API_KEY",
        headers: {
          "X-Organization": "org-id",
          "X-Project": "project-id"
        }
      }
    }
  }
}
```

32. Eslatmalar:

- 33. `remote.*` `models.providers.openai.*`dan ustun turadi.
- 34. `remote.headers` OpenAI headerlari bilan birlashtiriladi; kalitlar to‘qnashganda remote ustun bo‘ladi. 35. OpenAI sukut bo‘yicha qiymatlaridan foydalanish uchun `remote.headers`ni tashlab yuboring.
