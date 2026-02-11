---
summary: "25. OpenClaw（macOS 应用）的首次运行引导流程"
read_when:
  - 26. 设计 macOS 引导助手
  - 27. 实现认证或身份设置
title: "28. 引导（macOS 应用）"
sidebarTitle: "29. 引导：macOS 应用"
---

# 30. 引导（macOS 应用）

31. 本文档描述 **当前** 的首次运行引导流程。 32. 目标是一个
    流畅的“第 0 天”体验：选择 Gateway 的运行位置，连接认证，运行向导，并让代理自行完成引导启动。

<Steps>
<Step title="Approve macOS warning">33. 
<Frame><img src="/assets/macos-onboarding/01-macos-warning.jpeg" alt="" />34. 
</Frame></Step>
<Step title="Approve find local networks">35. 
<Frame><img src="/assets/macos-onboarding/02-local-networks.jpeg" alt="" />36. 
</Frame></Step>
<Step title="Welcome and security notice">37. 
<Frame caption="阅读显示的安全提示并据此做出决定"><img src="/assets/macos-onboarding/03-security-notice.png" alt="" />38. 
</Frame></Step>
<Step title="Local vs Remote">39. 
<Frame><img src="/assets/macos-onboarding/04-choose-gateway.png" alt="" />
</Frame>

40. Gateway 在哪里运行？

- 41. **此 Mac（仅本地）：** 引导流程可以运行 OAuth 流程并将凭据写入本地。
- 42. **远程（通过 SSH/Tailnet）：** 引导流程**不会**在本地运行 OAuth；凭据必须已存在于 gateway 主机上。
- 43. **稍后配置：** 跳过设置，让应用保持未配置状态。

<Tip>
44. **Gateway 认证提示：**
- 向导现在即使在回环情况下也会生成一个 **token**，因此本地 WS 客户端必须进行认证。
45. - 如果你禁用认证，任何本地进程都可以连接；仅在完全受信任的机器上使用。
46. - 对于多机器访问或非回环绑定，请使用 **token**。
</Tip>
</Step>
<Step title="Permissions">48. 
<Frame caption="选择你希望授予 OpenClaw 的权限"><img src="/assets/macos-onboarding/05-permissions.png" alt="" />
</Frame>

49. 引导流程请求所需的 TCC 权限，用于：

- 50. 自动化（AppleScript）
- Notifications
- Accessibility
- 23. 屏幕录制
- 24. 麦克风
- Speech Recognition
- Camera
- 25. 位置

</Step>
<Step title="CLI">
  <Info>This step is optional</Info>
  The app can install the global `openclaw` CLI via npm/pnpm so terminal
  workflows and launchd tasks work out of the box.
</Step>
<Step title="Onboarding Chat (dedicated session)">
  After setup, the app opens a dedicated onboarding chat session so the agent can
  introduce itself and guide next steps. This keeps first‑run guidance separate
  from your normal conversation. See [Bootstrapping](/start/bootstrapping) for
  what happens on the gateway host during the first agent run.
</Step>
</Steps>
