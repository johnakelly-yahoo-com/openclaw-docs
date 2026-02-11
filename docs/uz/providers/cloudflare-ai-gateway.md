---
title: "Cloudflare AI Gateway sozlamalari (auth + model tanlash)"
summary: "Cloudflare AI Gateway setup (auth + model selection)"
read_when:
  - Sizga account ID, gateway ID yoki API kalit env o‘zgaruvchisi kerak
  - Cloudflare AI Gateway
---

# Cloudflare AI Gateway provider API’lari oldida joylashadi va analytics, caching hamda nazoratlarni qo‘shish imkonini beradi.

Anthropic uchun OpenClaw Gateway endpoint’ingiz orqali Anthropic Messages API’dan foydalanadi. Provider: `cloudflare-ai-gateway`

- Base URL: `https://gateway.ai.cloudflare.com/v1/<account_id>/<gateway_id>/anthropic`
- Standart model: `cloudflare-ai-gateway/claude-sonnet-4-5`
- API kalit: `CLOUDFLARE_AI_GATEWAY_API_KEY` (Gateway orqali yuboriladigan so‘rovlar uchun provider API kalitingiz)
- Anthropic modellari uchun Anthropic API kalitingizdan foydalaning.

Tezkor boshlash

## Provider API kaliti va Gateway tafsilotlarini sozlang:

1. openclaw onboard --auth-choice cloudflare-ai-gateway-api-key

```bash
Standart modelni sozlang:
```

2. {
   agents: {
   defaults: {
   model: { primary: "cloudflare-ai-gateway/claude-sonnet-4-5" },
   },
   },
   }

```json5
Interaktiv bo‘lmagan misol
```

openclaw onboard --non-interactive \
\--mode local \
\--auth-choice cloudflare-ai-gateway-api-key \
\--cloudflare-ai-gateway-account-id "your-account-id" \
\--cloudflare-ai-gateway-gateway-id "your-gateway-id" \
\--cloudflare-ai-gateway-api-key "$CLOUDFLARE_AI_GATEWAY_API_KEY"
-----------------------------------------------------------------------------------------------------------------------------------------------------

```bash
Autentifikatsiyalangan gateway’lar
```

## Agar Cloudflare’da Gateway autentifikatsiyasini yoqqan bo‘lsangiz, `cf-aig-authorization` header’ini qo‘shing (bu provider API kalitingizdan tashqari).

Agar Cloudflare’da Gateway autentifikatsiyasini yoqqan bo‘lsangiz, `cf-aig-authorization` sarlavhasini qo‘shing (bu provayder API kalitingizga qo‘shimcha ravishda kerak).

```json5
Muhit bo‘yicha eslatma
```

## Agar Gateway daemon sifatida (launchd/systemd) ishlayotgan bo‘lsa, `CLOUDFLARE_AI_GATEWAY_API_KEY` ushbu jarayon uchun mavjud ekanligiga ishonch hosil qiling (masalan, `~/.openclaw/.env` da yoki `env.shellEnv` orqali).

Kiruvchi ovozli eslatmalar uchun Deepgram transkripsiyasi
