---
summary: "OpenClaw’ni o‘rnating va birinchi chattingizni bir necha daqiqada ishga tushiring."
read_when:
  - Noldan birinchi sozlash
  - Siz ishlaydigan chatga eng tez yo‘lni xohlaysiz
title: "Boshlash"
---

# Boshlash

Maqsad: minimal sozlash bilan noldan birinchi ishlaydigan chatga yetib borish.

<Info>
Eng tezkor chat: Control UI’ni oching (kanal sozlamasi talab qilinmaydi). Run `openclaw dashboard`
and brauzerda chat qiling, yoki `http://127.0.0.1:18789/` ni oching
<Tooltip headline="Gateway host" tip="The machine running the OpenClaw gateway service.">gateway xosti</Tooltip>.
Hujjatlar: [Dashboard](/web/dashboard) va [Control UI](/web/control-ui).
</Info>

## Talablar

- Node 22 yoki undan yangisi

<Tip>
Check your Node version with `node --version` if you are unsure.
</Tip>

## Agar ishonchingiz komil bo‘lmasa, `node --version` bilan Node versiyangizni tekshiring.

<Steps>
  <Step title="Install OpenClaw (recommended)">
    <Tabs>
      <Tab title="macOS/Linux">Tezkor sozlash (CLI)</Tab>
      <Tab title="Windows (PowerShell)">```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```</Tab>
    </Tabs>

    ````
    ```powershell
    iwr -useb https://openclaw.ai/install.ps1 | iex
    ```
    ````

  </Step>
  <Step title="Run the onboarding wizard"></Step>

    ````
    ```bash
    openclaw onboard --install-daemon
    ```
    ````

  </Step>
  <Step title="Check the Gateway"></Step>

    ```
    Agar siz xizmatni o‘rnatgan bo‘lsangiz, u allaqachon ishlayotgan bo‘lishi kerak:
    ```

  </Step>
  <Step title="Open the Control UI"></Step></Step>
</Steps>

<Check>```bash
openclaw dashboard
```</Check>

## Agar Control UI yuklansa, Gateway foydalanishga tayyor.

<AccordionGroup>
  <Accordion title="Run the Gateway in the foreground">Ixtiyoriy tekshiruvlar va qo‘shimchalar

    ```
    Tezkor sinovlar yoki nosozliklarni aniqlash uchun foydali.
    ```

  </Accordion>
  <Accordion title="Send a test message"></Accordion>

    ````
    ```bash
    openclaw message send --target +15555550123 --message "Hello from OpenClaw"
    ```
    ````

  </Accordion>
</AccordionGroup>

## Foydali muhit o‘zgaruvchilari

Agar OpenClaw’ni xizmat hisobi sifatida ishga tushirsangiz yoki maxsus konfiguratsiya/holat joylashuvlarini xohlasangiz:

- `OPENCLAW_HOME` ichki yo‘l aniqlash uchun ishlatiladigan uy katalogini belgilaydi.
- `OPENCLAW_STATE_DIR` overrides the state directory.
- `OPENCLAW_CONFIG_PATH` overrides the config file path.

Full environment variable reference: [Environment vars](/help/environment).

## Go deeper

<Columns>
  <Card title="Onboarding Wizard (details)" href="/start/wizard">
    Full CLI wizard reference and advanced options.
  </Card>
  <Card title="macOS app onboarding" href="/start/onboarding">
    First run flow for the macOS app.
  </Card>
</Columns>

## What you will have

- A running Gateway
- Auth configured
- Control UI access or a connected channel

## Next steps

- DM safety and approvals: [Pairing](/channels/pairing)
- Connect more channels: [Channels](/channels)
- Advanced workflows and from source: [Setup](/start/setup)
