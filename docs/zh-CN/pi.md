---
title: "42. Pi 集成架构"
---

# 43. Pi 集成架构

44. 本文档描述了 OpenClaw 如何与 [pi-coding-agent](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent) 及其兄弟包（`pi-ai`、`pi-agent-core`、`pi-tui`）集成，以支持其 AI agent 能力。

## 45. 概述

46. OpenClaw 使用 pi SDK 将 AI 编码 agent 嵌入到其消息网关架构中。 47. OpenClaw 并非将 pi 作为子进程启动或使用 RPC 模式，而是直接通过 `createAgentSession()` 导入并实例化 pi 的 `AgentSession`。 48. 这种嵌入式方法提供了：

- 49. 对会话生命周期和事件处理的完全控制
- 50. 自定义工具注入（消息传递、沙箱、特定渠道的操作）
- 按频道/上下文进行系统提示自定义
- 支持分支/压缩的会话持久化
- 多账号认证配置轮换并支持故障转移
- Provider-agnostic model switching

## 包依赖

```json
{
  "@mariozechner/pi-agent-core": "0.49.3",
  "@mariozechner/pi-ai": "0.49.3",
  "@mariozechner/pi-coding-agent": "0.49.3",
  "@mariozechner/pi-tui": "0.49.3"
}
```

| 包                 | 用途                                                                              |
| ----------------- | ------------------------------------------------------------------------------- |
| `pi-ai`           | 核心 LLM 抽象：`Model`、`streamSimple`、消息类型、提供商 API                                   |
| `pi-agent-core`   | Agent 循环、工具执行、`AgentMessage` 类型                                                 |
| `pi-coding-agent` | 高级 SDK：`createAgentSession`、`SessionManager`、`AuthStorage`、`ModelRegistry`、内置工具 |
| `pi-tui`          | 终端 UI 组件（用于 OpenClaw 的本地 TUI 模式）                                                |

## 文件结构

```
src/agents/
├── pi-embedded-runner.ts          # 从 pi-embedded-runner/ 重新导出
├── pi-embedded-runner/
│   ├── run.ts                     # 主入口：runEmbeddedPiAgent()
│   ├── run/
│   │   ├── attempt.ts             # 单次尝试逻辑，包含会话设置
│   │   ├── params.ts              # RunEmbeddedPiAgentParams 类型
│   │   ├── payloads.ts            # 从运行结果构建响应负载
│   │   ├── images.ts              # 视觉模型图像注入
│   │   └── types.ts               # EmbeddedRunAttemptResult
│   ├── abort.ts                   # 中止错误检测
│   ├── cache-ttl.ts               # 用于上下文裁剪的缓存 TTL 跟踪
│   ├── compact.ts                 # 手动/自动压缩逻辑
│   ├── extensions.ts              # 为嵌入式运行加载 pi 扩展
│   ├── extra-params.ts            # 提供商特定的流式参数
│   ├── google.ts                  # Google/Gemini 回合顺序修复
│   ├── history.ts                 # 历史限制（私聊 vs 群组）
│   ├── lanes.ts                   # 会话/全局命令通道
│   ├── logger.ts                  # 子系统日志记录器
│   ├── model.ts                   # 通过 ModelRegistry 进行模型解析
│   ├── runs.ts                    # 活跃运行跟踪、中止、队列
│   ├── sandbox-info.ts            # 系统提示用的沙箱信息
│   ├── session-manager-cache.ts   # SessionManager 实例缓存
│   ├── session-manager-init.ts    # 会话文件初始化
│   ├── system-prompt.ts           # 系统提示构建器
│   ├── tool-split.ts              # 将工具拆分为 builtIn 与 custom
│   ├── types.ts                   # EmbeddedPiAgentMeta、EmbeddedPiRunResult
│   └── utils.ts                   # ThinkLevel 映射、错误描述
├── pi-embedded-subscribe.ts       # 会话事件订阅/分发
├── pi-embedded-subscribe.types.ts # SubscribeEmbeddedPiSessionParams
├── pi-embedded-subscribe.handlers.ts # 事件处理器工厂
├── pi-embedded-subscribe.handlers.lifecycle.ts
├── pi-embedded-subscribe.handlers.types.ts
├── pi-embedded-block-chunker.ts   # 流式块回复分块
├── pi-embedded-messaging.ts       # 消息工具发送跟踪
├── pi-embedded-helpers.ts         # 错误分类、回合校验
├── pi-embedded-helpers/           # 辅助模块
├── pi-embedded-utils.ts           # 格式化工具
├── pi-tools.ts                    # createOpenClawCodingTools()
├── pi-tools.abort.ts              # 工具用 AbortSignal 包装
├── pi-tools.policy.ts             # 工具白名单/黑名单策略
├── pi-tools.read.ts               # Read 工具自定义
├── pi-tools.schema.ts             # 工具 schema 规范化
├── pi-tools.types.ts              # AnyAgentTool 类型别名
├── pi-tool-definition-adapter.ts  # AgentTool -> ToolDefinition 适配器
├── pi-settings.ts                 # 设置覆盖
├── pi-extensions/                 # 自定义 pi 扩展
│   ├── compaction-safeguard.ts    # 保护扩展
│   ├── compaction-safeguard-runtime.ts
│   ├── context-pruning.ts         # 基于 Cache-TTL 的上下文裁剪扩展
│   └── context-pruning/
├── model-auth.ts                  # 认证配置解析
├── auth-profiles.ts               # 配置存储、冷却、故障转移
├── model-selection.ts             # 默认模型解析
├── models-config.ts               # models.json 生成
├── model-catalog.ts               # 模型目录缓存
├── context-window-guard.ts        # 上下文窗口校验
├── failover-error.ts              # FailoverError 类
├── defaults.ts                    # DEFAULT_PROVIDER、DEFAULT_MODEL
├── system-prompt.ts               # buildAgentSystemPrompt()
├── system-prompt-params.ts        # 系统提示参数解析
├── system-prompt-report.ts        # 调试报告生成
├── tool-summaries.ts              # 工具描述摘要
├── tool-policy.ts                 # 工具策略解析
├── transcript-policy.ts           # 转录校验策略
├── skills.ts                      # 技能快照/提示构建
├── skills/                        # 技能子系统
├── sandbox.ts                     # 沙箱上下文解析
├── sandbox/                       # 沙箱子系统
├── channel-tools.ts               # 按频道注入工具
├── openclaw-tools.ts              # OpenClaw 专用工具
├── bash-tools.ts                  # exec/process 工具
├── apply-patch.ts                 # apply_patch 工具（OpenAI）
├── tools/                         # 各个工具实现
│   ├── browser-tool.ts
│   ├── canvas-tool.ts
│   ├── cron-tool.ts
│   ├── discord-actions*.ts
│   ├── gateway-tool.ts
│   ├── image-tool.ts
│   ├── message-tool.ts
│   ├── nodes-tool.ts
│   ├── session*.ts
│   ├── slack-actions.ts
│   ├── telegram-actions.ts
│   ├── web-*.ts
│   └── whatsapp-actions.ts
└── ...
```

## Core Integration Flow

### 1. 运行嵌入式 Agent

主入口位于 `pi-embedded-runner/run.ts` 中的 `runEmbeddedPiAgent()`：

```typescript
import { runEmbeddedPiAgent } from "./agents/pi-embedded-runner.js";

const result = await runEmbeddedPiAgent({
  sessionId: "user-123",
  sessionKey: "main:whatsapp:+1234567890",
  sessionFile: "/path/to/session.jsonl",
  workspaceDir: "/path/to/workspace",
  config: openclawConfig,
  prompt: "Hello, how are you?",
  provider: "anthropic",
  model: "claude-sonnet-4-20250514",
  timeoutMs: 120_000,
  runId: "run-abc",
  onBlockReply: async (payload) => {
    await sendToChannel(payload.text, payload.mediaUrls);
  },
});
```

### 2. 会话创建

在 `runEmbeddedAttempt()`（由 `runEmbeddedPiAgent()` 调用）内部，使用 pi SDK：

```typescript
import {
  createAgentSession,
  DefaultResourceLoader,
  SessionManager,
  SettingsManager,
} from "@mariozechner/pi-coding-agent";

const resourceLoader = new DefaultResourceLoader({
  cwd: resolvedWorkspace,
  agentDir,
  settingsManager,
  additionalExtensionPaths,
});
await resourceLoader.reload();

const { session } = await createAgentSession({
  cwd: resolvedWorkspace,
  agentDir,
  authStorage: params.authStorage,
  modelRegistry: params.modelRegistry,
  model: params.model,
  thinkingLevel: mapThinkingLevel(params.thinkLevel),
  tools: builtInTools,
  customTools: allCustomTools,
  sessionManager,
  settingsManager,
  resourceLoader,
});

applySystemPromptOverrideToSession(session, systemPromptOverride);
```

### 3. 事件订阅

`subscribeEmbeddedPiSession()` 订阅 pi 的 `AgentSession` 事件：

```typescript
const subscription = subscribeEmbeddedPiSession({
  session: activeSession,
  runId: params.runId,
  verboseLevel: params.verboseLevel,
  reasoningMode: params.reasoningLevel,
  toolResultFormat: params.toolResultFormat,
  onToolResult: params.onToolResult,
  onReasoningStream: params.onReasoningStream,
  onBlockReply: params.onBlockReply,
  onPartialReply: params.onPartialReply,
  onAgentEvent: params.onAgentEvent,
});
```

处理的事件包括：

- `message_start` / `message_end` / `message_update`（流式文本/思考）
- `tool_execution_start` / `tool_execution_update` / `tool_execution_end`
- `turn_start` / `turn_end`
- `agent_start` / `agent_end`
- `auto_compaction_start` / `auto_compaction_end`

### 4. 提示

完成设置后，对会话进行提示：

```typescript
await session.prompt(effectivePrompt, { images: imageResult.images });
```

SDK 处理完整的 agent 循环：发送到 LLM、执行工具调用、流式返回响应。

## 工具架构

### 工具流水线

1. **基础工具**：pi 的 `codingTools`（read、bash、edit、write）
2. **自定义替换**：OpenClaw 将 bash 替换为 `exec`/`process`，并为沙箱自定义 read/edit/write
3. **OpenClaw 工具**：消息、浏览器、画布、会话、cron、gateway 等
4. **频道工具**：Discord/Telegram/Slack/WhatsApp 专用动作工具
5. **策略过滤**：根据配置、提供商、agent、群组、沙箱策略过滤工具
6. **Schema 规范化**：为 Gemini/OpenAI 的特殊情况清理 Schema
7. **AbortSignal 包装**：对工具进行包装以尊重 abort 信号

### 工具定义适配器

pi-agent-core 的 `AgentTool` 的 `execute` 签名与 pi-coding-agent 的 `ToolDefinition` 不同。 `pi-tool-definition-adapter.ts` 中的适配器用于桥接这一差异：

```typescript
export function toToolDefinitions(tools: AnyAgentTool[]): ToolDefinition[] {
  return tools.map((tool) => ({
    name: tool.name,
    label: tool.label ?? name,
    description: tool.description ?? "",
    parameters: tool.parameters,
    execute: async (toolCallId, params, onUpdate, _ctx, signal) => {
      // pi-coding-agent signature differs from pi-agent-core
      return await tool.execute(toolCallId, params, signal, onUpdate);
    },
  }));
}
```

### 工具拆分策略

`splitSdkTools()` 通过 `customTools` 传递所有工具：

```typescript
export function splitSdkTools(options: { tools: AnyAgentTool[]; sandboxEnabled: boolean }) {
  return {
    builtInTools: [], // Empty. We override everything
    customTools: toToolDefinitions(options.tools),
  };
}
```

这确保了 OpenClaw 的策略过滤、沙箱集成以及扩展工具集在各个提供方之间保持一致。

## 系统提示词构建

系统提示词在 `buildAgentSystemPrompt()`（`system-prompt.ts`）中构建。 它组装了一个完整的提示词，包含多个部分，包括 Tooling、Tool Call Style、安全防护栏、OpenClaw CLI 参考、Skills、Docs、Workspace、Sandbox、Messaging、Reply Tags、Voice、Silent Replies、Heartbeats、Runtime 元数据，以及在启用时的 Memory 和 Reactions，还有可选的上下文文件和额外的系统提示内容。 对于子代理使用的最小提示词模式，会对各个部分进行裁剪。

在会话创建之后，通过 `applySystemPromptOverrideToSession()` 应用该提示词：

```typescript
const systemPromptOverride = createSystemPromptOverride(appendPrompt);
applySystemPromptOverrideToSession(session, systemPromptOverride);
```

## 会话管理

### 会话文件

会话是具有树结构的 JSONL 文件（通过 id/parentId 进行关联）。 Pi 的 `SessionManager` 负责持久化：

```typescript
const sessionManager = SessionManager.open(params.sessionFile);
```

OpenClaw 使用 `guardSessionManager()` 对其进行包装，以确保工具结果的安全性。

### 会话缓存

`session-manager-cache.ts` caches SessionManager instances to avoid repeated file parsing:

```typescript
await prewarmSessionFile(params.sessionFile);
sessionManager = SessionManager.open(params.sessionFile);
trackSessionManagerAccess(params.sessionFile);
```

### 历史限制

`limitHistoryTurns()` 会根据频道类型（私聊 vs 群聊）裁剪对话历史。

### 压缩（Compaction）

在上下文溢出时会自动触发压缩。 `compactEmbeddedPiSessionDirect()` 处理手动压缩：

```typescript
const compactResult = await compactEmbeddedPiSessionDirect({
  sessionId, sessionFile, provider, model, ...
});
```

## 认证与模型解析

### 认证配置

OpenClaw 维护一个认证配置存储，每个提供方可包含多个 API key：

```typescript
const authStore = ensureAuthProfileStore(agentDir, { allowKeychainPrompt: false });
const profileOrder = resolveAuthProfileOrder({ cfg, store: authStore, provider, preferredProfile });
```

在发生失败时，配置会进行轮换并跟踪冷却时间：

```typescript
await markAuthProfileFailure({ store, profileId, reason, cfg, agentDir });
const rotated = await advanceAuthProfile();
```

### 模型解析

```typescript
import { resolveModel } from "./pi-embedded-runner/model.js";

const { model, error, authStorage, modelRegistry } = resolveModel(
  provider,
  modelId,
  agentDir,
  config,
);

// Uses pi's ModelRegistry and AuthStorage
authStorage.setRuntimeApiKey(model.provider, apiKeyInfo.apiKey);
```

### 故障转移（Failover）

当配置了故障转移时，`FailoverError` 会触发模型回退：

```typescript
if (fallbackConfigured && isFailoverErrorMessage(errorText)) {
  throw new FailoverError(errorText, {
    reason: promptFailoverReason ?? "unknown",
    provider,
    model: modelId,
    profileId,
    status: resolveFailoverStatus(promptFailoverReason),
  });
}
```

## Pi 扩展

OpenClaw 加载自定义的 pi 扩展以实现特定行为：

### 压缩防护

`pi-extensions/compaction-safeguard.ts` 为压缩添加防护栏，包括自适应 token 预算，以及工具失败和文件操作摘要：

```typescript
if (resolveCompactionMode(params.cfg) === "safeguard") {
  setCompactionSafeguardRuntime(params.sessionManager, { maxHistoryShare });
  paths.push(resolvePiExtensionPath("compaction-safeguard"));
}
```

### 上下文裁剪

`pi-extensions/context-pruning.ts` 实现了基于缓存 TTL 的上下文裁剪：

```typescript
if (cfg?.agents?.defaults?.contextPruning?.mode === "cache-ttl") {
  setContextPruningRuntime(params.sessionManager, {
    settings,
    contextWindowTokens,
    isToolPrunable,
    lastCacheTouchAt,
  });
  paths.push(resolvePiExtensionPath("context-pruning"));
}
```

## 流式输出与分块回复

### Block Chunking

`EmbeddedBlockChunker` manages streaming text into discrete reply blocks:

```typescript
const blockChunker = blockChunking ? new EmbeddedBlockChunker(blockChunking) : null;
```

### Thinking/Final Tag Stripping

Streaming output is processed to strip `<think>`/`<thinking>` blocks and extract `<final>` content:

```typescript
const stripBlockTags = (text: string, state: { thinking: boolean; final: boolean }) => {
  // Strip <think>...</think> content
  // If enforceFinalTag, only return <final>...</final> content
};
```

### Reply Directives

Reply directives like `[[media:url]]`, `[[voice]]`, `[[reply:id]]` are parsed and extracted:

```typescript
const { text: cleanedText, mediaUrls, audioAsVoice, replyToId } = consumeReplyDirectives(chunk);
```

## Error Handling

### Error Classification

`pi-embedded-helpers.ts` classifies errors for appropriate handling:

```typescript
isContextOverflowError(errorText)     // Context too large
isCompactionFailureError(errorText)   // Compaction failed
isAuthAssistantError(lastAssistant)   // Auth failure
isRateLimitAssistantError(...)        // Rate limited
isFailoverAssistantError(...)         // Should failover
classifyFailoverReason(errorText)     // "auth" | "rate_limit" | "quota" | "timeout" | ...
```

### Thinking Level Fallback

If a thinking level is unsupported, it falls back:

```typescript
const fallbackThinking = pickFallbackThinkingLevel({
  message: errorText,
  attempted: attemptedThinking,
});
if (fallbackThinking) {
  thinkLevel = fallbackThinking;
  continue;
}
```

## Sandbox Integration

When sandbox mode is enabled, tools and paths are constrained:

```typescript
const sandbox = await resolveSandboxContext({
  config: params.config,
  sessionKey: sandboxSessionKey,
  workspaceDir: resolvedWorkspace,
});

if (sandboxRoot) {
  // Use sandboxed read/edit/write tools
  // Exec runs in container
  // Browser uses bridge URL
}
```

## Provider-Specific Handling

### Anthropic

- Refusal magic string scrubbing
- Turn validation for consecutive roles
- Claude Code parameter compatibility

### Google/Gemini

- Turn ordering fixes (`applyGoogleTurnOrderingFix`)
- Tool schema sanitization (`sanitizeToolsForGoogle`)
- Session history sanitization (`sanitizeSessionHistory`)

### OpenAI

- `apply_patch` tool for Codex models
- Thinking level downgrade handling

## TUI Integration

OpenClaw also has a local TUI mode that uses pi-tui components directly:

```typescript
// src/tui/tui.ts
import { ... } from "@mariozechner/pi-tui";
```

This provides the interactive terminal experience similar to pi's native mode.

## Key Differences from Pi CLI

| Aspect                         | Pi CLI                              | OpenClaw Embedded                                                                                                      |
| ------------------------------ | ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Invocation                     | `pi` command / RPC                  | SDK via `createAgentSession()`                                                                                         |
| Tools                          | Default coding tools                | Custom OpenClaw tool suite                                                                                             |
| System prompt                  | AGENTS.md + prompts | Dynamic per-channel/context                                                                                            |
| Session storage                | `~/.pi/agent/sessions/`             | 1. `~/.openclaw/agents/<agentId>/sessions/`（或 `$OPENCLAW_STATE_DIR/agents/<agentId>/sessions/`） |
| 2. 认证   | 3. 单一凭据      | 4. 多配置文件并支持轮换                                                                                   |
| 5. 扩展   | 6. 从磁盘加载     | 7. 编程方式 + 磁盘路径                                                                                  |
| 8. 事件处理 | 9. TUI 渲染    | 10. 基于回调（onBlockReply 等）                                                                        |

## 11. 未来考虑

12. 潜在需要重构的领域：

1. 13. **工具签名对齐**：当前在 pi-agent-core 与 pi-coding-agent 的签名之间进行适配
2. 14. **会话管理器封装**：`guardSessionManager` 增加了安全性，但也提高了复杂度
3. 15. **扩展加载**：可以更直接地使用 pi 的 `ResourceLoader`
4. 16. **流式处理器复杂性**：`subscribeEmbeddedPiSession` 规模已变得较大
5. 17. **提供方特性差异**：存在许多提供方特定的代码路径，pi 可能可以统一处理

## 18) 测试

19. 覆盖 pi 集成及其扩展的所有现有测试：

- 20. `src/agents/pi-embedded-block-chunker.test.ts`
- 21. `src/agents/pi-embedded-helpers.buildbootstrapcontextfiles.test.ts`
- 22. `src/agents/pi-embedded-helpers.classifyfailoverreason.test.ts`
- 23. `src/agents/pi-embedded-helpers.downgradeopenai-reasoning.test.ts`
- 24. `src/agents/pi-embedded-helpers.formatassistanterrortext.test.ts`
- 25. `src/agents/pi-embedded-helpers.formatrawassistanterrorforui.test.ts`
- 26. `src/agents/pi-embedded-helpers.image-dimension-error.test.ts`
- 27. `src/agents/pi-embedded-helpers.image-size-error.test.ts`
- 28. `src/agents/pi-embedded-helpers.isautherrormessage.test.ts`
- 29. `src/agents/pi-embedded-helpers.isbillingerrormessage.test.ts`
- 30. `src/agents/pi-embedded-helpers.iscloudcodeassistformaterror.test.ts`
- 31. `src/agents/pi-embedded-helpers.iscompactionfailureerror.test.ts`
- 32. `src/agents/pi-embedded-helpers.iscontextoverflowerror.test.ts`
- 33. `src/agents/pi-embedded-helpers.isfailovererrormessage.test.ts`
- 34. `src/agents/pi-embedded-helpers.islikelycontextoverflowerror.test.ts`
- 35. `src/agents/pi-embedded-helpers.ismessagingtoolduplicate.test.ts`
- 36. `src/agents/pi-embedded-helpers.messaging-duplicate.test.ts`
- 37. `src/agents/pi-embedded-helpers.normalizetextforcomparison.test.ts`
- 38. `src/agents/pi-embedded-helpers.resolvebootstrapmaxchars.test.ts`
- 39. `src/agents/pi-embedded-helpers.sanitize-session-messages-images.keeps-tool-call-tool-result-ids-unchanged.test.ts`
- 40. `src/agents/pi-embedded-helpers.sanitize-session-messages-images.removes-empty-assistant-text-blocks-but-preserves.test.ts`
- `src/agents/pi-embedded-helpers.sanitizegoogleturnordering.test.ts`
- 42. `src/agents/pi-embedded-helpers.sanitizesessionmessagesimages-thought-signature-stripping.test.ts`
- 43. `src/agents/pi-embedded-helpers.sanitizetoolcallid.test.ts`
- 44. `src/agents/pi-embedded-helpers.sanitizeuserfacingtext.test.ts`
- 45. `src/agents/pi-embedded-helpers.stripthoughtsignatures.test.ts`
- 46. `src/agents/pi-embedded-helpers.validate-turns.test.ts`
- 47. `src/agents/pi-embedded-runner-extraparams.live.test.ts`（实时）
- `src/agents/pi-embedded-runner-extraparams.test.ts`
- 49. `src/agents/pi-embedded-runner.applygoogleturnorderingfix.test.ts`
- 50. `src/agents/pi-embedded-runner.buildembeddedsandboxinfo.test.ts`
- `src/agents/pi-embedded-runner.get-dm-history-limit-from-session-key.falls-back-provider-default-per-dm-not.test.ts`
- `src/agents/pi-embedded-runner.get-dm-history-limit-from-session-key.returns-undefined-sessionkey-is-undefined.test.ts`
- `src/agents/pi-embedded-runner.google-sanitize-thinking.test.ts`
- `src/agents/pi-embedded-runner.guard.test.ts`
- `src/agents/pi-embedded-runner.limithistoryturns.test.ts`
- `src/agents/pi-embedded-runner.resolvesessionagentids.test.ts`
- `src/agents/pi-embedded-runner.run-embedded-pi-agent.auth-profile-rotation.test.ts`
- `src/agents/pi-embedded-runner.sanitize-session-history.test.ts`
- `src/agents/pi-embedded-runner.splitsdktools.test.ts`
- `src/agents/pi-embedded-runner.test.ts`
- `src/agents/pi-embedded-subscribe.code-span-awareness.test.ts`
- `src/agents/pi-embedded-subscribe.reply-tags.test.ts`
- `src/agents/pi-embedded-subscribe.subscribe-embedded-pi-session.calls-onblockreplyflush-before-tool-execution-start-preserve.test.ts`
- `src/agents/pi-embedded-subscribe.subscribe-embedded-pi-session.does-not-append-text-end-content-is.test.ts`
- `src/agents/pi-embedded-subscribe.subscribe-embedded-pi-session.does-not-call-onblockreplyflush-callback-is-not.test.ts`
- `src/agents/pi-embedded-subscribe.subscribe-embedded-pi-session.does-not-duplicate-text-end-repeats-full.test.ts`
- `src/agents/pi-embedded-subscribe.subscribe-embedded-pi-session.does-not-emit-duplicate-block-replies-text.test.ts`
- `src/agents/pi-embedded-subscribe.subscribe-embedded-pi-session.emits-block-replies-text-end-does-not.test.ts`
- `src/agents/pi-embedded-subscribe.subscribe-embedded-pi-session.emits-reasoning-as-separate-message-enabled.test.ts`
- `src/agents/pi-embedded-subscribe.subscribe-embedded-pi-session.filters-final-suppresses-output-without-start-tag.test.ts`
- `src/agents/pi-embedded-subscribe.subscribe-embedded-pi-session.includes-canvas-action-metadata-tool-summaries.test.ts`
- `src/agents/pi-embedded-subscribe.subscribe-embedded-pi-session.keeps-assistanttexts-final-answer-block-replies-are.test.ts`
- `src/agents/pi-embedded-subscribe.subscribe-embedded-pi-session.keeps-indented-fenced-blocks-intact.test.ts`
- `src/agents/pi-embedded-subscribe.subscribe-embedded-pi-session.reopens-fenced-blocks-splitting-inside-them.test.ts`
- `src/agents/pi-embedded-subscribe.subscribe-embedded-pi-session.splits-long-single-line-fenced-blocks-reopen.test.ts`
- `src/agents/pi-embedded-subscribe.subscribe-embedded-pi-session.streams-soft-chunks-paragraph-preference.test.ts`
- `src/agents/pi-embedded-subscribe.subscribe-embedded-pi-session.subscribeembeddedpisession.test.ts`
- `src/agents/pi-embedded-subscribe.subscribe-embedded-pi-session.suppresses-message-end-block-replies-message-tool.test.ts`
- `src/agents/pi-embedded-subscribe.subscribe-embedded-pi-session.waits-multiple-compaction-retries-before-resolving.test.ts`
- `src/agents/pi-embedded-subscribe.tools.test.ts`
- `src/agents/pi-embedded-utils.test.ts`
- `src/agents/pi-extensions/compaction-safeguard.test.ts`
- `src/agents/pi-extensions/context-pruning.test.ts`
- `src/agents/pi-extensions/context-pruning.test.ts`
- `src/agents/pi-settings.test.ts`
- `src/agents/pi-tools-agent-config.test.ts`
- `src/agents/pi-tools.create-openclaw-coding-tools.adds-claude-style-aliases-schemas-without-dropping-b.test.ts`
- `src/agents/pi-tools.create-openclaw-coding-tools.adds-claude-style-aliases-schemas-without-dropping-d.test.ts`
- `src/agents/pi-tools.create-openclaw-coding-tools.adds-claude-style-aliases-schemas-without-dropping-f.test.ts`
- `src/agents/pi-tools.create-openclaw-coding-tools.adds-claude-style-aliases-schemas-without-dropping.test.ts`
- `src/agents/pi-tools.policy.test.ts`
- `src/agents/pi-tools.safe-bins.test.ts`
- `src/agents/pi-tools.workspace-paths.test.ts`
- `src/agents/pi-tools.workspace-paths.test.ts`
