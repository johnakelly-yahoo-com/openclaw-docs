---
summary: 35. Node + tsx “__name is not a function” 崩溃说明与解决方法
read_when:
  - 36. 调试仅限 Node 的开发脚本或 watch 模式失败
  - 37. 调查 OpenClaw 中的 tsx/esbuild 加载器崩溃
title: "38. Node + tsx 崩溃"
---

# 39. Node + tsx “__name is not a function” 崩溃

## 40. 总结

41. 通过 Node 使用 `tsx` 运行 OpenClaw 时，在启动阶段失败，错误如下：

```
42. [openclaw] Failed to start CLI: TypeError: __name is not a function
    at createSubsystemLogger (.../src/logging/subsystem.ts:203:25)
    at .../src/agents/auth-profiles/constants.ts:25:20
```

43. 这在将开发脚本从 Bun 切换到 `tsx`（提交 `2871657e`，2026-01-06）之后开始出现。 44. 相同的运行路径在使用 Bun 时可以正常工作。

## 45. 环境

- 46. Node：v25.x（在 v25.3.0 上观察到）
- 47. tsx：4.21.0
- 48. 操作系统：macOS（在其他运行 Node 25 的平台上也可能复现）

## 49. 复现步骤（仅限 Node）

```bash
50. # in repo root
node --version
pnpm install
node --import tsx src/entry.ts status
```

## Minimal repro in repo

```bash
node --import tsx scripts/repro/tsx-name-repro.ts
```

## Node version check

- Node 25.3.0: fails
- Node 22.22.0 (Homebrew `node@22`): fails
- Node 24: not installed here yet; needs verification

## Notes / hypothesis

- `tsx` uses esbuild to transform TS/ESM. esbuild’s `keepNames` emits a `__name` helper and wraps function definitions with `__name(...)`.
- The crash indicates `__name` exists but is not a function at runtime, which implies the helper is missing or overwritten for this module in the Node 25 loader path.
- Similar `__name` helper issues have been reported in other esbuild consumers when the helper is missing or rewritten.

## Regression history

- `2871657e` (2026-01-06): scripts changed from Bun to tsx to make Bun optional.
- Before that (Bun path), `openclaw status` and `gateway:watch` worked.

## Workarounds

- Use Bun for dev scripts (current temporary revert).

- Use Node + tsc watch, then run compiled output:

  ```bash
  pnpm exec tsc --watch --preserveWatchOutput
  node --watch openclaw.mjs status
  ```

- Confirmed locally: `pnpm exec tsc -p tsconfig.json` + `node openclaw.mjs status` works on Node 25.

- Disable esbuild keepNames in the TS loader if possible (prevents `__name` helper insertion); tsx does not currently expose this.

- Test Node LTS (22/24) with `tsx` to see if the issue is Node 25–specific.

## References

- [https://opennext.js.org/cloudflare/howtos/keep_names](https://opennext.js.org/cloudflare/howtos/keep_names)
- [https://esbuild.github.io/api/#keep-names](https://esbuild.github.io/api/#keep-names)
- [https://github.com/evanw/esbuild/issues/1031](https://github.com/evanw/esbuild/issues/1031)

## Next steps

- Repro on Node 22/24 to confirm Node 25 regression.
- Test `tsx` nightly or pin to earlier version if a known regression exists.
- If reproduces on Node LTS, file a minimal repro upstream with the `__name` stack trace.
