---
summary: "31. Bonjour/mDNS aniqlash + nosozliklarni tuzatish (Gateway mayaklari, mijozlar va keng tarqalgan nosozlik holatlari)"
read_when:
  - 32. macOS/iOS da Bonjour aniqlash muammolarini tuzatish
  - 33. mDNS xizmat turlarini, TXT yozuvlarini yoki aniqlash UX’ini o‘zgartirish
title: "34. Bonjour aniqlash"
---

# 35. Bonjour / mDNS aniqlash

36. OpenClaw faol Gateway (WebSocket endpoint) ni aniqlash uchun **faqat LAN doirasidagi qulaylik** sifatida Bonjour (mDNS / DNS‑SD) dan foydalanadi. 37. Bu best‑effort bo‘lib, SSH yoki Tailnet asosidagi ulanishni **almashtirmaydi**.

## 38. Tailscale orqali keng hududli Bonjour (Unicast DNS‑SD)

39. Agar tugun va gateway turli tarmoqlarda bo‘lsa, multicast mDNS chegaradan o‘tmaydi. 40. Tailscale orqali **unicast DNS‑SD** ("Wide‑Area Bonjour") ga o‘tib, xuddi shu aniqlash UX’ini saqlab qolishingiz mumkin.

41. Yuqori darajadagi qadamlar:

1. 42. Gateway xostida DNS serverni ishga tushiring (Tailnet orqali yetib boriladigan).
2. 43. Ajratilgan zona ostida `_openclaw-gw._tcp` uchun DNS‑SD yozuvlarini e’lon qiling
       (misol: `openclaw.internal.`).
3. 44. Tanlangan domeningiz mijozlar (jumladan iOS) uchun o‘sha DNS server orqali yechilishi uchun Tailscale **split DNS** ni sozlang.

45) OpenClaw istalgan aniqlash domenini qo‘llab-quvvatlaydi; `openclaw.internal.` faqat misol.
46) iOS/Android tugunlari `local.` va siz sozlagan keng hududli domenni birgalikda ko‘rib chiqadi.

### 47. Gateway konfiguratsiyasi (tavsiya etiladi)

```json5
48. {
  gateway: { bind: "tailnet" }, // faqat tailnet (tavsiya etiladi)
  discovery: { wideArea: { enabled: true } }, // keng hududli DNS‑SD e’lon qilishni yoqadi
}
```

### 49. Bir martalik DNS server sozlamasi (gateway xosti)

```bash
50. openclaw dns setup --apply
```

1. Bu CoreDNS’ni o‘rnatadi va uni quyidagicha sozlaydi:

- 2. 53‑portda faqat gateway’ning Tailscale interfeyslarida tinglaydi
- 3. tanlangan domeningizni (misol: `openclaw.internal.`) `~/.openclaw/dns/<domain>.db` dan xizmat qiladi

4. Tailnet’ga ulangan mashinadan tekshiring:

```bash
5. dns-sd -B _openclaw-gw._tcp openclaw.internal.
dig @<TAILNET_IPV4> -p 53 _openclaw-gw._tcp.openclaw.internal PTR +short
```

### 6. Tailscale DNS sozlamalari

7. Tailscale admin konsolida:

- 8. Gateway’ning tailnet IP manziliga (UDP/TCP 53) yo‘naltirilgan nameserver qo‘shing.
- 9. Discovery domeningiz shu nameserver’dan foydalanishi uchun split DNS qo‘shing.

10. Mijozlar tailnet DNS’ni qabul qilgach, iOS tugunlari multicast’siz discovery domeningizda
    `_openclaw-gw._tcp` ni ko‘ra oladi.

### 11. Gateway tinglovchi xavfsizligi (tavsiya etiladi)

12. Gateway WS porti (standart `18789`) sukut bo‘yicha loopback’ga bog‘lanadi. 13. LAN/tailnet
    kirish uchun, aniq bog‘lang va autentifikatsiyani yoqilgan holda qoldiring.

14. Faqat tailnet sozlamalari uchun:

- 15. `~/.openclaw/openclaw.json` faylida `gateway.bind: "tailnet"` ni o‘rnating.
- 16. Gateway’ni qayta ishga tushiring (yoki macOS menyubar ilovasini qayta ishga tushiring).

## 17. Nimalar e’lon qilinadi

18. Faqat Gateway `_openclaw-gw._tcp` ni e’lon qiladi.

## 19. Xizmat turlari

- 20. `_openclaw-gw._tcp` — gateway transport beacon (macOS/iOS/Android tugunlari tomonidan ishlatiladi).

## 21. TXT kalitlari (maxfiy bo‘lmagan ishoralar)

22. Gateway UI jarayonlarini qulay qilish uchun kichik, maxfiy bo‘lmagan ishoralarni e’lon qiladi:

- 23. `role=gateway`
- 24. `displayName=<friendly name>`
- 25. `lanHost=<hostname>.local`
- 26. `gatewayPort=<port>` (Gateway WS + HTTP)
- 27. `gatewayTls=1` (faqat TLS yoqilganida)
- 28. `gatewayTlsSha256=<sha256>` (faqat TLS yoqilgan va fingerprint mavjud bo‘lganda)
- 29. `canvasPort=<port>` (faqat canvas xosti yoqilganda; standart `18793`)
- 30. `sshPort=<port>` (o‘zgartirilmagan bo‘lsa, sukut bo‘yicha 22)
- 31. `transport=gateway`
- 32. `cliPath=<path>` (ixtiyoriy; ishga tushiriladigan `openclaw` kirish nuqtasiga mutlaq yo‘l)
- 33. `tailnetDns=<magicdns>` (Tailnet mavjud bo‘lganda ixtiyoriy ishora)

## 34. macOS’da nosozliklarni tuzatish

35. Foydali o‘rnatilgan vositalar:

- 36. Instansiyalarni ko‘rish:

  ```bash
  37. dns-sd -B _openclaw-gw._tcp local.
  ```

- 38. Bitta instansiyani aniqlash ( `<instance>` ni almashtiring):

  ```bash
  39. dns-sd -L "<instance>" _openclaw-gw._tcp local.
  ```

40. Agar ko‘rish ishlasa, lekin aniqlash ishlamasa, odatda LAN siyosati yoki
    mDNS rezolver muammosiga duch kelasiz.

## 41. Gateway loglarida nosozliklarni tuzatish

42. Gateway aylanuvchi log faylini yozadi (ishga tushishda quyidagicha chop etiladi:
    `gateway log file: ...`). 43. Ayniqsa `bonjour:` qatorlariga e’tibor bering:

- 44. `bonjour: advertise failed ...`
- 45. \`bonjour: ...
  46. name conflict resolved`/`hostname conflict resolved`47.`bonjour: watchdog detected non-announced service ...\`
- 48. iOS tugunida nosozliklarni tuzatish

## 49. iOS tuguni `_openclaw-gw._tcp` ni aniqlash uchun `NWBrowser` dan foydalanadi.

50. Loglarni olish uchun:

To capture logs:

- Settings → Gateway → Advanced → **Discovery Debug Logs**
- Settings → Gateway → Advanced → **Discovery Logs** → reproduce → **Copy**

The log includes browser state transitions and result‑set changes.

## Common failure modes

- **Bonjour doesn’t cross networks**: use Tailnet or SSH.
- `workdir`, `env`
- **Sleep / interface churn**: macOS may temporarily drop mDNS results; retry.
- **Browse works but resolve fails**: keep machine names simple (avoid emojis or
  punctuation), then restart the Gateway. The service instance name derives from
  the host name, so overly complex names can confuse some resolvers.

## Escaped instance names (`\032`)

Bonjour/DNS‑SD often escapes bytes in service instance names as decimal `\DDD`
sequences (e.g. spaces become `\032`).

- This is normal at the protocol level.
- **Multicast bloklangan**: ba’zi Wi‑Fi tarmoqlari mDNS’ni o‘chirib qo‘yadi.

## Disabling / configuration

- `OPENCLAW_DISABLE_BONJOUR=1` disables advertising (legacy: `OPENCLAW_DISABLE_BONJOUR`).
- `gateway.bind` in `~/.openclaw/openclaw.json` controls the Gateway bind mode.
- `OPENCLAW_SSH_PORT` overrides the SSH port advertised in TXT (legacy: `OPENCLAW_SSH_PORT`).
- `OPENCLAW_TAILNET_DNS` publishes a MagicDNS hint in TXT (legacy: `OPENCLAW_TAILNET_DNS`).
- `OPENCLAW_CLI_PATH` overrides the advertised CLI path (legacy: `OPENCLAW_CLI_PATH`).

## Related docs

- Discovery policy and transport selection: [Discovery](/gateway/discovery)
- Node pairing + approvals: [Gateway pairing](/gateway/pairing)
