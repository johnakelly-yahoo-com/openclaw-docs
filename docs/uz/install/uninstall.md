---
summary: "Agar `EACCES` xatolarini ko‘rsangiz, npm’ning global prefiksini foydalanuvchi yozishi mumkin bo‘lgan katalogga o‘tkazing:"
read_when:
  - mkdir -p "$HOME/.npm-global"

    npm config set prefix "$HOME/.npm-global"

    export PATH="$HOME/.npm-global/bin:$PATH"
  - Doimiy bo‘lishi uchun `export PATH=...` qatorini `~/.bashrc` yoki `~/.zshrc` ga qo‘shing.
title: "OpenClaw’ni to‘liq olib tashlash (CLI, xizmat, holat, ish maydoni)"
---

# Siz OpenClaw’ni kompyuterdan olib tashlamoqchisiz

O‘chirgandan keyin ham gateway xizmati ishlayapti

- O‘chirish
- O‘chirish

## Ikki yo‘l:

**Oson yo‘l** agar `openclaw` hali ham o‘rnatilgan bo‘lsa.

```bash
**Qo‘lda xizmatni olib tashlash** agar CLI yo‘q bo‘lsa, lekin xizmat ishlayotgan bo‘lsa.
```

Oson yo‘l (CLI hali ham o‘rnatilgan)

```bash
Tavsiya etiladi: o‘rnatilgan o‘chiruvchidan foydalaning:
```

openclaw uninstall

1. Interaktiv bo‘lmagan (avtomatlashtirish / npx):

```bash
openclaw uninstall --all --yes --non-interactive
npx -y openclaw uninstall --all --yes --non-interactive
```

2. Qo‘lda qadamlar (xuddi shu natija):

```bash
Gateway xizmatini to‘xtating:
```

3. 1. Holat va konfiguratsiyani o‘chirish:

```bash
rm -rf "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
```

Agar `OPENCLAW_CONFIG_PATH` ni holat katalogidan tashqaridagi maxsus joyga o‘rnatgan bo‘lsangiz, o‘sha faylni ham o‘chiring.

4. 4. Ish joyingizni o‘chiring (ixtiyoriy, agent fayllarini olib tashlaydi):

```bash
rm -rf ~/.openclaw/workspace
```

5. 6. CLI o‘rnatilishini olib tashlang (foydalanganingizni tanlang):

```bash
npm rm -g openclaw
pnpm remove -g openclaw
bun remove -g openclaw
```

6. 8. Agar macOS ilovasini o‘rnatgan bo‘lsangiz:

```bash
rm -rf /Applications/OpenClaw.app
```

10. Eslatmalar:

- 11. Agar profillardan (`--profile` / `OPENCLAW_PROFILE`) foydalangan bo‘lsangiz, har bir holat katalogi uchun 3-qadamni takrorlang (standartlari `~/.openclaw-<profile>`).
- 12. Masofaviy rejimda holat katalogi **gateway xost**da joylashadi, shuning uchun 1–4-qadamlarni u yerda ham bajaring.

## 13. Xizmatni qo‘lda olib tashlash (CLI o‘rnatilmagan)

14. Gateway xizmati ishlashda davom etib, lekin `openclaw` yo‘q bo‘lsa, shundan foydalaning.

### 15. macOS (launchd)

16. Standart yorliq `bot.molt.gateway` (yoki `bot.molt.<profile>`)17. `; eski `com.openclaw.\*\` hali ham mavjud bo‘lishi mumkin):

```bash
launchctl bootout gui/$UID/bot.molt.gateway
rm -f ~/Library/LaunchAgents/bot.molt.gateway.plist
```

19. Agar profildan foydalangan bo‘lsangiz, yorliq va plist nomini `bot.molt.<profile>` ga almashtiring.20. `. 21. Mavjud bo‘lsa, barcha eski `com.openclaw.\*\` plistlarini o‘chiring.

### 22. Linux (systemd foydalanuvchi unit’i)

23. Standart unit nomi `openclaw-gateway.service` (yoki `openclaw-gateway-<profile>.service`):

```bash
systemctl --user disable --now openclaw-gateway.service
rm -f ~/.config/systemd/user/openclaw-gateway.service
systemctl --user daemon-reload
```

### 25. Windows (Rejalashtirilgan vazifa)

26. Standart vazifa nomi `OpenClaw Gateway` (yoki `OpenClaw Gateway (<profile>)`).
27. Vazifa skripti holat katalogingiz ostida joylashgan.

```powershell
schtasks /Delete /F /TN "OpenClaw Gateway"
Remove-Item -Force "$env:USERPROFILE\.openclaw\gateway.cmd"
```

29. Agar profildan foydalangan bo‘lsangiz, mos vazifa nomini va `~\.openclaw-<profile>\gateway.cmd` faylini o‘chiring.

## 30. Oddiy o‘rnatish va manbadan (source) checkout o‘rtasidagi farq

### 31. Oddiy o‘rnatish (install.sh / npm / pnpm / bun)

32. Agar `https://openclaw.ai/install.sh` yoki `install.ps1` dan foydalangan bo‘lsangiz, CLI `npm install -g openclaw@latest` orqali o‘rnatilgan.
33. Uni `npm rm -g openclaw` bilan olib tashlang (yoki shu yo‘l bilan o‘rnatgan bo‘lsangiz `pnpm remove -g` / `bun remove -g`).

### 34. Manbadan checkout (git clone)

35. Agar repozitoriy checkout’idan ishlayotgan bo‘lsangiz (`git clone` + `openclaw ...` / `bun run openclaw ...`):

1. 36. Repo’ni o‘chirishdan **oldin** gateway xizmatini olib tashlang (yuqoridagi oson yo‘l yoki qo‘lda xizmatni olib tashlashdan foydalaning).
2. 37. Repo katalogini o‘chiring.
3. 38. Yuqorida ko‘rsatilgandek holat + ish joyini olib tashlang.
