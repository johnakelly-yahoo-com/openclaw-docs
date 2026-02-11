---
summary: "Sub-agentlar: natijalarni so‘rovchi chatga e’lon qilib, izolyatsiyalangan agent ishlarini ishga tushirish"
read_when:
  - Agent orqali fon/parallel ishni xohlaysiz
  - Siz sessions_spawn yoki sub-agent tool siyosatini o‘zgartiryapsiz
title: "Sub-agentlar"
---

# Sub-Agents

Sub-agents let you run background tasks without blocking the main conversation. When you spawn a sub-agent, it runs in its own isolated session, does its work, and announces the result back to the chat when finished.

**Use cases:**

- Research a topic while the main agent continues answering questions
- Run multiple long tasks in parallel (web scraping, code analysis, file processing)
- Delegate tasks to specialized agents in a multi-agent setup

## Quick Start

The simplest way to use sub-agents is to ask your agent naturally:

> "Spawn a sub-agent to research the latest Node.js release notes"

The agent will call the `sessions_spawn` tool behind the scenes. When the sub-agent finishes, it announces its findings back into your chat.

You can also be explicit about options:

> "Spawn a sub-agent to analyze the server logs from today. Use gpt-5.2 and set a 5-minute timeout."

## How It Works

<Steps>
  <Step title="Main agent spawns">
    The main agent calls `sessions_spawn` with a task description. The call is **non-blocking** — the main agent gets back `{ status: "accepted", runId, childSessionKey }` immediately.
  </Step>
  <Step title="Sub-agent runs in the background">
    A new isolated session is created (`agent:<agentId>:subagent:<uuid>`) on the dedicated `subagent` queue lane.
  </Step>
  <Step title="Result is announced">
    When the sub-agent finishes, it announces its findings back to the requester chat. The main agent posts a natural-language summary.
  </Step>
  <Step title="Session is archived">
    The sub-agent session is auto-archived after 60 minutes (configurable). Transcripts are preserved.
  </Step>
</Steps>

<Tip>
Each sub-agent has its **own** context and token usage. Set a cheaper model for sub-agents to save costs — see [Setting a Default Model](#setting-a-default-model) below.
</Tip>

## Configuration

Sub-agents work out of the box with no configuration. Defaults:

- Model: target agent’s normal model selection (unless `subagents.model` is set)
- Thinking: no sub-agent override (unless `subagents.thinking` is set)
- Max concurrent: 8
- Auto-archive: after 60 minutes

### Setting a Default Model

Use a cheaper model for sub-agents to save on token costs:

```json5
{
  agents: {
    defaults: {
      subagents: {
        model: "minimax/MiniMax-M2.1",
      },
    },
  },
}
```

### Setting a Default Thinking Level

```json5
{
  agents: {
    defaults: {
      subagents: {
        thinking: "low",
      },
    },
  },
}
```

### Per-Agent Overrides

In a multi-agent setup, you can set sub-agent defaults per agent:

```json5
{
  agents: {
    list: [
      {
        id: "researcher",
        subagents: {
          model: "anthropic/claude-sonnet-4",
        },
      },
      {
        id: "assistant",
        subagents: {
          model: "minimax/MiniMax-M2.1",
        },
      },
    ],
  },
}
```

### Concurrency

Control how many sub-agents can run at the same time:

```json5
{
  agents: {
    defaults: {
      subagents: {
        maxConcurrent: 4, // default: 8
      },
    },
  },
}
```

Sub-agents use a dedicated queue lane (`subagent`) separate from the main agent queue, so sub-agent runs don't block inbound replies.

### Auto-Archive

Sub-agent sessions are automatically archived after a configurable period:

```json5
{
  agents: {
    defaults: {
      subagents: {
        archiveAfterMinutes: 120, // default: 60
      },
    },
  },
}
```

<Note>
Archive renames the transcript to `*.deleted.<timestamp>` (same folder) — transcripts are preserved, not deleted. Auto-archive timers are best-effort; pending timers are lost if the gateway restarts.
</Note>

## The `sessions_spawn` Tool

This is the tool the agent calls to create sub-agents.

### Parameters

| Parameter           | Type                     | Default                               | Description                                                                                       |
| ------------------- | ------------------------ | ------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `task`              | string                   | _(required)_       | What the sub-agent should do                                                                      |
| `label`             | string                   | —                                     | Short label for identification                                                                    |
| `agentId`           | string                   | _(caller's agent)_ | Spawn under a different agent id (must be allowed)                             |
| `model`             | string                   | _(optional)_       | Override the model for this sub-agent                                                             |
| `thinking`          | string                   | _(optional)_       | Override thinking level (`off`, `low`, `medium`, `high`, etc.) |
| `runTimeoutSeconds` | number                   | `0` (no limit)     | Abort the sub-agent after N seconds                                                               |
| `cleanup`           | `"delete"` \\| `"keep"` | `"keep"`                              | `"delete"` archives immediately after announce                                                    |

### Model Resolution Order

The sub-agent model is resolved in this order (first match wins):

1. Explicit `model` parameter in the `sessions_spawn` call
2. Per-agent config: `agents.list[].subagents.model`
3. Global default: `agents.defaults.subagents.model`
4. Target agent’s normal model resolution for that new session

Thinking level is resolved in this order:

1. Explicit `thinking` parameter in the `sessions_spawn` call
2. Per-agent config: `agents.list[].subagents.thinking`
3. Global default: `agents.defaults.subagents.thinking`
4. Aks holda, sub-agentga xos fikrlashni bekor qiluvchi hech qanday sozlama qo‘llanilmaydi

<Note>
Noto‘g‘ri model qiymatlari jim tarzda o‘tkazib yuboriladi — sub-agent ogohlantirish bilan asbob natijasida keyingi yaroqli standart modelda ishga tushadi.</Note>

### Agentlararo ishga tushirish

Standart holatda, sub-agentlar faqat o‘z agent IDlari ostida ishga tushirilishi mumkin. Agentga boshqa agent IDlari ostida sub-agentlarni ishga tushirishga ruxsat berish uchun:

```json5
{
  agents: {
    list: [
      {
        id: "orchestrator",
        subagents: {
          allowAgents: ["researcher", "coder"], // yoki har qandayiga ruxsat berish uchun ["*"]
        },
      },
    ],
  },
}
```

<Tip>
`sessions_spawn` uchun hozirda qaysi agent IDlariga ruxsat berilganini aniqlash uchun `agents_list` asbobidan foydalaning.</Tip>

## Sub-agentlarni boshqarish (`/subagents`)

Joriy sessiya uchun sub-agent ishga tushirishlarini ko‘rish va boshqarish uchun `/subagents` slash-buyrug‘idan foydalaning:

| Buyruq                                     | Tavsif                                                                                      |
| ------------------------------------------ | ------------------------------------------------------------------------------------------- |
| `/subagents list`                          | Barcha sub-agent ishga tushirishlarini (faol va yakunlangan) ro‘yxatlash |
| `/subagents stop <id\\|#\\|all>`         | Ishlayotgan sub-agentni to‘xtatish                                                          |
| `/subagents log <id\\|#> [limit] [tools]` | Sub-agent transkriptini ko‘rish                                                             |
| `/subagents info <id\\|#>`                | Ishga tushirish haqida batafsil metama’lumotlarni ko‘rsatish                                |
| `/subagents send <id\\|#> <message>`      | Ishlayotgan sub-agentga xabar yuborish                                                      |

Sub-agentlarga ro‘yxat indekslari (`1`, `2`), run id prefiksi, to‘liq sessiya kaliti yoki `last` orqali murojaat qilishingiz mumkin.

<AccordionGroup>
  <Accordion title="Example: list and stop a sub-agent">
    ```
    /subagents list
    ```

    ````
    ```
    🧭 Subagents (current session)
    Active: 1 · Done: 2
    1) ✅ · research logs · 2m31s · run a1b2c3d4 · agent:main:subagent:...
    2) ✅ · check deps · 45s · run e5f6g7h8 · agent:main:subagent:...
    3) 🔄 · deploy staging · 1m12s · run i9j0k1l2 · agent:main:subagent:...
    ```
    
    ```
    /subagents stop 3
    ```
    
    ```
    ⚙️ Stop requested for deploy staging.
    ```
    ````

  </Accordion>
  <Accordion title="Example: inspect a sub-agent">
    ```
    /subagents info 1
    ```

    ````
    ```
    ℹ️ Subagent info
    Status: ✅
    Label: research logs
    Task: Research the latest server error logs and summarize findings
    Run: a1b2c3d4-...
    Session: agent:main:subagent:...
    Runtime: 2m31s
    Cleanup: keep
    Outcome: ok
    ```
    ````

  </Accordion>
  <Accordion title="Example: view sub-agent log">
    ```
    /subagents log 1 10
    ```

    ````
    Sub-agent transkriptidan oxirgi 10 ta xabarni ko‘rsatadi. Asbob chaqiruv xabarlarini ham kiritish uchun `tools` ni qo‘shing:
    
    ```
    /subagents log 1 10 tools
    ```
    ````

  </Accordion>
  <Accordion title="Example: send a follow-up message">
    ```
    /subagents send 3 "Also check the staging environment"
    ```

    ```
    Ishlayotgan sub-agent sessiyasiga xabar yuboradi va javobni 30 soniyagacha kutadi.
    ```

  </Accordion>
</AccordionGroup>

## E’lon qilish (Natijalar qanday qaytadi)

Sub-agent yakunlanganda, u **e’lon qilish** bosqichidan o‘tadi:

1. Sub-agentning yakuniy javobi qayd etiladi
2. Natija, holat va statistika bilan asosiy agent sessiyasiga xulosa xabari yuboriladi
3. Asosiy agent chatga tabiiy tilidagi xulosani joylaydi

E’lon qilingan javoblar mavjud bo‘lsa, thread/mavzu marshrutlashini saqlab qoladi (Slack thread’lari, Telegram topic’lari, Matrix thread’lari).

### E’lon statistikasi

Har bir e’lon quyidagilarni o‘z ichiga olgan statistika satrini o‘z ichiga oladi:

- Ishlash davomiyligi
- Token usage (input/output/total)
- Taxminiy xarajat (model narxlari `models.providers.*.models[].cost` orqali sozlanganda)
- Sessiya kaliti, sessiya IDsi va transkript yo‘li

### E’lon holati

E’lon xabari ishga tushirish natijasidan kelib chiqqan holatni o‘z ichiga oladi (model chiqishidan emas):

- **muvaffaqiyatli yakun** (`ok`) — vazifa odatdagidek bajarildi
- **xato** — vazifa bajarilmadi (tafsilotlar eslatmalarda)
- **vaqt tugadi** — vazifa `runTimeoutSeconds` dan oshib ketdi
- **noma’lum** — holatni aniqlab bo‘lmadi

<Tip>
Agar foydalanuvchiga ko‘rinadigan e’lon talab etilmasa, asosiy agentning xulosa bosqichi `NO_REPLY` ni qaytarishi mumkin va hech narsa joylanmaydi.
This is different from `ANNOUNCE_SKIP`, which is used in agent-to-agent announce flow (`sessions_send`).
</Tip>

## Tool Policy

By default, sub-agents get **all tools except** a set of denied tools that are unsafe or unnecessary for background tasks:

<AccordionGroup>
  <Accordion title="Default denied tools">
    | Denied tool | Reason |
    |-------------|--------|
    | `sessions_list` | Session management — main agent orchestrates |
    | `sessions_history` | Session management — main agent orchestrates |
    | `sessions_send` | Session management — main agent orchestrates |
    | `sessions_spawn` | No nested fan-out (sub-agents cannot spawn sub-agents) |
    | `gateway` | System admin — dangerous from sub-agent |
    | `agents_list` | System admin |
    | `whatsapp_login` | Interactive setup — not a task |
    | `session_status` | Status/scheduling — main agent coordinates |
    | `cron` | Status/scheduling — main agent coordinates |
    | `memory_search` | Pass relevant info in spawn prompt instead |
    | `memory_get` | Pass relevant info in spawn prompt instead |
  </Accordion>
</AccordionGroup>

### Customizing Sub-Agent Tools

You can further restrict sub-agent tools:

```json5
{
  tools: {
    subagents: {
      tools: {
        // deny always wins over allow
        deny: ["browser", "firecrawl"],
      },
    },
  },
}
```

To restrict sub-agents to **only** specific tools:

```json5
{
  tools: {
    subagents: {
      tools: {
        allow: ["read", "exec", "process", "write", "edit", "apply_patch"],
        // deny still wins if set
      },
    },
  },
}
```

<Note>
Custom deny entries are **added to** the default deny list. If `allow` is set, only those tools are available (the default deny list still applies on top).
</Note>

## Autentifikatsiya

Sub-agent auth **sessiya turi** bo‘yicha emas, balki **agent id** bo‘yicha hal qilinadi:

- The auth store is loaded from the target agent's `agentDir`
- The main agent's auth profiles are merged in as a **fallback** (agent profiles win on conflicts)
- The merge is additive — main profiles are always available as fallbacks

<Note>
Fully isolated auth per sub-agent is not currently supported.
</Note>

## Context and System Prompt

Sub-agents receive a reduced system prompt compared to the main agent:

- **Included:** Tooling, Workspace, Runtime sections, plus `AGENTS.md` and `TOOLS.md`
- **Not included:** `SOUL.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`, `BOOTSTRAP.md`

The sub-agent also receives a task-focused system prompt that instructs it to stay focused on the assigned task, complete it, and not act as the main agent.

## Stopping Sub-Agents

| Method                 | Effect                                                                    |
| ---------------------- | ------------------------------------------------------------------------- |
| `/stop` in the chat    | Aborts the main session **and** all active sub-agent runs spawned from it |
| `/subagents stop <id>` | Stops a specific sub-agent without affecting the main session             |
| `runTimeoutSeconds`    | Automatically aborts the sub-agent run after the specified time           |

<Note>
`runTimeoutSeconds` does **not** auto-archive the session. The session remains until the normal archive timer fires.
</Note>

## Full Configuration Example

<Accordion title="Complete sub-agent configuration">
```json5
{
  agents: {
    defaults: {
      model: { primary: "anthropic/claude-sonnet-4" },
      subagents: {
        model: "minimax/MiniMax-M2.1",
        thinking: "low",
        maxConcurrent: 4,
        archiveAfterMinutes: 30,
      },
    },
    list: [
      {
        id: "main",
        default: true,
        name: "Personal Assistant",
      },
      {
        id: "ops",
        name: "Ops Agent",
        subagents: {
          model: "anthropic/claude-sonnet-4",
          allowAgents: ["main"], // ops can spawn sub-agents under "main"
        },
      },
    ],
  },
  tools: {
    subagents: {
      tools: {
        deny: ["browser"], // sub-agents can't use the browser
      },
    },
  },
}
```
</Accordion>

## Limitations

<Warning>
- **Best-effort announce:** If the gateway restarts, pending announce work is lost.
- **No nested spawning:** Sub-agents cannot spawn their own sub-agents.
- **Shared resources:** Sub-agents share the gateway process; use `maxConcurrent` as a safety valve.
- **Auto-archive is best-effort:** Pending archive timers are lost on gateway restart.
</Warning>

## See Also

- [Session Tools](/concepts/session-tool) — details on `sessions_spawn` and other session tools
- [Multi-Agent Sandbox and Tools](/tools/multi-agent-sandbox-tools) — per-agent tool restrictions and sandboxing
- [Configuration](/gateway/configuration) — `agents.defaults.subagents` reference
- [Queue](/concepts/queue) — how the `subagent` lane works
