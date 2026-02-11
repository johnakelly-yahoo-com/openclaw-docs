---
summary: "1. macOS’da Gateway hayotiy sikli (launchd)"
read_when:
  - Integrating the mac app with the gateway lifecycle
title: "3. Gateway hayotiy sikli"
---

# 4. macOS’da Gateway hayotiy sikli

The macOS app **manages the Gateway via launchd** by default and does not spawn
the Gateway as a child process. 6. Avval u sozlangan portda allaqachon ishlayotgan Gateway’ga ulanishga harakat qiladi; agar hech biri mavjud bo‘lmasa, tashqi `openclaw` CLI orqali launchd xizmatini yoqadi (ichki runtime yo‘q). 7. Bu tizimga kirishda ishonchli avtomatik ishga tushirishni va nosozliklardan keyin qayta ishga tushirishni ta’minlaydi.

Child‑process mode (Gateway spawned directly by the app) is **not in use** today.
If you need tighter coupling to the UI, run the Gateway manually in a terminal.

## Default behavior (launchd)

- 11. Ilova `bot.molt.gateway` yorlig‘iga ega bo‘lgan per‑user LaunchAgent’ni o‘rnatadi
      (yoki `bot.molt.<profile>` when using `--profile`/`OPENCLAW_PROFILE`; legacy `com.openclaw.*` is supported).
- 13. Local rejim yoqilganda, ilova LaunchAgent yuklanganini ta’minlaydi va kerak bo‘lsa Gateway’ni ishga tushiradi.
- Logs are written to the launchd gateway log path (visible in Debug Settings).

15. Keng tarqalgan buyruqlar:

```bash
16. launchctl kickstart -k gui/$UID/bot.molt.gateway
launchctl bootout gui/$UID/bot.molt.gateway
```

Replace the label with `bot.molt.<profile>18. ` \`.

## Unsigned dev builds

20. `scripts/restart-mac.sh --no-sign` — imzolash kalitlari bo‘lmaganda tezkor lokal build’lar uchun. To prevent launchd from pointing at an unsigned relay binary, it:

- 22. `~/.openclaw/disable-launchagent` ni yozadi.

23. `scripts/restart-mac.sh` ning imzolangan ishga tushirilishi, agar marker mavjud bo‘lsa, bu override’ni tozalaydi. 24. Qo‘lda tiklash uchun:

```bash
25. rm ~/.openclaw/disable-launchagent
```

## 26. Faqat ulanish rejimi

27. macOS ilovasini **hech qachon launchd’ni o‘rnatmasligi yoki boshqarmasligi** uchun uni `--attach-only` (yoki `--no-launchd`) bilan ishga tushiring. 28. Bu `~/.openclaw/disable-launchagent` ni o‘rnatadi, shuning uchun ilova faqat allaqachon ishlayotgan Gateway’ga ulanadi. 29. Xuddi shu xatti-harakatni Debug Settings’da yoqib/o‘chirishingiz mumkin.

## 30. Remote rejim

31. Remote rejim hech qachon lokal Gateway’ni ishga tushirmaydi. 32. Ilova masofaviy xostga SSH tunneli orqali ulanadi va shu tunnel orqali bog‘lanadi.

## 33. Nega biz launchd’ni afzal ko‘ramiz

- 34. Tizimga kirishda avtomatik ishga tushirish.
- 35. O‘rnatilgan qayta ishga tushirish/KeepAlive semantikasi.
- 36. Bashorat qilinadigan loglar va nazorat.

37. Agar haqiqiy bola-jarayon rejimi yana kerak bo‘lsa, u alohida, aniq dev‑only rejim sifatida hujjatlashtirilishi kerak.
