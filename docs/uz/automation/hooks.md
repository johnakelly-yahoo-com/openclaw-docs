---
summary: "15. Sinov"
read_when:
  - "16. Kuzatilayotgan inbox’ga xabar yuboring:"
  - 17. gog gmail send \
title: "  --account openclaw@gmail.com \\"
---

# --to openclaw@gmail.com \

\--subject "watch test" \   --body "ping"

## 18. Watch holati va tarixini tekshiring:

19. gog gmail watch status --account openclaw@gmail.com
    gog gmail history --account openclaw@gmail.com --since <historyId> 20. Nosozliklarni bartaraf etish

- 21. `Invalid topicName`: loyiha nomuvofiqligi (topic OAuth client loyihasida emas).
- 22. `User not authorized`: topic’da `roles/pubsub.publisher` yetishmaydi. 23. Bo‘sh xabarlar: Gmail push faqat `historyId` beradi; `gog gmail history` orqali olib keling.

24. Tozalash

25. gog gmail watch stop --account openclaw@gmail.com
    gcloud pubsub subscriptions delete gog-gmail-watch-push
    gcloud pubsub topics delete gog-gmail-watch

- 26. Hooks: buyruqlar va hayotiy sikl hodisalari uchun hodisaga asoslangan avtomatlashtirish
- 27. Siz /new, /reset, /stop va agent hayotiy sikli hodisalari uchun hodisaga asoslangan avtomatlashtirishni xohlaysiz
- 28. Siz hook’larni yaratmoqchi, o‘rnatmoqchi yoki nosozliklarni tuzatmoqchisiz
- 29. Hooks

30. Hooks 31. Hooks agent buyruqlari va hodisalariga javoban harakatlarni avtomatlashtirish uchun kengaytiriladigan hodisaga asoslangan tizimni taqdim etadi.

## 32. Hooks kataloglardan avtomatik aniqlanadi va CLI buyruqlari orqali boshqariladi, xuddi OpenClaw’dagi skill’lar kabi.

33. Yo‘naltiruvchi ma’lumot

- 34. Hooks — biror narsa sodir bo‘lganda ishga tushadigan kichik skriptlar.
- 35. Ikki xil turi mavjud:
- Trigger custom automations on agent lifecycle events
- Extend OpenClaw's behavior without modifying core code

## 12. Boshlash

### Bundled Hooks

OpenClaw ships with four bundled hooks that are automatically discovered:

- **💾 session-memory**: Saves session context to your agent workspace (default `~/.openclaw/workspace/memory/`) when you issue `/new`
- **📝 command-logger**: Logs all command events to `~/.openclaw/logs/commands.log`
- 13. **🚀 boot-md**: Shlyuz ishga tushganda `BOOT.md` ni ishga tushiradi (ichki hooklar yoqilgan bo‘lishi kerak)
- **😈 soul-evil**: Swaps injected `SOUL.md` content with `SOUL_EVIL.md` during a purge window or by random chance

List available hooks:

```bash
openclaw hooks list
```

14. Hookni yoqish:

```bash
15. openclaw hooks enable session-memory
```

Check hook status:

```bash
openclaw hooks check
```

Get detailed information:

```bash
openclaw hooks info session-memory
```

### 16. Onboarding

17. Onboarding paytida (`openclaw onboard`), sizga tavsiya etilgan hooklarni yoqish taklif etiladi. The wizard automatically discovers eligible hooks and presents them for selection.

## Hook Discovery

Hooks are automatically discovered from three directories (in order of precedence):

1. **Workspace hooks**: `<workspace>/hooks/` (per-agent, highest precedence)
2. **Managed hooks**: `~/.openclaw/hooks/` (user-installed, shared across workspaces)
3. **Bundled hooks**: `<openclaw>/dist/hooks/bundled/` (shipped with OpenClaw)

Managed hook directories can be either a **single hook** or a **hook pack** (package directory).

Each hook is a directory containing:

```
my-hook/
├── HOOK.md          # Metadata + documentation
└── handler.ts       # Handler implementation
```

## 18. Hook paketlari (npm/arxivlar)

Hook packs are standard npm packages that export one or more hooks via `openclaw.hooks` in
`package.json`. Install them with:

```bash
openclaw hooks install <path-or-spec>
```

Example `package.json`:

```json
{
  "name": "@acme/my-hooks",
  "version": "0.1.0",
  "openclaw": {
    "hooks": ["./hooks/my-hook", "./hooks/other-hook"]
  }
}
```

Each entry points to a hook directory containing `HOOK.md` and `handler.ts` (or `index.ts`).
Hook packs can ship dependencies; they will be installed under `~/.openclaw/hooks/<id>`.

## Hook Structure

### HOOK.md Format

The `HOOK.md` file contains metadata in YAML frontmatter plus Markdown documentation:

```markdown
---
name: my-hook
description: "Short description of what this hook does"
homepage: https://docs.openclaw.ai/hooks#my-hook
metadata:
  { "openclaw": { "emoji": "🔗", "events": ["command:new"], "requires": { "bins": ["node"] } } }
---

# My Hook

Detailed documentation goes here...

## What It Does

- Listens for `/new` commands
- Performs some action
- Logs the result

## Requirements

- Node.js must be installed

## Configuration

No configuration needed.
```

### Metadata Fields

The `metadata.openclaw` object supports:

- **`emoji`**: Display emoji for CLI (e.g., `"💾"`)
- **`events`**: Array of events to listen for (e.g., `["command:new", "command:reset"]`)
- **`export`**: Named export to use (defaults to `"default"`)
- **`homepage`**: Documentation URL
- **`requires`**: Optional requirements
  - **`bins`**: Required binaries on PATH (e.g., `["git", "node"]`)
  - **`anyBins`**: At least one of these binaries must be present
  - **`env`**: Required environment variables
  - **`config`**: Required config paths (e.g., `["workspace.dir"]`)
  - **`os`**: Required platforms (e.g., `["darwin", "linux"]`)
- **`always`**: Bypass eligibility checks (boolean)
- **`install`**: Installation methods (for bundled hooks: `[{"id":"bundled","kind":"bundled"}]`)

### Handler Implementation

The `handler.ts` file exports a `HookHandler` function:

```typescript
import type { HookHandler } from "../../src/hooks/hooks.js";

const myHandler: HookHandler = async (event) => {
  // Only trigger on 'new' command
  if (event.type !== "command" || event.action !== "new") {
    return;
  }

  console.log(`[my-hook] New command triggered`);
  console.log(`  Session: ${event.sessionKey}`);
  console.log(`  Timestamp: ${event.timestamp.toISOString()}`);

  // Your custom logic here

  // Optionally send message to user
  event.messages.push("✨ My hook executed!");
};

export default myHandler;
```

#### Event Context

Each event includes:

```typescript
{
  type: 'command' | 'session' | 'agent' | 'gateway',
  action: string,              // e.g., 'new', 'reset', 'stop'
  sessionKey: string,          // Session identifier
  timestamp: Date,             // When the event occurred
  messages: string[],          // Push messages here to send to user
  context: {
    sessionEntry?: SessionEntry,
    sessionId?: string,
    sessionFile?: string,
    commandSource?: string,    // e.g., 'whatsapp', 'telegram'
    senderId?: string,
    workspaceDir?: string,
    bootstrapFiles?: WorkspaceBootstrapFile[],
    cfg?: OpenClawConfig
  }
}
```

## Event Types

### Command Events

Triggered when agent commands are issued:

- **`command`**: All command events (general listener)
- **`command:new`**: When `/new` command is issued
- **`command:reset`**: When `/reset` command is issued
- **`command:stop`**: When `/stop` command is issued

### Agent Events

- **`agent:bootstrap`**: Before workspace bootstrap files are injected (hooks may mutate `context.bootstrapFiles`)

### Gateway Events

Triggered when the gateway starts:

- **`gateway:startup`**: After channels start and hooks are loaded

### Tool Result Hooks (Plugin API)

These hooks are not event-stream listeners; they let plugins synchronously adjust tool results before OpenClaw persists them.

- **`tool_result_persist`**: transform tool results before they are written to the session transcript. Must be synchronous; return the updated tool result payload or `undefined` to keep it as-is. See [Agent Loop](/concepts/agent-loop).

### Future Events

Planned event types:

- **`session:start`**: When a new session begins
- **`session:end`**: When a session ends
- **`agent:error`**: When an agent encounters an error
- **`message:sent`**: When a message is sent
- **`message:received`**: When a message is received

## Creating Custom Hooks

### 1. Choose Location

- **Workspace hooks** (`<workspace>/hooks/`): Per-agent, highest precedence
- **Managed hooks** (`~/.openclaw/hooks/`): Shared across workspaces

### 2. Create Directory Structure

```bash
mkdir -p ~/.openclaw/hooks/my-hook
cd ~/.openclaw/hooks/my-hook
```

### 3. Create HOOK.md

```markdown
---
name: my-hook
description: "Does something useful"
metadata: { "openclaw": { "emoji": "🎯", "events": ["command:new"] } }
---

# My Custom Hook

This hook does something useful when you issue `/new`.
```

### 4. Create handler.ts

```typescript
import type { HookHandler } from "../../src/hooks/hooks.js";

const handler: HookHandler = async (event) => {
  if (event.type !== "command" || event.action !== "new") {
    return;
  }

  console.log("[my-hook] Running!");
  // Your logic here
};

export default handler;
```

### 5. Enable and Test

```bash
# Verify hook is discovered
openclaw hooks list

# Enable it
openclaw hooks enable my-hook

# Restart your gateway process (menu bar app restart on macOS, or restart your dev process)

# Trigger the event
# Send /new via your messaging channel
```

## Configuration

### New Config Format (Recommended)

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "session-memory": { "enabled": true },
        "command-logger": { "enabled": false }
      }
    }
  }
}
```

### Per-Hook Configuration

Hooks can have custom configuration:

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "my-hook": {
          "enabled": true,
          "env": {
            "MY_CUSTOM_VAR": "value"
          }
        }
      }
    }
  }
}
```

### Extra Directories

Load hooks from additional directories:

```json
19. {
  "hooks": {
    "internal": {
      "enabled": true,
      "load": {
        "extraDirs": ["/path/to/more/hooks"]
      }
    }
  }
}
```

### Legacy Config Format (Still Supported)

The old config format still works for backwards compatibility:

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "handlers": [
        {
          "event": "command:new",
          "module": "./hooks/handlers/my-handler.ts",
          "export": "default"
        }
      ]
    }
  }
}
```

**Migration**: Use the new discovery-based system for new hooks. Legacy handlers are loaded after directory-based hooks.

## CLI Commands

### List Hooks

```bash
# List all hooks
openclaw hooks list

# Show only eligible hooks
openclaw hooks list --eligible

# Verbose output (show missing requirements)
openclaw hooks list --verbose

# JSON output
openclaw hooks list --json
```

### Hook Information

```bash
20. # Hook haqida batafsil ma’lumotni ko‘rsatish
openclaw hooks info session-memory

# JSON chiqishi
openclaw hooks info session-memory --json
```

### Check Eligibility

```bash
# Show eligibility summary
openclaw hooks check

# JSON output
openclaw hooks check --json
```

### Enable/Disable

```bash
# Enable a hook
openclaw hooks enable session-memory

# Disable a hook
openclaw hooks disable command-logger
```

## Bundled hook reference

### 21. session-memory

Saves session context to memory when you issue `/new`.

**Events**: `command:new`

**Requirements**: `workspace.dir` must be configured

**Output**: `<workspace>/memory/YYYY-MM-DD-slug.md` (defaults to `~/.openclaw/workspace`)

**What it does**:

1. Uses the pre-reset session entry to locate the correct transcript
2. Extracts the last 15 lines of conversation
3. Uses LLM to generate a descriptive filename slug
4. Saves session metadata to a dated memory file

**Example output**:

```markdown
# Session: 2026-01-16 14:30:00 UTC

- **Session Key**: agent:main:main
- **Session ID**: abc123def456
- **Source**: telegram
```

**Filename examples**:

- `2026-01-16-vendor-pitch.md`
- `2026-01-16-api-design.md`
- `2026-01-16-1430.md` (fallback timestamp if slug generation fails)

**Enable**:

```bash
openclaw hooks enable session-memory
```

### command-logger

Logs all command events to a centralized audit file.

**Events**: `command`

**Requirements**: None

**Output**: `~/.openclaw/logs/commands.log`

**What it does**:

1. Captures event details (command action, timestamp, session key, sender ID, source)
2. JSONL formatida log fayliga qo‘shadi
3. Fon rejimida jim ishlaydi

**Misol log yozuvlari**:

```jsonl
{"timestamp":"2026-01-16T14:30:00.000Z","action":"new","sessionKey":"agent:main:main","senderId":"+1234567890","source":"telegram"}
{"timestamp":"2026-01-16T15:45:22.000Z","action":"stop","sessionKey":"agent:main:main","senderId":"user@example.com","source":"whatsapp"}
```

**Loglarni ko‘rish**:

```bash
# View recent commands
tail -n 20 ~/.openclaw/logs/commands.log

# Pretty-print with jq
cat ~/.openclaw/logs/commands.log | jq .

# Filter by action
grep '"action":"new"' ~/.openclaw/logs/commands.log | jq .
```

**Yoqish**:

```bash
openclaw hooks enable command-logger
```

### soul-evil

Purge oynasi davomida yoki tasodifiy ehtimol bilan kiritilgan `SOUL.md` tarkibini `SOUL_EVIL.md` bilan almashtiradi.

**Hodisalar**: `agent:bootstrap`

**Hujjatlar**: [SOUL Evil Hook](/hooks/soul-evil)

**Chiqish**: Hech qanday fayl yozilmaydi; almashtirishlar faqat xotirada amalga oshadi.

**Yoqish**:

```bash
openclaw hooks enable soul-evil
```

**Konfiguratsiya**:

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "soul-evil": {
          "enabled": true,
          "file": "SOUL_EVIL.md",
          "chance": 0.1,
          "purge": { "at": "21:00", "duration": "15m" }
        }
      }
    }
  }
}
```

### boot-md

Gateway ishga tushganda (kanallar ishga tushgandan so‘ng) `BOOT.md` ni ishga tushiradi.
Buning ishlashi uchun ichki hooklar yoqilgan bo‘lishi kerak.

**Hodisalar**: `gateway:startup`

**Talablar**: `workspace.dir` sozlangan bo‘lishi kerak

**Nima qiladi**:

1. Workspace’ingizdan `BOOT.md` ni o‘qiydi
2. Ko‘rsatmalarni agent runner orqali bajaradi
3. So‘ralgan barcha tashqi xabarlarni message tool orqali yuboradi

**Yoqish**:

```bash
openclaw hooks enable boot-md
```

## Eng Yaxshi Amaliyotlar

### Handlerlarni Tez Saqlang

Hooklar buyruqlarni qayta ishlash jarayonida ishlaydi. Ularni yengil saqlang:

```typescript
// ✓ Good - async work, returns immediately
const handler: HookHandler = async (event) => {
  void processInBackground(event); // Fire and forget
};

// ✗ Bad - blocks command processing
const handler: HookHandler = async (event) => {
  await slowDatabaseQuery(event);
  await evenSlowerAPICall(event);
};
```

### Xatolarni Muloyimlik Bilan Qayta Ishlang

Xavfli amallarni har doim o‘rab oling:

```typescript
const handler: HookHandler = async (event) => {
  try {
    await riskyOperation(event);
  } catch (err) {
    console.error("[my-handler] Failed:", err instanceof Error ? err.message : String(err));
    // Don't throw - let other handlers run
  }
};
```

### Hodisalarni Erta Filtrlash

Agar hodisa mos kelmasa, darhol qayting:

```typescript
const handler: HookHandler = async (event) => {
  // Only handle 'new' commands
  if (event.type !== "command" || event.action !== "new") {
    return;
  }

  // Your logic here
};
```

### Aniq Hodisa Kalitlaridan Foydalaning

Imkon bo‘lsa, metadata’da aniq hodisalarni ko‘rsating:

```yaml
metadata: { "openclaw": { "events": ["command:new"] } } # Specific
```

O‘rniga:

```yaml
metadata: { "openclaw": { "events": ["command"] } } # General - more overhead
```

## Nosozliklarni Tuzatish

### Hook Loglashni Yoqish

Gateway ishga tushishda hook yuklanishini loglaydi:

```
Registered hook: session-memory -> command:new
Registered hook: command-logger -> command
Registered hook: boot-md -> gateway:startup
```

### Kashfiyotni Tekshirish

Topilgan barcha hooklarni ro‘yxatlash:

```bash
1. openclaw hooks list --verbose
```

### 2. Roʻyxatdan oʻtishni tekshiring

3. Handler ichida, chaqirilgan paytini log qiling:

```typescript
4. const handler: HookHandler = async (event) => {
  console.log("[my-handler] Triggered:", event.type, event.action);
  // Sizning mantiqingiz
};
```

### 5. Moslikni tekshiring

6. Hook nima uchun mos emasligini tekshiring:

```bash
7. openclaw hooks info my-hook
```

8. Chiqishda yetishmayotgan talablarni qidiring.

## 9. Test qilish

### 10. Gateway loglari

11. Hook bajarilishini ko‘rish uchun gateway loglarini kuzating:

```bash
12. # macOS
./scripts/clawlog.sh -f

# Boshqa platformalar
tail -f ~/.openclaw/gateway.log
```

### 13. Hook’larni bevosita test qilish

14. Handler’laringizni alohida holatda test qiling:

```typescript
15. import { test } from "vitest";
import { createHookEvent } from "./src/hooks/hooks.js";
import myHandler from "./hooks/my-hook/handler.js";

test("my handler works", async () => {
  const event = createHookEvent("command", "new", "test-session", {
    foo: "bar",
  });

  await myHandler(event);

  // Yon ta’sirlarni tekshirish
});
```

## 16. Arxitektura

### 17. Asosiy komponentlar

- 18. **`src/hooks/types.ts`**: Tip ta’riflari
- 19. **`src/hooks/workspace.ts`**: Kataloglarni skanerlash va yuklash
- 20. **`src/hooks/frontmatter.ts`**: HOOK.md metadata’ni ajratib olish
- 21. **`src/hooks/config.ts`**: Moslikni tekshirish
- 22. **`src/hooks/hooks-status.ts`**: Holatni hisobot qilish
- 23. **`src/hooks/loader.ts`**: Dinamik modul yuklovchi
- 24. **`src/cli/hooks-cli.ts`**: CLI buyruqlari
- 25. **`src/gateway/server-startup.ts`**: Gateway ishga tushganda hook’larni yuklaydi
- 26. **`src/auto-reply/reply/commands-core.ts`**: Buyruq hodisalarini ishga tushiradi

### 27. Aniqlash oqimi

```
28. Gateway ishga tushishi
    ↓
Kataloglarni skanerlash (workspace → managed → bundled)
    ↓
HOOK.md fayllarini tahlil qilish
    ↓
Moslikni tekshirish (binlar, env, config, OS)
    ↓
Mos hook’lardan handler’larni yuklash
    ↓
Hodisalar uchun handler’larni ro‘yxatdan o‘tkazish
```

### 29. Hodisa oqimi

```
30. Foydalanuvchi /new yuboradi
    ↓
Buyruqni tekshirish
    ↓
Hook hodisasini yaratish
    ↓
Hook’ni ishga tushirish (barcha ro‘yxatdan o‘tgan handler’lar)
    ↓
Buyruqni qayta ishlash davom etadi
    ↓
Sessiyani qayta o‘rnatish
```

## 31. Nosozliklarni bartaraf etish

### 32. Hook topilmadi

1. 33. Katalog tuzilmasini tekshiring:

   ```bash
   34. ls -la ~/.openclaw/hooks/my-hook/
   # Quyidagilar bo‘lishi kerak: HOOK.md, handler.ts
   ```

2. 35. HOOK.md formatini tekshiring:

   ```bash
   36. cat ~/.openclaw/hooks/my-hook/HOOK.md
   # name va metadata’ga ega YAML frontmatter bo‘lishi kerak
   ```

3. 37. Barcha aniqlangan hook’larni ro‘yxatlang:

   ```bash
   38. openclaw hooks list
   ```

### 39) Hook mos emas

40. Talablarni tekshiring:

```bash
41. openclaw hooks info my-hook
```

42. Yetishmayotganlarni qidiring:

- 43. Binariylar (PATH’ni tekshiring)
- 44. Muhit o‘zgaruvchilari
- 45. Konfiguratsiya qiymatlari
- 46. OS mosligi

### 47. Hook bajarilmayapti

1. 48. Hook yoqilganligini tekshiring:

   ```bash
   49. openclaw hooks list
   # Yoqilgan hook’lar yonida ✓ bo‘lishi kerak
   ```

2. 50. Hook’lar qayta yuklanishi uchun gateway jarayonini qayta ishga tushiring.

3. Check gateway logs for errors:

   ```bash
   ./scripts/clawlog.sh | grep hook
   ```

### Handler Errors

Check for TypeScript/import errors:

```bash
# Test import directly
node -e "import('./path/to/handler.ts').then(console.log)"
```

## Migration Guide

### From Legacy Config to Discovery

**Before**:

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "handlers": [
        {
          "event": "command:new",
          "module": "./hooks/handlers/my-handler.ts"
        }
      ]
    }
  }
}
```

**After**:

1. Create hook directory:

   ```bash
   mkdir -p ~/.openclaw/hooks/my-hook
   mv ./hooks/handlers/my-handler.ts ~/.openclaw/hooks/my-hook/handler.ts
   ```

2. Create HOOK.md:

   ```markdown
   ---
   name: my-hook
   description: "My custom hook"
   metadata: { "openclaw": { "emoji": "🎯", "events": ["command:new"] } }
   ---

   # My Hook

   Does something useful.
   ```

3. Update config:

   ```json
   {
     "hooks": {
       "internal": {
         "enabled": true,
         "entries": {
           "my-hook": { "enabled": true }
         }
       }
     }
   }
   ```

4. Verify and restart your gateway process:

   ```bash
   openclaw hooks list
   # Should show: 🎯 my-hook ✓
   ```

**Benefits of migration**:

- Automatic discovery
- CLI management
- Eligibility checking
- Better documentation
- Consistent structure

## 22. Shuningdek qarang

- [CLI Reference: hooks](/cli/hooks)
- [Bundled Hooks README](https://github.com/openclaw/openclaw/tree/main/src/hooks/bundled)
- [Webhook Hooks](/automation/webhook)
- [Configuration](/gateway/configuration#hooks)
