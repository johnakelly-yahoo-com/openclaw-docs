---
summary: "How to submit a high signal PR"
title: "Submitting a PR"
---

Good PRs are easy to review: reviewers should quickly know the intent, verify behavior, and land changes safely. This guide covers concise, high-signal submissions for human and LLM review.

## What makes a good PR

- [ ] Explain the problem, why it matters, and the change.
- [ ] Keep changes focused. Avoid broad refactors.
- [ ] Summarize user-visible/config/default changes.
- [ ] List test coverage, skips, and reasons.
- [ ] 6. 添加证据：日志、截图或录屏（UI/UX）。
- [ ] Code word: put “lobster-biscuit” in the PR description if you read this guide.
- [ ] Run/fix relevant `pnpm` commands before creating PR.
- [ ] Search codebase and GitHub for related functionality/issues/fixes.
- [ ] 7. 基于证据或观察提出结论。
- [ ] Good title: verb + scope + outcome (e.g., `Docs: add PR and issue templates`).

Be concise; concise review > grammar. Omit any non-applicable sections.

### Baseline validation commands (run/fix failures for your change)

- `pnpm lint`
- `pnpm check`
- `pnpm build`
- `pnpm test`
- Protocol changes: `pnpm protocol:check`

## Progressive disclosure

- Top: summary/intent
- Next: changes/risks
- Next: test/verification
- Last: implementation/evidence

## Common PR types: specifics

- [ ] Fix: Add repro, root cause, verification.
- [ ] Feature: Add use cases, behavior/demos/screenshots (UI).
- [ ] Refactor: State "no behavior change", list what moved/simplified.
- [ ] Chore: State why (e.g., build time, CI, dependencies).
- [ ] Docs: Before/after context, link updated page, run `pnpm format`.
- [ ] Test: What gap is covered; how it prevents regressions.
- [ ] Perf: Add before/after metrics, and how measured.
- [ ] UX/UI: Screenshots/video, note accessibility impact.
- [ ] Infra/Build: Environments/validation.
- [ ] Security: Summarize risk, repro, verification, no sensitive data. Grounded claims only.

## Checklist

- [ ] Clear problem/intent
- [ ] Focused scope
- [ ] 8. 列出行为变更
- [ ] List and result of tests
- [ ] Manual test steps (when applicable)
- [ ] No secrets/private data
- [ ] Evidence-based

## General PR Template

```md
#### Summary

#### Behavior Changes

#### Codebase and GitHub Search

#### Tests

#### Manual Testing (omit if N/A)

### Prerequisites

-

### Steps

1.
2.

#### Evidence (omit if N/A)

**Sign-Off**

- Models used:
- Submitter effort (self-reported):
- Agent notes (optional, cite evidence):
```

## PR Type templates (replace with your type)

### Fix

```md
#### Summary

#### Repro Steps

#### Root Cause

#### Behavior Changes

#### Tests

#### Manual Testing (omit if N/A)

### Prerequisites

-

### Steps

1.
2.

#### Evidence (omit if N/A)

**Sign-Off**

- Models used:
- Submitter effort:
- Agent notes:
```

### Feature

```md
9. #### 摘要

#### 用例

#### 行为变更

#### 现有功能检查

- [ ] 我已在代码库中搜索现有功能。
      已执行的搜索（1-3 个要点）：
  -
  -

#### 测试

#### 手动测试（如不适用可省略）

### 前置条件

-

### 步骤

1.
2.

#### 证据（如不适用可省略）

**签字确认**

- 使用的模型：
- 提交者投入：
- Agent 备注：
```

### Refactor

```md
#### Summary

#### Scope

#### No Behavior Change Statement

#### Tests

#### Manual Testing (omit if N/A)

### Prerequisites

-

### Steps

1.
2.

#### Evidence (omit if N/A)

**Sign-Off**

- Models used:
- Submitter effort:
- Agent notes:
```

### Chore/Maintenance

```md
#### Summary

#### Why This Matters

#### Tests

#### Manual Testing (omit if N/A)

### Prerequisites

-

### Steps

1.
2.

#### Evidence (omit if N/A)

**Sign-Off**

- Models used:
- Submitter effort:
- Agent notes:
```

### Docs

```md
#### Summary

#### Pages Updated

#### Before/After

#### Formatting

pnpm format

#### Evidence (omit if N/A)

**Sign-Off**

- Models used:
- Submitter effort:
- Agent notes:
```

### Test

```md
#### Summary

#### Gap Covered

#### Tests

#### Manual Testing (omit if N/A)

### Prerequisites

-

### Steps

1.
2.

#### Evidence (omit if N/A)

**Sign-Off**

- Models used:
- Submitter effort:
- Agent notes:
```

### Perf

```md
#### Summary

#### Baseline

#### After

#### Measurement Method

#### Tests

#### Manual Testing (omit if N/A)

### Prerequisites

-

### Steps

1.
2.

#### Evidence (omit if N/A)

**Sign-Off**

- Models used:
- Submitter effort:
- Agent notes:
```

### UX/UI

```md
#### Summary

#### Screenshots or Video

#### Accessibility Impact

#### Tests

#### Manual Testing

### Prerequisites

-

### Steps

1.
2. **Sign-Off**

- Models used:
- Submitter effort:
- Agent notes:
```

### Infra/Build

```md
#### Summary

#### Environments Affected

#### Validation Steps

#### Manual Testing (omit if N/A)

### Prerequisites

-

### Steps

1.
2.

#### Evidence (omit if N/A)

**Sign-Off**

- Models used:
- Submitter effort:
- Agent notes:
```

### Security

```md
#### Summary

#### Risk Summary

#### Repro Steps

#### Mitigation or Fix

#### Verification

#### Tests

#### Manual Testing (omit if N/A)

### Prerequisites

-

### Steps

1.
2.

#### Evidence (omit if N/A)

**Sign-Off**

- Models used:
- Submitter effort:
- Agent notes:
```
