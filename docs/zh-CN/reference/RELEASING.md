---
summary: "26. npm + macOS 应用的逐步发布清单"
read_when:
  - 27. 发布新的 npm 版本
  - 28. 发布新的 macOS 应用版本
  - 29. 发布前验证元数据
---

# 30. 发布清单（npm + macOS）

31. 在仓库根目录使用 `pnpm`（Node 22+）。 32. 在打标签/发布前保持工作区干净。

## 33. 操作员触发器

34. 当操作员说“release”时，立即执行以下预检（除非被阻塞，否则不要提出额外问题）：

- 35. 阅读本文档以及 `docs/platforms/mac/release.md`。
- 36. 从 `~/.profile` 加载环境变量，并确认已设置 `SPARKLE_PRIVATE_KEY_FILE` 和 App Store Connect 相关变量（`SPARKLE_PRIVATE_KEY_FILE` 应位于 `~/.profile`）。
- 37. 如有需要，使用位于 `~/Library/CloudStorage/Dropbox/Backup/Sparkle` 的 Sparkle 密钥。

1. 38. **版本与元数据**

- [ ] Bump `package.json` version (e.g., `2026.1.29`).
- [ ] 40. 运行 `pnpm plugins:sync` 以对齐扩展包版本和更新日志。
- [ ] 41. 更新 CLI/版本字符串：[`src/cli/program.ts`](https://github.com/openclaw/openclaw/blob/main/src/cli/program.ts) 以及 [`src/provider-web.ts`](https://github.com/openclaw/openclaw/blob/main/src/provider-web.ts) 中的 Baileys 用户代理。
- [ ] 42. 确认包元数据（名称、描述、仓库、关键词、许可证），并确保 `bin` 映射指向 [`openclaw.mjs`](https://github.com/openclaw/openclaw/blob/main/openclaw.mjs) 以供 `openclaw` 使用。
- [ ] 43. 如果依赖发生变化，运行 `pnpm install` 以确保 `pnpm-lock.yaml` 为最新。

2. 44. **构建与产物**

- [ ] 45) 如果 A2UI 输入发生变化，运行 `pnpm canvas:a2ui:bundle`，并提交任何更新的 [`src/canvas-host/a2ui/a2ui.bundle.js`](https://github.com/openclaw/openclaw/blob/main/src/canvas-host/a2ui/a2ui.bundle.js)。
- [ ] 46. `pnpm run build`（重新生成 `dist/`）。
- [ ] 47. 验证 npm 包的 `files` 包含所有必需的 `dist/*` 文件夹（尤其是用于无头 node + ACP CLI 的 `dist/node-host/**` 和 `dist/acp/**`）。
- [ ] 48. 确认存在 `dist/build-info.json`，并且其中包含预期的 `commit` 哈希（CLI 横幅在 npm 安装时会使用它）。
- [ ] 49. 可选：构建后运行 `npm pack --pack-destination /tmp`；检查生成的 tarball 内容，并保留以用于 GitHub 发布（**不要**提交它）。

3. 50. **更新日志与文档**

- [ ] Update `CHANGELOG.md` with user-facing highlights (create the file if missing); keep entries strictly descending by version.
- [ ] Ensure README examples/flags match current CLI behavior (notably new commands or options).

4. **Validation**

- [ ] `pnpm build`
- [ ] `pnpm check`
- [ ] `pnpm test` (or `pnpm test:coverage` if you need coverage output)
- [ ] `pnpm release:check` (verifies npm pack contents)
- [ ] `OPENCLAW_INSTALL_SMOKE_SKIP_NONROOT=1 pnpm test:install:smoke` (Docker install smoke test, fast path; required before release)
  - If the immediate previous npm release is known broken, set `OPENCLAW_INSTALL_SMOKE_PREVIOUS=<last-good-version>` or `OPENCLAW_INSTALL_SMOKE_SKIP_PREVIOUS=1` for the preinstall step.
- [ ] (Optional) Full installer smoke (adds non-root + CLI coverage): `pnpm test:install:smoke`
- [ ] (Optional) Installer E2E (Docker, runs `curl -fsSL https://openclaw.ai/install.sh | bash`, onboards, then runs real tool calls):
  - `pnpm test:install:e2e:openai` (requires `OPENAI_API_KEY`)
  - `pnpm test:install:e2e:anthropic` (requires `ANTHROPIC_API_KEY`)
  - `pnpm test:install:e2e` (requires both keys; runs both providers)
- [ ] (Optional) Spot-check the web gateway if your changes affect send/receive paths.

5. **macOS app (Sparkle)**

- [ ] Build + sign the macOS app, then zip it for distribution.
- [ ] Generate the Sparkle appcast (HTML notes via [`scripts/make_appcast.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/make_appcast.sh)) and update `appcast.xml`.
- [ ] Keep the app zip (and optional dSYM zip) ready to attach to the GitHub release.
- [ ] Follow [macOS release](/platforms/mac/release) for the exact commands and required env vars.
  - `APP_BUILD` must be numeric + monotonic (no `-beta`) so Sparkle compares versions correctly.
  - If notarizing, use the `openclaw-notary` keychain profile created from App Store Connect API env vars (see [macOS release](/platforms/mac/release)).

6. **Publish (npm)**

- [ ] Confirm git status is clean; commit and push as needed.
- [ ] `npm login` (verify 2FA) if needed.
- [ ] `npm publish --access public` (use `--tag beta` for pre-releases).
- [ ] Verify the registry: `npm view openclaw version`, `npm view openclaw dist-tags`, and `npx -y openclaw@X.Y.Z --version` (or `--help`).

### Troubleshooting (notes from 2.0.0-beta2 release)

- **npm pack/publish hangs or produces huge tarball**: the macOS app bundle in `dist/OpenClaw.app` (and release zips) get swept into the package. Fix by whitelisting publish contents via `package.json` `files` (include dist subdirs, docs, skills; exclude app bundles). Confirm with `npm pack --dry-run` that `dist/OpenClaw.app` is not listed.
- **npm auth web loop for dist-tags**: use legacy auth to get an OTP prompt:
  - `NPM_CONFIG_AUTH_TYPE=legacy npm dist-tag add openclaw@X.Y.Z latest`
- **`npx` verification fails with `ECOMPROMISED: Lock compromised`**: retry with a fresh cache:
  - `NPM_CONFIG_CACHE=/tmp/npm-cache-$(date +%s) npx -y openclaw@X.Y.Z --version`
- **Tag needs repointing after a late fix**: force-update and push the tag, then ensure the GitHub release assets still match:
  - `git tag -f vX.Y.Z && git push -f origin vX.Y.Z`

7. **GitHub release + appcast**

- [ ] Tag and push: `git tag vX.Y.Z && git push origin vX.Y.Z` (or `git push --tags`).
- [ ] Create/refresh the GitHub release for `vX.Y.Z` with **title `openclaw X.Y.Z`** (not just the tag); body should include the **full** changelog section for that version (Highlights + Changes + Fixes), inline (no bare links), and **must not repeat the title inside the body**.
- [ ] Attach artifacts: `npm pack` tarball (optional), `OpenClaw-X.Y.Z.zip`, and `OpenClaw-X.Y.Z.dSYM.zip` (if generated).
- [ ] Commit the updated `appcast.xml` and push it (Sparkle feeds from main).
- [ ] From a clean temp directory (no `package.json`), run `npx -y openclaw@X.Y.Z send --help` to confirm install/CLI entrypoints work.
- [ ] Announce/share release notes.

## Plugin publish scope (npm)

We only publish **existing npm plugins** under the `@openclaw/*` scope. Bundled
plugins that are not on npm stay **disk-tree only** (still shipped in
`extensions/**`).

Process to derive the list:

1. `npm search @openclaw --json` and capture the package names.
2. Compare with `extensions/*/package.json` names.
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
