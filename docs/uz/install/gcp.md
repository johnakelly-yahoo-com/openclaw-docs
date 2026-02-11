---
summary: "Run OpenClaw Gateway 24/7 on a GCP Compute Engine VM (Docker) with durable state"
read_when:
  - You want OpenClaw running 24/7 on GCP
  - You want a production-grade, always-on Gateway on your own VM
  - You want full control over persistence, binaries, and restart behavior
title: "GCP"
---

# OpenClaw on GCP Compute Engine (Docker, Production VPS Guide)

## Goal

Run a persistent OpenClaw Gateway on a GCP Compute Engine VM using Docker, with durable state, baked-in binaries, and safe restart behavior.

If you want "OpenClaw 24/7 for ~$5-12/mo", this is a reliable setup on Google Cloud.
Pricing varies by machine type and region; pick the smallest VM that fits your workload and scale up if you hit OOMs.

## What are we doing (simple terms)?

- Create a GCP project and enable billing
- Create a Compute Engine VM
- Install Docker (isolated app runtime)
- Start the OpenClaw Gateway in Docker
- Persist `~/.openclaw` + `~/.openclaw/workspace` on the host (survives restarts/rebuilds)
- Access the Control UI from your laptop via an SSH tunnel

The Gateway can be accessed via:

- SSH port forwarding from your laptop
- Direct port exposure if you manage firewalling and tokens yourself

This guide uses Debian on GCP Compute Engine.
Ubuntu also works; map packages accordingly.
For the generic Docker flow, see [Docker](/install/docker).

---

## Quick path (experienced operators)

1. Create GCP project + enable Compute Engine API
2. Create Compute Engine VM (e2-small, Debian 12, 20GB)
3. SSH into the VM
4. Install Docker
5. Clone OpenClaw repository
6. Create persistent host directories
7. Configure `.env` and `docker-compose.yml`
8. Bake required binaries, build, and launch

---

## What you need

- GCP account (free tier eligible for e2-micro)
- gcloud CLI installed (or use Cloud Console)
- SSH access from your laptop
- Basic comfort with SSH + copy/paste
- ~20-30 minutes
- Docker and Docker Compose
- Model autentifikatsiya ma’lumotlari
- Optional provider credentials
  - WhatsApp QR
  - Telegram bot token
  - Gmail OAuth

---

## 1. Install gcloud CLI (or use Console)

**Option A: gcloud CLI** (recommended for automation)

Install from [https://cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)

Initialize and authenticate:

```bash
gcloud init
gcloud auth login
```

**Option B: Cloud Console**

All steps can be done via the web UI at [https://console.cloud.google.com](https://console.cloud.google.com)

---

## 2. Create a GCP project

**CLI:**

```bash
gcloud projects create my-openclaw-project --name="OpenClaw Gateway"
gcloud config set project my-openclaw-project
```

Enable billing at [https://console.cloud.google.com/billing](https://console.cloud.google.com/billing) (required for Compute Engine).

Enable the Compute Engine API:

```bash
gcloud services enable compute.googleapis.com
```

**Console:**

1. Go to IAM & Admin > Create Project
2. Name it and create
3. Enable billing for the project
4. Navigate to APIs & Services > Enable APIs > search "Compute Engine API" > Enable

---

## 3. Create the VM

**Machine types:**

| Type     | Specs                                             | Narx                    | Eslatmalar                         |
| -------- | ------------------------------------------------- | ----------------------- | ---------------------------------- |
| e2-small | 2 vCPU, 2GB RAM                                   | ~$12/oy | Tavsiya etilgan                    |
| e2-micro | 2 vCPU (bo‘lishilgan), 1GB RAM | Bepul qatlamga mos      | Yuklama ostida OOM bo‘lishi mumkin |

**CLI:**

```bash
gcloud compute instances create openclaw-gateway \
  --zone=us-central1-a \
  --machine-type=e2-small \
  --boot-disk-size=20GB \
  --image-family=debian-12 \
  --image-project=debian-cloud
```

**Konsol:**

1. Compute Engine > VM instances > Create instance bo‘limiga o‘ting
2. Nomi: `openclaw-gateway`
3. Mintaqa: `us-central1`, Zona: `us-central1-a`
4. Mashina turi: `e2-small`
5. Yuklash diski: Debian 12, 20GB
6. Yaratish

---

## 4. VM ga SSH orqali kiring

**CLI:**

```bash
gcloud compute ssh openclaw-gateway --zone=us-central1-a
```

**Konsol:**

Compute Engine boshqaruv panelida VM yonidagi "SSH" tugmasini bosing.

Eslatma: VM yaratilgandan so‘ng SSH kalitlari tarqalishi 1–2 daqiqa vaqt olishi mumkin. Agar ulanish rad etilsa, kuting va qayta urinib ko‘ring.

---

## 5. Docker’ni o‘rnating (VM’da)

```bash
sudo apt-get update
sudo apt-get install -y git curl ca-certificates
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
```

Guruh o‘zgarishi kuchga kirishi uchun tizimdan chiqib qayta kiring:

```bash
exit
```

So‘ng yana SSH orqali kiring:

```bash
gcloud compute ssh openclaw-gateway --zone=us-central1-a
```

Tekshirish:

```bash
docker --version
docker compose version
```

---

## 6. OpenClaw repozitoriyasini klonlash

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
```

Ushbu qo‘llanma binarlarning saqlanib qolishini kafolatlash uchun maxsus image qurishingizni nazarda tutadi.

---

## 7. Doimiy host kataloglarini yarating

Docker konteynerlari vaqtinchalik (ephemeral).
Uzoq muddatli barcha holat host’da saqlanishi kerak.

```bash
mkdir -p ~/.openclaw
mkdir -p ~/.openclaw/workspace
```

---

## 8. Muhit o‘zgaruvchilarini sozlash

Repozitoriya ildizida `.env` yarating.

```bash
OPENCLAW_IMAGE=openclaw:latest
OPENCLAW_GATEWAY_TOKEN=change-me-now
OPENCLAW_GATEWAY_BIND=lan
OPENCLAW_GATEWAY_PORT=18789

OPENCLAW_CONFIG_DIR=/home/$USER/.openclaw
OPENCLAW_WORKSPACE_DIR=/home/$USER/.openclaw/workspace

GOG_KEYRING_PASSWORD=change-me-now
XDG_CONFIG_HOME=/home/node/.openclaw
```

Kuchli maxfiy kalitlar yarating:

```bash
openssl rand -hex 32
```

**Ushbu faylni commit qilmang.**

---

## 9. Docker Compose konfiguratsiyasi

`docker-compose.yml` ni yarating yoki yangilang.

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
      # Tavsiya etiladi: Gateway’ni VM’da faqat loopback’da qoldiring; SSH tunneli orqali kiring.
      # Uni ommaviy tarzda ochish uchun `127.0.0.1:` prefiksini olib tashlang va firewall’ni moslang.
      - "127.0.0.1:${OPENCLAW_GATEWAY_PORT}:18789"

      # Ixtiyoriy: faqat iOS/Android tugunlarini ushbu VM ga ulab, Canvas host kerak bo‘lsa.
      # Agar buni ommaviy ochsangiz, /gateway/security ni o‘qing va firewall’ni moslang.
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
      ]
```

---

## 10. Kerakli binarlarni imijga qoʻshib pishiring (muhim)

Ishlayotgan konteyner ichiga binarlarni oʻrnatish — bu tuzoq.
Ishga tushirish vaqtida oʻrnatilgan har qanday narsa qayta ishga tushirilganda yoʻqoladi.

Skill’lar talab qiladigan barcha tashqi binarlar imijni qurish vaqtida oʻrnatilishi shart.

Quyidagi misollar faqat uchta keng tarqalgan binarni koʻrsatadi:

- `gog` — Gmail’ga kirish uchun
- `goplaces` — Google Places uchun
- `wacli` — WhatsApp uchun

Bular misollar, toʻliq roʻyxat emas.
Xuddi shu andoza yordamida istalgancha binarlarni oʻrnatishingiz mumkin.

Agar keyinroq qoʻshimcha binarlarga bogʻliq yangi skill’lar qoʻshsangiz, quyidagilarni bajarishingiz kerak:

1. Dockerfile’ni yangilang
2. Imijni qayta yarating
3. Konteynerlarni qayta ishga tushiring

**Misol Dockerfile**

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

## 11. Qurish va ishga tushirish

```bash
docker compose build
docker compose up -d openclaw-gateway
```

Binarlarni tekshiring:

```bash
docker compose exec openclaw-gateway which gog
docker compose exec openclaw-gateway which goplaces
docker compose exec openclaw-gateway which wacli
```

Kutilgan chiqish:

```
/usr/local/bin/gog
/usr/local/bin/goplaces
/usr/local/bin/wacli
```

---

## 12. Gateway’ni tekshirish

```bash
docker compose logs -f openclaw-gateway
```

Muvaffaqiyat:

```
[gateway] listening on ws://0.0.0.0:18789
```

---

## 13. Noutbukingizdan kirish

Gateway portini yoʻnaltirish uchun SSH tunnel yarating:

```bash
gcloud compute ssh openclaw-gateway --zone=us-central1-a -- -L 18789:127.0.0.1:18789
```

Brauzeringizda oching:

`http://127.0.0.1:18789/`

Gateway tokeningizni joylashtiring.

---

## Nima qayerda saqlanadi (asosiy manba)

OpenClaw Docker’da ishlaydi, ammo Docker asosiy manba emas.
Barcha uzoq muddatli holat qayta ishga tushirishlar, qayta qurishlar va qayta yuklashlardan omon qolishi kerak.

| Komponent                         | Joylashuv                                       | Saqlanish mexanizmi     | Izohlar                                      |
| --------------------------------- | ----------------------------------------------- | ----------------------- | -------------------------------------------- |
| Gateway konfiguratsiyasi          | `/home/node/.openclaw/`                         | Host volume mount       | `openclaw.json`, tokenlarni o‘z ichiga oladi |
| Model autentifikatsiya profillari | `/home/node/.openclaw/`                         | Host volume mount       | OAuth tokenlari, API kalitlari               |
| Skill konfiguratsiyalari          | `/home/node/.openclaw/skills/`                  | Host volume mount       | Ko‘nikma darajasi holati                     |
| Agent ish maydoni                 | /home/node/.openclaw/workspace/ | Xost hajmini ulash      | Kod va agent artefaktlari                    |
| WhatsApp sessiyasi                | /home/node/.openclaw/           | Xost hajmini ulash      | QR orqali kirishni saqlaydi                  |
| Gmail kalitlar ombori             | /home/node/.openclaw/           | Xost hajmi + parol      | `GOG_KEYRING_PASSWORD` talab qilinadi        |
| Tashqi binar fayllar              | /usr/local/bin/                                 | Docker imiji            | Build vaqtida joylashtirilishi shart         |
| Node ish vaqti                    | Konteyner fayl tizimi                           | Docker imiji            | Har bir imij buildida qayta yig‘iladi        |
| OS paketlari                      | Konteyner fayl tizimi                           | Docker imiji            | Ish vaqtida o‘rnatmang                       |
| Docker konteyneri                 | Vaqtinchalik                                    | Qayta ishga tushiriladi | O‘chirish xavfsiz                            |

---

## Yangilanishlar

VM’da OpenClaw’ni yangilash uchun:

```bash
cd ~/openclaw
git pull
docker compose build
docker compose up -d
```

---

## Nosozliklarni bartaraf etish

**SSH ulanishi rad etildi**

VM yaratilgandan so‘ng SSH kalitlari tarqalishi 1–2 daqiqa vaqt olishi mumkin. Kuting va qayta urinib ko‘ring.

**OS Login muammolari**

OS Login profilingizni tekshiring:

```bash
gcloud compute os-login describe-profile
```

Hisobingizda zarur IAM ruxsatlari (Compute OS Login yoki Compute OS Admin Login) mavjudligiga ishonch hosil qiling.

**Xotira yetishmasligi (OOM)**

Agar e2-micro’dan foydalanib OOM muammosiga duch kelsangiz, e2-small yoki e2-medium’ga yangilang:

```bash
# Avval VM’ni to‘xtating
gcloud compute instances stop openclaw-gateway --zone=us-central1-a

# Mashina turini o‘zgartiring
gcloud compute instances set-machine-type openclaw-gateway \
  --zone=us-central1-a \
  --machine-type=e2-small

# VM’ni ishga tushiring
gcloud compute instances start openclaw-gateway --zone=us-central1-a
```

---

## Xizmat hisoblari (xavfsizlik bo‘yicha eng yaxshi amaliyot)

Shaxsiy foydalanish uchun standart foydalanuvchi hisobingiz yetarli.

Avtomatlashtirish yoki CI/CD quvurlari uchun minimal ruxsatlarga ega alohida xizmat hisobini yarating:

1. Xizmat hisobini yarating:

   ```bash
   gcloud iam service-accounts create openclaw-deploy \
     --display-name="OpenClaw Deployment"
   ```

2. Compute Instance Admin rolini (yoki torroq maxsus rolni) bering:

   ```bash
   gcloud projects add-iam-policy-binding my-openclaw-project \
     --member="serviceAccount:openclaw-deploy@my-openclaw-project.iam.gserviceaccount.com" \
     --role="roles/compute.instanceAdmin.v1"
   ```

Avtomatlashtirish uchun Owner rolidan foydalanishdan saqlaning. Eng kam imtiyozlar tamoyilidan foydalaning.

IAM rollari tafsilotlari uchun [https://cloud.google.com/iam/docs/understanding-roles](https://cloud.google.com/iam/docs/understanding-roles) sahifasiga qarang.

---

## Keyingi qadamlar

- Xabar almashish kanallarini sozlang: [Channels](/channels)
- Mahalliy qurilmalarni tugunlar sifatida juftlang: [Nodes](/nodes)
- Gateway-ni sozlang: [Gateway configuration](/gateway/configuration)
