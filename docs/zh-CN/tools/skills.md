---
summary: "44. 技能：托管 vs 工作区、门控规则以及配置/环境变量的连接方式"
read_when:
  - 45. 添加或修改技能
  - 46. 更改技能门控或加载规则
title: "47. 技能"
---

# 48. 技能（OpenClaw）

49. OpenClaw 使用 **[AgentSkills](https://agentskills.io)-compatible** 的技能文件夹来教会代理如何使用工具。 50. 每个技能都是一个目录，包含带有 YAML 前置元数据和说明的 `SKILL.md`。 1. OpenClaw 会加载 **内置技能** 以及可选的本地覆盖，并在加载时根据环境、配置和二进制文件的存在情况进行过滤。

## 2. 位置与优先级

3. 技能从 **三个** 位置加载：

1. **Bundled skills**: shipped with the install (npm package or OpenClaw.app)
2. 5. **托管/本地技能**：`~/.openclaw/skills`
3. 6. **工作区技能**：`<workspace>/skills`

7) 如果技能名称冲突，优先级为：

8. `<workspace>/skills`（最高） → `~/.openclaw/skills` → 内置技能（最低）

9. 另外，你可以通过 `~/.openclaw/openclaw.json` 中的
   `skills.load.extraDirs` 配置额外的技能文件夹（最低优先级）。

## 10. 按代理区分 vs 共享技能

11. 在 **多代理** 设置中，每个代理都有自己的工作区。 12. 这意味着：

- 13. **按代理技能** 仅存在于该代理的 `<workspace>/skills` 中。
- 14. **共享技能** 位于 `~/.openclaw/skills`（托管/本地），并对同一台机器上的 **所有代理** 可见。
- 15. 如果你希望多个代理使用同一套技能包，也可以通过 `skills.load.extraDirs` 添加 **共享文件夹**（最低优先级）。

16. 如果同一技能名称存在于多个位置，则适用通常的优先级规则：工作区优先，其次是托管/本地，最后是内置。

## 17. 插件 + 技能

18. 插件可以通过在 `openclaw.plugin.json` 中列出 `skills` 目录（相对于插件根目录的路径）来随插件提供自己的技能。 19. 当插件启用时，插件技能会被加载，并参与正常的技能优先级规则。
19. 你可以通过插件配置项中的 `metadata.openclaw.requires.config` 来对其进行门控。 21. 有关发现/配置请参见 [Plugins](/tools/plugin)，有关这些技能所教授的工具界面请参见 [Tools](/tools)。

## 22. ClawHub（安装 + 同步）

ClawHub is the public skills registry for OpenClaw. 24. 浏览地址：
[https://clawhub.com](https://clawhub.com)。 25. 使用它来发现、安装、更新和备份技能。
26. 完整指南：[ClawHub](/tools/clawhub)。

27. 常见流程：

- 28. 将技能安装到你的工作区：
  - 29. `clawhub install <skill-slug>`
- Update all installed skills:
  - `clawhub update --all`
- 32. 同步（扫描 + 发布更新）：
  - 33. `clawhub sync --all`

34. 默认情况下，`clawhub` 会安装到当前工作目录下的 `./skills`
    （或回退到已配置的 OpenClaw 工作区）。 35. OpenClaw 会在下一次会话中
    将其识别为 `<workspace>/skills`。

## 36. 安全注意事项

- 37. 将第三方技能视为 **不受信任的代码**。 38. 在启用之前先阅读它们。
- 39. 对不受信任的输入和高风险工具，优先使用沙盒运行。 40. 参见 [Sandboxing](/gateway/sandboxing)。
- 41. `skills.entries.*.env` 和 `skills.entries.*.apiKey` 会将密钥注入到该代理回合的 **宿主** 进程中
      （而不是沙盒）。 Keep secrets out of prompts and logs.
- 43. 有关更广泛的威胁模型和检查清单，请参见 [Security](/gateway/security)。

## 44. 格式（AgentSkills + 兼容 Pi）

45. `SKILL.md` 必须至少包含：

```markdown
46. ---
name: nano-banana-pro
description: 通过 Gemini 3 Pro Image 生成或编辑图像
---
```

47. 备注：

- 48. 我们遵循 AgentSkills 规范来定义布局和意图。
- 49. 嵌入式代理使用的解析器仅支持 **单行** frontmatter 键。
- 50. `metadata` 应为 **单行 JSON 对象**。
- Use `{baseDir}` in instructions to reference the skill folder path.
- Optional frontmatter keys:
  - `homepage` — URL surfaced as “Website” in the macOS Skills UI (also supported via `metadata.openclaw.homepage`).
  - `user-invocable` — `true|false` (default: `true`). When `true`, the skill is exposed as a user slash command.
  - `disable-model-invocation` — `true|false` (default: `false`). When `true`, the skill is excluded from the model prompt (still available via user invocation).
  - `command-dispatch` — `tool` (optional). When set to `tool`, the slash command bypasses the model and dispatches directly to a tool.
  - `command-tool` — tool name to invoke when `command-dispatch: tool` is set.
  - `command-arg-mode` — `raw` (default). For tool dispatch, forwards the raw args string to the tool (no core parsing).

    The tool is invoked with params:
    `{ command: "<raw args>", commandName: "<slash command>", skillName: "<skill name>" }`.

## Gating (load-time filters)

OpenClaw **filters skills at load time** using `metadata` (single-line JSON):

```markdown
---
name: nano-banana-pro
description: Generate or edit images via Gemini 3 Pro Image
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["uv"], "env": ["GEMINI_API_KEY"], "config": ["browser.enabled"] },
        "primaryEnv": "GEMINI_API_KEY",
      },
  }
---
```

Fields under `metadata.openclaw`:

- `always: true` — always include the skill (skip other gates).
- `emoji` — optional emoji used by the macOS Skills UI.
- `homepage` — optional URL shown as “Website” in the macOS Skills UI.
- `os` — optional list of platforms (`darwin`, `linux`, `win32`). If set, the skill is only eligible on those OSes.
- `requires.bins` — list; each must exist on `PATH`.
- `requires.anyBins` — list; at least one must exist on `PATH`.
- `requires.env` — list; env var must exist **or** be provided in config.
- `requires.config` — list of `openclaw.json` paths that must be truthy.
- `primaryEnv` — env var name associated with `skills.entries.<name>.apiKey`.
- `install` — optional array of installer specs used by the macOS Skills UI (brew/node/go/uv/download).

Note on sandboxing:

- `requires.bins` is checked on the **host** at skill load time.
- If an agent is sandboxed, the binary must also exist **inside the container**.
  Install it via `agents.defaults.sandbox.docker.setupCommand` (or a custom image).
  `setupCommand` runs once after the container is created.
  Package installs also require network egress, a writable root FS, and a root user in the sandbox.
  Example: the `summarize` skill (`skills/summarize/SKILL.md`) needs the `summarize` CLI
  in the sandbox container to run there.

Installer example:

```markdown
---
name: gemini
description: Use Gemini CLI for coding assistance and Google search lookups.
metadata:
  {
    "openclaw":
      {
        "emoji": "♊️",
        "requires": { "bins": ["gemini"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "gemini-cli",
              "bins": ["gemini"],
              "label": "Install Gemini CLI (brew)",
            },
          ],
      },
  }
---
```

Notes:

- If multiple installers are listed, the gateway picks a **single** preferred option (brew when available, otherwise node).
- If all installers are `download`, OpenClaw lists each entry so you can see the available artifacts.
- Installer specs can include `os: ["darwin"|"linux"|"win32"]` to filter options by platform.
- Node installs honor `skills.install.nodeManager` in `openclaw.json` (default: npm; options: npm/pnpm/yarn/bun).
  This only affects **skill installs**; the Gateway runtime should still be Node
  (Bun is not recommended for WhatsApp/Telegram).
- Go installs: if `go` is missing and `brew` is available, the gateway installs Go via Homebrew first and sets `GOBIN` to Homebrew’s `bin` when possible.
- Download installs: `url` (required), `archive` (`tar.gz` | `tar.bz2` | `zip`), `extract` (default: auto when archive detected), `stripComponents`, `targetDir` (default: `~/.openclaw/tools/<skillKey>`).

If no `metadata.openclaw` is present, the skill is always eligible (unless
disabled in config or blocked by `skills.allowBundled` for bundled skills).

## Config overrides (`~/.openclaw/openclaw.json`)

Bundled/managed skills can be toggled and supplied with env values:

```json5
{
  skills: {
    entries: {
      "nano-banana-pro": {
        enabled: true,
        apiKey: "GEMINI_KEY_HERE",
        env: {
          GEMINI_API_KEY: "GEMINI_KEY_HERE",
        },
        config: {
          endpoint: "https://example.invalid",
          model: "nano-pro",
        },
      },
      peekaboo: { enabled: true },
      sag: { enabled: false },
    },
  },
}
```

1. 注意：如果技能名称包含连字符，请将键用引号括起来（JSON5 允许带引号的键）。

2. 默认情况下，配置键与 **技能名称** 匹配。 3. 如果某个技能定义了
   `metadata.openclaw.skillKey`，请在 `skills.entries` 下使用该键。

4. 规则：

- 5. `enabled: false` 会禁用该技能，即使它已被捆绑/安装。
- 6. `env`：**仅当**该变量尚未在进程中设置时才会注入。
- 7. `apiKey`：为声明了 `metadata.openclaw.primaryEnv` 的技能提供的便捷方式。
- 8. `config`：可选的自定义字段容器（per-skill）；自定义键必须放在这里。
- 9. `allowBundled`：仅针对**捆绑**技能的可选允许列表。 10. 如果设置了该项，则只有列表中的
     捆绑技能才有资格（不影响 managed/workspace 技能）。

## 11. 环境变量注入（每次 agent 运行）

12. 当一次 agent 运行开始时，OpenClaw：

1. 13. 读取技能元数据。
2. 14. 应用任何 `skills.entries.<key>`15. `.env` 或 `skills.entries.<key>`16. `.apiKey` 到
       `process.env`。
3. 17. 使用**符合条件**的技能构建 system prompt。
4. 18. 在运行结束后恢复原始环境。

19) 这是**作用域限定为 agent 运行**的，而不是全局 shell 环境。

## 20. 会话快照（性能）

21. OpenClaw 在**会话开始时**对符合条件的技能进行快照，并在同一会话的后续轮次中复用该列表。 22. 对技能或配置的更改会在下一个新会话中生效。

23. 当启用 skills watcher 或出现新的符合条件的远程节点时，技能也可以在会话中途刷新（见下文）。 24. 可将其视为一种**热重载**：刷新后的列表会在下一次 agent 轮次中生效。

## 25. 远程 macOS 节点（Linux 网关）

26. 如果 Gateway 运行在 Linux 上，但连接了一个**macOS 节点**且**允许 `system.run`**（Exec approvals security 未设置为 `deny`），当该节点上存在所需二进制文件时，OpenClaw 可以将仅限 macOS 的技能视为符合条件。 27. agent 应通过 `nodes` 工具（通常是 `nodes.run`）来执行这些技能。

28. 这依赖于节点上报其命令支持情况，以及通过 `system.run` 进行的二进制探测。 29. 如果 macOS 节点随后离线，这些技能仍然可见；在节点重新连接之前，调用可能会失败。

## 30. Skills watcher（自动刷新）

31. 默认情况下，OpenClaw 会监视技能文件夹，并在 `SKILL.md` 文件发生更改时更新技能快照。 32. 在 `skills.load` 下进行配置：

```json5
33. {
  skills: {
    load: {
      watch: true,
      watchDebounceMs: 250,
    },
  },
}
```

## 34. Token 影响（技能列表）

35. 当技能符合条件时，OpenClaw 会通过 `pi-coding-agent` 中的 `formatSkillsForPrompt`，将一个紧凑的 XML 可用技能列表注入到 system prompt 中。 36. 成本是确定的：

- 37. **基础开销（仅当 ≥1 个技能时）：** 195 个字符。
- 38. **每个技能：** 97 个字符 + XML 转义后的 `<name>`、`<description>` 和 `<location>` 值的长度。

39. 公式（字符数）：

```
40. total = 195 + Σ (97 + len(name_escaped) + len(description_escaped) + len(location_escaped))
```

41. 说明：

- 42. XML 转义会将 `& < > " '` 扩展为实体（`&amp;`、`&lt;` 等），从而增加长度。
- 43. 不同模型的分词器会导致 token 数不同。 44. 一个粗略的 OpenAI 风格估算是 ~4 字符/token，因此**97 个字符 ≈ 每个技能 24 个 token**，再加上你的实际字段长度。

## 45. Managed skills 生命周期

46. OpenClaw 随安装（npm 包或 OpenClaw.app）提供一组基线技能，作为**捆绑技能**。 47. `~/.openclaw/skills` 用于本地
    覆盖（例如，在不更改捆绑副本的情况下固定/修补某个技能）。 48. Workspace 技能由用户拥有，并在名称冲突时覆盖前两者。

## 49. 配置参考

50. 完整的配置 schema 请参见 [Skills config](/tools/skills-config)。

## Looking for more skills?

Browse [https://clawhub.com](https://clawhub.com).

---
