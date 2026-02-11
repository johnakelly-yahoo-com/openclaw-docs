---
summary: "How OpenClaw rotates auth profiles and falls back across models"
read_when:
  - Diagnosing auth profile rotation, cooldowns, or model fallback behavior
  - Updating failover rules for auth profiles or models
title: "Model Failover"
---

# Model failover

OpenClaw handles failures in two stages:

1. **Auth profile rotation** within the current provider.
2. **Model fallback** to the next model in `agents.defaults.model.fallbacks`.

This doc explains the runtime rules and the data that backs them.

## Auth storage (keys + OAuth)

OpenClaw uses **auth profiles** for both API keys and OAuth tokens.

- Secrets live in `~/.openclaw/agents/<agentId>/agent/auth-profiles.json` (legacy: `~/.openclaw/agent/auth-profiles.json`).
- Config `auth.profiles` / `auth.order` are **metadata + routing only** (no secrets).
- Legacy import-only OAuth file: `~/.openclaw/credentials/oauth.json` (imported into `auth-profiles.json` on first use).

More detail: [/concepts/oauth](/concepts/oauth)

Credential types:

- `type: "api_key"` → `{ provider, key }`
- `type: "oauth"` → `{ provider, access, refresh, expires, email? }` (+ `projectId`/`enterpriseUrl` for some providers)

## Profile IDs

OAuth logins create distinct profiles so multiple accounts can coexist.

- Default: `provider:default` when no email is available.
- OAuth with email: `provider:<email>` (for example `google-antigravity:user@gmail.com`).

Profiles live in `~/.openclaw/agents/<agentId>/agent/auth-profiles.json` under `profiles`.

## Rotation order

When a provider has multiple profiles, OpenClaw chooses an order like this:

1. **Explicit config**: `auth.order[provider]` (if set).
2. **Configured profiles**: `auth.profiles` filtered by provider.
3. **Stored profiles**: entries in `auth-profiles.json` for the provider.

If no explicit order is configured, OpenClaw uses a round‑robin order:

- **Primary key:** profile type (**OAuth before API keys**).
- **Secondary key:** `usageStats.lastUsed` (oldest first, within each type).
- **Cooldown/disabled profiles** are moved to the end, ordered by soonest expiry.

### Session stickiness (cache-friendly)

1. OpenClaw **tanlangan auth profilini sessiya davomida mahkamlaydi** — bu provayder keshlarini “issiq” holatda saqlash uchun.
2. U har bir so‘rovda **aylantirilmaydi**. 3. Mahkamlangan profil quyidagilargacha qayta ishlatiladi:

- 4. sessiya qayta o‘rnatilgunga qadar (`/new` / `/reset`)
- 5. kompaksiyalash yakunlangunga qadar (kompaksiyalash hisoblagichi oshadi)
- 6. profil cooldown holatida yoki o‘chirilgan bo‘lsa

7. `/model …@<profileId>` orqali qo‘lda tanlash shu sessiya uchun **foydalanuvchi override** ni o‘rnatadi
   va yangi sessiya boshlanmaguncha avtomatik aylantirilmaydi.

8. Avtomatik mahkamlangan profillar (sessiya routeri tomonidan tanlangan) **afzallik** sifatida qaraladi:
   ular avval sinab ko‘riladi, ammo rate limitlar/timeoutlar bo‘lsa, OpenClaw boshqa profilga o‘tishi mumkin.
9. Foydalanuvchi mahkamlagan profillar o‘sha profilga qulflanib qoladi; agar u ishlamasa va model fallbacklar
   sozlangan bo‘lsa, OpenClaw profilni almashtirish o‘rniga keyingi modelga o‘tadi.

### 10. Nega OAuth “yo‘qolgandek” ko‘rinishi mumkin

11. Agar bir provayder uchun ham OAuth profili, ham API key profili bo‘lsa, round‑robin mahkamlashsiz xabarlar orasida ular o‘rtasida almashishi mumkin. 12. Bitta profilni majburlash uchun:

- 13. `auth.order[provider] = ["provider:profileId"]` bilan mahkamlang, yoki
- 14. UI/chat interfeysingiz qo‘llab-quvvatlaganida `/model …` orqali profil override bilan har sessiya uchun override’dan foydalaning.

## 15. Cooldownlar

16. Profil auth/rate‑limit xatolari (yoki rate limitingga o‘xshash timeout) sababli ishlamay qolsa, OpenClaw uni cooldown holatiga o‘tkazadi va keyingi profilga o‘tadi.
17. Format/yaroqsiz so‘rov xatolari (masalan, Cloud Code Assist tool call ID tekshiruv xatolari) ham failoverga loyiq deb qaraladi va xuddi shu cooldownlardan foydalanadi.

18. Cooldownlar eksponensial backoff’dan foydalanadi:

- 19. 1 daqiqa
- 20. 5 daqiqa
- 21. 25 daqiqa
- 22. 1 soat (maksimal)

23. Holat `auth-profiles.json` faylida `usageStats` ostida saqlanadi:

```json
24. {
  "usageStats": {
    "provider:profile": {
      "lastUsed": 1736160000000,
      "cooldownUntil": 1736160600000,
      "errorCount": 2
    }
  }
}
```

## 25. Billing sababli o‘chirishlar

26. Billing/kredit xatolari (masalan, “insufficient credits” / “credit balance too low”) failoverga loyiq deb qaraladi, ammo ular odatda vaqtinchalik bo‘lmaydi. 27. Qisqa cooldown o‘rniga, OpenClaw profilni **o‘chirilgan** deb belgilaydi (uzoqroq backoff bilan) va keyingi profil/provayderga o‘tadi.

28. Holat `auth-profiles.json` faylida saqlanadi:

```json
29. {
  "usageStats": {
    "provider:profile": {
      "disabledUntil": 1736178000000,
      "disabledReason": "billing"
    }
  }
}
```

30. Sukut bo‘yicha:

- 31. Billing backoff **5 soat**dan boshlanadi, har bir billing xatosida ikki baravar oshadi va **24 soat**da chegaralanadi.
- 32. Agar profil **24 soat** davomida xato bermagan bo‘lsa, backoff hisoblagichlari qayta o‘rnatiladi (sozlanadi).

## 33. Model fallback

34. Agar provayder uchun barcha profillar ishlamasa, OpenClaw `agents.defaults.model.fallbacks` dagi keyingi modelga o‘tadi. 35. Bu auth xatolari, rate limitlar va
    profil aylantirish tugagan timeoutlarga taalluqli (boshqa xatolar fallbackni oldinga siljitmaydi).

36. Ish model override (hooks yoki CLI) bilan boshlanganida ham, fallbacklar sozlangan fallbacklarni sinab ko‘rgach `agents.defaults.model.primary` da yakunlanadi.

## 37. Bog‘liq konfiguratsiya

38. Quyidagilar uchun [Gateway configuration](/gateway/configuration) sahifasiga qarang:

- 39. `auth.profiles` / `auth.order`
- 40. `auth.cooldowns.billingBackoffHours` / `auth.cooldowns.billingBackoffHoursByProvider`
- 41. `auth.cooldowns.billingMaxHours` / `auth.cooldowns.failureWindowHours`
- 42. `agents.defaults.model.primary` / `agents.defaults.model.fallbacks`
- 43. `agents.defaults.imageModel` marshrutlash

44. Model tanlash va fallbacklarning umumiy ko‘rinishi uchun [Models](/concepts/models) sahifasiga qarang.
