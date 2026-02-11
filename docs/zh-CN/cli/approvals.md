---
summary: "`openclaw approvals` 的 CLI 参考（用于 Gateway 或节点主机的执行审批）"
read_when:
  - 你希望通过 CLI 编辑执行审批
  - 你需要在 Gateway 或节点主机上管理允许列表
title: "approvals"
---

# `openclaw approvals`

管理**本地主机**、**网关主机**或**节点主机**的 exec 审批。
默认情况下，命令会作用于磁盘上的本地审批文件。 Use `--gateway` to target the gateway, or `--node` to target a specific node.

相关：

- Exec 审批：[Exec approvals](/tools/exec-approvals)
- Nodes: [Nodes](/nodes)

## Common commands

```bash
openclaw approvals get
openclaw approvals get --node <id|name|ip>
openclaw approvals get --gateway
```

## 从文件替换审批

```bash
openclaw approvals set --file ./exec-approvals.json
openclaw approvals set --node <id|name|ip> --file ./exec-approvals.json
openclaw approvals set --gateway --file ./exec-approvals.json
```

## 允许列表辅助工具

```bash
openclaw approvals allowlist add "~/Projects/**/bin/rg"
openclaw approvals allowlist add --agent main --node <id|name|ip> "/usr/bin/uptime"
openclaw approvals allowlist add --agent "*" "/usr/bin/uname"

openclaw approvals allowlist remove "~/Projects/**/bin/rg"
```

## 说明

- `--node` uses the same resolver as `openclaw nodes` (id, name, ip, or id prefix).
- `--agent` 默认为 `"*"`，适用于所有 agent。
- The node host must advertise `system.execApprovals.get/set` (macOS app or headless node host).
- 审批文件按主机存储在 `~/.openclaw/exec-approvals.json`。
