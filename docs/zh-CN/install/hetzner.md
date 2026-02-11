---
summary: "8. 在廉价的 Hetzner VPS（Docker）上 24/7 运行 OpenClaw Gateway，具备持久化状态和内置二进制文件"
read_when:
  - 你希望 OpenClaw 在云 VPS 上 24/7 运行（不是你的笔记本电脑）
  - 10. 你希望在自己的 VPS 上运行一个生产级、始终在线的 Gateway
  - 11. 你希望完全控制持久化、二进制文件和重启行为
  - 12. 你正在 Hetzner 或类似提供商上通过 Docker 运行 OpenClaw
title: "13. Hetzner"
---

# 14. Hetzner 上的 OpenClaw（Docker，生产 VPS 指南）

## 15. 目标

16. 使用 Docker 在 Hetzner VPS 上运行一个持久化的 OpenClaw Gateway，具备持久化状态、内置二进制文件和安全的重启行为。

17. 如果你想要“约 $5 的 24/7 OpenClaw”，这是最简单且可靠的设置。
    Hetzner 的定价会变化；选择最小的 Debian/Ubuntu VPS，如果遇到 OOM 再进行扩容。

## 19. 我们在做什么（通俗解释）？

- 20. 租用一台小型 Linux 服务器（Hetzner VPS）
- 21. 安装 Docker（隔离的应用运行时）
- 22. 在 Docker 中启动 OpenClaw Gateway
- 23. 在宿主机上持久化 `~/.openclaw` + `~/.openclaw/workspace`（重启/重建后仍然保留）
- 24. 通过 SSH 隧道从你的笔记本访问控制界面（Control UI）

25. Gateway 可通过以下方式访问：

- 从你的笔记本电脑进行 SSH 端口转发
- 27. 如果你自行管理防火墙和令牌，也可以直接暴露端口

28. 本指南假设你在 Hetzner 上使用 Ubuntu 或 Debian。
29. 如果你使用其他 Linux VPS，请相应映射软件包。
30. 通用 Docker 流程请参见 [Docker](/install/docker)。

---

## 31. 快速路径（有经验的运维人员）

1. 32. 购买 Hetzner VPS
2. 安装 Docker
3. 34. 克隆 OpenClaw 仓库
4. 35. 创建持久化的宿主机目录
5. 36. 配置 `.env` 和 `docker-compose.yml`
6. 37. 将所需二进制文件烘焙进镜像
7. 38. `docker compose up -d`
8. 39. 验证持久化和 Gateway 访问

---

## 40. 你需要准备

- 41. 具备 root 访问权限的 Hetzner VPS
- 42. 从你的笔记本进行 SSH 访问
- 对 SSH + 复制/粘贴有基本熟悉度
- 44. 约 20 分钟
- 45. Docker 和 Docker Compose
- 46. 模型认证凭据
- 47. 可选的提供商凭据
  - 48. WhatsApp 二维码
  - 49. Telegram 机器人令牌
  - 50. Gmail OAuth

---

## 1. Provision the VPS

Create an Ubuntu or Debian VPS in Hetzner.

以 root 身份连接：

```bash
ssh root@YOUR_VPS_IP
```

This guide assumes the VPS is stateful.
不要将其视为一次性基础设施。

---

## 2. Install Docker (on the VPS)

```bash
apt-get update
apt-get install -y git curl ca-certificates
curl -fsSL https://get.docker.com | sh
```

Verify:

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

## 4. Create persistent host directories

Docker containers are ephemeral.
所有长期存在的状态必须保存在主机上。

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

`--allow-unconfigured` 仅用于引导阶段的便利，并不能替代正确的网关配置。 仍然需要设置认证（`gateway.auth.token` 或密码），并为你的部署使用安全的绑定设置。

---

## 7. Bake required binaries into the image (critical)

Installing binaries inside a running container is a trap.
Anything installed at runtime will be lost on restart.

All external binaries required by skills must be installed at image build time.

The examples below show three common binaries only:

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

从你的笔记本电脑：

```bash
ssh -N -L 18789:127.0.0.1:18789 root@YOUR_VPS_IP
```

3. 打开：

`http://127.0.0.1:18789/`

5. 粘贴你的网关令牌。

---

## 6. 哪些内容持久化到哪里（真实来源）

7. OpenClaw 运行在 Docker 中，但 Docker 不是事实来源。
   所有长期存在的状态必须在重启、重建和重新启动后仍然存在。

| 9. 组件           | 10. 位置                   | 11. 持久化机制     | 12. 备注                    |
| -------------------------------------- | ----------------------------------------------- | ------------------------------------ | ------------------------------------------------ |
| 13. 网关配置        | /home/node/.openclaw/           | 15. 主机卷挂载     | 16. 包含 `openclaw.json`、令牌 |
| 17. 模型认证配置      | /home/node/.openclaw/           | 19. 主机卷挂载     | 20. OAuth 令牌、API 密钥       |
| 21. 技能配置        | /home/node/.openclaw/skills/    | 23. 主机卷挂载     | 24. 技能级状态                 |
| 25. 代理工作区       | /home/node/.openclaw/workspace/ | 27. 主机卷挂载     | 28. 代码和代理产物               |
| 29. WhatsApp 会话 | /home/node/.openclaw/           | 31. 主机卷挂载     | 32. 保留二维码登录               |
| 33. Gmail 密钥环   | /home/node/.openclaw/           | 35. 主机卷 + 密码  | 需要 `GOG_KEYRING_PASSWORD`                        |
| 37. 外部二进制文件     | /usr/local/bin/                                 | 39. Docker 镜像 | 40. 必须在构建时烘焙进镜像           |
| 41. Node 运行时    | 42. 容器文件系统               | 43. Docker 镜像 | 44. 每次镜像构建都会重建            |
| 45. 操作系统包       | 46. 容器文件系统               | 47. Docker 镜像 | 48. 不要在运行时安装              |
| 49. Docker 容器   | 50. 临时的                  | 可重启                                  | 可安全销毁                                            |
