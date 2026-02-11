---
summary: "O‘rnatuvchi skriptlar qanday ishlaydi (install.sh, install-cli.sh, install.ps1), flaglar va avtomatlashtirish"
read_when:
  - "`openclaw.ai/install.sh` ni tushunmoqchisiz"
  - O‘rnatishni avtomatlashtirmoqchisiz (CI / headless)
  - GitHub checkout’dan o‘rnatmoqchisiz
title: "Installer Internals"
---

# O‘rnatuvchi ichki tuzilishi

OpenClaw ships three installer scripts, served from `openclaw.ai`.

| Script                             | Platforma                               | What it does                                                                                                                                                           |
| ---------------------------------- | --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`install.sh`](#installsh)         | macOS / Linux / WSL                     | Installs Node if needed, installs OpenClaw via npm (default) or git, and can run onboarding.                                        |
| [`install-cli.sh`](#install-clish) | macOS / Linux / WSL                     | Installs Node + OpenClaw into a local prefix (`~/.openclaw`). Root huquqi talab etilmaydi.                          |
| [`install.ps1`](#installps1)       | Windows (PowerShell) | Agar kerak bo‘lsa Node’ni o‘rnatadi, OpenClaw’ni npm (standart) yoki git orqali o‘rnatadi va onboarding’ni ishga tushirishi mumkin. |

## Quick commands

<Tabs>
  <Tab title="install.sh">
    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash
    ```

    ````
    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --help
    ```
    ````

  </Tab>
  <Tab title="install-cli.sh">
    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash
    ```

    ````
    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --help
    ```
    ````

  </Tab>
  <Tab title="install.ps1">
    ```powershell
    iwr -useb https://openclaw.ai/install.ps1 | iex
    ```

    ````
    ```powershell
    & ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -Tag beta -NoOnboard -DryRun
    ```
    ````

  </Tab>
</Tabs>

<Note>
If install succeeds but `openclaw` is not found in a new terminal, see [Node.js troubleshooting](/install/node#troubleshooting).
</Note>

---

## install.sh

<Tip>
Recommended for most interactive installs on macOS/Linux/WSL.
</Tip>

### Flow (install.sh)

<Steps>
  <Step title="Detect OS">
    Supports macOS and Linux (including WSL). If macOS is detected, installs Homebrew if missing.
  </Step>
  <Step title="Ensure Node.js 22+">
    Checks Node version and installs Node 22 if needed (Homebrew on macOS, NodeSource setup scripts on Linux apt/dnf/yum).
  </Step>
  <Step title="Ensure Git">
    Installs Git if missing.
  </Step>
  <Step title="Install OpenClaw">
    - `npm` method (default): global npm install
    - `git` method: clone/update repo, install deps with pnpm, build, then install wrapper at `~/.local/bin/openclaw`
  </Step>
  <Step title="Post-install tasks">
    - Runs `openclaw doctor --non-interactive` on upgrades and git installs (best effort)
    - Attempts onboarding when appropriate (TTY available, onboarding not disabled, and bootstrap/config checks pass)
    - Defaults `SHARP_IGNORE_GLOBAL_LIBVIPS=1`
  </Step>
</Steps>

### Source checkout detection

If run inside an OpenClaw checkout (`package.json` + `pnpm-workspace.yaml`), the script offers:

- use checkout (`git`), or
- use global install (`npm`)

If no TTY is available and no install method is set, it defaults to `npm` and warns.

The script exits with code `2` for invalid method selection or invalid `--install-method` values.

### Examples (install.sh)

<Tabs>
  <Tab title="Default">
    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash
    ```
  </Tab>
  <Tab title="Skip onboarding">
    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --no-onboard
    ```
  </Tab>
  <Tab title="Git install">
    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --install-method git
    ```
  </Tab>
  <Tab title="Dry run">
    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --dry-run
    ```
  </Tab>
</Tabs>

<AccordionGroup>
  <Accordion title="Flags reference">

| Flag                              | Description                                                                                                                       |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `--install-method npm\\|git`     | O‘rnatish usulini tanlang (standart: `npm`). Alias: `--method` |
| `--npm`                           | npm usuli uchun qisqartma                                                                                                         |
| `--git`                           | git usuli uchun qisqartma. Alias: `--github`                                                      |
| `--version <version\\|dist-tag>` | npm versiyasi yoki dist-tag (standart: `latest`)                                               |
| `--beta`                          | Agar mavjud bo‘lsa beta dist-tag’dan foydalaning, aks holda `latest` ga qayting                                                   |
| `--git-dir <path>`                | Checkout katalogi (standart: `~/openclaw`). Alias: `--dir`     |
| `--no-git-update`                 | Mavjud checkout uchun `git pull` ni o‘tkazib yuborish                                                                             |
| `--no-prompt`                     | So‘rovlarni o‘chirish                                                                                                             |
| `--no-onboard`                    | Onboarding’ni o‘tkazib yuborish                                                                                                   |
| `--onboard`                       | Onboarding’ni yoqish                                                                                                              |
| `--dry-run`                       | O‘zgarishlarni qo‘llamasdan, bajariladigan amallarni chiqarish                                                                    |
| `--verbose`                       | Debug chiqishini yoqish (`set -x`, npm notice-darajadagi loglar)                                               |
| `--help`                          | Foydalanish bo‘yicha ma’lumotni ko‘rsatish (`-h`)                                                              |

  </Accordion>

  <Accordion title="Environment variables reference">

| O‘zgaruvchi                                     | Tavsif                                                                                       |
| ----------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `OPENCLAW_INSTALL_METHOD=git\\|npm`            | O‘rnatish usuli                                                                              |
| `OPENCLAW_VERSION=latest\\|next\\|<semver>`   | npm versiyasi yoki dist-tag                                                                  |
| `OPENCLAW_BETA=0\\|1`                          | Agar mavjud bo‘lsa betadan foydalanish                                                       |
| `OPENCLAW_GIT_DIR=<path>`                       | Checkout katalogi                                                                            |
| `OPENCLAW_GIT_UPDATE=0\\|1`                    | git yangilanishlarini yoqish/o‘chirish                                                       |
| `OPENCLAW_NO_PROMPT=1`                          | So‘rovlarni o‘chirish                                                                        |
| `OPENCLAW_NO_ONBOARD=1`                         | Onboarding’ni o‘tkazib yuborish                                                              |
| `OPENCLAW_DRY_RUN=1`                            | Dry run rejimi                                                                               |
| `OPENCLAW_VERBOSE=1`                            | Debug rejimi                                                                                 |
| `OPENCLAW_NPM_LOGLEVEL=error\\|warn\\|notice` | npm log darajasi                                                                             |
| `SHARP_IGNORE_GLOBAL_LIBVIPS=0\\|1`            | sharp/libvips xatti-harakatini boshqarish (standart: `1`) |

  </Accordion>
</AccordionGroup>

---

## install-cli.sh

<Info>Mahalliy prefiks ostida hammasi bo‘lishini xohlaydigan muhitlar uchun mo‘ljallangan (standart `~/.openclaw`) va tizimdagi Node’ga bog‘liqlik yo‘q.</Info>

### Jarayon (install-cli.sh)

<Steps>
  <Step title="Install local Node runtime">Node tarball’ni (standart `22.22.0`) ` ga yuklab oladi<prefix>/tools/node-v<version>` va SHA-256 ni tekshiradi.</Step>
  <Step title="Ensure Git">Agar Git mavjud bo‘lmasa, Linux’da apt/dnf/yum yoki macOS’da Homebrew orqali o‘rnatishga urinadi.</Step>
  <Step title="Install OpenClaw under prefix">npm orqali `--prefix` yordamida o‘rnatadi<prefix>`, so‘ng wrapper’ni ` ga yozadi<prefix>/bin/openclaw` ga yozadi.</Step>
</Steps>

### Misollar (install-cli.sh)

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

| Bayroq                 | Tavsif                                                                                                      |
| ---------------------- | ----------------------------------------------------------------------------------------------------------- |
| `--prefix <path>`      | O‘rnatish prefiksi (standart: `~/.openclaw`)                             |
| `--version <ver>`      | OpenClaw versiyasi yoki dist-teg (standart: `latest`)                    |
| `--node-version <ver>` | Node versiyasi (standart: `22.22.0`)                                     |
| `--json`               | NDJSON hodisalarini chiqaradi                                                                               |
| `--onboard`            | O‘rnatishdan so‘ng `openclaw onboard` ni ishga tushiradi                                                    |
| `--no-onboard`         | Onboarding’ni o‘tkazib yuboradi (standart)                                               |
| `--set-npm-prefix`     | Linux’da joriy prefiks yozish uchun ruxsatli bo‘lmasa, npm prefiksini majburan `~/.npm-global` ga o‘rnatadi |
| `--help`               | Foydalanishni ko‘rsatadi (`-h`)                                                          |

  </Accordion>

  <Accordion title="Environment variables reference">

| O‘zgaruvchi                                     | Tavsif                                                                                                                   |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `OPENCLAW_PREFIX=<path>`                        | O‘rnatish prefiksi                                                                                                       |
| `OPENCLAW_VERSION=<ver>`                        | OpenClaw versiyasi yoki dist-teg                                                                                         |
| `OPENCLAW_NODE_VERSION=<ver>`                   | Node versiyasi                                                                                                           |
| `OPENCLAW_NO_ONBOARD=1`                         | Onboarding’ni o‘tkazib yuboradi                                                                                          |
| `OPENCLAW_NPM_LOGLEVEL=error\\|warn\\|notice` | npm jurnal darajasi                                                                                                      |
| `OPENCLAW_GIT_DIR=<path>`                       | Eski tozalash uchun qidiruv yo‘li (eski `Peekaboo` submodule checkout’ni olib tashlashda ishlatiladi) |
| `SHARP_IGNORE_GLOBAL_LIBVIPS=0\\|1`            | Control sharp/libvips behavior (default: `1`)                                         |

  </Accordion>
</AccordionGroup>

---

## install.ps1

### Flow (install.ps1)

<Steps>
  <Step title="Ensure PowerShell + Windows environment">
    Requires PowerShell 5+.
  </Step>
  <Step title="Ensure Node.js 22+">Agar mavjud bo‘lmasa, avval winget orqali, so‘ng Chocolatey, undan keyin Scoop orqali o‘rnatishga urinadi.</Step>
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
  <Tab title="install-cli.sh (JSON)">
    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --json --prefix /opt/openclaw
    ```
  </Tab>
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
    Git is required for `git` install method. `npm` orqali o‘rnatishda, bog‘liqliklar git URLlardan foydalanganda `spawn git ENOENT` xatolarini oldini olish uchun Git hali ham tekshiriladi/o‘rnatiladi.
  </Accordion>

  <Accordion title="Why does npm hit EACCES on Linux?">
    Ba’zi Linux sozlamalarida npm global prefix root egasiga tegishli yo‘llarga ko‘rsatilgan bo‘ladi. `install.sh` prefixni `~/.npm-global` ga o‘zgartirishi va (agar mavjud bo‘lsa) shell rc fayllariga PATH eksportlarini qo‘shishi mumkin.
  </Accordion>

  <Accordion title="sharp/libvips issues">
    Skriptlar sharp’ning tizimdagi libvips bilan qurilishini oldini olish uchun sukut bo‘yicha `SHARP_IGNORE_GLOBAL_LIBVIPS=1` ni o‘rnatadi. Bekor qilish uchun:

    ````
    ```bash
    SHARP_IGNORE_GLOBAL_LIBVIPS=0 curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash
    ```
    ````

  </Accordion>

  <Accordion title='Windows: "npm error spawn git / ENOENT"'>Git for Windows’ni o‘rnating, PowerShell’ni qayta oching, o‘rnatuvchini yana ishga tushiring.</Accordion>

  <Accordion title='Windows: "openclaw is not recognized"'>`npm config get prefix` ni ishga tushiring, oxiriga `\bin` qo‘shing, o‘sha katalogni foydalanuvchi PATH’iga qo‘shing, so‘ng PowerShell’ni qayta oching.</Accordion>

  <Accordion title="openclaw not found after install">
    Odatda bu PATH bilan bog‘liq muammo. [Node.js troubleshooting](/install/node#troubleshooting) ga qarang.
  </Accordion>
</AccordionGroup>
