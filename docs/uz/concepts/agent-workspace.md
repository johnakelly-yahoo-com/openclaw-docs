---
summary: "Agent workspace: location, layout, and backup strategy"
read_when:
  - You need to explain the agent workspace or its file layout
  - You want to back up or migrate an agent workspace
title: "Agent Workspace"
---

# Agent workspace

The workspace is the agent's home. It is the only working directory used for
file tools and for workspace context. Keep it private and treat it as memory.

This is separate from `~/.openclaw/`, which stores config, credentials, and
sessions.

**Important:** the workspace is the **default cwd**, not a hard sandbox. Tools
resolve relative paths against the workspace, but absolute paths can still reach
elsewhere on the host unless sandboxing is enabled. `HEARTBEAT.md`
When sandboxing is enabled and `workspaceAccess` is not `"rw"`, tools operate
inside a sandbox workspace under `~/.openclaw/sandboxes`, not your host workspace.

## Default location

- Default: `~/.openclaw/workspace`
- 1. Agar `OPENCLAW_PROFILE` o‘rnatilgan bo‘lsa va `"default"` bo‘lmasa, standart joy quyidagicha bo‘ladi
     `~/.openclaw/workspace-<profile>`.
- 2. `~/.openclaw/openclaw.json` faylida almashtirish:

```json5
3. {
  agent: {
    workspace: "~/.openclaw/workspace",
  },
}
```

4. `openclaw onboard`, `openclaw configure` yoki `openclaw setup` buyruqlari
   workspace’ni yaratadi va agar ular yo‘q bo‘lsa, bootstrap fayllarini boshlang‘ich holatda joylaydi.

5. Agar siz workspace fayllarini allaqachon o‘zingiz boshqarsangiz, bootstrap
   fayllarini yaratishni o‘chirib qo‘yishingiz mumkin:

```json5
6. { agent: { skipBootstrap: true } }
```

## 7. Qo‘shimcha workspace papkalari

8. Eski o‘rnatishlar `~/openclaw` ni yaratgan bo‘lishi mumkin. 9. Bir nechta workspace kataloglarini saqlab yurish chalkash autentifikatsiya yoki holatning siljishiga olib kelishi mumkin, chunki bir vaqtning o‘zida faqat bitta workspace faol bo‘ladi.

10. **Tavsiya:** bitta faol workspace’ni saqlang. 11. Agar qo‘shimcha papkalardan endi foydalanmasangiz, ularni arxivlang yoki Chiqindiga ko‘chiring (masalan `trash ~/openclaw`).
11. Agar siz ataylab bir nechta workspace’ni saqlasangiz, `agents.defaults.workspace` faol bo‘lganiga ishora qilayotganiga ishonch hosil qiling.

13. `openclaw doctor` qo‘shimcha workspace kataloglarini aniqlaganda ogohlantiradi.

## 14. Workspace fayllari xaritasi (har bir fayl nimani anglatadi)

15. Bular OpenClaw workspace ichida kutadigan standart fayllardir:

- `AGENTS.md`
  - 17. Agent uchun ishlash ko‘rsatmalari va xotiradan qanday foydalanishi kerakligi.
  - 18. Har bir sessiya boshida yuklanadi.
  - 19. Qoidalar, ustuvorliklar va "qanday tutish kerak" tafsilotlari uchun yaxshi joy.

- `SOUL.md`
  - 21. Persona, ohang va chegaralar.
  - 22. Har bir sessiyada yuklanadi.

- `USER.md`
  - 24. Foydalanuvchi kimligi va unga qanday murojaat qilish.
  - 25. Har bir sessiyada yuklanadi.

- `IDENTITY.md`
  - 27. Agentning nomi, kayfiyati (vibe) va emoji.
  - 28. Bootstrap marosimi davomida yaratiladi/yangilanadi.

- `TOOLS.md`
  - 30. Mahalliy vositalaringiz va kelishuvlaringiz haqidagi eslatmalar.
  - 31. Vositalar mavjudligini boshqarmaydi; bu faqat yo‘l-yo‘riq.

- README bilan boshlamang (merge konfliktlaridan qochish uchun).
  - 33. Heartbeat ishga tushirishlari uchun ixtiyoriy kichik chek-list.
  - 34. Tokenlarni bekorga sarflamaslik uchun qisqa tuting.

- `BOOT.md`
  - 36. Ichki hook’lar yoqilganda gateway qayta ishga tushirilganda bajariladigan ixtiyoriy boshlang‘ich chek-list.
  - 37. Qisqa tuting; tashqi yuborishlar uchun message vositasidan foydalaning.

- `BOOTSTRAP.md`
  - 39. Bir martalik birinchi ishga tushirish marosimi.
  - 40. Faqat mutlaqo yangi workspace uchun yaratiladi.
  - 41. Marosim tugagach, uni o‘chirib tashlang.

- `memory/YYYY-MM-DD.md`
  - 43. Kundalik xotira jurnali (har kun uchun bitta fayl).
  - 44. Sessiya boshida bugungi + kechagini o‘qish tavsiya etiladi.

- `MEMORY.md` (ixtiyoriy)
  - 46. Tanlab olingan uzoq muddatli xotira.
  - 47. Faqat asosiy, shaxsiy sessiyada yuklang (umumiy/guruh kontekstlarida emas).

48. Ish jarayoni va avtomatik xotira tozalash uchun [Memory](/concepts/memory) ga qarang.

- `skills/` (ixtiyoriy)
  - 50. Workspace’ga xos ko‘nikmalar.
  - Overrides managed/bundled skills when names collide.

- `canvas/` (optional)
  - Canvas UI files for node displays (for example `canvas/index.html`).

If any bootstrap file is missing, OpenClaw injects a "missing file" marker into
the session and continues. Large bootstrap files are truncated when injected;
adjust the limit with `agents.defaults.bootstrapMaxChars` (default: 20000).
`openclaw setup` can recreate missing defaults without overwriting existing
files.

## What is NOT in the workspace

These live under `~/.openclaw/` and should NOT be committed to the workspace repo:

- `~/.openclaw/openclaw.json` (config)
- `~/.openclaw/credentials/` (OAuth tokens, API keys)
- `~/.openclaw/agents/<agentId>/sessions/` (session transcripts + metadata)
- `~/.openclaw/skills/` (managed skills)

If you need to migrate sessions or config, copy them separately and keep them
out of version control.

## Git backup (recommended, private)

Treat the workspace as private memory. Put it in a **private** git repo so it is
backed up and recoverable.

Run these steps on the machine where the Gateway runs (that is where the
workspace lives).

### 1. Initialize the repo

If git is installed, brand-new workspaces are initialized automatically. If this
workspace is not already a repo, run:

```bash
cd ~/.openclaw/workspace
git init
git add AGENTS.md SOUL.md TOOLS.md IDENTITY.md USER.md HEARTBEAT.md memory/
git commit -m "Add agent workspace"
```

### 2. Add a private remote (beginner-friendly options)

Option A: GitHub web UI

1. Create a new **private** repository on GitHub.
2. Do not initialize with a README (avoids merge conflicts).
3. Copy the HTTPS remote URL.
4. Add the remote and push:

```bash
git branch -M main
git remote add origin <https-url>
git push -u origin main
```

Option B: GitHub CLI (`gh`)

```bash
gh auth login
gh repo create openclaw-workspace --private --source . --remote origin --push
```

Option C: GitLab web UI

1. Create a new **private** repository on GitLab.
2. Yo‘naltirish konfiguratsiyasi uchun [Channel routing](/channels/channel-routing) ga qarang.
3. Copy the HTTPS remote URL.
4. Add the remote and push:

```bash
git branch -M main
git remote add origin <https-url>
git push -u origin main
```

### 3. Ongoing updates

```bash
git status
git add .
git commit -m "Update memory"
git push
```

## Do not commit secrets

Even in a private repo, avoid storing secrets in the workspace:

- API keys, OAuth tokens, passwords, or private credentials.
- Anything under `~/.openclaw/`.
- Raw dumps of chats or sensitive attachments.

If you must store sensitive references, use placeholders and keep the real
secret elsewhere (password manager, environment variables, or `~/.openclaw/`).

Suggested `.gitignore` starter:

```gitignore
.DS_Store
.env
**/*.key
**/*.pem
**/secrets*
```

## Moving the workspace to a new machine

1. Clone the repo to the desired path (default `~/.openclaw/workspace`).
2. Set `agents.defaults.workspace` to that path in `~/.openclaw/openclaw.json`.
3. Run `openclaw setup --workspace <path>` to seed any missing files.
4. 1. Agar sizga sessiyalar kerak bo‘lsa, `~/.openclaw/agents/<agentId>/sessions/` papkasini eski mashinadan alohida nusxalab oling.

## 2) Kengaytirilgan eslatmalar

- 3. Ko‘p agentli marshrutlash har bir agent uchun turli ish maydonlaridan foydalanishi mumkin. OpenClaw **pi-mono** dan olingan bitta ichki agent runtime’ni ishga tushiradi.
- 5. Agar `agents.defaults.sandbox` yoqilgan bo‘lsa, asosiy bo‘lmagan sessiyalar `agents.defaults.sandbox.workspaceRoot` ostida sessiya-bo‘yicha sandbox ish maydonlaridan foydalanishi mumkin.
