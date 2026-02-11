---
summary: "19. LINE Messaging API plagini: o‘rnatish, sozlash va foydalanish"
read_when:
  - 20. Siz OpenClaw’ni LINE’ga ulashni xohlaysiz
  - 21. Sizga LINE webhook va hisob ma’lumotlarini sozlash kerak
  - 22. Siz LINE’ga xos xabar opsiyalarini xohlaysiz
title: 23. LINE
---

# 24. LINE (plagin)

25. LINE OpenClaw’ga LINE Messaging API orqali ulanadi. 26. Plagin gateway’da webhook qabul qiluvchisi sifatida ishlaydi va
    autentifikatsiya uchun kanalga kirish tokeningiz + kanal maxfiy kalitingizdan foydalanadi.

27. Holati: plagin orqali qo‘llab-quvvatlanadi. 28. Shaxsiy xabarlar, guruh chatlari, media, joylashuvlar, Flex xabarlar,
    shablon xabarlar va tezkor javoblar qo‘llab-quvvatlanadi. 29. Reaksiyalar va thread’lar
    qo‘llab-quvvatlanmaydi.

## 30. Plagin talab qilinadi

31. LINE plaginini o‘rnating:

```bash
32. openclaw plugins install @openclaw/line
```

33. Lokal checkout (git repozitoriydan ishga tushirilganda):

```bash
34. openclaw plugins install ./extensions/line
```

## 35. Sozlash

1. 36. LINE Developers akkauntini yarating va Konsolni oching:
       [https://developers.line.biz/console/](https://developers.line.biz/console/)
2. 37. Provider yarating (yoki tanlang) va **Messaging API** kanalini qo‘shing.
3. 38. Kanal sozlamalaridan **Channel access token** va **Channel secret** ni nusxalab oling.
4. 39. Messaging API sozlamalarida **Use webhook** ni yoqing.
5. 40. Webhook URL’ni gateway endpoint’ingizga o‘rnating (HTTPS talab qilinadi):

```
41. https://gateway-host/line/webhook
```

42. Gateway LINE’ning webhook tekshiruviga (GET) va kiruvchi hodisalarga (POST) javob beradi.
43. Agar sizga maxsus yo‘l kerak bo‘lsa, `channels.line.webhookPath` yoki
    `channels.line.accounts.<id>` ni sozlang44. `.webhookPath` va URL’ni mos ravishda yangilang.

## 45. Sozlash

46. Minimal konfiguratsiya:

```json5
47. {
  channels: {
    line: {
      enabled: true,
      channelAccessToken: "LINE_CHANNEL_ACCESS_TOKEN",
      channelSecret: "LINE_CHANNEL_SECRET",
      dmPolicy: "pairing",
    },
  },
}
```

48. Muhit o‘zgaruvchilari (faqat standart akkaunt uchun):

- 49. `LINE_CHANNEL_ACCESS_TOKEN`
- 50. `LINE_CHANNEL_SECRET`

1. Token/maxfiy fayllar:

```json5
2. {
  channels: {
    line: {
      tokenFile: "/path/to/line-token.txt",
      secretFile: "/path/to/line-secret.txt",
    },
  },
}
```

3. Bir nechta akkauntlar:

```json5
4. {
  channels: {
    line: {
      accounts: {
        marketing: {
          channelAccessToken: "...",
          channelSecret: "...",
          webhookPath: "/line/marketing",
        },
      },
    },
  },
}
```

## 5. Kirishni boshqarish

6. To‘g‘ridan-to‘g‘ri xabarlar (DM) sukut bo‘yicha juftlashga o‘rnatilgan. 7. Noma’lum jo‘natuvchilarga juftlash kodi beriladi va ular tasdiqlanmaguncha xabarlari e’tiborsiz qoldiriladi.

```bash
8. openclaw pairing list line
openclaw pairing approve line <CODE>
```

9. Ruxsat etilgan ro‘yxatlar va siyosatlar:

- 10. `channels.line.dmPolicy`: `pairing | allowlist | open | disabled`
- 11. `channels.line.allowFrom`: DM uchun ruxsat etilgan LINE foydalanuvchi IDlari
- 12. `channels.line.groupPolicy`: `allowlist | open | disabled`
- 13. `channels.line.groupAllowFrom`: guruhlar uchun ruxsat etilgan LINE foydalanuvchi IDlari
- 14. Guruh bo‘yicha alohida sozlamalar: `channels.line.groups.<groupId>`15. `.allowFrom`

16. LINE IDlari katta-kichik harflarga sezgir. 17. Yaroqli IDlar quyidagicha ko‘rinadi:

- 18. Foydalanuvchi: `U` + 32 ta hex belgi
- 19. Guruh: `C` + 32 ta hex belgi
- 20. Xona: `R` + 32 ta hex belgi

## 21. Xabarlar xatti-harakati

- 22. Matn 5000 belgidan bo‘laklarga ajratiladi.
- 23. Markdown formatlash olib tashlanadi; kod bloklari va jadvallar imkon qadar Flex kartalarga aylantiriladi.
- 24. Oqimli javoblar buferlanadi; agent ishlayotgan paytda LINE to‘liq bo‘laklarni yuklanish animatsiyasi bilan qabul qiladi.
- 25. Media yuklab olishlar `channels.line.mediaMaxMb` bilan cheklanadi (sukut bo‘yicha 10).

## 26. Kanal ma’lumotlari (boy xabarlar)

27. Tezkor javoblar, joylashuvlar, Flex kartalar yoki shablon xabarlarni yuborish uchun `channelData.line` dan foydalaning.

```json5
28. {
  text: "Here you go",
  channelData: {
    line: {
      quickReplies: ["Status", "Help"],
      location: {
        title: "Office",
        address: "123 Main St",
        latitude: 35.681236,
        longitude: 139.767125,
      },
      flexMessage: {
        altText: "Status card",
        contents: {
          /* Flex payload */
        },
      },
      templateMessage: {
        type: "confirm",
        text: "Proceed?",
        confirmLabel: "Yes",
        confirmData: "yes",
        cancelLabel: "No",
        cancelData: "no",
      },
    },
  },
}
```

29. LINE plagini Flex xabarlar uchun tayyor sozlamalarga ega `/card` buyrug‘ini ham taqdim etadi:

```
30. /card info "Welcome" "Thanks for joining!"
```

## 31. Nosozliklarni bartaraf etish

- 32. **Webhook tekshiruvi muvaffaqiyatsiz:** webhook URL HTTPS ekanligiga va `channelSecret` LINE konsolidagi qiymatga mos kelishiga ishonch hosil qiling.
- 33. **Kirish hodisalari yo‘q:** webhook yo‘li `channels.line.webhookPath` ga mos kelishini va shlyuz LINE’dan yetib borilishi mumkinligini tasdiqlang.
- 34. **Media yuklab olish xatolari:** media sukut bo‘yicha limitdan oshsa, `channels.line.mediaMaxMb` ni oshiring.
