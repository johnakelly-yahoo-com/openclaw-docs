---
summary: "25.\ 

  \    ```bash

  \    openclaw status

  \    openclaw gateway status

  \    openclaw nodes status

  \    openclaw nodes describe --node "
read_when:
  - |-
    26. 
        openclaw logs --follow
        ```
  - |-
    27. Yaxshi chiqish quyidagicha ko‘rinadi:

    - Tugun ulangan va `node` roli uchun pairing qilingan.
    - Chaqqirayotgan buyruq uchun imkoniyat mavjud.
    - Asbob uchun ruxsat holati berilgan.

    Keng tarqalgan log imzolari:

    - `NODE_BACKGROUND_UNAVAILABLE` → tugun ilovasini foreground’ga olib chiqing.
    - `*_PERMISSION_REQUIRED` → OS ruxsati rad etilgan/yo‘q.
    - `SYSTEM_RUN_DENIED: approval required` → exec tasdiqlanishi kutilmoqda.
    - `SYSTEM_RUN_DENIED: allowlist miss` → buyruq exec allowlist’da yo‘q.

    Chuqur sahifalar:

    - [/gateway/troubleshooting#node-paired-tool-fails](/gateway/troubleshooting#node-paired-tool-fails)
    - [/nodes/troubleshooting](/nodes/troubleshooting)
    - [/tools/exec-approvals](/tools/exec-approvals)
title: "28.\ 

  \    ```bash

  \    openclaw status

  \    openclaw gateway status

  \    openclaw browser status

  \    openclaw logs --follow

  \    openclaw doctor

  \    ```"
---

# 29. Yaxshi chiqish quyidagicha ko‘rinadi:- Browser holati `running: true` va tanlangan brauzer/profilni ko‘rsatadi.
- `openclaw` profili ishga tushadi yoki `chrome` relay ulangan tab’ga ega.Keng tarqalgan log imzolari:- `Failed to start Chrome CDP on port` → lokal brauzerni ishga tushirish muvaffaqiyatsiz.
- `browser.executablePath not found` → sozlangan binar yo‘l noto‘g‘ri.
- `Chrome extension relay is running, but no tab is connected` → kengaytma ulanmagan.
- `Browser attachOnly is enabled ... not reachable` → attach-only profilda tirik CDP nishoni yo‘q.Chuqur sahifalar:- [/gateway/troubleshooting#browser-tool-fails](/gateway/troubleshooting#browser-tool-fails)
- [/tools/browser-linux-troubleshooting](/tools/browser-linux-troubleshooting)
- [/tools/chrome-extension](/tools/chrome-extension)

30. </Accordion> 31. SOUL Evil hook (SOUL.md o‘rniga SOUL_EVIL.md ni almashtirish)

## 32. Siz SOUL Evil hook’ni yoqmoqchisiz yoki sozlamoqchisiz

33. Siz purge oynasini yoki tasodifiy ehtimol bilan persona almashtirishni xohlaysiz 34. SOUL Evil Hook

35. SOUL Evil Hook

## 36. SOUL Evil hook **injected** `SOUL.md` tarkibini purge oynasi davomida yoki tasodifiy ehtimol bilan `SOUL_EVIL.md` ga almashtiradi.

```bash
37. U diskdagi fayllarni **o‘zgartirmaydi**.
```

38. Qanday ishlaydi

```json
39. `agent:bootstrap` ishga tushganda, hook tizim prompti yig‘ilishidan oldin xotiradagi `SOUL.md` tarkibini almashtirishi mumkin.
```

40. Agar `SOUL_EVIL.md` yo‘q yoki bo‘sh bo‘lsa, OpenClaw ogohlantirishni log qiladi va oddiy `SOUL.md` ni saqlab qoladi.

## 41. Sub-agent ishga tushishlari o‘z bootstrap fayllariga `SOUL.md` ni kiritmaydi, shuning uchun bu hook sub-agentlarga ta’sir qilmaydi.

- 42. Yoqish
- 43. openclaw hooks enable soul-evil
- 44. So‘ng konfiguratsiyani o‘rnating:
- `purge.duration` (davomiylik): oyna uzunligi (masalan, `30s`, `10m`, `1h`)

**Ustuvorlik:** purge oynasi tasodif ehtimolidan ustun turadi.

**Vaqt zonasi:** agar sozlangan bo‘lsa `agents.defaults.userTimezone` ishlatiladi; aks holda xost vaqt zonasi.

## Eslatmalar

- Diskda hech qanday fayl yozilmaydi yoki o‘zgartirilmaydi.
- Agar `SOUL.md` bootstrap ro‘yxatida bo‘lmasa, hook hech narsa qilmaydi.

## Shuningdek qarang

- [Hooks](/automation/hooks)
