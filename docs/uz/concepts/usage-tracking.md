---
summary: "Foydalanishni kuzatish interfeyslari va credential talablari"
read_when:
  - Siz provayder foydalanish/kvota interfeyslarini ulayapsiz
  - Siz foydalanishni kuzatish xatti-harakati yoki autentifikatsiya talablarini tushuntirishingiz kerak
title: "Foydalanishni kuzatish"
---

# Foydalanishni kuzatish

## Bu nima

- Provayder foydalanish/kvotasini ularning foydalanish endpointlaridan to‘g‘ridan-to‘g‘ri oladi.
- Taxminiy xarajatlar yo‘q; faqat provayder xabar bergan oynalar.

## Qayerda ko‘rinadi

- `/status` chatlarda: emoji‑ga boy status kartasi, sessiya tokenlari + taxminiy xarajat (faqat API kaliti bilan). Mavjud bo‘lganda, **joriy model provayderi** uchun provayder foydalanishi ko‘rsatiladi.
- `/usage off|tokens|full` chatlarda: har bir javob uchun foydalanish pastki qismi (OAuth faqat tokenlarni ko‘rsatadi).
- `/usage cost` chatlarda: OpenClaw sessiya loglaridan jamlangan mahalliy xarajatlar xulosasi.
- CLI: `openclaw status --usage` har bir provayder bo‘yicha to‘liq tafsilotni chiqaradi.
- CLI: `openclaw channels list` xuddi shu foydalanish snapshotini provayder konfiguratsiyasi bilan birga chiqaradi (`--no-usage` bilan o‘tkazib yuborish mumkin).
- macOS menyu paneli: Context ostida “Usage” bo‘limi (faqat mavjud bo‘lsa).

## Provayderlar + credentiallar

- **Anthropic (Claude)**: auth profillarida OAuth tokenlari.
- **GitHub Copilot**: auth profillarida OAuth tokenlari.
- **Gemini CLI**: auth profillarida OAuth tokenlari.
- **Antigravity**: auth profillarida OAuth tokenlari.
- **OpenAI Codex**: auth profillarida OAuth tokenlari (mavjud bo‘lsa accountId ishlatiladi).
- **MiniMax**: API kaliti (coding plan kaliti; `MINIMAX_CODE_PLAN_KEY` yoki `MINIMAX_API_KEY`); 5 soatlik coding plan oynasidan foydalanadi.
- **z.ai**: env/config/auth store orqali API kaliti.

Mos OAuth/API credentiallar mavjud bo‘lmasa, foydalanish yashiriladi.
