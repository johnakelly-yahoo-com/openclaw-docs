---
summary: "Integratsiyalashgan brauzer boshqaruv xizmati + action buyruqlari"
read_when:
  - Agent tomonidan boshqariladigan brauzer avtomatlashtirishini qo‘shish
  - Nega openclaw sizning Chrome’ingizga xalaqit berayotganini diagnostika qilish
  - macOS ilovasida brauzer sozlamalari va hayot siklini amalga oshirish
title: "Brauzer (OpenClaw tomonidan boshqariladi)"
---

# Brauzer (openclaw tomonidan boshqariladi)

OpenClaw agent boshqaradigan **maxsus Chrome/Brave/Edge/Chromium profilini** ishga tushirishi mumkin.
U shaxsiy brauzeringizdan ajratilgan va Gateway ichidagi kichik lokal boshqaruv xizmati orqali (faqat loopback) boshqariladi.

Boshlovchilar uchun ko‘rinish:

- Buni **agentlar uchun alohida brauzer** deb tasavvur qiling.
- `openclaw` profili shaxsiy brauzer profilingizga **tegmaydi**.
- Agent **xavfsiz muhitda** tablarni ochishi, sahifalarni o‘qishi, bosishi va matn kiritishi mumkin.
- Standart `chrome` profili **tizimdagi standart Chromium brauzeri**dan kengaytma relayi orqali foydalanadi; izolyatsiyalangan boshqariladigan brauzer uchun `openclaw` ga o‘ting.

## Nimalarga ega bo‘lasiz

- **openclaw** nomli alohida brauzer profili (standartda to‘q sariq aksent).
- Deterministik tab boshqaruvi (ro‘yxatlash/ochish/fokuslash/yopish).
- Agent harakatlari (bosish/kiritish/sudrash/tanlash), snapshotlar, skrinshotlar, PDFlar.
- Ixtiyoriy ko‘p-profilli qo‘llab-quvvatlash (`openclaw`, `work`, `remote`, ...).

Bu brauzer **kundalik foydalanish uchun emas**. Bu agent avtomatlashtirish va tekshirish uchun xavfsiz, izolyatsiyalangan muhit.

## Tezkor boshlash

```bash
openclaw browser --browser-profile openclaw status
openclaw browser --browser-profile openclaw start
openclaw browser --browser-profile openclaw open https://example.com
openclaw browser --browser-profile openclaw snapshot
```

Agar “Browser disabled” xabarini ko‘rsangiz, konfiguratsiyada (quyida qarang) yoqing va Gateway’ni qayta ishga tushiring.

## Profillar: `openclaw` va `chrome`

- `openclaw`: boshqariladigan, izolyatsiyalangan brauzer (kengaytma talab qilinmaydi).
- `chrome`: **tizim brauzeringiz**ga kengaytma relayi (OpenClaw kengaytmasi tabga ulangan bo‘lishi kerak).

Agar boshqariladigan rejimni standart qilishni xohlasangiz, `browser.defaultProfile: "openclaw"` ni sozlang.

## Konfiguratsiya

12. Brauzer sozlamalari `~/.openclaw/openclaw.json` da joylashgan.

```json5
{
  browser: {
    enabled: true, // default: true
    // cdpUrl: "http://127.0.0.1:18792", // legacy single-profile override
    remoteCdpTimeoutMs: 1500, // remote CDP HTTP timeout (ms)
    remoteCdpHandshakeTimeoutMs: 3000, // remote CDP WebSocket handshake timeout (ms)
    defaultProfile: "chrome",
    color: "#FF4500",
    headless: false,
    noSandbox: false,
    attachOnly: false,
    executablePath: "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    profiles: {
      openclaw: { cdpPort: 18800, color: "#FF4500" },
      work: { cdpPort: 18801, color: "#0066CC" },
      remote: { cdpUrl: "http://10.0.0.42:9222", color: "#00AA00" },
    },
  },
}
```

Notes:

- The browser control service binds to loopback on a port derived from `gateway.port`
  (default: `18791`, which is gateway + 2). The relay uses the next port (`18792`).
- If you override the Gateway port (`gateway.port` or `OPENCLAW_GATEWAY_PORT`),
  the derived browser ports shift to stay in the same “family”.
- `cdpUrl` defaults to the relay port when unset.
- `remoteCdpTimeoutMs` applies to remote (non-loopback) CDP reachability checks.
- `remoteCdpHandshakeTimeoutMs` applies to remote CDP WebSocket reachability checks.
- `attachOnly: true` means “never launch a local browser; only attach if it is already running.”
- `color` + per-profile `color` tint the browser UI so you can see which profile is active.
- Default profile is `chrome` (extension relay). Use `defaultProfile: "openclaw"` for the managed browser.
- Auto-detect order: system default browser if Chromium-based; otherwise Chrome → Brave → Edge → Chromium → Chrome Canary.
- Local `openclaw` profiles auto-assign `cdpPort`/`cdpUrl` — set those only for remote CDP.

## Use Brave (or another Chromium-based browser)

If your **system default** browser is Chromium-based (Chrome/Brave/Edge/etc),
OpenClaw uses it automatically. Set `browser.executablePath` to override
auto-detection:

CLI example:

```bash
openclaw config set browser.executablePath "/usr/bin/google-chrome"
```

```json5
// macOS
{
  browser: {
    executablePath: "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
  }
}

// Windows
{
  browser: {
    executablePath: "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
  }
}

// Linux
{
  browser: {
    executablePath: "/usr/bin/brave-browser"
  }
}
```

## Local vs remote control

- **Local control (default):** the Gateway starts the loopback control service and can launch a local browser.
- **Remote control (node host):** run a node host on the machine that has the browser; the Gateway proxies browser actions to it.
- **Remote CDP:** set `browser.profiles.<name>.cdpUrl` (or `browser.cdpUrl`) to
  attach to a remote Chromium-based browser. In this case, OpenClaw will not launch a local browser.

Remote CDP URLs can include auth:

- Query tokens (e.g., `https://provider.example?token=<token>`)
- HTTP Basic auth (e.g., `https://user:pass@provider.example`)

OpenClaw preserves the auth when calling `/json/*` endpoints and when connecting
to the CDP WebSocket. Prefer environment variables or secrets managers for
tokens instead of committing them to config files.

## Node browser proxy (zero-config default)

If you run a **node host** on the machine that has your browser, OpenClaw can
auto-route browser tool calls to that node without any extra browser config.
This is the default path for remote gateways.

Notes:

- The node host exposes its local browser control server via a **proxy command**.
- Profiles come from the node’s own `browser.profiles` config (same as local).
- Disable if you don’t want it:
  - On the node: `nodeHost.browserProxy.enabled=false`
  - On the gateway: `gateway.nodes.browser.mode="off"`

## Browserless (hosted remote CDP)

[Browserless](https://browserless.io) is a hosted Chromium service that exposes
CDP endpoints over HTTPS. You can point a OpenClaw browser profile at a
Browserless region endpoint and authenticate with your API key.

Example:

```json5
{
  browser: {
    enabled: true,
    defaultProfile: "browserless",
    remoteCdpTimeoutMs: 2000,
    remoteCdpHandshakeTimeoutMs: 4000,
    profiles: {
      browserless: {
        cdpUrl: "https://production-sfo.browserless.io?token=<BROWSERLESS_API_KEY>",
        color: "#00AA00",
      },
    },
  },
}
```

Notes:

- Replace `<BROWSERLESS_API_KEY>` with your real Browserless token.
- Choose the region endpoint that matches your Browserless account (see their docs).

## 13. Xavfsizlik

Key ideas:

- Browser control is loopback-only; access flows through the Gateway’s auth or node pairing.
- Keep the Gateway and any node hosts on a private network (Tailscale); avoid public exposure.
- Treat remote CDP URLs/tokens as secrets; prefer env vars or a secrets manager.

Remote CDP tips:

- Prefer HTTPS endpoints and short-lived tokens where possible.
- Avoid embedding long-lived tokens directly in config files.

## Profiles (multi-browser)

OpenClaw supports multiple named profiles (routing configs). Profiles can be:

- **openclaw-managed**: a dedicated Chromium-based browser instance with its own user data directory + CDP port
- **remote**: an explicit CDP URL (Chromium-based browser running elsewhere)
- **extension relay**: your existing Chrome tab(s) via the local relay + Chrome extension

Defaults:

- The `openclaw` profile is auto-created if missing.
- The `chrome` profile is built-in for the Chrome extension relay (points at `http://127.0.0.1:18792` by default).
- Local CDP ports allocate from **18800–18899** by default.
- Deleting a profile moves its local data directory to Trash.

All control endpoints accept `?profile=<name>`; the CLI uses `--browser-profile`.

## Chrome extension relay (use your existing Chrome)

OpenClaw can also drive **your existing Chrome tabs** (no separate “openclaw” Chrome instance) via a local CDP relay + a Chrome extension.

Full guide: [Chrome extension](/tools/chrome-extension)

Flow:

- The Gateway runs locally (same machine) or a node host runs on the browser machine.
- A local **relay server** listens at a loopback `cdpUrl` (default: `http://127.0.0.1:18792`).
- You click the **OpenClaw Browser Relay** extension icon on a tab to attach (it does not auto-attach).
- The agent controls that tab via the normal `browser` tool, by selecting the right profile.

If the Gateway runs elsewhere, run a node host on the browser machine so the Gateway can proxy browser actions.

### Sandboxed sessions

If the agent session is sandboxed, the `browser` tool may default to `target="sandbox"` (sandbox browser).
Chrome extension relay takeover requires host browser control, so either:

- run the session unsandboxed, or
- set `agents.defaults.sandbox.browser.allowHostControl: true` and use `target="host"` when calling the tool.

### Setup

1. Load the extension (dev/unpacked):

```bash
openclaw browser extension install
```

- Chrome → `chrome://extensions` → enable “Developer mode”
- “Load unpacked” → select the directory printed by `openclaw browser extension path`
- Pin the extension, then click it on the tab you want to control (badge shows `ON`).

2. Use it:

- CLI: `openclaw browser --browser-profile chrome tabs`
- Agent tool: `browser` with `profile="chrome"`

Optional: if you want a different name or relay port, create your own profile:

```bash
openclaw browser create-profile \
  --name my-chrome \
  --driver extension \
  --cdp-url http://127.0.0.1:18792 \
  --color "#00AA00"
```

Notes:

- This mode relies on Playwright-on-CDP for most operations (screenshots/snapshots/actions).
- Detach by clicking the extension icon again.

## Isolation guarantees

- **Dedicated user data dir**: never touches your personal browser profile.
- **Dedicated ports**: avoids `9222` to prevent collisions with dev workflows.
- **Deterministic tab control**: target tabs by `targetId`, not “last tab”.

## Browser selection

When launching locally, OpenClaw picks the first available:

1. Chrome
2. Brave
3. Edge
4. Chromium
5. Chrome Canary

You can override with `browser.executablePath`.

Platforms:

- macOS: checks `/Applications` and `~/Applications`.
- Linux: looks for `google-chrome`, `brave`, `microsoft-edge`, `chromium`, etc.
- Windows: checks common install locations.

## Control API (optional)

For local integrations only, the Gateway exposes a small loopback HTTP API:

- Status/start/stop: `GET /`, `POST /start`, `POST /stop`
- Tabs: `GET /tabs`, `POST /tabs/open`, `POST /tabs/focus`, `DELETE /tabs/:targetId`
- Snapshot/screenshot: `GET /snapshot`, `POST /screenshot`
- Actions: `POST /navigate`, `POST /act`
- Hooks: `POST /hooks/file-chooser`, `POST /hooks/dialog`
- Downloads: `POST /download`, `POST /wait/download`
- Debugging: `GET /console`, `POST /pdf`
- Debugging: `GET /errors`, `GET /requests`, `POST /trace/start`, `POST /trace/stop`, `POST /highlight`
- Network: `POST /response/body`
- State: `GET /cookies`, `POST /cookies/set`, `POST /cookies/clear`
- State: `GET /storage/:kind`, `POST /storage/:kind/set`, `POST /storage/:kind/clear`
- Settings: `POST /set/offline`, `POST /set/headers`, `POST /set/credentials`, `POST /set/geolocation`, `POST /set/media`, `POST /set/timezone`, `POST /set/locale`, `POST /set/device`

All endpoints accept `?profile=<name>`.

### Playwright requirement

Some features (navigate/act/AI snapshot/role snapshot, element screenshots, PDF) require
Playwright. If Playwright isn’t installed, those endpoints return a clear 501
error. ARIA snapshots and basic screenshots still work for openclaw-managed Chrome.
For the Chrome extension relay driver, ARIA snapshots and screenshots require Playwright.

If you see `Playwright is not available in this gateway build`, install the full
Playwright package (not `playwright-core`) and restart the gateway, or reinstall
OpenClaw with browser support.

#### Docker Playwright install

If your Gateway runs in Docker, avoid `npx playwright` (npm override conflicts).
Use the bundled CLI instead:

```bash
docker compose run --rm openclaw-cli \
  node /app/node_modules/playwright-core/cli.js install chromium
```

To persist browser downloads, set `PLAYWRIGHT_BROWSERS_PATH` (for example,
`/home/node/.cache/ms-playwright`) and make sure `/home/node` is persisted via
`OPENCLAW_HOME_VOLUME` or a bind mount. See [Docker](/install/docker).

## How it works (internal)

High-level flow:

- A small **control server** accepts HTTP requests.
- It connects to Chromium-based browsers (Chrome/Brave/Edge/Chromium) via **CDP**.
- For advanced actions (click/type/snapshot/PDF), it uses **Playwright** on top
  of CDP.
- When Playwright is missing, only non-Playwright operations are available.

This design keeps the agent on a stable, deterministic interface while letting
you swap local/remote browsers and profiles.

## CLI quick reference

All commands accept `--browser-profile <name>` to target a specific profile.
All commands also accept `--json` for machine-readable output (stable payloads).

Basics:

- `openclaw browser status`
- 14. `openclaw browser start`
- `openclaw browser stop`
- `openclaw browser tabs`
- 15. `openclaw browser tab`
- 16. `openclaw browser tab new`
- 17. `openclaw browser tab select 2`
- `openclaw browser tab close 2`
- 18. `openclaw browser open https://example.com`
- `openclaw browser focus abcd1234`
- `openclaw browser close abcd1234`

Inspection:

- `openclaw browser screenshot`
- 19. `openclaw browser screenshot --full-page`
- `openclaw browser screenshot --ref 12`
- 20. `openclaw browser screenshot --ref e12`
- `openclaw browser snapshot`
- `openclaw browser snapshot --format aria --limit 200`
- `openclaw browser snapshot --interactive --compact --depth 6`
- `openclaw browser snapshot --efficient`
- `openclaw browser snapshot --labels`
- `openclaw browser snapshot --selector "#main" --interactive`
- `openclaw browser snapshot --frame "iframe#main" --interactive`
- `openclaw browser console --level error`
- `openclaw browser errors --clear`
- `openclaw browser requests --filter api --clear`
- `openclaw browser pdf`
- `openclaw browser responsebody "**/api" --max-chars 5000`

Actions:

- `openclaw browser navigate https://example.com`
- `openclaw browser resize 1280 720`
- `openclaw browser click 12 --double`
- `openclaw browser click e12 --double`
- `openclaw browser type 23 "hello" --submit`
- `openclaw browser press Enter`
- `openclaw browser hover 44`
- `openclaw browser scrollintoview e12`
- `openclaw browser drag 10 11`
- `openclaw browser select 9 OptionA OptionB`
- `openclaw browser download e12 /tmp/report.pdf`
- `openclaw browser waitfordownload /tmp/report.pdf`
- `openclaw browser upload /tmp/file.pdf`
- `openclaw browser fill --fields '[{"ref":"1","type":"text","value":"Ada"}]'`
- `openclaw browser dialog --accept`
- `openclaw browser wait --text "Done"`
- `openclaw browser wait "#main" --url "**/dash" --load networkidle --fn "window.ready===true"`
- `openclaw browser evaluate --fn '(el) => el.textContent' --ref 7`
- `openclaw browser highlight e12`
- `openclaw browser trace start`
- `openclaw browser trace stop`

21. Holat:

- `openclaw browser cookies`
- `openclaw browser cookies set session abc123 --url "https://example.com"`
- `openclaw browser cookies clear`
- `openclaw browser storage local get`
- `openclaw browser storage local set theme dark`
- `openclaw browser storage session clear`
- `openclaw browser set offline on`
- `openclaw browser set headers --json '{"X-Debug":"1"}'`
- `openclaw browser set credentials user pass`
- `openclaw browser set credentials --clear`
- `openclaw browser set geo 37.7749 -122.4194 --origin "https://example.com"`
- `openclaw browser set geo --clear`
- `openclaw browser set media dark`
- 22. `openclaw browser set timezone America/New_York`
- `openclaw browser set locale en-US`
- `openclaw browser set device "iPhone 14"`

Eslatmalar:

- `upload` va `dialog` **qurollantiruvchi** chaqiruvlar; tanlovchi/dialogni ishga tushiradigan bosish/pressdan oldin ularni ishga tushiring.
- `upload` fayl kiritish maydonlarini `--input-ref` yoki `--element` orqali to‘g‘ridan-to‘g‘ri ham sozlashi mumkin.
- `snapshot`:
  - `--format ai` (Playwright o‘rnatilganida standart): raqamli referenslar (`aria-ref="<n>"`) bilan AI snapshotni qaytaradi.
  - `--format aria`: accessibility daraxtini qaytaradi (referenslar yo‘q; faqat tekshirish uchun).
  - `--efficient` (yoki `--mode efficient`): ixcham rol snapshot preseti (interaktiv + ixcham + chuqurlik + pastroq maxChars).
  - Standart konfiguratsiya (faqat tool/CLI): chaqiruvchi rejimni uzatmasa samarali snapshotlardan foydalanish uchun `browser.snapshotDefaults.mode: "efficient"` ni o‘rnating (qarang: [Gateway configuration](/gateway/configuration#browser-openclaw-managed-browser)).
  - Rol snapshot parametrlari (`--interactive`, `--compact`, `--depth`, `--selector`) `ref=e12` kabi referenslar bilan rolga asoslangan snapshotni majburiy qiladi.
  - `--frame "<iframe selector>"` rol snapshotlarini iframe ichida cheklaydi ( `e12` kabi rol referenslari bilan juftlashadi).
  - `--interactive` interaktiv elementlarning tekis, tanlash oson ro‘yxatini chiqaradi (harakatlarni boshqarish uchun eng yaxshisi).
  - 23. `--labels` faqat viewport uchun overlay qilingan ref yorliqlari bilan skrinshot qo‘shadi (`MEDIA:<path>` ni chiqaradi).
- `click`/`type`/va boshqalar `snapshot` dan olingan `ref` ni talab qiladi (raqamli `12` yoki rol referensi `e12`).
  Harakatlar uchun CSS selektorlar ataylab qo‘llab-quvvatlanmaydi.

## Snapshotlar va referenslar

OpenClaw ikki xil “snapshot” uslubini qo‘llab-quvvatlaydi:

- **AI snapshot (raqamli referenslar)**: `openclaw browser snapshot` (standart; `--format ai`)
  - Chiqish: raqamli referenslarni o‘z ichiga olgan matnli snapshot.
  - Harakatlar: `openclaw browser click 12`, `openclaw browser type 23 "hello"`.
  - Ichki tomondan, referens Playwright’ning `aria-ref` orqali aniqlanadi.

- **Rol snapshot ( `e12` kabi rol referenslari)**: `openclaw browser snapshot --interactive` (yoki `--compact`, `--depth`, `--selector`, `--frame`)
  - Chiqish: `[ref=e12]` (va ixtiyoriy `[nth=1]`) bilan rolga asoslangan ro‘yxat/daraxt.
  - Harakatlar: `openclaw browser click e12`, `openclaw browser highlight e12`.
  - Ichki tomondan, referens `getByRole(...)` orqali aniqlanadi (takrorlar uchun `nth()` bilan).
  - Ustma-ust qo‘yilgan `e12` yorliqlari bilan ko‘rinish oynasi skrinshotini qo‘shish uchun `--labels` ni qo‘shing.

Referenslar xatti-harakati:

- Referenslar **navigatsiyalar orasida barqaror emas**; agar biror narsa ishlamasa, `snapshot` ni qayta ishga tushiring va yangi referensdan foydalaning.
- Agar rol snapshot `--frame` bilan olingan bo‘lsa, keyingi rol snapshotigacha rol referenslari o‘sha iframe doirasida qoladi.

## Kutish kuchaytmalari

Faqat vaqt/matn emas, ko‘proq narsalarni ham kutishingiz mumkin:

- URLni kutish (Playwright tomonidan qo‘llab-quvvatlanadigan globlar):
  - `openclaw browser wait --url "**/dash"`
- Yuklanish holatini kutish:
  - 1. `openclaw browser wait --load networkidle`
- 2. JS predikati bajarilishini kuting:
  - 3. `openclaw browser wait --fn "window.ready===true"`
- 4. Selektor ko‘rinadigan bo‘lishini kuting:
  - 5. `openclaw browser wait "#main"`

6. Bularni birlashtirish mumkin:

```bash
7. openclaw browser wait "#main" \
  --url "**/dash" \
  --load networkidle \
  --fn "window.ready===true" \
  --timeout-ms 15000
```

## 8. Ish jarayonlarini nosozlikdan o‘tkazish

9. Harakat muvaffaqiyatsiz bo‘lganda (masalan, “ko‘rinmaydi”, “qat’iy rejim buzilishi”, “ustini yopib qo‘yilgan”):

1. 10. `openclaw browser snapshot --interactive`
2. 11. `click <ref>` / `type <ref>` dan foydalaning (interaktiv rejimda rolga asoslangan ref’larni afzal ko‘ring)
3. 12. Agar baribir ishlamasa: Playwright nimani nishonga olayotganini ko‘rish uchun `openclaw browser highlight <ref>`
4. 13. Agar sahifa g‘alati tutsa:
   - 14. `openclaw browser errors --clear`
   - 15. `openclaw browser requests --filter api --clear`
5. 16. Chuqur nosozliklarni aniqlash uchun: treys yozib oling:
   - 17. `openclaw browser trace start`
   - 18. muammoni qayta yuzaga keltiring
   - 19. `openclaw browser trace stop` ( `TRACE:<path>` ni chiqaradi)

## 20) JSON chiqishi

21. `--json` skriptlash va tuzilmaviy vositalar uchun mo‘ljallangan.

22. Misollar:

```bash
23. openclaw browser status --json
openclaw browser snapshot --interactive --json
openclaw browser requests --filter api --json
openclaw browser cookies --json
```

24. JSON’dagi rol snapshotlari `refs` hamda kichik `stats` blokini (lines/chars/refs/interactive) o‘z ichiga oladi, shunda vositalar yuklama hajmi va zichligini baholay oladi.

## 25. Holat va muhit sozlamalari

26. Bular “saytni X kabi tutishga majbur qilish” ish jarayonlari uchun foydali:

- 27. Cookie’lar: `cookies`, `cookies set`, `cookies clear`
- 28. Saqlash: `storage local|session get|set|clear`
- 29. Oflayn: `set offline on|off`
- 30. Sarlavhalar: `set headers --json '{"X-Debug":"1"}'` (yoki `--clear`)
- 31. HTTP basic autentifikatsiya: `set credentials user pass` (yoki `--clear`)
- 32. Geolokatsiya: `set geo <lat> <lon> --origin "https://example.com"` (yoki `--clear`)
- 33. Media: `set media dark|light|no-preference|none`
- 34. Vaqt zonasi / til sozlamasi: `set timezone ...`, `set locale ...`
- 35. Qurilma / viewport:
  - 36. `set device "iPhone 14"` (Playwright qurilma presetlari)
  - 37. `set viewport 1280 720`

## 38. Xavfsizlik va maxfiylik

- 39. openclaw brauzer profili tizimga kirilgan sessiyalarni o‘z ichiga olishi mumkin; uni maxfiy deb hisoblang.
- 40. `browser act kind=evaluate` / `openclaw browser evaluate` va `wait --fn`
      sahifa kontekstida ixtiyoriy JavaScript’ni bajaradi. 41. Prompt injection buni boshqarishi mumkin. 42. Agar kerak bo‘lmasa, `browser.evaluateEnabled=false` bilan o‘chirib qo‘ying.
- 43. Login va anti-bot eslatmalari (X/Twitter va boshqalar) uchun [Browser login + X/Twitter posting](/tools/browser-login) ga qarang.
- 44. Gateway/node xostini yopiq saqlang (loopback yoki faqat tailnet).
- 45. Masofaviy CDP endpointlari kuchli; ularni tunnel qiling va himoyalang.

## 46. Nosozliklarni bartaraf etish

47. Linux’ga xos muammolar (ayniqsa snap Chromium) uchun
    [Browser troubleshooting](/tools/browser-linux-troubleshooting) ga qarang.

## 48. Agent vositalari + boshqaruv qanday ishlaydi

49. Agent brauzer avtomatlashtirish uchun **bitta vosita** oladi:

- 50. `browser` — status/start/stop/tabs/open/focus/close/snapshot/screenshot/navigate/act

1. Qanday xaritalanadi:

- 2. `browser snapshot` barqaror UI daraxtini qaytaradi (AI yoki ARIA).
- 3. `browser act` snapshotdagi `ref` ID’lardan foydalanib bosish/yozish/sudrash/tanlashni amalga oshiradi.
- 4. `browser screenshot` piksellarni ushlaydi (butun sahifa yoki element).
- 5. `browser` qabul qiladi:
  - 6. `profile` — nomlangan brauzer profilini tanlash uchun (openclaw, chrome yoki remote CDP).
  - 7. `target` (`sandbox` | `host` | `node`) — brauzer qayerda ishlashini tanlash uchun.
  - 8. Sandboxlangan sessiyalarda `target: "host"` ishlashi uchun `agents.defaults.sandbox.browser.allowHostControl=true` talab qilinadi.
  - 9. Agar `target` ko‘rsatilmasa: sandboxlangan sessiyalar sukut bo‘yicha `sandbox`, sandbox bo‘lmagan sessiyalar `host` bo‘ladi.
  - 10. Agar brauzerga qodir node ulangan bo‘lsa, asbob avtomatik ravishda unga yo‘naltirishi mumkin, agar siz `target="host"` yoki `target="node"` ni qat’iy belgilamasangiz.

11. Bu agentni deterministik qiladi va mo‘rt selektorlarning oldini oladi.
