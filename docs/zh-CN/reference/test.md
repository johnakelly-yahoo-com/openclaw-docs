---
summary: "8. 如何在本地运行测试（vitest），以及何时使用 force/coverage 模式"
read_when:
  - 9. 运行或修复测试
title: "10. 测试"
---

# 11. 测试

- 12. 完整测试套件（suites、live、Docker）：[Testing](/help/testing)

- 13. `pnpm test:force`：终止任何仍在占用默认控制端口的网关进程，然后使用隔离的网关端口运行完整的 Vitest 套件，以避免服务器测试与正在运行的实例发生冲突。 14. 当先前的网关运行导致端口 18789 被占用时使用此命令。

- 15. `pnpm test:coverage`：使用 V8 覆盖率运行 Vitest。 16. 全局阈值为行/分支/函数/语句 70%。 17. 覆盖率排除了集成较重的入口点（CLI 接线、gateway/telegram 桥接、webchat 静态服务器），以便将目标集中在可进行单元测试的逻辑上。

- 18. `pnpm test:e2e`：运行网关端到端冒烟测试（多实例 WS/HTTP/node 配对）。

- 19. `pnpm test:live`：运行提供方实时测试（minimax/zai）。 20. 需要 API 密钥以及 `LIVE=1`（或特定提供方的 `*_LIVE_TEST=1`）才能取消跳过。

## 21. 模型延迟基准测试（本地密钥）

22. 脚本：[`scripts/bench-model.ts`](https://github.com/openclaw/openclaw/blob/main/scripts/bench-model.ts)

23. 用法：

- 24. `source ~/.profile && pnpm tsx scripts/bench-model.ts --runs 10`
- Optional env: `MINIMAX_API_KEY`, `MINIMAX_BASE_URL`, `MINIMAX_MODEL`, `ANTHROPIC_API_KEY`
- 26. 默认提示词：“Reply with a single word: ok. 27. 不要使用标点或添加额外文本。”

28. 最近一次运行（2025-12-31，20 次）：

- 29. minimax 中位数 1279ms（最小 1114，最大 2431）
- 30. opus 中位数 2454ms（最小 1224，最大 3170）

## 31. 入门引导 E2E（Docker）

32. Docker 是可选的；仅在进行容器化入门冒烟测试时需要。

Full cold-start flow in a clean Linux container:

```bash
34. scripts/e2e/onboard-docker.sh
```

35. 该脚本通过伪 TTY 驱动交互式向导，验证配置/工作区/会话文件，然后启动网关并运行 `openclaw health`。

## 36. 二维码导入冒烟测试（Docker）

37. 确保 `qrcode-terminal` 在 Docker 中的 Node 22+ 下可加载：

```bash
38. pnpm test:docker:qr
```
