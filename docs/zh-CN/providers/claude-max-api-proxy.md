---
summary: "Use Claude Max/Pro subscription as an OpenAI-compatible API endpoint"
read_when:
  - You want to use Claude Max subscription with OpenAI-compatible tools
  - You want a local API server that wraps Claude Code CLI
  - You want to save money by using subscription instead of API keys
title: "Claude Max API Proxy"
---

# Claude Max API Proxy

31. **claude-max-api-proxy** 是一个社区工具，可将你的 Claude Max/Pro 订阅作为与 OpenAI 兼容的 API 端点暴露出来。 2. 这使你可以在任何支持 OpenAI API 格式的工具中使用你的订阅。

## 3. 为什么使用它？

| 4. 实现方式           | 5. 成本                                      | 6. 最适合           |
| ---------------------------------------- | ----------------------------------------------------------------- | --------------------------------------- |
| 32. Anthropic API | 33. 按 token 计费（Opus：输入约 $15/百万，输出约 $75/百万） | 9. 生产级应用，高调用量    |
| 10. Claude Max 订阅 | 34. 每月 $200 的固定费用                          | 12. 个人使用、开发、无限用量 |

13. 如果你拥有 Claude Max 订阅，并希望将其用于兼容 OpenAI 的工具，这个代理可以为你节省大量成本。

## 14. 工作原理

```
15. 你的应用 → claude-max-api-proxy → Claude Code CLI → Anthropic（通过订阅）
     （OpenAI 格式）              （格式转换）      （使用你的登录）
```

16. 该代理：

1. 17. 在 `http://localhost:3456/v1/chat/completions` 接收 OpenAI 格式的请求
2. 18. 将其转换为 Claude Code CLI 命令
3. 19. 以 OpenAI 格式返回响应（支持流式传输）

## 20) 安装

```bash
21. # 需要 Node.js 20+ 和 Claude Code CLI
npm install -g claude-max-api-proxy

# 验证 Claude CLI 已完成认证
claude --version
```

## 22. 使用方法

### 23. 启动服务器

```bash
24. claude-max-api
# 服务器运行在 http://localhost:3456
```

### 25. 测试

```bash
26. # 健康检查
curl http://localhost:3456/health

# 列出模型
curl http://localhost:3456/v1/models

# 聊天补全
curl http://localhost:3456/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-opus-4",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### 27. 与 OpenClaw 一起使用

28. 你可以将 OpenClaw 指向该代理，作为自定义的 OpenAI 兼容端点：

```json5
29. {
  env: {
    OPENAI_API_KEY: "not-needed",
    OPENAI_BASE_URL: "http://localhost:3456/v1",
  },
  agents: {
    defaults: {
      model: { primary: "openai/claude-opus-4" },
    },
  },
}
```

## 30. 可用模型

| 31. 模型 ID             | 32. 映射到             |
| -------------------------------------------- | ------------------------------------------ |
| 33. `claude-opus-4`   | 34. Claude Opus 4   |
| 35. `claude-sonnet-4` | 36. Claude Sonnet 4 |
| 37. `claude-haiku-4`  | 38. Claude Haiku 4  |

## 39. 在 macOS 上自动启动

40. 创建一个 LaunchAgent 以自动运行该代理：

```bash
41. cat > ~/Library/LaunchAgents/com.claude-max-api.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.claude-max-api</string>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/local/bin/node</string>
    <string>/usr/local/lib/node_modules/claude-max-api-proxy/dist/server/standalone.js</string>
  </array>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key>
    <string>/usr/local/bin:/opt/homebrew/bin:~/.local/bin:/usr/bin:/bin</string>
  </dict>
</dict>
</plist>
EOF

launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.claude-max-api.plist
```

## 42. 链接

- 43. **npm：** [https://www.npmjs.com/package/claude-max-api-proxy](https://www.npmjs.com/package/claude-max-api-proxy)
- 44. **GitHub：** [https://github.com/atalovesyou/claude-max-api-proxy](https://github.com/atalovesyou/claude-max-api-proxy)
- 45. **问题反馈：** [https://github.com/atalovesyou/claude-max-api-proxy/issues](https://github.com/atalovesyou/claude-max-api-proxy/issues)

## 46. 备注

- 47. 这是一个**社区工具**，并未得到 Anthropic 或 OpenClaw 的官方支持
- 48. 需要有效的 Claude Max/Pro 订阅，并已完成 Claude Code CLI 认证
- 49. 该代理在本地运行，不会将数据发送到任何第三方服务器
- 50. 完全支持流式响应

## 另请参阅

- 35. [Anthropic provider](/providers/anthropic) - 通过 Claude setup-token 或 API key 的原生 OpenClaw 集成
- [OpenAI 提供商](/providers/openai) - 适用于 OpenAI/Codex 订阅
