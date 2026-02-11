---
summary: "4. apply_patch vositasi bilan ko‘p faylli patchlarni qo‘llash"
read_when:
  - Sizga bir nechta fayl bo‘ylab tuzilgan tahrirlar kerak
  - 5. Patch-ga asoslangan tahrirlarni hujjatlashtirmoqchi yoki nosozliklarni tuzatmoqchisiz
title: "6. apply_patch Vositasi"
---

# apply_patch vositasi

Fayl o‘zgarishlarini tuzilgan patch formatidan foydalanib qo‘llash. Bu bir nechta fayl yoki
bir nechta hunk tahrirlari uchun ideal, chunki bitta `edit` chaqiruvi beqaror bo‘lishi mumkin.

Vosita bitta `input` satrini qabul qiladi, u bir yoki bir nechta fayl amallarini o‘rab oladi:

```
*** Begin Patch
*** Add File: path/to/file.txt
+line 1
+line 2
*** Update File: src/app.ts
@@
-old line
+new line
*** Delete File: obsolete.txt
*** End Patch
```

## Parametrlar

- `input` (majburiy): `*** Begin Patch` va `*** End Patch` ni o‘z ichiga olgan to‘liq patch mazmuni.

## Eslatmalar

- Yo‘llar workspace ildiziga nisbatan aniqlanadi.
- `*** Update File:` hunk ichida fayllarni qayta nomlash uchun `*** Move to:` dan foydalaning.
- Kerak bo‘lganda faqat EOF qo‘shishni belgilash uchun `*** End of File` ishlatiladi.
- Eksperimental va sukut bo‘yicha o‘chirilgan. `tools.exec.applyPatch.enabled` bilan yoqing.
- Faqat OpenAI uchun (OpenAI Codex’ni ham o‘z ichiga oladi). Ixtiyoriy ravishda model bo‘yicha cheklash:
  `tools.exec.applyPatch.allowModels`.
- Konfiguratsiya faqat `tools.exec` ostida joylashgan.

## Misol

```json
{
  "tool": "apply_patch",
  "input": "*** Begin Patch\n*** Update File: src/index.ts\n@@\n-const foo = 1\n+const foo = 2\n*** End Patch"
}
```
