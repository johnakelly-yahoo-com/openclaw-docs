---
title: "47. Pi 开发工作流"
---

# 48. Pi 开发工作流

49. 本指南总结了在 OpenClaw 中开发 pi 集成的一个合理工作流程。

## 50. 类型检查与代码检查

- 1. 类型检查并构建：`pnpm build`
- 2. 代码检查（Lint）：`pnpm lint`
- 3. 格式检查：`pnpm format`
- 4. 推送前的完整关卡：`pnpm lint && pnpm build && pnpm test`

## 5. 运行 Pi 测试

6. 使用专用脚本运行 pi 集成测试集：

```bash
7. scripts/pi/run-tests.sh
```

8. 若要包含验证真实提供方行为的实时测试：

```bash
9. scripts/pi/run-tests.sh --live
```

10. 该脚本通过以下 glob 运行所有与 pi 相关的单元测试：

- 11. `src/agents/pi-*.test.ts`
- 12. `src/agents/pi-embedded-*.test.ts`
- 13. `src/agents/pi-tools*.test.ts`
- 14. `src/agents/pi-settings.test.ts`
- 15. `src/agents/pi-tool-definition-adapter.test.ts`
- 16. `src/agents/pi-extensions/*.test.ts`

## 17. 手动测试

18. 推荐流程：

- 19. 以开发模式运行网关：
  - 20. `pnpm gateway:dev`
- 21. 直接触发 agent：
  - 22. `pnpm openclaw agent --message "Hello" --thinking low`
- 23. 使用 TUI 进行交互式调试：
  - 24. `pnpm tui`

25. 对于工具调用行为，提示执行 `read` 或 `exec` 操作，这样你可以看到工具流式输出和负载处理。

## 26. 清空状态重置

27. 状态存放在 OpenClaw 状态目录下。 Default is `~/.openclaw`. 29. 如果设置了 `OPENCLAW_STATE_DIR`，则使用该目录。

30. 要重置所有内容：

- 31. `openclaw.json` 用于配置
- 32. `credentials/` 用于认证配置文件和令牌
- 33. `agents/<agentId>/sessions/` 用于 agent 会话历史
- 34. `agents/<agentId>/sessions.json` 用于会话索引
- 35. 如果存在旧路径，则包括 `sessions/`
- 36. 如果需要空白工作区，则包括 `workspace/`

37. 如果只想重置会话，请删除该 agent 的 `agents/<agentId>/sessions/` 和 `agents/<agentId>/sessions.json`。 Keep `credentials/` if you do not want to reauthenticate.

## 39. 参考资料

- 40. [https://docs.openclaw.ai/testing](https://docs.openclaw.ai/testing)
- 41. [https://docs.openclaw.ai/start/getting-started](https://docs.openclaw.ai/start/getting-started)
