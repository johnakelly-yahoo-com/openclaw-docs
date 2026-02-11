---
summary: "Models CLI: list, set, aliases, fallbacks, scan, status"
read_when:
  - Adding or modifying models CLI (models list/set/scan/aliases/fallbacks)
  - Changing model fallback behavior or selection UX
  - Updating model scan probes (tools/images)
title: "Models CLI"
---

# Models CLI

See [/concepts/model-failover](/concepts/model-failover) for auth profile
rotation, cooldowns, and how that interacts with fallbacks.
Quick provider overview + examples: [/concepts/model-providers](/concepts/model-providers).

## How model selection works

OpenClaw selects models in this order:

1. **Primary** model (`agents.defaults.model.primary` or `agents.defaults.model`).
2. **Fallbacks** in `agents.defaults.model.fallbacks` (in order).
3. **Provider auth failover** happens inside a provider before moving to the
   next model.

Related:

- `agents.defaults.models` is the allowlist/catalog of models OpenClaw can use (plus aliases).
- `agents.defaults.imageModel` is used **only when** the primary model can’t accept images.
- Per-agent defaults can override `agents.defaults.model` via `agents.list[].model` plus bindings (see [/concepts/multi-agent](/concepts/multi-agent)).

## Quick model picks (anecdotal)

- **GLM**: a bit better for coding/tool calling.
- **MiniMax**: better for writing and vibes.

## Setup wizard (recommended)

If you don’t want to hand-edit config, run the onboarding wizard:

```bash
openclaw onboard
```

It can set up model + auth for common providers, including **OpenAI Code (Codex)
subscription** (OAuth) and **Anthropic** (API key recommended; `claude
setup-token` also supported).

## Config keys (overview)

- `agents.defaults.model.primary` and `agents.defaults.model.fallbacks`
- `agents.defaults.imageModel.primary` and `agents.defaults.imageModel.fallbacks`
- `agents.defaults.models` (allowlist + aliases + provider params)
- `models.providers` (custom providers written into `models.json`)

Model refs are normalized to lowercase. Provider aliases like `z.ai/*` normalize
to `zai/*`.

Provider configuration examples (including OpenCode Zen) live in
[/gateway/configuration](/gateway/configuration#opencode-zen-multi-model-proxy).

## “Model is not allowed” (and why replies stop)

If `agents.defaults.models` is set, it becomes the **allowlist** for `/model` and for
session overrides. When a user selects a model that isn’t in that allowlist,
OpenClaw returns:

```
Model "provider/model" is not allowed. Use /model to list available models.
```

This happens **before** a normal reply is generated, so the message can feel
like it “didn’t respond.” The fix is to either:

- Add the model to `agents.defaults.models`, or
- Clear the allowlist (remove `agents.defaults.models`), or
- Pick a model from `/model list`.

Example allowlist config:

```json5
{
  agent: {
    model: { primary: "anthropic/claude-sonnet-4-5" },
    models: {
      "anthropic/claude-sonnet-4-5": { alias: "Sonnet" },
      "anthropic/claude-opus-4-6": { alias: "Opus" },
    },
  },
}
```

## Switching models in chat (`/model`)

You can switch models for the current session without restarting:

```
/model
/model list
/model 3
/model openai/gpt-5.2
/model status
```

Notes:

- `/model` (and `/model list`) is a compact, numbered picker (model family + available providers).
- `/model <#>` selects from that picker.
- `/model status` is the detailed view (auth candidates and, when configured, provider endpoint `baseUrl` + `api` mode).
- Model refs are parsed by splitting on the **first** `/`. Use `provider/model` when typing `/model <ref>`.
- If the model ID itself contains `/` (OpenRouter-style), you must include the provider prefix (example: `/model openrouter/moonshotai/kimi-k2`).
- If you omit the provider, OpenClaw treats the input as an alias or a model for the **default provider** (only works when there is no `/` in the model ID).

Full command behavior/config: [Slash commands](/tools/slash-commands).

## CLI commands

```bash
openclaw models list
openclaw models status
openclaw models set <provider/model>
openclaw models set-image <provider/model>

openclaw models aliases list
openclaw models aliases add <alias> <provider/model>
openclaw models aliases remove <alias>

openclaw models fallbacks list
openclaw models fallbacks add <provider/model>
openclaw models fallbacks remove <provider/model>
openclaw models fallbacks clear

openclaw models image-fallbacks list
openclaw models image-fallbacks add <provider/model>
openclaw models image-fallbacks remove <provider/model>
openclaw models image-fallbacks clear
```

`openclaw models` (no subcommand) is a shortcut for `models status`.

### `models list`

Shows configured models by default. Useful flags:

- `--all`: full catalog
- `--local`: local providers only
- `--provider <name>`: filter by provider
- `--plain`: one model per line
- `--json`: mashina tomonidan o‘qiladigan chiqish

### `models status`

Sozlangan provayderlar uchun aniqlangan asosiy model, zaxira modellar, rasm modeli va autentifikatsiya sharhini ko‘rsatadi. Shuningdek, autentifikatsiya omborida topilgan profillar uchun OAuth amal qilish muddati holatini ko‘rsatadi
(standart bo‘yicha 24 soat ichida ogohlantiradi). `--plain` faqat aniqlangan
asosiy modelni chiqaradi.
OAuth holati har doim ko‘rsatiladi (va `--json` chiqishiga kiritiladi). Agar sozlangan
provayderda hisob ma’lumotlari bo‘lmasa, `models status` **Missing auth** bo‘limini chiqaradi.
JSON tarkibiga `auth.oauth` (ogohlantirish oynasi + profillar) va `auth.providers`
(har bir provayder bo‘yicha samarali autentifikatsiya) kiradi.
Avtomatlashtirish uchun `--check` dan foydalaning (yo‘qolgan/muddati o‘tgan bo‘lsa `1`, muddati yaqinlashayotgan bo‘lsa `2` bilan chiqadi).

Anthropic uchun afzal ko‘rilgan autentifikatsiya — Claude Code CLI setup-token (istalgan joyda ishga tushiring; kerak bo‘lsa, gateway xostga joylashtiring):

```bash
claude setup-token
openclaw models status
```

## Skanerlash (OpenRouter bepul modellari)

`openclaw models scan` OpenRouter’ning **bepul model katalogi**ni tekshiradi va
ixtiyoriy ravishda modellarni asboblar va rasm qo‘llab-quvvatlashi bo‘yicha sinab ko‘rishi mumkin.

Asosiy flaglar:

- `--no-probe`: jonli tekshiruvlarni o‘tkazib yuborish (faqat metadata)
- `--min-params <b>`: minimal parametr hajmi (milliardlarda)
- `--max-age-days <days>`: eski modellarni o‘tkazib yuborish
- `--provider <name>`: provayder prefiksi bo‘yicha filtr
- `--max-candidates <n>`: zaxira ro‘yxati hajmi
- `--set-default`: `agents.defaults.model.primary` ni birinchi tanlovga o‘rnatish
- `--set-image`: `agents.defaults.imageModel.primary` ni birinchi rasm tanloviga o‘rnatish

Tekshiruv uchun OpenRouter API kaliti talab qilinadi (auth profillaridan yoki
`OPENROUTER_API_KEY`). Kalitsiz, faqat nomzodlarni ro‘yxatlash uchun `--no-probe` dan foydalaning.

Skan natijalari quyidagilar bo‘yicha reytinglanadi:

1. Rasm qo‘llab-quvvatlashi
2. Asboblar kechikishi
3. Kontekst hajmi
4. Parametrlar soni

Kirish

- OpenRouter `/models` ro‘yxati (filter `:free`)
- Auth profillaridan yoki `OPENROUTER_API_KEY` dan OpenRouter API kaliti talab qilinadi (qarang [/environment](/help/environment))
- Ixtiyoriy filtrlar: `--max-age-days`, `--min-params`, `--provider`, `--max-candidates`
- Tekshiruv boshqaruvlari: `--timeout`, `--concurrency`

TTY da ishga tushirilganda, zaxiralarni interaktiv tarzda tanlashingiz mumkin. Interaktiv bo‘lmagan
rejimda, standartlarni qabul qilish uchun `--yes` ni bering.

## Modellar reyestri (`models.json`)

`models.providers` dagi maxsus provayderlar agent katalogi ostidagi `models.json` ga yoziladi
(standart `~/.openclaw/agents/<agentId>/models.json`). Bu fayl
`models.mode` `replace` ga o‘rnatilmaguncha standart bo‘yicha birlashtiriladi.
