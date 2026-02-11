---
summary: "Slash commands: text vs native, config, and supported commands"
read_when:
  - Using or configuring chat commands
  - Debugging command routing or permissions
title: "Slash Commands"
---

# Slash commands

Commands are handled by the Gateway. Most commands must be sent as a **standalone** message that starts with `/`.
The host-only bash chat command uses `! <cmd>` (with `/bash <cmd>` as an alias).

There are two related systems:

- **Commands**: standalone `/...` messages.
- **Directives**: `/think`, `/verbose`, `/reasoning`, `/elevated`, `/exec`, `/model`, `/queue`.
  - Directives are stripped from the message before the model sees it.
  - In normal chat messages (not directive-only), they are treated as “inline hints” and do **not** persist session settings.
  - In directive-only messages (the message contains only directives), they persist to the session and reply with an acknowledgement.
  - Directives are only applied for **authorized senders** (channel allowlists/pairing plus `commands.useAccessGroups`).
    Unauthorized senders see directives treated as plain text.

There are also a few **inline shortcuts** (allowlisted/authorized senders only): `/help`, `/commands`, `/status`, `/whoami` (`/id`).
They run immediately, are stripped before the model sees the message, and the remaining text continues through the normal flow.

## Config

```json5
{
  commands: {
    native: "auto",
    nativeSkills: "auto",
    text: true,
    bash: false,
    bashForegroundMs: 2000,
    config: false,
    debug: false,
    restart: false,
    useAccessGroups: true,
  },
}
```

- `commands.text` (default `true`) enables parsing `/...` in chat messages.
  - On surfaces without native commands (WhatsApp/WebChat/Signal/iMessage/Google Chat/MS Teams), text commands still work even if you set this to `false`.
- `commands.native` (default `"auto"`) registers native commands.
  - Auto: on for Discord/Telegram; off for Slack (until you add slash commands); ignored for providers without native support.
  - Set `channels.discord.commands.native`, `channels.telegram.commands.native`, or `channels.slack.commands.native` to override per provider (bool or `"auto"`).
  - `false` clears previously registered commands on Discord/Telegram at startup. Slack commands are managed in the Slack app and are not removed automatically.
- `commands.nativeSkills` (default `"auto"`) registers **skill** commands natively when supported.
  - Auto: on for Discord/Telegram; off for Slack (Slack requires creating a slash command per skill).
  - Set `channels.discord.commands.nativeSkills`, `channels.telegram.commands.nativeSkills`, or `channels.slack.commands.nativeSkills` to override per provider (bool or `"auto"`).
- `commands.bash` (default `false`) enables `! <cmd>` to run host shell commands (`/bash <cmd>` is an alias; requires `tools.elevated` allowlists).
- `commands.bashForegroundMs` (default `2000`) controls how long bash waits before switching to background mode (`0` backgrounds immediately).
- `commands.config` (default `false`) enables `/config` (reads/writes `openclaw.json`).
- `commands.debug` (default `false`) enables `/debug` (runtime-only overrides).
- `commands.useAccessGroups` (default `true`) enforces allowlists/policies for commands.

## Command list

Text + native (when enabled):

- `/help`
- `/commands`
- `/skill <name> [input]` (run a skill by name)
- `/status` (show current status; includes provider usage/quota for the current model provider when available)
- `/allowlist` (list/add/remove allowlist entries)
- `/approve <id> allow-once|allow-always|deny` (resolve exec approval prompts)
- `/context [list|detail|json]` (explain “context”; `detail` shows per-file + per-tool + per-skill + system prompt size)
- `/whoami` (show your sender id; alias: `/id`)
- `/subagents list|stop|log|info|send` (inspect, stop, log, or message sub-agent runs for the current session)
- `/config show|get|set|unset`（将配置持久化到磁盘，仅所有者；需要 `commands.config: true`）
- `/debug show|set|unset|reset`（运行时覆盖，仅所有者；需要 `commands.debug: true`）
- `/usage off|tokens|full|cost`（每条回复的用量页脚或本地成本汇总）
- `/tts off|always|inbound|tagged|status|provider|limit|summary|audio`（控制 TTS；参见 [/tts](/tts)）
  - Discord：原生命令是 `/voice`（Discord 保留 `/tts`）；文本 `/tts` 仍然可用。
- `/stop`
- `/restart`
- `/dock-telegram`（别名：`/dock_telegram`）（将回复切换到 Telegram）
- `/dock-discord` (alias: `/dock_discord`) (switch replies to Discord)
- `/dock-slack`（别名：`/dock_slack`）（将回复切换到 Slack）
- `/activation mention|always`（仅群组）
- `/send on|off|inherit`（仅所有者）
- `/reset` 或 `/new [model]`（可选模型提示；其余内容将原样传递）
- `/think <off|minimal|low|medium|high|xhigh>`（由模型/提供商动态决定选项；别名：`/thinking`、`/t`）
- `/verbose on|full|off`（别名：`/v`）
- `/reasoning on|off|stream`（别名：`/reason`；开启时会发送一条以 `Reasoning:` 为前缀的单独消息；`stream` = 仅 Telegram 草稿）
- `/elevated on|off|ask|full`（别名：`/elev`；`full` 跳过执行审批）
- `/exec host=<sandbox|gateway|node> security=<deny|allowlist|full> ask=<off|on-miss|always> node=<id>` (send `/exec` to show current)
- `/model <name>`（别名：`/models`；或来自 `agents.defaults.models.*.alias` 的 `/<alias>`）
- `/queue <mode>`（以及诸如 `debounce:2s cap:25 drop:summarize` 等选项；发送 `/queue` 查看当前设置）
- `/bash <command>`（仅主机；`! <command>` 的别名；需要 `commands.bash: true` + `tools.elevated` 允许列表） 仅文本：

`/compact [instructions]`（参见 [/concepts/compaction](/concepts/compaction)）

- `! <command>`（仅主机；一次一个；长时间任务使用 `!poll` + `!stop`）
- `!poll`（检查输出/状态；可选 `sessionId`；`/bash poll` 也可用） `!stop`（停止正在运行的 bash 任务；可选 `sessionId`；`/bash stop` 也可用）
- 注意：
- 命令在命令与参数之间可选使用 `:`（例如 `/think: high`、`/send: on`、`/help:`）。

`/new <model>` 接受模型别名、`provider/model` 或提供商名称（模糊匹配）；若无匹配，则将文本视为消息正文。

- 要查看完整的提供商用量明细，请使用 `openclaw status --usage`。
- `/allowlist add|remove` 需要 `commands.config=true`，并遵循频道 `configWrites`。
- `/usage` 控制每条回复的用量页脚；`/usage cost` 从 OpenClaw 会话日志中打印本地成本汇总。
- `/restart` 默认禁用；设置 `commands.restart: true` 以启用。
- `/verbose` 用于调试和额外可见性；正常使用中请保持 **关闭**。
- `/reasoning`（以及 `/verbose`）在群组环境中存在风险：可能会暴露你不打算公开的内部推理或工具输出。
- 尤其是在群聊中，建议保持它们关闭。
- **快速路径：** 来自允许列表发送者的仅命令消息会被立即处理（绕过队列 + 模型）。 **群组提及门控：** 来自允许列表发送者的仅命令消息会绕过提及要求。
- **内联快捷方式（仅允许列表发送者）：** 某些命令在普通消息中内嵌也可生效，并在模型看到剩余文本前被移除。
- 示例：`hey /status` 会触发状态回复，其余文本继续走正常流程。
- 当前支持：`/help`、`/commands`、`/status`、`/whoami`（`/id`）。
  - 未授权的仅命令消息会被静默忽略，内联的 `/...` 标记将被当作普通文本处理。
- **技能命令：** `user-invocable` 技能会以斜杠命令形式暴露。
- 名称会被规范化为 `a-z0-9_`（最多 32 个字符）；冲突会添加数字后缀（例如 `_2`）。
- `/skill <name> [input]` 按名称运行技能（当原生命令限制阻止按技能创建命令时很有用）。 默认情况下，技能命令会作为普通请求转发给模型。
  - 技能可选声明 `command-dispatch: tool`，将命令直接路由到工具（确定性、无模型）。
  - 示例：`/prose`（OpenProse 插件）——参见 [OpenProse](/prose)。
  - Skills may optionally declare `command-dispatch: tool` to route the command directly to a tool (deterministic, no model).
  - Example: `/prose` (OpenProse plugin) — see [OpenProse](/prose).
- 1. **原生命令参数：** Discord 对动态选项使用自动补全（当你省略必需参数时，也会显示按钮菜单）。 2. 当命令支持选项且你省略参数时，Telegram 和 Slack 会显示一个按钮菜单。

## 3. 使用展示位置（哪些内容显示在哪里）

- 4. **提供商使用量/配额**（示例：“Claude 剩余 80%”）在启用使用量跟踪时，会显示在当前模型提供商的 `/status` 中。
- 5. **每次回复的 token/成本** 由 `/usage off|tokens|full` 控制（附加在正常回复后）。
- 6. `/model status` 关注的是 **模型/认证/端点**，而不是使用量。

## 7. 模型选择（`/model`）

8. `/model` 作为一个指令（directive）实现。

9. 示例：

```
10. /model
/model list
/model 3
/model openai/gpt-5.2
/model opus@anthropic:default
/model status
```

11. 说明：

- 12. `/model` 和 `/model list` 显示一个紧凑的、带编号的选择器（模型家族 + 可用提供商）。
- 13. `/model <#>` 从该选择器中进行选择（并在可能的情况下优先使用当前提供商）。
- 14. `/model status` 显示详细视图，包括已配置的提供商端点（`baseUrl`）以及 API 模式（`api`）（如果可用）。

## 15. 调试覆盖项

16. `/debug` 允许你设置 **仅运行时** 的配置覆盖（内存中，不写入磁盘）。 17. 仅限所有者。 18. 默认禁用；使用 `commands.debug: true` 启用。

19. 示例：

```
20. /debug show
/debug set messages.responsePrefix="[openclaw]"
/debug set channels.whatsapp.allowFrom=["+1555","+4477"]
/debug unset messages.responsePrefix
/debug reset
```

21. 说明：

- 22. 覆盖项会立即应用于新的配置读取，但 **不会** 写入 `openclaw.json`。
- 23. 使用 `/debug reset` 清除所有覆盖并返回到磁盘上的配置。

## Config updates

25. `/config` 会写入磁盘上的配置（`openclaw.json`）。 26. 仅限所有者。 27. 默认禁用；使用 `commands.config: true` 启用。

28. 示例：

```
29. /config show
/config show messages.responsePrefix
/config get messages.responsePrefix
/config set messages.responsePrefix="[openclaw]"
/config unset messages.responsePrefix
```

30. 说明：

- 31. 配置在写入前会进行校验；无效的更改将被拒绝。
- 32. `/config` 更新在重启后仍然生效。

## 33. 界面说明

- 34. **文本命令** 在普通聊天会话中运行（私信共享 `main`，群组各自拥有独立会话）。
- 35. **原生命令** 使用隔离的会话：
  - 36. Discord：`agent:<agentId>:discord:slash:<userId>`
  - 37. Slack：`agent:<agentId>:slack:slash:<userId>`（前缀可通过 `channels.slack.slashCommand.sessionPrefix` 配置）
  - 38. Telegram：`telegram:slash:<userId>`（通过 `CommandTargetSessionKey` 定位到聊天会话）
- 39. **`/stop`** 作用于活动的聊天会话，以便中止当前运行。
- 40. **Slack：** 仍然支持用于单个 `/openclaw` 风格命令的 `channels.slack.slashCommand`。 41. 如果你启用 `commands.native`，则必须为每个内置命令创建一个 Slack 斜杠命令（名称与 `/help` 中相同）。 42. Slack 的命令参数菜单以临时（ephemeral）的 Block Kit 按钮形式提供。
