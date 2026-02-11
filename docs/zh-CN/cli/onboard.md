---
summary: "32. `openclaw onboard` 的 CLI 参考（交互式引导向导）"
read_when:
  - 33. 你希望获得关于网关、工作区、认证、渠道和技能的引导式设置
title: "34. onboard"
---

# 35. `openclaw onboard`

36. 交互式引导向导（本地或远程 Gateway 设置）。

## 12. 相关指南

- 38. CLI 引导中心：[Onboarding Wizard (CLI)](/start/wizard)
- 39. CLI 引导参考：[CLI Onboarding Reference](/start/wizard-cli-reference)
- 40. CLI 自动化：[CLI Automation](/start/wizard-cli-automation)
- 41. macOS 引导：[Onboarding (macOS App)](/start/onboarding)

## 42. 示例

```bash
43. openclaw onboard
openclaw onboard --flow quickstart
openclaw onboard --flow manual
openclaw onboard --mode remote --remote-url ws://gateway-host:18789
```

44. 流程说明：

- 45. `quickstart`：最少提示，自动生成网关令牌。
- 46. `manual`：用于端口/绑定/认证的完整提示（`advanced` 的别名）。
- 47. 最快开始首次聊天：`openclaw dashboard`（控制界面，无需设置渠道）。

## 48. 常见后续命令

```bash
49. openclaw configure
openclaw agents add <name>
```

<Note>
50. `--json` 并不意味着非交互模式。 Use `--non-interactive` for scripts.
</Note>
