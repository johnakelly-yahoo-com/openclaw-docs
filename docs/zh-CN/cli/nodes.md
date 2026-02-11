---
summary: "CLI reference for `openclaw nodes` (list/status/approve/invoke, camera/canvas/screen)"
read_when:
  - You’re managing paired nodes (cameras, screen, canvas)
  - You need to approve requests or invoke node commands
title: "nodes"
---

# `openclaw nodes`

Manage paired nodes (devices) and invoke node capabilities.

Related:

- Nodes overview: [Nodes](/nodes)
- 1. 摄像头：[Camera nodes](/nodes/camera)
- 2. 图像：[Image nodes](/nodes/images)

Common options:

- 4. `--url`、`--token`、`--timeout`、`--json`

## 5. 常用命令

```bash
6. openclaw 节点列表
openclaw nodes list
openclaw nodes list --connected
openclaw nodes list --last-connected 24h
openclaw nodes pending
openclaw nodes approve <requestId>
openclaw nodes status
openclaw nodes status --connected
openclaw nodes status --last-connected 24h
```

7. `nodes list` 会打印待处理/已配对表格。 8. 已配对行包含最近一次连接的时长（Last Connect）。
8. 使用 `--connected` 仅显示当前已连接的节点。 10. 使用 `--last-connected <duration>`
   筛选在指定时长内有连接的节点（例如 `24h`、`7d`）。

## 11. 调用 / 运行

```bash
12. openclaw nodes invoke --node <id|name|ip> --command <command> --params <json>
openclaw nodes run --node <id|name|ip> <command...>
openclaw nodes run --raw "git status"
openclaw nodes run --agent main --node <id|name|ip> --raw "git status"
```

13. 调用标志：

- 14. `--params <json>`：JSON 对象字符串（默认 `{}`）。
- 10. `--invoke-timeout <ms>`：节点调用超时（默认 `15000`）。
- 11. `--idempotency-key <key>`：可选的幂等键。

### 17. Exec 风格默认行为

18. `nodes run` 镜像模型的 exec 行为（默认值 + 审批）：

- 19. 读取 `tools.exec.*`（以及 `agents.list[].tools.exec.*` 覆盖项）。
- 20. 在调用 `system.run` 之前使用 exec 审批（`exec.approval.request`）。
- 21. 当设置了 `tools.exec.node` 时，可以省略 `--node`。
- 22. 需要一个声明支持 `system.run` 的节点（macOS 伴生应用或无头节点主机）。

23. 标志：

- 24. `--cwd <path>`：工作目录。
- 25. `--env <key=val>`：环境变量覆盖（可重复）。
- 26. `--command-timeout <ms>`：命令超时。
- 27. `--invoke-timeout <ms>`：节点调用超时（默认 `30000`）。
- 28. `--needs-screen-recording`：需要屏幕录制权限。
- 29. `--raw <command>`：运行一个 shell 字符串（`/bin/sh -lc` 或 `cmd.exe /c`）。
- 30. `--agent <id>`：代理作用域的审批/允许列表（默认为已配置的代理）。
- 31. `--ask <off|on-miss|always>`、`--security <deny|allowlist|full>`：覆盖设置。
