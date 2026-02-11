---
summary: "6. 排查节点配对、前台要求、权限以及工具失败问题"
read_when:
  - 7. 节点已连接，但 camera/canvas/screen/exec 工具失败
  - 8. 你需要理解节点配对与审批的心智模型
title: "9. 节点故障排查"
---

# 10. 节点故障排查

11. 当状态中可见节点但节点工具失败时，使用此页面。

## 12. 命令阶梯

```bash
13. openclaw status
```

openclaw gateway status

```bash
openclaw logs --follow
```

openclaw doctor

- openclaw channels status --probe
- 14. 然后运行节点特定检查：
- 15. openclaw nodes status

## openclaw nodes describe --node <idOrNameOrIp>

openclaw approvals get --node <idOrNameOrIp>

16. 健康信号：

```bash
17. 节点已连接并以角色 `node` 完成配对。
```

18. `nodes describe` 包含你正在调用的能力。

## 19. Exec 审批显示预期的模式/允许列表。

| 20. 前台要求          | 21. `canvas.*`、`camera.*` 和 `screen.*` 在 iOS/Android 节点上仅限前台。 | 22. 快速检查与修复：                | 23. openclaw nodes describe --node <idOrNameOrIp> | openclaw nodes canvas snapshot --node <idOrNameOrIp> |
| ---------------------------------------- | ------------------------------------------------------------------------------------ | -------------------------------------------------- | ------------------------------------------------------------------------ | ---------------------------------------------------- |
| openclaw logs --follow                   | 24. 如果看到 `NODE_BACKGROUND_UNAVAILABLE`，请将节点应用切换到前台后重试。        | 25. 权限矩阵                    | 26. 能力                                            | 27. iOS                       |
| 28. Android       | 29. macOS 节点应用                                                | 30. 典型失败代码                  | 31. `camera.snap`、`camera.clip`                   | 32. 相机（剪辑音频需要麦克风）             |
| 33. 相机（剪辑音频需要麦克风） | 34. 相机（剪辑音频需要麦克风）                                             | 35. `*_PERMISSION_REQUIRED` | 36. `screen.record`                               | 37. 屏幕录制（麦克风可选）               |
| 38. 屏幕捕获提示（麦克风可选） | 39. 屏幕录制                                                      | 40. `*_PERMISSION_REQUIRED` | 41. `location.get`                                | 42. 使用期间或始终（取决于模式）            |

## 1. 配对与审批的区别

2. 这是两个不同的关卡：

1. 3. **设备配对**：该节点能否连接到网关？
2. **执行审批**：该节点是否可以运行某个特定的 shell 命令？

5) 快速检查：

```bash
6. openclaw devices list
openclaw nodes status
openclaw approvals get --node <idOrNameOrIp>
openclaw approvals allowlist add --node <idOrNameOrIp> "/usr/bin/uname"
```

如果缺少配对，请先批准该节点设备。
8. 如果配对正常但 `system.run` 失败，请修复执行审批/允许列表。

## 9. 常见节点错误码

- 10. `NODE_BACKGROUND_UNAVAILABLE` → 应用在后台；将其切换到前台。
- 11. `CAMERA_DISABLED` → 节点设置中关闭了摄像头开关。
- `*_PERMISSION_REQUIRED` → 缺少或被拒绝了操作系统权限。
- 13. `LOCATION_DISABLED` → 定位模式已关闭。
- 14. `LOCATION_PERMISSION_REQUIRED` → 请求的定位模式未被授予。
- 15. `LOCATION_BACKGROUND_UNAVAILABLE` → 应用在后台，但仅拥有“使用期间”权限。
- `SYSTEM_RUN_DENIED: approval required` → 执行请求需要显式批准。
- 17. `SYSTEM_RUN_DENIED: allowlist miss` → 命令被允许列表模式阻止。

## 18. 快速恢复循环

```bash
19. openclaw nodes status
openclaw nodes describe --node <idOrNameOrIp>
openclaw approvals get --node <idOrNameOrIp>
openclaw logs --follow
```

如果仍然卡住：

- 21. 重新批准设备配对。
- 22. 重新打开节点应用（切换到前台）。
- 重新授予操作系统权限。
- 24. 重新创建/调整执行审批策略。

25. 相关：

- 26. [/nodes/index](/nodes/index)
- [/nodes/camera](/nodes/camera)
- 28. [/nodes/location-command](/nodes/location-command)
- 29. [/tools/exec-approvals](/tools/exec-approvals)
- 30. [/gateway/pairing](/gateway/pairing)
