---
summary: "6. OpenClaw bilan OpenCode Zen’dan foydalaning"
read_when:
  - 7. Modelga kirish uchun OpenCode Zen’ni xohlaysiz
  - 8. Kodlashga qulay modellar ro‘yxatini xohlaysiz
title: "9. OpenCode Zen"
---

# 10. OpenCode Zen

11. OpenCode Zen — bu OpenCode jamoasi tomonidan kodlash agentlari uchun tavsiya etilgan **saralangan modellar ro‘yxati**.
12. Bu API kalitidan va `opencode` provayderidan foydalanadigan ixtiyoriy, xostlangan modelga kirish yo‘lidir.
13. Zen hozirda beta bosqichida.

## 14. CLI sozlash

```bash
openclaw onboard --auth-choice opencode-zen
# or non-interactive
openclaw onboard --opencode-zen-api-key "$OPENCODE_API_KEY"
```

## 16. Konfiguratsiya parchasi

```json5
{
  env: { OPENCODE_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "opencode/claude-opus-4-6" } } },
}
```

## 18. Eslatmalar

- 19. `OPENCODE_ZEN_API_KEY` ham qo‘llab-quvvatlanadi.
- 20. Siz Zen’ga tizimga kirasiz, billing ma’lumotlarini qo‘shasiz va API kalitingizni nusxalaysiz.
- 21. OpenCode Zen har bir so‘rov bo‘yicha hisob-kitob qiladi; tafsilotlar uchun OpenCode boshqaruv panelini tekshiring.
