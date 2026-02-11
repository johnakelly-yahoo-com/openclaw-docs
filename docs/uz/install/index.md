---
summary: "OpenClaw’ni o‘rnatish — o‘rnatuvchi skript, npm/pnpm, manba kodidan, Docker va boshqalar"
read_when:
  - Sizga Getting Started tezkor qo‘llanmasidan tashqari o‘rnatish usuli kerak
  - Siz bulutli platformaga joylashtirmoqchisiz
  - Sizga yangilash, migratsiya qilish yoki o‘chirish kerak
title: "O‘rnatish"
---

# O‘rnatish

Allaqachon [Getting Started](/start/getting-started) qo‘llanmasiga amal qildingizmi? Hammasi tayyor — bu sahifa muqobil o‘rnatish usullari, platformaga xos ko‘rsatmalar va texnik xizmat uchun.

## Tizim talablari

- **[Node 22+](/install/node)** (agar mavjud bo‘lmasa, [o‘rnatuvchi skript](#install-methods) uni o‘rnatadi)
- macOS, Linux yoki Windows
- `pnpm` faqat manba kodidan yig‘ilganda kerak

<Note>Windows’da OpenClaw’ni [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) ostida ishga tushirishni qat’iy tavsiya qilamiz.</Note>

## O‘rnatish usullari

<Tip>
**O‘rnatuvchi skript** OpenClaw’ni o‘rnatishning tavsiya etilgan usuli. U Node’ni aniqlash, o‘rnatish va boshlang‘ich sozlashni bir bosqichda bajaradi.
</Tip>

<AccordionGroup>
  <Accordion title="Installer script" icon="rocket" defaultOpen>CLI’ni yuklab oladi, uni npm orqali global o‘rnatadi va boshlang‘ich sozlash ustasini ishga tushiradi.

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
    
    Shu bilan tamom — skript Node’ni aniqlash, o‘rnatish va boshlang‘ich sozlashni o‘zi bajaradi.
    
    Boshlang‘ich sozlashni o‘tkazib yuborib, faqat binarni o‘rnatish uchun:
    
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
    
    Barcha flaglar, muhit o‘zgaruvchilari va CI/avtomatlashtirish variantlari uchun [Installer internals](/install/installer) sahifasiga qarang.
    ```

  </Accordion>

  <Accordion title="npm / pnpm" icon="package">Agar sizda allaqachon Node 22+ mavjud bo‘lsa va o‘rnatishni o‘zingiz boshqarishni xohlasangiz:

    ```
    <Tabs>
      <Tab title="npm">
        ```bash
        npm install -g openclaw@latest
        openclaw onboard --install-daemon
        ```
    
        <Accordion title="sharp build errors?">
          Agar sizda libvips global o‘rnatilgan bo‘lsa (macOS’da Homebrew orqali tez-tez uchraydi) va `sharp` xato bersa, tayyor binarlarni majburan ishlating:
    
          ```bash
          SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install -g openclaw@latest
          ```
    
          Agar `sharp: Please add node-gyp to your dependencies` xabarini ko‘rsangiz, yoki qurilish vositalarini o‘rnating (macOS: Xcode CLT + `npm install -g node-gyp`), yoki yuqoridagi muhit o‘zgaruvchisidan foydalaning.
        </Accordion>
      </Tab>
      <Tab title="pnpm">
        ```bash
        pnpm add -g openclaw@latest
        pnpm approve-builds -g        # openclaw, node-llama-cpp, sharp va boshqalarni tasdiqlang
        openclaw onboard --install-daemon
        ```
    
        <Note>
        pnpm qurilish skriptlariga ega paketlar uchun aniq tasdiqlashni talab qiladi. Birinchi o‘rnatishda "Ignored build scripts" ogohlantirishi chiqqach, `pnpm approve-builds -g` buyrug‘ini ishga tushiring va ro‘yxatdagi paketlarni tanlang.
        </Note>
      </Tab>
    </Tabs>
    ```

  </Accordion>

  <Accordion title="From source" icon="github">Hissa qo‘shuvchilar yoki lokal checkout’dan ishga tushirmoqchi bo‘lganlar uchun.

    ```
    <Steps>
      <Step title="Clone and build">
        [OpenClaw repo](https://github.com/openclaw/openclaw) ni klonlab, yig‘ing:
    
        ```bash
        git clone https://github.com/openclaw/openclaw.git
        cd openclaw
        pnpm install
        pnpm ui:build
        pnpm build
        ```
      </Step>
      <Step title="Link the CLI">
        `openclaw` buyrug‘ini global mavjud qiling:
    
        ```bash
        pnpm link --global
        ```
    
        Yoki link qilmasdan, repozitoriya ichidan `pnpm openclaw ...` orqali buyruqlarni ishga tushiring.
      </Step>
      <Step title="Run onboarding">
        ```bash
        openclaw onboard --install-daemon
        ```
      </Step>
    </Steps>
    
    Chuqurroq ishlab chiqish jarayonlari uchun [Setup](/start/setup) sahifasiga qarang.
    ```

  </Accordion>
</AccordionGroup>

## Boshqa o‘rnatish usullari

<CardGroup cols={2}>
  <Card title="Docker" href="/install/docker" icon="container">Konteynerlangan yoki headless joylashtirishlar.</Card>
  <Card title="Nix" href="/install/nix" icon="snowflake">Nix orqali deklarativ o‘rnatish.</Card>
  <Card title="Ansible" href="/install/ansible" icon="server">Avtomatlashtirilgan park (fleet) tayyorlash.</Card>
  <Card title="Bun" href="/install/bun" icon="zap">Bun runtime orqali faqat CLI’dan foydalanish.</Card>
</CardGroup>

## O‘rnatilgandan so‘ng

Hammasi ishlayotganini tekshiring:

```bash
openclaw doctor         # konfiguratsiya muammolarini tekshirish
openclaw status         # gateway holati
openclaw dashboard      # brauzer UI’ni ochish
```

Agar sizga maxsus runtime yo‘llari kerak bo‘lsa, quyidagilardan foydalaning:

- Uy katalogiga asoslangan ichki yo‘llar uchun `OPENCLAW_HOME`
- O‘zgaruvchan holat joylashuvi uchun `OPENCLAW_STATE_DIR`
- Konfiguratsiya fayli joylashuvi uchun `OPENCLAW_CONFIG_PATH`

Ustuvorlik va to‘liq tafsilotlar uchun [Environment vars](/help/environment) ga qarang.

## Nosozliklarni bartaraf etish: `openclaw` topilmadi

<Accordion title="PATH diagnosis and fix">Tezkor tashxis:

```bash
node -v
npm -v
npm prefix -g
echo "$PATH"
```

Agar `$(npm prefix -g)/bin` (macOS/Linux) yoki `$(npm prefix -g)` (Windows) **$PATH** ichida bo‘lmasa, shell global npm binarlarini (jumladan `openclaw`) topa olmaydi.

Tuzatish — uni shell’ning ishga tushish fayliga qo‘shing (`~/.zshrc` yoki `~/.bashrc`):

```bash
export PATH="$(npm prefix -g)/bin:$PATH"
```

Windows’da `npm prefix -g` chiqishini PATH’ga qo‘shing.

So‘ng yangi terminal oching (yoki zsh’da `rehash` / bash’da `hash -r`). </Accordion>

## Yangilash / o‘chirish

<CardGroup cols={3}>
  <Card title="Updating" href="/install/updating" icon="refresh-cw">OpenClaw’ni yangilab turing.</Card>
  <Card title="Migrating" href="/install/migrating" icon="arrow-right">Yangi kompyuterga ko‘chirish.</Card>
  <Card title="Uninstall" href="/install/uninstall" icon="trash-2">OpenClaw’ni to‘liq olib tashlash.</Card>
</CardGroup>
