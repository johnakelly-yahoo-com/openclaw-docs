---
title: Fly.io
description: Deploy OpenClaw on Fly.io
---

# Fly.io Deployment

**Goal:** OpenClaw Gateway running on a [Fly.io](https://fly.io) machine with persistent storage, automatic HTTPS, and Discord/channel access.

## What you need

- [flyctl CLI](https://fly.io/docs/hands-on/install-flyctl/) installed
- Fly.io account (free tier works)
- Model auth: Anthropic API key (or other provider keys)
- Channel credentials: Discord bot token, Telegram token, etc.

## Beginner quick path

1. Clone repo → customize `fly.toml`
2. Create app + volume → set secrets
3. Deploy with `fly deploy`
4. SSH in to create config or use Control UI

## 1) Create the Fly app

```bash
# Clone the repo
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# Create a new Fly app (pick your own name)
fly apps create my-openclaw

# Create a persistent volume (1GB is usually enough)
fly volumes create openclaw_data --size 1 --region iad
```

**Tip:** Choose a region close to you. Common options: `lhr` (London), `iad` (Virginia), `sjc` (San Jose).

## 2. Configure fly.toml

Edit `fly.toml` to match your app name and requirements.

**Security note:** The default config exposes a public URL. For a hardened deployment with no public IP, see [Private Deployment](#private-deployment-hardened) or use `fly.private.toml`.

```toml
app = "my-openclaw"  # Your app name
primary_region = "iad"

[build]
  dockerfile = "Dockerfile"

[env]
  NODE_ENV = "production"
  OPENCLAW_PREFER_PNPM = "1"
  OPENCLAW_STATE_DIR = "/data"
  NODE_OPTIONS = "--max-old-space-size=1536"

[processes]
  app = "node dist/index.js gateway --allow-unconfigured --port 3000 --bind lan"

[http_service]
  internal_port = 3000
  force_https = true
  auto_stop_machines = false
  auto_start_machines = true
  min_machines_running = 1
  processes = ["app"]

[[vm]]
  size = "shared-cpu-2x"
  memory = "2048mb"

[mounts]
  source = "openclaw_data"
  destination = "/data"
```

**Key settings:**

| Setting                        | Why                                                                                            |
| ------------------------------ | ---------------------------------------------------------------------------------------------- |
| `--bind lan`                   | Binds to `0.0.0.0` so Fly's proxy can reach the gateway                                        |
| `--allow-unconfigured`         | Starts without a config file (you'll create one after)                      |
| `internal_port = 3000`         | Must match `--port 3000` (or `OPENCLAW_GATEWAY_PORT`) for Fly health checks |
| `memory = "2048mb"`            | 512MB is too small; 2GB recommended                                                            |
| `OPENCLAW_STATE_DIR = "/data"` | Persists state on the volume                                                                   |

## 3. Set secrets

```bash
# Required: Gateway token (for non-loopback binding)
fly secrets set OPENCLAW_GATEWAY_TOKEN=$(openssl rand -hex 32)

# Model provider API keys
fly secrets set ANTHROPIC_API_KEY=sk-ant-...

# Optional: Other providers
fly secrets set OPENAI_API_KEY=sk-...
fly secrets set GOOGLE_API_KEY=...

# Channel tokens
fly secrets set DISCORD_BOT_TOKEN=MTQ...
```

**Notes:**

- Non-loopback binds (`--bind lan`) require `OPENCLAW_GATEWAY_TOKEN` for security.
- Treat these tokens like passwords.
- **Prefer env vars over config file** for all API keys and tokens. This keeps secrets out of `openclaw.json` where they could be accidentally exposed or logged.

## 4. Deploy

```bash
fly deploy
```

First deploy builds the Docker image (~2-3 minutes). Keyingi deploylar tezroq bo‘ladi.

Deploydan so‘ng tekshiring:

```bash
fly status
fly logs
```

Quyidagini ko‘rishingiz kerak:

```
[gateway] listening on ws://0.0.0.0:3000 (PID xxx)
[discord] logged in to discord as xxx
```

## 5. Konfiguratsiya faylini yarating

To‘g‘ri konfiguratsiya yaratish uchun mashinaga SSH orqali kiring:

```bash
fly ssh console
```

Konfiguratsiya katalogi va faylini yarating:

```bash
mkdir -p /data
cat > /data/openclaw.json << 'EOF'
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-opus-4-6",
        "fallbacks": ["anthropic/claude-sonnet-4-5", "openai/gpt-4o"]
      },
      "maxConcurrent": 4
    },
    "list": [
      {
        "id": "main",
        "default": true
      }
    ]
  },
  "auth": {
    "profiles": {
      "anthropic:default": { "mode": "token", "provider": "anthropic" },
      "openai:default": { "mode": "token", "provider": "openai" }
    }
  },
  "bindings": [
    {
      "agentId": "main",
      "match": { "channel": "discord" }
    }
  ],
  "channels": {
    "discord": {
      "enabled": true,
      "groupPolicy": "allowlist",
      "guilds": {
        "YOUR_GUILD_ID": {
          "channels": { "general": { "allow": true } },
          "requireMention": false
        }
      }
    }
  },
  "gateway": {
    "mode": "local",
    "bind": "auto"
  },
  "meta": {
    "lastTouchedVersion": "2026.1.29"
  }
}
EOF
```

**Eslatma:** `OPENCLAW_STATE_DIR=/data` bo‘lsa, konfiguratsiya yo‘li `/data/openclaw.json` bo‘ladi.

**Eslatma:** Discord tokeni quyidagilardan biridan olinishi mumkin:

- Muhit o‘zgaruvchisi: `DISCORD_BOT_TOKEN` (maxfiy ma’lumotlar uchun tavsiya etiladi)
- Konfiguratsiya fayli: `channels.discord.token`

Agar env var ishlatilsa, tokenni konfiguratsiyaga qo‘shish shart emas. Gateway `DISCORD_BOT_TOKEN` ni avtomatik o‘qiydi.

Qo‘llash uchun qayta ishga tushiring:

```bash
exit
fly machine restart <machine-id>
```

## 6. Gateway’ga kirish

### Boshqaruv UI

Brauzerda oching:

```bash
fly open
```

Yoki `https://my-openclaw.fly.dev/` ga tashrif buyuring

Autentifikatsiya uchun gateway tokeningizni (`OPENCLAW_GATEWAY_TOKEN` dan olinganini) kiriting.

### Loglar

```bash
fly logs              # Jonli loglar
fly logs --no-tail    # So‘nggi loglar
```

### SSH konsol

```bash
fly ssh console
```

## Nosozliklarni bartaraf etish

### "Ilova kutilgan manzilda tinglamayapti"

Gateway `0.0.0.0` o‘rniga `127.0.0.1` ga bog‘lanmoqda.

**Yechim:** `fly.toml` dagi jarayon buyruqingizga `--bind lan` qo‘shing.

### Health check’lar muvaffaqiyatsiz / ulanish rad etildi

Fly sozlangan port orqali gateway’ga yetib bora olmayapti.

**Yechim:** `internal_port` gateway portiga mos kelishiga ishonch hosil qiling (`--port 3000` yoki `OPENCLAW_GATEWAY_PORT=3000` ni sozlang).

### OOM / Xotira muammolari

Konteyner doimiy ravishda qayta ishga tushmoqda yoki o‘chirib yuborilmoqda. Belgilar: `SIGABRT`, `v8::internal::Runtime_AllocateInYoungGeneration` yoki jim qayta ishga tushishlar.

**Yechim:** `fly.toml` da xotirani oshiring:

```toml
[[vm]]
  memory = "2048mb"
```

Yoki mavjud mashinani yangilang:

```bash
fly machine update <machine-id> --vm-memory 2048 -y
```

**Eslatma:** 512MB juda kichik. 1GB ishlashi mumkin, lekin yuklama yoki batafsil loglashda OOM bo‘lishi mumkin. **2GB tavsiya etiladi.**

### Gateway Lock muammolari

Gateway "already running" xatolari bilan ishga tushishni rad etadi.

Bu konteyner qayta ishga tushganda, lekin PID lock fayli volumeda qolib ketganda sodir bo‘ladi.

**Yechim:** Lock faylini o‘chiring:

```bash
fly ssh console --command "rm -f /data/gateway.*.lock"
fly machine restart <machine-id>
```

1. Lock fayl `/data/gateway.*.lock` da joylashgan (pastki katalogda emas).

### 2. Konfiguratsiya o‘qilmayapti

3. Agar `--allow-unconfigured` ishlatilsa, gateway minimal konfiguratsiyani yaratadi. 4. `/data/openclaw.json` dagi maxsus konfiguratsiyangiz qayta ishga tushirilganda o‘qilishi kerak.

5. Konfiguratsiya mavjudligini tekshiring:

```bash
6. fly ssh console --command "cat /data/openclaw.json"
```

### 7. SSH orqali konfiguratsiya yozish

8. `fly ssh console -C` buyrug‘i shell redirection’ni qo‘llab-quvvatlamaydi. 9. Konfiguratsiya faylini yozish uchun:

```bash
10. # echo + tee dan foydalaning (lokaldan remote’ga pipe orqali)
echo '{"your":"config"}' | fly ssh console -C "tee /data/openclaw.json"

# Yoki sftp dan foydalaning
fly sftp shell
> put /local/path/config.json /data/openclaw.json
```

11. **Eslatma:** agar fayl allaqachon mavjud bo‘lsa, `fly sftp` ishlamay qolishi mumkin. 12. Avval o‘chiring:

```bash
13. fly ssh console --command "rm /data/openclaw.json"
```

### 14. Holat saqlanmayapti

15. Agar qayta ishga tushirgandan keyin credential yoki sessiyalar yo‘qolsa, state katalogi konteyner fayl tizimiga yozilmoqda.

16. **Tuzatish:** `fly.toml` da `OPENCLAW_STATE_DIR=/data` o‘rnatilganiga ishonch hosil qiling va qayta deploy qiling.

## 17. Yangilanishlar

```bash
18. # So‘nggi o‘zgarishlarni olish
git pull

# Qayta deploy
fly deploy

# Holatni tekshirish
fly status
fly logs
```

### 19. Machine buyrug‘ini yangilash

20. To‘liq redeploy qilmasdan ishga tushirish buyrug‘ini o‘zgartirish kerak bo‘lsa:

```bash
21. # Machine ID ni olish
fly machines list

# Buyruqni yangilash
fly machine update <machine-id> --command "node dist/index.js gateway --port 3000 --bind lan" -y

# Yoki xotirani oshirish bilan
fly machine update <machine-id> --vm-memory 2048 --command "node dist/index.js gateway --port 3000 --bind lan" -y
```

22. **Eslatma:** `fly deploy` dan keyin machine buyrug‘i `fly.toml` dagi holatiga qaytishi mumkin. 23. Agar qo‘lda o‘zgarishlar qilgan bo‘lsangiz, deploy’dan keyin ularni qayta qo‘llang.

## 24. Xususiy deploy (mustahkamlangan)

25. Odatiy holatda Fly umumiy IP manzillar ajratadi, bu gateway’ni `https://your-app.fly.dev` orqali ochiq qiladi. 26. Bu qulay, ammo deploy internet skanerlari (Shodan, Censys va boshqalar) uchun ko‘rinadigan bo‘lib qoladi.

27. **Ommaviy ochiqliksiz** mustahkamlangan deploy uchun private template’dan foydalaning.

### 28. Qachon private deploy’dan foydalanish kerak

- 29. Siz faqat **chiqish** chaqiruvlari/xabarlarini yuborasiz (kiruvchi webhook’lar yo‘q)
- 30. Har qanday webhook callback’lar uchun **ngrok yoki Tailscale** tunnellaridan foydalanasiz
- 31. Gateway’ga brauzer orqali emas, **SSH, proxy yoki WireGuard** orqali kirasiz
- 32. Deploy’ni **internet skanerlaridan yashirishni** xohlaysiz

### 33. O‘rnatish

34. Standart konfiguratsiya o‘rniga `fly.private.toml` dan foydalaning:

```bash
35. # Private konfiguratsiya bilan deploy
fly deploy -c fly.private.toml
```

36. Yoki mavjud deploy’ni o‘zgartiring:

```bash
37. # Joriy IP’larni ro‘yxatlash
fly ips list -a my-openclaw

# Ommaviy IP’larni bo‘shatish
fly ips release <public-ipv4> -a my-openclaw
fly ips release <public-ipv6> -a my-openclaw

# Kelajakdagi deploy’lar ommaviy IP qayta ajratmasligi uchun private konfiguratsiyaga o‘ting
# ([http_service] ni olib tashlang yoki private template bilan deploy qiling)
fly deploy -c fly.private.toml

# Faqat private IPv6 ajratish
fly ips allocate-v6 --private -a my-openclaw
```

38. Shundan so‘ng, `fly ips list` faqat `private` turdagi IP’ni ko‘rsatishi kerak:

```
39. VERSION  IP                   TYPE             REGION
v6       fdaa:x:x:x:x::x      private          global
```

### 40. Private deploy’ga kirish

41. Ommaviy URL bo‘lmagani uchun, quyidagi usullardan birini ishlating:

42. **Variant 1: Lokal proxy (eng sodda)**

```bash
43. # Lokal 3000-portni ilovaga yo‘naltirish
fly proxy 3000:3000 -a my-openclaw

# So‘ng brauzerda http://localhost:3000 ni oching
```

44. **Variant 2: WireGuard VPN**

```bash
45. # WireGuard konfiguratsiyasini yaratish (bir martalik)
fly wireguard create

# WireGuard klientiga import qiling, so‘ng ichki IPv6 orqali kiring
# Misol: http://[fdaa:x:x:x:x::x]:3000
```

46. **Variant 3: Faqat SSH**

```bash
47. fly ssh console -a my-openclaw
```

### 48. Private deploy’da webhook’lar

49. Agar webhook callback’lari (Twilio, Telnyx va boshqalar) kerak bo‘lsa 50. ommaviy ochiqliksiz:

1. **ngrok tunnel** - Run ngrok inside the container or as a sidecar
2. **Tailscale Funnel** - Expose specific paths via Tailscale
3. **Outbound-only** - Some providers (Twilio) work fine for outbound calls without webhooks

Example voice-call config with ngrok:

```json
{
  "plugins": {
    "entries": {
      "voice-call": {
        "enabled": true,
        "config": {
          "provider": "twilio",
          "tunnel": { "provider": "ngrok" },
          "webhookSecurity": {
            "allowedHosts": ["example.ngrok.app"]
          }
        }
      }
    }
  }
}
```

The ngrok tunnel runs inside the container and provides a public webhook URL without exposing the Fly app itself. Set `webhookSecurity.allowedHosts` to the public tunnel hostname so forwarded host headers are accepted.

### Security benefits

| Aspect            | Public       | Private    |
| ----------------- | ------------ | ---------- |
| Internet scanners | Discoverable | Hidden     |
| Direct attacks    | Possible     | Blocked    |
| Control UI access | Browser      | Proxy/VPN  |
| Webhook delivery  | Direct       | Via tunnel |

## Notes

- Fly.io uses **x86 architecture** (not ARM)
- The Dockerfile is compatible with both architectures
- For WhatsApp/Telegram onboarding, use `fly ssh console`
- Persistent data lives on the volume at `/data`
- Signal requires Java + signal-cli; use a custom image and keep memory at 2GB+.

## Cost

With the recommended config (`shared-cpu-2x`, 2GB RAM):

- ~$10-15/month depending on usage
- Free tier includes some allowance

See [Fly.io pricing](https://fly.io/docs/about/pricing/) for details.
