---
summary: "19. CLI 入门向导：用于网关、工作区、频道和技能的引导式设置"
read_when:
  - 20. 运行或配置入门向导
  - 21. 设置一台新机器
title: "22. 入门向导（CLI）"
sidebarTitle: "23. 入门：CLI"
---

# 24. 入门向导（CLI）

25. 入门向导是**推荐**在 macOS、Linux 或 Windows（通过 WSL2；强烈推荐）上设置 OpenClaw 的方式。
26. 它在一个引导流程中配置本地网关或远程网关连接，以及频道、技能和工作区默认值。

```bash
27. openclaw onboard
```

<Info>
28. 最快的首次聊天：打开 Control UI（无需频道设置）。 29. 运行
`openclaw dashboard` 并在浏览器中聊天。 30. 文档：[Dashboard](/web/dashboard)。
</Info>

31. 之后重新配置：

```bash
32. openclaw configure
openclaw agents add <name>
```

<Note>
33. `--json` 并不意味着非交互模式。 34. 对于脚本，请使用 `--non-interactive`。
</Note>

<Tip>
35. 建议：设置 Brave Search API key，以便代理可以使用 `web_search`（`web_fetch` 无需密钥即可使用）。 36. 最简单的方式：`openclaw configure --section web`
它会存储 `tools.web.search.apiKey`。 37. 文档：[Web tools](/tools/web)。
</Tip>

## 38. QuickStart 与 Advanced

39. 向导以 **QuickStart**（默认值）或 **Advanced**（完全控制）开始。

<Tabs>
  <Tab title="QuickStart (defaults)">40. 
    - 本地网关（回环）
    - 工作区默认值（或现有工作区）
    - 网关端口 **18789**
    - 网关认证 **Token**（即使在回环模式下也会自动生成）
    - Tailscale 暴露 **关闭**
    - Telegram + WhatsApp 私信默认为 **允许列表**（将提示你输入手机号）
  </Tab>
  <Tab title="Advanced (full control)">41. 
    - 暴露每一步（模式、工作区、网关、频道、守护进程、技能）。
  </Tab>
</Tabs>

## 42. 向导会配置的内容

43. **本地模式（默认）** 将引导你完成以下步骤：

1. 44. **模型/认证** — Anthropic API key（推荐）、OAuth、OpenAI 或其他提供商。 45. 选择一个默认模型。
2. 46. **工作区** — 代理文件的位置（默认 `~/.openclaw/workspace`）。 47. 初始化引导文件。
3. 48. **网关** — 端口、绑定地址、认证模式、Tailscale 暴露。
4. 49. **频道** — WhatsApp、Telegram、Discord、Google Chat、Mattermost、Signal、BlueBubbles 或 iMessage。
5. 50. **守护进程** — 安装 LaunchAgent（macOS）或 systemd 用户单元（Linux/WSL2）。
6. 1. **健康检查** — 启动 Gateway 并验证其是否正在运行。
7. **技能** — 安装推荐的技能和可选依赖。

<Note>
3. 重新运行向导**不会**清除任何内容，除非你明确选择 **Reset**（或传递 `--reset`）。
4. 如果配置无效或包含旧版键，向导会要求你先运行 `openclaw doctor`。
</Note>

5. **远程模式** 仅配置本地客户端以连接到其他位置的 Gateway。
6. 它**不会**在远程主机上安装或更改任何内容。

## 7. 添加另一个代理

8. 使用 `openclaw agents add <name>` 创建一个具有自己工作区、会话和认证配置文件的独立代理。 9. 在未指定 `--workspace` 的情况下运行会启动向导。

10. 它会设置的内容：

- `agents.list[].name`
- 12. `agents.list[].workspace`
- 13. `agents.list[].agentDir`

14. 说明：

- 默认工作区遵循 `~/.openclaw/workspace-<agentId>`。
- 16. 添加 `bindings` 以路由入站消息（向导可以完成此操作）。
- 17. 非交互式标志：`--model`、`--agent-dir`、`--bind`、`--non-interactive`。

## 18. 完整参考

19. 有关详细的分步说明、非交互式脚本、Signal 设置、RPC API 以及向导写入的全部配置字段列表，请参见
    [向导参考](/reference/wizard)。

## 相关文档

- 21. CLI 命令参考：[`openclaw onboard`](/cli/onboard)
- 22. macOS 应用入门： [Onboarding](/start/onboarding)
- 23. 代理首次运行仪式： [Agent Bootstrapping](/start/bootstrapping)
