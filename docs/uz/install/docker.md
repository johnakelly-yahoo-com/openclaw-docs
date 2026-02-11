---
summary: "OpenClaw uchun ixtiyoriy Docker-ga asoslangan sozlash va onboarding"
read_when:
  - Mahalliy o‘rnatishlar o‘rniga konteynerlashtirilgan gateway xohlaysiz
  - Siz Docker oqimini tekshirmoqdasiz
title: "Docker"
---

# Docker (ixtiyoriy)

Docker **ixtiyoriy**. Uni faqat konteynerlashtirilgan gateway xohlasangiz yoki Docker oqimini tekshirmoqchi bo‘lsangiz foydalaning.

## Docker menga mosmi?

- **Ha**: siz izolyatsiyalangan, vaqtinchalik gateway muhiti xohlaysiz yoki OpenClaw’ni mahalliy o‘rnatishlarsiz xostda ishga tushirmoqchisiz.
- **Yo‘q**: siz o‘z kompyuteringizda ishlayapsiz va eng tezkor dev siklini xohlaysiz. Buning o‘rniga odatiy o‘rnatish oqimidan foydalaning.
- **Sandboxing eslatmasi**: agent sandboxingi ham Docker’dan foydalanadi, ammo butun gateway’ni Docker’da ishga tushirishni **talab qilmaydi**. Qarang: [Sandboxing](/gateway/sandboxing).

Ushbu qo‘llanma quyidagilarni qamrab oladi:

- Konteynerlashtirilgan Gateway (Docker’da to‘liq OpenClaw)
- Har sessiya uchun Agent Sandbox (xost gateway + Docker’da izolyatsiyalangan agent vositalari)

Sandboxing tafsilotlari: [Sandboxing](/gateway/sandboxing)

## Talablar

- Docker Desktop (yoki Docker Engine) + Docker Compose v2
- Tasvirlar + jurnallar uchun yetarli disk joyi

## Konteynerlangan Gateway (Docker Compose)

### Tezkor boshlash (tavsiya etiladi)

Repo ildizidan:

```bash
./docker-setup.sh
```

Ushbu skript:

- gateway tasvirini yaratadi
- onboarding ustasini ishga tushiradi
- ixtiyoriy provayder sozlash bo‘yicha maslahatlarni chiqaradi
- Docker Compose orqali gateway’ni ishga tushiradi
- gateway tokenini yaratadi va uni `.env` fayliga yozadi

Ixtiyoriy env o‘zgaruvchilar:

- `OPENCLAW_DOCKER_APT_PACKAGES` — build vaqtida qo‘shimcha apt paketlarni o‘rnatish
- `OPENCLAW_EXTRA_MOUNTS` — qo‘shimcha host bind mount’larni qo‘shish
- `OPENCLAW_HOME_VOLUME` — nomlangan volume’da `/home/node` ni saqlab qolish

Tugagach:

- Brauzeringizda `http://127.0.0.1:18789/` ni oching.
- Tokenni Control UI’ga joylang (Settings → token).
- URL yana kerakmi? `docker compose run --rm openclaw-cli dashboard --no-open` ni ishga tushiring.

U hostda konfiguratsiya/workspace yozadi:

- `~/.openclaw/`
- `~/.openclaw/workspace`

VPS’da ishlayapsizmi? [Hetzner (Docker VPS)](/install/hetzner) ga qarang.

### Qo‘lda oqim (compose)

```bash
docker build -t openclaw:local -f Dockerfile .
docker compose run --rm openclaw-cli onboard
docker compose up -d openclaw-gateway
```

Eslatma: `docker compose ...` ni repo ildizidan ishga tushiring. Agar siz
`OPENCLAW_EXTRA_MOUNTS` yoki `OPENCLAW_HOME_VOLUME` ni yoqqan bo‘lsangiz, sozlash skripti
`docker-compose.extra.yml` ni yozadi; boshqa joyda Compose ishga tushirganda uni qo‘shing:

```bash
docker compose -f docker-compose.yml -f docker-compose.extra.yml <command>
```

### Control UI tokeni + juftlash (Docker)

Agar “unauthorized” yoki “disconnected (1008): pairing required” ni ko‘rsangiz, yangi dashboard havolasini oling va brauzer qurilmasini tasdiqlang:

```bash
docker compose run --rm openclaw-cli dashboard --no-open
docker compose run --rm openclaw-cli devices list
docker compose run --rm openclaw-cli devices approve <requestId>
```

Batafsil: [Dashboard](/web/dashboard), [Devices](/cli/devices).

### Qo‘shimcha mount’lar (ixtiyoriy)

Agar qo‘shimcha host kataloglarini konteynerlarga mount qilmoqchi bo‘lsangiz, `docker-setup.sh` ni ishga tushirishdan oldin
`OPENCLAW_EXTRA_MOUNTS` ni o‘rnating. Bu vergul bilan ajratilgan Docker bind mount’lar ro‘yxatini qabul qiladi va
`docker-compose.extra.yml` ni yaratish orqali ularni ham `openclaw-gateway`, ham `openclaw-cli` ga qo‘llaydi.

Misol:

```bash
export OPENCLAW_EXTRA_MOUNTS="$HOME/.codex:/home/node/.codex:ro,$HOME/github:/home/node/github:rw"
./docker-setup.sh
```

Eslatmalar:

- macOS/Windows’da yo‘llar Docker Desktop bilan bo‘lishilgan bo‘lishi kerak.
- `OPENCLAW_EXTRA_MOUNTS` ni tahrirlasangiz, qo‘shimcha compose faylini qayta yaratish uchun
  `docker-setup.sh` ni yana ishga tushiring.
- `docker-compose.extra.yml` yaratiladi. Uni qo‘lda tahrirlamang.

### Butun konteyner home’ini saqlab qolish (ixtiyoriy)

Agar `/home/node` konteyner qayta yaratilganda saqlanib qolishini istasangiz, `OPENCLAW_HOME_VOLUME` orqali nomlangan volume o‘rnating. Bu Docker volume’ini yaratadi va uni
`/home/node` ga mount qiladi, shu bilan birga standart config/workspace bind mount’larini saqlab qoladi. Bu yerda nomlangan volume’dan foydalaning (bind path emas); bind mount’lar uchun
`OPENCLAW_EXTRA_MOUNTS` dan foydalaning.

Misol:

```bash
export OPENCLAW_HOME_VOLUME="openclaw_home"
./docker-setup.sh
```

You can combine this with extra mounts:

```bash
export OPENCLAW_HOME_VOLUME="openclaw_home"
export OPENCLAW_EXTRA_MOUNTS="$HOME/.codex:/home/node/.codex:ro,$HOME/github:/home/node/github:rw"
./docker-setup.sh
```

Notes:

- If you change `OPENCLAW_HOME_VOLUME`, rerun `docker-setup.sh` to regenerate the
  extra compose file.
- The named volume persists until removed with `docker volume rm <name>`.

### Install extra apt packages (optional)

If you need system packages inside the image (for example, build tools or media
libraries), set `OPENCLAW_DOCKER_APT_PACKAGES` before running `docker-setup.sh`.
This installs the packages during the image build, so they persist even if the
container is deleted.

Example:

```bash
export OPENCLAW_DOCKER_APT_PACKAGES="ffmpeg build-essential"
./docker-setup.sh
```

Notes:

- This accepts a space-separated list of apt package names.
- If you change `OPENCLAW_DOCKER_APT_PACKAGES`, rerun `docker-setup.sh` to rebuild
  the image.

### Power-user / full-featured container (opt-in)

The default Docker image is **security-first** and runs as the non-root `node`
user. This keeps the attack surface small, but it means:

- no system package installs at runtime
- no Homebrew by default
- no bundled Chromium/Playwright browsers

If you want a more full-featured container, use these opt-in knobs:

1. **Persist `/home/node`** so browser downloads and tool caches survive:

```bash
export OPENCLAW_HOME_VOLUME="openclaw_home"
./docker-setup.sh
```

2. **Bake system deps into the image** (repeatable + persistent):

```bash
export OPENCLAW_DOCKER_APT_PACKAGES="git curl jq"
./docker-setup.sh
```

3. **Install Playwright browsers without `npx`** (avoids npm override conflicts):

```bash
docker compose run --rm openclaw-cli \
  node /app/node_modules/playwright-core/cli.js install chromium
```

If you need Playwright to install system deps, rebuild the image with
`OPENCLAW_DOCKER_APT_PACKAGES` instead of using `--with-deps` at runtime.

4. **Persist Playwright browser downloads**:

- Set `PLAYWRIGHT_BROWSERS_PATH=/home/node/.cache/ms-playwright` in
  `docker-compose.yml`.
- Ensure `/home/node` persists via `OPENCLAW_HOME_VOLUME`, or mount
  `/home/node/.cache/ms-playwright` via `OPENCLAW_EXTRA_MOUNTS`.

### Permissions + EACCES

The image runs as `node` (uid 1000). If you see permission errors on
`/home/node/.openclaw`, make sure your host bind mounts are owned by uid 1000.

Example (Linux host):

```bash
sudo chown -R 1000:1000 /path/to/openclaw-config /path/to/openclaw-workspace
```

If you choose to run as root for convenience, you accept the security tradeoff.

### Faster rebuilds (recommended)

To speed up rebuilds, order your Dockerfile so dependency layers are cached.
This avoids re-running `pnpm install` unless lockfiles change:

```dockerfile
FROM node:22-bookworm

# Install Bun (required for build scripts)
RUN curl -fsSL https://bun.sh/install | bash
ENV PATH="/root/.bun/bin:${PATH}"

RUN corepack enable

WORKDIR /app

# Cache dependencies unless package metadata changes
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml .npmrc ./
COPY ui/package.json ./ui/package.json
COPY scripts ./scripts

RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm build
RUN pnpm ui:install
RUN pnpm ui:build

ENV NODE_ENV=production

CMD ["node","dist/index.js"]
```

### Channel setup (optional)

Use the CLI container to configure channels, then restart the gateway if needed.

WhatsApp (QR):

```bash
docker compose run --rm openclaw-cli channels login
```

Telegram (bot token):

```bash
docker compose run --rm openclaw-cli channels add --channel telegram --token "<token>"
```

Discord (bot token):

```bash
docker compose run --rm openclaw-cli channels add --channel discord --token "<token>"
```

Docs: [WhatsApp](/channels/whatsapp), [Telegram](/channels/telegram), [Discord](/channels/discord)

### OpenAI Codex OAuth (headless Docker)

If you pick OpenAI Codex OAuth in the wizard, it opens a browser URL and tries
to capture a callback on `http://127.0.0.1:1455/auth/callback`. In Docker or
headless setups that callback can show a browser error. Copy the full redirect
URL you land on and paste it back into the wizard to finish auth.

### Health check

```bash
docker compose exec openclaw-gateway node dist/index.js health --token "$OPENCLAW_GATEWAY_TOKEN"
```

### E2E smoke test (Docker)

```bash
scripts/e2e/onboard-docker.sh
```

### QR import smoke test (Docker)

```bash
pnpm test:docker:qr
```

### Notes

- Gateway bind defaults to `lan` for container use.
- Dockerfile CMD uses `--allow-unconfigured`; mounted config with `gateway.mode` not `local` will still start. Override CMD to enforce the guard.
- The gateway container is the source of truth for sessions (`~/.openclaw/agents/<agentId>/sessions/`).

## Agent Sandbox (host gateway + Docker tools)

Deep dive: [Sandboxing](/gateway/sandboxing)

### What it does

When `agents.defaults.sandbox` is enabled, **non-main sessions** run tools inside a Docker
container. The gateway stays on your host, but the tool execution is isolated:

- scope: `"agent"` by default (one container + workspace per agent)
- scope: `"session"` for per-session isolation
- per-scope workspace folder mounted at `/workspace`
- optional agent workspace access (`agents.defaults.sandbox.workspaceAccess`)
- allow/deny tool policy (deny wins)
- inbound media is copied into the active sandbox workspace (`media/inbound/*`) so tools can read it (with `workspaceAccess: "rw"`, this lands in the agent workspace)

Warning: `scope: "shared"` disables cross-session isolation. All sessions share
one container and one workspace.

### Per-agent sandbox profiles (multi-agent)

If you use multi-agent routing, each agent can override sandbox + tool settings:
`agents.list[].sandbox` and `agents.list[].tools` (plus `agents.list[].tools.sandbox.tools`). This lets you run
mixed access levels in one gateway:

- Full access (personal agent)
- Read-only tools + read-only workspace (family/work agent)
- No filesystem/shell tools (public agent)

See [Multi-Agent Sandbox & Tools](/tools/multi-agent-sandbox-tools) for examples,
precedence, and troubleshooting.

### Default behavior

- Image: `openclaw-sandbox:bookworm-slim`
- One container per agent
- Agent workspace access: `workspaceAccess: "none"` (default) uses `~/.openclaw/sandboxes`
  - `"ro"` keeps the sandbox workspace at `/workspace` and mounts the agent workspace read-only at `/agent` (disables `write`/`edit`/`apply_patch`)
  - `"rw"` mounts the agent workspace read/write at `/workspace`
- Auto-prune: idle > 24h OR age > 7d
- Network: `none` by default (explicitly opt-in if you need egress)
- Default allow: `exec`, `process`, `read`, `write`, `edit`, `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `session_status`
- Default deny: `browser`, `canvas`, `nodes`, `cron`, `discord`, `gateway`

### Enable sandboxing

If you plan to install packages in `setupCommand`, note:

- Default `docker.network` is `"none"` (no egress).
- `readOnlyRoot: true` blocks package installs.
- `user` must be root for `apt-get` (omit `user` or set `user: "0:0"`).
  OpenClaw auto-recreates containers when `setupCommand` (or docker config) changes
  unless the container was **recently used** (within ~5 minutes). Issiq konteynerlar
  aniq `openclaw sandbox recreate ...` buyrug‘i bilan ogohlantirishni log qiling.

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main", // off | non-main | all
        scope: "agent", // session | agent | shared (agent is default)
        workspaceAccess: "none", // none | ro | rw
        workspaceRoot: "~/.openclaw/sandboxes",
        docker: {
          image: "openclaw-sandbox:bookworm-slim",
          workdir: "/workspace",
          readOnlyRoot: true,
          tmpfs: ["/tmp", "/var/tmp", "/run"],
          network: "none",
          user: "1000:1000",
          capDrop: ["ALL"],
          env: { LANG: "C.UTF-8" },
          setupCommand: "apt-get update && apt-get install -y git curl jq",
          pidsLimit: 256,
          memory: "1g",
          memorySwap: "2g",
          cpus: 1,
          ulimits: {
            nofile: { soft: 1024, hard: 2048 },
            nproc: 256,
          },
          seccompProfile: "/path/to/seccomp.json",
          apparmorProfile: "openclaw-sandbox",
          dns: ["1.1.1.1", "8.8.8.8"],
          extraHosts: ["internal.service:10.0.0.5"],
        },
        prune: {
          idleHours: 24, // 0 disables idle pruning
          maxAgeDays: 7, // 0 disables max-age pruning
        },
      },
    },
  },
  tools: {
    sandbox: {
      tools: {
        allow: [
          "exec",
          "process",
          "read",
          "write",
          "edit",
          "sessions_list",
          "sessions_history",
          "sessions_send",
          "sessions_spawn",
          "session_status",
        ],
        deny: ["browser", "canvas", "nodes", "cron", "discord", "gateway"],
      },
    },
  },
}
```

Qattiqlashtirish sozlamalari `agents.defaults.sandbox.docker` ostida joylashgan:
`network`, `user`, `pidsLimit`, `memory`, `memorySwap`, `cpus`, `ulimits`,
`seccompProfile`, `apparmorProfile`, `dns`, `extraHosts`.

Ko‘p-agentli: har bir agent uchun `agents.list[].sandbox.{docker,browser,prune}.*` orqali `agents.defaults.sandbox.{docker,browser,prune}.*` ni bekor qiling
(`agents.defaults.sandbox.scope` / `agents.list[].sandbox.scope` "shared" bo‘lsa, e’tiborga olinmaydi).

### Standart sandbox image’ni yig‘ing

```bash
scripts/sandbox-setup.sh
```

Bu `Dockerfile.sandbox` dan foydalanib `openclaw-sandbox:bookworm-slim` ni yig‘adi.

### Sandbox umumiy image (ixtiyoriy)

Agar umumiy build asboblari (Node, Go, Rust va h.k.) bilan sandbox image xohlasangiz, umumiy image’ni yig‘ing:

```bash
scripts/sandbox-common-setup.sh
```

Bu `openclaw-sandbox-common:bookworm-slim` ni yig‘adi. Uni ishlatish uchun:

```json5
{
  agents: {
    defaults: {
      sandbox: { docker: { image: "openclaw-sandbox-common:bookworm-slim" } },
    },
  },
}
```

### Sandbox brauzer image’i

Sandbox ichida brauzer vositasini ishga tushirish uchun brauzer image’ni yig‘ing:

```bash
scripts/sandbox-browser-setup.sh
```

Bu `Dockerfile.sandbox-browser` dan foydalanib `openclaw-sandbox-browser:bookworm-slim` ni yig‘adi. Konteyner CDP yoqilgan Chromium’ni va
ixtiyoriy noVNC kuzatuvchini (Xvfb orqali headful) ishga tushiradi.

Eslatmalar:

- Headful (Xvfb) headless’ga nisbatan bot bloklashni kamaytiradi.
- `agents.defaults.sandbox.browser.headless=true` qilib, headless’ni ham ishlatish mumkin.
- To‘liq ish stoli muhiti (GNOME) kerak emas; Xvfb displeyni ta’minlaydi.

Konfiguratsiyadan foydalaning:

```json5
{
  agents: {
    defaults: {
      sandbox: {
        browser: { enabled: true },
      },
    },
  },
}
```

Maxsus brauzer image’i:

```json5
{
  agents: {
    defaults: {
      sandbox: { browser: { image: "my-openclaw-browser" } },
    },
  },
}
```

Yoqilganda, agent quyidagilarni oladi:

- sandbox brauzerini boshqarish URL’i (`browser` vositasi uchun)
- noVNC URL’i (agar yoqilgan bo‘lsa va headless=false)

Eslab qoling: agar vositalar uchun allowlist’dan foydalansangiz, `browser` ni qo‘shing (va deny’dan olib tashlang), aks holda vosita bloklangan bo‘lib qoladi.
Prune qoidalari (`agents.defaults.sandbox.prune`) brauzer konteynerlariga ham qo‘llanadi.

### Maxsus sandbox image’i

O‘zingizning image’ingizni yig‘ing va konfiguratsiyani unga yo‘naltiring:

```bash
docker build -t my-openclaw-sbx -f Dockerfile.sandbox .
```

```json5
{
  agents: {
    defaults: {
      sandbox: { docker: { image: "my-openclaw-sbx" } },
    },
  },
}
```

### Vositlar siyosati (allow/deny)

- `deny` `allow`dan ustun turadi.
- Agar `allow` bo‘sh bo‘lsa: barcha vositalar (deny’dan tashqari) mavjud.
- Agar `allow` bo‘sh bo‘lmasa: faqat `allow` dagi vositalar mavjud (deny chiqarib tashlanadi).

### Pruning strategiyasi

Ikki sozlama:

- `prune.idleHours`: X soat davomida ishlatilmagan konteynerlarni o‘chirish (0 = o‘chirilgan)
- `prune.maxAgeDays`: X kundan eski konteynerlarni o‘chirish (0 = o‘chirilgan)

Misol:

- Band sessiyalarni saqlab, lekin umrini cheklash:
  `idleHours: 24`, `maxAgeDays: 7`
- Hech qachon prune qilmang:
  `idleHours: 0`, `maxAgeDays: 0`

### Xavfsizlik eslatmalari

- Qattiq devor faqat **vositalar** ga taalluqli (exec/read/write/edit/apply_patch).
- Brauzer/kamera/canvas kabi host-only vositalar sukut bo‘yicha bloklangan.
- Sandbox’da `browser`ga ruxsat berish **izolyatsiyani buzadi** (brauzer host’da ishlaydi).

## 1. Nosozliklarni bartaraf etish

- 2. Tasvir yo‘q: [`scripts/sandbox-setup.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/sandbox-setup.sh) bilan build qiling yoki `agents.defaults.sandbox.docker.image` ni o‘rnating.
- 3. Konteyner ishlamayapti: u sessiya uchun talab bo‘yicha avtomatik yaratiladi.
- 4. Sandbox’dagi ruxsat xatolari: `docker.user` ni siz ulanayotgan workspace egaligiga mos UID:GID ga o‘rnating (yoki workspace papkasini chown qiling).
- 5. Maxsus vositalar topilmadi: OpenClaw buyruqlarni `sh -lc` (login shell) bilan ishga tushiradi, bu esa `/etc/profile` ni yuklaydi va PATH ni qayta o‘rnatishi mumkin. 6. `docker.env.PATH` ni sozlab, maxsus vosita yo‘llarini oldindan qo‘shing (masalan, `/custom/bin:/usr/local/share/npm-global/bin`), yoki Dockerfile’ingizda `/etc/profile.d/` ostiga skript qo‘shing.
