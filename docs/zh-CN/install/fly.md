---
title: 5. Fly.io
description: 6. 在 Fly.io 上部署 OpenClaw
---

# 7. Fly.io 部署

8. **目标：** 在一台 [Fly.io](https://fly.io) 机器上运行 OpenClaw Gateway，具备持久化存储、自动 HTTPS，以及 Discord/频道访问。

## 9. 你需要的东西

- 10. 已安装 [flyctl CLI](https://fly.io/docs/hands-on/install-flyctl/)
- 11. Fly.io 账号（免费套餐即可）
- 12. 模型认证：Anthropic API 密钥（或其他提供商的密钥）
- 42. 渠道凭证：Discord 机器人令牌、Telegram 令牌等。

## 14. 新手快速路径

1. 15. 克隆仓库 → 自定义 `fly.toml`
2. 16. 创建应用 + 卷 → 设置密钥
3. 17. 使用 `fly deploy` 部署
4. 18. 通过 SSH 登录以创建配置，或使用控制面板 UI

## 43) 1) 创建 Fly 应用

```bash
20. # 克隆仓库
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# 创建一个新的 Fly 应用（选择你自己的名称）
fly apps create my-openclaw

# 创建一个持久化卷（通常 1GB 就足够）
fly volumes create openclaw_data --size 1 --region iad
```

21. **提示：** 选择一个离你较近的区域。 22. 常见选项：`lhr`（伦敦）、`iad`（弗吉尼亚）、`sjc`（圣何塞）。

## 23. 2. 配置 fly.toml

24. 编辑 `fly.toml` 以匹配你的应用名称和需求。

25. **安全提示：** 默认配置会暴露一个公共 URL。 26. 如需无公共 IP 的加固部署，请参见 [Private Deployment](#private-deployment-hardened) 或使用 `fly.private.toml`。

```toml
44. app = "my-openclaw"  # 你的应用名称
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

28. **关键设置：**

| 29. 设置                             | 30. 原因                                                           |
| --------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| 31. `--bind lan`                   | 32. 绑定到 `0.0.0.0`，以便 Fly 的代理能够访问网关                               |
| 33. `--allow-unconfigured`         | 34. 在没有配置文件的情况下启动（之后你会创建一个）                                      |
| 35. `internal_port = 3000`         | 36. 必须与 `--port 3000`（或 `OPENCLAW_GATEWAY_PORT`）一致，以通过 Fly 的健康检查 |
| 37. `memory = "2048mb"`            | 38. 512MB 太小；推荐 2GB                                              |
| 39. `OPENCLAW_STATE_DIR = "/data"` | 40. 在卷上持久化状态                                                     |

## 41. 3. 设置密钥

```bash
42. # 必需：Gateway 令牌（用于非回环绑定）
fly secrets set OPENCLAW_GATEWAY_TOKEN=$(openssl rand -hex 32)

# 模型提供商 API 密钥
fly secrets set ANTHROPIC_API_KEY=sk-ant-...

# 可选：其他提供商
fly secrets set OPENAI_API_KEY=sk-...
fly secrets set GOOGLE_API_KEY=...

# 频道令牌
fly secrets set DISCORD_BOT_TOKEN=MTQ...
```

43. **注意：**

- 44. 非回环绑定（`--bind lan`）出于安全考虑需要 `OPENCLAW_GATEWAY_TOKEN`。
- 45. 请像对待密码一样对待这些令牌。
- 46. **所有 API 密钥和令牌优先使用环境变量**，而不是配置文件。 47. 这样可以避免密钥出现在 `openclaw.json` 中，被意外暴露或记录到日志。

## 48. 4. 部署

```bash
49. fly deploy
```

50. 首次部署会构建 Docker 镜像（约 2–3 分钟）。 1. 后续部署会更快。

2. 部署完成后，验证：

```bash
3. fly status
fly logs
```

4. 你应该看到：

```
5. [gateway] 正在监听 ws://0.0.0.0:3000 (PID xxx)
[discord] 已以 xxx 身份登录到 discord
```

## 6. 5. 创建配置文件

7. 通过 SSH 进入机器以创建正确的配置：

```bash
8. fly ssh console
```

9. 创建配置目录和文件：

```bash
10. mkdir -p /data
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

11. **注意：** 当 `OPENCLAW_STATE_DIR=/data` 时，配置路径为 `/data/openclaw.json`。

12. **注意：** Discord token 可以来自以下任一方式：

- 13. 环境变量：`DISCORD_BOT_TOKEN`（推荐用于存放密钥）
- 14. 配置文件：`channels.discord.token`

15. 如果使用环境变量，则无需在配置中添加 token。 16. 网关会自动读取 `DISCORD_BOT_TOKEN`。

17. 重启以生效：

```bash
45. exit
fly machine restart <machine-id>
```

## 19. 6. 访问网关

### 20. 控制 UI

21. 在浏览器中打开：

```bash
22. fly open
```

23. 或访问 `https://my-openclaw.fly.dev/`

24. 粘贴你的网关 token（来自 `OPENCLAW_GATEWAY_TOKEN`）以进行身份验证。

### 25. 日志

```bash
26. fly logs              # 实时日志
fly logs --no-tail    # 最近日志
```

### 27. SSH 控制台

```bash
28. fly ssh console
```

## 29. 故障排查

### 30. “App is not listening on expected address”

31. 网关绑定到了 `127.0.0.1`，而不是 `0.0.0.0`。

46. **修复：** 在 `fly.toml` 的进程命令中添加 `--bind lan`。

### 33. 健康检查失败 / 连接被拒绝

34. Fly 无法在配置的端口上访问网关。

35. **修复：** 确保 `internal_port` 与网关端口一致（设置 `--port 3000` 或 `OPENCLAW_GATEWAY_PORT=3000`）。

### 36. OOM / 内存问题

37. 容器不断重启或被杀死。 38. 迹象：`SIGABRT`、`v8::internal::Runtime_AllocateInYoungGeneration`，或无提示重启。

39. **修复：** 在 `fly.toml` 中增加内存：

```toml
40. [[vm]]
  memory = "2048mb"
```

41. 或更新现有机器：

```bash
42. fly machine update <machine-id> --vm-memory 2048 -y
```

43. **注意：** 512MB 太小。 44. 1GB 可能可用，但在负载较高或启用详细日志时可能 OOM。 45. **推荐使用 2GB。**

### 46. 网关锁问题

47. 网关因“already running”错误而拒绝启动。

48. 当容器重启但 PID 锁文件仍保留在卷上时会发生这种情况。

49. **修复：** 删除锁文件：

```bash
50. fly ssh console --command "rm -f /data/gateway.*.lock"
fly machine restart <machine-id>
```

锁文件位于 `/data/gateway.*.lock`（不在子目录中）。

### 配置未被读取

如果使用 `--allow-unconfigured`，网关会创建一个最小配置。 你在 `/data/openclaw.json` 的自定义配置应在重启后被读取。

验证配置是否存在：

```bash
fly ssh console --command "cat /data/openclaw.json"
```

### 通过 SSH 写入配置

`fly ssh console -C` 命令不支持 shell 重定向。 写入配置文件的方法：

```bash
# 使用 echo + tee（从本地通过管道传到远程）
echo '{"your":"config"}' | fly ssh console -C "tee /data/openclaw.json"

# 或使用 sftp
fly sftp shell
> put /local/path/config.json /data/openclaw.json
```

**注意：** 如果文件已存在，`fly sftp` 可能会失败。 47. 先删除：

```bash
fly ssh console --command "rm /data/openclaw.json"
```

### 状态未持久化

如果在重启后丢失凭据或会话，说明状态目录正在写入容器文件系统。

**修复：** 确保在 `fly.toml` 中设置了 `OPENCLAW_STATE_DIR=/data`，然后重新部署。

## 更新

```bash
# 拉取最新更改
git pull

# 重新部署
fly deploy

# 检查健康状态
fly status
fly logs
```

### 48. 更新机器命令

如果需要在不进行完整重新部署的情况下更改启动命令：

```bash
# 获取机器 ID
fly machines list

# 更新命令
fly machine update <machine-id> --command "node dist/index.js gateway --port 3000 --bind lan" -y

# 或增加内存
fly machine update <machine-id> --vm-memory 2048 --command "node dist/index.js gateway --port 3000 --bind lan" -y
```

**注意：** 在执行 `fly deploy` 之后，机器命令可能会重置为 `fly.toml` 中的内容。 如果你做了手动更改，请在部署后重新应用它们。

## 私有部署（加固）

默认情况下，Fly 会分配公共 IP，使你的网关可通过 `https://your-app.fly.dev` 访问。 49. 这很方便，但意味着你的部署会被互联网扫描器（Shodan、Censys 等）发现。

如果需要 **无任何公网暴露** 的加固部署，请使用私有模板。

### 何时使用私有部署

- 你只进行 **出站** 调用/消息（没有入站 Webhook）
- 你使用 **ngrok 或 Tailscale** 隧道来处理任何 Webhook 回调
- 你通过 **SSH、代理或 WireGuard** 访问网关，而不是通过浏览器
- 你希望部署 **对互联网扫描器隐藏**

### 设置

使用 `fly.private.toml` 而不是标准配置：

```bash
# 使用私有配置部署
fly deploy -c fly.private.toml
```

或转换现有部署：

```bash
# 列出当前 IP
fly ips list -a my-openclaw

# 释放公共 IP
fly ips release <public-ipv4> -a my-openclaw
fly ips release <public-ipv6> -a my-openclaw

# 切换到私有配置，使未来的部署不会重新分配公共 IP
#（移除 [http_service] 或使用私有模板部署）
fly deploy -c fly.private.toml

# 分配仅私有的 IPv6
fly ips allocate-v6 --private -a my-openclaw
```

完成后，`fly ips list` 应只显示一个 `private` 类型的 IP：

```
VERSION  IP                   TYPE             REGION
v6       fdaa:x:x:x:x::x      private          global
```

### 访问私有部署

由于没有公共 URL，请使用以下方法之一：

**选项 1：本地代理（最简单）**

```bash
# 将本地端口 3000 转发到应用
fly proxy 3000:3000 -a my-openclaw

# 然后在浏览器中打开 http://localhost:3000
```

**选项 2：WireGuard VPN**

```bash
# 创建 WireGuard 配置（一次性）
fly wireguard create

# 导入到 WireGuard 客户端，然后通过内部 IPv6 访问
# 示例：http://[fdaa:x:x:x:x::x]:3000
```

50. **选项 3：仅 SSH**

```bash
fly ssh console -a my-openclaw
```

### 私有部署下的 Webhook

如果你需要 Webhook 回调（Twilio、Telnyx 等） 且不进行公网暴露：

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
| 直接攻击              | Possible     | Blocked    |
| Control UI access | Browser      | Proxy/VPN  |
| Webhook delivery  | Direct       | Via tunnel |

## Notes

- Fly.io 使用 **x86 架构**（不是 ARM）
- The Dockerfile is compatible with both architectures
- For WhatsApp/Telegram onboarding, use `fly ssh console`
- Persistent data lives on the volume at `/data`
- Signal requires Java + signal-cli; use a custom image and keep memory at 2GB+.

## Cost

With the recommended config (`shared-cpu-2x`, 2GB RAM):

- ~$10-15/month depending on usage
- Free tier includes some allowance

See [Fly.io pricing](https://fly.io/docs/about/pricing/) for details.
