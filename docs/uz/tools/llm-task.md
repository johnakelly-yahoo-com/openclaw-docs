---
summary: "tizim promptida yoki sxemada ko‘rinmasa, model uni chaqira olmaydi."
read_when:
  - Ish oqimlari uchun faqat JSON’dan iborat LLM vazifalari (ixtiyoriy plagin vositasi)
  - Siz ish oqimlari ichida faqat JSON chiqaradigan LLM bosqichini xohlaysiz
title: "Avtomatlashtirish uchun sxema bilan tekshiriladigan LLM chiqishi kerak"
---

# LLM Vazifa

LLM Vazifa

`llm-task` — bu **ixtiyoriy plagin vositasi** bo‘lib, faqat JSON’dan iborat LLM vazifasini ishga tushiradi va tuzilgan chiqishni qaytaradi (ixtiyoriy ravishda JSON Schema bo‘yicha tekshiriladi).

## Bu Lobster kabi ish oqimi dvijoklari uchun juda qulay: har bir ish oqimi uchun maxsus OpenClaw kodi yozmasdan bitta LLM bosqichini qo‘shishingiz mumkin.

1. Plaginni yoqing

```json
Plaginni yoqing:
```

2. {
   "plugins": {
   "entries": {
   "llm-task": { "enabled": true }
   }
   }
   }

```json
Vosita uchun allowlist qo‘shing (u `optional: true` bilan ro‘yxatdan o‘tgan):
```

{
"agents": {
"list": [
{
"id": "main",
"tools": { "allow": ["llm-task"] }
}
]
}
}
-

```json
Sozlama (ixtiyoriy)
```

{
"plugins": {
"entries": {
"llm-task": {
"enabled": true,
"config": {
"defaultProvider": "openai-codex",
"defaultModel": "gpt-5.2",
"defaultAuthProfileId": "main",
"allowedModels": ["openai-codex/gpt-5.3-codex"],
"maxTokens": 800,
"timeoutMs": 30000
}
}
}
}
} Agar sozlangan bo‘lsa, ro‘yxatdan tashqaridagi har qanday so‘rov rad etiladi.

## Asbob parametrlari

- `prompt` (string, majburiy)
- `input` (any, ixtiyoriy)
- `schema` (object, ixtiyoriy JSON Schema)
- `provider` (string, ixtiyoriy)
- `model` (string, ixtiyoriy)
- `authProfileId` (string, ixtiyoriy)
- `temperature` (number, ixtiyoriy)
- `maxTokens` (number, ixtiyoriy)
- `timeoutMs` (number, ixtiyoriy)

## Chiqish

`details.json` qaytaradi, unda tahlil qilingan JSON mavjud (va agar berilgan bo‘lsa,
`schema` ga nisbatan tekshiradi).

## Misol: Lobster ish jarayoni qadami

```lobster
openclaw.invoke --tool llm-task --action json --args-json '{
  "prompt": "Given the input email, return intent and draft.",
  "input": {
    "subject": "Hello",
    "body": "Can you help?"
  },
  "schema": {
    "type": "object",
    "properties": {
      "intent": { "type": "string" },
      "draft": { "type": "string" }
    },
    "required": ["intent", "draft"],
    "additionalProperties": false
  }
}'
```

## Xavfsizlik eslatmalari

- Asbob **faqat JSON** uchun mo‘ljallangan va modelga faqat JSON chiqarishni buyuradi (kod bloklari yo‘q, izohlar yo‘q).
- Ushbu ishga tushirishda modelga hech qanday asboblar ochilmaydi.
- `schema` bilan tekshirmaguningizcha chiqishni ishonchsiz deb hisoblang.
- Har qanday yon ta’sirli qadamdan (yuborish, joylash, bajarish) oldin tasdiqlarni qo‘ying.
