---
summary: "OpenClaw Gateway-ni 24/7 arzon Hetzner VPS’da (Docker) mustahkam holat va ichiga kiritilgan binar fayllar bilan ishga tushiring"
read_when:
  - Siz OpenClaw’ning bulut VPS’da (noutbukingizda emas) 24/7 ishlashini xohlaysiz
  - Siz o‘zingizning VPS’ingizda ishlab chiqarish darajasidagi, doimiy ishlovchi Gateway’ni xohlaysiz
  - Siz saqlanish (persistence), binar fayllar va qayta ishga tushirish xatti-harakatlari ustidan to‘liq nazoratni xohlaysiz
  - Siz OpenClaw’ni Hetzner yoki shunga o‘xshash provayderda Docker’da ishga tushiryapsiz
title: "Hetzner"
---

# Hetzner’da OpenClaw (Docker, Production VPS Guide)

## Maqsad

Docker’dan foydalangan holda Hetzner VPS’da mustahkam holat, ichiga kiritilgan binar fayllar va xavfsiz qayta ishga tushirish xatti-harakati bilan doimiy OpenClaw Gateway’ni ishga tushirish.

Agar siz “~$5 ga OpenClaw 24/7” ni xohlasangiz, bu eng sodda va ishonchli sozlama.
Hetzner narxlari o‘zgaradi; eng kichik Debian/Ubuntu VPS’ni tanlang va OOM’larga duch kelsangiz, kattalashtiring.

## Biz nima qilyapmiz (oddiy qilib)?

- Kichik Linux serverini ijaraga olish (Hetzner VPS)
- Docker’ni o‘rnatish (izolyatsiyalangan ilova ish muhiti)
- OpenClaw Gateway’ni Docker’da ishga tushirish
- Xostda `~/.openclaw` + `~/.openclaw/workspace` ni saqlash (qayta ishga tushirish/qayta qurishlardan keyin ham saqlanadi)
- Noutbukingizdan SSH tunneli orqali Control UI’ga kirish

Gateway’ga quyidagicha kirish mumkin:

- Noutbukingizdan SSH port forwarding orqali
- Agar siz firewall va tokenlarni o‘zingiz boshqarsangiz, portlarni to‘g‘ridan-to‘g‘ri ochish orqali

Ushbu qo‘llanma Hetzner’da Ubuntu yoki Debian’ni nazarda tutadi.  
Agar siz boshqa Linux VPS’da bo‘lsangiz, paketlarni mos ravishda xaritalang.
Umumiy Docker jarayoni uchun [Docker](/install/docker) bo‘limiga qarang.

---

## Tezkor yo‘l (tajribali operatorlar uchun)

1. Hetzner VPS’ni tayyorlash
2. Docker’ni o‘rnatish
3. OpenClaw repozitoriyasini klonlash
4. Doimiy xost kataloglarini yaratish
5. `.env` va `docker-compose.yml` ni sozlash
6. Kerakli binar fayllarni image ichiga kiritish
7. `docker compose up -d`
8. Saqlanishni va Gateway’ga kirishni tekshirish

---

## Sizga kerak bo‘ladi

- Root kirish huquqiga ega Hetzner VPS
- Noutbukingizdan SSH orqali kirish
- SSH va copy/paste bilan asosiy darajada ishlay olish
- ~20 daqiqa
- Docker va Docker Compose
- Model autentifikatsiya ma’lumotlari
- Ixtiyoriy provayder autentifikatsiya ma’lumotlari
  - WhatsApp QR
  - Telegram bot tokeni
  - Gmail OAuth

---

## 1. Provision the VPS

Hetzner’da Ubuntu yoki Debian VPS yarating.

Connect as root:

```bash
ssh root@YOUR_VPS_IP
```

This guide assumes the VPS is stateful.
Do not treat it as disposable infrastructure.

---

## 2. Docker’ni o‘rnating (VPS’da)

```bash
apt-get update
apt-get install -y git curl ca-certificates
curl -fsSL https://get.docker.com | sh
```

Tekshirish:

```bash
docker --version
docker compose version
```

---

## 3. Clone the OpenClaw repository

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
```

This guide assumes you will build a custom image to guarantee binary persistence.

---

## 4. Doimiy xost kataloglarini yarating

Docker konteynerlari vaqtinchalik (ephemeral).
All long-lived state must live on the host.

```bash
mkdir -p /root/.openclaw/workspace

# Set ownership to the container user (uid 1000):
chown -R 1000:1000 /root/.openclaw
```

---

## 5. Configure environment variables

Create `.env` in the repository root.

```bash
OPENCLAW_IMAGE=openclaw:latest
OPENCLAW_GATEWAY_TOKEN=change-me-now
OPENCLAW_GATEWAY_BIND=lan
OPENCLAW_GATEWAY_PORT=18789

OPENCLAW_CONFIG_DIR=/root/.openclaw
OPENCLAW_WORKSPACE_DIR=/root/.openclaw/workspace

GOG_KEYRING_PASSWORD=change-me-now
XDG_CONFIG_HOME=/home/node/.openclaw
```

Generate strong secrets:

```bash
openssl rand -hex 32
```

**Do not commit this file.**

---

## 6. Docker Compose configuration

Create or update `docker-compose.yml`.

```yaml
services:
  openclaw-gateway:
    image: ${OPENCLAW_IMAGE}
    build: .
    restart: unless-stopped
    env_file:
      - .env
    environment:
      - HOME=/home/node
      - NODE_ENV=production
      - TERM=xterm-256color
      - OPENCLAW_GATEWAY_BIND=${OPENCLAW_GATEWAY_BIND}
      - OPENCLAW_GATEWAY_PORT=${OPENCLAW_GATEWAY_PORT}
      - OPENCLAW_GATEWAY_TOKEN=${OPENCLAW_GATEWAY_TOKEN}
      - GOG_KEYRING_PASSWORD=${GOG_KEYRING_PASSWORD}
      - XDG_CONFIG_HOME=${XDG_CONFIG_HOME}
      - PATH=/home/linuxbrew/.linuxbrew/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
    volumes:
      - ${OPENCLAW_CONFIG_DIR}:/home/node/.openclaw
      - ${OPENCLAW_WORKSPACE_DIR}:/home/node/.openclaw/workspace
    ports:
      # Recommended: keep the Gateway loopback-only on the VPS; access via SSH tunnel.
      # To expose it publicly, remove the `127.0.0.1:` prefix and firewall accordingly.
      - "127.0.0.1:${OPENCLAW_GATEWAY_PORT}:18789"

      # Optional: only if you run iOS/Android nodes against this VPS and need Canvas host.
      # If you expose this publicly, read /gateway/security and firewall accordingly.
      # - "18793:18793"
    command:
      [
        "node",
        "dist/index.js",
        "gateway",
        "--bind",
        "${OPENCLAW_GATEWAY_BIND}",
        "--port",
        "${OPENCLAW_GATEWAY_PORT}",
        "--allow-unconfigured",
      ]
```

`--allow-unconfigured` faqat boshlang‘ich qulaylik uchun mo‘ljallangan, u to‘g‘ri gateway konfiguratsiyasining o‘rnini bosa olmaydi. Baribir autentifikatsiyani (`gateway.auth.token` yoki parol) sozlang va joylashtirish uchun xavfsiz bind sozlamalaridan foydalaning.

---

## 7. Bake required binaries into the image (critical)

Installing binaries inside a running container is a trap.
Anything installed at runtime will be lost on restart.

Ko‘nikmalar (skills) uchun zarur bo‘lgan barcha tashqi binar fayllar image build vaqtida o‘rnatilishi kerak.

Quyidagi misollar faqat uchta keng tarqalgan binar faylni ko‘rsatadi:

- `gog` for Gmail access
- `goplaces` for Google Places
- `wacli` for WhatsApp

These are examples, not a complete list.
You may install as many binaries as needed using the same pattern.

If you add new skills later that depend on additional binaries, you must:

1. Update the Dockerfile
2. Rebuild the image
3. Restart the containers

**Example Dockerfile**

```dockerfile
FROM node:22-bookworm

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

# Example binary 1: Gmail CLI
RUN curl -L https://github.com/steipete/gog/releases/latest/download/gog_Linux_x86_64.tar.gz \
  | tar -xz -C /usr/local/bin && chmod +x /usr/local/bin/gog

# Example binary 2: Google Places CLI
RUN curl -L https://github.com/steipete/goplaces/releases/latest/download/goplaces_Linux_x86_64.tar.gz \
  | tar -xz -C /usr/local/bin && chmod +x /usr/local/bin/goplaces

# Example binary 3: WhatsApp CLI
RUN curl -L https://github.com/steipete/wacli/releases/latest/download/wacli_Linux_x86_64.tar.gz \
  | tar -xz -C /usr/local/bin && chmod +x /usr/local/bin/wacli

# Add more binaries below using the same pattern

WORKDIR /app
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml .npmrc ./
COPY ui/package.json ./ui/package.json
COPY scripts ./scripts

RUN corepack enable
RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm build
RUN pnpm ui:install
RUN pnpm ui:build

ENV NODE_ENV=production

CMD ["node","dist/index.js"]
```

---

## 8. Build and launch

```bash
docker compose build
docker compose up -d openclaw-gateway
```

Verify binaries:

```bash
docker compose exec openclaw-gateway which gog
docker compose exec openclaw-gateway which goplaces
docker compose exec openclaw-gateway which wacli
```

Expected output:

```
/usr/local/bin/gog
/usr/local/bin/goplaces
/usr/local/bin/wacli
```

---

## 9. Verify Gateway

```bash
docker compose logs -f openclaw-gateway
```

Success:

```
[gateway] listening on ws://0.0.0.0:18789
```

From your laptop:

```bash
ssh -N -L 18789:127.0.0.1:18789 root@YOUR_VPS_IP
```

Open:

`http://127.0.0.1:18789/`

Paste your gateway token.

---

## What persists where (source of truth)

OpenClaw runs in Docker, but Docker is not the source of truth.
All long-lived state must survive restarts, rebuilds, and reboots.

| Component           | Location                          | Persistence mechanism      | Notes                            |
| ------------------- | --------------------------------- | -------------------------- | -------------------------------- |
| Gateway config      | `/home/node/.openclaw/`           | Host volume mount          | Includes `openclaw.json`, tokens |
| Model auth profiles | `/home/node/.openclaw/`           | Host volume mount          | OAuth tokens, API keys           |
| Skill configs       | `/home/node/.openclaw/skills/`    | Host volume mount          | Skill-level state                |
| Agent workspace     | `/home/node/.openclaw/workspace/` | Host volume mount          | Code and agent artifacts         |
| WhatsApp session    | `/home/node/.openclaw/`           | Host volume mount          | Preserves QR login               |
| Gmail keyring       | `/home/node/.openclaw/`           | Host volume + password     | Requires `GOG_KEYRING_PASSWORD`  |
| External binaries   | `/usr/local/bin/`                 | Docker image               | Must be baked at build time      |
| Node runtime        | Konteyner fayl tizimi             | Docker image               | Rebuilt every image build        |
| OS packages         | Container filesystem              | Docker image               | Do not install at runtime        |
| Docker container    | Ephemeral                         | Qayta ishga tushiriladigan | Yo‘q qilish xavfsiz              |
