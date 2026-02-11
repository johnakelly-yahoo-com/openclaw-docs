---
summary: "Clawnet refactor: unify network protocol, roles, auth, approvals, identity"
read_when:
  - Planning a unified network protocol for nodes + operator clients
  - Reworking approvals, pairing, TLS, and presence across devices
title: "Clawnet Refactor"
---

# Clawnet refactor (protocol + auth unification)

## Hi

Hi Peter — great direction; this unlocks simpler UX + stronger security.

## Purpose

Single, rigorous document for:

- Current state: protocols, flows, trust boundaries.
- Pain points: approvals, multi‑hop routing, UI duplication.
- Proposed new state: one protocol, scoped roles, unified auth/pairing, TLS pinning.
- Identity model: stable IDs + cute slugs.
- Migration plan, risks, open questions.

## Goals (from discussion)

- One protocol for all clients (mac app, CLI, iOS, Android, headless node).
- Every network participant authenticated + paired.
- Role clarity: nodes vs operators.
- Central approvals routed to where the user is.
- TLS encryption + optional pinning for all remote traffic.
- Minimal code duplication.
- Single machine should appear once (no UI/node duplicate entry).

## Non‑goals (explicit)

- Remove capability separation (still need least‑privilege).
- Expose full gateway control plane without scope checks.
- Make auth depend on human labels (slugs remain non‑security).

---

# Current state (as‑is)

## Two protocols

### 1. Gateway WebSocket (control plane)

- Full API surface: config, channels, models, sessions, agent runs, logs, nodes, etc.
- Default bind: loopback. Remote access via SSH/Tailscale.
- Auth: token/password via `connect`.
- No TLS pinning (relies on loopback/tunnel).
- Code:
  - `src/gateway/server/ws-connection/message-handler.ts`
  - `src/gateway/client.ts`
  - `docs/gateway/protocol.md`

### 2. Bridge (node transport)

- Narrow allowlist surface, node identity + pairing.
- JSONL over TCP; optional TLS + cert fingerprint pinning.
- TLS advertises fingerprint in discovery TXT.
- Code:
  - `src/infra/bridge/server/connection.ts`
  - `src/gateway/server-bridge.ts`
  - `src/node-host/bridge-client.ts`
  - `docs/gateway/bridge-protocol.md`

## Control plane clients today

- CLI → Gateway WS via `callGateway` (`src/gateway/call.ts`).
- macOS app UI → Gateway WS (`GatewayConnection`).
- Web Control UI → Gateway WS.
- ACP → Gateway WS.
- Browser control uses its own HTTP control server.

## Nodes today

- macOS app in node mode connects to Gateway bridge (`MacNodeBridgeSession`).
- iOS/Android apps connect to Gateway bridge.
- Pairing + per‑node token stored on gateway.

## Current approval flow (exec)

- Agent uses `system.run` via Gateway.
- Gateway invokes node over bridge.
- Node runtime decides approval.
- UI prompt shown by mac app (when node == mac app).
- Node returns `invoke-res` to Gateway.
- Multi‑hop, UI tied to node host.

## Presence + identity today

- Gateway presence entries from WS clients.
- Node presence entries from bridge.
- mac app can show two entries for same machine (UI + node).
- Node identity stored in pairing store; UI identity separate.

---

# Problems / pain points

- 1. Saqlab turilishi kerak bo‘lgan ikki protokol steki (WS + Bridge).
- 2. Masofaviy tugunlarda tasdiqlash: so‘rov foydalanuvchi joylashgan joyda emas, balki tugun xostida paydo bo‘ladi.
- 3. TLS pinning faqat bridge uchun mavjud; WS esa SSH/Tailscale’ga bog‘liq.
- 4. Identifikatsiya takrorlanishi: bir xil mashina bir nechta instansiya sifatida ko‘rinadi.
- 5. Noaniq rollar: UI + node + CLI imkoniyatlari aniq ajratilmagan.

---

# 6. Taklif etilayotgan yangi holat (Clawnet)

## 7. Bitta protokol, ikki rol

8. Rol + scope bilan yagona WS protokoli.

- 9. **Rol: node** (imkoniyatlar xosti)
- 10. **Rol: operator** (boshqaruv tekisligi)
- 11. Operator uchun ixtiyoriy **scope**:
  - 12. `operator.read` (holat + ko‘rish)
  - 13. `operator.write` (agentni ishga tushirish, yuborishlar)
  - 14. `operator.admin` (konfiguratsiya, kanallar, modellar)

### 15. Rol xatti-harakatlari

16. **Node**

- 17. Imkoniyatlarni ro‘yxatdan o‘tkazishi mumkin (`caps`, `commands`, ruxsatlar).
- 18. `invoke` buyruqlarini qabul qilishi mumkin (`system.run`, `camera.*`, `canvas.*`, `screen.record` va h.k.).
- 19. Hodisalarni yuborishi mumkin: `voice.transcript`, `agent.request`, `chat.subscribe`.
- 20. Konfiguratsiya/modellar/kanallar/sessiyalar/agent boshqaruv tekisligi API’larini chaqira olmaydi.

21. **Operator**

- 22. Scope bilan cheklangan to‘liq boshqaruv tekisligi API’si.
- 23. Barcha tasdiqlashlarni qabul qiladi.
- 24. OS darajasidagi amallarni bevosita bajarmaydi; ularni tugunlarga yo‘naltiradi.

### 25. Asosiy qoida

26. Rol qurilma bo‘yicha emas, ulanish bo‘yicha belgilanadi. 27. Bitta qurilma alohida-alohida holda ikkala rolni ham ochishi mumkin.

---

# 28. Yagona autentifikatsiya + juftlash

## 29. Mijoz identifikatsiyasi

30. Har bir mijoz taqdim etadi:

- 31. `deviceId` (barqaror, qurilma kalitidan hosil qilingan).
- 32. `displayName` (inson uchun qulay nom).
- 33. `role` + `scope` + `caps` + `commands`.

## 34. Juftlash jarayoni (yagona)

- 35. Mijoz autentifikatsiyasiz ulanadi.
- 36. Gateway ushbu `deviceId` uchun **juftlash so‘rovi** yaratadi.
- 37. Operator so‘rovni oladi; tasdiqlaydi yoki rad etadi.
- 38. Gateway quyidagilarga bog‘langan hisob ma’lumotlarini beradi:
  - 39. qurilmaning ochiq kaliti
  - 40. rol(lar)
  - 41. scope(lar)
  - 42. imkoniyatlar/buyruqlar
- 43. Mijoz tokenni saqlaydi va autentifikatsiyalangan holda qayta ulanadi.

## 44. Qurilmaga bog‘langan autentifikatsiya (bearer tokenni qayta ijro etishni oldini olish)

45. Afzal: qurilma kalit juftliklari.

- 46. Qurilma kalit juftligini bir marta yaratadi.
- 47. `deviceId = fingerprint(publicKey)`.
- 48. Gateway nonce yuboradi; qurilma imzolaydi; gateway tekshiradi.
- 49. Tokenlar satrga emas, ochiq kalitga (proof‑of‑possession) beriladi.

50. Muqobillar:

- mTLS (client certs): strongest, more ops complexity.
- Short‑lived bearer tokens only as a temporary phase (rotate + revoke early).

## Silent approval (SSH heuristic)

Define it precisely to avoid a weak link. Prefer one:

- **Local‑only**: auto‑pair when client connects via loopback/Unix socket.
- **Challenge via SSH**: gateway issues nonce; client proves SSH by fetching it.
- **Physical presence window**: after a local approval on gateway host UI, allow auto‑pair for a short window (e.g. 10 minutes).

Always log + record auto‑approvals.

---

# TLS everywhere (dev + prod)

## Reuse existing bridge TLS

Use current TLS runtime + fingerprint pinning:

- `src/infra/bridge/server/tls.ts`
- fingerprint verification logic in `src/node-host/bridge-client.ts`

## Apply to WS

- WS server supports TLS with same cert/key + fingerprint.
- WS clients can pin fingerprint (optional).
- Discovery advertises TLS + fingerprint for all endpoints.
  - Discovery is locator hints only; never a trust anchor.

## Why

- Reduce reliance on SSH/Tailscale for confidentiality.
- Make remote mobile connections safe by default.

---

# Approvals redesign (centralized)

## Current

Approval happens on node host (mac app node runtime). Prompt appears where node runs.

## Proposed

Approval is **gateway‑hosted**, UI delivered to operator clients.

### New flow

1. Gateway receives `system.run` intent (agent).
2. Gateway creates approval record: `approval.requested`.
3. Operator UI(s) show prompt.
4. Approval decision sent to gateway: `approval.resolve`.
5. Gateway invokes node command if approved.
6. Node executes, returns `invoke-res`.

### Approval semantics (hardening)

- Broadcast to all operators; only the active UI shows a modal (others get a toast).
- First resolution wins; gateway rejects subsequent resolves as already settled.
- Default timeout: deny after N seconds (e.g. 60s), log reason.
- Resolution requires `operator.approvals` scope.

## Benefits

- Prompt appears where user is (mac/phone).
- Consistent approvals for remote nodes.
- Node runtime stays headless; no UI dependency.

---

# Role clarity examples

## iPhone app

- **Node role** for: mic, camera, voice chat, location, push‑to‑talk.
- Optional **operator.read** for status and chat view.
- Optional **operator.write/admin** only when explicitly enabled.

## macOS app

- 1. Operator roli sukut bo‘yicha (boshqaruv UI).
- 2. “Mac node” yoqilganda Node roli (system.run, screen, camera).
- 3. Ikkala ulanish uchun bir xil deviceId → UI’da birlashtirilgan yozuv.

## 4. CLI

- 5. Operator roli har doim.
- 6. Scope subbuyruqdan kelib chiqadi:
  - 7. `status`, `logs` → o‘qish
  - 8. `agent`, `message` → yozish
  - 9. `config`, `channels` → admin
  - 10. tasdiqlashlar + juftlash → `operator.approvals` / `operator.pairing`

---

# 11. Identifikatsiya + sluglar

## 12. Barqaror ID

13. Autentifikatsiya uchun talab qilinadi; hech qachon o‘zgarmaydi.
14. Afzal:

- 15. Kalit juftligi fingerprinti (ochiq kalit xeshi).

## 16. Yoqimli slug (omar mavzusida)

17. Faqat inson uchun yorliq.

- 18. Misol: `scarlet-claw`, `saltwave`, `mantis-pinch`.
- 19. Gateway reyestrida saqlanadi, tahrirlash mumkin.
- 20. To‘qnashuvni hal qilish: `-2`, `-3`.

## 21. UI’da guruhlash

22. Rollar bo‘yicha bir xil `deviceId` → bitta “Instance” qatori:

- 23. Belgilar: `operator`, `node`.
- 24. Imkoniyatlar + oxirgi ko‘rilgan vaqtni ko‘rsatadi.

---

# 25. Migratsiya strategiyasi

## 26. 0-bosqich: Hujjatlash + moslashtirish

- 27. Ushbu hujjatni nashr qilish.
- 28. Barcha protokol chaqiriqlari + tasdiqlash oqimlarini inventarizatsiya qilish.

## 29. 1-bosqich: WS’ga rollar/scope’larni qo‘shish

- 30. `connect` parametrlarini `role`, `scope`, `deviceId` bilan kengaytirish.
- 31. Node roli uchun allowlist cheklovini qo‘shish.

## 32. 2-bosqich: Moslik ko‘prigi

- 33. Ko‘prikni ishlashda qoldirish.
- 34. Parallel ravishda WS’da node qo‘llab-quvvatlashini qo‘shish.
- 35. Funksiyalarni konfiguratsiya flagi ortida yopish.

## 36. 3-bosqich: Markaziy tasdiqlashlar

- Add approval request + resolve events in WS.
- 38. Mac ilova UI’sini so‘rash + javob berishga yangilash.
- 39. Node runtime UI so‘rashni to‘xtatadi.

## 40. 4-bosqich: TLS’ni birxillashtirish

- 41. WS uchun TLS konfiguratsiyasini ko‘prik TLS runtime’idan foydalanib qo‘shish.
- 42. Mijozlarga pinning qo‘shish.

## 43. 5-bosqich: Ko‘prikni bekor qilish

- 44. iOS/Android/mac node’ni WS’ga ko‘chirish.
- 45. Barqarorlashguncha ko‘prikni zaxira sifatida qoldirish; keyin olib tashlash.

## 46. 6-bosqich: Qurilmaga bog‘langan autentifikatsiya

- 47. Barcha lokal bo‘lmagan ulanishlar uchun kalitga asoslangan identifikatsiyani talab qilish.
- 48. Bekor qilish + aylantirish UI’sini qo‘shish.

---

# 49. Xavfsizlik eslatmalari

- Role/allowlist enforced at gateway boundary.
- Hech bir mijoz operator scope bo‘lmasdan “to‘liq” API olmaydi.
- Barcha ulanishlar uchun juftlash (pairing) talab qilinadi.
- TLS + pinning mobil qurilmalarda MITM xavfini kamaytiradi.
- SSH jim tasdiqlash — qulaylik; baribir yozib boriladi va bekor qilinishi mumkin.
- Discovery hech qachon ishonch tayanchi emas.
- Capability da’volari platforma/tur bo‘yicha server allowlistlari bilan tekshiriladi.

# Streaming + katta payloadlar (node media)

Kichik xabarlar uchun WS control plane yetarli, ammo node’lar yana quyidagilarni ham bajaradi:

- kamera kliplari
- ekran yozuvlari
- audio oqimlari

Variantlar:

1. WS binary freymlar + bo‘laklash (chunking) + backpressure qoidalari.
2. Alohida streaming endpoint (baribir TLS + auth).
3. Media og‘ir buyruqlar uchun bridge’ni uzoqroq saqlash, oxirida migratsiya qilish.

Drift bo‘lmasligi uchun implementatsiyadan oldin bittasini tanlang.

# Capability + buyruq siyosati

- Node xabar qilgan capability/buyruqlar **da’vo** sifatida ko‘riladi.
- Gateway platforma bo‘yicha allowlistlarni majburiy qo‘llaydi.
- Har qanday yangi buyruq operator tasdig‘i yoki aniq allowlist o‘zgarishini talab qiladi.
- O‘zgarishlarni vaqt belgisi bilan audit qiling.

# Audit + rate limiting

- Log qiling: pairing so‘rovlari, tasdiqlashlar/rad etishlar, token berish/aylantirish/bekor qilish.
- Pairing spamini va tasdiqlash promptlarini rate‑limit qiling.

# Protokol gigiyenasi

- Aniq protokol versiyasi + xato kodlari.
- Reconnect qoidalari + heartbeat siyosati.
- Presence TTL va last‑seen semantikasi.

---

# Ochiq savollar

1. Ikkala rolni ham bajarayotgan bitta qurilma: token modeli
   - Har bir rol uchun alohida tokenlarni tavsiya etamiz (node vs operator).
   - Bir xil deviceId; turli scopelar; aniqroq bekor qilish.

2. Operator scope granularligi
   - read/write/admin + approvals + pairing (minimal yetarli).
   - Keyinroq per‑feature scopelarni ko‘rib chiqing.

3. Token aylantirish + bekor qilish UX
   - Rol o‘zgarganda avtomatik aylantirish.
   - deviceId + rol bo‘yicha bekor qilish uchun UI.

4. Discovery
   - Joriy Bonjour TXT’ni WS TLS fingerprint + rol ishoralarini qo‘shib kengaytirish.
   - Faqat joylashuv ishoralari sifatida ko‘ring.

5. Tarmoqlararo tasdiqlash
   - Barcha operator mijozlariga broadcast; faol UI modal ko‘rsatadi.
   - Birinchi javob yutadi; gateway atomiklikni ta’minlaydi.

---

# Xulosa (TL;DR)

- Bugun: WS control plane + Bridge node transport.
- Muammo: tasdiqlashlar + takrorlanish + ikki stack.
- Taklif: aniq rollar + scopelar bilan bitta WS protokoli, yagona pairing + TLS pinning, gateway‑hosted tasdiqlashlar, barqaror device ID’lar + yoqimli sluglar.
- Natija: soddaroq UX, kuchliroq xavfsizlik, kamroq takrorlanish, mobil marshrutlash yaxshiroq.
