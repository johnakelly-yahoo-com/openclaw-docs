---
summary: "Expose an OpenResponses-compatible /v1/responses HTTP endpoint from the Gateway"
read_when:
  - Integrating clients that speak the OpenResponses API
  - You want item-based inputs, client tool calls, or SSE events
title: "OpenResponses API"
---

# OpenResponses API (HTTP)

OpenClaw’s Gateway can serve an OpenResponses-compatible `POST /v1/responses` endpoint.

This endpoint is **disabled by default**. Enable it in config first.

- `POST /v1/responses`
- Same port as the Gateway (WS + HTTP multiplex): `http://<gateway-host>:<port>/v1/responses`

Under the hood, requests are executed as a normal Gateway agent run (same codepath as
`openclaw agent`), so routing/permissions/config match your Gateway.

## Authentication

Uses the Gateway auth configuration. Send a bearer token:

- `Authorization: Bearer <token>`

Notes:

- When `gateway.auth.mode="token"`, use `gateway.auth.token` (or `OPENCLAW_GATEWAY_TOKEN`).
- When `gateway.auth.mode="password"`, use `gateway.auth.password` (or `OPENCLAW_GATEWAY_PASSWORD`).

## Choosing an agent

No custom headers required: encode the agent id in the OpenResponses `model` field:

- `model: "openclaw:<agentId>"` (example: `"openclaw:main"`, `"openclaw:beta"`)
- `model: "agent:<agentId>"` (alias)

Or target a specific OpenClaw agent by header:

- `x-openclaw-agent-id: <agentId>` (default: `main`)

Advanced:

- `x-openclaw-session-key: <sessionKey>` to fully control session routing.

## Endpointni yoqish

`gateway.http.endpoints.responses.enabled` ni `true` ga o‘rnating:

```json5
{
  gateway: {
    http: {
      endpoints: {
        responses: { enabled: true },
      },
    },
  },
}
```

## Endpointni o‘chirish

`gateway.http.endpoints.responses.enabled` ni `false` ga o‘rnating:

```json5
{
  gateway: {
    http: {
      endpoints: {
        responses: { enabled: false },
      },
    },
  },
}
```

## Sessiya xulq-atvori

Standart holatda endpoint **har bir so‘rov uchun stateless** (har bir chaqiruvda yangi sessiya kaliti yaratiladi).

Agar so‘rov OpenResponses `user` qatorini o‘z ichiga olsa, Gateway undan barqaror sessiya kalitini hosil qiladi, shunda takroriy chaqiruvlar bitta agent sessiyasini bo‘lishishi mumkin.

## So‘rov shakli (qo‘llab-quvvatlanadi)

So‘rov itemlarga asoslangan kirish bilan OpenResponses API ga amal qiladi. Joriy qo‘llab-quvvatlash:

- `input`: satr yoki item obyektlari massivi.
- `instructions`: system prompt ga birlashtiriladi.
- `tools`: mijoz asboblari ta’riflari (funksiya asboblari).
- `tool_choice`: mijoz tool’larini filtrlash yoki majburiy qilish.
- `stream`: SSE oqimini yoqadi.
- `max_output_tokens`: eng yaxshi urinishdagi chiqish limiti (provayderga bog‘liq).
- `user`: barqaror sessiya marshrutlash.

Qabul qilinadi, ammo **hozircha e’tiborsiz qoldiriladi**:

- `max_tool_calls`
- `reasoning`
- `metadata`
- `store`
- `previous_response_id`
- `truncation`

## Itemlar (kiritish)

### `message`

Rollar: `system`, `developer`, `user`, `assistant`.

- `system` va `developer` system prompt ga qo‘shiladi.
- Eng so‘nggi `user` yoki `function_call_output` itemi “joriy xabar” ga aylanadi.
- Oldingi user/assistant xabarlari kontekst uchun tarix sifatida kiritiladi.

### `function_call_output` (navbatga asoslangan tool’lar)

Tool natijalarini modelga qayta yuboring:

```json
{
  "type": "function_call_output",
  "call_id": "call_123",
  "output": "{\"temperature\": \"72F\"}"
}
```

### `reasoning` va `item_reference`

Sxema mosligi uchun qabul qilinadi, ammo promptni tuzishda e’tiborsiz qoldiriladi.

## Tool’lar (mijoz tomoni funksiya tool’lari)

`tools: [{ type: "function", function: { name, description?, parameters?
    } }]` orqali tool’larni taqdim eting. Agar agent tool chaqirishga qaror qilsa, javob `function_call` chiqish itemini qaytaradi.

Keyin navbatni davom ettirish uchun `function_call_output` bilan keyingi so‘rovni yuborasiz.
Rasmlar (`input_image`)

## Base64 yoki URL manbalarini qo‘llab-quvvatlaydi:

{
"type": "input_image",
"source": { "type": "url", "url": "https://example.com/image.png" }
}

```json
Ruxsat etilgan MIME turlari (joriy): `image/jpeg`, `image/png`, `image/gif`, `image/webp`.
```

Maksimal hajm (joriy): 10MB.
Fayllar (`input_file`)

## Base64 yoki URL manbalarini qo‘llab-quvvatlaydi:

{
"type": "input_file",
"source": {
"type": "base64",
"media_type": "text/plain",
"data": "SGVsbG8gV29ybGQh",
"filename": "hello.txt"
}
}

```json
{
  "type": "input_file",
  "source": {
    "type": "base64",
    "media_type": "text/plain",
    "data": "SGVsbG8gV29ybGQh",
    "filename": "hello.txt"
  }
}
```

1. Ruxsat etilgan MIME turlari (joriy): `text/plain`, `text/markdown`, `text/html`, `text/csv`,
   `application/json`, `application/pdf`.

2. Maksimal hajm (joriy): 5MB.

3. Joriy xatti-harakat:

- 4. Fayl mazmuni dekodlanadi va foydalanuvchi xabariga emas, balki **system prompt** ga qo‘shiladi,
     shuning uchun u vaqtinchalik bo‘lib qoladi (sessiya tarixida saqlanmaydi).
- 5. PDF fayllardan matn ajratib olinadi. 6. Agar matn kam topilsa, birinchi sahifalar rasterizatsiya qilinadi
     va modelga tasvirlar sifatida uzatiladi.

7. PDF tahlili Node uchun mos `pdfjs-dist` legacy build yordamida amalga oshiriladi (worker yo‘q). 8. Zamonaviy
   PDF.js build brauzer workerlari/DOM global o‘zgaruvchilarini talab qiladi, shuning uchun Gateway’da ishlatilmaydi.

9. URL orqali yuklash uchun standart sozlamalar:

- 10. `files.allowUrl`: `true`
- 11. `images.allowUrl`: `true`
- 12. So‘rovlar himoyalangan (DNS aniqlash, xususiy IP’larni bloklash, yo‘naltirishlar soni cheklovi, timeoutlar).

## 13. Fayl + tasvir cheklovlari (konfiguratsiya)

Standart sozlamalarni `gateway.http.endpoints.responses` ostida moslash mumkin:

```json5
15. {
  gateway: {
    http: {
      endpoints: {
        responses: {
          enabled: true,
          maxBodyBytes: 20000000,
          files: {
            allowUrl: true,
            allowedMimes: [
              "text/plain",
              "text/markdown",
              "text/html",
              "text/csv",
              "application/json",
              "application/pdf",
            ],
            maxBytes: 5242880,
            maxChars: 200000,
            maxRedirects: 3,
            timeoutMs: 10000,
            pdf: {
              maxPages: 4,
              maxPixels: 4000000,
              minTextChars: 200,
            },
          },
          images: {
            allowUrl: true,
            allowedMimes: ["image/jpeg", "image/png", "image/gif", "image/webp"],
            maxBytes: 10485760,
            maxRedirects: 3,
            timeoutMs: 10000,
          },
        },
      },
    },
  },
}
```

16. Ko‘rsatilmaganida qo‘llaniladigan standartlar:

- 17. `maxBodyBytes`: 20MB
- 18. `files.maxBytes`: 5MB
- 19. `files.maxChars`: 200k
- `files.maxRedirects`: 3
- 21. `files.timeoutMs`: 10s
- 22. `files.pdf.maxPages`: 4
- 23. `files.pdf.maxPixels`: 4,000,000
- 24. `files.pdf.minTextChars`: 200
- 25. `images.maxBytes`: 10MB
- 26. `images.maxRedirects`: 3
- 27. `images.timeoutMs`: 10s

## 28. Oqimli uzatish (SSE)

29. Server-Sent Events (SSE) olish uchun `stream: true` ni o‘rnating:

- 30. `Content-Type: text/event-stream`
- 31. Har bir hodisa satri `event: <type>` va `data: <json>` ko‘rinishida bo‘ladi
- 32. Oqim `data: [DONE]` bilan yakunlanadi

33. Hozirda chiqariladigan hodisa turlari:

- 34. `response.created`
- 35. `response.in_progress`
- 36. `response.output_item.added`
- 37. `response.content_part.added`
- 38. `response.output_text.delta`
- 39. `response.output_text.done`
- 40. `response.content_part.done`
- 41. `response.output_item.done`
- 42. `response.completed`
- 43. `response.failed` (xato yuz berganda)

## 44. Foydalanish

45. `usage` asosiy provayder tokenlar sonini bildirganda to‘ldiriladi.

## 46. Xatolar

47. Xatolar quyidagiga o‘xshash JSON obyektidan foydalanadi:

```json
48. { "error": { "message": "...", "type": "invalid_request_error" } }
```

49. Keng tarqalgan holatlar:

- 50. `401` — autentifikatsiya yo‘q yoki noto‘g‘ri
- `400` noto‘g‘ri so‘rov tanasi
- `405` noto‘g‘ri metod

## Misollar

Oqimsiz:

```bash
curl -sS http://127.0.0.1:18789/v1/responses \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'x-openclaw-agent-id: main' \
  -d '{
    "model": "openclaw",
    "input": "hi"
  }'
```

Oqimli:

```bash
curl -N http://127.0.0.1:18789/v1/responses \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'x-openclaw-agent-id: main' \
  -d '{
    "model": "openclaw",
    "stream": true,
    "input": "hi"
  }'
```
