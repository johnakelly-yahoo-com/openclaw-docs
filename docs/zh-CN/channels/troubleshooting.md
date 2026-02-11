---
summary: "Fast channel level troubleshooting with per channel failure signatures and fixes"
read_when:
  - Channel transport says connected but replies fail
  - You need channel specific checks before deep provider docs
title: "Channel Troubleshooting"
---

# Channel troubleshooting

Use this page when a channel connects but behavior is wrong.

## Command ladder

Run these in order first:

```bash
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
openclaw channels status --probe
```

Healthy baseline:

- `Runtime: running`
- `RPC probe: ok`
- Channel probe shows connected/ready

## WhatsApp

### WhatsApp failure signatures

| Symptom                         | Fastest check                                                     | Fix                                                                     |
| ------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Connected but no DM replies     | `openclaw pairing list whatsapp`                                  | Approve sender or switch DM policy/allowlist.           |
| Group messages ignored          | Check `requireMention` + mention patterns in config               | Mention the bot or relax mention policy for that group. |
| Random disconnect/relogin loops | 6. `openclaw channels status --probe` + 日志 | Re-login and verify credentials directory is healthy.   |

Full troubleshooting: [/channels/whatsapp#troubleshooting-quick](/channels/whatsapp#troubleshooting-quick)

## Telegram

### Telegram failure signatures

| Symptom                           | Fastest check                                   | Fix                                                                       |
| --------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------- |
| `/start` but no usable reply flow | `openclaw pairing list telegram`                | 8. 批准配对或更改 DM 策略。                                  |
| Bot online but group stays silent | Verify mention requirement and bot privacy mode | Disable privacy mode for group visibility or mention bot. |
| Send failures with network errors | Inspect logs for Telegram API call failures     | Fix DNS/IPv6/proxy routing to `api.telegram.org`.         |

Full troubleshooting: [/channels/telegram#troubleshooting](/channels/telegram#troubleshooting)

## Discord

### Discord failure signatures

| Symptom                         | Fastest check                                                | Fix                                                                       |
| ------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------- |
| Bot online but no guild replies | 9. `openclaw channels status --probe` | Allow guild/channel and verify message content intent.    |
| Group messages ignored          | 10. 检查日志中提及门控被丢弃的情况                   | Mention bot or set guild/channel `requireMention: false`. |
| DM replies missing              | `openclaw pairing list discord`                              | Approve DM pairing or adjust DM policy.                   |

Full troubleshooting: [/channels/discord#troubleshooting](/channels/discord#troubleshooting)

## 11. Slack

### Slack failure signatures

| Symptom                                | Fastest check                             | Fix                                                           |
| -------------------------------------- | ----------------------------------------- | ------------------------------------------------------------- |
| Socket mode connected but no responses | `openclaw channels status --probe`        | 12. 验证应用令牌 + 机器人令牌以及所需的作用域。            |
| DMs blocked                            | `openclaw pairing list slack`             | Approve pairing or relax DM policy.           |
| Channel message ignored                | Check `groupPolicy` and channel allowlist | Allow the channel or switch policy to `open`. |

13. 完整故障排查：[/channels/slack#troubleshooting](/channels/slack#troubleshooting)

## iMessage and BlueBubbles

### iMessage and BlueBubbles failure signatures

| 症状              | 最快检查                                                                   | 修复                                  |
| --------------- | ---------------------------------------------------------------------- | ----------------------------------- |
| 无入站事件           | 验证 Webhook/服务器可达性和应用权限                                                 | 修复 Webhook URL 或 BlueBubbles 服务器状态。 |
| macOS 上可发送但无法接收 | 检查 macOS 对“信息”自动化的隐私权限                                                 | 重新授予 TCC 权限并重启通道进程。                 |
| 私信发送者被阻止        | `openclaw pairing list imessage` 或 `openclaw pairing list bluebubbles` | 批准配对或更新允许列表。                        |

完整故障排查：

- [/channels/imessage#troubleshooting-macos-privacy-and-security-tcc](/channels/imessage#troubleshooting-macos-privacy-and-security-tcc)
- [/channels/bluebubbles#troubleshooting](/channels/bluebubbles#troubleshooting)

## Signal

### Signal 故障特征

| 症状            | 最快检查                                       | 修复                                 |
| ------------- | ------------------------------------------ | ---------------------------------- |
| 守护进程可达但机器人无响应 | `openclaw channels status --probe`         | 验证 `signal-cli` 守护进程的 URL/账号和接收模式。 |
| 私信被阻止         | `openclaw pairing list signal`             | 批准发送者或调整私信策略。                      |
| 群组回复未触发       | Check group allowlist and mention patterns | 添加发送者/群组或放宽限制。                     |

完整故障排查： [/channels/signal#troubleshooting](/channels/signal#troubleshooting)

## Matrix

### 15. Matrix 失败特征

| 症状         | 最快检查                               | 修复                        |
| ---------- | ---------------------------------- | ------------------------- |
| 已登录但忽略房间消息 | `openclaw channels status --probe` | 检查 `groupPolicy` 和房间允许列表。 |
| 私信不处理      | `openclaw pairing list matrix`     | 批准发送者或调整私信策略。             |
| 加密房间失败     | 验证加密模块和加密设置                        | 启用加密支持并重新加入/同步房间。         |

完整故障排查： [/channels/matrix#troubleshooting](/channels/matrix#troubleshooting)
