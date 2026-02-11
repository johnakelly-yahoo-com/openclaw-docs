---
summary: "37. OpenClaw’da ko‘plab modellarga kirish uchun Qianfan’ning yagona API’sidan foydalaning"
read_when:
  - 38. Ko‘plab LLM’lar uchun bitta API kalitini xohlaysiz
  - 39. Baidu Qianfan sozlash bo‘yicha yo‘riqnoma kerak
title: "40. Qianfan"
---

# 41. Qianfan provayder qo‘llanmasi

42. Qianfan — Baidu’ning MaaS platformasi bo‘lib, **yagona API** taqdim etadi va bitta
    endpoint hamda API kaliti ortida ko‘plab modellarga so‘rovlarni yo‘naltiradi. 43. U OpenAI bilan mos keladi, shuning uchun ko‘pchilik OpenAI SDK’lari bazaviy URL’ni almashtirish orqali ishlaydi.

## 44. Talablar

1. 45. Qianfan API’ga kirish huquqiga ega Baidu Cloud hisobi
2. 46. Qianfan konsolidan olingan API kaliti
3. 47. Tizimingizda OpenClaw o‘rnatilgan

## 48) API kalitingizni olish

1. 49. [Qianfan Console](https://console.bce.baidu.com/qianfan/ais/console/apiKey) sahifasiga tashrif buyuring
2. 50. Yangi ilova yarating yoki mavjudini tanlang
3. API kalitini yarating (format: `bce-v3/ALTAK-...`)
4. OpenClaw bilan foydalanish uchun API kalitini nusxalab oling

## CLI sozlamalari

```bash
openclaw onboard --auth-choice qianfan-api-key
```

## Tegishli hujjatlar

- [OpenClaw konfiguratsiyasi](/gateway/configuration)
- [Model provayderlari](/concepts/model-providers)
- [Agent sozlamalari](/concepts/agent)
- [Qianfan API hujjatlari](https://cloud.baidu.com/doc/qianfan-api/s/3m7of64lb)
