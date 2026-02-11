---
summary: "Exec tasdiqlari, ruxsat roʻyxatlari va sandboxdan chiqish promptlari"
read_when:
  - Exec tasdiqlari yoki ruxsat roʻyxatlarini sozlash
  - macOS ilovasida exec tasdiqlari UX’ini joriy etish
  - Sandboxdan chiqish promptlarini va ularning oqibatlarini ko‘rib chiqish
title: "Exec tasdiqlari"
---

# Exec tasdiqlari

Exec tasdiqlari — bu sandboxlangan agentga haqiqiy xostda (`gateway` yoki `node`) buyruqlarni bajarishga ruxsat berish uchun **hamroh ilova / node xost himoya mexanizmi**. Buni xavfsizlik blokirovkasi sifatida tasavvur qiling:
buyruqlarga faqat siyosat + ruxsat roʻyxati + (ixtiyoriy) foydalanuvchi tasdig‘i barchasi mos kelgandagina ruxsat beriladi.
Exec tasdiqlari vosita siyosati va yuqori darajadagi cheklovlardan **qo‘shimcha** hisoblanadi (agar elevated `full` ga o‘rnatilgan bo‘lsa, tasdiqlar o‘tkazib yuboriladi).
Amaldagi siyosat `tools.exec.*` va tasdiqlar standartlaridan **eng qat’iyrog‘i** hisoblanadi; agar tasdiqlar maydoni ko‘rsatilmagan bo‘lsa, `tools.exec` qiymati ishlatiladi.

Agar hamroh ilova UI’i **mavjud bo‘lmasa**, prompt talab qiladigan har qanday so‘rov **ask fallback** orqali hal qilinadi (standart: deny).

## Qo‘llaniladigan joylar

Exec tasdiqlari bajarilish xostida mahalliy ravishda majburiy qo‘llanadi:

- **gateway host** → gateway mashinasidagi `openclaw` jarayoni
- **node host** → node runner (macOS hamroh ilovasi yoki boshqaruvsiz node xosti)

macOS bo‘linishi:

- **node host service** `system.run` ni mahalliy IPC orqali **macOS ilovasi**ga uzatadi.
- **macOS ilovasi** tasdiqlarni majburiy qo‘llaydi + buyruqni UI kontekstida bajaradi.

## Sozlamalar va saqlash

Tasdiqlar bajarilish xostidagi mahalliy JSON faylida saqlanadi:

~/.openclaw/exec-approvals.json

Namunaviy sxema:

```json
{
  "version": 1,
  "socket": {
    "path": "~/.openclaw/exec-approvals.sock",
    "token": "base64url-token"
  },
  "defaults": {
    "security": "deny",
    "ask": "on-miss",
    "askFallback": "deny",
    "autoAllowSkills": false
  },
  "agents": {
    "main": {
      "security": "allowlist",
      "ask": "on-miss",
      "askFallback": "deny",
      "autoAllowSkills": true,
      "allowlist": [
        {
          "id": "B0C8C0B3-2C2D-4F8A-9A3C-5A4B3C2D1E0F",
          "pattern": "~/Projects/**/bin/rg",
          "lastUsedAt": 1737150000000,
          "lastUsedCommand": "rg -n TODO",
          "lastResolvedPath": "/Users/user/Projects/.../bin/rg"
        }
      ]
    }
  }
}
```

## Siyosat sozlagichlari

### Xavfsizlik (`exec.security`)

- **deny**: barcha xost exec so‘rovlarini bloklash.
- **allowlist**: faqat ruxsat ro‘yxatiga kiritilgan buyruqlarga ruxsat berish.
- **full**: hammasiga ruxsat berish (elevated ga teng).

### So‘rash (`exec.ask`)

- **off**: hech qachon prompt chiqarmaslik.
- **on-miss**: faqat ruxsat ro‘yxati mos kelmaganda prompt chiqarish.
- **always**: har bir buyruqda prompt chiqarish.

### So‘rash uchun zaxira (`askFallback`)

Agar prompt talab qilinsa, lekin UI’ga ulanib bo‘lmasa, zaxira qarorni belgilaydi:

- **deny**: bloklash.
- **allowlist**: faqat ruxsat ro‘yxati mos kelsa ruxsat berish.
- **full**: ruxsat berish.

## Ruxsat ro‘yxati (har bir agent uchun)

Ruxsat ro‘yxatlari **har bir agent uchun alohida**. Agar bir nechta agent mavjud bo‘lsa, macOS ilovasida qaysi agentni tahrirlayotganingizni almashtiring. Patternlar **katta-kichik harfga sezgir bo‘lmagan glob moslashlar**.
Patternlar **ikkilik fayl yo‘llari**ga yechilishi kerak (faqat basename’dan iborat yozuvlar e’tiborga olinmaydi).
Eski `agents.default` yozuvlari yuklash vaqtida `agents.main` ga ko‘chiriladi.

Misollar:

- `~/Projects/**/bin/peekaboo`
- `~/.local/bin/*`
- `/opt/homebrew/bin/rg`

Har bir ruxsat ro‘yxati yozuvi quyidagilarni kuzatadi:

- **id** — UI identifikatsiyasi uchun ishlatiladigan barqaror UUID (ixtiyoriy)
- **oxirgi ishlatilgan** vaqt belgisi
- **oxirgi ishlatilgan buyruq**
- **oxirgi aniqlangan yo‘l**

## Skill CLI’larini avtomatik ruxsat berish

**Skill CLI’larini avtomatik ruxsat berish** yoqilganda, ma’lum skilllar tomonidan murojaat qilingan bajariluvchi fayllar tugunlarda (macOS tuguni yoki headless tugun xosti) ruxsat etilganlar ro‘yxatida deb hisoblanadi. Bu Gateway RPC orqali skill bin ro‘yxatini olish uchun `skills.bins` dan foydalanadi. Agar qat’iy qo‘lda boshqariladigan ruxsat ro‘yxatlarini xohlasangiz, buni o‘chiring.

## Xavfsiz binlar (faqat stdin)

`tools.exec.safeBins` **faqat stdin** bilan ishlaydigan kichik binarlar ro‘yxatini belgilaydi (masalan `jq`), ular **aniq ruxsat ro‘yxati yozuvlarisiz** ruxsat rejimida ishlashi mumkin. Xavfsiz binlar pozitsion fayl argumentlari va yo‘lga o‘xshash tokenlarni rad etadi, shuning uchun ular faqat kiruvchi oqim bilan ishlaydi.
Ruxsat ro‘yxati rejimida shell zanjirlash va yo‘naltirishlar avtomatik ruxsat etilmaydi.

Shell zanjirlash (`&&`, `||`, `;`) har bir yuqori darajadagi segment ruxsat ro‘yxati talablariga javob berganda (jumladan xavfsiz binlar yoki skill avtomatik ruxsati) ruxsat etiladi. Ruxsat ro‘yxati rejimida yo‘naltirishlar hanuz qo‘llab-quvvatlanmaydi.
Buyruq almashtirish (`$()` / backticks) ruxsat ro‘yxatini tahlil qilish jarayonida rad etiladi, jumladan qo‘shtirnoq ichida ham; agar sizga literal `$()` matni kerak bo‘lsa, yakka qo‘shtirnoqlardan foydalaning.

Standart xavfsiz binlar: `jq`, `grep`, `cut`, `sort`, `uniq`, `head`, `tail`, `tr`, `wc`.

## Control UI tahriri

Standartlarni, agentga xos sozlamalarni va ruxsat ro‘yxatlarini tahrirlash uchun **Control UI → Nodes → Exec approvals** kartasidan foydalaning. Qamrovni tanlang (Standartlar yoki agent), siyosatni sozlang, ruxsat ro‘yxati naqshlarini qo‘shing/olib tashlang, so‘ng **Save** ni bosing. UI har bir naqsh bo‘yicha **oxirgi ishlatilgan** metama’lumotni ko‘rsatadi, shunda ro‘yxatni tartibli saqlashingiz mumkin.

Nishon tanlagichi **Gateway** (mahalliy tasdiqlar) yoki **Node** ni tanlaydi. Tugunlar `system.execApprovals.get/set` ni e’lon qilishi kerak (macOS ilovasi yoki headless tugun xosti).
Agar tugun hali exec tasdiqlarini e’lon qilmasa, uning mahalliy `~/.openclaw/exec-approvals.json` faylini bevosita tahrirlang.

CLI: `openclaw approvals` gateway yoki tugun tahririni qo‘llab-quvvatlaydi (qarang [Approvals CLI](/cli/approvals)).

## Tasdiqlash oqimi

Tasdiq talab qilinganda, gateway operator mijozlariga `exec.approval.requested` ni efirga uzatadi.
Control UI va macOS ilovasi uni `exec.approval.resolve` orqali hal qiladi, so‘ng gateway tasdiqlangan so‘rovni tugun xostiga uzatadi.

Tasdiqlar talab qilinganda, exec asbobi darhol tasdiq identifikatori bilan qaytadi. Keyingi tizim hodisalarini (`Exec finished` / `Exec denied`) moslashtirish uchun shu identifikatordan foydalaning. Agar belgilangan vaqt ichida qaror kelmasa, so‘rov tasdiq vaqti tugashi sifatida ko‘riladi va rad etish sababi sifatida ko‘rsatiladi.

Tasdiqlash dialogi quyidagilarni o‘z ichiga oladi:

- buyruq + argumentlar
- cwd
- agent id
- aniqlangan bajariluvchi yo‘l
- xost + siyosat metama’lumotlari

Amallar:

- **Bir marta ruxsat berish** → hozir ishga tushirish
- **Doim ruxsat berish** → ruxsat ro‘yxatiga qo‘shish + ishga tushirish
- **Rad etish** → bloklash

## Chat kanallariga tasdiqlarni yo‘naltirish

Exec tasdiqlash so‘rovlarini istalgan chat kanaliga (jumladan plagin kanallari) yo‘naltirishingiz va ularni `/approve` bilan tasdiqlashingiz mumkin. Bu odatiy chiqish yetkazib berish quvuridan foydalanadi.

Konfiguratsiya:

```json5
{
  approvals: {
    exec: {
      enabled: true,
      mode: "session", // "session" | "targets" | "both"
      agentFilter: ["main"],
      sessionFilter: ["discord"], // substring yoki regex
      targets: [
        { channel: "slack", to: "U12345678" },
        { channel: "telegram", to: "123456789" },
      ],
    },
  },
}
```

Chatda javob berish:

```
/approve <id> allow-once
/approve <id> allow-always
/approve <id> deny
```

### macOS IPC oqimi

```
Gateway -> Node Service (WS)
                 |  IPC (UDS + token + HMAC + TTL)
                 v
             Mac App (UI + approvals + system.run)
```

Xavfsizlik eslatmalari:

- Unix soket rejimi `0600`, token `exec-approvals.json` da saqlanadi.
- Bir xil UID tekshiruvi.
- Challenge/response (nonce + HMAC token + request hash) + short TTL.

## System events

Exec lifecycle is surfaced as system messages:

- `Exec running` (only if the command exceeds the running notice threshold)
- `Exec finished`
- `Exec denied`

These are posted to the agent’s session after the node reports the event.
Gateway-host exec approvals emit the same lifecycle events when the command finishes (and optionally when running longer than the threshold).
Approval-gated execs reuse the approval id as the `runId` in these messages for easy correlation.

## Implications

- **full** is powerful; prefer allowlists when possible.
- **ask** keeps you in the loop while still allowing fast approvals.
- Per-agent allowlists prevent one agent’s approvals from leaking into others.
- Approvals only apply to host exec requests from **authorized senders**. Unauthorized senders cannot issue `/exec`.
- `/exec security=full` is a session-level convenience for authorized operators and skips approvals by design.
  To hard-block host exec, set approvals security to `deny` or deny the `exec` tool via tool policy.

Related:

- [Exec tool](/tools/exec)
- [Elevated mode](/tools/elevated)
- [Skills](/tools/skills)
