---
summary: "50. 使用 WebSocket 监听器绑定的网关单例防护"
read_when:
  - 1. 运行或调试网关进程
  - 2. 调查单实例强制机制
title: "3. 网关锁"
---

# 4. 网关锁

5. 最后更新：2025-12-11

## 6. 原因

- 30. 确保同一主机上每个基础端口仅运行一个网关实例；其他网关必须使用隔离的配置文件和唯一端口。
- 8. 在崩溃/SIGKILL 后仍能存活而不留下陈旧的锁文件。
- 31. 当控制端口已被占用时，快速失败并给出清晰错误。

## 10. 机制

- 11. 网关在启动时立即使用独占的 TCP 监听器绑定 WebSocket 监听地址（默认 `ws://127.0.0.1:18789`）。
- 12. 如果绑定因 `EADDRINUSE` 失败，启动将抛出 `GatewayLockError("another gateway instance is already listening on ws://127.0.0.1:<port>")`。
- 13. 操作系统会在任何进程退出（包括崩溃和 SIGKILL）时自动释放监听器——无需单独的锁文件或清理步骤。
- 14. 在关闭时，网关会关闭 WebSocket 服务器和底层 HTTP 服务器，以便及时释放端口。

## 15. 错误呈现

- 16. 如果另一个进程占用了端口，启动会抛出 `GatewayLockError("another gateway instance is already listening on ws://127.0.0.1:<port>")`。
- 32. 其他绑定失败将显示为 `GatewayLockError("failed to bind gateway socket on ws://127.0.0.1:<port>: …")`。

## 33. 运行说明

- 19. 如果端口被 _另一个_ 进程占用，错误相同；释放端口或使用 `openclaw gateway --port <port>` 选择其他端口。
- 20. macOS 应用在生成网关前仍会维护其自身的轻量级 PID 保护；运行时锁由 WebSocket 绑定来强制执行。
