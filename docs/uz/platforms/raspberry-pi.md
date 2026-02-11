---
summary: "Raspberry Pi’da OpenClaw (byudjetli self-hosted sozlama)"
read_when:
  - Raspberry Pi’da OpenClaw’ni sozlash
  - ARM qurilmalarida OpenClaw’ni ishga tushirish
  - Arzon, doimiy ishlaydigan shaxsiy AI yaratish
title: "Raspberry Pi"
---

# Raspberry Pi’da OpenClaw

## Maqsad

**~$35–80** bir martalik xarajat bilan (oylik to‘lovsiz) Raspberry Pi’da doimiy, doimo yoqilgan OpenClaw Gateway’ni ishga tushirish.

Mos keladi:

- 24/7 shaxsiy AI yordamchi
- Uy avtomatlashtirish markazi
- Kam quvvat sarflovchi, doim mavjud Telegram/WhatsApp bot

## Uskuna talablari

| Pi modeli       | RAM     | Ishlaydimi?  | Eslatmalar                                          |
| --------------- | ------- | ------------ | --------------------------------------------------- |
| **Pi 5**        | 4GB/8GB | ✅ Eng yaxshi | Eng tezkor, tavsiya etiladi                         |
| **Pi 4**        | 4GB     | ✅ Yaxshi     | Ko‘pchilik foydalanuvchilar uchun eng maqbul tanlov |
| **Pi 4**        | 2GB     | ✅ OK         | Works, add swap                                     |
| **Pi 4**        | 1GB     | ⚠️ Tight     | Possible with swap, minimal config                  |
| **Pi 3B+**      | 1GB     | ⚠️ Slow      | Works but sluggish                                  |
| **Pi Zero 2 W** | 512MB   | ❌            | Not recommended                                     |

**Minimum specs:** 1GB RAM, 1 core, 500MB disk  
**Recommended:** 2GB+ RAM, 64-bit OS, 16GB+ SD card (or USB SSD)

## What You'll Need

- Raspberry Pi 4 or 5 (2GB+ recommended)
- MicroSD card (16GB+) or USB SSD (better performance)
- Power supply (official Pi PSU recommended)
- Network connection (Ethernet or WiFi)
- ~30 minutes

## 1. Flash the OS

Use **Raspberry Pi OS Lite (64-bit)** — no desktop needed for a headless server.

1. Download [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
2. Choose OS: **Raspberry Pi OS Lite (64-bit)**
3. Click the gear icon (⚙️) to pre-configure:
   - Set hostname: `gateway-host`
   - Enable SSH
   - Set username/password
   - Configure WiFi (if not using Ethernet)
4. Flash to your SD card / USB drive
5. Insert and boot the Pi

## 2) Connect via SSH

```bash
ssh user@gateway-host
# or use the IP address
ssh user@192.168.x.x
```

## 3. System Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y git curl build-essential

# Set timezone (important for cron/reminders)
sudo timedatectl set-timezone America/Chicago  # Change to your timezone
```

## 4. Install Node.js 22 (ARM64)

```bash
# Install Node.js via NodeSource
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs

# Verify
node --version  # Should show v22.x.x
npm --version
```

## 5. Add Swap (Important for 2GB or less)

Swap prevents out-of-memory crashes:

```bash
# Create 2GB swap file
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Make permanent
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Optimize for low RAM (reduce swappiness)
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

## 6. Install OpenClaw

### Option A: Standard Install (Recommended)

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

### Option B: Hackable Install (For tinkering)

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
npm install
npm run build
npm link
```

The hackable install gives you direct access to logs and code — useful for debugging ARM-specific issues.

## 7. Run Onboarding

```bash
1. openclaw onboard --install-daemon
```

2. Yo‘riqnomaga amal qiling:

1. 3. **Gateway rejimi:** Local
2. 4. **Auth:** API kalitlari tavsiya etiladi (OAuth boshqaruvsiz Pi’da injiq bo‘lishi mumkin)
3. 5. **Kanallar:** Boshlash uchun Telegram eng oson
4. 6. **Daemon:** Ha (systemd)

## 7) 8) O‘rnatishni tekshirish

```bash
8. # Holatni tekshirish
openclaw status

# Xizmatni tekshirish
sudo systemctl status openclaw

# Loglarni ko‘rish
journalctl -u openclaw -f
```

## 9. 9. Dashboard’ga kirish

10. Pi boshqaruvsiz bo‘lgani uchun SSH tunnel’dan foydalaning:

```bash
11. # Noutbuk/desktop’dan
ssh -L 18789:localhost:18789 user@gateway-host

# So‘ng brauzerda oching
open http://localhost:18789
```

12. Yoki doimiy ulanish uchun Tailscale’dan foydalaning:

```bash
13. # Pi’da
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

# Konfiguratsiyani yangilang
openclaw config set gateway.bind tailnet
sudo systemctl restart openclaw
```

---

## 14. Ishlash samaradorligini optimallashtirish

### 15. USB SSD’dan foydalaning (katta yaxshilanish)

16. SD kartalar sekin va tez eskiradi. 17. USB SSD ishlashni sezilarli darajada yaxshilaydi:

```bash
18. # USB’dan yuklanayotganini tekshirish
lsblk
```

19. Sozlash uchun [Pi USB yuklash qo‘llanmasi](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#usb-mass-storage-boot) ni ko‘ring.

### 20. Xotira sarfini kamaytirish

```bash
21. # GPU xotirasini o‘chirish (boshqaruvsiz)
echo 'gpu_mem=16' | sudo tee -a /boot/config.txt

# Kerak bo‘lmasa Bluetooth’ni o‘chiring
sudo systemctl disable bluetooth
```

### 22. Resurslarni kuzatish

```bash
23. # Xotirani tekshirish
free -h

# CPU haroratini tekshirish
vcgencmd measure_temp

# Jonli monitoring
htop
```

---

## 24. ARM’ga xos eslatmalar

### 25. Binar moslik

26. OpenClaw’ning aksariyat funksiyalari ARM64’da ishlaydi, ammo ba’zi tashqi binarlar ARM build’larini talab qilishi mumkin:

| 27. Asbob                                 | 28. ARM64 holati | 29. Izohlar                             |
| ---------------------------------------------------------------- | --------------------------------------- | -------------------------------------------------------------- |
| 30. Node.js               | 31. ✅            | 32. Juda yaxshi ishlaydi                |
| 33. WhatsApp (Baileys) | 34. ✅            | 35. To‘liq JS, muammo yo‘q              |
| 36. Telegram                              | 37. ✅            | 38. To‘liq JS, muammo yo‘q              |
| 39. gog (Gmail CLI)    | 40. ⚠️           | 41. ARM relizini tekshiring             |
| 42. Chromium (brauzer) | 43. ✅            | 44. `sudo apt install chromium-browser` |

45. Agar skill ishlamasa, uning binari ARM build’iga ega ekanini tekshiring. 46. Ko‘plab Go/Rust asboblari bor; ba’zilari yo‘q.

### 47. 32-bit vs 64-bit

48. **Har doim 64-bit OS’dan foydalaning.** Node.js va ko‘plab zamonaviy asboblar buni talab qiladi. 49. Tekshirish:

```bash
50. uname -m
# Shuni ko‘rsatishi kerak: aarch64 (64-bit), armv7l (32-bit) emas
```

---

## Recommended Model Setup

Since the Pi is just the Gateway (models run in the cloud), use API-based models:

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-sonnet-4-20250514",
        "fallbacks": ["openai/gpt-4o-mini"]
      }
    }
  }
}
```

**Don't try to run local LLMs on a Pi** — even small models are too slow. Let Claude/GPT do the heavy lifting.

---

## Auto-Start on Boot

The onboarding wizard sets this up, but to verify:

```bash
# Check service is enabled
sudo systemctl is-enabled openclaw

# Enable if not
sudo systemctl enable openclaw

# Start on boot
sudo systemctl start openclaw
```

---

## Troubleshooting

### Out of Memory (OOM)

```bash
# Check memory
free -h

# Add more swap (see Step 5)
# Or reduce services running on the Pi
```

### Slow Performance

- Use USB SSD instead of SD card
- Disable unused services: `sudo systemctl disable cups bluetooth avahi-daemon`
- Check CPU throttling: `vcgencmd get_throttled` (should return `0x0`)

### Service Won't Start

```bash
# Check logs
journalctl -u openclaw --no-pager -n 100

# Common fix: rebuild
cd ~/openclaw  # if using hackable install
npm run build
sudo systemctl restart openclaw
```

### ARM Binary Issues

If a skill fails with "exec format error":

1. Ikkilik faylda ARM64 build mavjudligini tekshiring
2. Try building from source
3. Or use a Docker container with ARM support

### WiFi Drops

For headless Pis on WiFi:

```bash
# Disable WiFi power management
sudo iwconfig wlan0 power off

# Make permanent
echo 'wireless-power off' | sudo tee -a /etc/network/interfaces
```

---

## Cost Comparison

| Setup                             | One-Time Cost        | Monthly Cost             | Notes                                               |
| --------------------------------- | -------------------- | ------------------------ | --------------------------------------------------- |
| **Pi 4 (2GB)** | ~$45 | $0                       | + power (~$5/yr) |
| **Pi 4 (4GB)** | ~$55 | $0                       | Recommended                                         |
| **Pi 5 (4GB)** | ~$60 | $0                       | Best performance                                    |
| **Pi 5 (8GB)** | ~$80 | $0                       | Overkill but future-proof                           |
| DigitalOcean                      | $0                   | $6/mo                    | $72/year                                            |
| Hetzner                           | $0                   | €3.79/mo | ~$50/year                           |

**Break-even:** A Pi pays for itself in ~6-12 months vs cloud VPS.

---

## See Also

- [Linux guide](/platforms/linux) — general Linux setup
- [DigitalOcean guide](/platforms/digitalocean) — cloud alternative
- [Hetzner guide](/install/hetzner) — Docker setup
- [Tailscale](/gateway/tailscale) — remote access
- [Nodes](/nodes) — pair your laptop/phone with the Pi gateway
