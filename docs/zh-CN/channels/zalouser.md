---
summary: "通过 zca-cli（二维码登录）支持 Zalo 个人账号，其功能与配置说明。"
read_when:
  - 为 OpenClaw 设置 Zalo Personal
  - 调试 Zalo Personal 登录或消息流
title: "Zalo Personal"
---

# Zalo Personal（非官方）

状态：实验性。 此集成通过 `zca-cli` 自动化 **Zalo 个人账号**。

> 38. **警告：** 这是一个非官方集成，可能导致账号被暂停/封禁。 使用风险自负。

## 39. 需要插件

Zalo Personal 以插件形式提供，未包含在核心安装中。

- 通过 CLI 安装：`openclaw plugins install @openclaw/zalouser`
- 或从源码检出安装：`openclaw plugins install ./extensions/zalouser`
- 详情：[Plugins](/tools/plugin)

## 40. 前置条件：zca-cli

网关机器必须在 `PATH` 中可用 `zca` 二进制文件。

- 验证：`zca --version`
- 41. 如果缺失，请安装 zca-cli（参见 `extensions/zalouser/README.md` 或上游 zca-cli 文档）。

## 快速设置（新手）

1. 安装插件（见上文）。
2. 登录（QR，在 Gateway 机器上）：
   - `openclaw channels login --channel zalouser`
   - 使用 Zalo 手机应用扫描终端中的二维码。
3. 启用该通道：

```json5
{
  channels: {
    zalouser: {
      enabled: true,
      dmPolicy: "pairing",
    },
  },
}
```

4. 重启 Gateway（或完成引导流程）。
5. DM 访问默认为配对；首次联系时批准配对码。

## 42) 它是什么

- 使用 `zca listen` 接收入站消息。
- 使用 `zca msg ...` 发送回复（文本/媒体/链接）。
- 为 Zalo Bot API 不可用的“个人账号”使用场景而设计。

## 命名

通道 id 为 `zalouser`，以明确这是在自动化一个 **个人 Zalo 用户账号**（非官方）。 我们保留 `zalo` 以备将来可能的官方 Zalo API 集成。

## 查找 ID（目录）

使用目录 CLI 发现联系人/群组及其 ID：

```bash
openclaw directory self --channel zalouser
openclaw directory peers list --channel zalouser --query "name"
openclaw directory groups list --channel zalouser --query "work"
```

## 限制

- 出站文本会被分块为约 2000 个字符（Zalo 客户端限制）。
- 默认阻止流式传输。

## 访问控制（DM）

`channels.zalouser.dmPolicy` 支持：`pairing | allowlist | open | disabled`（默认：`pairing`）。
`channels.zalouser.allowFrom` 接受用户 ID 或名称。 向导在可用时会通过 `zca friend find` 将名称解析为 ID。

43. 批准方式：

- `openclaw pairing list zalouser`
- `openclaw pairing approve zalouser <code>`

## 群组访问（可选）

- 默认：`channels.zalouser.groupPolicy = "open"`（允许群组）。 在未设置时，使用 `channels.defaults.groupPolicy` 覆盖默认值。
- 使用以下方式限制为允许列表：
  - `channels.zalouser.groupPolicy = "allowlist"`
  - `channels.zalouser.groups`（键为群组 ID 或名称）
- 阻止所有群组：`channels.zalouser.groupPolicy = "disabled"`。
- 44. 配置向导可以提示设置群组允许列表。
- 启动时，OpenClaw 会将允许列表中的群组/用户名称解析为 ID 并记录映射；无法解析的条目将按原样保留。

示例：

```json5
{
  channels: {
    zalouser: {
      groupPolicy: "allowlist",
      groups: {
        "123456789": { allow: true },
        "Work Chat": { allow: true },
      },
    },
  },
}
```

## 多账号

账号映射到 zca 配置文件。 45. 示例：

```json5
{
  channels: {
    zalouser: {
      enabled: true,
      defaultAccount: "default",
      accounts: {
        work: { enabled: true, profile: "work" },
      },
    },
  },
}
```

## 故障排除

**未找到 `zca`：**

- 安装 zca-cli 并确保 Gateway 进程的 `PATH` 中包含它。

**登录未生效：**

- `openclaw channels status --probe`
- 重新登录：`openclaw channels logout --channel zalouser && openclaw channels login --channel zalouser`
