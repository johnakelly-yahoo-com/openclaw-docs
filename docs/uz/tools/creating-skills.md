---
title: "Creating Skills"
---

# Creating Custom Skills 🛠

OpenClaw is designed to be easily extensible. "Skills" are the primary way to add new capabilities to your assistant.

## What is a Skill?

A skill is a directory containing a `SKILL.md` file (which provides instructions and tool definitions to the LLM) and optionally some scripts or resources.

## Step-by-Step: Your First Skill

### 1. Create the Directory

Skills live in your workspace, usually `~/.openclaw/workspace/skills/`. Create a new folder for your skill:

```bash
mkdir -p ~/.openclaw/workspace/skills/hello-world
```

### 2. Define the `SKILL.md`

Create a `SKILL.md` file in that directory. This file uses YAML frontmatter for metadata and Markdown for instructions.

```markdown
---
name: hello_world
description: A simple skill that says hello.
---

# Hello World Skill

When the user asks for a greeting, use the `echo` tool to say "Hello from your custom skill!".
```

### 3. Add Tools (Optional)

You can define custom tools in the frontmatter or instruct the agent to use existing system tools (like `bash` or `browser`).

### 4. Refresh OpenClaw

Ask your agent to "refresh skills" or restart the gateway. OpenClaw will discover the new directory and index the `SKILL.md`.

## Best Practices

- 1. **Qisqa bo‘ling**: Modelga _nima_ qilish kerakligini ayting, uni qanday qilib AI bo‘lishini emas.
- 2. **Xavfsizlik birinchi o‘rinda**: Agar sizning ko‘nikmangiz `bash` dan foydalansa, promptlar ishonchsiz foydalanuvchi kiritmalaridan ixtiyoriy buyruq injeksiyasiga yo‘l qo‘ymasligiga ishonch hosil qiling.
- 3. **Mahalliy sinovdan o‘tkazing**: Sinash uchun `openclaw agent --message "use my new skill"` dan foydalaning.

## 4. Umumiy ko‘nikmalar

5. Shuningdek, siz [ClawHub](https://clawhub.com) orqali ko‘nikmalarni ko‘rib chiqishingiz va ularga hissa qo‘shishingiz mumkin.
