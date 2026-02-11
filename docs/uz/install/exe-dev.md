---
summary: "7. Masofaviy kirish uchun OpenClaw Gateway’ni exe.dev’da (VM + HTTPS proxy) ishga tushiring"
read_when:
  - 8. Siz Gateway uchun arzon, doimiy ishlaydigan Linux xost xohlaysiz
  - 9. O‘zingiz VPS ishga tushirmasdan masofaviy Control UI kirishini xohlaysiz
title: "10. exe.dev"
---

# 11. exe.dev

12. Maqsad: OpenClaw Gateway exe.dev VM’da ishlashi va noutbukingizdan `https://<vm-name>.exe.xyz` orqali ochilishi

13. Ushbu sahifa exe.dev’ning standart **exeuntu** tasvirini nazarda tutadi. 14. Agar boshqa distro tanlagan bo‘lsangiz, paketlarni mos ravishda moslashtiring.

## 15. Boshlovchilar uchun tezkor yo‘l

1. 16. [https://exe.new/openclaw](https://exe.new/openclaw)
2. 17. Kerak bo‘lsa, autentifikatsiya kaliti/tokeningizni kiriting
3. 18. VM yonidagi "Agent" tugmasini bosing va kuting...
4. 19. ???
5. 20. Foyda

## 21) Sizga kerak bo‘ladiganlar

- 22. exe.dev akkaunti
- 23. [exe.dev](https://exe.dev) virtual mashinalariga `ssh exe.dev` orqali kirish (ixtiyoriy)

## 24. Shelley yordamida avtomatlashtirilgan o‘rnatish

25. exe.dev’ning agenti bo‘lgan Shelley bizning prompt orqali OpenClaw’ni bir zumda o‘rnatib bera oladi. 26. Quyida ishlatiladigan prompt keltirilgan:

```
27. Ushbu VM’da OpenClaw’ni (https://docs.openclaw.ai/install) sozlang. OpenClaw onboarding uchun non-interactive va accept-risk flag’laridan foydalaning. Kerak bo‘lsa, taqdim etilgan auth yoki tokenni qo‘shing. Nginx’ni sozlab, standart yoqilgan sayt konfiguratsiyasida 18789 portidan root joylashuvga yo‘naltiring va Websocket qo‘llab-quvvatlashini yoqing. Pairing `openclaw devices list` va `openclaw device approve <request id>` orqali amalga oshiriladi. Dashboard’da OpenClaw’ning sog‘ligi OK ekanini tekshiring. exe.dev biz uchun 8000 portdan 80/443 portlarga va HTTPS’ga yo‘naltirishni amalga oshiradi, shuning uchun yakuniy "reachable" <vm-name>.exe.xyz bo‘lishi kerak, portsiz.
```

## 28. Qo‘lda o‘rnatish

## 29. 1. VM yarating

30. Qurilmangizdan:

```bash
31. ssh exe.dev new
```

32. So‘ng ulanib oling:

```bash
33. ssh <vm-name>.exe.xyz
```

34. Maslahat: ushbu VM’ni **stateful** holda saqlang. 35. OpenClaw holatni `~/.openclaw/` va `~/.openclaw/workspace/` ostida saqlaydi.

## 36. 2. Oldindan talab qilinadiganlarni o‘rnating (VM’da)

```bash
37. sudo apt-get update
sudo apt-get install -y git curl jq ca-certificates openssl
```

## 38. 3. OpenClaw’ni o‘rnating

39. OpenClaw o‘rnatish skriptini ishga tushiring:

```bash
40. curl -fsSL https://openclaw.ai/install.sh | bash
```

## 41. 4. OpenClaw’ni 8000 portga proxy qilish uchun nginx’ni sozlang

42. `/etc/nginx/sites-enabled/default` faylini quyidagicha tahrirlang

```
43. server {
    listen 80 default_server;
    listen [::]:80 default_server;
    listen 8000;
    listen [::]:8000;

    server_name _;

    location / {
        proxy_pass http://127.0.0.1:18789;
        proxy_http_version 1.1;

        # WebSocket qo‘llab-quvvatlashi
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Standart proxy sarlavhalari
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Uzoq davom etuvchi ulanishlar uchun timeout sozlamalari
        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
    }
}
```

## 44. 5. OpenClaw’ga kiring va imtiyozlarni bering

45. `https://<vm-name>.exe.xyz/` manziliga kiring (onboarding paytidagi Control UI chiqishiga qarang). 46. Agar autentifikatsiya so‘ralsa, VM’dagi `gateway.auth.token` dan tokenni joylashtiring (`openclaw config get gateway.auth.token` bilan oling yoki `openclaw doctor --generate-gateway-token` bilan yarating). 47. Qurilmalarni `openclaw devices list` va `openclaw devices approve <requestId>` yordamida tasdiqlang. 48. Shubha tug‘ilganda, brauzeringizdan Shelley’dan foydalaning!

## 49. Masofaviy kirish

50. Masofaviy kirish [exe.dev](https://exe.dev) autentifikatsiyasi orqali boshqariladi. By
    default, HTTP traffic from port 8000 is forwarded to `https://<vm-name>.exe.xyz`
    with email auth.

## Updating

```bash
npm i -g openclaw@latest
openclaw doctor
openclaw gateway restart
openclaw health
```

Guide: [Updating](/install/updating)
