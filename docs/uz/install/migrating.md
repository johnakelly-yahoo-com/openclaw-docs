---
summary: "OpenClaw o‘rnatilmasini bir mashinadan boshqasiga ko‘chirish (migratsiya)"
read_when:
  - Siz OpenClaw’ni yangi noutbuk/serverga ko‘chiryapsiz
  - Siz sessiyalarni, autentifikatsiyani va kanal loginlarini (WhatsApp va boshqalar) saqlab qolmoqchisiz
title: "Migratsiya qo‘llanmasi"
---

# OpenClaw’ni yangi mashinaga ko‘chirish

Ushbu qo‘llanma OpenClaw Gateway’ni bir mashinadan boshqasiga **onboarding’ni qayta bajarilmasdan** ko‘chiradi.

Migratsiya kontseptual jihatdan sodda:

- **Holat katalogi**ni nusxalang (`$OPENCLAW_STATE_DIR`, standart: `~/.openclaw/`) — bu konfiguratsiya, autentifikatsiya, sessiyalar va kanal holatini o‘z ichiga oladi.
- **Workspace**’ingizni nusxalang (standart bo‘yicha `~/.openclaw/workspace/`) — bu agent fayllaringizni (xotira, promptlar va hokazo) o‘z ichiga oladi.

Ammo **profil**lar, **ruxsatlar** va **qisman nusxalar** bilan bog‘liq keng tarqalgan xatolar mavjud.

## Before you start (what you are migrating)

### 1. Identify your state directory

Most installs use the default:

- **State dir:** `~/.openclaw/`

But it may be different if you use:

- `--profile <name>` (often becomes `~/.openclaw-<profile>/`)
- `OPENCLAW_STATE_DIR=/some/path`

If you’re not sure, run on the **old** machine:

```bash
openclaw status
```

Look for mentions of `OPENCLAW_STATE_DIR` / profile in the output. If you run multiple gateways, repeat for each profile.

### 2. Identify your workspace

Common defaults:

- `~/.openclaw/workspace/` (recommended workspace)
- a custom folder you created

Your workspace is where files like `MEMORY.md`, `USER.md`, and `memory/*.md` live.

### 3. Understand what you will preserve

If you copy **both** the state dir and workspace, you keep:

- Gateway configuration (`openclaw.json`)
- Auth profiles / API keys / OAuth tokens
- Session history + agent state
- Channel state (e.g. WhatsApp login/session)
- Your workspace files (memory, skills notes, etc.)

If you copy **only** the workspace (e.g., via Git), you do **not** preserve:

- sessions
- credentials
- channel logins

Those live under `$OPENCLAW_STATE_DIR`.

## Migration steps (recommended)

### Step 0 — Make a backup (old machine)

On the **old** machine, stop the gateway first so files aren’t changing mid-copy:

```bash
openclaw gateway stop
```

(Optional but recommended) archive the state dir and workspace:

```bash
# Adjust paths if you use a profile or custom locations
cd ~
tar -czf openclaw-state.tgz .openclaw

tar -czf openclaw-workspace.tgz .openclaw/workspace
```

If you have multiple profiles/state dirs (e.g. `~/.openclaw-main`, `~/.openclaw-work`), archive each.

### Step 1 — Install OpenClaw on the new machine

On the **new** machine, install the CLI (and Node if needed):

- See: [Install](/install)

At this stage, it’s OK if onboarding creates a fresh `~/.openclaw/` — you will overwrite it in the next step.

### Step 2 — Copy the state dir + workspace to the new machine

Copy **both**:

- `$OPENCLAW_STATE_DIR` (default `~/.openclaw/`)
- your workspace (default `~/.openclaw/workspace/`)

Common approaches:

- `scp` the tarballs and extract
- `rsync -a` over SSH
- external drive

After copying, ensure:

- Hidden directories were included (e.g. `.openclaw/`)
- File ownership is correct for the user running the gateway

### 1. 3-qadam — Doktorni ishga tushirish (migratsiyalar + xizmatlarni tiklash)

2. **yangi** mashinada:

```bash
3. openclaw doctor
```

4. Doctor — bu “xavfsiz va zerikarli” buyruq. 5. U xizmatlarni tuzatadi, konfiguratsiya migratsiyalarini qo‘llaydi va nomuvofiqliklar haqida ogohlantiradi.

6. So‘ng:

```bash
7. openclaw gateway restart
openclaw status
```

## 8. Keng tarqalgan xatolar (va ularni qanday oldini olish)

### 9. Xato: profil / state-dir nomuvofiqligi

10. Agar eski gateway’ni profil (yoki `OPENCLAW_STATE_DIR`) bilan ishga tushirgan bo‘lsangiz va yangi gateway boshqasidan foydalansa, quyidagi alomatlarni ko‘rasiz:

- 11. konfiguratsiya o‘zgarishlari kuchga kirmaydi
- 12. kanallar yo‘qolgan / tizimdan chiqib ketgan
- 13. bo‘sh sessiya tarixi

14. Yechim: migratsiya qilingan **xuddi shu** profil/state dir’dan foydalanib gateway/xizmatni ishga tushiring, so‘ng yana ishga tushiring:

```bash
15. openclaw doctor
```

### 16. Xato: faqat `openclaw.json` ni ko‘chirish

17. `openclaw.json` yetarli emas. 18. Ko‘plab provayderlar holatni quyida saqlaydi:

- 19. `$OPENCLAW_STATE_DIR/credentials/`
- 20. `$OPENCLAW_STATE_DIR/agents/<agentId>/...`

21. Har doim butun `$OPENCLAW_STATE_DIR` papkasini migratsiya qiling.

### 22. Xato: ruxsatlar / egalik

23. Agar root sifatida ko‘chirgan bo‘lsangiz yoki foydalanuvchini o‘zgartirgan bo‘lsangiz, gateway credential’lar/sessiyalarni o‘qiy olmasligi mumkin.

24. Yechim: state dir va workspace gateway’ni ishga tushirayotgan foydalanuvchiga tegishli ekanini ta’minlang.

### 25. Xato: masofaviy/mahalliy rejimlar o‘rtasida migratsiya

- 26. Agar UI (WebUI/TUI) **masofaviy** gateway’ga ulanayotgan bo‘lsa, sessiya ombori va workspace masofaviy xostga tegishli bo‘ladi.
- 27. Noutbukingizni migratsiya qilish masofaviy gateway’ning holatini ko‘chirmaydi.

28. Agar masofaviy rejimda bo‘lsangiz, **gateway xostini** migratsiya qiling.

### 29. Xato: zaxira nusxalardagi sirlar

30. `$OPENCLAW_STATE_DIR` ichida sirlar mavjud (API kalitlari, OAuth tokenlari, WhatsApp credential’lari). 31. Zaxira nusxalarini ishlab chiqarish sirlaridek ko‘ring:

- 32. shifrlangan holda saqlang
- 33. xavfsiz bo‘lmagan kanallar orqali ulashishdan saqlaning
- 34. oshkor bo‘lganidan shubhalansangiz, kalitlarni aylantiring

## 35. Tekshiruv ro‘yxati

36. Yangi mashinada quyidagilarni tasdiqlang:

- 37. `openclaw status` gateway ishlayotganini ko‘rsatadi
- 38. Kanallaringiz hanuz ulangan (masalan, WhatsApp qayta juftlashni talab qilmaydi)
- 39. Boshqaruv paneli ochiladi va mavjud sessiyalarni ko‘rsatadi
- 40. Workspace fayllaringiz (xotira, konfiguratsiyalar) mavjud

## 41. Bog‘liq

- 42. [Doctor](/gateway/doctor)
- 43. [Gateway nosozliklarini bartaraf etish](/gateway/troubleshooting)
- 44. [OpenClaw ma’lumotlarini qayerda saqlaydi?](/help/faq#where-does-openclaw-store-its-data)
