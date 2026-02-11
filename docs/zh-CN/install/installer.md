---
summary: "安装脚本的工作原理（install.sh、install-cli.sh、install.ps1）、标志以及自动化"
read_when:
  - 你想了解 `openclaw.ai/install.sh`
  - 你想要自动化安装（CI / 无头）
  - 你想从 GitHub 检出进行安装
title: "1. 安装器内部机制"
---

# 2. 安装器内部机制

3. OpenClaw 提供三个安装脚本，由 `openclaw.ai` 提供服务。

| 4. 脚本                                  | 5. 平台                   | 6. 功能说明                                                                       |
| ------------------------------------------------------------- | ---------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| 7. [`install.sh`](#installsh)          | 8. macOS / Linux / WSL  | 9. 如有需要则安装 Node，通过 npm（默认）或 git 安装 OpenClaw，并可运行引导流程。                         |
| 10. [`install-cli.sh`](#install-clish) | 11. macOS / Linux / WSL | 12. 将 Node + OpenClaw 安装到本地前缀（`~/.openclaw`）。 13. 无需 root 权限。 |
| 14. [`install.ps1`](#installps1)       | 15. Windows（PowerShell） | 16. 如有需要则安装 Node，通过 npm（默认）或 git 安装 OpenClaw，并可运行引导流程。                        |

## 17. 快速命令

<Tabs>
  <Tab title="install.sh">
    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash
    ```

    ```
        ```bash
        curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash
        ```
    ```

  </Tab>
  <Tab title="install-cli.sh">  </Tab>

    ````
    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --help
    ```
    ````

  </Tab>
  <Tab title="install.ps1">```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --help
```

    ```
      </Tab>
    ```

  </Tab>
</Tabs>

<Note>    ```powershell
    iwr -useb https://openclaw.ai/install.ps1 | iex
    ```</Note>

---

## ```powershell
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -Tag beta -NoOnboard -DryRun
```

<Tip>  </Tab></Tip>

### Flow (install.sh)

<Steps>
  <Step title="Detect OS">
    如果安装成功但在新终端中找不到 `openclaw`，请参阅 [Node.js 故障排查](/install/node#troubleshooting)。 28. install.sh
  </Step>
  <Step title="Ensure Node.js 22+">
    Checks Node version and installs Node 22 if needed (Homebrew on macOS, NodeSource setup scripts on Linux apt/dnf/yum).
  </Step>
  <Step title="Ensure Git">推荐用于 macOS/Linux/WSL 上的大多数交互式安装。</Step>
  <Step title="Install OpenClaw">30. 流程（install.sh）</Step>
  <Step title="Post-install tasks">31. 支持 macOS 和 Linux（包括 WSL）。</Step>
</Steps>

### 32. 如果检测到 macOS，则在缺失时安装 Homebrew。

If run inside an OpenClaw checkout (`package.json` + `pnpm-workspace.yaml`), the script offers:

- ```
  检查 Node 版本，如有需要则安装 Node 22（macOS 使用 Homebrew，Linux 使用 NodeSource 安装脚本，适用于 apt/dnf/yum）。
  ```
- use global install (`npm`)

```
如缺失则安装 Git。
```

The script exits with code `2` for invalid method selection or invalid `--install-method` values.

### ```
- `npm` 方式（默认）：全局 npm 安装
- `git` 方式：克隆/更新仓库，使用 pnpm 安装依赖、构建，然后在 `~/.local/bin/openclaw` 安装包装器
```

<Tabs>
  <Tab title="Default">
    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash
    ```
  </Tab>
  <Tab title="Skip onboarding">    - 在升级和 git 安装时运行 `openclaw doctor --non-interactive`（尽力而为）
    - 在合适条件下尝试运行引导流程（有 TTY、未禁用引导，且引导/配置检查通过）
    - 默认设置 `SHARP_IGNORE_GLOBAL_LIBVIPS=1`</Tab>
  <Tab title="Git install">37. 源码检出检测</Tab>
  <Tab title="Dry run">38. 如果在 OpenClaw 的检出目录中运行（存在 `package.json` + `pnpm-workspace.yaml`），脚本将提供：</Tab>
</Tabs>

<AccordionGroup>
  <Accordion title="Flags reference">

| 39. 使用检出版本（`git`），或                         | 40. 使用全局安装（`npm`）                                                                                      |
| ------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| 41. 如果没有可用的 TTY 且未设置安装方式，则默认使用 `npm` 并给出警告。 | Choose install method (default: `npm`). Alias: `--method`  |
| `--npm`                                                            | Shortcut for npm method                                                                                                       |
| `--git`                                                            | Shortcut for git method. Alias: `--github`                                                    |
| `--version <version\\|dist-tag>`                                  | npm version or dist-tag (default: `latest`)                                                |
| `--beta`                                                           | Use beta dist-tag if available, else fallback to `latest`                                                                     |
| `--git-dir <path>`                                                 | Checkout directory (default: `~/openclaw`). Alias: `--dir` |
| `--no-git-update`                                                  | Skip `git pull` for existing checkout                                                                                         |
| `--no-prompt`                                                      | Disable prompts                                                                                                               |
| `--no-onboard`                                                     | Skip onboarding                                                                                                               |
| `--onboard`                                                        | Enable onboarding                                                                                                             |
| `--dry-run`                                                        | Print actions without applying changes                                                                                        |
| `--verbose`                                                        | Enable debug output (`set -x`, npm notice-level logs)                                                      |
| `--help`                                                           | Show usage (`-h`)                                                                                          |

  </Accordion>

  <Accordion title="Environment variables reference">

| Variable                                        | Description                 |
| ----------------------------------------------- | --------------------------- |
| `OPENCLAW_INSTALL_METHOD=git\\|npm`            | Install method              |
| `OPENCLAW_VERSION=latest\\|next\\|<semver>`   | npm version or dist-tag     |
| `OPENCLAW_BETA=0\\|1`                          | Use beta if available       |
| `OPENCLAW_GIT_DIR=<path>`                       | Checkout directory          |
| `OPENCLAW_GIT_UPDATE=0\\|1`                    | Toggle git updates          |
| `OPENCLAW_NO_PROMPT=1`                          | Disable prompts             |
| `OPENCLAW_NO_ONBOARD=1`                         | Skip onboarding             |
| `OPENCLAW_DRY_RUN=1`                            | Dry run mode                |
| `OPENCLAW_VERBOSE=1`                            | Debug mode                  |
| `OPENCLAW_NPM_LOGLEVEL=error\\|warn\\|notice` | npm log level               |
| `SHARP_IGNORE_GLOBAL_LIBVIPS=0\\|1`            | 控制 sharp/libvips 行为（默认：`1`） |

  </Accordion>
</AccordionGroup>

---

## install-cli.sh

<Info>适用于希望将所有内容安装在本地前缀下（默认 `~/.openclaw`）且不依赖系统 Node 的环境。</Info>

### 流程（install-cli.sh）

<Steps>
  <Step title="Install local Node runtime">下载 Node 压缩包（默认 `22.22.0`）到 `<prefix>/tools/node-v<version>` 并验证 SHA-256。</Step>
  <Step title="Ensure Git">如果缺少 Git，则在 Linux 上尝试通过 apt/dnf/yum 安装，或在 macOS 上通过 Homebrew 安装。</Step>
  <Step title="Install OpenClaw under prefix">使用 npm 并通过 `--prefix <prefix>` 安装，然后将包装器写入 `<prefix>/bin/openclaw`。</Step>
</Steps>

### 示例（install-cli.sh）

<Tabs>
  <Tab title="Default">```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash
```</Tab>
  <Tab title="Custom prefix + version">```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --prefix /opt/openclaw --version latest
```</Tab>
  <Tab title="Automation JSON output">```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --json --prefix /opt/openclaw
```</Tab>
  <Tab title="Run onboarding">```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --onboard
```</Tab>
</Tabs>

<AccordionGroup>
  <Accordion title="Flags reference">

| 标志                     | 说明                                                |
| ---------------------- | ------------------------------------------------- |
| `--prefix <path>`      | 安装前缀（默认：`~/.openclaw`）                            |
| `--version <ver>`      | OpenClaw 版本或 dist-tag（默认：`latest`）                |
| `--node-version <ver>` | Node 版本（默认：`22.22.0`）                             |
| `--json`               | 输出 NDJSON 事件                                      |
| `--onboard`            | 安装后运行 `openclaw onboard`                          |
| `--no-onboard`         | 跳过引导流程（默认）                                        |
| `--set-npm-prefix`     | 在 Linux 上，如果当前前缀不可写，则强制将 npm 前缀设为 `~/.npm-global` |
| `--help`               | 显示用法（`-h`）                                        |

  </Accordion>

  <Accordion title="Environment variables reference">

| 变量                                              | 说明                                                                               |
| ----------------------------------------------- | -------------------------------------------------------------------------------- |
| `OPENCLAW_PREFIX=<path>`                        | 安装前缀                                                                             |
| `OPENCLAW_VERSION=<ver>`                        | OpenClaw 版本或 dist-tag                                                            |
| `OPENCLAW_NODE_VERSION=<ver>`                   | Node 版本                                                                          |
| `OPENCLAW_NO_ONBOARD=1`                         | 跳过引导流程                                                                           |
| `OPENCLAW_NPM_LOGLEVEL=error\\|warn\\|notice` | npm 日志级别                                                                         |
| `OPENCLAW_GIT_DIR=<path>`                       | 旧版清理查找路径（在移除旧的 `Peekaboo` 子模块检出时使用）                                              |
| `SHARP_IGNORE_GLOBAL_LIBVIPS=0\\|1`            | Control sharp/libvips behavior (default: `1`) |

  </Accordion>
</AccordionGroup>

---

## install.ps1

### Flow (install.ps1)

<Steps>
  <Step title="Ensure PowerShell + Windows environment">
    Requires PowerShell 5+.
  </Step>
  <Step title="Ensure Node.js 22+">
    If missing, attempts install via winget, then Chocolatey, then Scoop.
  </Step>
  <Step title="Install OpenClaw">
    - `npm` method (default): global npm install using selected `-Tag`
    - `git` method: clone/update repo, install/build with pnpm, and install wrapper at `%USERPROFILE%\.local\bin\openclaw.cmd`
  </Step>
  <Step title="Post-install tasks">
    Adds needed bin directory to user PATH when possible, then runs `openclaw doctor --non-interactive` on upgrades and git installs (best effort).
  </Step>
</Steps>

### Examples (install.ps1)

<Tabs>
  <Tab title="Default">
    ```powershell
    iwr -useb https://openclaw.ai/install.ps1 | iex
    ```
  </Tab>
  <Tab title="Git install">
    ```powershell
    & ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -InstallMethod git
    ```
  </Tab>
  <Tab title="Custom git directory">
    ```powershell
    & ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -InstallMethod git -GitDir "C:\openclaw"
    ```
  </Tab>
  <Tab title="Dry run">
    ```powershell
    & ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -DryRun
    ```
  </Tab>
</Tabs>

<AccordionGroup>
  <Accordion title="Flags reference">

| Flag                        | Description                                                                                |
| --------------------------- | ------------------------------------------------------------------------------------------ |
| `-InstallMethod npm\\|git` | Install method (default: `npm`)                         |
| `-Tag <tag>`                | npm dist-tag (default: `latest`)                        |
| `-GitDir <path>`            | Checkout directory (default: `%USERPROFILE%\openclaw`) |
| `-NoOnboard`                | Skip onboarding                                                                            |
| `-NoGitUpdate`              | Skip `git pull`                                                                            |
| `-DryRun`                   | Print actions only                                                                         |

  </Accordion>

  <Accordion title="Environment variables reference">

| Variable                             | Description        |
| ------------------------------------ | ------------------ |
| `OPENCLAW_INSTALL_METHOD=git\\|npm` | Install method     |
| `OPENCLAW_GIT_DIR=<path>`            | Checkout directory |
| `OPENCLAW_NO_ONBOARD=1`              | Skip onboarding    |
| `OPENCLAW_GIT_UPDATE=0`              | Disable git pull   |
| `OPENCLAW_DRY_RUN=1`                 | Dry run mode       |

  </Accordion>
</AccordionGroup>

<Note>
If `-InstallMethod git` is used and Git is missing, the script exits and prints the Git for Windows link.
</Note>

---

## CI and automation

Use non-interactive flags/env vars for predictable runs.

<Tabs>
  <Tab title="install.sh (non-interactive npm)">
    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --no-prompt --no-onboard
    ```
  </Tab>
  <Tab title="install.sh (non-interactive git)">
    ```bash
    OPENCLAW_INSTALL_METHOD=git OPENCLAW_NO_PROMPT=1 \
      curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash
    ```
  </Tab>
  <Tab title="install-cli.sh (JSON)">```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --json --prefix /opt/openclaw
```</Tab>
  <Tab title="install.ps1 (skip onboarding)">
    ```powershell
    & ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard
    ```
  </Tab>
</Tabs>

---

## Troubleshooting

<AccordionGroup>
  <Accordion title="Why is Git required?">
    Git is required for `git` install method. 对于 `npm` 安装，仍会检查/安装 Git，以避免当依赖使用 git URL 时出现 `spawn git ENOENT` 失败。
  </Accordion>

  <Accordion title="Why does npm hit EACCES on Linux?">
    某些 Linux 环境会将 npm 全局前缀指向 root 拥有的路径。 `install.sh` 可以将前缀切换到 `~/.npm-global`，并在 shell rc 文件存在时向其中追加 PATH 导出。
  </Accordion>

  <Accordion title="sharp/libvips issues">
    脚本默认设置 `SHARP_IGNORE_GLOBAL_LIBVIPS=1`，以避免 sharp 针对系统 libvips 进行构建。 要覆盖该设置：

    ````
    ```bash
    SHARP_IGNORE_GLOBAL_LIBVIPS=0 curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash
    ```
    ````

  </Accordion>

  <Accordion title='Windows: "npm error spawn git / ENOENT"'>安装 Git for Windows，重新打开 PowerShell，然后重新运行安装程序。</Accordion>

  <Accordion title='Windows: "openclaw is not recognized"'>运行 `npm config get prefix`，在结果后追加 `\bin`，将该目录添加到用户 PATH，然后重新打开 PowerShell。</Accordion>

  <Accordion title="openclaw not found after install">
    通常是 PATH 问题。 参见 [Node.js 故障排除](/install/node#troubleshooting)。
  </Accordion>
</AccordionGroup>
