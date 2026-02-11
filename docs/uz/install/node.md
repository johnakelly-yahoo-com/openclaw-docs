---
title: "Node.js"
summary: "Install and configure Node.js for OpenClaw — version requirements, install options, and PATH troubleshooting"
read_when:
  - "You need to install Node.js before installing OpenClaw"
  - "You installed OpenClaw but `openclaw` is command not found"
  - "npm install -g fails with permissions or PATH issues"
---

# Node.js

OpenClaw requires **Node 22 or newer**. The [installer script](/install#install-methods) will detect and install Node automatically — this page is for when you want to set up Node yourself and make sure everything is wired up correctly (versions, PATH, global installs).

## Check your version

```bash
node -v
```

If this prints `v22.x.x` or higher, you're good. If Node isn't installed or the version is too old, pick an install method below.

## Install Node

<Tabs>
  <Tab title="macOS">**Homebrew** (tavsiya etiladi):

    ````
    ```bash
    brew install node
    ```
    ````

  </Tab>
  <Tab title="Linux"></Tab>

    ```
    **Ubuntu / Debian:**
    ```

  </Tab>
  <Tab title="Windows">**Fedora / RHEL:**

```bash
sudo dnf install nodejs
```

Yoki versiya menejeridan foydalaning (quyida qarang).

    ````
    ```powershell
    winget install OpenJS.NodeJS.LTS
    ```
    
    **Chocolatey:**
    
    ```powershell
    choco install nodejs-lts
    ```
    
    Yoki Windows o‘rnatuvchisini [nodejs.org](https://nodejs.org/) saytidan yuklab oling.
    ````

  </Tab>
</Tabs>

<Accordion title="Using a version manager (nvm, fnm, mise, asdf)">
  ```powershell
winget install OpenJS.NodeJS.LTS
``` **Chocolatey:**

```powershell
choco install nodejs-lts
```

Yoki Windows o‘rnatkichini [nodejs.org](https://nodejs.org/) saytidan yuklab oling.

- </Tab>
- Versiya menejerlari Node versiyalari orasida oson almashishga imkon beradi.
- Mashhur variantlar:

[**fnm**](https://github.com/Schniz/fnm) — tezkor, kross-platforma

```bash
[**nvm**](https://github.com/nvm-sh/nvm) — macOS/Linux’da keng qo‘llaniladi
```

  <Warning>
  [**mise**](https://mise.jdx.dev/) — poliglot (Node, Python, Ruby va boshqalar) fnm bilan misol:
  </Warning>
</Accordion>

fnm install 22
fnm use 22
----------

### Versiya menejeringiz shell ishga tushish faylida (`~/.zshrc` yoki `~/.bashrc`) ishga tushirilganiga ishonch hosil qiling.

Agar shunday bo‘lmasa, yangi terminal sessiyalarida `openclaw` topilmasligi mumkin, chunki PATH Node’ning bin katalogini o‘z ichiga olmaydi.

<Steps>
  <Step title="Find your global npm prefix">Nosozliklarni bartaraf etish</Step>
  <Step title="Check if it's on your PATH">`openclaw: command not found`

    ```
    Bu deyarli har doim npm’ning global bin katalogi PATH’da yo‘qligini anglatadi.
    ```

  </Step>
  <Step title="Add it to your shell startup file">
    <Tabs>
      <Tab title="macOS / Linux">```bash
echo "$PATH"
```

        ```
        Natijada `<npm-prefix>/bin` (macOS/Linux) yoki `<npm-prefix>` (Windows) borligini tekshiring.
        ```

  </Step>
</Steps>

### `~/.zshrc` yoki `~/.bashrc` ga qo‘shing:

```bash
export PATH="$(npm prefix -g)/bin:$PATH"
```So‘ng yangi terminal oching (yoki zsh’da `rehash` / bash’da `hash -r` ni ishga tushiring). </Tab> <Tab title="Windows">
`npm prefix -g` chiqishini Sozlamalar → Tizim → Atrof-muhit o‘zgaruvchilari orqali tizim PATH’iga qo‘shing. </Tab> </Tabs>

```bash
</Step>
```

`npm install -g` da ruxsat xatolari (Linux)
