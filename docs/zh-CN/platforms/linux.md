---
summary: "Linux 支持 + 伴侣应用状态"
read_when:
  - 查找 Linux 伴侣应用状态
  - 规划平台覆盖或贡献
title: "Linux 应用"
---

# Linux 应用

Gateway 在 Linux 上得到完全支持。 **Node 是推荐的运行时**。
不建议在 Gateway 上使用 Bun（存在 WhatsApp/Telegram 的问题）。

原生 Linux 伴侣应用已在计划中。 如果你想帮助构建一个，欢迎贡献。

## 新手快速路径（VPS）

1. 安装 Node 22+
2. `npm i -g openclaw@latest`
3. `openclaw onboard --install-daemon`
4. 从你的笔记本电脑：`ssh -N -L 18789:127.0.0.1:18789 <user>@<host>`
5. 打开 `http://127.0.0.1:18789/` 并粘贴你的令牌

分步 VPS 指南：[exe.dev](/install/exe-dev)

## 安装

- [入门](/start/getting-started)
- [安装与更新](/install/updating)
- 可选流程：[Bun（实验性）](/install/bun)，[Nix](/install/nix)，[Docker](/install/docker)

## Gateway

- [Gateway 运行手册](/gateway)
- [配置](/gateway/configuration)

## Gateway 服务安装（CLI）

使用以下之一：

```
openclaw onboard --install-daemon
```

或者：

```
openclaw gateway install
```

或者：

```
openclaw configure
```

在提示时选择 **Gateway 服务**。

修复/迁移：

```
openclaw doctor
```

## 系统控制（systemd 用户单元）

OpenClaw 默认安装一个 systemd **用户** 服务。 对于共享或始终在线的服务器，使用 **system**
服务。 完整的单元示例和指导
位于 [Gateway 运行手册](/gateway) 中。

最小化设置：

创建 `~/.config/systemd/user/openclaw-gateway[-<profile>].service`：

```
[Unit]
Description=OpenClaw Gateway (profile: <profile>, v<version>)
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/local/bin/openclaw gateway --port 18789
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
```

Enable it:

```
systemctl --user enable --now openclaw-gateway[-<profile>].service
```
