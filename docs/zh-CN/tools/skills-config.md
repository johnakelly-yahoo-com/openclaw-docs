---
summary: "10. 技能配置架构与示例"
read_when:
  - 11. 添加或修改技能配置
  - 12. 调整捆绑的允许列表或安装行为
title: "13. 技能配置"
---

# Skills Config

15. 所有与技能相关的配置都位于 `~/.openclaw/openclaw.json` 中的 `skills` 下。

```json5
{
  skills: {
    allowBundled: ["gemini", "peekaboo"],
    load: {
      extraDirs: ["~/Projects/agent-scripts/skills", "~/Projects/oss/some-skill-pack/skills"],
      watch: true,
      watchDebounceMs: 250,
    },
    install: {
      preferBrew: true,
      nodeManager: "npm", // npm | pnpm | yarn | bun (Gateway runtime still Node; bun not recommended)
    },
    entries: {
      "nano-banana-pro": {
        enabled: true,
        apiKey: "GEMINI_KEY_HERE",
        env: {
          GEMINI_API_KEY: "GEMINI_KEY_HERE",
        },
      },
      peekaboo: { enabled: true },
      sag: { enabled: false },
    },
  },
}
```

## 17. 字段

- 18. `allowBundled`：仅针对**捆绑**技能的可选允许列表。 19. 设置后，只有列表中的捆绑技能才有资格（托管/工作区技能不受影响）。
- 20. `load.extraDirs`：要扫描的额外技能目录（优先级最低）。
- 21. `load.watch`：监视技能文件夹并刷新技能快照（默认：true）。
- 22. `load.watchDebounceMs`：技能监视事件的防抖时间（毫秒，默认：250）。
- 23. `install.preferBrew`：在可用时优先使用 brew 安装器（默认：true）。
- `install.nodeManager`: node installer preference (`npm` | `pnpm` | `yarn` | `bun`, default: npm).
  25. 这只影响**技能安装**；Gateway 运行时仍应使用 Node（不建议在 WhatsApp/Telegram 上使用 Bun）。
- 26. `entries.<skillKey>`27. ：按技能覆盖设置。

28. 按技能字段：

- 29. `enabled`：即使技能已捆绑/安装，也可将其设置为 `false` 以禁用。
- 30. `env`：为代理运行注入的环境变量（仅在尚未设置时）。
- 31. `apiKey`：为声明了主环境变量的技能提供的可选便捷配置。

## 32. 说明

- 33. `entries` 下的键默认映射为技能名称。 34. 如果技能定义了
      `metadata.openclaw.skillKey`，则使用该键。
- 35. 当启用监视器时，对技能的更改会在下一次代理轮次中生效。

### 36. 沙盒化技能与环境变量

37. 当会话处于**沙盒**状态时，技能进程会在 Docker 内运行。 38. 沙盒**不会**继承主机的 `process.env`。

39. 可使用以下方式之一：

- 40. `agents.defaults.sandbox.docker.env`（或按代理的 `agents.list[].sandbox.docker.env`）
- 41. 将环境变量烘焙进你的自定义沙盒镜像

42. 全局 `env` 和 `skills.entries.<skill>43. `.env/apiKey\` 仅适用于**主机**运行。
