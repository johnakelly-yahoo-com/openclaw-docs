---
summary: "How OpenClaw sandboxing works: modes, scopes, workspace access, and images"
title: Sandboxing
read_when: "You want a dedicated explanation of sandboxing or need to tune agents.defaults.sandbox."
status: active
---

# Sandboxing

OpenClaw can run **tools inside Docker containers** to reduce blast radius.
This is **optional** and controlled by configuration (`agents.defaults.sandbox` or
`agents.list[].sandbox`). If sandboxing is off, tools run on the host.
The Gateway stays on the host; tool execution runs in an isolated sandbox
when enabled.

This is not a perfect security boundary, but it materially limits filesystem
and process access when the model does something dumb.

## What gets sandboxed

- Tool execution (`exec`, `read`, `write`, `edit`, `apply_patch`, `process`, etc.).
- 1. Ixtiyoriy sandboxlangan brauzer (`agents.defaults.sandbox.browser`).
  - By default, the sandbox browser auto-starts (ensures CDP is reachable) when the browser tool needs it.
    Configure via `agents.defaults.sandbox.browser.autoStart` and `agents.defaults.sandbox.browser.autoStartTimeoutMs`.
  - `agents.defaults.sandbox.browser.allowHostControl` lets sandboxed sessions target the host browser explicitly.
  - Optional allowlists gate `target: "custom"`: `allowedControlUrls`, `allowedControlHosts`, `allowedControlPorts`.

Not sandboxed:

- The Gateway process itself.
- Any tool explicitly allowed to run on the host (e.g. `tools.elevated`).
  - **Elevated exec runs on the host and bypasses sandboxing.**
  - If sandboxing is off, `tools.elevated` does not change execution (already on host). See [Elevated Mode](/tools/elevated).

## Modes

`agents.defaults.sandbox.mode` controls **when** sandboxing is used:

- `"off"`: no sandboxing.
- `"non-main"`: sandbox only **non-main** sessions (default if you want normal chats on host).
- `"all"`: every session runs in a sandbox.
  Note: `"non-main"` is based on `session.mainKey` (default `"main"`), not agent id.
  Group/channel sessions use their own keys, so they count as non-main and will be sandboxed.

## Scope

`agents.defaults.sandbox.scope` controls **how many containers** are created:

- `"session"` (default): one container per session.
- `"agent"`: one container per agent.
- `"shared"`: one container shared by all sandboxed sessions.

## Workspace access

`agents.defaults.sandbox.workspaceAccess` controls **what the sandbox can see**:

- `"none"` (default): tools see a sandbox workspace under `~/.openclaw/sandboxes`.
- `"ro"`: mounts the agent workspace read-only at `/agent` (disables `write`/`edit`/`apply_patch`).
- `"rw"`: mounts the agent workspace read/write at `/workspace`.

Inbound media is copied into the active sandbox workspace (`media/inbound/*`).
Skills note: the `read` tool is sandbox-rooted. With `workspaceAccess: "none"`,
OpenClaw mirrors eligible skills into the sandbox workspace (`.../skills`) so
they can be read. With `"rw"`, workspace skills are readable from
`/workspace/skills`.

## Custom bind mounts

`agents.defaults.sandbox.docker.binds` mounts additional host directories into the container.
Format: `host:container:mode` (e.g., `"/home/user/source:/source:rw"`).

Global and per-agent binds are **merged** (not replaced). Under `scope: "shared"`, per-agent binds are ignored.

Example (read-only source + docker socket):

```json5
{
  agents: {
    defaults: {
      sandbox: {
        docker: {
          binds: ["/home/user/source:/source:ro", "/var/run/docker.sock:/var/run/docker.sock"],
        },
      },
    },
    list: [
      {
        id: "build",
        sandbox: {
          docker: {
            binds: ["/mnt/cache:/cache:rw"],
          },
        },
      },
    ],
  },
}
```

1. Xavfsizlik bo‘yicha eslatmalar:

- 2. Bindlar sandbox fayl tizimini chetlab o‘tadi: ular siz belgilagan rejimda (`:ro` yoki `:rw`) xost yo‘llarini ochib beradi.
- 3. Sezgir mountlar (masalan, `docker.sock`, sirlar, SSH kalitlari) mutlaqo zarur bo‘lmaguncha `:ro` bo‘lishi kerak.
- 2. Agar ish maydoniga faqat o‘qish huquqi kerak bo‘lsa, `workspaceAccess: "ro"` bilan birlashtiring; bog‘lash rejimlari mustaqil qoladi.
- 5. Bindlar tool policy va elevated exec bilan qanday o‘zaro ishlashini bilish uchun [Sandbox vs Tool Policy vs Elevated](/gateway/sandbox-vs-tool-policy-vs-elevated) ga qarang.

## 6. Image’lar + sozlash

7. Standart image: `openclaw-sandbox:bookworm-slim`

8. Uni bir marta build qiling:

```bash
9. scripts/sandbox-setup.sh
```

10. Eslatma: standart image **Node** ni o‘z ichiga olmaydi. 11. Agar skill’ga Node (yoki boshqa runtime’lar) kerak bo‘lsa, yoki maxsus image pishiring, yoki `sandbox.docker.setupCommand` orqali o‘rnating (tarmoq chiqishi + yoziladigan root + root foydalanuvchi talab etiladi).

12. Sandboxlangan brauzer image’i:

```bash
3. scripts/sandbox-browser-setup.sh
```

14. Standart holatda sandbox konteynerlar **tarmoqsiz** ishlaydi.
15. `agents.defaults.sandbox.docker.network` bilan bekor qiling.

16. Docker o‘rnatmalari va konteynerlangan gateway shu yerda joylashgan:
    [Docker](/install/docker)

## 17. setupCommand (konteynerni bir martalik sozlash)

18. `setupCommand` sandbox konteyneri yaratilgandan so‘ng **bir marta** ishlaydi (har bir ishga tushishda emas).
19. U konteyner ichida `sh -lc` orqali bajariladi.

20. Yo‘llar:

- 21. Global: `agents.defaults.sandbox.docker.setupCommand`
- 22. Har bir agent uchun: `agents.list[].sandbox.docker.setupCommand`

23. Keng tarqalgan xatolar:

- 24. Standart `docker.network` — `"none"` (chiqish yo‘q), shuning uchun paket o‘rnatishlar muvaffaqiyatsiz bo‘ladi.
- 25. `readOnlyRoot: true` yozishni taqiqlaydi; `readOnlyRoot: false` ga o‘rnating yoki maxsus image pishiring.
- 26. Paket o‘rnatish uchun `user` root bo‘lishi kerak (`user` ni olib tashlang yoki `user: "0:0"` deb belgilang).
- 27. Sandbox exec xostning `process.env` ini **meros qilib olmaydi**. 28. Skill API kalitlari uchun
      `agents.defaults.sandbox.docker.env` (yoki maxsus image) dan foydalaning.

## 29. Tool policy + chiqish yo‘llari

30. Tool’larni ruxsat/taqiqlash siyosatlari sandbox qoidalaridan oldin hamon amal qiladi. 31. Agar biror tool global yoki agent darajasida taqiqlangan bo‘lsa, sandboxlash uni qayta yoqmaydi.

4. `tools.elevated` — xostda `exec`ni ishga tushiradigan aniq chiqish yo‘li.
5. `/exec` direktivalari faqat vakolatli jo‘natuvchilar uchun amal qiladi va sessiya bo‘yicha saqlanadi; `exec`ni butunlay o‘chirish uchun tool policy deny’dan foydalaning (qarang [Sandbox vs Tool Policy vs Elevated](/gateway/sandbox-vs-tool-policy-vs-elevated)).

34. Debugging:

- 35. Samarali sandbox rejimi, tool policy va fix-it konfiguratsiya kalitlarini ko‘rish uchun `openclaw sandbox explain` dan foydalaning.
- 36. “Nega bu bloklangan?” degan mental model uchun [Sandbox vs Tool Policy vs Elevated](/gateway/sandbox-vs-tool-policy-vs-elevated) ga qarang.
  37. Uni qattiq yopiq holda saqlang.

## 38. Multi-agent override’lar

39. Har bir agent sandbox + tool’larni bekor qilishi mumkin:
    `agents.list[].sandbox` va `agents.list[].tools` (shuningdek sandbox tool policy uchun `agents.list[].tools.sandbox.tools`).
40. Ustuvorliklar uchun [Multi-Agent Sandbox & Tools](/tools/multi-agent-sandbox-tools) ga qarang.

## 41. Minimal yoqish misoli

```json5
42. {
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main",
        scope: "session",
        workspaceAccess: "none",
      },
    },
  },
}
```

## 43. Bog‘liq hujjatlar

- 44. [Sandbox Configuration](/gateway/configuration#agentsdefaults-sandbox)
- 45. [Multi-Agent Sandbox & Tools](/tools/multi-agent-sandbox-tools)
- 46. [Security](/gateway/security)
