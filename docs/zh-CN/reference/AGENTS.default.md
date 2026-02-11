---
summary: "用于个人助理设置的默认 OpenClaw 代理指令和技能清单"
read_when:
  - 开始一个新的 OpenClaw 代理会话
  - 启用或审计默认技能
---

# AGENTS.md — OpenClaw 个人助理（默认）

## 首次运行（推荐）

OpenClaw 为代理使用一个专用的工作区目录。 默认值：`~/.openclaw/workspace`（可通过 `agents.defaults.workspace` 配置）。

1. 创建工作区（如果尚不存在）：

```bash
mkdir -p ~/.openclaw/workspace
```

2. 将默认工作区模板复制到工作区中：

```bash
cp docs/reference/templates/AGENTS.md ~/.openclaw/workspace/AGENTS.md
cp docs/reference/templates/SOUL.md ~/.openclaw/workspace/SOUL.md
cp docs/reference/templates/TOOLS.md ~/.openclaw/workspace/TOOLS.md
```

3. 可选：如果你想要个人助理的技能清单，用此文件替换 AGENTS.md：

```bash
cp docs/reference/AGENTS.default.md ~/.openclaw/workspace/AGENTS.md
```

4. 可选：通过设置 `agents.defaults.workspace` 选择不同的工作区（支持 `~`）：

```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
}
```

## 安全默认值

- 不要将目录或机密信息倾倒到聊天中。
- 除非明确要求，否则不要运行具有破坏性的命令。
- 不要向外部消息平台发送部分/流式回复（仅发送最终回复）。

## 会话开始（必需）

- 读取 `SOUL.md`、`USER.md`、`memory.md`，以及 `memory/` 中的今天+昨天。
- 在回应之前完成这些步骤。

## 灵魂（必需）

- `SOUL.md` 定义身份、语气和边界。 保持其为最新状态。
- 如果你更改了 `SOUL.md`，请告知用户。
- 你在每个会话中都是一个全新实例；连续性存在于这些文件中。

## 共享空间（推荐）

- 你不是用户的代言人；在群聊或公共频道中要谨慎。
- 不要分享私人数据、联系方式或内部笔记。

## 记忆系统（推荐）

- 每日日志：`memory/YYYY-MM-DD.md`（如有需要请创建 `memory/`）。
- 长期记忆：用于持久事实、偏好和决策的 `memory.md`。
- 会话开始时，读取今天 + 昨天 + `memory.md`（如果存在）。
- 记录：决策、偏好、约束、未完成事项。
- 除非明确要求，否则避免记录机密信息。

## Tools & skills

- Tools live in skills; follow each skill’s `SKILL.md` when you need it.
- 将特定于环境的说明保存在 `TOOLS.md`（技能说明）中。

## 备份提示（推荐）

如果你将此工作区视为 Clawd 的“记忆”，请将其设为一个 git 仓库（最好是私有的），以便备份 `AGENTS.md` 和你的记忆文件。

```bash
cd ~/.openclaw/workspace
git init
git add AGENTS.md
git commit -m "Add Clawd workspace"
# Optional: add a private remote + push
```

## OpenClaw 的功能

- 运行 WhatsApp 网关 + Pi 编码代理，使助理能够读取/写入聊天、获取上下文，并通过主机 Mac 运行技能。
- macOS 应用管理权限（屏幕录制、通知、麦克风），并通过其捆绑的二进制文件暴露 `openclaw` CLI。
- 默认情况下，直接聊天会折叠到代理的 `main` 会话中；群组保持隔离为 `agent:<agentId>:<channel>:group:<id>`（房间/频道：`agent:<agentId>:<channel>:channel:<id>`）；心跳用于保持后台任务存活。

## 核心技能（在“设置 → 技能”中启用）

- **mcporter** — 用于管理外部技能后端的工具服务器运行时/CLI。
- **Peekaboo** — 快速的 macOS 截图工具，支持可选的 AI 视觉分析。
- 1. **camsnap** — 从 RTSP/ONVIF 安防摄像头捕获帧、片段或运动警报。
- 2. **oracle** — 面向 OpenAI 的智能体 CLI，支持会话回放和浏览器控制。
- 3. **eightctl** — 在终端中控制你的睡眠。
- 4. **imsg** — 发送、读取、流式处理 iMessage 和 SMS。
- 5. **wacli** — WhatsApp CLI：同步、搜索、发送。
- 6. **discord** — Discord 操作：表情反应、贴纸、投票。 Use `user:<id>` or `channel:<id>` targets (bare numeric ids are ambiguous).
- 8. **gog** — Google 套件 CLI：Gmail、日历、云端硬盘、联系人。
- 9. **spotify-player** — 终端版 Spotify 客户端，用于搜索/排队/控制播放。
- 10. **sag** — 具有 mac 风格 say 体验的 ElevenLabs 语音；默认流式输出到扬声器。
- 11. **Sonos CLI** — 通过脚本控制 Sonos 音箱（发现/状态/播放/音量/分组）。
- 12. **blucli** — 通过脚本播放、分组并自动化 BluOS 播放器。
- **OpenHue CLI** — Philips Hue lighting control for scenes and automations.
- 14. **OpenAI Whisper** — 本地语音转文本，用于快速听写和语音信箱转录。
- **Gemini CLI** — Google Gemini models from the terminal for fast Q&A.
- 16. **agent-tools** — 用于自动化和辅助脚本的实用工具包。

## 17. 使用说明

- 18. 脚本编写优先使用 `openclaw` CLI；mac 应用负责处理权限。
- 19. 从 Skills 选项卡运行安装；如果已存在二进制文件，它会隐藏按钮。
- 20. 保持心跳启用，以便助手能够安排提醒、监控收件箱并触发摄像头捕获。
- 21. Canvas UI 以全屏运行，并带有原生叠加层。 22. 避免将关键控件放在左上/右上/底部边缘；在布局中添加明确的边距（gutters），不要依赖安全区域内边距。
- 23. 进行浏览器驱动的验证时，使用 `openclaw browser`（标签/状态/截图），并使用 OpenClaw 管理的 Chrome 配置文件。
- 24. 进行 DOM 检查时，使用 `openclaw browser eval|query|dom|snapshot`（需要机器输出时使用 `--json`/`--out`）。
- For interactions, use `openclaw browser click|type|hover|drag|select|upload|press|wait|navigate|back|evaluate|run` (click/type require snapshot refs; use `evaluate` for CSS selectors).
