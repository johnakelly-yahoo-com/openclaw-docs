---
summary: "Remote access using SSH tunnels (Gateway WS) and tailnets"
read_when:
  - Running or troubleshooting remote gateway setups
title: "Remote Access"
---

# Remote access (SSH, tunnels, and tailnets)

This repo supports “remote over SSH” by keeping a single Gateway (the master) running on a dedicated host (desktop/server) and connecting clients to it.

- For **operators (you / the macOS app)**: SSH tunneling is the universal fallback.
- For **nodes (iOS/Android and future devices)**: connect to the Gateway **WebSocket** (LAN/tailnet or SSH tunnel as needed).

## The core idea

- The Gateway WebSocket binds to **loopback** on your configured port (defaults to 18789).
- For remote use, you forward that loopback port over SSH (or use a tailnet/VPN and tunnel less).

## Common VPN/tailnet setups (where the agent lives)

Think of the **Gateway host** as “where the agent lives.” It owns sessions, auth profiles, channels, and state.
Your laptop/desktop (and nodes) connect to that host.

### 1. Always-on Gateway in your tailnet (VPS or home server)

Run the Gateway on a persistent host and reach it via **Tailscale** or SSH.

- **Best UX:** keep `gateway.bind: "loopback"` and use **Tailscale Serve** for the Control UI.
- **Fallback:** keep loopback + SSH tunnel from any machine that needs access.
- **Examples:** [exe.dev](/install/exe-dev) (easy VM) or [Hetzner](/install/hetzner) (production VPS).

This is ideal when your laptop sleeps often but you want the agent always-on.

### 2. Home desktop runs the Gateway, laptop is remote control

The laptop does **not** run the agent. It connects remotely:

- Use the macOS app’s **Remote over SSH** mode (Settings → General → “OpenClaw runs”).
- The app opens and manages the tunnel, so WebChat + health checks “just work.”

Runbook: [macOS remote access](/platforms/mac/remote).

### 3. Laptop runs the Gateway, remote access from other machines

Keep the Gateway local but expose it safely:

- SSH tunnel to the laptop from other machines, or
- Tailscale Serve the Control UI and keep the Gateway loopback-only.

Guide: [Tailscale](/gateway/tailscale) and [Web overview](/web).

## Command flow (what runs where)

One gateway service owns state + channels. Nodes are peripherals.

Flow example (Telegram → node):

- Telegram message arrives at the **Gateway**.
- Gateway runs the **agent** and decides whether to call a node tool.
- Gateway calls the **node** over the Gateway WebSocket (`node.*` RPC).
- Node returns the result; Gateway replies back out to Telegram.

Notes:

- **Nodes do not run the gateway service.** Only one gateway should run per host unless you intentionally run isolated profiles (see [Multiple gateways](/gateway/multiple-gateways)).
- macOS app “node mode” is just a node client over the Gateway WebSocket.

## SSH tunnel (CLI + tools)

Create a local tunnel to the remote Gateway WS:

```bash
ssh -N -L 18789:127.0.0.1:18789 user@host
```

With the tunnel up:

- `openclaw health` and `openclaw status --deep` now reach the remote gateway via `ws://127.0.0.1:18789`.
- `openclaw gateway {status,health,send,agent,call}` can also target the forwarded URL via `--url` when needed.

Note: replace `18789` with your configured `gateway.port` (or `--port`/`OPENCLAW_GATEWAY_PORT`).
Note: when you pass `--url`, the CLI does not fall back to config or environment credentials.
Include `--token` or `--password` explicitly. Missing explicit credentials is an error.

## CLI remote defaults

You can persist a remote target so CLI commands use it by default:

```json5
{
  gateway: {
    mode: "remote",
    remote: {
      url: "ws://127.0.0.1:18789",
      token: "your-token",
    },
  },
}
```

Agar gateway faqat loopback rejimida bo‘lsa, URL’ni `ws://127.0.0.1:18789` holatida qoldiring va avval SSH tunnelini oching.

## SSH orqali Chat UI

WebChat endi alohida HTTP portdan foydalanmaydi. SwiftUI chat UI to‘g‘ridan-to‘g‘ri Gateway WebSocket’iga ulanadi.

- SSH orqali `18789` ni forward qiling (yuqoriga qarang), so‘ng klientlarni `ws://127.0.0.1:18789` ga ulang.
- macOS’da tunnelni avtomatik boshqaradigan ilovaning “Remote over SSH” rejimini afzal ko‘ring.

## macOS ilovasi “Remote over SSH”

macOS menyu panelidagi ilova bir xil sozlamani boshidan oxirigacha boshqarishi mumkin (masofaviy holat tekshiruvlari, WebChat va Voice Wake forwarding).

Runbook: [macOS remote access](/platforms/mac/remote).

## Xavfsizlik qoidalari (remote/VPN)

Qisqa versiya: **Gateway’ni loopback-only holatda saqlang**, agar bind kerakligiga ishonchingiz komil bo‘lmasa.

- **Loopback + SSH/Tailscale Serve** eng xavfsiz standartdir (ommaviy ochilishsiz).
- **Non-loopback bindlar** (`lan`/`tailnet`/`custom`, yoki loopback mavjud bo‘lmaganda `auto`) auth tokenlar/parollardan foydalanishi shart.
- `gateway.remote.token` **faqat** masofaviy CLI chaqiriqlari uchun — u lokal auth’ni **yoqmaydi**.
- `gateway.remote.tlsFingerprint` `wss://` ishlatilganda masofaviy TLS sertifikatini pin qiladi.
- **Tailscale Serve** `gateway.auth.allowTailscale: true` bo‘lganda identifikatsiya sarlavhalari orqali autentifikatsiya qilishi mumkin.
  Agar tokenlar/parollarni xohlasangiz, uni `false` ga o‘rnating.
- Brauzer boshqaruvini operator kirishi kabi ko‘ring: faqat tailnet + ongli node juftlash.

Chuqur tahlil: [Security](/gateway/security).
