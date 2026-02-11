---
title: "Node.js"
summary: "为 OpenClaw 安装并配置 Node.js — 版本要求、安装选项以及 PATH 故障排查"
read_when:
  - "在安装 OpenClaw 之前，你需要先安装 Node.js"
  - "你已安装 OpenClaw，但提示 `openclaw` 命令未找到"
  - "npm install -g 因权限或 PATH 问题而失败"
---

# Node.js

OpenClaw 需要 **Node 22 或更新版本**。 [安装脚本](/install#install-methods) 会自动检测并安装 Node —— 本页面适用于你希望自行设置 Node 并确保一切正确连接（版本、PATH、全局安装）的情况。

## 检查你的版本

```bash
node -v
```

如果输出 `v22.x.x` 或更高版本，则表示可以使用。 如果未安装 Node 或版本过旧，请在下方选择一种安装方式。

## 安装 Node

<Tabs>
  <Tab title="macOS">**Homebrew**（推荐）：

    ````
    ```bash
    brew install node
    ```
    ````

  </Tab>
  <Tab title="Linux"></Tab>

    ```
    **Ubuntu / Debian：**
    ```

  </Tab>
  <Tab title="Windows">**Fedora / RHEL：**

```bash
sudo dnf install nodejs
```

或者使用版本管理器（见下文）。

    ```
    </Tab>
    ```

  </Tab>
</Tabs>

<Accordion title="Using a version manager (nvm, fnm, mise, asdf)">
  版本管理器可以让你轻松在不同 Node 版本之间切换。 **Chocolatey：**

```powershell
choco install nodejs-lts
```

或从 [nodejs.org](https://nodejs.org/) 下载 Windows 安装程序。

- </Tab>
- 版本管理器可以让你轻松在不同的 Node 版本之间切换。
- 常见选择：

使用 fnm 的示例：

```bash
[**nvm**](https://github.com/nvm-sh/nvm) — 在 macOS/Linux 上广泛使用
```

  <Warning>
  确保你的版本管理器已在 shell 启动文件（`~/.zshrc` 或 `~/.bashrc`）中初始化。 以 fnm 为例：
  </Warning>
</Accordion>

fnm install 22
fnm use 22
----------

### `openclaw: command not found`

否则，在新的终端会话中可能找不到 `openclaw`，因为 PATH 中不会包含 Node 的 bin 目录。

<Steps>
  <Step title="Find your global npm prefix">故障排查</Step>
  <Step title="Check if it's on your PATH">
    ```bash
    echo "$PATH"
    ```

    ```
    这几乎总是意味着 npm 的全局 bin 目录没有加入 PATH。
    ```

  </Step>
  <Step title="Add it to your shell startup file">
    <Tabs>
      <Tab title="macOS / Linux">```bash
echo "$PATH"
```

        ```
        在输出中查找 `<npm-prefix>/bin`（macOS/Linux）或 `<npm-prefix>`（Windows）。
        ```

  </Step>
</Steps>

### 添加到 `~/.zshrc` 或 `~/.bashrc`：

```bash
export PATH="$(npm prefix -g)/bin:$PATH"
```

```bash
然后打开一个新的终端（或在 zsh 中运行 `rehash` / 在 bash 中运行 `hash -r`）。
</Tab>
<Tab title="Windows">
  通过“设置 → 系统 → 环境变量”将 `npm prefix -g` 的输出添加到系统 PATH。
</Tab>
</Tabs>
```

</Step>
