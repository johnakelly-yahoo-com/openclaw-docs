---
summary: "当你需要隔离或 iMessage 时，在沙箱化的 macOS VM（本地或托管）中运行 OpenClaw。"
read_when:
  - 你希望将 OpenClaw 与你的主 macOS 环境隔离。
  - 你希望在沙箱中使用 iMessage 集成（BlueBubbles）。
  - 你希望拥有一个可重置、可克隆的 macOS 环境。
  - 你想比较本地与托管的 macOS VM 选项。
title: "macOS 虚拟机"
---

# macOS 虚拟机上的 OpenClaw（沙箱化）

## 推荐默认选项（适合大多数用户）

- **小型 Linux VPS**，用于始终在线的 Gateway，成本低。 参见 [VPS 托管](/vps)。
- 如果你想要完全控制并获得用于浏览器自动化的**住宅 IP**，请选择 **专用硬件**（Mac mini 或 Linux 主机）。 许多网站会封锁数据中心 IP，因此本地浏览通常效果更好。
- **混合方案：** 将 Gateway 放在便宜的 VPS 上，在需要浏览器/UI 自动化时将你的 Mac 作为 **节点** 连接。 参见 [节点](/nodes) 和 [Gateway 远程](/gateway/remote)。

当你明确需要仅限 macOS 的能力（iMessage/BlueBubbles）或希望与日常使用的 Mac 严格隔离时，使用 macOS VM。

## macOS VM 选项

### 在你的 Apple Silicon Mac（Lume）上运行本地 VM

使用 [Lume](https://cua.ai/docs/lume) 在你现有的 Apple Silicon Mac 上的沙箱化 macOS VM 中运行 OpenClaw。

这将为你提供：

- 完全隔离的 macOS 环境（宿主保持干净）
- 通过 BlueBubbles 支持 iMessage（在 Linux/Windows 上不可能）
- 通过克隆 VM 实现即时重置
- 无需额外硬件或云成本

### 托管 Mac 提供商（云）

如果你想在云中使用 macOS，托管 Mac 提供商同样可行：

- [MacStadium](https://www.macstadium.com/)（托管 Mac）
- 其他托管 Mac 供应商也可以使用；遵循其 VM + SSH 文档即可。

一旦你通过 SSH 访问到 macOS VM，请从下面的第 6 步继续。

---

## 快速路径（Lume，经验用户）

1. 安装 Lume
2. `lume create openclaw --os macos --ipsw latest`
3. 完成设置助理，启用远程登录（SSH）
4. `lume run openclaw --no-display`
5. 通过 SSH 登录，安装 OpenClaw，配置通道
6. 完成

---

## 你需要的条件（Lume）

- Apple Silicon Mac（M1/M2/M3/M4）
- 宿主机为 macOS Sequoia 或更高版本
- 每个 VM 约 60 GB 可用磁盘空间
- 约 20 分钟

---

## 1. Install Lume

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/trycua/cua/main/libs/lume/scripts/install.sh)"
```

If `~/.local/bin` isn't in your PATH:

```bash
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.zshrc && source ~/.zshrc
```

Verify:

```bash
lume --version
```

Docs: [Lume Installation](https://cua.ai/docs/lume/guide/getting-started/installation)

---

## 2. Create the macOS VM

```bash
lume create openclaw --os macos --ipsw latest
```

This downloads macOS and creates the VM. VNC 窗口会自动打开。

Note: The download can take a while depending on your connection.

---

## 3. Complete Setup Assistant

在 VNC 窗口中：

1. Select language and region
2. Skip Apple ID (or sign in if you want iMessage later)
3. Create a user account (remember the username and password)
4. 跳过所有可选功能

After setup completes, enable SSH:

1. Open System Settings → General → Sharing
2. Enable "Remote Login"

---

## 4. Get the VM's IP address

```bash
lume get openclaw
```

Look for the IP address (usually `192.168.64.x`).

---

## 5. SSH into the VM

```bash
ssh youruser@192.168.64.X
```

将 `youruser` 替换为你创建的账户，将 IP 替换为你的 VM 的 IP。

---

## 6. Install OpenClaw

Inside the VM:

```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

Follow the onboarding prompts to set up your model provider (Anthropic, OpenAI, etc.).

---

## 7. Configure channels

Edit the config file:

```bash
nano ~/.openclaw/openclaw.json
```

Add your channels:

```json
{
  "channels": {
    "whatsapp": {
      "dmPolicy": "allowlist",
      "allowFrom": ["+15551234567"]
    },
    "telegram": {
      "botToken": "YOUR_BOT_TOKEN"
    }
  }
}
```

Then login to WhatsApp (scan QR):

```bash
openclaw channels login
```

---

## 8. Run the VM headlessly

Stop the VM and restart without display:

```bash
lume stop openclaw
lume run openclaw --no-display
```

The VM runs in the background. OpenClaw's daemon keeps the gateway running.

To check status:

```bash
ssh youruser@192.168.64.X "openclaw status"
```

---

## Bonus: iMessage integration

This is the killer feature of running on macOS. Use [BlueBubbles](https://bluebubbles.app) to add iMessage to OpenClaw.

Inside the VM:

1. Download BlueBubbles from bluebubbles.app
2. 使用你的 Apple ID 登录
3. 启用 Web API 并设置一个密码
4. 将 BlueBubbles 的 webhook 指向你的网关（示例：`https://your-gateway-host:3000/bluebubbles-webhook?password=<password>`）

添加到你的 OpenClaw 配置中：

```json
{
  "channels": {
    "bluebubbles": {
      "serverUrl": "http://localhost:1234",
      "password": "your-api-password",
      "webhookPath": "/bluebubbles-webhook"
    }
  }
}
```

Restart the gateway. 现在你的代理可以发送和接收 iMessage 了。

完整设置详情：[BlueBubbles channel](/channels/bluebubbles)

---

## 保存一个黄金镜像

在进一步自定义之前，为你的干净状态创建快照：

```bash
lume stop openclaw
```

lume clone openclaw openclaw-golden

```bash
随时重置：
```

---

## lume stop openclaw && lume delete openclaw

lume clone openclaw-golden openclaw

- lume run openclaw --no-display
- 在“系统设置 → 节能”中禁用睡眠
- 通过以下方式保持 VM 持续运行：

让你的 Mac 保持接通电源 在系统设置 → 节能中禁用睡眠

---

## 如有需要，使用 `caffeinate`

| 如果需要真正的全天候运行，考虑使用专用的 Mac mini 或小型 VPS。 | 参见 [VPS hosting](/vps)。 |
| -------------------------------------- | ----------------------- |
| 故障排除                                   | 问题                      |
| 解决方案                                   | 无法 SSH 连接到 VM           |
| 未找到 Lume 命令                            | VM IP 未显示               |
| 等待 VM 完全启动后，再次运行 `lume get openclaw`   | 找不到 Lume 命令             |

---

## 将 `~/.local/bin` 添加到你的 PATH 中

- WhatsApp 二维码无法扫描
- 运行 `openclaw channels login` 时，确保你已登录到 VM（而不是宿主机）
- 相关文档
- [BlueBubbles 频道](/channels/bluebubbles)
- [Nodes](/nodes)
- [Gateway remote](/gateway/remote)
- [BlueBubbles channel](/channels/bluebubbles)
- [Lume Quickstart](https://cua.ai/docs/lume/guide/getting-started/quickstart)
