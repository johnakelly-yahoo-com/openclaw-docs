---
summary: "Testing kit: unit/e2e/live suites, Docker runners, and what each test covers"
read_when:
  - Running tests locally or in CI
  - Adding regressions for model/provider bugs
  - Debugging gateway + agent behavior
title: "Testing"
---

# Testing

OpenClaw has three Vitest suites (unit/integration, e2e, live) and a small set of Docker runners.

This doc is a “how we test” guide:

- What each suite covers (and what it deliberately does _not_ cover)
- Which commands to run for common workflows (local, pre-push, debugging)
- How live tests discover credentials and select models/providers
- How to add regressions for real-world model/provider issues

## Quick start

Most days:

- Full gate (expected before push): `pnpm build && pnpm check && pnpm test`

When you touch tests or want extra confidence:

- Coverage gate: `pnpm test:coverage`
- E2E suite: `pnpm test:e2e`

When debugging real providers/models (requires real creds):

- Live suite (models + gateway tool/image probes): `pnpm test:live`

Maslahat: faqat bitta muvaffaqiyatsiz holat kerak bo‘lsa, quyida tasvirlangan allowlist muhit o‘zgaruvchilari orqali live testlarni toraytirishni afzal ko‘ring.

## Test suites (what runs where)

Think of the suites as “increasing realism” (and increasing flakiness/cost):

### Unit / integration (default)

- Buyruq: `pnpm test`
- Config: `vitest.config.ts`
- Files: `src/**/*.test.ts`
- Scope:
  - Pure unit tests
  - In-process integration tests (gateway auth, routing, tooling, parsing, config)
  - Deterministic regressions for known bugs
- Expectations:
  - Runs in CI
  - Haqiqiy kalitlar talab qilinmaydi
  - Should be fast and stable

### E2E (gateway smoke)

- Command: `pnpm test:e2e`
- Config: `vitest.e2e.config.ts`
- Files: `src/**/*.e2e.test.ts`
- Scope:
  - Multi-instance gateway end-to-end behavior
  - WebSocket/HTTP surfaces, node pairing, and heavier networking
- Expectations:
  - Runs in CI (when enabled in the pipeline)
  - Haqiqiy kalitlar talab qilinmaydi
  - More moving parts than unit tests (can be slower)

### Live (real providers + real models)

- Command: `pnpm test:live`
- Config: `vitest.live.config.ts`
- Files: `src/**/*.live.test.ts`
- Default: **enabled** by `pnpm test:live` (sets `OPENCLAW_LIVE_TEST=1`)
- Scope:
  - “Does this provider/model actually work _today_ with real creds?”
  - Catch provider format changes, tool-calling quirks, auth issues, and rate limit behavior
- Kutilmalar:
  - Not CI-stable by design (real networks, real provider policies, quotas, outages)
  - Costs money / uses rate limits
  - Prefer running narrowed subsets instead of “everything”
  - Live runs will source `~/.profile` to pick up missing API keys
  - Anthropic key rotation: set `OPENCLAW_LIVE_ANTHROPIC_KEYS="sk-...,sk-..."` (or `OPENCLAW_LIVE_ANTHROPIC_KEY=sk-...`) or multiple `ANTHROPIC_API_KEY*` vars; tests will retry on rate limits

## Which suite should I run?

Use this decision table:

- Editing logic/tests: run `pnpm test` (and `pnpm test:coverage` if you changed a lot)
- Touching gateway networking / WS protocol / pairing: add `pnpm test:e2e`
- Debugging “my bot is down” / provider-specific failures / tool calling: run a narrowed `pnpm test:live`

## Live: model smoke (profile keys)

Live tests are split into two layers so we can isolate failures:

- “Direct model” bizga provayder/model berilgan kalit bilan umuman javob bera olishini bildiradi.
- “Gateway smoke” tells us the full gateway+agent pipeline works for that model (sessions, history, tools, sandbox policy, etc.).

### Layer 1: Direct model completion (no gateway)

- Test: `src/agents/models.profiles.live.test.ts`
- Goal:
  - Enumerate discovered models
  - Use `getApiKeyForModel` to select models you have creds for
  - Har bir model uchun kichik yakunlashni ishga tushiring (zarur bo‘lsa, maqsadli regressiyalar bilan)
- Qanday yoqish:
  - `pnpm test:live` (yoki Vitest’ni to‘g‘ridan-to‘g‘ri chaqirayotgan bo‘lsangiz `OPENCLAW_LIVE_TEST=1`)
- Bu to‘plamni haqiqatan ham ishga tushirish uchun `OPENCLAW_LIVE_MODELS=modern` (yoki `all`, modern uchun alias) ni o‘rnating; aks holda u o‘tkazib yuboriladi va `pnpm test:live` gateway smoke testlariga yo‘naltirilgan bo‘lib qoladi
- Modellarni qanday tanlash:
  - Zamonaviy ruxsat etilgan ro‘yxatni ishga tushirish uchun `OPENCLAW_LIVE_MODELS=modern` (Opus/Sonnet/Haiku 4.5, GPT-5.x + Codex, Gemini 3, GLM 4.7, MiniMax M2.1, Grok 4)
  - `OPENCLAW_LIVE_MODELS=all` — zamonaviy ruxsat etilgan ro‘yxat uchun alias
  - yoki `OPENCLAW_LIVE_MODELS="openai/gpt-5.2,anthropic/claude-opus-4-6,..."` (vergul bilan ajratilgan allowlist)
- Provayderlarni qanday tanlash:
  - `OPENCLAW_LIVE_PROVIDERS="google,google-antigravity,google-gemini-cli"` (vergul bilan ajratilgan allowlist)
- Kalitlar qayerdan olinadi:
  - Sukut bo‘yicha: profil ombori va muhit (env) fallback’lari
  - Faqat **profil ombori**ni majburiy qilish uchun `OPENCLAW_LIVE_REQUIRE_PROFILE_KEYS=1` ni o‘rnating
- Nega bu mavjud:
  - “Provayder API buzilgan / kalit yaroqsiz” holatini “gateway agent pipeline buzilgan” holatidan ajratadi
  - Kichik, izolyatsiyalangan regressiyalarni o‘z ichiga oladi (masalan: OpenAI Responses/Codex Responses mantiqiy qayta ijro + tool-call oqimlari)

### 2-qavat: Gateway + dev agent smoke ("@openclaw" aslida nima qiladi)

- Test: `src/gateway/gateway-models.profiles.live.test.ts`
- Maqsad:
  - Jarayon ichidagi gateway’ni ishga tushiring
  - `agent:dev:*` sessiyasini yaratish/patch qilish (har ishga tushirishda modelni override qilish)
  - Kalitlari bor modellar bo‘ylab aylanish va quyidagilarni tekshirish:
    - “mazmunli” javob (toolsiz)
    - haqiqiy tool chaqiruvi ishlashi (read probe)
    - ixtiyoriy qo‘shimcha tool probelari (exec+read probe)
    - OpenAI regressiya yo‘llari (faqat tool-call → follow-up) ishlashda davom etadi
- Probe tafsilotlari (nosozliklarni tez tushuntira olish uchun):
  - `read` probe: test ish maydonida nonce fayl yozadi va agentdan uni `read` qilib nonce’ni qayta aks ettirishni so‘raydi.
  - `exec+read` probe: test agentdan nonce’ni vaqtinchalik faylga `exec` orqali yozishni, so‘ng uni `read` qilib qaytarishni so‘raydi.
  - image probe: test yaratilgan PNG’ni (mushuk + tasodifiy kod) biriktiradi va modeldan `cat <CODE>` qaytarishini kutadi.
  - Implementatsiya uchun havola: `src/gateway/gateway-models.profiles.live.test.ts` va `src/gateway/live-image-probe.ts`.
- Qanday yoqish:
  - `pnpm test:live` (yoki Vitest’ni to‘g‘ridan-to‘g‘ri chaqirayotgan bo‘lsangiz `OPENCLAW_LIVE_TEST=1`)
- Modellarni qanday tanlash:
  - Odatiy: zamonaviy ruxsat etilgan ro‘yxat (Opus/Sonnet/Haiku 4.5, GPT-5.x + Codex, Gemini 3, GLM 4.7, MiniMax M2.1, Grok 4)
  - `OPENCLAW_LIVE_GATEWAY_MODELS=all` — zamonaviy ruxsat etilgan ro‘yxat uchun alias
  - Yoki toraytirish uchun `OPENCLAW_LIVE_GATEWAY_MODELS="provider/model"` (yoki vergul bilan ajratilgan ro‘yxat) ni o‘rnating
- Provayderlarni qanday tanlash (“OpenRouter everything”dan qochish):
  - `OPENCLAW_LIVE_GATEWAY_PROVIDERS="google,google-antigravity,google-gemini-cli,openai,anthropic,zai,minimax"` (vergul bilan ajratilgan allowlist)
- Tool + image probelari bu live testda har doim yoqilgan:
  - `read` probe + `exec+read` probe (tool stress)
  - Model image input qo‘llab-quvvatlashini e’lon qilganda image probe ishga tushadi
  - Oqim (yuqori darajada):
    - Test “CAT” + tasodifiy kod bilan kichik PNG yaratadi (`src/gateway/live-image-probe.ts`)
    - Uni `agent` orqali `attachments: [{ mimeType: "image/png", content: "<base64>" }]` bilan yuboradi
    - Gateway biriktirmalarni `images[]` ga ajratadi (`src/gateway/server-methods/agent.ts` + `src/gateway/chat-attachments.ts`)
    - Ichki agent multimodal foydalanuvchi xabarini modelga uzatadi
    - Tekshiruv: javob `cat` + kodni o‘z ichiga oladi (OCR tolerantligi: kichik xatolarga ruxsat beriladi)

Maslahat: mashinangizda nimani test qilishingiz mumkinligini (va aniq `provider/model` ID’larini) ko‘rish uchun quyidagini ishga tushiring:

```bash
openclaw models list
```

## Live: Anthropic setup-token smoke

- Test: `src/agents/anthropic.setup-token.live.test.ts`
- Goal: verify Claude Code CLI setup-token (or a pasted setup-token profile) can complete an Anthropic prompt.
- Enable:
  - `pnpm test:live` (or `OPENCLAW_LIVE_TEST=1` if invoking Vitest directly)
  - `OPENCLAW_LIVE_SETUP_TOKEN=1`
- Token sources (pick one):
  - Profile: `OPENCLAW_LIVE_SETUP_TOKEN_PROFILE=anthropic:setup-token-test`
  - Raw token: `OPENCLAW_LIVE_SETUP_TOKEN_VALUE=sk-ant-oat01-...`
- Model override (optional):
  - `OPENCLAW_LIVE_SETUP_TOKEN_MODEL=anthropic/claude-opus-4-6`

Setup example:

```bash
openclaw models auth paste-token --provider anthropic --profile-id anthropic:setup-token-test
OPENCLAW_LIVE_SETUP_TOKEN=1 OPENCLAW_LIVE_SETUP_TOKEN_PROFILE=anthropic:setup-token-test pnpm test:live src/agents/anthropic.setup-token.live.test.ts
```

## Live: CLI backend smoke (Claude Code CLI or other local CLIs)

- Test: `src/gateway/gateway-cli-backend.live.test.ts`
- Goal: validate the Gateway + agent pipeline using a local CLI backend, without touching your default config.
- Yoqish:
  - `pnpm test:live` (or `OPENCLAW_LIVE_TEST=1` if invoking Vitest directly)
  - `OPENCLAW_LIVE_CLI_BACKEND=1`
- Defaults:
  - Model: `claude-cli/claude-sonnet-4-5`
  - Buyruq: `claude`
  - Args: `["-p","--output-format","json","--dangerously-skip-permissions"]`
- Overrides (optional):
  - `OPENCLAW_LIVE_CLI_BACKEND_MODEL="claude-cli/claude-opus-4-6"`
  - `OPENCLAW_LIVE_CLI_BACKEND_MODEL="codex-cli/gpt-5.3-codex"`
  - `OPENCLAW_LIVE_CLI_BACKEND_COMMAND="/full/path/to/claude"`
  - `OPENCLAW_LIVE_CLI_BACKEND_ARGS='["-p","--output-format","json","--permission-mode","bypassPermissions"]'`
  - `OPENCLAW_LIVE_CLI_BACKEND_CLEAR_ENV='["ANTHROPIC_API_KEY","ANTHROPIC_API_KEY_OLD"]'`
  - `OPENCLAW_LIVE_CLI_BACKEND_IMAGE_PROBE=1` to send a real image attachment (paths are injected into the prompt).
  - `OPENCLAW_LIVE_CLI_BACKEND_IMAGE_ARG="--image"` to pass image file paths as CLI args instead of prompt injection.
  - `IMAGE_ARG` o‘rnatilganda rasm argumentlari qanday uzatilishini boshqarish uchun `OPENCLAW_LIVE_CLI_BACKEND_IMAGE_MODE="repeat"` (yoki `"list"`).
  - `OPENCLAW_LIVE_CLI_BACKEND_RESUME_PROBE=1` to send a second turn and validate resume flow.
- `OPENCLAW_LIVE_CLI_BACKEND_DISABLE_MCP_CONFIG=0` to keep Claude Code CLI MCP config enabled (default disables MCP config with a temporary empty file).

Example:

```bash
OPENCLAW_LIVE_CLI_BACKEND=1 \
  OPENCLAW_LIVE_CLI_BACKEND_MODEL="claude-cli/claude-sonnet-4-5" \
  pnpm test:live src/gateway/gateway-cli-backend.live.test.ts
```

### Recommended live recipes

Narrow, explicit allowlists are fastest and least flaky:

- Single model, direct (no gateway):
  - `OPENCLAW_LIVE_MODELS="openai/gpt-5.2" pnpm test:live src/agents/models.profiles.live.test.ts`

- Single model, gateway smoke:
  - `OPENCLAW_LIVE_GATEWAY_MODELS="openai/gpt-5.2" pnpm test:live src/gateway/gateway-models.profiles.live.test.ts`

- Tool calling across several providers:
  - `OPENCLAW_LIVE_GATEWAY_MODELS="openai/gpt-5.2,anthropic/claude-opus-4-6,google/gemini-3-flash-preview,zai/glm-4.7,minimax/minimax-m2.1" pnpm test:live src/gateway/gateway-models.profiles.live.test.ts`

- Google focus (Gemini API key + Antigravity):
  - Gemini (API key): `OPENCLAW_LIVE_GATEWAY_MODELS="google/gemini-3-flash-preview" pnpm test:live src/gateway/gateway-models.profiles.live.test.ts`
  - Antigravity (OAuth): `OPENCLAW_LIVE_GATEWAY_MODELS="google-antigravity/claude-opus-4-6-thinking,google-antigravity/gemini-3-pro-high" pnpm test:live src/gateway/gateway-models.profiles.live.test.ts`

Notes:

- `google/...` uses the Gemini API (API key).
- `google-antigravity/...` uses the Antigravity OAuth bridge (Cloud Code Assist-style agent endpoint).
- `google-gemini-cli/...` mashinangizdagi lokal Gemini CLI’dan foydalanadi (alohida autentifikatsiya + asboblar o‘ziga xosliklari).
- Gemini API va Gemini CLI taqqoslanishi:
  - API: OpenClaw Google’ning joylashtirilgan Gemini API’sini HTTP orqali chaqiradi (API kaliti / profil autentifikatsiyasi); ko‘pchilik foydalanuvchilar “Gemini” deganda shuni nazarda tutadi.
  - CLI: OpenClaw lokal `gemini` binarini ishga tushiradi; uning o‘z autentifikatsiyasi bor va u boshqacha ishlashi mumkin (striming/asboblar qo‘llab-quvvatlashi/versiya nomuvofiqligi).

## Live: model matritsasi (biz qamrab oladiganlari)

Doimiy “CI model ro‘yxati” yo‘q (live — ixtiyoriy), ammo bular kalitlari mavjud bo‘lgan dev mashinada muntazam qamrab olish uchun **tavsiya etilgan** modellardir.

### Zamonaviy smoke to‘plam (asbob chaqirish + rasm)

Bu biz ishlashini saqlab qolishni kutadigan “umumiy modellar” yugurishi:

- OpenAI (Codex emas): `openai/gpt-5.2` (ixtiyoriy: `openai/gpt-5.1`)
- OpenAI Codex: `openai-codex/gpt-5.3-codex` (ixtiyoriy: `openai-codex/gpt-5.3-codex-codex`)
- Anthropic: `anthropic/claude-opus-4-6` (yoki `anthropic/claude-sonnet-4-5`)
- Google (Gemini API): `google/gemini-3-pro-preview` va `google/gemini-3-flash-preview` (eski Gemini 2.x modellaridan qoching)
- Google (Antigravity): `google-antigravity/claude-opus-4-6-thinking` va `google-antigravity/gemini-3-flash`
- Z.AI (GLM): `zai/glm-4.7`
- MiniMax: `minimax/minimax-m2.1`

Gateway smoke’ni asboblar + rasm bilan ishga tushiring:
`OPENCLAW_LIVE_GATEWAY_MODELS="openai/gpt-5.2,openai-codex/gpt-5.3-codex,anthropic/claude-opus-4-6,google/gemini-3-pro-preview,google/gemini-3-flash-preview,google-antigravity/claude-opus-4-6-thinking,google-antigravity/gemini-3-flash,zai/glm-4.7,minimax/minimax-m2.1" pnpm test:live src/gateway/gateway-models.profiles.live.test.ts`

### Asosiy: asbob chaqirish (Read + ixtiyoriy Exec)

Har bir provayder oilasidan kamida bittasini tanlang:

- OpenAI: `openai/gpt-5.2` (yoki `openai/gpt-5-mini`)
- Anthropic: `anthropic/claude-opus-4-6` (yoki `anthropic/claude-sonnet-4-5`)
- Google: `google/gemini-3-flash-preview` (yoki `google/gemini-3-pro-preview`)
- Z.AI (GLM): `zai/glm-4.7`
- MiniMax: `minimax/minimax-m2.1`

Ixtiyoriy qo‘shimcha qamrov (bo‘lsa yaxshi):

- xAI: `xai/grok-4` (yoki mavjud eng so‘nggi)
- Mistral: `mistral/`… (sizda yoqilgan “tools” imkoniyatiga ega bitta modelni tanlang)
- Cerebras: `cerebras/`… (agar ruxsatingiz bo‘lsa)
- LM Studio: `lmstudio/`… (lokal; asbob chaqirish API rejimiga bog‘liq)

### Vision: rasm yuborish (ilova → multimodal xabar)

`OPENCLAW_LIVE_GATEWAY_MODELS` ichiga kamida bitta rasmni qo‘llab-quvvatlaydigan modelni kiriting (Claude/Gemini/OpenAI’ning vision imkoniyatli variantlari va h.k.) rasm tekshiruvini ishga tushirish uchun.

### Aggregatorlar / muqobil gateway’lar

Agar kalitlaringiz yoqilgan bo‘lsa, biz quyidagilar orqali ham testlashni qo‘llab-quvvatlaymiz:

- OpenRouter: `openrouter/...` (yuzlab modellar; asbob+rasm imkoniyatiga ega nomzodlarni topish uchun `openclaw models scan` dan foydalaning)
- OpenCode Zen: `opencode/...` (`OPENCODE_API_KEY` / `OPENCODE_ZEN_API_KEY` orqali autentifikatsiya)

Live matritsaga kiritishingiz mumkin bo‘lgan yana provayderlar (agar credential/config bo‘lsa):

- O‘rnatilgan: `openai`, `openai-codex`, `anthropic`, `google`, `google-vertex`, `google-antigravity`, `google-gemini-cli`, `zai`, `openrouter`, `opencode`, `xai`, `groq`, `cerebras`, `mistral`, `github-copilot`
- `models.providers` orqali (maxsus endpoint’lar): `minimax` (cloud/API), shuningdek OpenAI/Anthropic’ga mos keladigan istalgan proksi (LM Studio, vLLM, LiteLLM va h.k.)

Maslahat: hujjatlarda “barcha modellar”ni qattiq kodlashga urinmang. Rasmiy ro‘yxat — bu sizning mashinangizda `discoverModels(...)` nimani qaytarsa + mavjud kalitlar.

## Credential’lar (hech qachon commit qilmang)

Live testlar credential’larni CLI qanday topса, xuddi shunday topadi. Amaliy oqibatlar:

- Agar CLI ishlasa, live testlar ham xuddi shu kalitlarni topishi kerak.

- Agar live test “no creds” desa, `openclaw models list` / model tanlashni qanday debug qilsangiz, xuddi shunday debug qiling.

- Profil ombori: `~/.openclaw/credentials/` (afzal; testlarda “profile keys” degani shu)

- Konfiguratsiya: `~/.openclaw/openclaw.json` (yoki `OPENCLAW_CONFIG_PATH`)

If you want to rely on env keys (e.g. exported in your `~/.profile`), run local tests after `source ~/.profile`, or use the Docker runners below (they can mount `~/.profile` into the container).

## Deepgram live (audio transcription)

- Test: `src/media-understanding/providers/deepgram/audio.live.test.ts`
- Enable: `DEEPGRAM_API_KEY=... DEEPGRAM_LIVE_TEST=1 pnpm test:live src/media-understanding/providers/deepgram/audio.live.test.ts`

## Docker runners (optional “works in Linux” checks)

These run `pnpm test:live` inside the repo Docker image, mounting your local config dir and workspace (and sourcing `~/.profile` if mounted):

- Direct models: `pnpm test:docker:live-models` (script: `scripts/test-live-models-docker.sh`)
- Gateway + dev agent: `pnpm test:docker:live-gateway` (script: `scripts/test-live-gateway-models-docker.sh`)
- Onboarding wizard (TTY, full scaffolding): `pnpm test:docker:onboard` (script: `scripts/e2e/onboard-docker.sh`)
- Gateway networking (two containers, WS auth + health): `pnpm test:docker:gateway-network` (script: `scripts/e2e/gateway-network-docker.sh`)
- Plugins (custom extension load + registry smoke): `pnpm test:docker:plugins` (script: `scripts/e2e/plugins-docker.sh`)

Useful env vars:

- `OPENCLAW_CONFIG_DIR=...` (default: `~/.openclaw`) mounted to `/home/node/.openclaw`
- `OPENCLAW_WORKSPACE_DIR=...` (default: `~/.openclaw/workspace`) mounted to `/home/node/.openclaw/workspace`
- `OPENCLAW_PROFILE_FILE=...` (default: `~/.profile`) mounted to `/home/node/.profile` and sourced before running tests
- `OPENCLAW_LIVE_GATEWAY_MODELS=...` / `OPENCLAW_LIVE_MODELS=...` to narrow the run
- `OPENCLAW_LIVE_REQUIRE_PROFILE_KEYS=1` to ensure creds come from the profile store (not env)

## Docs sanity

Run docs checks after doc edits: `pnpm docs:list`.

## Offline regression (CI-safe)

These are “real pipeline” regressions without real providers:

- Gateway tool calling (mock OpenAI, real gateway + agent loop): `src/gateway/gateway.tool-calling.mock-openai.test.ts`
- Gateway wizard (WS `wizard.start`/`wizard.next`, writes config + auth enforced): `src/gateway/gateway.wizard.e2e.test.ts`

## Agent reliability evals (skills)

We already have a few CI-safe tests that behave like “agent reliability evals”:

- Mock tool-calling through the real gateway + agent loop (`src/gateway/gateway.tool-calling.mock-openai.test.ts`).
- End-to-end wizard flows that validate session wiring and config effects (`src/gateway/gateway.wizard.e2e.test.ts`).

What’s still missing for skills (see [Skills](/tools/skills)):

- **Decisioning:** when skills are listed in the prompt, does the agent pick the right skill (or avoid irrelevant ones)?
- **Compliance:** does the agent read `SKILL.md` before use and follow required steps/args?
- **Workflow contracts:** multi-turn scenarios that assert tool order, session history carryover, and sandbox boundaries.

Future evals should stay deterministic first:

- A scenario runner using mock providers to assert tool calls + order, skill file reads, and session wiring.
- A small suite of skill-focused scenarios (use vs avoid, gating, prompt injection).
- Optional live evals (opt-in, env-gated) only after the CI-safe suite is in place.

## Adding regressions (guidance)

When you fix a provider/model issue discovered in live:

- Add a CI-safe regression if possible (mock/stub provider, or capture the exact request-shape transformation)
- If it’s inherently live-only (rate limits, auth policies), keep the live test narrow and opt-in via env vars
- Prefer targeting the smallest layer that catches the bug:
  - provider request conversion/replay bug → direct models test
  - gateway session/history/tool pipeline bug → gateway live smoke or CI-safe gateway mock test
