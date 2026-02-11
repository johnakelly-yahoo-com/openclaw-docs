---
summary: "8. Oracle Cloud’da OpenClaw (Always Free ARM)"
read_when:
  - 9. Oracle Cloud’da OpenClaw’ni sozlash
  - Looking for low-cost VPS hosting for OpenClaw
  - 11. Kichik serverda 24/7 OpenClaw xohlaysizmi
title: "12. Oracle Cloud"
---

# 13. Oracle Cloud’da OpenClaw (OCI)

## 14. Maqsad

15. Oracle Cloud’ning **Always Free** ARM qatlamida doimiy OpenClaw Gateway’ni ishga tushirish.

16. Oracle’ning bepul qatlamı OpenClaw uchun juda mos bo‘lishi mumkin (ayniqsa sizda allaqachon OCI hisobi bo‘lsa), ammo u ayrim murosalar bilan keladi:

- 17. ARM arxitekturasi (ko‘p narsa ishlaydi, ammo ayrim binarlar faqat x86 bo‘lishi mumkin)
- 18. Sig‘im va ro‘yxatdan o‘tish ba’zan muammoli bo‘lishi mumkin

## 19. Xarajatlar taqqoslanishi (2026)

| 20. Provayder    | 21. Reja            | 22. Xususiyatlar           | 23. Narx/oy              | 24. Izohlar                           |
| --------------------------------------- | ------------------------------------------ | ------------------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------ |
| 25. Oracle Cloud | 26. Always Free ARM | 27. 4 OCPU gacha, 24GB RAM | 28. $0                   | 29. ARM, cheklangan sig‘im            |
| 30. Hetzner      | 31. CX22            | 32. 2 vCPU, 4GB RAM        | 33. ~ $4 | 34. Eng arzon pullik variant          |
| 35. DigitalOcean | 36. Basic           | 37. 1 vCPU, 1GB RAM        | 38. $6                   | 39. Qulay interfeys, yaxshi hujjatlar |
| 40. Vultr        | 41. Cloud Compute   | 42. 1 vCPU, 1GB RAM        | 43. $6                   | 44. Ko‘plab joylashuvlar              |
| 45. Linode       | 46. Nanode          | 47. 1 vCPU, 1GB RAM        | 48. $5                   | 49. Endi Akamai tarkibida             |

---

## 50. Talablar

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
- Use the "Always Free" filter when selecting shape

### Tailscale won't connect

```bash
# Check status
sudo tailscale status

# Re-authenticate
sudo tailscale up --ssh --hostname=openclaw --reset
```

### Gateway ishga tushmayapti

```bash
openclaw gateway status
openclaw doctor --non-interactive
journalctl --user -u openclaw-gateway -n 50
```

### Control UI ga kira olmayapman

```bash
# Tailscale Serve ishlayotganini tekshiring
tailscale serve status

# Gateway tinglayotganini tekshiring
curl http://localhost:18789

# Kerak bo‘lsa qayta ishga tushiring
systemctl --user restart openclaw-gateway
```

### ARM binar muammolari

Ba’zi vositalarda ARM buildlari bo‘lmasligi mumkin. Tekshiring:

```bash
uname -m  # Should show aarch64
```

Ko‘pchilik npm paketlari muammosiz ishlaydi. Binarlar uchun `linux-arm64` yoki `aarch64` relizlarini qidiring.

---

## Saqlanish (Persistence)

Barcha holat ma’lumotlari shu yerda saqlanadi:

- `~/.openclaw/` — config, credentials, session data
- `~/.openclaw/workspace/` — ish maydoni (SOUL.md, xotira, artefaktlar)

Vaqti-vaqti bilan zaxira nusxa oling:

```bash
tar -czvf openclaw-backup.tar.gz ~/.openclaw ~/.openclaw/workspace
```

---

## Shuningdek qarang

- [Gateway remote access](/gateway/remote) — masofaviy kirishning boshqa usullari
- [Tailscale integration](/gateway/tailscale) — Tailscale bo‘yicha to‘liq hujjatlar
- [Gateway configuration](/gateway/configuration) — barcha konfiguratsiya variantlari
- [DigitalOcean guide](/platforms/digitalocean) — pullik + osonroq ro‘yxatdan o‘tish istasangiz
- [Hetzner guide](/install/hetzner) — Docker asosidagi muqobil yechim
