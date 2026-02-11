---
summary: "8. Oracle Cloud 上的 OpenClaw（永久免费 ARM）"
read_when:
  - 9. 在 Oracle Cloud 上设置 OpenClaw
  - 10. 寻找适合 OpenClaw 的低成本 VPS 托管
  - 11. 想要在小型服务器上运行 24/7 的 OpenClaw
title: "12. Oracle Cloud"
---

# 13. Oracle Cloud（OCI）上的 OpenClaw

## 14. 目标

15. 在 Oracle Cloud 的 **永久免费** ARM 层上运行一个持久的 OpenClaw Gateway。

16. Oracle 的免费层非常适合 OpenClaw（尤其是如果你已经有 OCI 账户），但也存在一些权衡：

- 17. ARM 架构（大多数功能可用，但某些二进制文件可能仅支持 x86）
- 18. 容量和注册流程可能比较挑剔

## 19. 成本对比（2026）

| 20. 提供商          | 21. 套餐       | 22. 配置                | 23. 价格/月                 | 24. 备注          |
| --------------------------------------- | ----------------------------------- | -------------------------------------------- | ----------------------------------------------- | -------------------------------------- |
| 25. Oracle Cloud | 26. 永久免费 ARM | 27. 最多 4 OCPU，24GB 内存 | 28. $0                   | 29. ARM，容量有限    |
| 30. Hetzner      | 31. CX22     | 32. 2 vCPU，4GB 内存     | 33. ~ $4 | 34. 最便宜的付费选项    |
| 35. DigitalOcean | 36. 基础版      | 37. 1 vCPU，1GB 内存     | 38. $6                   | 39. 界面简单，文档完善   |
| 40. Vultr        | 41. 云计算      | 42. 1 vCPU，1GB 内存     | 43. $6                   | 44. 多个地区可选      |
| 45. Linode       | 46. Nanode   | 47. 1 vCPU，1GB 内存     | 48. $5                   | 49. 现已并入 Akamai |

---

## 50. 前提条件

- Oracle Cloud account ([signup](https://www.oracle.com/cloud/free/)) — see [community signup guide](https://gist.github.com/rssnyder/51e3cfedd730e7dd5f4a816143b25dbd) if you hit issues
- Tailscale account (free at [tailscale.com](https://tailscale.com))
- ~30 minutes

## 1. Create an OCI Instance

1. Log into [Oracle Cloud Console](https://cloud.oracle.com/)
2. Navigate to **Compute → Instances → Create Instance**
3. Configure:
   - **Name:** `openclaw`
   - **Image:** Ubuntu 24.04 (aarch64)
   - **Shape:** `VM.Standard.A1.Flex` (Ampere ARM)
   - **OCPUs:** 2 (or up to 4)
   - **Memory:** 12 GB (or up to 24 GB)
   - **Boot volume:** 50 GB (up to 200 GB free)
   - **SSH key:** Add your public key
4. Click **Create**
5. Note the public IP address

**Tip:** If instance creation fails with "Out of capacity", try a different availability domain or retry later. Free tier capacity is limited.

## 2. Connect and Update

```bash
# Connect via public IP
ssh ubuntu@YOUR_PUBLIC_IP

# Update system
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential
```

**Note:** `build-essential` is required for ARM compilation of some dependencies.

## 3. Configure User and Hostname

```bash
# Set hostname
sudo hostnamectl set-hostname openclaw

# Set password for ubuntu user
sudo passwd ubuntu

# Enable lingering (keeps user services running after logout)
sudo loginctl enable-linger ubuntu
```

## 4. Install Tailscale

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up --ssh --hostname=openclaw
```

This enables Tailscale SSH, so you can connect via `ssh openclaw` from any device on your tailnet — no public IP needed.

Verify:

```bash
tailscale status
```

**From now on, connect via Tailscale:** `ssh ubuntu@openclaw` (or use the Tailscale IP).

## 5. Install OpenClaw

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
source ~/.bashrc
```

When prompted "How do you want to hatch your bot?", select **"Do this later"**.

> Note: If you hit ARM-native build issues, start with system packages (e.g. `sudo apt install -y build-essential`) before reaching for Homebrew.

## 6. Configure Gateway (loopback + token auth) and enable Tailscale Serve

Use token auth as the default. It’s predictable and avoids needing any “insecure auth” Control UI flags.

```bash
# Keep the Gateway private on the VM
openclaw config set gateway.bind loopback

# Require auth for the Gateway + Control UI
openclaw config set gateway.auth.mode token
openclaw doctor --generate-gateway-token

# Expose over Tailscale Serve (HTTPS + tailnet access)
openclaw config set gateway.tailscale.mode serve
openclaw config set gateway.trustedProxies '["127.0.0.1"]'

systemctl --user restart openclaw-gateway
```

## 7. Verify

```bash
# Check version
openclaw --version

# Check daemon status
systemctl --user status openclaw-gateway

# Check Tailscale Serve
tailscale serve status

# Test local response
curl http://localhost:18789
```

## 8. Lock Down VCN Security

Now that everything is working, lock down the VCN to block all traffic except Tailscale. OCI's Virtual Cloud Network acts as a firewall at the network edge — traffic is blocked before it reaches your instance.

1. Go to **Networking → Virtual Cloud Networks** in the OCI Console
2. Click your VCN → **Security Lists** → Default Security List
3. **Remove** all ingress rules except:
   - `0.0.0.0/0 UDP 41641` (Tailscale)
4. Keep default egress rules (allow all outbound)

This blocks SSH on port 22, HTTP, HTTPS, and everything else at the network edge. From now on, you can only connect via Tailscale.

---

## Access the Control UI

From any device on your Tailscale network:

```
https://openclaw.<tailnet-name>.ts.net/
```

Replace `<tailnet-name>` with your tailnet name (visible in `tailscale status`).

No SSH tunnel needed. Tailscale provides:

- HTTPS encryption (automatic certs)
- Authentication via Tailscale identity
- Access from any device on your tailnet (laptop, phone, etc.)

---

## Security: VCN + Tailscale (recommended baseline)

With the VCN locked down (only UDP 41641 open) and the Gateway bound to loopback, you get strong defense-in-depth: public traffic is blocked at the network edge, and admin access happens over your tailnet.

This setup often removes the _need_ for extra host-based firewall rules purely to stop Internet-wide SSH brute force — but you should still keep the OS updated, run `openclaw security audit`, and verify you aren’t accidentally listening on public interfaces.

### What's Already Protected

| Traditional Step   | Needed?     | Why                                                                          |
| ------------------ | ----------- | ---------------------------------------------------------------------------- |
| UFW firewall       | No          | VCN blocks before traffic reaches instance                                   |
| fail2ban           | No          | No brute force if port 22 blocked at VCN                                     |
| sshd hardening     | No          | Tailscale SSH doesn't use sshd                                               |
| Disable root login | No          | Tailscale uses Tailscale identity, not system users                          |
| SSH key-only auth  | No          | Tailscale authenticates via your tailnet                                     |
| IPv6 hardening     | Usually not | Depends on your VCN/subnet settings; verify what’s actually assigned/exposed |

### Still Recommended

- **Credential permissions:** `chmod 700 ~/.openclaw`
- **Security audit:** `openclaw security audit`
- **System updates:** `sudo apt update && sudo apt upgrade` regularly
- **Monitor Tailscale:** Review devices in [Tailscale admin console](https://login.tailscale.com/admin)

### Verify Security Posture

```bash
# Confirm no public ports listening
sudo ss -tlnp | grep -v '127.0.0.1\|::1'

# Verify Tailscale SSH is active
tailscale status | grep -q 'offers: ssh' && echo "Tailscale SSH active"

# Optional: disable sshd entirely
sudo systemctl disable --now ssh
```

---

## Fallback: SSH Tunnel

If Tailscale Serve isn't working, use an SSH tunnel:

```bash
# From your local machine (via Tailscale)
ssh -L 18789:127.0.0.1:18789 ubuntu@openclaw
```

Then open `http://localhost:18789`.

---

## Troubleshooting

### Instance creation fails ("Out of capacity")

Free tier ARM instances are popular. Try:

- Different availability domain
- Retry during off-peak hours (early morning)
- 1. 选择规格时使用“Always Free”筛选器

### 2. Tailscale 无法连接

```bash
3. # 检查状态
```

### sudo tailscale status

```bash
# 重新认证
```

### sudo tailscale up --ssh --hostname=openclaw --reset

```bash
4. 网关无法启动
```

### 5. openclaw gateway status

openclaw doctor --non-interactive journalctl --user -u openclaw-gateway -n 50

```bash
6. 无法访问控制界面（Control UI）
```

7. # 验证 Tailscale Serve 是否在运行 tailscale serve status

---

## # 检查网关是否在监听

curl http://localhost:18789

- `~/.openclaw/` — config, credentials, session data
- systemctl --user restart openclaw-gateway

8. ARM 二进制问题

```bash
9. 一些工具可能没有 ARM 构建版本。
```

---

## 10. 检查：

- 11. uname -m  # Should show aarch64
- 12. 大多数 npm 包都可以正常工作。
- 13. 对于二进制文件，查找 `linux-arm64` 或 `aarch64` 版本。
- [DigitalOcean guide](/platforms/digitalocean) — if you want paid + easier signup
- 15. 所有状态数据都存放在：
