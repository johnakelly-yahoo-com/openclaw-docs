---
title: Lobster
summary: "OpenClaw uchun qayta tiklanadigan tasdiqlash darvozalari bilan tiplangan ish jarayoni runtime’i."
description: OpenClaw uchun tiplangan ish jarayoni runtime’i — tasdiqlash darvozalari bilan kompozitsiyalanadigan quvurlar.
read_when:
  - Siz aniq tasdiqlar bilan deterministik ko‘p bosqichli ish jarayonlarini xohlaysiz
  - Oldingi qadamlarni qayta ishga tushirmasdan ish jarayonini davom ettirishingiz kerak
---

# Lobster

Lobster — OpenClaw’ga aniq tasdiqlash nuqtalari bilan ko‘p bosqichli asboblar ketma-ketligini yagona, deterministik operatsiya sifatida bajarishga imkon beruvchi ish jarayoni qobig‘i.

## Hook

Yordamchingiz o‘zini boshqaradigan asboblarni yaratishi mumkin. Ish jarayonini so‘rang, va 30 daqiqadan so‘ng sizda bitta chaqiruvda ishlaydigan CLI hamda quvurlar bo‘ladi. Lobster — yetishmayotgan bo‘lak: deterministik quvurlar, aniq tasdiqlar va qayta tiklanadigan holat.

## Nega

Bugun murakkab ish jarayonlari ko‘plab oldinga-orqaga asbob chaqiruvlarini talab qiladi. Har bir chaqiruv tokenlarga tushadi va LLM har bir qadamni orkestratsiya qilishi kerak. Lobster bu orkestratsiyani tiplangan runtime’ga ko‘chiradi:

- **Ko‘p chaqiruvlar o‘rniga bitta**: OpenClaw bitta Lobster asbob chaqiruvini bajaradi va tuzilgan natijani oladi.
- **Tasdiqlar ichiga qurilgan**: Yon ta’sirlar (email yuborish, izoh joylash) aniq tasdiqlanmaguncha ish jarayonini to‘xtatadi.
- **Qayta tiklanadigan**: To‘xtatilgan ish jarayonlari token qaytaradi; tasdiqlang va hammasini qayta ishga tushirmasdan davom eting.

## Nega oddiy dasturlar o‘rniga DSL?

Lobster ataylab kichik. Maqsad “yangi til” emas, balki birinchi darajali tasdiqlar va davom ettirish tokenlari bilan bashorat qilinadigan, AI’ga qulay quvur spetsifikatsiyasidir.

- **Tasdiqlash/davom ettirish ichiga qurilgan**: Oddiy dastur odamdan so‘rashi mumkin, ammo siz o‘zingiz alohida runtime ixtiro qilmasdan mustahkam token bilan _to‘xtab davom eta olmaydi_.
- **Deterministiklik + auditlanish**: Quvurlar ma’lumotdir, shuning uchun ularni yozib olish, farqlash, qayta ijro etish va ko‘rib chiqish oson.
- **AI uchun cheklangan sirt**: Kichik grammatika + JSON quvurlash “ijodiy” kod yo‘llarini kamaytiradi va tekshiruvni real qiladi.
- **Xavfsizlik siyosati ichiga singdirilgan**: Timeoutlar, chiqish cheklovlari, sandbox tekshiruvlari va allowlistlar har bir skript emas, balki runtime tomonidan majburlanadi.
- **Hali ham dasturlanadigan**: Har bir qadam istalgan CLI yoki skriptni chaqirishi mumkin. Agar JS/TS xohlasangiz, `.lobster` fayllarini koddan yarating.

## Qanday ishlaydi

OpenClaw lokal `lobster` CLI’ni **asbob rejimida** ishga tushiradi va stdout’dan JSON konvertini tahlil qiladi.
Agar quvur tasdiqlash uchun to‘xtasa, asbob keyinroq davom ettirish uchun `resumeToken` qaytaradi.

## 1. Naqsh: kichik CLI + JSON quvurlari + tasdiqlashlar

2. JSON bilan gaplashadigan juda kichik buyruqlarni yarating, so‘ng ularni bitta Lobster chaqiruviga zanjirlab ulang. 3. (Quyida buyruq nomlariga misollar — o‘zingiznikiga almashtiring.)

```bash
4. inbox list --json
inbox categorize --json
inbox apply --json
```

```json
5. {
  "action": "run",
  "pipeline": "exec --json --shell 'inbox list --json' | exec --stdin json --shell 'inbox categorize --json' | exec --stdin json --shell 'inbox apply --json' | approve --preview-from-stdin --limit 5 --prompt 'Apply changes?'",
  "timeoutMs": 30000
}
```

6. Agar quvur tasdiqlashni so‘rasa, token bilan davom ettiring:

```json
46. {
  "action": "resume",
  "token": "<resumeToken>",
  "approve": true
}
```

8. AI ish jarayonini ishga tushiradi; Lobster bosqichlarni bajaradi. 9. Tasdiqlash darvozalari yon ta’sirlarni aniq va audit qilinadigan holatda saqlaydi.

10. Misol: kirish elementlarini asbob chaqiruvlariga moslash:

```bash
11. gog.gmail.search --query 'newer_than:1d' \
  | openclaw.invoke --tool message --action send --each --item-key message --args-json '{"provider":"telegram","to":"..."}'
```

## 12. Faqat JSON bo‘lgan LLM bosqichlari (llm-task)

13. **Tuzilgan LLM bosqichi** kerak bo‘lgan ish jarayonlari uchun ixtiyoriy
    `llm-task` plagin asbobini yoqing va uni Lobster’dan chaqiring. 14. Bu ish jarayonini deterministik holatda saqlaydi, shu bilan birga model yordamida tasniflash/xulosa qilish/qoralama yozishga imkon beradi.

47. Vositanı yoqing:

```json
48. {
  "plugins": {
    "entries": {
      "llm-task": { "enabled": true }
    }
  },
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": { "allow": ["llm-task"] }
      }
    ]
  }
}
```

17. Uni quvurda ishlating:

```lobster
18. openclaw.invoke --tool llm-task --action json --args-json '{
  "prompt": "Given the input email, return intent and draft.",
  "input": { "subject": "Hello", "body": "Can you help?" },
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

49. Tafsilotlar va sozlash variantlari uchun [LLM Task](/tools/llm-task) ga qarang.

## 50. Workflow fayllari (.lobster)

21. Lobster `name`, `args`, `steps`, `env`, `condition` va `approval` maydonlariga ega YAML/JSON ish jarayoni fayllarini ishga tushira oladi. 22. OpenClaw asbob chaqiruvlarida `pipeline` ni fayl yo‘liga o‘rnating.

```yaml
name: inbox-triage
args:
  tag:
    default: "family"
steps:
  - id: collect
    command: inbox list --json
  - id: categorize
    command: inbox categorize --json
    stdin: $collect.stdout
  - id: approve
    command: inbox apply --approve
    stdin: $categorize.stdout
    approval: required
  - id: execute
    command: inbox apply --execute
    stdin: $categorize.stdout
    condition: $approve.approved
```

24. Eslatmalar:

- 25. `stdin: $step.stdout` va `stdin: $step.json` oldingi bosqich chiqishini uzatadi.
- 26. `condition` (yoki `when`) bosqichlarni `$step.approved` ga qarab cheklashi mumkin.

## 27. Lobster’ni o‘rnating

28. OpenClaw Gateway ishlaydigan **xuddi shu xost**ga Lobster CLI’ni o‘rnating ([Lobster repozitoriyasi](https://github.com/openclaw/lobster)ga qarang) va `lobster` `PATH`da ekanini ta’minlang.
29. Agar maxsus binar joylashuvdan foydalanmoqchi bo‘lsangiz, asbob chaqiruvida **mutlaq** `lobsterPath` ni bering.

## 30. Asbobni yoqing

31. Lobster — **ixtiyoriy** plagin asbob (sukut bo‘yicha yoqilmagan).

32. Tavsiya etiladi (qo‘shimcha, xavfsiz):

```json
33. {
  "tools": {
    "alsoAllow": ["lobster"]
  }
}
```

34. Yoki agent bo‘yicha:

```json
35. {
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": {
          "alsoAllow": ["lobster"]
        }
      }
    ]
  }
}
```

36. Cheklovchi allowlist rejimida ishlashni ko‘zlamagan bo‘lsangiz, `tools.allow: ["lobster"]` dan foydalanishdan saqlaning.

37. Eslatma: allowlistlar ixtiyoriy plaginlar uchun opt-in hisoblanadi. 38. Agar allowlistingiz faqat
    `lobster` kabi plagin asboblarini nomlasa, OpenClaw asosiy asboblarni yoqilgan holda qoldiradi. 39. Asosiy
    asboblarni cheklash uchun allowlistga xohlagan asosiy asboblar yoki guruhlarni ham kiriting.

## 40. Misol: Email saralash

41. Lobster’siz:

```
42. Foydalanuvchi: "Emailimni tekshir va javoblar qoralamasini tayyorla"
→ openclaw gmail.list ni chaqiradi
→ LLM xulosa qiladi
→ Foydalanuvchi: "#2 va #5 ga javoblar qoralamasini yoz"
→ LLM qoralama yozadi
→ Foydalanuvchi: "#2 ni yubor"
→ openclaw gmail.send ni chaqiradi
(har kuni takrorlanadi, nima saralanganini eslab qolmaydi)
```

43. Lobster bilan:

```json
44. {
  "action": "run",
  "pipeline": "email.triage --limit 20",
  "timeoutMs": 30000
}
```

45. JSON konvertini qaytaradi (qisqartirilgan):

```json
46. {
  "ok": true,
  "status": "needs_approval",
  "output": [{ "summary": "5 need replies, 2 need action" }],
  "requiresApproval": {
    "type": "approval_request",
    "prompt": "Send 2 draft replies?",
    "items": [],
    "resumeToken": "..."
  }
}
```

47. Foydalanuvchi tasdiqlaydi → davom ettirish:

```json
48. {
  "action": "resume",
  "token": "<resumeToken>",
  "approve": true
}
```

49. Bitta ish jarayoni. 50. Deterministik. 1. Xavfsiz.

## 2. Asbob parametrlari

### 3. `run`

4. Asbob rejimida pipeline-ni ishga tushiring.

```json
5. {
  "action": "run",
  "pipeline": "gog.gmail.search --query 'newer_than:1d' | email.triage",
  "cwd": "/path/to/workspace",
  "timeoutMs": 30000,
  "maxStdoutBytes": 512000
}
```

6. Argumentlar bilan workflow faylini ishga tushiring:

```json
7. {
  "action": "run",
  "pipeline": "/path/to/inbox-triage.lobster",
  "argsJson": "{\"tag\":\"family\"}"
}
```

### 8. `resume`

9. Tasdiqlangandan so‘ng to‘xtatilgan workflow-ni davom ettiring.

```json
10. {
  "action": "resume",
  "token": "<resumeToken>",
  "approve": true
}
```

### 11. Ixtiyoriy kirishlar

- 12. `lobsterPath`: Lobster binar faylining mutlaq yo‘li (`PATH` dan foydalanish uchun qoldiring).
- 13. `cwd`: Pipeline uchun ishchi katalog (standart bo‘yicha joriy jarayonning ishchi katalogi).
- 14. `timeoutMs`: Agar subprocess bu davomiylikdan oshsa, uni to‘xtatadi (standart: 20000).
- 15. `maxStdoutBytes`: Agar stdout bu hajmdan oshsa, subprocess-ni to‘xtatadi (standart: 512000).
- 16. `argsJson`: `lobster run --args-json` ga uzatiladigan JSON satri (faqat workflow fayllari uchun).

## 17. Chiqish konverti

18. Lobster uchta holatdan biri bilan JSON konvertini qaytaradi:

- 19. `ok` → muvaffaqiyatli yakunlandi
- 20. `needs_approval` → pauza qilingan; davom ettirish uchun `requiresApproval.resumeToken` talab qilinadi
- 21. `cancelled` → ochiqchasiga rad etilgan yoki bekor qilingan

22. Asbob konvertni ham `content` (chiroyli JSON), ham `details` (xom obyekt) da ko‘rsatadi.

## 23. Tasdiqlar

24. Agar `requiresApproval` mavjud bo‘lsa, so‘rovni ko‘rib chiqing va qaror qabul qiling:

- 25. `approve: true` → davom ettiring va yon ta’sirlarni davom ettiring
- 26. `approve: false` → bekor qiling va workflow-ni yakunlang

27. Maxsus jq/heredoc bog‘lovchisiz tasdiq so‘rovlariga JSON ko‘rinishini biriktirish uchun `approve --preview-from-stdin --limit N` dan foydalaning. 28. Resume tokenlari endi ixcham: Lobster workflow-ni davom ettirish holatini o‘zining state katalogida saqlaydi va kichik token kalitini qaytaradi.

## 29. OpenProse

30. OpenProse Lobster bilan yaxshi ishlaydi: ko‘p-agentli tayyorgarlikni boshqarish uchun `/prose` dan foydalaning, so‘ng deterministik tasdiqlar uchun Lobster pipeline-ni ishga tushiring. 31. Agar Prose dasturiga Lobster kerak bo‘lsa, sub-agentlar uchun `tools.subagents.tools` orqali `lobster` asbobiga ruxsat bering. 32. [OpenProse](/prose) ni ko‘ring.

## 33. Xavfsizlik

- 34. **Faqat mahalliy subprocess** — plagin o‘zi tarmoq chaqiruvlarini qilmaydi.
- 35. **Maxfiy ma’lumotlar yo‘q** — Lobster OAuth-ni boshqarmaydi; u buni qiladigan OpenClaw asboblarini chaqiradi.
- 36. **Sandbox-ga mos** — asbob konteksti sandbox qilingan bo‘lsa, o‘chiriladi.
- 37. **Mustahkamlangan** — agar ko‘rsatilsa, `lobsterPath` mutlaq bo‘lishi shart; timeout va chiqish cheklovlari majburiy.

## 38. Muammolarni bartaraf etish

- 39. **`lobster subprocess timed out`** → `timeoutMs` ni oshiring yoki uzun pipeline-ni bo‘ling.
- 40. **`lobster output exceeded maxStdoutBytes`** → `maxStdoutBytes` ni oshiring yoki chiqish hajmini kamaytiring.
- 41. **`lobster returned invalid JSON`** → pipeline asbob rejimida ishlashini va faqat JSON chop etishini ta’minlang.
- 42. **`lobster failed (code …)`** → stderr-ni ko‘rish uchun xuddi shu pipeline-ni terminalda ishga tushiring.

## 43. Batafsil ma’lumot

- 44. [Plugins](/tools/plugin)
- 45. [Plugin tool authoring](/plugins/agent-tools)

## 46. Amaliy tadqiqot: hamjamiyat workflow-lari

47. Bitta ommaviy misol: uchta Markdown omborini (shaxsiy, hamkor, umumiy) boshqaradigan “ikkinchi miya” CLI + Lobster pipeline-lari. 48. CLI statistika, inbox ro‘yxatlari va eskirganlarni skanerlash uchun JSON chiqaradi; Lobster esa bu buyruqlarni `weekly-review`, `inbox-triage`, `memory-consolidation` va `shared-task-sync` kabi, har biri tasdiqlash darvozalari bilan workflow-larga zanjirlaydi. 49. AI mavjud bo‘lganda hukm chiqarishni (toifalashni) bajaradi va mavjud bo‘lmaganda deterministik qoidalarga tayanadi.

- 50. Mavzu: [https://x.com/plattenschieber/status/2014508656335770033](https://x.com/plattenschieber/status/2014508656335770033)
- Repo: [https://github.com/bloomedai/brain-cli](https://github.com/bloomedai/brain-cli)
