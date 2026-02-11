---
title: "Pi ishlab chiqish jarayoni"
---

# Pi ishlab chiqish jarayoni

Ushbu qo‘llanma OpenClaw’dagi pi integratsiyasi ustida ishlash uchun oqilona ish jarayonini umumlashtiradi.

## Tur tekshiruvi va linting

- Type check and build: `pnpm build`
- Lint: `pnpm lint`
- 3. Formatni tekshirish: `pnpm format`
- 4. Push qilishdan oldingi to‘liq tekshiruv: `pnpm lint && pnpm build && pnpm test`

## 5. Pi testlarini ishga tushirish

6. Pi integratsiya testlari to‘plami uchun maxsus skriptdan foydalaning:

```bash
scripts/pi/run-tests.sh
```

8. Haqiqiy provayder xatti-harakatini sinovdan o‘tkazadigan live testni qo‘shish uchun:

```bash
scripts/pi/run-tests.sh --live
```

10. Skript quyidagi globlar orqali barcha pi bilan bog‘liq unit testlarni ishga tushiradi:

- `src/agents/pi-*.test.ts`
- `src/agents/pi-embedded-*.test.ts`
- 13. `src/agents/pi-tools*.test.ts`
- `src/agents/pi-settings.test.ts`
- 15. `src/agents/pi-tool-definition-adapter.test.ts`
- 16. `src/agents/pi-extensions/*.test.ts`

## Manual Testing

18. Tavsiya etilgan jarayon:

- Run the gateway in dev mode:
  - `pnpm gateway:dev`
- 21. Agentni bevosita ishga tushiring:
  - 22. `pnpm openclaw agent --message "Hello" --thinking low`
- 23. Interaktiv debug qilish uchun TUI’dan foydalaning:
  - 24. `pnpm tui`

25. Tool chaqiruv xatti-harakatlari uchun `read` yoki `exec` amalini so‘rang, shunda tool streaming va payloadni qayta ishlashni ko‘rishingiz mumkin.

## 26. Toza holatga qaytarish

27. Holat OpenClaw state katalogida saqlanadi. 28. Standart qiymat `~/.openclaw`. 29. Agar `OPENCLAW_STATE_DIR` o‘rnatilgan bo‘lsa, uning o‘rniga shu katalogdan foydalaniladi.

30. Hammasini reset qilish uchun:

- 31. `openclaw.json` — konfiguratsiya uchun
- 32. `credentials/` — autentifikatsiya profillari va tokenlar uchun
- 33. `agents/<agentId>/sessions/` — agent sessiya tarixi uchun
- 34. `agents/<agentId>/sessions.json` — sessiyalar indeksi uchun
- 35. Agar eski yo‘llar mavjud bo‘lsa, `sessions/`
- 36. Agar bo‘sh ishchi muhit xohlasangiz, `workspace/`

37. Agar faqat sessiyalarni reset qilmoqchi bo‘lsangiz, shu agent uchun `agents/<agentId>/sessions/` va `agents/<agentId>/sessions.json` ni o‘chiring. 38. Qayta autentifikatsiya qilishni istamasangiz, `credentials/` ni saqlab qoling.

## 39. Manbalar

- 40. [https://docs.openclaw.ai/testing](https://docs.openclaw.ai/testing)
- 41. [https://docs.openclaw.ai/start/getting-started](https://docs.openclaw.ai/start/getting-started)
