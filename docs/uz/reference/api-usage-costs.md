---
summary: "Audit what can spend money, which keys are used, and how to view usage"
read_when:
  - You want to understand which features may call paid APIs
  - You need to audit keys, costs, and usage visibility
  - You’re explaining /status or /usage cost reporting
title: "API Usage and Costs"
---

# API usage & costs

This doc lists **features that can invoke API keys** and where their costs show up. It focuses on
OpenClaw features that can generate provider usage or paid API calls.

## Where costs show up (chat + CLI)

**Per-session cost snapshot**

- `/status` shows the current session model, context usage, and last response tokens.
- If the model uses **API-key auth**, `/status` also shows **estimated cost** for the last reply.

**Per-message cost footer**

- `/usage full` appends a usage footer to every reply, including **estimated cost** (API-key only).
- `/usage tokens` shows tokens only; OAuth flows hide dollar cost.

**CLI usage windows (provider quotas)**

- `openclaw status --usage` and `openclaw channels list` show provider **usage windows**
  (quota snapshots, not per-message costs).

See [Token use & costs](/reference/token-use) for details and examples.

## How keys are discovered

OpenClaw can pick up credentials from:

- **Auth profiles** (per-agent, stored in `auth-profiles.json`).
- **Environment variables** (e.g. `OPENAI_API_KEY`, `BRAVE_API_KEY`, `FIRECRAWL_API_KEY`).
- **Config** (`models.providers.*.apiKey`, `tools.web.search.*`, `tools.web.fetch.firecrawl.*`,
  `memorySearch.*`, `talk.apiKey`).
- **Skills** (`skills.entries.<name>.apiKey`) which may export keys to the skill process env.

## Features that can spend keys

### 1. Core model responses (chat + tools)

Every reply or tool call uses the **current model provider** (OpenAI, Anthropic, etc). This is the
primary source of usage and cost.

See [Models](/providers/models) for pricing config and [Token use & costs](/reference/token-use) for display.

### 2. Media understanding (audio/image/video)

Inbound media can be summarized/transcribed before the reply runs. This uses model/provider APIs.

- Audio: OpenAI / Groq / Deepgram (now **auto-enabled** when keys exist).
- Image: OpenAI / Anthropic / Google.
- 1. Video: Google.

2. [Media understanding](/nodes/media-understanding) ga qarang.

### 3. 3. Xotira embeddinglari + semantik qidiruv

4. Semantik xotira qidiruvi masofaviy provayderlar uchun sozlanganda **embedding API** laridan foydalanadi:

- 5. `memorySearch.provider = "openai"` → OpenAI embeddinglari
- `memorySearch.provider = "gemini"` → Gemini embeddings
- 7. `memorySearch.provider = "voyage"` → Voyage embeddinglari
- Optional fallback to a remote provider if local embeddings fail

9. `memorySearch.provider = "local"` bilan uni mahalliy holda saqlashingiz mumkin (API ishlatilmaydi).

10. [Memory](/concepts/memory) ga qarang.

### 4. Web search tool (Brave / Perplexity via OpenRouter)

12. `web_search` API kalitlaridan foydalanadi va foydalanish to‘lovlarini keltirib chiqarishi mumkin:

- **Brave Search API**: `BRAVE_API_KEY` or `tools.web.search.apiKey`
- 14. **Perplexity** (OpenRouter orqali): `PERPLEXITY_API_KEY` yoki `OPENROUTER_API_KEY`

15. **Brave bepul darajasi (saxiy):**

- 16. **Oyiga 2 000 so‘rov**
- 17. **Soniyasiga 1 so‘rov**
- 18. Tekshirish uchun **kredit karta talab qilinadi** (yangilamaguningizcha to‘lov olinmaydi)

19. [Web tools](/tools/web) ga qarang.

### 20. 5. Veb fetch vositasi (Firecrawl)

21. `web_fetch` API kaliti mavjud bo‘lsa **Firecrawl** ni chaqirishi mumkin:

- 22. `FIRECRAWL_API_KEY` yoki `tools.web.fetch.firecrawl.apiKey`

23. Agar Firecrawl sozlanmagan bo‘lsa, vosita to‘g‘ridan-to‘g‘ri fetch + readability ga qaytadi (pullik API yo‘q).

24. [Web tools](/tools/web) ga qarang.

### 25. 6. Provayderlardan foydalanish suratlari (holat/sog‘liq)

26. Ba’zi holat buyruqlari kvota oynalari yoki autentifikatsiya sog‘lig‘ini ko‘rsatish uchun **provayderdan foydalanish endpoint** larini chaqiradi.
27. Bular odatda kam hajmli chaqiruvlar, ammo baribir provayder API lariga murojaat qiladi:

- 28. `openclaw status --usage`
- 29. `openclaw models status --json`

30. [Models CLI](/cli/models) ga qarang.

### 31. 7. Siqishdan himoya qiluvchi xulosalash

32. Siqishdan himoya mexanizmi sessiya tarixini **joriy model** yordamida xulosalashi mumkin, bu ishga tushganda provayder API larini chaqiradi.

33. [Session management + compaction](/reference/session-management-compaction) ga qarang.

### 34. 8. Model skaneri / zondlash

35. `openclaw models scan` OpenRouter modellarini zondlashi mumkin va zondlash yoqilganda `OPENROUTER_API_KEY` dan foydalanadi.

36. [Models CLI](/cli/models) ga qarang.

### 37. 9. Talk (nutq)

38. Talk rejimi sozlanganda **ElevenLabs** ni chaqirishi mumkin:

- 39. `ELEVENLABS_API_KEY` yoki `talk.apiKey`

40. [Talk mode](/nodes/talk) ga qarang.

### 41. 10. Ko‘nikmalar (uchinchi tomon API lari)

42. Ko‘nikmalar `apiKey` ni `skills.entries.<name>43. .apiKey` da saqlashi mumkin. 44. Agar ko‘nikma ushbu kalitdan tashqi API lar uchun foydalansa, ko‘nikma provayderiga muvofiq xarajatlarni keltirib chiqarishi mumkin.

45. [Skills](/tools/skills) ga qarang.
