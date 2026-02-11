---
summary: "Linux qo‘llab-quvvatlashi + hamroh ilova holati"
read_when:
  - Linux uchun hamroh ilova holatini qidiryapsizmi
  - Platformalarni qamrab olish yoki hissa qo‘shishni rejalashtiryapsizmi
title: "Linux App"
---

# Linux App

Gateway Linux’da to‘liq qo‘llab-quvvatlanadi. **Node tavsiya etilgan runtime hisoblanadi**.
Gateway uchun Bun tavsiya etilmaydi (WhatsApp/Telegram xatolari).

Mahalliy Linux hamroh ilovalari rejalashtirilgan. Agar yaratishda yordam bermoqchi bo‘lsangiz, hissalar qabul qilinadi.

## Boshlovchilar uchun tezkor yo‘l (VPS)

1. Node 22+ ni o‘rnating
2. `npm i -g openclaw@latest`
3. `openclaw onboard --install-daemon`
4. Noutbukingizdan: `ssh -N -L 18789:127.0.0.1:18789 <user>@<host>`
5. `http://127.0.0.1:18789/` ni oching va tokeningizni joylashtiring

Bosqichma-bosqich VPS qo‘llanma: [exe.dev](/install/exe-dev)

## O‘rnatish

- [Getting Started](/start/getting-started)
- [Install & updates](/install/updating)
- Ixtiyoriy oqimlar: [Bun (experimental)](/install/bun), [Nix](/install/nix), [Docker](/install/docker)

## Gateway

- [Gateway runbook](/gateway)
- [Configuration](/gateway/configuration)

## Gateway xizmatini o‘rnatish (CLI)

Quyidagilardan birini ishlating:

```
openclaw onboard --install-daemon
```

Yoki:

```
openclaw gateway install
```

Yoki:

```
openclaw configure
```

So‘ralganda **Gateway service** ni tanlang.

Ta’mirlash/ko‘chirish:

```
openclaw doctor
```

## Tizim boshqaruvi (systemd user unit)

OpenClaw sukut bo‘yicha systemd **user** xizmatini o‘rnatadi. Ulashilgan yoki doimiy ishlaydigan serverlar uchun **system**
xizmatidan foydalaning. To‘liq unit namunasi va ko‘rsatmalar
[Gateway runbook](/gateway) da joylashgan.

Minimal sozlama:

`~/.config/systemd/user/openclaw-gateway[-<profile>].service` ni yarating:

```
[Unit]
Description=OpenClaw Gateway (profile: <profile>, v<version>)
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/local/bin/openclaw gateway --port 18789
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
```

Uni yoqing:

```
systemctl --user enable --now openclaw-gateway[-<profile>].service
```
