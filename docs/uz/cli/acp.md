---
summary: "49. IDE integratsiyalari uchun ACP bridge’ni ishga tushiring"
read_when:
  - 50. ACP-ga asoslangan IDE integratsiyalarini sozlash
  - Gateway’ga ACP sessiya marshrutlashini nosozliklardan tozalash
title: "acp"
---

# acp

OpenClaw Gateway bilan bog‘lanadigan ACP (Agent Client Protocol) ko‘prigini ishga tushiring.

Bu buyruq IDE’lar uchun stdio orqali ACP’da gaplashadi va so‘rovlarni WebSocket orqali Gateway’ga yo‘naltiradi. U ACP sessiyalarini Gateway sessiya kalitlariga moslab turadi.

## Foydalanish

```bash
openclaw acp

# Masofaviy Gateway
openclaw acp --url wss://gateway-host:18789 --token <token>

# Mavjud sessiya kalitiga ulanmoq
openclaw acp --session agent:main:main

# Yorliq bo‘yicha ulanish (oldindan mavjud bo‘lishi kerak)
openclaw acp --session-label "support inbox"

# Birinchi so‘rovdan oldin sessiya kalitini tiklash
openclaw acp --session agent:main:main --reset-session
```

## ACP mijozi (debug)

IDE’siz ko‘prikni tekshirish uchun ichki ACP mijozidan foydalaning.
U ACP ko‘prigini ishga tushiradi va so‘rovlarni interaktiv tarzda kiritishga imkon beradi.

```bash
openclaw acp client

# Ishga tushirilgan ko‘prikni masofaviy Gateway’ga yo‘naltirish
openclaw acp client --server-args --url wss://gateway-host:18789 --token <token>

# Server buyrug‘ini almashtirish (standart: openclaw)
openclaw acp client --server "node" --server-args openclaw.mjs acp --url ws://127.0.0.1:19001
```

## Bundan qanday foydalanish

IDE (yoki boshqa mijoz) Agent Client Protocol’da gaplashganda va u OpenClaw Gateway sessiyasini boshqarishini xohlaganingizda ACP’dan foydalaning.

1. Gateway ishga tushirilganligiga ishonch hosil qiling (lokal yoki masofaviy).
2. Gateway nishonini sozlang (konfiguratsiya yoki flaglar orqali).
3. IDE’ngizni stdio orqali `openclaw acp` ni ishga tushirishga yo‘naltiring.

Misol konfiguratsiya (saqlanadi):openclaw config set gateway.remote.url wss://gateway-host:18789
openclaw config set gateway.remote.token <token>

```bash
To‘g‘ridan-to‘g‘ri ishga tushirish misoli (konfiguratsiya yozilmaydi):

openclaw acp --url wss://gateway-host:18789 --token <token>
```

Agentlarni tanlash

```bash
ACP agentlarni to‘g‘ridan-to‘g‘ri tanlamaydi.
```

## U Gateway sessiya kaliti orqali marshrutlaydi.

Muayyan agentni nishonga olish uchun agent doirasidagi sessiya kalitlaridan foydalaning:openclaw acp --session agent:main:main
openclaw acp --session agent:design:main
openclaw acp --session agent:qa:bug-123 Har bir ACP sessiyasi bitta Gateway sessiya kalitiga mos keladi.

Bitta agentda ko‘plab sessiyalar bo‘lishi mumkin; ACP standart holatda ajratilgan `acp:<uuid>` sessiyasidan foydalanadi, agar siz kalit yoki yorliqni almashtirmasangiz.

```bash
Zed muharriri sozlamalari
```

`~/.config/zed/settings.json` fayliga maxsus ACP agent qo‘shing (yoki Zed’ning Settings UI’dan foydalaning):{
"agent_servers": {
"OpenClaw ACP": {
"type": "custom",
"command": "openclaw",
"args": ["acp"],
"env": {}
}
}
} Muayyan Gateway yoki agentni nishonga olish uchun:{
"agent_servers": {
"OpenClaw ACP": {
"type": "custom",
"command": "openclaw",
"args": [
"acp",
"--url",
"wss://gateway-host:18789",
"--token",
"<token>",
"--session",
"agent:design:main"
],
"env": {}
}
}
}

## Zed’da Agent panelini oching va oqimni boshlash uchun “OpenClaw ACP” ni tanlang.

Sessiyalarni moslash

```json
Standart holatda ACP sessiyalari `acp:` prefiksi bilan ajratilgan Gateway sessiya kalitini oladi.
```

Ma’lum sessiyani qayta ishlatish uchun sessiya kaliti yoki yorliqni uzating:

```json
`--session <key>`: muayyan Gateway sessiya kalitidan foydalanish.
```

`--session-label <label>`: mavjud sessiyani yorliq orqali aniqlash.

## `--reset-session`: shu kalit uchun yangi sessiya identifikatorini yaratish (bir xil kalit, yangi transkript).

Agar ACP mijozingiz metadata’ni qo‘llab-quvvatlasa, har bir sessiya uchun alohida sozlashingiz mumkin:{
"_meta": {
"sessionKey": "agent:main:main",
"sessionLabel": "support inbox",
"resetSession": true
}
}
Sessiya kalitlari haqida batafsil ma’lumotni [/concepts/session](/concepts/session) sahifasida o‘rganing.

- Variantlar
- `--url <url>`: Gateway WebSocket URL’i (sozlangan bo‘lsa, gateway.remote.url standart bo‘ladi).
- `--token <token>`: Gateway autentifikatsiya tokeni.

`--password <password>`: Gateway autentifikatsiya paroli.

```json
`--session <key>`: standart sessiya kaliti.
```

`--session-label <label>`: aniqlash uchun standart sessiya yorlig‘i.

## `--require-existing`: agar sessiya kaliti/yorlig‘i mavjud bo‘lmasa, xatolik bilan to‘xtaydi.

- `--url <url>`: Gateway WebSocket URL (defaults to gateway.remote.url when configured).
- `--token <token>`: Gateway auth token.
- `--password <password>`: Gateway auth password.
- `--session <key>`: default session key.
- `--session-label <label>`: default session label to resolve.
- `--require-existing`: fail if the session key/label does not exist.
- `--reset-session`: birinchi foydalanishdan oldin sessiya kalitini qayta o‘rnatadi.
- `--no-prefix-cwd`: so‘rovlarni ishchi katalog bilan prefikslashni o‘chiradi.
- `--verbose, -v`: stderr ga batafsil loglash.

### `acp client` parametrlari

- `--cwd <dir>`: ACP sessiyasi uchun ishchi katalog.
- `--server <command>`: ACP server buyrug‘i (standart: `openclaw`).
- `--server-args <args...>`: ACP serveriga uzatiladigan qo‘shimcha argumentlar.
- `--server-verbose`: ACP serverida batafsil loglashni yoqadi.
- `--verbose, -v`: mijoz tomoni uchun batafsil loglash.
