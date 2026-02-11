---
summary: "Run multiple OpenClaw Gateways on one host (isolation, ports, and profiles)"
read_when:
  - Running more than one Gateway on the same machine
  - 每个 Gateway 需要隔离的配置/状态/端口
title: "多个 Gateway"
---

# Multiple Gateways (same host)

大多数部署应使用一个 Gateway，因为单个 Gateway 可以处理多个消息连接和代理。 If you need stronger isolation or redundancy (e.g., a rescue bot), run separate Gateways with isolated profiles/ports.

## 隔离清单（必需）

- `OPENCLAW_CONFIG_PATH` — 每实例配置文件
- `OPENCLAW_STATE_DIR` — 每实例会话、凭据、缓存
- `agents.defaults.workspace` — 每实例工作区根目录
- `gateway.port`（或 `--port`）— 每实例唯一
- 派生端口（浏览器/canvas）不得重叠

如果这些被共享，将会发生配置竞争和端口冲突。

## 推荐：配置档（`--profile`）

配置档会自动限定 `OPENCLAW_STATE_DIR` + `OPENCLAW_CONFIG_PATH`，并为服务名称添加后缀。

```bash
# main
openclaw --profile main setup
openclaw --profile main gateway --port 18789

# rescue
openclaw --profile rescue setup
openclaw --profile rescue gateway --port 19001
```

按配置档的服务：

```bash
openclaw --profile main gateway install
openclaw --profile rescue gateway install
```

## 救援机器人指南

在同一主机上运行第二个 Gateway，并拥有其独立的：

- 配置档/配置
- 状态目录
- 工作区
- 基础端口（以及派生端口）

这样可以将救援机器人与主机器人隔离，当主机器人宕机时可进行调试或应用配置更改。

端口间隔：基础端口之间至少留出 20 个端口，以确保派生的浏览器/canvas/CDP 端口不会发生冲突。

### 如何安装（救援机器人）

```bash
# 主机器人（现有或全新，不带 --profile 参数）
# 运行在端口 18789 + Chrome CDC/Canvas/... 端口
openclaw onboard
openclaw gateway install

# 救援机器人（隔离的配置档 + 端口）
openclaw --profile rescue onboard
# 说明：
# - 默认情况下，工作区名称会追加 -rescue 后缀
# - 端口应至少为 18789 + 20 个端口，
#   更好是选择完全不同的基础端口，例如 19789，
# - 其余入门流程与正常情况相同

# 安装服务（如果在入门过程中未自动完成）
openclaw --profile rescue gateway install
```

## 端口映射（派生）

基础端口 = `gateway.port`（或 `OPENCLAW_GATEWAY_PORT` / `--port`）。

- 浏览器控制服务端口 = 基础端口 + 2（仅回环）
- `canvasHost.port = base + 4`
- 浏览器配置文件 CDP 端口会从 `browser.controlPort + 9 .. + 108` 自动分配

If you override any of these in config or env, you must keep them unique per instance.

## Browser/CDP notes (common footgun)

- Do **not** pin `browser.cdpUrl` to the same values on multiple instances.
- Each instance needs its own browser control port and CDP range (derived from its gateway port).
- If you need explicit CDP ports, set `browser.profiles.<name>.cdpPort` per instance.
- Remote Chrome: use `browser.profiles.<name>.cdpUrl` (per profile, per instance).

## Manual env example

```bash
OPENCLAW_CONFIG_PATH=~/.openclaw/main.json \
OPENCLAW_STATE_DIR=~/.openclaw-main \
openclaw gateway --port 18789

OPENCLAW_CONFIG_PATH=~/.openclaw/rescue.json \
OPENCLAW_STATE_DIR=~/.openclaw-rescue \
openclaw gateway --port 19001
```

## 快速检查

```bash
openclaw --profile main status
openclaw --profile rescue status
openclaw --profile rescue browser status
```
