---
summary: "Run OpenClaw Gateway 24/7 on a GCP Compute Engine VM (Docker) with durable state"
read_when:
  - 你希望 OpenClaw 在 GCP 上 24/7 运行
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
- 通过 SSH 隧道从你的笔记本电脑访问控制 UI

网关可以通过以下方式访问：

- 从你的笔记本电脑进行 SSH 端口转发
- 如果你自行管理防火墙和令牌，可以直接暴露端口

本指南在 GCP Compute Engine 上使用 Debian。
Ubuntu 也可以使用；请相应映射软件包。
如需通用的 Docker 流程，请参阅 [Docker](/install/docker)。

---

## 快速路径（有经验的运维人员）

1. 创建 GCP 项目并启用 Compute Engine API
2. 创建 Compute Engine VM（e2-small，Debian 12，20GB）
3. 通过 SSH 登录到 VM
4. 安装 Docker
5. 克隆 OpenClaw 仓库
6. 创建持久化主机目录
7. 配置 `.env` 和 `docker-compose.yml`
8. 构建所需二进制文件、构建并启动

---

## 你需要准备的内容

- GCP 账号（e2-micro 可享受免费层）
- 已安装 gcloud CLI（或使用 Cloud Console）
- 从你的笔记本电脑进行 SSH 访问
- 对 SSH 和复制/粘贴有基本熟悉度
- 约 20–30 分钟
- Docker 和 Docker Compose
- 模型认证凭据
- 可选的提供商凭据
  - WhatsApp 二维码
  - Telegram 机器人令牌
  - Gmail OAuth

---

## 1. 安装 gcloud CLI（或使用 Console）

**选项 A：gcloud CLI**（推荐用于自动化）

从 [https://cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install) 安装

初始化并进行身份验证：

```bash
gcloud init
gcloud auth login
```

**Option B: Cloud Console**

所有步骤都可以通过 Web UI 在 [https://console.cloud.google.com](https://console.cloud.google.com) 完成

---

## 2. 创建 GCP 项目

**CLI：**

```bash
gcloud projects create my-openclaw-project --name="OpenClaw Gateway"
gcloud config set project my-openclaw-project
```

在 [https://console.cloud.google.com/billing](https://console.cloud.google.com/billing) 启用结算（Compute Engine 所必需）。

启用 Compute Engine API：

```bash
gcloud services enable compute.googleapis.com
```

**Console：**

1. 前往 IAM & Admin > Create Project
2. 命名并创建
3. 为该项目启用结算
4. 导航到 APIs & Services > Enable APIs > 搜索“Compute Engine API”> Enable

---

## 3. 创建 VM

**机器类型：**

| 类型                                 | 规格                                          | 1. 成本                       | 2. 备注           |
| ---------------------------------- | ------------------------------------------- | -------------------------------------------------- | -------------------------------------- |
| 3. e2-small | 4. 2 vCPU，2GB 内存     | 5. 约 ~$12/月 | 6. 推荐           |
| 7. e2-micro | 8. 2 vCPU（共享），1GB 内存 | 9. 符合免费层资格                  | 10. 在负载下可能会 OOM |

11. **CLI：**

```bash
12. gcloud compute instances create openclaw-gateway \
  --zone=us-central1-a \
  --machine-type=e2-small \
  --boot-disk-size=20GB \
  --image-family=debian-12 \
  --image-project=debian-cloud
```

13. **控制台：**

1. 14. 前往 Compute Engine > VM instances > Create instance
2. 15. 名称：`openclaw-gateway`
3. 16. 区域：`us-central1`，可用区：`us-central1-a`
4. 17. 机器类型：`e2-small`
5. 18. 启动磁盘：Debian 12，20GB
6. 19. 创建

---

## 20. 4. SSH 登录到 VM

21. **CLI：**

```bash
22. gcloud compute ssh openclaw-gateway --zone=us-central1-a
```

23. **控制台：**

24. 在 Compute Engine 控制台中，点击你的 VM 旁边的 “SSH” 按钮。

25. 注意：VM 创建后，SSH 密钥传播可能需要 1–2 分钟。 26. 如果连接被拒绝，请等待后重试。

---

## 27. 5. 安装 Docker（在 VM 上）

```bash
28. sudo apt-get update
sudo apt-get install -y git curl ca-certificates
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
```

29. 注销并重新登录以使用户组更改生效：

```bash
30. exit
```

31. 然后重新通过 SSH 登录：

```bash
32. gcloud compute ssh openclaw-gateway --zone=us-central1-a
```

33. 验证：

```bash
34. docker --version
docker compose version
```

---

## 35. 6. 克隆 OpenClaw 仓库

```bash
36. git clone https://github.com/openclaw/openclaw.git
cd openclaw
```

37. 本指南假定你将构建一个自定义镜像以确保二进制文件的持久性。

---

## 38. 7. 创建持久化的主机目录

39. Docker 容器是短暂的。
40. 所有长期存在的状态都必须存放在主机上。

```bash
41. mkdir -p ~/.openclaw
mkdir -p ~/.openclaw/workspace
```

---

## 42. 8. 配置环境变量

43. 在仓库根目录创建 `.env`。

```bash
44. OPENCLAW_IMAGE=openclaw:latest
OPENCLAW_GATEWAY_TOKEN=change-me-now
OPENCLAW_GATEWAY_BIND=lan
OPENCLAW_GATEWAY_PORT=18789

OPENCLAW_CONFIG_DIR=/home/$USER/.openclaw
OPENCLAW_WORKSPACE_DIR=/home/$USER/.openclaw/workspace

GOG_KEYRING_PASSWORD=change-me-now
XDG_CONFIG_HOME=/home/node/.openclaw
```

45. 生成强随机密钥：

```bash
46. openssl rand -hex 32
```

47. **不要提交此文件。**

---

## 48. 9. Docker Compose 配置

49. 创建或更新 `docker-compose.yml`。

```yaml
50. services:
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
      # 推荐：在 VM 上仅将 Gateway 绑定到回环地址；通过 SSH 隧道访问。
      # 若要公开暴露，请移除 `127.0.0.1:` 前缀并相应配置防火墙。
      - "127.0.0.1:${OPENCLAW_GATEWAY_PORT}:18789"

      # 可选：仅当你针对该 VM 运行 iOS/Android 节点并需要 Canvas 主机时使用。
      # 如果将其公开暴露，请阅读 /gateway/security 并相应配置防火墙。
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

## 1. 10）将所需的二进制文件烘焙进镜像（关键）

2. 在运行中的容器内安装二进制文件是一个陷阱。
3. 任何在运行时安装的内容都会在重启时丢失。

4. 技能所需的所有外部二进制文件都必须在构建镜像时安装。

5. 下面的示例仅展示了三个常见的二进制文件：

- 6. `gog` 用于 Gmail 访问
- 7. `goplaces` 用于 Google Places
- 8. `wacli` 用于 WhatsApp

9. 这些只是示例，并非完整列表。
10. 你可以使用相同的模式安装任意数量的二进制文件。

11. 如果你之后添加依赖额外二进制文件的新技能，你必须：

1. 更新 Dockerfile
2. 13. 重新构建镜像
3. 14. 重启容器

15) **示例 Dockerfile**

```dockerfile
16. FROM node:22-bookworm

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

## 17. 11）构建并启动

```bash
18. docker compose build
docker compose up -d openclaw-gateway
```

19. 验证二进制文件：

```bash
20. docker compose exec openclaw-gateway which gog
docker compose exec openclaw-gateway which goplaces
docker compose exec openclaw-gateway which wacli
```

预期输出：

```
22. /usr/local/bin/gog
/usr/local/bin/goplaces
/usr/local/bin/wacli
```

---

## 23. 12）验证 Gateway

```bash
24. docker compose logs -f openclaw-gateway
```

Success:

```
26. [gateway] listening on ws://0.0.0.0:18789
```

---

## 27. 13）从你的笔记本电脑访问

28. 创建一个 SSH 隧道以转发 Gateway 端口：

```bash
29. gcloud compute ssh openclaw-gateway --zone=us-central1-a -- -L 18789:127.0.0.1:18789
```

30. 在浏览器中打开：

31. `http://127.0.0.1:18789/`

32. 粘贴你的 gateway token。

---

## 33. 数据持久化位置（事实来源）

34. OpenClaw 运行在 Docker 中，但 Docker 并不是事实来源。
35. 所有长期存在的状态都必须在重启、重建和重启主机后依然保留。

| 36. 组件         | 37. 位置                             | 38. 持久化机制 | 39. 备注                        |
| ------------------------------------- | --------------------------------------------------------- | -------------------------------- | ---------------------------------------------------- |
| 40. Gateway 配置 | 41. `/home/node/.openclaw/`        | 42. 主机卷挂载 | 43. 包含 `openclaw.json`、tokens |
| 44. 模型认证配置文件   | 45. `/home/node/.openclaw/`        | 46. 主机卷挂载 | 47. OAuth tokens、API keys     |
| 48. 技能配置       | 49. `/home/node/.openclaw/skills/` | 50. 主机卷挂载 | 技能级别状态                                               |
| Agent 工作区                             | /home/node/.openclaw/workspace/           | 主机卷挂载                            | 代码和 Agent 产物                                         |
| WhatsApp 会话                           | /home/node/.openclaw/                     | 主机卷挂载                            | 保留二维码登录                                              |
| Gmail 密钥环                             | /home/node/.openclaw/                     | 主机卷 + 密码                         | 需要 `GOG_KEYRING_PASSWORD`                            |
| 外部二进制文件                               | /usr/local/bin/                                           | Docker 镜像                        | 必须在构建时烘焙进镜像                                          |
| Node 运行时                              | 容器文件系统                                                    | Docker 镜像                        | 每次镜像构建都会重新构建                                         |
| 操作系统软件包                               | 容器文件系统                                                    | Docker 镜像                        | 不要在运行时安装                                             |
| Docker 容器                             | 临时的                                                       | 可重启的                             | 可安全销毁                                                |

---

## 更新

在 VM 上更新 OpenClaw：

```bash
cd ~/openclaw
git pull
docker compose build
docker compose up -d
```

---

## 故障排查

**SSH 连接被拒绝**

VM 创建后，SSH 密钥传播可能需要 1–2 分钟。 等待后重试。

**OS 登录问题**

检查你的 OS Login 配置文件：

```bash
gcloud compute os-login describe-profile
```

确保你的账号具有所需的 IAM 权限（Compute OS Login 或 Compute OS Admin Login）。

**内存不足（OOM）**

如果使用 e2-micro 并遇到 OOM，请升级到 e2-small 或 e2-medium：

```bash
# Stop the VM first
gcloud compute instances stop openclaw-gateway --zone=us-central1-a

# Change machine type
gcloud compute instances set-machine-type openclaw-gateway \
  --zone=us-central1-a \
  --machine-type=e2-small

# Start the VM
gcloud compute instances start openclaw-gateway --zone=us-central1-a
```

---

## 服务账号（安全最佳实践）

个人使用时，默认用户账号即可正常工作。

对于自动化或 CI/CD 流水线，请创建一个具有最小权限的专用服务账号：

1. 创建服务账号：

   ```bash
   gcloud iam service-accounts create openclaw-deploy \
     --display-name="OpenClaw Deployment"
   ```

2. 授予 Compute Instance Admin 角色（或更窄的自定义角色）：

   ```bash
   gcloud projects add-iam-policy-binding my-openclaw-project \
     --member="serviceAccount:openclaw-deploy@my-openclaw-project.iam.gserviceaccount.com" \
     --role="roles/compute.instanceAdmin.v1"
   ```

1) 避免在自动化中使用 Owner 角色。 2. 使用最小权限原则。

3. 有关 IAM 角色详情，请参见 [https://cloud.google.com/iam/docs/understanding-roles](https://cloud.google.com/iam/docs/understanding-roles)。

---

## 4. 后续步骤

- 5. 设置消息通道：[Channels](/channels)
- 6. 将本地设备配对为节点：[Nodes](/nodes)
- 7. 配置 Gateway：[Gateway configuration](/gateway/configuration)
