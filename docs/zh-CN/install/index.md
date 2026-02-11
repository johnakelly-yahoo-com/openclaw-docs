---
summary: "安装 OpenClaw —— 安装脚本、npm/pnpm、从源码、Docker 等多种方式"
read_when:
  - 你需要一种不同于 Getting Started 快速入门的安装方式
  - 你想要部署到云平台
  - 你需要更新、迁移或卸载
title: "安装"
---

# 安装

已经按照 [Getting Started](/start/getting-started) 操作过了吗？ 一切就绪 —— 本页面用于介绍替代安装方法、平台特定说明以及维护。

## 系统要求

- **[Node 22+](/install/node)**（如果缺失，[安装脚本](#install-methods) 会自动安装）
- macOS、Linux 或 Windows
- 仅在从源码构建时需要 `pnpm`

<Note>
在 Windows 上，我们强烈建议在 [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) 下运行 OpenClaw。
</Note>

## 安装方式

<Tip>
**安装脚本** 是安装 OpenClaw 的推荐方式。 它在一步中完成 Node 检测、安装和引导配置。
</Tip>

<AccordionGroup>
  <Accordion title="Installer script" icon="rocket" defaultOpen>
    下载 CLI，通过 npm 全局安装，并启动引导向导。


    ```
    <Tabs>
      <Tab title="macOS / Linux / WSL2">
        ```bash
        curl -fsSL https://openclaw.ai/install.sh | bash
        ```
      </Tab>
      <Tab title="Windows (PowerShell)">
        ```powershell
        iwr -useb https://openclaw.ai/install.ps1 | iex
        ```
      </Tab>
    </Tabs>
    
    就是这样 —— 脚本会处理 Node 检测、安装和引导配置。
    
    如果要跳过引导，仅安装二进制文件：
    
    <Tabs>
      <Tab title="macOS / Linux / WSL2">
        ```bash
        curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard
        ```
      </Tab>
      <Tab title="Windows (PowerShell)">
        ```powershell
        & ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard
        ```
      </Tab>
    </Tabs>
    
    有关所有标志、环境变量以及 CI/自动化选项，请参见 [Installer internals](/install/installer)。
    ```

  </Accordion>

  <Accordion title="npm / pnpm" icon="package">
    如果你已经有 Node 22+，并且希望自行管理安装：

    ```
    <Tabs>
      <Tab title="npm">
        ```bash
        npm install -g openclaw@latest
        openclaw onboard --install-daemon
        ```
    
        <Accordion title="sharp 构建错误？">
          如果你全局安装了 libvips（在 macOS 上通过 Homebrew 很常见），并且 `sharp` 失败，请强制使用预编译二进制文件：
    
          ```bash
          SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install -g openclaw@latest
          ```
    
          如果你看到 `sharp: Please add node-gyp to your dependencies`，请安装构建工具（macOS：Xcode CLT + `npm install -g node-gyp`），或使用上述环境变量。
        </Accordion>
      </Tab>
      <Tab title="pnpm">
        ```bash
        pnpm add -g openclaw@latest
        pnpm approve-builds -g        # approve openclaw, node-llama-cpp, sharp, etc.
        openclaw onboard --install-daemon
        ```
    
        <Note>
        pnpm 需要对包含构建脚本的包进行显式批准。首次安装显示 “Ignored build scripts” 警告后，请运行 `pnpm approve-builds -g` 并选择列出的包。
        </Note>
      </Tab>
    </Tabs>
    ```

  </Accordion>

  <Accordion title="From source" icon="github">
    面向贡献者或任何希望从本地检出运行的人。

    ```
    <Steps>
      <Step title="克隆并构建">
        克隆 [OpenClaw 仓库](https://github.com/openclaw/openclaw) 并构建：
    
        ```bash
        git clone https://github.com/openclaw/openclaw.git
        cd openclaw
        pnpm install
        pnpm ui:build
        pnpm build
        ```
      </Step>
      <Step title="链接 CLI">
        使 `openclaw` 命令在全局可用：
    
        ```bash
        pnpm link --global
        ```
    
        或者，跳过链接，直接在仓库内通过 `pnpm openclaw ...` 运行命令。
      </Step>
      <Step title="运行引导配置">
        ```bash
        openclaw onboard --install-daemon
        ```
      </Step>
    </Steps>
    
    有关更深入的开发工作流，请参见 [Setup](/start/setup)。
    ```

  </Accordion>
</AccordionGroup>

## 其他安装方式

<CardGroup cols={2}>
  <Card title="Docker" href="/install/docker" icon="container">
    容器化或无头部署。
  </Card>
  <Card title="Nix" href="/install/nix" icon="snowflake">
    通过 Nix 进行声明式安装。
  </Card>
  <Card title="Ansible" href="/install/ansible" icon="server">
    自动化的集群/规模化部署。
  </Card>
  <Card title="Bun" href="/install/bun" icon="zap">
    通过 Bun 运行时进行仅 CLI 使用。
  </Card>
</CardGroup>

## 安装完成后

验证一切是否正常工作：

```bash
openclaw doctor         # 检查配置问题
openclaw status         # 网关状态
openclaw dashboard      # 打开浏览器 UI
```

如果需要自定义运行时路径，请使用：

- 基于主目录的内部路径使用 `OPENCLAW_HOME`
- 可变状态位置使用 `OPENCLAW_STATE_DIR`
- 配置文件位置使用 `OPENCLAW_CONFIG_PATH`

有关优先级和完整细节，请参见 [Environment vars](/help/environment)。

## 故障排查：未找到 `openclaw`

<Accordion title="PATH diagnosis and fix">
  快速诊断：

```bash
node -v
npm -v
npm prefix -g
echo "$PATH"
```

如果 `$(npm prefix -g)/bin`（macOS/Linux）或 `$(npm prefix -g)`（Windows）**不在**你的 `$PATH` 中，shell 将无法找到全局 npm 二进制文件（包括 `openclaw`）。

修复 —— 将其添加到你的 shell 启动文件（`~/.zshrc` 或 `~/.bashrc`）：

```bash
export PATH="$(npm prefix -g)/bin:$PATH"
```

在 Windows 上，将 `npm prefix -g` 的输出添加到你的 PATH。

然后打开一个新的终端（或在 zsh 中执行 `rehash` / 在 bash 中执行 `hash -r`）。 </Accordion>

## 更新 / 卸载

<CardGroup cols={3}>
  <Card title="Updating" href="/install/updating" icon="refresh-cw">
    保持 OpenClaw 为最新版本。
  </Card>
  <Card title="Migrating" href="/install/migrating" icon="arrow-right">
    迁移到新机器。
  </Card>
  <Card title="Uninstall" href="/install/uninstall" icon="trash-2">
    完全移除 OpenClaw。
  </Card>
</CardGroup>
