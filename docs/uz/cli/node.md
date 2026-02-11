---
summary: "`openclaw node` uchun CLI ma’lumotnomasi (headless node host)"
read_when:
  - Headless node hostni ishga tushirish
  - system.run uchun macOS bo‘lmagan nodeni juftlash
title: "node"
---

# `openclaw node`

Gateway WebSocket’iga ulanadigan va ushbu mashinada `system.run` / `system.which` ni taqdim etadigan **headless node host** ni ishga tushiring.

## Nega node host’dan foydalanish kerak?

Tarmog‘ingizdagi **boshqa mashinalarda buyruqlarni bajarish** uchun, u yerlarga to‘liq macOS hamroh ilovasini o‘rnatmasdan, node host’dan foydalaning.

Keng tarqalgan foydalanish holatlari:

- Masofadagi Linux/Windows mashinalarida buyruqlarni bajarish (build serverlar, laboratoriya mashinalari, NAS).
- Gateway’da exec’ni **sandbox** holatda saqlang, lekin tasdiqlangan bajarishlarni boshqa xostlarga topshiring.
- Bajarish hali ham **exec tasdiqlari** va tugun xostidagi har bir agent uchun ruxsat etilgan ro‘yxatlar bilan himoyalangan, shuning uchun buyruqlarga kirishni aniq va cheklangan holda saqlashingiz mumkin.

Brauzer proksi (nol konfiguratsiya)

## Agar tugunda `browser.enabled` o‘chirilmagan bo‘lsa, tugun xostlari avtomatik ravishda brauzer proksini e’lon qiladi.

Bu agentga qo‘shimcha sozlamalarsiz shu tugunda brauzer avtomatlashtirishdan foydalanish imkonini beradi. Agar kerak bo‘lsa, tugunda o‘chiring:

{
nodeHost: {
browserProxy: {
enabled: false,
},
},
}

```json5
Ishga tushirish (oldingi rejim)
```

## openclaw node run --host <gateway-host> --port 18789

```bash
Variantlar:
```

`--host <host>`: Gateway WebSocket xosti (standart: `127.0.0.1`)

- `--port <port>`: Gateway WebSocket porti (standart: `18789`)
- `--tls`: Gateway ulanishi uchun TLS dan foydalanish
- `--tls-fingerprint <sha256>`: Kutilayotgan TLS sertifikat barmoq izi (sha256)
- `--node-id <id>`: Tugun identifikatorini almashtirish (juftlash tokenini tozalaydi)
- `--display-name <name>`: Tugun ko‘rinadigan nomini almashtirish
- Xizmat (orqa fonda)

## Foydalanuvchi xizmati sifatida headless tugun xostini o‘rnating.

openclaw node install --host <gateway-host> --port 18789

```bash
Variantlar:
```

`--host <host>`: Gateway WebSocket xosti (standart: `127.0.0.1`)

- `--port <port>`: Gateway WebSocket porti (standart: `18789`)
- `--tls`: Gateway ulanishi uchun TLS dan foydalanish
- `--tls-fingerprint <sha256>`: Kutilayotgan TLS sertifikat barmoq izi (sha256)
- `--node-id <id>`: Tugun identifikatorini almashtirish (juftlash tokenini tozalaydi)
- `--display-name <name>`: Tugun ko‘rinadigan nomini almashtirish
- `--runtime <runtime>`: Xizmat muhiti (`node` yoki `bun`)
- `--force`: Agar allaqachon o‘rnatilgan bo‘lsa, qayta o‘rnatish/ustiga yozish
- Xizmatni boshqarish:

openclaw node status
openclaw node stop
openclaw node restart
openclaw node uninstall

```bash
Oldingi rejimdagi tugun xosti (xizmatsiz) uchun `openclaw node run` dan foydalaning.
```

Xizmat buyruqlari mashina o‘qiy oladigan chiqish uchun `--json` ni qabul qiladi.

Juftlash

## Birinchi ulanish Gateway’da kutilayotgan tugun juftlash so‘rovini yaratadi.

Uni quyidagilar orqali tasdiqlang:
openclaw nodes pending
openclaw nodes approve <requestId>

```bash
Tugun xosti o‘zining tugun identifikatori, tokeni, ko‘rinadigan nomi va gateway ulanish ma’lumotlarini `~/.openclaw/node.json` da saqlaydi.
```

Exec tasdiqlari

## `system.run` mahalliy exec tasdiqlari bilan cheklanadi:

`~/.openclaw/exec-approvals.json`

- [Exec tasdiqlari](/tools/exec-approvals)
- `openclaw approvals --node <id|name|ip>` (Gateway’dan tahrirlash)
- `openclaw nodes` uchun CLI ma’lumotnomasi (ro‘yxat/holat/tasdiqlash/chaqirish, kamera/canvas/ekran)
