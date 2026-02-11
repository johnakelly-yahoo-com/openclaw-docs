---
summary: "Voice wake and push-to-talk modes plus routing details in the mac app"
read_when:
  - Working on voice wake or PTT pathways
title: "Voice Wake"
---

# Voice Wake & Push-to-Talk

## Modes

- **Wake-word mode** (default): always-on Speech recognizer waits for trigger tokens (`swabbleTriggerWords`). On match it starts capture, shows the overlay with partial text, and auto-sends after silence.
- **Push-to-talk (Right Option hold)**: hold the right Option key to capture immediately—no trigger needed. The overlay appears while held; releasing finalizes and forwards after a short delay so you can tweak text.

## 运行时行为（唤醒词）

- 2. 语音识别器位于 `VoiceWakeRuntime` 中。
- 3. 只有在唤醒词与下一个词之间存在**有意义的停顿**时才会触发（约 0.55 秒间隔）。 4. 覆盖层/提示音可以在停顿时就开始，甚至在命令真正开始之前。
- 5. 静默窗口：语音持续时为 2.0 秒；如果只听到触发词则为 5.0 秒。
- 6. 硬停止：120 秒，用于防止会话失控。
- 7. 会话之间的去抖：350 毫秒。
- 8. 覆盖层由 `VoiceWakeOverlayController` 驱动，支持已提交/易变配色。
- 9. 发送完成后，识别器会干净地重启以监听下一个触发。

## 10. 生命周期不变式

- 11. 如果启用了 Voice Wake 且权限已授予，唤醒词识别器应当处于监听状态（除非正在进行显式的按键说话捕获）。
- 12. 覆盖层的可见性（包括通过 X 按钮手动关闭）绝不能阻止识别器恢复。

## 13. 覆盖层卡住的失败模式（之前）

14. 之前，如果覆盖层卡在可见状态并且你手动关闭它，Voice Wake 可能会显得“失效”，因为运行时的重启尝试可能会被覆盖层可见性阻塞，而且之后也没有安排再次重启。

15. 加固：

- 16. 唤醒运行时的重启不再受覆盖层可见性阻塞。
- 17. 覆盖层关闭完成会通过 `VoiceSessionCoordinator` 触发一次 `VoiceWakeRuntime.refresh(...)`，因此手动通过 X 关闭总能恢复监听。

## 18. 按键说话（Push-to-talk）细节

- 19. 热键检测使用全局 `.flagsChanged` 监听 **右 Option**（`keyCode 61` + `.option`）。 20. 我们只观察事件（不吞掉）。
- 21. 捕获管线位于 `VoicePushToTalk`：立即启动语音识别，将部分结果流式发送到覆盖层，并在松开时调用 `VoiceWakeForwarder`。
- 22. 当按键说话开始时，我们会暂停唤醒词运行时以避免音频 tap 冲突；松开后会自动重启。
- 23. 权限：需要麦克风 + 语音；要看到事件需要“辅助功能/输入监控”批准。
- 24. 外接键盘：有些可能不会按预期暴露右 Option——如果用户反馈漏检，提供一个备用快捷键。

## 25. 面向用户的设置

- 26. **Voice Wake** 开关：启用唤醒词运行时。
- 27. **按住 Cmd+Fn 说话**：启用按键说话监听。 在 macOS < 26 上禁用。
- 语言与麦克风选择器、实时电平表、触发词表、测试器（仅本地；不转发）。
- 30. 麦克风选择器会在设备断开时保留上一次选择，显示已断开提示，并在其返回前临时回退到系统默认设备。
- 31. **声音**：在检测到触发和发送时播放提示音；默认使用 macOS 的“Glass”系统音。 你可以为每个事件选择任意 `NSSound` 可加载的文件（例如 MP3/WAV/AIFF），或选择**无声音**。

## 33. 转发行为

- 34. 当启用 Voice Wake 时，转录内容会被转发到活动的网关/代理（与 mac 应用其余部分使用的本地/远程模式相同）。
- 35. 回复会投递到**最近使用的主提供方**（WhatsApp/Telegram/Discord/WebChat）。 如果投递失败，错误会被记录，且仍可通过 WebChat/会话日志查看该运行。

## 37. 转发负载

- 38. `VoiceWakeForwarder.prefixedTranscript(_:)` 在发送前会添加机器提示前缀。 39. 在唤醒词和按键说话路径之间共享。

## 40. 快速验证

- 41. 打开按键说话，按住 Cmd+Fn，说话，松开：覆盖层应显示部分结果然后发送。
- 42. 按住期间，菜单栏的耳朵应保持放大（使用 `triggerVoiceEars(ttl:nil)`）；松开后会恢复。
