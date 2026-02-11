---
summary: "5. 计划：一个干净的插件 SDK + 运行时，用于所有消息连接器"
read_when:
  - 6. 定义或重构插件架构
  - 7. 将频道连接器迁移到插件 SDK / 运行时
title: "8. 插件 SDK 重构"
---

# 9. 插件 SDK + 运行时重构计划

10. 目标：每个消息连接器都是一个插件（内置或外部），使用一个稳定的 API。
11. 插件不得直接从 `src/**` 导入。 12. 所有依赖都通过 SDK 或运行时。

## 13. 为什么是现在

- 14. 当前连接器混合了多种模式：直接核心导入、仅 dist 的桥接，以及自定义辅助工具。
- 15. 这使升级变得脆弱，并阻碍了干净的外部插件接口。

## 16. 目标架构（两层）

### 17. 1. 插件 SDK（编译期、稳定、可发布）

18. 范围：类型、辅助工具和配置工具。 19. 无运行时状态，无副作用。

20. 内容（示例）：

- 21. 类型：`ChannelPlugin`、适配器、`ChannelMeta`、`ChannelCapabilities`、`ChannelDirectoryEntry`。
- 22. 配置辅助工具：`buildChannelConfigSchema`、`setAccountEnabledInConfigSection`、`deleteAccountFromConfigSection`,
      `applyAccountNameToChannelSection`。
- 23. 配对辅助工具：`PAIRING_APPROVED_MESSAGE`、`formatPairingApproveHint`。
- 24. 引导辅助工具：`promptChannelAccessConfig`、`addWildcardAllowFrom`、引导相关类型。
- 25. 工具参数辅助：`createActionGate`、`readStringParam`、`readNumberParam`、`readReactionParams`、`jsonResult`。
- 26. 文档链接辅助：`formatDocsLink`。

27. 交付：

- 28. 以 `openclaw/plugin-sdk` 发布（或从 core 中以 `openclaw/plugin-sdk` 导出）。
- 29. 采用 Semver，并提供明确的稳定性保证。

### 30. 2. 插件运行时（执行层，注入式）

31. 范围：所有涉及核心运行时行为的内容。
32. 通过 `OpenClawPluginApi.runtime` 访问，使插件永远不导入 `src/**`。

33. 建议的接口（最小但完整）：

```ts
export type PluginRuntime = {
  channel: {
    text: {
      chunkMarkdownText(text: string, limit: number): string[];
      resolveTextChunkLimit(cfg: OpenClawConfig, channel: string, accountId?: string): number;
      hasControlCommand(text: string, cfg: OpenClawConfig): boolean;
    };
    reply: {
      dispatchReplyWithBufferedBlockDispatcher(params: {
        ctx: unknown;
        cfg: unknown;
        dispatcherOptions: {
          deliver: (payload: {
            text?: string;
            mediaUrls?: string[];
            mediaUrl?: string;
          }) => void | Promise<void>;
          onError?: (err: unknown, info: { kind: string }) => void;
        };
      }): Promise<void>;
      createReplyDispatcherWithTyping?: unknown; // adapter for Teams-style flows
    };
    routing: {
      resolveAgentRoute(params: {
        cfg: unknown;
        channel: string;
        accountId: string;
        peer: { kind: RoutePeerKind; id: string };
      }): { sessionKey: string; accountId: string };
    };
    pairing: {
      buildPairingReply(params: { channel: string; idLine: string; code: string }): string;
      readAllowFromStore(channel: string): Promise<string[]>;
      upsertPairingRequest(params: {
        channel: string;
        id: string;
        meta?: { name?: string };
      }): Promise<{ code: string; created: boolean }>;
    };
    media: {
      fetchRemoteMedia(params: { url: string }): Promise<{ buffer: Buffer; contentType?: string }>;
      saveMediaBuffer(
        buffer: Uint8Array,
        contentType: string | undefined,
        direction: "inbound" | "outbound",
        maxBytes: number,
      ): Promise<{ path: string; contentType?: string }>;
    };
    mentions: {
      buildMentionRegexes(cfg: OpenClawConfig, agentId?: string): RegExp[];
      matchesMentionPatterns(text: string, regexes: RegExp[]): boolean;
    };
    groups: {
      resolveGroupPolicy(
        cfg: OpenClawConfig,
        channel: string,
        accountId: string,
        groupId: string,
      ): {
        allowlistEnabled: boolean;
        allowed: boolean;
        groupConfig?: unknown;
        defaultConfig?: unknown;
      };
      resolveRequireMention(
        cfg: OpenClawConfig,
        channel: string,
        accountId: string,
        groupId: string,
        override?: boolean,
      ): boolean;
    };
    debounce: {
      createInboundDebouncer<T>(opts: {
        debounceMs: number;
        buildKey: (v: T) => string | null;
        shouldDebounce: (v: T) => boolean;
        onFlush: (entries: T[]) => Promise<void>;
        onError?: (err: unknown) => void;
      }): { push: (v: T) => void; flush: () => Promise<void> };
      resolveInboundDebounceMs(cfg: OpenClawConfig, channel: string): number;
    };
    commands: {
      resolveCommandAuthorizedFromAuthorizers(params: {
        useAccessGroups: boolean;
        authorizers: Array<{ configured: boolean; allowed: boolean }>;
      }): boolean;
    };
  };
  logging: {
    shouldLogVerbose(): boolean;
    getChildLogger(name: string): PluginLogger;
  };
  state: {
    resolveStateDir(cfg: OpenClawConfig): string;
  };
};
```

34. 说明：

- 35. 运行时是访问核心行为的唯一方式。
- 36. SDK 被有意设计得小且稳定。
- 37. 每个运行时方法都映射到现有的核心实现（无重复）。

## 38. 迁移计划（分阶段，安全）

### 39. 第 0 阶段：脚手架

- 40. 引入 `openclaw/plugin-sdk`。
- 41. 在 `OpenClawPluginApi` 中添加 `api.runtime`，提供上述接口。
- 42. 在过渡期内保留现有导入（弃用警告）。

### 43. 第 1 阶段：桥接清理（低风险）

- 44. 用 `api.runtime` 替换每个扩展的 `core-bridge.ts`。
- 45. 优先迁移 BlueBubbles、Zalo、Zalo Personal（已经很接近）。
- 46. 移除重复的桥接代码。

### 47. 第 2 阶段：轻度直接导入的插件

- 48. 将 Matrix 迁移到 SDK + 运行时。
- 49. 验证引导流程、目录、群组提及逻辑。

### 50. 第 3 阶段：重度直接导入的插件

- 1. 迁移 MS Teams（最大的运行时辅助集合）。
- 2. 确保回复/正在输入语义与当前行为一致。

### 3. 第 4 阶段：iMessage 插件化

- 4. 将 iMessage 移入 `extensions/imessage`。
- 5. 用 `api.runtime` 替换直接的 core 调用。
- 6. 保持配置键、CLI 行为和文档不变。

### 7. 第 5 阶段：强制执行

- 8. 添加 lint 规则 / CI 检查：禁止从 `src/**` 导入 `extensions/**`。
- 9. 添加插件 SDK/版本兼容性检查（runtime + SDK semver）。

## 10. 兼容性与版本控制

- 11. SDK：遵循 semver，已发布，并记录变更。
- 12. Runtime：按 core 发布版本进行版本化。 Add `api.runtime.version`.
- Plugins declare a required runtime range (e.g., `openclawRuntime: ">=2026.2.0"`).

## Testing strategy

- 16. 适配器级单元测试（使用真实 core 实现来执行 runtime 函数）。
- Golden tests per plugin: ensure no behavior drift (routing, pairing, allowlist, mention gating).
- A single end-to-end plugin sample used in CI (install + run + smoke).

## Open questions

- 20. SDK 类型应托管在哪里：独立包还是 core 导出？
- 21. Runtime 类型分发：在 SDK 中（仅类型）还是在 core 中？
- 22. 如何为内置插件与外部插件暴露文档链接？
- 23. 过渡期间是否允许仓库内插件有限度地直接导入 core？

## 24. 成功标准

- 25. 所有渠道连接器都是使用 SDK + runtime 的插件。
- 26. 不允许从 `src/**` 导入 `extensions/**`。
- 27. 新的连接器模板仅依赖 SDK + runtime。
- 28. 外部插件可以在无需访问 core 源码的情况下开发和更新。

29. 相关文档：[Plugins](/tools/plugin)、[Channels](/channels/index)、[Configuration](/gateway/configuration)。
