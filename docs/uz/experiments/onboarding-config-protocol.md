---
summary: "Onboarding ustasi va konfiguratsiya sxemasi uchun RPC protokoli eslatmalari"
read_when: "Onboarding ustasi qadamlarini yoki konfiguratsiya sxemasi endpointlarini o‘zgartirish"
title: "Onboarding va Konfiguratsiya Protokoli"
---

# Onboarding + Konfiguratsiya Protokoli

Maqsad: CLI, macOS ilovasi va Web UI bo‘ylab umumiy onboarding + konfiguratsiya interfeyslarini ta’minlash.

## Komponentlar

- Usta dvigateli (umumiy sessiya + so‘rovlar + onboarding holati).
- CLI onboarding UI mijozlari bilan bir xil usta oqimidan foydalanadi.
- Gateway RPC usta + konfiguratsiya sxemasi endpointlarini taqdim etadi.
- macOS onboarding usta qadamlar modelidan foydalanadi.
- Web UI konfiguratsiya shakllarini JSON Schema + UI ko‘rsatmalaridan render qiladi.

## Gateway RPC

- `wizard.start` parametrlari: `{ mode?: "local"|"remote", workspace?: string }`
- `wizard.next` parametrlari: `{ sessionId, answer?: { stepId, value? } }`
- `wizard.cancel` parametrlari: `{ sessionId }`
- `wizard.status` parametrlari: `{ sessionId }`
- `config.schema` parametrlari: `{}`

Javoblar (tuzilishi)

- Usta: `{ sessionId, done, step?, status?, error? } }`
- Konfiguratsiya sxemasi: `{ schema, uiHints, version, generatedAt }`

## UI ko‘rsatmalari

- `uiHints` yo‘l bo‘yicha kalitlangan; ixtiyoriy metama’lumotlar (label/help/group/order/advanced/sensitive/placeholder).
- Sensitive maydonlar parol kiritish maydonlari sifatida render qilinadi; redaksiyalash qatlami yo‘q.
- Qo‘llab-quvvatlanmaydigan sxema tugunlari xom JSON muharririga qaytadi.

## Eslatmalar

- Bu hujjat onboarding/konfiguratsiya uchun protokol refaktorlarini kuzatishdagi yagona joydir.
