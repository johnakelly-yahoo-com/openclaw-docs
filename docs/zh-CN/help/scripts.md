---
summary: "Repository scripts: purpose, scope, and safety notes"
read_when:
  - 1. 从仓库中运行脚本
  - Adding or changing scripts under ./scripts
title: "Scripts"
---

# Scripts

The `scripts/` directory contains helper scripts for local workflows and ops tasks.
Use these when a task is clearly tied to a script; otherwise prefer the CLI.

## Conventions

- Scripts are **optional** unless referenced in docs or release checklists.
- 2. 在存在 CLI 接口时优先使用它们（例如：认证监控使用 `openclaw models status --check`）。
- 3. 假设脚本是与主机相关的；在新机器上运行前先阅读它们。

## 4. 认证监控脚本

5. 认证监控脚本文档在此：
   [/automation/auth-monitoring](/automation/auth-monitoring)

## When adding scripts

- Keep scripts focused and documented.
- Add a short entry in the relevant doc (or create one if missing).
