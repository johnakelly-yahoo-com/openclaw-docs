---
summary: "Har bir agent uchun sandbox + vosita cheklovlari, ustuvorlik va misollar"
title: Ko‘p agentli sandbox va vositalar
read_when: "Siz ko‘p agentli shlyuzda har bir agent uchun alohida sandbox yoki har bir agent uchun vositalarni ruxsat berish/taqiqlash siyosatini xohlaysiz."
status: faol
---

# Ko‘p agentli sandbox va vositalarni sozlash

## Umumiy ko‘rinish

Ko‘p agentli sozlamada har bir agent endi quyidagilarga ega bo‘lishi mumkin:

- **Sandbox konfiguratsiyasi** (`agents.list[].sandbox` `agents.defaults.sandbox` ni bekor qiladi)
- **Vosita cheklovlari** (`tools.allow` / `tools.deny`, shuningdek `agents.list[].tools`)

Bu turli xavfsizlik profillariga ega bir nechta agentlarni ishga tushirishga imkon beradi:

- To‘liq kirish huquqiga ega shaxsiy yordamchi
- Cheklangan vositalarga ega oila/ish agentlari
- Sandboxlarda joylashgan ommaga ochiq agentlar

`setupCommand` `sandbox.docker` ostida (global yoki har bir agent uchun) joylashadi va konteyner yaratilganda bir marta ishga tushadi.

Autentifikatsiya har bir agent uchun alohida: har bir agent o‘zining `agentDir` autentifikatsiya omboridan quyidagi manzilda o‘qiydi:

```
~/.openclaw/agents/<agentId>/agent/auth-profiles.json
```

Hisob ma’lumotlari agentlar o‘rtasida **ulashilmaydi**. Agentlar o‘rtasida hech qachon `agentDir` ni qayta ishlatmang.
Agar hisob ma’lumotlarini ulashmoqchi bo‘lsangiz, `auth-profiles.json` ni boshqa agentning `agentDir` ichiga nusxalang.

Sandboxing ish vaqtida qanday tutishini bilish uchun [Sandboxing](/gateway/sandboxing) ga qarang.
“Nega bu bloklangan?” ni nosozliklarni tuzatish uchun [Sandbox vs Tool Policy vs Elevated](/gateway/sandbox-vs-tool-policy-vs-elevated) va `openclaw sandbox explain` ga qarang.

---

## Konfiguratsiya misollari

### 1-misol: Shaxsiy + cheklangan oila agenti

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "default": true,
        "name": "Personal Assistant",
        "workspace": "~/.openclaw/workspace",
        "sandbox": { "mode": "off" }
      },
      {
        "id": "family",
        "name": "Family Bot",
        "workspace": "~/.openclaw/workspace-family",
        "sandbox": {
          "mode": "all",
          "scope": "agent"
        },
        "tools": {
          "allow": ["read"],
          "deny": ["exec", "write", "edit", "apply_patch", "process", "browser"]
        }
      }
    ]
  },
  "bindings": [
    {
      "agentId": "family",
      "match": {
        "provider": "whatsapp",
        "accountId": "*",
        "peer": {
          "kind": "group",
          "id": "120363424282127706@g.us"
        }
      }
    }
  ]
}
```

**Natija:**

- `main` agent: Xostda ishlaydi, barcha vositalarga to‘liq kirish
- `family` agent: Docker’da ishlaydi (har bir agent uchun bitta konteyner), faqat `read` vositasi

---

### 2-misol: Umumiy sandboxga ega ish agenti

```json
{
  "agents": {
    "list": [
      {
        "id": "personal",
        "workspace": "~/.openclaw/workspace-personal",
        "sandbox": { "mode": "off" }
      },
      {
        "id": "work",
        "workspace": "~/.openclaw/workspace-work",
        "sandbox": {
          "mode": "all",
          "scope": "shared",
          "workspaceRoot": "/tmp/work-sandboxes"
        },
        "tools": {
          "allow": ["read", "write", "apply_patch", "exec"],
          "deny": ["browser", "gateway", "discord"]
        }
      }
    ]
  }
}
```

---

### 2b-misol: Global kodlash profili + faqat xabar almashish agenti

```json
{
  "tools": { "profile": "coding" },
  "agents": {
    "list": [
      {
        "id": "support",
        "tools": { "profile": "messaging", "allow": ["slack"] }
      }
    ]
  }
}
```

**Natija:**

- standart agentlar kodlash vositalarini oladi
- `support` agent faqat xabar almashish uchun (+ Slack vositasi)

---

### 3-misol: Har bir agent uchun turli sandbox rejimlari

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main", // Global default
        "scope": "session"
      }
    },
    "list": [
      {
        "id": "main",
        "workspace": "~/.openclaw/workspace",
        "sandbox": {
          "mode": "off" // Override: main never sandboxed
        }
      },
      {
        "id": "public",
        "workspace": "~/.openclaw/workspace-public",
        "sandbox": {
          "mode": "all", // Override: public always sandboxed
          "scope": "agent"
        },
        "tools": {
          "allow": ["read"],
          "deny": ["exec", "write", "edit", "apply_patch"]
        }
      }
    ]
  }
}
```

---

## Konfiguratsiya ustuvorligi

Global (`agents.defaults.*`) va agentga xos (`agents.list[].*`) konfiguratsiyalar mavjud bo‘lganda:

### Sandbox konfiguratsiyasi

Agentga xos sozlamalar global sozlamalarni bekor qiladi:

```
agents.list[].sandbox.mode > agents.defaults.sandbox.mode
agents.list[].sandbox.scope > agents.defaults.sandbox.scope
agents.list[].sandbox.workspaceRoot > agents.defaults.sandbox.workspaceRoot
agents.list[].sandbox.workspaceAccess > agents.defaults.sandbox.workspaceAccess
agents.list[].sandbox.docker.* > agents.defaults.sandbox.docker.*
agents.list[].sandbox.browser.* > agents.defaults.sandbox.browser.*
agents.list[].sandbox.prune.* > agents.defaults.sandbox.prune.*
```

**Eslatmalar:**

- `agents.list[].sandbox.{docker,browser,prune}.*` ushbu agent uchun `agents.defaults.sandbox.{docker,browser,prune}.*` ni bekor qiladi (sandbox scope `"shared"` ga yechilganda e’tiborga olinmaydi).

### Vosita cheklovlari

Filtrlash tartibi quyidagicha:

1. **Vosita profili** (`tools.profile` yoki `agents.list[].tools.profile`)
2. **Provayder vosita profili** (`tools.byProvider[provider].profile` yoki `agents.list[].tools.byProvider[provider].profile`)
3. **Global vosita siyosati** (`tools.allow` / `tools.deny`)
4. **Provayder vosita siyosati** (`tools.byProvider[provider].allow/deny`)
5. **Agent-specific tool policy** (`agents.list[].tools.allow/deny`)
6. **Agent provider policy** (`agents.list[].tools.byProvider[provider].allow/deny`)
7. **Sandbox tool policy** (`tools.sandbox.tools` or `agents.list[].tools.sandbox.tools`)
8. **Subagent tool policy** (`tools.subagents.tools`, if applicable)

Each level can further restrict tools, but cannot grant back denied tools from earlier levels.
If `agents.list[].tools.sandbox.tools` is set, it replaces `tools.sandbox.tools` for that agent.
If `agents.list[].tools.profile` is set, it overrides `tools.profile` for that agent.
Provider tool keys accept either `provider` (e.g. `google-antigravity`) or `provider/model` (e.g. `openai/gpt-5.2`).

### Tool groups (shorthands)

Tool policies (global, agent, sandbox) support `group:*` entries that expand to multiple concrete tools:

- `group:runtime`: `exec`, `bash`, `process`
- `group:fs`: `read`, `write`, `edit`, `apply_patch`
- `group:sessions`: `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `session_status`
- `group:memory`: `memory_search`, `memory_get`
- `group:ui`: `browser`, `canvas`
- `group:automation`: `cron`, `gateway`
- `group:messaging`: `message`
- `group:nodes`: `nodes`
- `group:openclaw`: all built-in OpenClaw tools (excludes provider plugins)

### Elevated Mode

`tools.elevated` is the global baseline (sender-based allowlist). `agents.list[].tools.elevated` can further restrict elevated for specific agents (both must allow).

Mitigation patterns:

- Deny `exec` for untrusted agents (`agents.list[].tools.deny: ["exec"]`)
- Avoid allowlisting senders that route to restricted agents
- Disable elevated globally (`tools.elevated.enabled: false`) if you only want sandboxed execution
- Disable elevated per agent (`agents.list[].tools.elevated.enabled: false`) for sensitive profiles

---

## Migration from Single Agent

**Before (single agent):**

```json
{
  "agents": {
    "defaults": {
      "workspace": "~/.openclaw/workspace",
      "sandbox": {
        "mode": "non-main"
      }
    }
  },
  "tools": {
    "sandbox": {
      "tools": {
        "allow": ["read", "write", "apply_patch", "exec"],
        "deny": []
      }
    }
  }
}
```

**After (multi-agent with different profiles):**

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "default": true,
        "workspace": "~/.openclaw/workspace",
        "sandbox": { "mode": "off" }
      }
    ]
  }
}
```

Legacy `agent.*` configs are migrated by `openclaw doctor`; prefer `agents.defaults` + `agents.list` going forward.

---

## Tool Restriction Examples

### Read-only Agent

```json
{
  "tools": {
    "allow": ["read"],
    "deny": ["exec", "write", "edit", "apply_patch", "process"]
  }
}
```

### Safe Execution Agent (no file modifications)

```json
{
  "tools": {
    "allow": ["read", "exec", "process"],
    "deny": ["write", "edit", "apply_patch", "browser", "gateway"]
  }
}
```

### Communication-only Agent

```json
{
  "tools": {
    "allow": ["sessions_list", "sessions_send", "sessions_history", "session_status"],
    "deny": ["exec", "write", "edit", "apply_patch", "read", "browser"]
  }
}
```

---

## Common Pitfall: "non-main"

`agents.defaults.sandbox.mode: "non-main"` is based on `session.mainKey` (default `"main"`),
not the agent id. Group/channel sessions always get their own keys, so they
are treated as non-main and will be sandboxed. If you want an agent to never
sandbox, set `agents.list[].sandbox.mode: "off"`.

---

## Testing

After configuring multi-agent sandbox and tools:

1. **Check agent resolution:**

   ```exec
   openclaw agents list --bindings
   ```

2. **Verify sandbox containers:**

   ```exec
   docker ps --filter "name=openclaw-sbx-"
   ```

3. **Test tool restrictions:**
   - Send a message requiring restricted tools
   - Verify the agent cannot use denied tools

4. **Monitor logs:**

   ```exec
   tail -f "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/logs/gateway.log" | grep -E "routing|sandbox|tools"
   ```

---

## Troubleshooting

### Agent not sandboxed despite `mode: "all"`

- Check if there's a global `agents.defaults.sandbox.mode` that overrides it
- Agent-specific config takes precedence, so set `agents.list[].sandbox.mode: "all"`

### Tools still available despite deny list

- Check tool filtering order: global → agent → sandbox → subagent
- Each level can only further restrict, not grant back
- Verify with logs: `[tools] filtering tools for agent:${agentId}`

### Container not isolated per agent

- Set `scope: "agent"` in agent-specific sandbox config
- Default is `"session"` which creates one container per session

---

## See Also

- [Multi-Agent Routing](/concepts/multi-agent)
- [Sandbox Configuration](/gateway/configuration#agentsdefaults-sandbox)
- [Session Management](/concepts/session)
