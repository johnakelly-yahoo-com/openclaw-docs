---
summary: "Step-by-step release checklist for npm + macOS app"
read_when:
  - Cutting a new npm release
  - Cutting a new macOS app release
  - Verifying metadata before publishing
---

# Release Checklist (npm + macOS)

Use `pnpm` (Node 22+) from the repo root. Keep the working tree clean before tagging/publishing.

## Operator trigger

When the operator says “release”, immediately do this preflight (no extra questions unless blocked):

- Read this doc and `docs/platforms/mac/release.md`.
- Load env from `~/.profile` and confirm `SPARKLE_PRIVATE_KEY_FILE` + App Store Connect vars are set (SPARKLE_PRIVATE_KEY_FILE should live in `~/.profile`).
- Use Sparkle keys from `~/Library/CloudStorage/Dropbox/Backup/Sparkle` if needed.

1. **Version & metadata**

- [ ] Bump `package.json` version (e.g., `2026.1.29`).
- [ ] Run `pnpm plugins:sync` to align extension package versions + changelogs.
- [ ] Update CLI/version strings: [`src/cli/program.ts`](https://github.com/openclaw/openclaw/blob/main/src/cli/program.ts) and the Baileys user agent in [`src/provider-web.ts`](https://github.com/openclaw/openclaw/blob/main/src/provider-web.ts).
- [ ] Confirm package metadata (name, description, repository, keywords, license) and `bin` map points to [`openclaw.mjs`](https://github.com/openclaw/openclaw/blob/main/openclaw.mjs) for `openclaw`.
- [ ] If dependencies changed, run `pnpm install` so `pnpm-lock.yaml` is current.

2. **Build & artifacts**

- [ ] If A2UI inputs changed, run `pnpm canvas:a2ui:bundle` and commit any updated [`src/canvas-host/a2ui/a2ui.bundle.js`](https://github.com/openclaw/openclaw/blob/main/src/canvas-host/a2ui/a2ui.bundle.js).
- [ ] `pnpm run build` (regenerates `dist/`).
- [ ] Verify npm package `files` includes all required `dist/*` folders (notably `dist/node-host/**` and `dist/acp/**` for headless node + ACP CLI).
- [ ] Confirm `dist/build-info.json` exists and includes the expected `commit` hash (CLI banner uses this for npm installs).
- [ ] Optional: `npm pack --pack-destination /tmp` after the build; inspect the tarball contents and keep it handy for the GitHub release (do **not** commit it).

3. **Changelog & docs**

- [ ] `CHANGELOG.md` ni foydalanuvchiga ko‘rinadigan asosiy yangiliklar bilan yangilang (agar yo‘q bo‘lsa, fayl yarating); yozuvlar versiya bo‘yicha qat’iy ravishda kamayish tartibida bo‘lsin.
- [ ] README dagi misollar/flaglar joriy CLI xatti-harakatiga mos kelishini ta’minlang (ayniqsa yangi buyruqlar yoki opsiyalar).

4. **Tekshiruv**

- [ ] `pnpm build`
- [ ] `pnpm check`
- [ ] `pnpm test` (`pnpm test:coverage` agar qamrov chiqishi kerak bo‘lsa)
- [ ] `pnpm release:check` (npm pack tarkibini tekshiradi)
- [ ] `OPENCLAW_INSTALL_SMOKE_SKIP_NONROOT=1 pnpm test:install:smoke` (Docker o‘rnatish smoke testi, tezkor yo‘l; relizdan oldin majburiy)
  - Agar darhol oldingi npm relizi ma’lum darajada buzilgan bo‘lsa, preinstall bosqichi uchun `OPENCLAW_INSTALL_SMOKE_PREVIOUS=<oxirgi-yaxshi-versiya>` yoki `OPENCLAW_INSTALL_SMOKE_SKIP_PREVIOUS=1` ni o‘rnating.
- [ ] (Ixtiyoriy) To‘liq installer smoke (non-root + CLI qamrovini qo‘shadi): `pnpm test:install:smoke`
- [ ] (Ixtiyoriy) Installer E2E (Docker, `curl -fsSL https://openclaw.ai/install.sh | bash` ni ishga tushiradi, onboarding qiladi, so‘ng haqiqiy tool chaqiruvlarini bajaradi):
  - `pnpm test:install:e2e:openai` (`OPENAI_API_KEY` talab etiladi)
  - `pnpm test:install:e2e:anthropic` (`ANTHROPIC_API_KEY` talab etiladi)
  - `pnpm test:install:e2e` (ikkala kalit ham talab etiladi; ikkala provayderni ishga tushiradi)
- [ ] (Ixtiyoriy) Agar o‘zgarishlaringiz yuborish/qabul qilish yo‘llariga ta’sir qilsa, veb shlyuzni spot-tekshiring.

5. **macOS ilovasi (Sparkle)**

- [ ] macOS ilovasini build qiling va imzolang, so‘ng tarqatish uchun zip qiling.
- [ ] Sparkle appcast ni yarating (HTML eslatmalar [`scripts/make_appcast.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/make_appcast.sh) orqali) va `appcast.xml` ni yangilang.
- [ ] GitHub reliziga biriktirish uchun ilova zipi (va ixtiyoriy dSYM zipi) ni tayyor holda saqlang.
- [ ] Aniq buyruqlar va zarur muhit o‘zgaruvchilari uchun [macOS release](/platforms/mac/release) ga amal qiling.
  - `APP_BUILD` raqamli va monoton bo‘lishi shart (`-beta` yo‘q), shunda Sparkle versiyalarni to‘g‘ri solishtiradi.
  - Agar notarizatsiya qilinsa, App Store Connect API muhit o‘zgaruvchilaridan yaratilgan `openclaw-notary` keychain profilidan foydalaning (qarang: [macOS release](/platforms/mac/release)).

6. **Nashr etish (npm)**

- [ ] Git holati toza ekanini tasdiqlang; kerak bo‘lsa commit va push qiling.
- [ ] Kerak bo‘lsa `npm login` (2FA ni tekshiring).
- [ ] `npm publish --access public` (pre-relizlar uchun `--tag beta` dan foydalaning).
- [ ] Registrni tekshiring: `npm view openclaw version`, `npm view openclaw dist-tags`, va `npx -y openclaw@X.Y.Z --version` (yoki `--help`).

### Nosozliklarni bartaraf etish (2.0.0-beta2 relizidan eslatmalar)

- **npm pack/publish osilib qoladi yoki juda katta tarball hosil qiladi**: `dist/OpenClaw.app` ichidagi macOS ilova bundle’i (va reliz ziplar) paketga qo‘shilib ketadi. `package.json` dagi `files` orqali nashr tarkibini whitelist qilish bilan tuzating (dist quyi kataloglari, docs, skills ni kiriting; app bundle’larni chiqarib tashlang). `npm pack --dry-run` bilan `dist/OpenClaw.app` ro‘yxatda yo‘qligini tasdiqlang.
- **dist-tags uchun npm auth web loop**: OTP so‘rovi olish uchun legacy auth dan foydalaning:
  - `NPM_CONFIG_AUTH_TYPE=legacy npm dist-tag add openclaw@X.Y.Z latest`
- **`npx` tekshiruvi `ECOMPROMISED: Lock compromised` bilan muvaffaqiyatsiz**: yangi kesh bilan qayta urinib ko‘ring:
  - `NPM_CONFIG_CACHE=/tmp/npm-cache-$(date +%s) npx -y openclaw@X.Y.Z --version`
- **Kechikkan tuzatishdan so‘ng tagni qayta yo‘naltirish kerak**: tagni majburan yangilang va push qiling, so‘ng GitHub reliz aktivlari hanuz mos ekanini tekshiring:
  - `git tag -f vX.Y.Z && git push -f origin vX.Y.Z`

7. **GitHub relizi + appcast**

- [ ] Tag qo‘ying va push qiling: `git tag vX.Y.Z && git push origin vX.Y.Z` (yoki `git push --tags`).
- [ ] `vX.Y.Z` uchun GitHub relizini yarating/yangilang, **sarlavha `openclaw X.Y.Z`** bo‘lsin (faqat tag emas); body’da ushbu versiya uchun **to‘liq** changelog bo‘limi (Highlights + Changes + Fixes) inline bo‘lishi kerak (yalang‘och havolalarsiz) va **sarlavha body ichida takrorlanmasin**.
- [ ] Artefaktlarni biriktiring: `npm pack` tarball (ixtiyoriy), `OpenClaw-X.Y.Z.zip`, va `OpenClaw-X.Y.Z.dSYM.zip` (agar yaratilgan bo‘lsa).
- [ ] Yangilangan `appcast.xml` ni commit qiling va push qiling (Sparkle feed’lar main’dan olinadi).
- [ ] Toza vaqtinchalik katalogdan (hech qanday `package.json`siz) `npx -y openclaw@X.Y.Z send --help` ni ishga tushirib, o‘rnatish/CLI entrypoint’lar ishlashini tasdiqlang.
- [ ] Reliz eslatmalarini e’lon qiling/ulashing.

## Plagin nashri doirasi (npm)

Biz faqat **mavjud npm plaginlari**ni `@openclaw/*` doirasi ostida nashr qilamiz. npm’da bo‘lmagan, lekin bundle qilingan plaginlar **faqat disk-daraxt** holatida qoladi (baribir `extensions/**` ichida yetkaziladi).

Ro‘yxatni aniqlash jarayoni:

1. `npm search @openclaw --json` va paket nomlarini yozib oling.
2. `extensions/*/package.json` dagi nomlar bilan solishtiring.
3. Publish only the **intersection** (already on npm).

Current npm plugin list (update as needed):

- @openclaw/bluebubbles
- @openclaw/diagnostics-otel
- @openclaw/discord
- @openclaw/feishu
- @openclaw/lobster
- @openclaw/matrix
- @openclaw/msteams
- @openclaw/nextcloud-talk
- @openclaw/nostr
- @openclaw/voice-call
- @openclaw/zalo
- @openclaw/zalouser

Release notes must also call out **new optional bundled plugins** that are **not
on by default** (example: `tlon`).
