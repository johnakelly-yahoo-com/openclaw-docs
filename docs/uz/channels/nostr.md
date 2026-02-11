---
summary: "NIP-04 shifrlangan xabarlar orqali Nostr DM kanali"
read_when:
  - Siz OpenClaw’ning Nostr orqali DMlarni qabul qilishini xohlaysiz
  - Siz markazlashmagan xabar almashishni sozlayapsiz
title: "Nostr"
---

# Nostr

**Holat:** Ixtiyoriy plagin (standart bo‘yicha o‘chirilgan).

Nostr — ijtimoiy tarmoqlar uchun markazlashmagan protokol. Bu kanal OpenClaw’ga NIP-04 orqali shifrlangan to‘g‘ridan-to‘g‘ri xabarlarni (DM) qabul qilish va ularga javob berish imkonini beradi.

## O‘rnatish (talab bo‘yicha)

### Boshlang‘ich sozlash (tavsiya etiladi)

- Boshlang‘ich sozlash ustasi (`openclaw onboard`) va `openclaw channels add` ixtiyoriy kanal plaginlarini ro‘yxatlaydi.
- Nostr’ni tanlash plaginni talab bo‘yicha o‘rnatishni taklif qiladi.

Install defaults:

- **Dev kanali + git checkout mavjud:** lokal plagin yo‘lidan foydalanadi.
- **Stable/Beta:** npm’dan yuklab oladi.

Tanlovni so‘rov oynasida har doim o‘zgartirishingiz mumkin.

### Qo‘lda o‘rnatish

```bash
openclaw plugins install @openclaw/nostr
```

Lokal checkout’dan foydalanish (dev ish jarayonlari):

```bash
openclaw plugins install --link <path-to-openclaw>/extensions/nostr
```

Plaginlarni o‘rnatgandan yoki yoqgandan so‘ng Gateway’ni qayta ishga tushiring.

## Tezkor sozlash

1. Nostr kalit juftligini yarating (agar kerak bo‘lsa):

```bash
# Using nak
nak key generate
```

2. Konfiguratsiyaga qo‘shing:

```json
{
  "channels": {
    "nostr": {
      "privateKey": "${NOSTR_PRIVATE_KEY}"
    }
  }
}
```

3. Kalitni eksport qiling:

```bash
export NOSTR_PRIVATE_KEY="nsec1..."
```

4. Gateway’ni qayta ishga tushiring.

## Konfiguratsiya ma’lumotnomasi

| Kalit        | Turi                                                         | Standart                                                                                                                                                                      | Tavsif                                        |
| ------------ | ------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| `privateKey` | string                                                       | majburiy                                                                                                                                                                      | `nsec` yoki hex formatdagi maxfiy kalit       |
| `relays`     | string[] | ['wss://relay.damus.io', 'wss://nos.lol'] | Relay URL’lari (WebSocket) |
| `dmPolicy`   | string                                                       | `pairing`                                                                                                                                                                     | DM kirish siyosati                            |
| `allowFrom`  | string[] | `[]`                                                                                                                                                                          | Ruxsat etilgan yuboruvchi pubkey’lari         |
| `enabled`    | boolean                                                      | `true`                                                                                                                                                                        | Kanalni yoqish/o‘chirish                      |
| `name`       | string                                                       | -                                                                                                                                                                             | Ko‘rsatiladigan nom                           |
| `profile`    | obyekt                                                       | -                                                                                                                                                                             | NIP-01 profil metamaʼlumotlari                |

## Profil metamaʼlumotlari

Profil maʼlumotlari NIP-01 `kind:0` hodisasi sifatida eʼlon qilinadi. Uni Boshqaruv UI orqali (Channels -> Nostr -> Profile) boshqarishingiz yoki to‘g‘ridan-to‘g‘ri konfiguratsiyada o‘rnatishingiz mumkin.

Misol:

```json
{
  "channels": {
    "nostr": {
      "privateKey": "${NOSTR_PRIVATE_KEY}",
      "profile": {
        "name": "openclaw",
        "displayName": "OpenClaw",
        "about": "Personal assistant DM bot",
        "picture": "https://example.com/avatar.png",
        "banner": "https://example.com/banner.png",
        "website": "https://example.com",
        "nip05": "openclaw@example.com",
        "lud16": "openclaw@example.com"
      }
    }
  }
}
```

Eslatmalar:

- Profil URL’lari `https://` dan foydalanishi kerak.
- Relaylardan import qilish maydonlarni birlashtiradi va lokal ustuvor sozlamalarni saqlab qoladi.

## Kirishni boshqarish

### DM siyosatlari

- **pairing** (standart): nomaʼlum yuboruvchilar juftlash kodi oladi.
- **allowlist**: faqat `allowFrom` dagi pubkey’lar DM yubora oladi.
- **open**: ommaviy kiruvchi DM’lar (`allowFrom: ["*"]` talab etiladi).
- **disabled**: kiruvchi DM’larni eʼtiborsiz qoldirish.

### Allowlist misoli

```json
{
  "channels": {
    "nostr": {
      "privateKey": "${NOSTR_PRIVATE_KEY}",
      "dmPolicy": "allowlist",
      "allowFrom": ["npub1abc...", "npub1xyz..."]
    }
  }
}
```

## Kalit formatlari

Qabul qilinadigan formatlar:

- **Maxfiy kalit:** `nsec...` yoki 64 belgili hex
- **Pubkey’lar (`allowFrom`):** `npub...` yoki hex

## Relaylar

Standartlar: `relay.damus.io` va `nos.lol`.

```json
{
  "channels": {
    "nostr": {
      "privateKey": "${NOSTR_PRIVATE_KEY}",
      "relays": ["wss://relay.damus.io", "wss://relay.primal.net", "wss://nostr.wine"]
    }
  }
}
```

Maslahatlar:

- Zaxira uchun 2–3 ta relaydan foydalaning.
- Juda ko‘p relaylardan qoching (kechikish, takrorlanish).
- Pullik relaylar ishonchlilikni oshirishi mumkin.
- Mahalliy relaylar test qilish uchun mos (`ws://localhost:7777`).

## Protokol qo‘llab-quvvatlashi

| NIP    | Holat                | Tavsif                                           |
| ------ | -------------------- | ------------------------------------------------ |
| NIP-01 | Qo‘llab-quvvatlanadi | Asosiy hodisa formati + profil metamaʼlumotlari  |
| NIP-04 | Qo‘llab-quvvatlanadi | Shifrlangan DM’lar (`kind:4`) |
| NIP-17 | Rejalashtirilgan     | Sovg‘a o‘ramli DM’lar                            |
| NIP-44 | Rejalashtirilgan     | Versiyalangan shifrlash                          |

## Sinov

### 1. Mahalliy relay

```bash
2. # strfry ni ishga tushirish
docker run -p 7777:7777 ghcr.io/hoytech/strfry
```

```json
3. {
  "channels": {
    "nostr": {
      "privateKey": "${NOSTR_PRIVATE_KEY}",
      "relays": ["ws://localhost:7777"]
    }
  }
}
```

### 4. Qo‘lda test

1. 5. Loglardan bot pubkey (npub) ni qayd eting.
2. 6. Nostr mijozini oching (Damus, Amethyst va boshqalar).
3. 7. Bot pubkey ga DM yuboring.
4. 8. Javobni tekshiring.

## 9) Muammolarni bartaraf etish

### 10. Xabarlar olinmayapti

- 11. Maxfiy kalitning yaroqli ekanini tekshiring.
- 12. Relay URL manzillari yetib borilishini va `wss://` (yoki mahalliy uchun `ws://`) ishlatilayotganini ta’minlang.
- 13. `enabled` qiymati `false` emasligini tasdiqlang.
- 14. Relay ulanish xatolari uchun Gateway loglarini tekshiring.

### 15. Javoblar yuborilmayapti

- 16. Relay yozuvlarni qabul qilishini tekshiring.
- 17. Chiqish aloqasi mavjudligini tasdiqlang.
- 18. Relay rate limitlariga e’tibor bering.

### 19. Takroriy javoblar

- 20. Bir nechta relay ishlatilganda kutiladi.
- 21. Xabarlar event ID bo‘yicha deduplikatsiya qilinadi; faqat birinchi yetkazib berish javobni ishga tushiradi.

## 22. Xavfsizlik

- 23. Hech qachon maxfiy kalitlarni commit qilmang.
- 24. Kalitlar uchun muhit o‘zgaruvchilaridan foydalaning.
- 25. Ishlab chiqarish botlari uchun `allowlist` ni ko‘rib chiqing.

## 26. Cheklovlar (MVP)

- 27. Faqat to‘g‘ridan-to‘g‘ri xabarlar (guruh chatlari yo‘q).
- 28. Media biriktirmalari yo‘q.
- 29. Faqat NIP-04 (NIP-17 gift-wrap rejalashtirilgan).
