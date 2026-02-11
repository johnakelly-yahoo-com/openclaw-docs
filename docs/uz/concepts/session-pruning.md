---
summary: "Session pruning: tool-result trimming to reduce context bloat"
read_when:
  - You want to reduce LLM context growth from tool outputs
  - You are tuning agents.defaults.contextPruning
---

# Session Pruning

Session pruning trims **old tool results** from the in-memory context right before each LLM call. It does **not** rewrite the on-disk session history (`*.jsonl`).

## When it runs

- When `mode: "cache-ttl"` is enabled and the last Anthropic call for the session is older than `ttl`.
- Only affects the messages sent to the model for that request.
- Only active for Anthropic API calls (and OpenRouter Anthropic models).
- Asboblarni ruxsat berish/taqiqlash ro‘yxatlari — bu **asboblar**, ko‘nikmalar emas.
- After a prune, the TTL window resets so subsequent requests keep cache until `ttl` expires again.

## Smart defaults (Anthropic)

- **OAuth or setup-token** profiles: enable `cache-ttl` pruning and set heartbeat to `1h`.
- **API key** profiles: enable `cache-ttl` pruning, set heartbeat to `30m`, and default `cacheControlTtl` to `1h` on Anthropic models.
- If you set any of these values explicitly, OpenClaw does **not** override them.

## What this improves (cost + cache behavior)

- **Why prune:** Anthropic prompt caching only applies within the TTL. If a session goes idle past the TTL, the next request re-caches the full prompt unless you trim it first.
- **What gets cheaper:** pruning reduces the **cacheWrite** size for that first request after the TTL expires.
- **Why the TTL reset matters:** once pruning runs, the cache window resets, so follow‑up requests can reuse the freshly cached prompt instead of re-caching the full history again.
- **What it does not do:** pruning doesn’t add tokens or “double” costs; it only changes what gets cached on that first post‑TTL request.

## What can be pruned

- Only `toolResult` messages.
- User + assistant messages are **never** modified.
- The last `keepLastAssistants` assistant messages are protected; tool results after that cutoff are not pruned.
- If there aren’t enough assistant messages to establish the cutoff, pruning is skipped.
- Tool results containing **image blocks** are skipped (never trimmed/cleared).

## Context window estimation

Pruning uses an estimated context window (chars ≈ tokens × 4). The base window is resolved in this order:

1. `models.providers.*.models[].contextWindow` override.
2. Model definition `contextWindow` (from the model registry).
3. Default `200000` tokens.

If `agents.defaults.contextTokens` is set, it is treated as a cap (min) on the resolved window.

## Mode

### cache-ttl

- Pruning only runs if the last Anthropic call is older than `ttl` (default `5m`).
- Ishga tushganda: avvalgidek bir xil soft-trim + hard-clear xatti-harakati.

## Soft va hard pruning

- **Soft-trim**: faqat haddan tashqari katta tool natijalari uchun.
  - Bosh va oxirini saqlaydi, `...` qo‘shadi va asl hajmi bilan eslatma ilova qiladi.
  - Rasm bloklari bo‘lgan natijalarni o‘tkazib yuboradi.
- **Hard-clear**: butun tool natijasini `hardClear.placeholder` bilan almashtiradi.

## Tool tanlash

- `tools.allow` / `tools.deny` `*` wildcardlarni qo‘llab-quvvatlaydi.
- Deny ustun keladi.
- Moslash katta-kichik harfga sezgir emas.
- Bo‘sh allow ro‘yxati => barcha tool’lar ruxsat etilgan.

## Boshqa limitlar bilan o‘zaro ta’sir

- O‘rnatilgan tool’lar allaqachon o‘z chiqishini qisqartiradi; session pruning esa model kontekstida uzoq davom etadigan chatlarda juda ko‘p tool chiqishi to‘planib ketmasligi uchun qo‘shimcha qatlamdir.
- Compaction alohida: compaction xulosa qiladi va saqlab qoladi, pruning esa har bir so‘rov uchun vaqtinchalik. Eng yaxshi natijalar uchun `ttl` ni modelingizdagi `cacheControlTtl` bilan moslang.

## Standartlar (yoqilganda)

- `ttl`: `"5m"`
- `keepLastAssistants`: `3`
- `softTrimRatio`: `0.3`
- `hardClearRatio`: `0.5`
- `minPrunableToolChars`: `50000`
- `softTrim`: `{ maxChars: 4000, headChars: 1500, tailChars: 1500 }`
- `hardClear`: `{ enabled: true, placeholder: "[Old tool result content cleared]" }`

## Misollar

Standart (o‘chiq):

```json5
{
  agent: {
    contextPruning: { mode: "off" },
  },
}
```

TTL’ni hisobga olgan pruning’ni yoqish:

```json5
{
  agent: {
    contextPruning: { mode: "cache-ttl", ttl: "5m" },
  },
}
```

Pruning’ni muayyan tool’lar bilan cheklash:

```json5
{
  agent: {
    contextPruning: {
      mode: "cache-ttl",
      tools: { allow: ["exec", "read"], deny: ["*image*"] },
    },
  },
}
```

Config ma’lumotnomasini ko‘ring: [Gateway Configuration](/gateway/configuration)
