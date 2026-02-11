---
summary: "`openclaw devices` uchun CLI ma’lumotnomasi (qurilmalarni juftlash + tokenlarni aylantirish/bekor qilish)"
read_when:
  - Siz qurilma juftlash so‘rovlarini tasdiqlayapsiz
  - Siz qurilma tokenlarini aylantirishingiz yoki bekor qilishingiz kerak
title: "qurilmalar"
---

# `openclaw devices`

Qurilma juftlash so‘rovlari va qurilmaga bog‘langan tokenlarni boshqarish.

## Buyruqlar

### `openclaw devices list`

Kutilayotgan juftlash so‘rovlari va juftlangan qurilmalar ro‘yxatini ko‘rsatadi.

```
openclaw devices list
openclaw devices list --json
```

### `openclaw devices approve <requestId>`

Kutilayotgan qurilma juftlash so‘rovini tasdiqlash.

```
openclaw devices approve <requestId>
```

### `openclaw devices reject <requestId>`

Kutilayotgan qurilma juftlash so‘rovini rad etish.

```
openclaw devices reject <requestId>
```

### `openclaw devices rotate --device <id> --role <role> [--scope <scope...>]`

Muayyan rol uchun qurilma tokenini aylantirish (ixtiyoriy ravishda scope’larni yangilab).

```
openclaw devices rotate --device <deviceId> --role operator --scope operator.read --scope operator.write
```

### `openclaw devices revoke --device <id> --role <role>`

Muayyan rol uchun qurilma tokenini bekor qilish.

```
openclaw devices revoke --device <deviceId> --role node
```

## Umumiy parametrlar

- `--url <url>`: Gateway WebSocket URL’i (sozlangan bo‘lsa, sukut bo‘yicha `gateway.remote.url`).
- `--token <token>`: Gateway tokeni (agar talab qilinsa).
- `--password <password>`: Gateway paroli (parol orqali autentifikatsiya).
- `--timeout <ms>`: RPC vaqt cheklovi.
- `--json`: JSON chiqishi (skriptlar uchun tavsiya etiladi).

Eslatma: `--url` ni o‘rnatganingizda, CLI konfiguratsiya yoki muhit o‘zgaruvchilaridagi hisob ma’lumotlariga qaytmaydi.
`--token` yoki `--password` ni aniq ko‘rsating. Aniq ko‘rsatilgan hisob ma’lumotlarining yo‘qligi xato hisoblanadi.

## Eslatmalar

- Tokenni aylantirish yangi tokenni qaytaradi (maxfiy). Uni sir kabi saqlang.
- Bu buyruqlar `operator.pairing` (yoki `operator.admin`) scope’ini talab qiladi.
