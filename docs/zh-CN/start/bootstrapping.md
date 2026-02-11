---
summary: "Agent bootstrapping ritual that seeds the workspace and identity files"
read_when:
  - Understanding what happens on the first agent run
  - Explaining where bootstrapping files live
  - Debugging onboarding identity setup
title: "Agent Bootstrapping"
sidebarTitle: "Bootstrapping"
---

# 2. Agent 引导

Bootstrapping is the **first‑run** ritual that prepares an agent workspace and
collects identity details. 4. 它发生在完成入门之后，即代理第一次启动时。

## 5. 引导的作用

On the first agent run, OpenClaw bootstraps the workspace (default
`~/.openclaw/workspace`):

- Seeds `AGENTS.md`, `BOOTSTRAP.md`, `IDENTITY.md`, `USER.md`.
- 8. 运行一个简短的问答仪式（一次一个问题）。
- 9. 将身份信息和偏好写入 `IDENTITY.md`、`USER.md`、`SOUL.md`。
- 10. 完成后删除 `BOOTSTRAP.md`，以确保只运行一次。

## 11. 运行位置

12. 引导始终在 **网关主机** 上运行。 13. 如果 macOS 应用连接到
    远程 Gateway，工作区和引导文件将位于该远程
    机器上。

<Note>
When the Gateway runs on another machine, edit workspace files on the gateway
host (for example, `user@gateway-host:~/.openclaw/workspace`).
</Note>

## 15. 相关文档

- 16. macOS 应用入门：[Onboarding](/start/onboarding)
- 17. 工作区布局：[Agent workspace](/concepts/agent-workspace)
