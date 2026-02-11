---
summary: "Reja: OpenResponses /v1/responses endpointini qo‘shish va chat completions’ni toza tarzda eskirtirish"
owner: "openclaw"
status: "qoralama"
last_updated: "2026-01-19"
title: "OpenResponses Gateway rejasi"
---

# OpenResponses Gateway integratsiya rejasi

## Kontekst

OpenClaw Gateway hozirda OpenAI’ga mos minimal Chat Completions endpointini taqdim etadi
`/v1/chat/completions` da (qarang: [OpenAI Chat Completions](/gateway/openai-http-api)).

Open Responses — OpenAI Responses API asosidagi ochiq inferensiya standarti. U agentik ish jarayonlari uchun mo‘ljallangan
va elementlarga asoslangan kirishlar hamda semantik streaming hodisalaridan foydalanadi. OpenResponses
spetsifikatsiyasi `/v1/chat/completions` emas, balki `/v1/responses` ni belgilaydi.

## Maqsadlar

- OpenResponses semantikasiga mos keladigan `/v1/responses` endpointini qo‘shish.
- Chat Completions’ni o‘chirish oson bo‘lgan va oxir-oqibat olib tashlanadigan moslik qatlami sifatida saqlash.
- Izolyatsiyalangan, qayta foydalaniladigan sxemalar bilan validatsiya va parsingni standartlashtirish.

## Maqsad emas

- Birinchi bosqichda OpenResponses’ning to‘liq funksional tengligi (rasmlar, fayllar, xostlangan vositalar).
- Ichki agent bajarish mantiqi yoki vositalarni orkestratsiya qilishni almashtirish.
- Birinchi bosqich davomida mavjud `/v1/chat/completions` xatti-harakatini o‘zgartirish.

## Tadqiqot xulosasi

Manbalar: OpenResponses OpenAPI, OpenResponses spetsifikatsiya sayti va Hugging Face blog posti.

Ajratib olingan asosiy nuqtalar:

- `POST /v1/responses` `CreateResponseBody` maydonlarini qabul qiladi, masalan `model`, `input` (satr yoki
  `ItemParam[]`), `instructions`, `tools`, `tool_choice`, `stream`, `max_output_tokens` va
  `max_tool_calls`.
- `ItemParam` quyidagilardan iborat diskriminatsiyalangan birlashmadir:
  - `system`, `developer`, `user`, `assistant` rollariga ega `message` elementlari
  - `function_call` va `function_call_output`
  - `reasoning`
  - `item_reference`
- Muvaffaqiyatli javoblar `object: "response"`, `status` va
  `output` elementlariga ega `ResponseResource` ni qaytaradi.
- Streaming quyidagi semantik hodisalardan foydalanadi:
  - `response.created`, `response.in_progress`, `response.completed`, `response.failed`
  - `response.output_item.added`, `response.output_item.done`
  - `response.content_part.added`, `response.content_part.done`
  - `response.output_text.delta`, `response.output_text.done`
- Spetsifikatsiya quyidagini talab qiladi:
  - `Content-Type: text/event-stream`
  - `event:` must match the JSON `type` field
  - terminal event must be literal `[DONE]`
- Reasoning items may expose `content`, `encrypted_content`, and `summary`.
- HF examples include `OpenResponses-Version: latest` in requests (optional header).

## Proposed Architecture

- Add `src/gateway/open-responses.schema.ts` containing Zod schemas only (no gateway imports).
- Add `src/gateway/openresponses-http.ts` (or `open-responses-http.ts`) for `/v1/responses`.
- Keep `src/gateway/openai-http.ts` intact as a legacy compatibility adapter.
- Add config `gateway.http.endpoints.responses.enabled` (default `false`).
- Keep `gateway.http.endpoints.chatCompletions.enabled` independent; allow both endpoints to be
  toggled separately.
- Emit a startup warning when Chat Completions is enabled to signal legacy status.

## Deprecation Path for Chat Completions

- Maintain strict module boundaries: no shared schema types between responses and chat completions.
- Make Chat Completions opt-in by config so it can be disabled without code changes.
- Update docs to label Chat Completions as legacy once `/v1/responses` is stable.
- Optional future step: map Chat Completions requests to the Responses handler for a simpler
  removal path.

## Phase 1 Support Subset

- Accept `input` as string or `ItemParam[]` with message roles and `function_call_output`.
- Extract system and developer messages into `extraSystemPrompt`.
- Use the most recent `user` or `function_call_output` as the current message for agent runs.
- Reject unsupported content parts (image/file) with `invalid_request_error`.
- Return a single assistant message with `output_text` content.
- Return `usage` with zeroed values until token accounting is wired.

## Validation Strategy (No SDK)

- Implement Zod schemas for the supported subset of:
  - `CreateResponseBody`
  - `ItemParam` + message content part unions
  - `ResponseResource`
  - Streaming event shapes used by the gateway
- Keep schemas in a single, isolated module to avoid drift and allow future codegen.

## Streaming Implementation (Phase 1)

- SSE lines with both `event:` and `data:`.
- Required sequence (minimum viable):
  - `response.created`
  - `response.output_item.added`
  - `response.content_part.added`
  - `response.output_text.delta` (repeat as needed)
  - `response.output_text.done`
  - `response.content_part.done`
  - `response.completed`
  - `[DONE]`

## Tests and Verification Plan

- Add e2e coverage for `/v1/responses`:
  - Auth required
  - Non-stream response shape
  - Stream event ordering and `[DONE]`
  - Session routing with headers and `user`
- Keep `src/gateway/openai-http.e2e.test.ts` unchanged.
- Manual: curl to `/v1/responses` with `stream: true` and verify event ordering and terminal
  `[DONE]`.

## Doc Updates (Follow-up)

- `/v1/responses` dan foydalanish va misollar uchun yangi hujjatlar sahifasini qo‘shish.
- `/gateway/openai-http-api` ni meros (legacy) eslatmasi va `/v1/responses` ga yo‘naltirish bilan yangilash.
