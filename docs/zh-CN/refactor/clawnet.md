---
summary: "Clawnet refactor: unify network protocol, roles, auth, approvals, identity"
read_when:
  - Planning a unified network protocol for nodes + operator clients
  - Reworking approvals, pairing, TLS, and presence across devices
title: "Clawnet Refactor"
---

# Clawnet refactor (protocol + auth unification)

## Hi

Hi Peter — great direction; this unlocks simpler UX + stronger security.

## Purpose

Single, rigorous document for:

- Current state: protocols, flows, trust boundaries.
- Pain points: approvals, multi‑hop routing, UI duplication.
- Proposed new state: one protocol, scoped roles, unified auth/pairing, TLS pinning.
- Identity model: stable IDs + cute slugs.
- Migration plan, risks, open questions.

## Goals (from discussion)

- One protocol for all clients (mac app, CLI, iOS, Android, headless node).
- Every network participant authenticated + paired.
- Role clarity: nodes vs operators.
- Central approvals routed to where the user is.
- TLS encryption + optional pinning for all remote traffic.
- 1. 最小化代码重复。
- 2. 单台机器只应出现一次（无 UI/节点重复条目）。

## 3. 非目标（明确）

- 4. 移除能力隔离（仍需要最小权限）。
- 5. 在不进行作用域检查的情况下暴露完整的网关控制平面。
- 让鉴权依赖人工标签（slug 仍非安全项）。

---

# 7. 当前状态（as‑is）

## 8. 两种协议

### 9. 1. 网关 WebSocket（控制平面）

- 完整的 API 能力面：配置、通道、模型、会话、代理运行、日志、节点等。
- 11. 默认绑定：回环。 12. 通过 SSH/Tailscale 进行远程访问。
- 鉴权：通过 `connect` 使用令牌/密码。
- 14. 无 TLS 固定（依赖回环/隧道）。
- 15. 代码：
  - 16. `src/gateway/server/ws-connection/message-handler.ts`
  - 17. `src/gateway/client.ts`
  - 18. `docs/gateway/protocol.md`

### 19. 2. Bridge（节点传输）

- 20. 狭窄的允许列表面，节点身份 + 配对。
- 21. 基于 TCP 的 JSONL；可选 TLS + 证书指纹固定。
- 22. TLS 在发现 TXT 中通告指纹。
- 23. 代码：
  - 24. `src/infra/bridge/server/connection.ts`
  - 25. `src/gateway/server-bridge.ts`
  - 26. `src/node-host/bridge-client.ts`
  - 27. `docs/gateway/bridge-protocol.md`

## 28. 当前的控制平面客户端

- 29. CLI → 通过 `callGateway` 连接网关 WS（`src/gateway/call.ts`）。
- 30. macOS 应用 UI → 网关 WS（`GatewayConnection`）。
- 31. Web 控制 UI → 网关 WS。
- 32. ACP → 网关 WS。
- 33. 浏览器控制使用其自己的 HTTP 控制服务器。

## 34. 当前的节点

- 35. macOS 应用在节点模式下连接到网关 bridge（`MacNodeBridgeSession`）。
- 36. iOS/Android 应用连接到网关 bridge。
- 37. 配对 + 每节点令牌存储在网关上。

## 38. 当前审批流程（exec）

- 39. 代理通过网关使用 `system.run`。
- 40. 网关通过 bridge 调用节点。
- 41. 节点运行时决定是否批准。
- 42. 当节点 == mac 应用时，由 mac 应用显示 UI 提示。
- 43. 节点向网关返回 `invoke-res`。
- 44. 多跳，UI 绑定到节点主机。

## 45. 当前的在线状态 + 身份

- 46. 来自 WS 客户端的网关在线状态条目。
- 47. 来自 bridge 的节点在线状态条目。
- 48. mac 应用可能为同一台机器显示两个条目（UI + 节点）。
- 49. 节点身份存储在配对存储中；UI 身份是独立的。

---

# 50. 问题 / 痛点

- Two protocol stacks to maintain (WS + Bridge).
- Approvals on remote nodes: prompt appears on node host, not where user is.
- TLS pinning only exists for bridge; WS depends on SSH/Tailscale.
- Identity duplication: same machine shows as multiple instances.
- Ambiguous roles: UI + node + CLI capabilities not clearly separated.

---

# 提议的新状态（Clawnet）

## One protocol, two roles

Single WS protocol with role + scope.

- **Role: node** (capability host)
- **Role: operator** (control plane)
- Optional **scope** for operator:
  - `operator.read` (status + viewing)
  - `operator.write`（代理运行、发送）
  - `operator.admin`（配置、通道、模型）

### Role behaviors

**Node**

- Can register capabilities (`caps`, `commands`, permissions).
- 可接收 `invoke` 命令（`system.run`、`camera.*`、`canvas.*`、`screen.record` 等）。
- Can send events: `voice.transcript`, `agent.request`, `chat.subscribe`.
- Cannot call config/models/channels/sessions/agent control plane APIs.

**Operator**

- Full control plane API, gated by scope.
- Receives all approvals.
- Does not directly execute OS actions; routes to nodes.

### Key rule

Role is per‑connection, not per device. 一个设备可以分别打开这两种角色。

---

# Unified authentication + pairing

## Client identity

Every client provides:

- `deviceId` (stable, derived from device key).
- `displayName`（人类可读名称）。
- `role` + `scope` + `caps` + `commands`.

## Pairing flow (unified)

- Client connects unauthenticated.
- Gateway creates a **pairing request** for that `deviceId`.
- Operator receives prompt; approves/denies.
- Gateway issues credentials bound to:
  - device public key
  - role(s)
  - 作用域
  - capabilities/commands
- Client persists token, reconnects authenticated.

## Device‑bound auth (avoid bearer token replay)

Preferred: device keypairs.

- Device generates keypair once.
- `deviceId = fingerprint(publicKey)`.
- 网关发送随机数；设备签名；网关验证。
- Tokens are issued to a public key (proof‑of‑possession), not a string.

Alternatives:

- mTLS (client certs): strongest, more ops complexity.
- Short‑lived bearer tokens only as a temporary phase (rotate + revoke early).

## Silent approval (SSH heuristic)

Define it precisely to avoid a weak link. Prefer one:

- **Local‑only**: auto‑pair when client connects via loopback/Unix socket.
- **Challenge via SSH**: gateway issues nonce; client proves SSH by fetching it.
- **Physical presence window**: after a local approval on gateway host UI, allow auto‑pair for a short window (e.g. 10 minutes).

Always log + record auto‑approvals.

---

# TLS everywhere (dev + prod)

## Reuse existing bridge TLS

Use current TLS runtime + fingerprint pinning:

- `src/infra/bridge/server/tls.ts`
- fingerprint verification logic in `src/node-host/bridge-client.ts`

## Apply to WS

- WS server supports TLS with same cert/key + fingerprint.
- WS clients can pin fingerprint (optional).
- Discovery advertises TLS + fingerprint for all endpoints.
  - Discovery is locator hints only; never a trust anchor.

## Why

- Reduce reliance on SSH/Tailscale for confidentiality.
- Make remote mobile connections safe by default.

---

# 审批重设计（集中式）

## Current

Approval happens on node host (mac app node runtime). Prompt appears where node runs.

## Proposed

Approval is **gateway‑hosted**, UI delivered to operator clients.

### New flow

1. Gateway receives `system.run` intent (agent).
2. Gateway creates approval record: `approval.requested`.
3. Operator UI(s) show prompt.
4. Approval decision sent to gateway: `approval.resolve`.
5. Gateway invokes node command if approved.
6. Node executes, returns `invoke-res`.

### Approval semantics (hardening)

- Broadcast to all operators; only the active UI shows a modal (others get a toast).
- First resolution wins; gateway rejects subsequent resolves as already settled.
- Default timeout: deny after N seconds (e.g. 60s), log reason.
- Resolution requires `operator.approvals` scope.

## Benefits

- Prompt appears where user is (mac/phone).
- Consistent approvals for remote nodes.
- Node runtime stays headless; no UI dependency.

---

# Role clarity examples

## iPhone app

- **Node role** for: mic, camera, voice chat, location, push‑to‑talk.
- Optional **operator.read** for status and chat view.
- Optional **operator.write/admin** only when explicitly enabled.

## macOS app

- Operator role by default (control UI).
- Node role when “Mac node” enabled (system.run, screen, camera).
- Same deviceId for both connections → merged UI entry.

## CLI

- Operator role always.
- Scope derived by subcommand:
  - `status`, `logs` → read
  - `agent`, `message` → write
  - `config`, `channels` → admin
  - approvals + pairing → `operator.approvals` / `operator.pairing`

---

# Identity + slugs

## Stable ID

鉴权所必需；永不更改。
Preferred:

- Keypair fingerprint (public key hash).

## Cute slug (lobster‑themed)

Human label only.

- Example: `scarlet-claw`, `saltwave`, `mantis-pinch`.
- Stored in gateway registry, editable.
- 冲突处理：`-2`、`-3`。

## UI grouping

Same `deviceId` across roles → single “Instance” row:

- Badge: `operator`, `node`.
- Shows capabilities + last seen.

---

# Migration strategy

## Phase 0: Document + align

- Publish this doc.
- Inventory all protocol calls + approval flows.

## Phase 1: Add roles/scopes to WS

- Extend `connect` params with `role`, `scope`, `deviceId`.
- Add allowlist gating for node role.

## Phase 2: Bridge compatibility

- Keep bridge running.
- Add WS node support in parallel.
- Gate features behind config flag.

## Phase 3: Central approvals

- Add approval request + resolve events in WS.
- Update mac app UI to prompt + respond.
- Node runtime stops prompting UI.

## Phase 4: TLS unification

- Add TLS config for WS using bridge TLS runtime.
- Add pinning to clients.

## Phase 5: Deprecate bridge

- Migrate iOS/Android/mac node to WS.
- Keep bridge as fallback; remove once stable.

## Phase 6: Device‑bound auth

- Require key‑based identity for all non‑local connections.
- Add revocation + rotation UI.

---

# Security notes

- Role/allowlist enforced at gateway boundary.
- 1. 没有操作员作用域，任何客户端都无法获得“完整”的 API。
- 2. 所有连接都需要配对。
- TLS + 证书固定可降低移动端的中间人攻击风险。
- 4. SSH 静默批准只是便利功能；仍会被记录并且可撤销。
- 5. 发现机制绝不是信任锚点。
- 6. 能力声明会按平台/类型与服务器允许列表进行校验。

# 7. 流式传输 + 大负载（节点媒体）

8. WS 控制平面适合小消息，但节点还会处理：

- 9. 摄像头片段
- 10. 屏幕录制
- 11. 音频流

选项：

1. 13. WS 二进制帧 + 分块 + 背压规则。
2. 14. 独立的流式端点（仍使用 TLS + 认证）。
3. 15. 对于媒体密集型命令，保留桥接更久，最后再迁移。

16) 在实现前选定一种以避免漂移。

# 17. 能力 + 命令策略

- 18. 节点上报的能力/命令被视为**声明**。
- 19. 网关按平台强制执行允许列表。
- 20. 任何新命令都需要操作员批准或显式修改允许列表。
- 21. 以时间戳审计变更。

# 22. 审计 + 速率限制

- 23. 记录：配对请求、批准/拒绝、令牌签发/轮换/吊销。
- 24. 对配对刷请求和批准提示进行速率限制。

# 25. 协议规范

- 26. 明确的协议版本 + 错误码。
- 27. 重连规则 + 心跳策略。
- 28. 在线状态 TTL 与最后一次可见语义。

---

# 29. 未决问题

1. 30. 单一设备同时运行两种角色：令牌模型
   - 31. 建议为每个角色使用独立令牌（节点 vs 操作员）。
   - 32. 相同 deviceId；不同作用域；更清晰的吊销。

2. 33. 操作员作用域粒度
   - 34. 读/写/管理员 + 批准 + 配对（最小可行）。
   - 35. 之后再考虑按功能划分的作用域。

3. 36. 令牌轮换 + 吊销 UX
   - 37. 角色变更时自动轮换。
   - 38. 提供按 deviceId + 角色进行吊销的 UI。

4. 39. 发现
   - 40. 扩展当前的 Bonjour TXT，包含 WS TLS 指纹 + 角色提示。
   - 41. 仅将其视为定位提示。

5. 42. 跨网络批准
   - 43. 向所有操作员客户端广播；活跃 UI 显示模态框。
   - 44. 首个响应生效；网关保证原子性。

---

# 45. 总结（TL;DR）

- 46. 现状：WS 控制平面 + Bridge 节点传输。
- 47. 痛点：批准流程 + 重复 + 两套技术栈。
- 48. 提案：一个 WS 协议，具备明确的角色 + 作用域、统一的配对 + TLS 固定、由网关托管的批准、稳定的设备 ID + 可爱的短名。
- 49. 结果：更简单的 UX、更强的安全性、更少的重复、更好的移动端路由。
