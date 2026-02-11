---
summary: "`openclaw approvals` uchun CLI ma’lumotnomasi (gateway yoki node xostlari uchun exec tasdiqlari)"
read_when:
  - CLI orqali exec tasdiqlarini tahrirlashni xohlaysiz
  - Gateway yoki node xostlarida ruxsat etilgan ro‘yxatlarni boshqarishingiz kerak
title: "approvals"
---

# `openclaw approvals`

**Lokal xost**, **shlyuz xosti** yoki **tugun xosti** uchun exec tasdiqlarini boshqaring.
Standart bo‘yicha buyruqlar diskdagi lokal tasdiqlar fayliga yo‘naltiriladi. Shlyuzni nishonga olish uchun `--gateway`, yoki muayyan tugunni nishonga olish uchun `--node` dan foydalaning.

Bog‘liq:

- Exec tasdiqlari: [Exec approvals](/tools/exec-approvals)
- Tugunlar: [Nodes](/nodes)

## Umumiy buyruqlar

```bash
openclaw approvals get
openclaw approvals get --node <id|name|ip>
openclaw approvals get --gateway
```

## Fayldan tasdiqlarni almashtirish

```bash
openclaw approvals set --file ./exec-approvals.json
openclaw approvals set --node <id|name|ip> --file ./exec-approvals.json
openclaw approvals set --gateway --file ./exec-approvals.json
```

## Allowlist yordamchilari

```bash
openclaw approvals allowlist add "~/Projects/**/bin/rg"
openclaw approvals allowlist add --agent main --node <id|name|ip> "/usr/bin/uptime"
openclaw approvals allowlist add --agent "*" "/usr/bin/uname"

openclaw approvals allowlist remove "~/Projects/**/bin/rg"
```

## Eslatmalar

- `--node` `openclaw nodes` bilan bir xil resolverdan foydalanadi (id, nom, ip yoki id prefiksi).
- `--agent` standart bo‘yicha `"*"` bo‘lib, barcha agentlarga qo‘llanadi.
- Tugun xosti `system.execApprovals.get/set` ni e’lon qilishi kerak (macOS ilovasi yoki headless tugun xosti).
- Tasdiqlar fayllari har bir xost uchun `~/.openclaw/exec-approvals.json` da saqlanadi.
