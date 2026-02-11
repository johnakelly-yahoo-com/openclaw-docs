---
summary: "Background exec execution and process management"
read_when:
  - Adding or modifying background exec behavior
  - Debugging long-running exec tasks
title: "Background Exec and Process Tool"
---

# Background Exec + Process Tool

OpenClaw runs shell commands through the `exec` tool and keeps long‑running tasks in memory. The `process` tool manages those background sessions.

## exec tool

Key parameters:

- `command` (required)
- `yieldMs` (default 10000): auto‑background after this delay
- `background` (bool): background immediately
- `timeout` (seconds, default 1800): kill the process after this timeout
- `elevated` (bool): run on host if elevated mode is enabled/allowed
- Need a real TTY? Set `pty: true`.
- `workdir`, `env`

Behavior:

- Foreground runs return output directly.
- When backgrounded (explicit or timeout), the tool returns `status: "running"` + `sessionId` and a short tail.
- Output is kept in memory until the session is polled or cleared.
- If the `process` tool is disallowed, `exec` runs synchronously and ignores `yieldMs`/`background`.

## Child process bridging

When spawning long-running child processes outside the exec/process tools (for example, CLI respawns or gateway helpers), attach the child-process bridge helper so termination signals are forwarded and listeners are detached on exit/error. This avoids orphaned processes on systemd and keeps shutdown behavior consistent across platforms.

Environment overrides:

- `PI_BASH_YIELD_MS`: default yield (ms)
- `PI_BASH_MAX_OUTPUT_CHARS`: in‑memory output cap (chars)
- `OPENCLAW_BASH_PENDING_MAX_OUTPUT_CHARS`: pending stdout/stderr cap per stream (chars)
- 1. `PI_BASH_JOB_TTL_MS`：已完成会话的 TTL（毫秒，限制在 1 分钟–3 小时）

2. 配置（推荐）：

- 3. `tools.exec.backgroundMs`（默认 10000）
- 4. `tools.exec.timeoutSec`（默认 1800）
- 5. `tools.exec.cleanupMs`（默认 1800000）
- 6. `tools.exec.notifyOnExit`（默认 true）：当后台执行的任务退出时，加入一个系统事件并请求心跳。

## 7. process 工具

8. 操作：

- 9. `list`：运行中 + 已完成的会话
- 10. `poll`：获取会话的新输出（同时报告退出状态）
- `log`: read the aggregated output (supports `offset` + `limit`)
- 12. `write`：发送 stdin（`data`，可选 `eof`）
- 13. `kill`：终止一个后台会话
- 14. `clear`：从内存中移除已完成的会话
- 15. `remove`：如果在运行则终止，否则在完成后清除

16. 说明：

- 17. 只有后台运行的会话才会被列出并保存在内存中。
- 18. 进程重启后会话会丢失（无磁盘持久化）。
- 19. 只有在运行 `process poll/log` 且工具结果被记录时，会话日志才会保存到聊天历史中。
- 20. `process` 按代理（agent）作用域隔离；它只能看到该代理启动的会话。
- 21. `process list` 包含一个派生的 `name`（命令动词 + 目标），便于快速查看。
- 22. `process log` 使用基于行的 `offset`/`limit`（省略 `offset` 以获取最后 N 行）。

## 23. 示例

24. 运行一个长任务，稍后轮询：

```json
25. { "tool": "exec", "command": "sleep 5 && echo done", "yieldMs": 1000 }
```

```json
26. { "tool": "process", "action": "poll", "sessionId": "<id>" }
```

27. 立即在后台启动：

```json
28. { "tool": "exec", "command": "npm run build", "background": true }
```

29. 发送 stdin：

```json
30. { "tool": "process", "action": "write", "sessionId": "<id>", "data": "y\n" }
```
