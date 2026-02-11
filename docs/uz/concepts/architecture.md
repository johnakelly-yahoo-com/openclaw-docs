---
summary: "WebSocket gateway architecture, components, and client flows"
read_when:
  - Working on gateway protocol, clients, or transports
title: "Gateway Architecture"
---

# Gateway architecture

Last updated: 2026-01-22

## Overview

- A single long‑lived **Gateway** owns all messaging surfaces (WhatsApp via
  Baileys, Telegram via grammY, Slack, Discord, Signal, iMessage, WebChat).
- Control-plane clients (macOS app, CLI, web UI, automations) connect to the
  Gateway over **WebSocket** on the configured bind host (default
  `127.0.0.1:18789`).
- **Nodes** (macOS/iOS/Android/headless) also connect over **WebSocket**, but
  declare `role: node` with explicit caps/commands.
- One Gateway per host; it is the only place that opens a WhatsApp session.
- A **canvas host** (default `18793`) serves agent‑editable HTML and A2UI.

## Components and flows

### Gateway (daemon)

- Maintains provider connections.
- Exposes a typed WS API (requests, responses, server‑push events).
- Validates inbound frames against JSON Schema.
- Emits events like `agent`, `chat`, `presence`, `health`, `heartbeat`, `cron`.

### Clients (mac app / CLI / web admin)

- One WS connection per client.
- Send requests (`health`, `status`, `send`, `agent`, `system-presence`).
- Subscribe to events (`tick`, `agent`, `presence`, `shutdown`).

### Nodes (macOS / iOS / Android / headless)

- Connect to the **same WS server** with `role: node`.
- Provide a device identity in `connect`; pairing is **device‑based** (role `node`) and
  approval lives in the device pairing store.
- Expose commands like `canvas.*`, `camera.*`, `screen.record`, `location.get`.

Protocol details:

- [Gateway protocol](/gateway/protocol)

### WebChat

- Chat tarixi va yuborish uchun Gateway WS API’dan foydalanadigan statik UI.
- Masofaviy sozlamalarda, boshqa mijozlar bilan bir xil SSH/Tailscale tunneli orqali ulanadi.

## **Mahalliy bo‘lmagan** ulanishlar `connect.challenge` nonce’ini imzolashi va aniq tasdiqni talab qiladi.

```mermaid
42. `scope` qidiruvni rad etsa, OpenClaw aniqlangan `channel`/`chatType` bilan ogohlantirishni logga yozadi, shunda bo‘sh natijalarni tuzatish osonroq bo‘ladi.
```

## Simli protokol (qisqacha)

- Transport: WebSocket, JSON yuklamali matn freymlari.
- Birinchi freym **albatta** `connect` bo‘lishi kerak.
- Qo‘l siqishdan so‘ng:
  - So‘rovlar: `{type:"req", id, method, params}` → `{type:"res", id, ok, payload|error}`
  - Hodisalar: `{type:"event", event, payload, seq?, stateVersion?}`
- Agar `OPENCLAW_GATEWAY_TOKEN` (yoki `--token`) o‘rnatilgan bo‘lsa, `connect.params.auth.token` mos kelishi **shart**, aks holda soket yopiladi.
- Yon ta’sirga ega metodlar (`send`, `agent`) uchun xavfsiz qayta urinish maqsadida idempotentlik kalitlari talab qilinadi; server qisqa muddatli deduplikatsiya keshini saqlaydi.
- Tugunlar `connect` da `role: "node"` hamda caps/commands/permissions ni o‘z ichiga olishi kerak.

## Juftlash + mahalliy ishonch

- Barcha WS mijozlari (operatorlar + tugunlar) `connect` da **qurilma identifikatori** ni kiritadi.
- Yangi qurilma ID’lari juftlashni tasdiqlashni talab qiladi; Gateway keyingi ulanishlar uchun **qurilma tokeni** beradi.
- **Mahalliy** ulanishlar (loopback yoki gateway xostining o‘z tailnet manzili) bir xostdagi UX silliq bo‘lishi uchun avtomatik tasdiqlanishi mumkin.
- Tafsilotlar: [Gateway protocol](/gateway/protocol), [Pairing](/channels/pairing), [Security](/gateway/security).
- Gateway autentifikatsiyasi (`gateway.auth.*`) **barcha** ulanishlarga, mahalliy yoki masofaviy bo‘lishidan qat’i nazar, amal qiladi.

Xuddi shu handshake + auth token tunnel orqali ham qo‘llaniladi.

## Protokol tiplari va kod generatsiyasi

- TypeBox sxemalari protokolni belgilaydi.
- JSON Schema shu sxemalardan generatsiya qilinadi.
- Swift modellari JSON Schema’dan generatsiya qilinadi.

## Masofaviy kirish

- Afzal: Tailscale yoki VPN.

- Muqobil: SSH tunneli

  ```bash
  ssh -N -L 18789:127.0.0.1:18789 user@host
  ```

- Operatsiyalar snapshot’i

- Masofaviy sozlamalarda WS uchun TLS + ixtiyoriy pinning yoqilishi mumkin.

## **Project Context** ostida kiritilgan workspace bootstrap fayllari.

- Boshlash: `openclaw gateway` (oldingi rejimda, loglar stdout’ga).
- Sog‘liq: WS orqali `health` (shuningdek `hello-ok` ga kiritilgan).
- Nazorat: avtomatik qayta ishga tushirish uchun launchd/systemd.

## O‘zgarmaslar

- Har bir xostda aynan bitta Gateway bitta Baileys sessiyasini boshqaradi.
- Qo‘l siqish majburiy; JSON bo‘lmagan yoki birinchi freymi `connect` bo‘lmagan har qanday holat darhol yopiladi.
- Hodisalar qayta ijro etilmaydi; bo‘shliqlar bo‘lsa, mijozlar yangilashi kerak.
