---
summary: "9. ClawHub 指南：公共技能注册表 + CLI 工作流"
read_when:
  - Introducing ClawHub to new users
  - 11. 安装、搜索或发布技能
  - Explaining ClawHub CLI flags and sync behavior
title: "13. ClawHub"
---

# 14. ClawHub

15. ClawHub 是 **OpenClaw 的公共技能注册表**。 16. 这是一个免费服务：所有技能都是公开、开放，并对所有人可见，便于共享和复用。 17. 一个技能只是一个包含 `SKILL.md` 文件（以及支持性的文本文件）的文件夹。 18. 你可以在 Web 应用中浏览技能，或使用 CLI 来搜索、安装、更新和发布技能。

19. 网站：[clawhub.ai](https://clawhub.ai)

## 20. ClawHub 是什么

- 21. 一个用于 OpenClaw 技能的公共注册表。
- 22. 一个带版本的技能包及其元数据存储库。
- 23. 一个用于搜索、标签和使用信号的发现平台。

## 24. 工作原理

1. 25. 用户发布一个技能包（文件 + 元数据）。
2. 26. ClawHub 存储该技能包，解析元数据，并分配一个版本。
3. 27. 注册表会对技能建立索引，用于搜索和发现。
4. 28. 用户在 OpenClaw 中浏览、下载并安装技能。

## 29) 你可以做什么

- 30. 发布新技能以及现有技能的新版本。
- 31. 按名称、标签或搜索来发现技能。
- Download skill bundles and inspect their files.
- 33. 举报具有滥用性或不安全的技能。
- 34. 如果你是版主，可以隐藏、取消隐藏、删除或封禁。

## 35. 适合谁（对初学者友好）

36. 如果你想为你的 OpenClaw 代理添加新能力，ClawHub 是查找和安装技能的最简单方式。 37. 你不需要了解后端是如何工作的。 38. 你可以：

- 39. 使用自然语言搜索技能。
- 40. 将技能安装到你的工作区。
- 41. 以后使用一条命令更新技能。
- 42. 通过发布来备份你自己的技能。

## 43. 快速开始（非技术向）

1. 44. 安装 CLI（见下一节）。
2. 45. 搜索你需要的内容：
   - 46. `clawhub search "calendar"`
3. 47. 安装一个技能：
   - 48. `clawhub install <skill-slug>`
4. 49. 启动一个新的 OpenClaw 会话，以便加载新技能。

## 50) 安装 CLI

选择一种：

```bash
npm i -g clawhub
```

```bash
pnpm add -g clawhub
```

## 它如何融入 OpenClaw

默认情况下，CLI 会将技能安装到当前工作目录下的 `./skills`。 如果配置了 OpenClaw 工作区，`clawhub` 会回退到该工作区，除非你通过 `--workdir`（或 `CLAWHUB_WORKDIR`）进行覆盖。 OpenClaw 会从 `<workspace>/skills` 加载工作区技能，并会在**下一次**会话中生效。 如果你已经使用 `~/.openclaw/skills` 或内置技能，工作区技能具有更高优先级。

有关技能如何被加载、共享和受控的更多细节，请参见
[Skills](/tools/skills)。

## 技能系统概览

技能是一个带版本的文件包，用于教会 OpenClaw 如何执行
特定任务。 每次发布都会创建一个新版本，注册表会保留
版本历史，以便用户审计更改。

一个典型的技能包括：

- 一个 `SKILL.md` 文件，包含主要说明和使用方法。
- 技能使用的可选配置、脚本或支持文件。
- 诸如标签、摘要和安装要求等元数据。

ClawHub 使用元数据来支持发现，并安全地暴露技能能力。
注册表还会跟踪使用信号（例如星标和下载量），以改进
排名和可见性。

## 服务提供的内容（功能）

- 技能及其 `SKILL.md` 内容的**公开浏览**。
- 由嵌入（向量搜索）驱动的**搜索**，而不仅仅是关键词。
- 基于 semver 的**版本管理**，包含变更日志和标签（包括 `latest`）。
- 按版本提供的 **下载**（zip 格式）。
- 用于社区反馈的 **星标和评论**。
- 用于审批和审计的 **审核** 钩子。
- 便于自动化和脚本的 **CLI 友好 API**。

## 安全与审核

ClawHub 默认是开放的。 任何人都可以上传技能，但用于发布的 GitHub 账号必须
至少创建一周。 这有助于减缓滥用行为，而不会阻止
合法贡献者。

举报与审核：

- 任何已登录用户都可以举报技能。
- 举报原因是必填的，并会被记录。
- 每个用户同时最多可以有 20 个有效举报。
- 拥有超过 3 个不同用户举报的技能将默认被自动隐藏。
- 版主可以查看被隐藏的技能、将其取消隐藏、删除它们，或封禁用户。
- 滥用举报功能可能会导致账号被封禁。

有兴趣成为版主吗？ 请在 OpenClaw Discord 中咨询，并联系一位
版主或维护者。

## CLI 命令和参数

全局选项（适用于所有命令）：

- `--workdir <dir>`：工作目录（默认：当前目录；回退到 OpenClaw 工作区）。
- `--dir <dir>`：技能目录，相对于 workdir（默认：`skills`）。
- `--site <url>`：站点基础 URL（浏览器登录）。
- `--registry <url>`：注册表 API 基础 URL。
- `--no-input`：禁用提示（非交互式）。
- `-V, --cli-version`：输出 CLI 版本。

认证：

- `clawhub login`（浏览器流程）或 `clawhub login --token <token>`
- `clawhub logout`
- `clawhub whoami`

Options:

- `--token <token>`: Paste an API token.
- `--label <label>`: Label stored for browser login tokens (default: `CLI token`).
- `--no-browser`: Do not open a browser (requires `--token`).

Search:

- `clawhub search "query"`
- `--limit <n>`: Max results.

Install:

- `clawhub install <slug>`
- `--version <version>`: Install a specific version.
- `--force`: Overwrite if the folder already exists.

Update:

- `clawhub update <slug>`
- `clawhub update --all`
- `--version <version>`: Update to a specific version (single slug only).
- `--force`: Overwrite when local files do not match any published version.

List:

- `clawhub list` (reads `.clawhub/lock.json`)

Publish:

- `clawhub publish <path>`
- `--slug <slug>`: Skill slug.
- `--name <name>`: Display name.
- `--version <version>`: Semver version.
- `--changelog <text>`: Changelog text (can be empty).
- `--tags <tags>`: Comma-separated tags (default: `latest`).

Delete/undelete (owner/admin only):

- `clawhub delete <slug> --yes`
- `clawhub undelete <slug> --yes`

Sync (scan local skills + publish new/updated):

- `clawhub sync`
- `--root <dir...>`: Extra scan roots.
- `--all`: Upload everything without prompts.
- `--dry-run`: Show what would be uploaded.
- `--bump <type>`: `patch|minor|major` for updates (default: `patch`).
- `--changelog <text>`: Changelog for non-interactive updates.
- `--tags <tags>`: Comma-separated tags (default: `latest`).
- `--concurrency <n>`: Registry checks (default: 4).

## Common workflows for agents

### Search for skills

```bash
clawhub search "postgres backups"
```

### Download new skills

```bash
clawhub install my-skill-pack
```

### Update installed skills

```bash
clawhub update --all
```

### Back up your skills (publish or sync)

For a single skill folder:

```bash
clawhub publish ./my-skill --slug my-skill --name "My Skill" --version 1.0.0 --tags latest
```

To scan and back up many skills at once:

```bash
clawhub sync --all
```

## Advanced details (technical)

### Versioning and tags

- Each publish creates a new **semver** `SkillVersion`.
- Tags (like `latest`) point to a version; moving tags lets you roll back.
- Changelogs are attached per version and can be empty when syncing or publishing updates.

### Local changes vs registry versions

Updates compare the local skill contents to registry versions using a content hash. If local files do not match any published version, the CLI asks before overwriting (or requires `--force` in non-interactive runs).

### Sync scanning and fallback roots

`clawhub sync` scans your current workdir first. If no skills are found, it falls back to known legacy locations (for example `~/openclaw/skills` and `~/.openclaw/skills`). This is designed to find older skill installs without extra flags.

### Storage and lockfile

- Installed skills are recorded in `.clawhub/lock.json` under your workdir.
- Auth tokens are stored in the ClawHub CLI config file (override via `CLAWHUB_CONFIG_PATH`).

### Telemetry (install counts)

When you run `clawhub sync` while logged in, the CLI sends a minimal snapshot to compute install counts. You can disable this entirely:

```bash
export CLAWHUB_DISABLE_TELEMETRY=1
```

## Environment variables

- `CLAWHUB_SITE`: Override the site URL.
- `CLAWHUB_REGISTRY`: Override the registry API URL.
- `CLAWHUB_CONFIG_PATH`: Override where the CLI stores the token/config.
- `CLAWHUB_WORKDIR`: Override the default workdir.
- `CLAWHUB_DISABLE_TELEMETRY=1`: Disable telemetry on `sync`.
