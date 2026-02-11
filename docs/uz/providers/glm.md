---
summary: "41. GLM model oilasiga umumiy ko‘rinish va uni OpenClaw’da qanday ishlatish"
read_when:
  - 42. Siz OpenClaw’da GLM modellardan foydalanmoqchisiz
  - 43. Sizga model nomlash konvensiyasi va sozlash kerak
title: "44. GLM modellari"
---

# 45. GLM modellari

46. GLM — bu **model oilasi** (kompaniya emas) bo‘lib, Z.AI platformasi orqali taqdim etiladi. 47. OpenClaw’da GLM modellarga `zai` provayderi va `zai/glm-4.7` kabi model ID’lari orqali kiriladi.

## 48. CLI sozlash

```bash
49. openclaw onboard --auth-choice zai-api-key
```

## 50. Konfiguratsiya parchasi

```json5
{
  env: { ZAI_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "zai/glm-4.7" } } },
}
```

## Eslatmalar

- GLM versiyalari va mavjudligi o‘zgarishi mumkin; eng so‘nggi ma’lumotlar uchun Z.AI hujjatlarini tekshiring.
- Model ID’lariga `glm-4.7` va `glm-4.6` misol bo‘la oladi.
- Provayder tafsilotlari uchun [/providers/zai](/providers/zai) sahifasiga qarang.
