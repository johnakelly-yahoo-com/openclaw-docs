---
summary: "Loopback WebChat static host and Gateway WS usage for chat UI"
read_when:
  - Debugging or configuring WebChat access
title: "WebChat"
---

# WebChat (Gateway WebSocket UI)

Status: the macOS/iOS SwiftUI chat UI talks directly to the Gateway WebSocket.

## What it is

- A native chat UI for the gateway (no embedded browser and no local static server).
- Uses the same sessions and routing rules as other channels.
- Deterministic routing: replies always go back to WebChat.

## Quick start

1. Start the gateway.
2. Open the WebChat UI (macOS/iOS app) or the Control UI chat tab.
3. Ensure gateway auth is configured (required by default, even on loopback).

## How it works (behavior)

- The UI connects to the Gateway WebSocket and uses `chat.history`, `chat.send`, and `chat.inject`.
- `chat.inject` appends an assistant note directly to the transcript and broadcasts it to the UI (no agent run).
- History is always fetched from the gateway (no local file watching).
- If the gateway is unreachable, WebChat is read-only.

## Remote use

- Remote mode tunnels the gateway WebSocket over SSH/Tailscale.
- You do not need to run a separate WebChat server.

## Configuration reference (WebChat)

Full configuration: [Configuration](/gateway/configuration)

2. Maxsus `webchat.*` bloki yo‘q.

- 3. WebChat quyidagi gateway endpointi + autentifikatsiya sozlamalaridan foydalanadi. 4. Tegishli global sozlamalar:

5. `gateway.port`, `gateway.bind`: WebSocket xost/porti.

- 6. `gateway.auth.mode`, `gateway.auth.token`, `gateway.auth.password`: WebSocket autentifikatsiyasi.
- 7. `gateway.remote.url`, `gateway.remote.token`, `gateway.remote.password`: masofaviy gateway manzili.
- 8. `session.*`: sessiya saqlash va asosiy kalitning sukut bo‘yicha qiymatlari.
- 9. {
     agents: {
     list: [
     { id: "main" },
     {
     id: "clawd-fan",
     workspace: "/home/user/clawd-fan",
     agentDir: "/home/user/.openclaw/agents/clawd-fan/agent",
     },
     {
     id: "clawd-xi",
     workspace: "/home/user/clawd-xi",
     agentDir: "/home/user/.openclaw/agents/clawd-xi/agent",
     },
     ],
     },
     bindings: [
     {
     agentId: "main",
     match: {
     channel: "feishu",
     peer: { kind: "direct", id: "ou_xxx" },
     },
     },
     {
     agentId: "clawd-fan",
     match: {
     channel: "feishu",
     peer: { kind: "direct", id: "ou_yyy" },
     },
     },
     {
     agentId: "clawd-xi",
     match: {
     channel: "feishu",
     peer: { kind: "group", id: "oc_zzz" },
     },
     },
     ],
     }
