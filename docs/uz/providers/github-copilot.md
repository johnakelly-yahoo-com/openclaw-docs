---
summary: "7. Qurilma oqimi orqali OpenClaw’dan GitHub Copilot’ga kiring"
read_when:
  - 8. Siz GitHub Copilot’ni model provayderi sifatida ishlatmoqchisiz
  - 9. Sizga `openclaw models auth login-github-copilot` oqimi kerak
title: "10. GitHub Copilot"
---

# 11. GitHub Copilot

## 12. GitHub Copilot nima?

GitHub Copilot — GitHub’ning AI kod yozish yordamchisi. 14. U GitHub hisobingiz va rejangiz uchun Copilot modellarga kirishni ta’minlaydi. OpenClaw Copilot’ni model provayderi sifatida ikki xil usulda ishlata oladi.

## 16. OpenClaw’da Copilot’dan foydalanishning ikki yo‘li

### 17. 1. Ichki GitHub Copilot provayderi (`github-copilot`)

GitHub tokenini olish uchun native device-login oqimidan foydalaning, so‘ng OpenClaw ishga tushganda uni Copilot API tokenlariga almashtiring. 19. Bu **standart** va eng sodda yo‘l, chunki VS Code talab etilmaydi.

### 20. 2. Copilot Proxy plagini (`copilot-proxy`)

21. Mahalliy ko‘prik sifatida **Copilot Proxy** VS Code kengaytmasidan foydalaning. 22. OpenClaw proksining `/v1` endpoint’iga ulanadi va u yerda sozlagan model ro‘yxatidan foydalanadi. 23. Agar siz allaqachon VS Code’da Copilot Proxy’ni ishga tushirgan bo‘lsangiz yoki trafikni u orqali yo‘naltirishingiz kerak bo‘lsa, shuni tanlang.
22. Siz plaginini yoqishingiz va VS Code kengaytmasini doimiy ishlatib turishingiz kerak.

25. GitHub Copilot’ni model provayderi sifatida ishlating (`github-copilot`). 26. Kirish buyrug‘i GitHub qurilma oqimini ishga tushiradi, autentifikatsiya profilini saqlaydi va konfiguratsiyangizni shu profildan foydalanishga yangilaydi.

## 27. CLI sozlash

```bash
28. openclaw models auth login-github-copilot
```

29. Sizdan URL manziliga kirish va bir martalik kodni kiritish so‘raladi. 30. Jarayon tugaguncha terminalni ochiq qoldiring.

### 31. Ixtiyoriy bayroqlar

```bash
32. openclaw models auth login-github-copilot --profile-id github-copilot:work
openclaw models auth login-github-copilot --yes
```

## 33. Standart modelni o‘rnatish

```bash
openclaw models set github-copilot/gpt-4o
```

### 35. Konfiguratsiya parchasi

```json5
36. {
  agents: { defaults: { model: { primary: "github-copilot/gpt-4o" } } },
}
```

## 37. Eslatmalar

- 38. Interaktiv TTY talab etiladi; buyruqni to‘g‘ridan-to‘g‘ri terminalda ishga tushiring.
- 39. Copilot modellari mavjudligi rejangizga bog‘liq; agar model rad etilsa, boshqa ID’ni sinab ko‘ring (masalan `github-copilot/gpt-4.1`).
- 40. Kirish jarayoni GitHub tokenini autentifikatsiya profillari omborida saqlaydi va OpenClaw ishga tushganda uni Copilot API tokeniga almashtiradi.
