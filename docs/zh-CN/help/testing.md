---
summary: "27. 测试套件：单元/e2e/在线（live）套件、Docker 运行器，以及每个测试覆盖的内容"
read_when:
  - 28. 在本地或 CI 中运行测试
  - 29. 为模型/提供方缺陷添加回归测试
  - 30. 调试网关 + 代理行为
title: "31. 测试"
---

# 32. 测试

33. OpenClaw 有三个 Vitest 套件（单元/集成、e2e、在线）以及一小组 Docker 运行器。

34. 本文档是“我们如何测试”的指南：

- 35. 每个套件覆盖的内容（以及刻意 _不_ 覆盖的内容）
- 36. 常见工作流要运行的命令（本地、推送前、调试）
- 37. 在线测试如何发现凭据并选择模型/提供方
- 38. 如何为真实世界的模型/提供方问题添加回归测试

## 39. 快速开始

40. 大多数时候：

- 12. 完整门禁（推送前预期执行）：`pnpm build && pnpm check && pnpm test`

42. 当你修改了测试或需要额外信心时：

- 43. 覆盖率门禁：`pnpm test:coverage`
- 44. E2E 套件：`pnpm test:e2e`

45. 调试真实提供方/模型时（需要真实凭据）：

- 46. 在线套件（模型 + 网关工具/镜像探测）：`pnpm test:live`

47. 提示：当你只需要一个失败用例时，优先通过下面描述的 allowlist 环境变量来缩小在线测试范围。

## 48. 测试套件（在哪运行）

49. 将这些套件视为“逐步增加的真实度”（以及逐步增加的不稳定性/成本）：

### 50. 单元 / 集成（默认）

- Command: `pnpm test`
- Config: `vitest.config.ts`
- Files: `src/**/*.test.ts`
- Scope:
  - 13. 纯单元测试
  - In-process integration tests (gateway auth, routing, tooling, parsing, config)
  - Deterministic regressions for known bugs
- Expectations:
  - Runs in CI
  - 14. 不需要真实密钥
  - Should be fast and stable

### 15. E2E（网关冒烟测试）

- Command: `pnpm test:e2e`
- Config: `vitest.e2e.config.ts`
- Files: `src/**/*.e2e.test.ts`
- Scope:
  - Multi-instance gateway end-to-end behavior
  - WebSocket/HTTP surfaces, node pairing, and heavier networking
- Expectations:
  - Runs in CI (when enabled in the pipeline)
  - No real keys required
  - More moving parts than unit tests (can be slower)

### Live (real providers + real models)

- Command: `pnpm test:live`
- Config: `vitest.live.config.ts`
- Files: `src/**/*.live.test.ts`
- Default: **enabled** by `pnpm test:live` (sets `OPENCLAW_LIVE_TEST=1`)
- Scope:
  - “Does this provider/model actually work _today_ with real creds?”
  - Catch provider format changes, tool-calling quirks, auth issues, and rate limit behavior
- Expectations:
  - Not CI-stable by design (real networks, real provider policies, quotas, outages)
  - Costs money / uses rate limits
  - Prefer running narrowed subsets instead of “everything”
  - Live runs will source `~/.profile` to pick up missing API keys
  - Anthropic key rotation: set `OPENCLAW_LIVE_ANTHROPIC_KEYS="sk-...,sk-..."` (or `OPENCLAW_LIVE_ANTHROPIC_KEY=sk-...`) or multiple `ANTHROPIC_API_KEY*` vars; tests will retry on rate limits

## Which suite should I run?

Use this decision table:

- Editing logic/tests: run `pnpm test` (and `pnpm test:coverage` if you changed a lot)
- Touching gateway networking / WS protocol / pairing: add `pnpm test:e2e`
- Debugging “my bot is down” / provider-specific failures / tool calling: run a narrowed `pnpm test:live`

## Live: model smoke (profile keys)

Live tests are split into two layers so we can isolate failures:

- “Direct model” tells us the provider/model can answer at all with the given key.
- “Gateway smoke” tells us the full gateway+agent pipeline works for that model (sessions, history, tools, sandbox policy, etc.).

### Layer 1: Direct model completion (no gateway)

- Test: `src/agents/models.profiles.live.test.ts`
- Goal:
  - Enumerate discovered models
  - Use `getApiKeyForModel` to select models you have creds for
  - 1. 每个模型运行一次小型补全（必要时包含针对性的回归测试）
- 2. 如何启用：
  - 16. `pnpm test:live`（或在直接调用 Vitest 时使用 `OPENCLAW_LIVE_TEST=1`）
- 4. 设置 `OPENCLAW_LIVE_MODELS=modern`（或 `all`，modern 的别名）以实际运行该测试套件；否则将跳过，以便让 `pnpm test:live` 专注于网关冒烟测试
- 5. 如何选择模型：
  - 6. `OPENCLAW_LIVE_MODELS=modern` 运行现代允许列表（Opus/Sonnet/Haiku 4.5、GPT-5.x + Codex、Gemini 3、GLM 4.7、MiniMax M2.1、Grok 4）
  - 7. `OPENCLAW_LIVE_MODELS=all` 是现代允许列表的别名
  - 8. 或 `OPENCLAW_LIVE_MODELS="openai/gpt-5.2,anthropic/claude-opus-4-6,..."`（逗号分隔的允许列表）
- 17. 如何选择提供方：
  - 10. `OPENCLAW_LIVE_PROVIDERS="google,google-antigravity,google-gemini-cli"`（逗号分隔的允许列表）
- 11. 密钥来源：
  - 12. 默认：配置文件存储和环境变量回退
  - 13. 设置 `OPENCLAW_LIVE_REQUIRE_PROFILE_KEYS=1` 以仅强制使用**配置文件存储**
- 14. 为什么要有这个：
  - 15. 将“提供商 API 出问题 / 密钥无效”与“网关代理流水线出问题”区分开来
  - 16. 包含小而独立的回归测试（示例：OpenAI Responses/Codex Responses 的推理回放 + 工具调用流程）

### 17. 第 2 层：网关 + 开发代理冒烟测试（“@openclaw” 实际做了什么）

- 18. 测试：`src/gateway/gateway-models.profiles.live.test.ts`
- 19. 目标：
  - 20. 启动一个进程内网关
  - 21. 创建/修改一个 `agent:dev:*` 会话（每次运行可覆盖模型）
  - 22. 遍历有密钥的模型并断言：
    - 23. “有意义的”响应（不使用工具）
    - 24. 一个真实的工具调用可以正常工作（read 探针）
    - 25. 可选的额外工具探针（exec+read 探针）
    - 26. OpenAI 回归路径（仅工具调用 → 跟进）持续可用
- 27. 探针细节（便于你快速解释失败原因）：
  - 28. `read` 探针：测试在工作区写入一个 nonce 文件，并让代理 `read` 该文件并回显 nonce。
  - 29. `exec+read` 探针：测试让代理通过 `exec` 将 nonce 写入临时文件，然后再 `read` 读取回来。
  - 30. 图像探针：测试附加一个生成的 PNG（猫 + 随机代码），并期望模型返回 `cat <CODE>`。
  - 31. 实现参考：`src/gateway/gateway-models.profiles.live.test.ts` 和 `src/gateway/live-image-probe.ts`。
- 32. 如何启用：
  - 33. `pnpm test:live`（或直接调用 Vitest 时使用 `OPENCLAW_LIVE_TEST=1`）
- 34. 如何选择模型：
  - 35. 默认：现代允许列表（Opus/Sonnet/Haiku 4.5、GPT-5.x + Codex、Gemini 3、GLM 4.7、MiniMax M2.1、Grok 4）
  - 36. `OPENCLAW_LIVE_GATEWAY_MODELS=all` 是现代允许列表的别名
  - 37. 或设置 `OPENCLAW_LIVE_GATEWAY_MODELS="provider/model"`（或逗号列表）以缩小范围
- 38. 如何选择提供商（避免“OpenRouter 全部”）：
  - 39. `OPENCLAW_LIVE_GATEWAY_PROVIDERS="google,google-antigravity,google-gemini-cli,openai,anthropic,zai,minimax"`（逗号分隔的允许列表）
- 40. 在此实时测试中，工具和图像探针始终启用：
  - 41. `read` 探针 + `exec+read` 探针（工具压力测试）
  - 42. 当模型声明支持图像输入时运行图像探针
  - 43. 流程（高层）：
    - 44. 测试生成一个包含“CAT”+ 随机代码的小型 PNG（`src/gateway/live-image-probe.ts`）
    - 45. 通过 `agent` 发送，`attachments: [{ mimeType: "image/png", content: "<base64>" }]`
    - 46. 网关将附件解析为 `images[]`（`src/gateway/server-methods/agent.ts` + `src/gateway/chat-attachments.ts`）
    - 47. 嵌入式代理向模型转发一条多模态用户消息
    - 48. 断言：回复包含 `cat` + 代码（OCR 容错：允许轻微错误）

49. 提示：要查看你在本机上可以测试的内容（以及精确的 `provider/model` ID），运行：

```bash
50. openclaw models list
```

## Live: Anthropic setup-token smoke

- Test: `src/agents/anthropic.setup-token.live.test.ts`
- Goal: verify Claude Code CLI setup-token (or a pasted setup-token profile) can complete an Anthropic prompt.
- Enable:
  - `pnpm test:live` (or `OPENCLAW_LIVE_TEST=1` if invoking Vitest directly)
  - `OPENCLAW_LIVE_SETUP_TOKEN=1`
- Token sources (pick one):
  - Profile: `OPENCLAW_LIVE_SETUP_TOKEN_PROFILE=anthropic:setup-token-test`
  - Raw token: `OPENCLAW_LIVE_SETUP_TOKEN_VALUE=sk-ant-oat01-...`
- Model override (optional):
  - 20. `OPENCLAW_LIVE_SETUP_TOKEN_MODEL=anthropic/claude-opus-4-6`

21. 设置示例：

```bash
openclaw models auth paste-token --provider anthropic --profile-id anthropic:setup-token-test
OPENCLAW_LIVE_SETUP_TOKEN=1 OPENCLAW_LIVE_SETUP_TOKEN_PROFILE=anthropic:setup-token-test pnpm test:live src/agents/anthropic.setup-token.live.test.ts
```

## Live: CLI backend smoke (Claude Code CLI or other local CLIs)

- Test: `src/gateway/gateway-cli-backend.live.test.ts`
- Goal: validate the Gateway + agent pipeline using a local CLI backend, without touching your default config.
- Enable:
  - `pnpm test:live` (or `OPENCLAW_LIVE_TEST=1` if invoking Vitest directly)
  - `OPENCLAW_LIVE_CLI_BACKEND=1`
- Defaults:
  - Model: `claude-cli/claude-sonnet-4-5`
  - Command: `claude`
  - Args: `["-p","--output-format","json","--dangerously-skip-permissions"]`
- Overrides (optional):
  - `OPENCLAW_LIVE_CLI_BACKEND_MODEL="claude-cli/claude-opus-4-6"`
  - `OPENCLAW_LIVE_CLI_BACKEND_MODEL="codex-cli/gpt-5.3-codex"`
  - `OPENCLAW_LIVE_CLI_BACKEND_COMMAND="/full/path/to/claude"`
  - `OPENCLAW_LIVE_CLI_BACKEND_ARGS='["-p","--output-format","json","--permission-mode","bypassPermissions"]'`
  - `OPENCLAW_LIVE_CLI_BACKEND_CLEAR_ENV='["ANTHROPIC_API_KEY","ANTHROPIC_API_KEY_OLD"]'`
  - `OPENCLAW_LIVE_CLI_BACKEND_IMAGE_PROBE=1` to send a real image attachment (paths are injected into the prompt).
  - `OPENCLAW_LIVE_CLI_BACKEND_IMAGE_ARG="--image"` to pass image file paths as CLI args instead of prompt injection.
  - `OPENCLAW_LIVE_CLI_BACKEND_IMAGE_MODE="repeat"` (or `"list"`) to control how image args are passed when `IMAGE_ARG` is set.
  - `OPENCLAW_LIVE_CLI_BACKEND_RESUME_PROBE=1` to send a second turn and validate resume flow.
- `OPENCLAW_LIVE_CLI_BACKEND_DISABLE_MCP_CONFIG=0` to keep Claude Code CLI MCP config enabled (default disables MCP config with a temporary empty file).

Example:

```bash
OPENCLAW_LIVE_CLI_BACKEND=1 \
  OPENCLAW_LIVE_CLI_BACKEND_MODEL="claude-cli/claude-sonnet-4-5" \
  pnpm test:live src/gateway/gateway-cli-backend.live.test.ts
```

### Recommended live recipes

Narrow, explicit allowlists are fastest and least flaky:

- Single model, direct (no gateway):
  - `OPENCLAW_LIVE_MODELS="openai/gpt-5.2" pnpm test:live src/agents/models.profiles.live.test.ts`

- Single model, gateway smoke:
  - `OPENCLAW_LIVE_GATEWAY_MODELS="openai/gpt-5.2" pnpm test:live src/gateway/gateway-models.profiles.live.test.ts`

- Tool calling across several providers:
  - `OPENCLAW_LIVE_GATEWAY_MODELS="openai/gpt-5.2,anthropic/claude-opus-4-6,google/gemini-3-flash-preview,zai/glm-4.7,minimax/minimax-m2.1" pnpm test:live src/gateway/gateway-models.profiles.live.test.ts`

- Google focus (Gemini API key + Antigravity):
  - Gemini (API key): `OPENCLAW_LIVE_GATEWAY_MODELS="google/gemini-3-flash-preview" pnpm test:live src/gateway/gateway-models.profiles.live.test.ts`
  - Antigravity (OAuth): `OPENCLAW_LIVE_GATEWAY_MODELS="google-antigravity/claude-opus-4-6-thinking,google-antigravity/gemini-3-pro-high" pnpm test:live src/gateway/gateway-models.profiles.live.test.ts`

Notes:

- `google/...` uses the Gemini API (API key).
- `google-antigravity/...` uses the Antigravity OAuth bridge (Cloud Code Assist-style agent endpoint).
- `google-gemini-cli/...` 使用你机器上的本地 Gemini CLI（独立的认证 + 工具细节差异）。
- Gemini API vs Gemini CLI：
  - API：OpenClaw 通过 HTTP 调用 Google 托管的 Gemini API（API key / profile 认证）；这通常是大多数用户所说的“Gemini”。
  - CLI：OpenClaw 通过 shell 调用本地 `gemini` 二进制；它有自己的一套认证方式，并且在行为上可能有所不同（流式、工具支持、版本偏差）。

## Live：模型矩阵（我们覆盖的内容）

不存在固定的“CI 模型列表”（live 是可选启用的），但以下是**推荐**在开发机器上、配好 key 后定期覆盖的模型。

### 现代 smoke 集（工具调用 + 图像）

这是我们期望持续保持可用的“常见模型”运行集合：

- OpenAI（非 Codex）：`openai/gpt-5.2`（可选：`openai/gpt-5.1`）
- OpenAI Codex：`openai-codex/gpt-5.3-codex`（可选：`openai-codex/gpt-5.3-codex-codex`）
- Anthropic：`anthropic/claude-opus-4-6`（或 `anthropic/claude-sonnet-4-5`）
- Google（Gemini API）：`google/gemini-3-pro-preview` 和 `google/gemini-3-flash-preview`（避免较旧的 Gemini 2.x 模型）
- Google（Antigravity）：`google-antigravity/claude-opus-4-6-thinking` 和 `google-antigravity/gemini-3-flash`
- Z.AI（GLM）：`zai/glm-4.7`
- MiniMax：`minimax/minimax-m2.1`

运行带工具 + 图像的 gateway smoke：
`OPENCLAW_LIVE_GATEWAY_MODELS="openai/gpt-5.2,openai-codex/gpt-5.3-codex,anthropic/claude-opus-4-6,google/gemini-3-pro-preview,google/gemini-3-flash-preview,google-antigravity/claude-opus-4-6-thinking,google-antigravity/gemini-3-flash,zai/glm-4.7,minimax/minimax-m2.1" pnpm test:live src/gateway/gateway-models.profiles.live.test.ts`

### 基线：工具调用（Read + 可选 Exec）

每个提供方家族至少选一个：

- OpenAI：`openai/gpt-5.2`（或 `openai/gpt-5-mini`）
- Anthropic：`anthropic/claude-opus-4-6`（或 `anthropic/claude-sonnet-4-5`）
- Google：`google/gemini-3-flash-preview`（或 `google/gemini-3-pro-preview`）
- Z.AI（GLM）：`zai/glm-4.7`
- MiniMax：`minimax/minimax-m2.1`

可选的额外覆盖（锦上添花）：

- xAI：`xai/grok-4`（或最新可用版本）
- Mistral：`mistral/`… （选择一个你已启用、支持“工具”的模型）
- Cerebras：`cerebras/`… （如果你有访问权限）
- LM Studio：`lmstudio/`… （本地；工具调用取决于 API 模式）

### Vision：图像发送（附件 → 多模态消息）

在 `OPENCLAW_LIVE_GATEWAY_MODELS` 中至少包含一个支持图像的模型（Claude / Gemini / OpenAI 的视觉版本等）， 以便覆盖图像探测。

### 聚合器 / 备用网关

如果你已启用相关 key，我们也支持通过以下方式测试：

- OpenRouter：`openrouter/...`（数百个模型；使用 `openclaw models scan` 查找支持工具 + 图像的候选）
- OpenCode Zen：`opencode/...`（通过 `OPENCODE_API_KEY` / `OPENCODE_ZEN_API_KEY` 认证）

你还可以在 live 矩阵中包含更多提供方（如果你有凭据/配置）：

- 内置：`openai`、`openai-codex`、`anthropic`、`google`、`google-vertex`、`google-antigravity`、`google-gemini-cli`、`zai`、`openrouter`、`opencode`、`xai`、`groq`、`cerebras`、`mistral`、`github-copilot`
- 通过 `models.providers`（自定义端点）：`minimax`（云/API），以及任何 OpenAI / Anthropic 兼容的代理（LM Studio、vLLM、LiteLLM 等）

提示：不要试图在文档中硬编码“所有模型”。 权威列表是你机器上 `discoverModels(...)` 返回的内容 + 当前可用的所有 key。

## 凭据（永远不要提交）

Live 测试发现凭据的方式与 CLI 完全一致。 实际影响：

- 如果 CLI 能工作，live 测试应该能找到相同的 key。

- 如果某个 live 测试提示“no creds”，请用与调试 `openclaw models list` / 模型选择相同的方法排查。

- Profile 存储：`~/.openclaw/credentials/`（首选；测试中“profile keys”的含义）

- 配置：`~/.openclaw/openclaw.json`（或 `OPENCLAW_CONFIG_PATH`）

If you want to rely on env keys (e.g. exported in your `~/.profile`), run local tests after `source ~/.profile`, or use the Docker runners below (they can mount `~/.profile` into the container).

## Deepgram live (audio transcription)

- Test: `src/media-understanding/providers/deepgram/audio.live.test.ts`
- Enable: `DEEPGRAM_API_KEY=... DEEPGRAM_LIVE_TEST=1 pnpm test:live src/media-understanding/providers/deepgram/audio.live.test.ts`

## Docker runners (optional “works in Linux” checks)

These run `pnpm test:live` inside the repo Docker image, mounting your local config dir and workspace (and sourcing `~/.profile` if mounted):

- Direct models: `pnpm test:docker:live-models` (script: `scripts/test-live-models-docker.sh`)
- Gateway + dev agent: `pnpm test:docker:live-gateway` (script: `scripts/test-live-gateway-models-docker.sh`)
- Onboarding wizard (TTY, full scaffolding): `pnpm test:docker:onboard` (script: `scripts/e2e/onboard-docker.sh`)
- Gateway networking (two containers, WS auth + health): `pnpm test:docker:gateway-network` (script: `scripts/e2e/gateway-network-docker.sh`)
- Plugins (custom extension load + registry smoke): `pnpm test:docker:plugins` (script: `scripts/e2e/plugins-docker.sh`)

Useful env vars:

- `OPENCLAW_CONFIG_DIR=...` (default: `~/.openclaw`) mounted to `/home/node/.openclaw`
- `OPENCLAW_WORKSPACE_DIR=...` (default: `~/.openclaw/workspace`) mounted to `/home/node/.openclaw/workspace`
- `OPENCLAW_PROFILE_FILE=...` (default: `~/.profile`) mounted to `/home/node/.profile` and sourced before running tests
- `OPENCLAW_LIVE_GATEWAY_MODELS=...` / `OPENCLAW_LIVE_MODELS=...` to narrow the run
- `OPENCLAW_LIVE_REQUIRE_PROFILE_KEYS=1` to ensure creds come from the profile store (not env)

## Docs sanity

Run docs checks after doc edits: `pnpm docs:list`.

## Offline regression (CI-safe)

These are “real pipeline” regressions without real providers:

- Gateway tool calling (mock OpenAI, real gateway + agent loop): `src/gateway/gateway.tool-calling.mock-openai.test.ts`
- Gateway wizard (WS `wizard.start`/`wizard.next`, writes config + auth enforced): `src/gateway/gateway.wizard.e2e.test.ts`

## Agent reliability evals (skills)

We already have a few CI-safe tests that behave like “agent reliability evals”:

- Mock tool-calling through the real gateway + agent loop (`src/gateway/gateway.tool-calling.mock-openai.test.ts`).
- End-to-end wizard flows that validate session wiring and config effects (`src/gateway/gateway.wizard.e2e.test.ts`).

What’s still missing for skills (see [Skills](/tools/skills)):

- **Decisioning:** when skills are listed in the prompt, does the agent pick the right skill (or avoid irrelevant ones)?
- **Compliance:** does the agent read `SKILL.md` before use and follow required steps/args?
- **Workflow contracts:** multi-turn scenarios that assert tool order, session history carryover, and sandbox boundaries.

Future evals should stay deterministic first:

- A scenario runner using mock providers to assert tool calls + order, skill file reads, and session wiring.
- A small suite of skill-focused scenarios (use vs avoid, gating, prompt injection).
- Optional live evals (opt-in, env-gated) only after the CI-safe suite is in place.

## Adding regressions (guidance)

When you fix a provider/model issue discovered in live:

- Add a CI-safe regression if possible (mock/stub provider, or capture the exact request-shape transformation)
- If it’s inherently live-only (rate limits, auth policies), keep the live test narrow and opt-in via env vars
- Prefer targeting the smallest layer that catches the bug:
  - provider request conversion/replay bug → direct models test
  - gateway session/history/tool pipeline bug → gateway live smoke or CI-safe gateway mock test
