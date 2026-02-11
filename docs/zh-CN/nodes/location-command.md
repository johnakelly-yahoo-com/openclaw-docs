---
summary: "5. 节点的位置命令（location.get）、权限模式以及后台行为"
read_when:
  - 6. 添加位置节点支持或权限 UI
  - 7. 设计后台位置 + 推送流程
title: "8. 位置命令"
---

# 9. 位置命令（节点）

## 10. TL;DR

- 11. `location.get` 是一个节点命令（通过 `node.invoke`）。
- 12. 默认关闭。
- 13. 设置使用选择器：关闭 / 使用期间 / 始终。
- 14. 单独的开关：精确位置。

## 15. 为什么使用选择器（而不仅仅是一个开关）

16. 操作系统权限是多级的。 17. 我们可以在应用内暴露一个选择器，但操作系统仍然决定实际授予的权限。

- 18. iOS/macOS：用户可以在系统提示/设置中选择 **使用期间** 或 **始终**。 19. 应用可以请求升级权限，但操作系统可能要求前往设置。
- 20. Android：后台位置是一个单独的权限；在 Android 10+ 上通常需要通过设置流程。
- 21. 精确位置是一个单独的授权（iOS 14+ 的“精确”，Android 的“fine” vs “coarse”）。

22. UI 中的选择器驱动我们请求的模式；实际授予的权限存在于操作系统设置中。

## 23. 设置模型

24. 按节点设备：

- 25. `location.enabledMode`: `off | whileUsing | always`
- 26. `location.preciseEnabled`: bool

27. UI 行为：

- 28. 选择 `whileUsing` 会请求前台权限。
- 29. 选择 `always` 时，先确保 `whileUsing`，然后请求后台权限（如有需要则引导用户前往设置）。
- 30. 如果操作系统拒绝所请求的级别，则回退到已授予的最高级别并显示状态。

## 31. 权限映射（node.permissions）

32. 可选。 33. macOS 节点通过权限映射报告 `location`；iOS/Android 可能会省略它。

## 34. 命令：`location.get`

35. 通过 `node.invoke` 调用。

36. 参数（建议）：

```json
37. {
  "timeoutMs": 10000,
  "maxAgeMs": 15000,
  "desiredAccuracy": "coarse|balanced|precise"
}
```

38. 响应负载：

```json
39. {
  "lat": 48.20849,
  "lon": 16.37208,
  "accuracyMeters": 12.5,
  "altitudeMeters": 182.0,
  "speedMps": 0.0,
  "headingDeg": 270.0,
  "timestamp": "2026-01-03T12:34:56.000Z",
  "isPrecise": true,
  "source": "gps|wifi|cell|unknown"
}
```

40. 错误（稳定代码）：

- 41. `LOCATION_DISABLED`：选择器为关闭。
- 42. `LOCATION_PERMISSION_REQUIRED`：缺少所请求模式所需的权限。
- 43. `LOCATION_BACKGROUND_UNAVAILABLE`：应用处于后台，但仅允许“使用期间”。
- 44. `LOCATION_TIMEOUT`：在规定时间内未获得定位。
- 45. `LOCATION_UNAVAILABLE`：系统故障 / 无可用提供者。

## 46. 后台行为（未来）

47. 目标：即使节点处于后台，模型也可以请求位置，但仅在以下情况下：

- 48. 用户选择了 **始终**。
- 49. 操作系统授予了后台位置权限。
- 50. 应用被允许在后台运行以获取位置（iOS 后台模式 / Android 前台服务或特殊许可）。

1. 推送触发流程（未来）：

1. 2. 网关向节点发送推送（静默推送或 FCM 数据）。
2. 3. 节点短暂唤醒并向设备请求位置。
3. 4. 节点将负载转发给网关。

5) 备注：

- 6. iOS：需要始终允许权限 + 后台定位模式。 7. 静默推送可能会被限流；预计会出现间歇性失败。
- 8. Android：后台定位可能需要前台服务；否则预计会被拒绝。

## 9. 模型/工具集成

- 10. 工具层：`nodes` 工具新增 `location_get` 操作（需要节点）。
- 11. CLI：`openclaw nodes location get --node <id>`。
- 12. Agent 指南：仅在用户已启用位置并理解范围时调用。

## 13. UX 文案（建议）

- 14. 关闭：“位置共享已禁用。”
- 15. 使用期间：“仅在 OpenClaw 打开时。”
- 16. 始终允许：“允许后台定位。 17. 需要系统权限。”
- 18. 精确：“使用精确的 GPS 定位。 19. 关闭开关以共享近似位置。”
