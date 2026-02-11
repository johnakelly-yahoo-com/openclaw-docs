---
summary: "OpenClaw CLI uchun skriptlashtirilgan onboarding va agent sozlamalari"
read_when:
  - Siz onboarding’ni skriptlar yoki CI orqali avtomatlashtiryapsiz
  - Muayyan provayderlar uchun interaktiv bo‘lmagan misollar kerak
title: "CLI avtomatlashtirish"
sidebarTitle: "CLI avtomatlashtirish"
---

# CLI avtomatlashtirish

`openclaw onboard` ni avtomatlashtirish uchun `--non-interactive` dan foydalaning.

<Note>
`--json` interaktiv bo‘lmagan rejimni anglatmaydi. Skriptlar uchun `--non-interactive` (va `--workspace`) dan foydalaning.
</Note>

## Asosiy interaktiv bo‘lmagan misol

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice apiKey \
  --anthropic-api-key "$ANTHROPIC_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback \
  --install-daemon \
  --daemon-runtime node \
  --skip-skills
```

Mashina o‘qiy oladigan xulosa uchun `--json` ni qo‘shing.

## Provayderga xos misollar

<AccordionGroup>
  <Accordion title="Gemini example">```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice gemini-api-key \
  --gemini-api-key "$GEMINI_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```</Accordion>
  <Accordion title="Z.AI example">```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice zai-api-key \
  --zai-api-key "$ZAI_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```</Accordion>
  <Accordion title="Vercel AI Gateway example">```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice ai-gateway-api-key \
  --ai-gateway-api-key "$AI_GATEWAY_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```</Accordion>
  <Accordion title="Cloudflare AI Gateway example">```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice cloudflare-ai-gateway-api-key \
  --cloudflare-ai-gateway-account-id "your-account-id" \
  --cloudflare-ai-gateway-gateway-id "your-gateway-id" \
  --cloudflare-ai-gateway-api-key "$CLOUDFLARE_AI_GATEWAY_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```</Accordion>
  <Accordion title="Moonshot example">```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice moonshot-api-key \
  --moonshot-api-key "$MOONSHOT_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```</Accordion>
  <Accordion title="Synthetic example">```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice synthetic-api-key \
  --synthetic-api-key "$SYNTHETIC_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```</Accordion>
  <Accordion title="OpenCode Zen example">```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice opencode-zen \
  --opencode-zen-api-key "$OPENCODE_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```</Accordion>
</AccordionGroup>

## Yana bir agent qo‘shish

Alohida workspace, sessiyalar va autentifikatsiya profillariga ega bo‘lgan alohida agent yaratish uchun `openclaw agents add <name>` dan foydalaning. `--workspace` siz ishga tushirilmasa, ustoz (wizard) ishga tushadi.

```bash
openclaw agents add work \
  --workspace ~/.openclaw/workspace-work \
  --model openai/gpt-5.2 \
  --bind whatsapp:biz \
  --non-interactive \
  --json
```

U nimani sozlaydi:

- `agents.list[].name`
- `agents.list[].workspace`
- `agents.list[].agentDir`

Eslatmalar:

- Standart workspace’lar `~/.openclaw/workspace-<agentId>` formatiga amal qiladi.
- Kirish xabarlarini yo‘naltirish uchun `bindings` qo‘shing (buni wizard ham qila oladi).
- Interaktiv bo‘lmagan flaglar: `--model`, `--agent-dir`, `--bind`, `--non-interactive`.

## Tegishli hujjatlar

- Onboarding markazi: [Onboarding Wizard (CLI)](/start/wizard)
- To‘liq ma’lumotnoma: [CLI Onboarding Reference](/start/wizard-cli-reference)
- Buyruqlar ma’lumotnomasi: [`openclaw onboard`](/cli/onboard)
