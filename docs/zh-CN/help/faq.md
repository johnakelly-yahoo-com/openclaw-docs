---
summary: "Frequently asked questions about OpenClaw setup, configuration, and usage"
title: "FAQ"
---

# FAQ

Quick answers plus deeper troubleshooting for real-world setups (local dev, VPS, multi-agent, OAuth/API keys, model failover). For runtime diagnostics, see [Troubleshooting](/gateway/troubleshooting). For the full config reference, see [Configuration](/gateway/configuration).

## 目录

- [快速开始和首次运行设置]
  - [我卡住了，最快的解卡方法是什么？](#im-stuck-whats-the-fastest-way-to-get-unstuck)
  - [安装和设置 OpenClaw 的推荐方式是什么？](#whats-the-recommended-way-to-install-and-set-up-openclaw)
  - [完成引导后，如何打开仪表盘？](#how-do-i-open-the-dashboard-after-onboarding)
  - [在 localhost 与远程环境中，如何进行仪表盘认证（token）？](#how-do-i-authenticate-the-dashboard-token-on-localhost-vs-remote)
  - [我需要什么运行时？](#what-runtime-do-i-need)
  - [可以在 Raspberry Pi 上运行吗？](#does-it-run-on-raspberry-pi)
  - [Raspberry Pi 安装有什么建议吗？](#any-tips-for-raspberry-pi-installs)
  - 它卡在 “wake up my friend” / 引导无法孵化。
    现在怎么办？ [可以在不重新进行引导的情况下，将我的设置迁移到新机器（Mac mini）吗？](#can-i-migrate-my-setup-to-a-new-machine-mac-mini-without-redoing-onboarding)
  - [在哪里可以看到最新版本的更新内容？](#where-do-i-see-what-is-new-in-the-latest-version)
  - 我无法访问 docs.openclaw.ai（SSL 错误）。
    现在怎么办？
  - [stable 和 beta 有什么区别？](#whats-the-difference-between-stable-and-beta) [如何安装 beta 版本？beta 和 dev 有什么区别？](#how-do-i-install-the-beta-version-and-whats-the-difference-between-beta-and-dev)
  - [如何体验最新版本？](#how-do-i-try-the-latest-bits)
  - [安装和引导通常需要多长时间？](#how-long-does-install-and-onboarding-usually-take)
  - 安装器卡住了？
    如何获取更多反馈？
  - [Windows 安装提示找不到 git 或无法识别 openclaw](#windows-install-says-git-not-found-or-openclaw-not-recognized)
  - [文档没有回答我的问题——如何获得更好的答案？](#the-docs-didnt-answer-my-question-how-do-i-get-a-better-answer) [如何在 Linux 上安装 OpenClaw？](#how-do-i-install-openclaw-on-linux)
  - [如何在 VPS 上安装 OpenClaw？](#how-do-i-install-openclaw-on-a-vps)
  - [云端 / VPS 的安装指南在哪里？](#where-are-the-cloudvps-install-guides)
  - [How do I install OpenClaw on Linux?](#how-do-i-install-openclaw-on-linux)
  - [引导向导实际上做了什么？](#what-does-the-onboarding-wizard-actually-do)
  - [运行这个需要 Claude 或 OpenAI 订阅吗？](#do-i-need-a-claude-or-openai-subscription-to-run-this)
  - [可以在没有 API key 的情况下使用 Claude Max 订阅吗](#can-i-use-claude-max-subscription-without-an-api-key)
  - [What does the onboarding wizard actually do?](#what-does-the-onboarding-wizard-actually-do)
  - [Do I need a Claude or OpenAI subscription to run this?](#do-i-need-a-claude-or-openai-subscription-to-run-this)
  - [是否支持 Claude 订阅认证（Claude Pro 或 Max）？](#do-you-support-claude-subscription-auth-claude-pro-or-max)
  - [为什么我会看到来自 Anthropic 的 `HTTP 429: rate_limit_error`？](#why-am-i-seeing-http-429-ratelimiterror-from-anthropic)
  - [是否支持 AWS Bedrock？](#is-aws-bedrock-supported)
  - [Codex 的认证是如何工作的？](#how-does-codex-auth-work)
  - [是否支持 OpenAI 订阅认证（Codex OAuth）？](#do-you-support-openai-subscription-auth-codex-oauth)
  - [如何设置 Gemini CLI OAuth](#how-do-i-set-up-gemini-cli-oauth)
  - [本地模型适合随意聊天吗？](#is-a-local-model-ok-for-casual-chats)
  - [Do you support OpenAI subscription auth (Codex OAuth)?](#do-you-support-openai-subscription-auth-codex-oauth)
  - [必须购买 Mac mini 才能安装这个吗？](#do-i-have-to-buy-a-mac-mini-to-install-this)
  - [iMessage 支持是否需要 Mac mini？](#do-i-need-a-mac-mini-for-imessage-support)
  - [如果我购买 Mac mini 来运行 OpenClaw，能把它连接到我的 MacBook Pro 吗？](#if-i-buy-a-mac-mini-to-run-openclaw-can-i-connect-it-to-my-macbook-pro)
  - [可以使用 Bun 吗？](#can-i-use-bun)
  - [Telegram：`allowFrom` 里应该填写什么？](#telegram-what-goes-in-allowfrom)
  - [是否可以让多个人使用同一个 WhatsApp 号码，但连接到不同的 OpenClaw 实例？](#can-multiple-people-use-one-whatsapp-number-with-different-openclaw-instances)
  - [可以同时运行一个“快速聊天”代理和一个“用于编程的 Opus”代理吗？](#can-i-run-a-fast-chat-agent-and-an-opus-for-coding-agent)
  - [Homebrew 在 Linux 上能用吗？](#does-homebrew-work-on-linux)
  - [可修改（git）安装与 npm 安装有什么区别？](#whats-the-difference-between-the-hackable-git-install-and-npm-install)
  - [之后可以在 npm 安装和 git 安装之间切换吗？](#can-i-switch-between-npm-and-git-installs-later)
  - [Does Homebrew work on Linux?](#does-homebrew-work-on-linux)
  - [What's the difference between the hackable (git) install and npm install?](#whats-the-difference-between-the-hackable-git-install-and-npm-install)
  - [Can I switch between npm and git installs later?](#can-i-switch-between-npm-and-git-installs-later)
  - [Should I run the Gateway on my laptop or a VPS?](#should-i-run-the-gateway-on-my-laptop-or-a-vps)
  - [How important is it to run OpenClaw on a dedicated machine?](#how-important-is-it-to-run-openclaw-on-a-dedicated-machine)
  - [What are the minimum VPS requirements and recommended OS?](#what-are-the-minimum-vps-requirements-and-recommended-os)
  - [Can I run OpenClaw in a VM and what are the requirements](#can-i-run-openclaw-in-a-vm-and-what-are-the-requirements)
- [What is OpenClaw?](#what-is-openclaw)
  - [What is OpenClaw, in one paragraph?](#what-is-openclaw-in-one-paragraph)
  - [What's the value proposition?](#whats-the-value-proposition)
  - [I just set it up what should I do first](#i-just-set-it-up-what-should-i-do-first)
  - [What are the top five everyday use cases for OpenClaw](#what-are-the-top-five-everyday-use-cases-for-openclaw)
  - [Can OpenClaw help with lead gen outreach ads and blogs for a SaaS](#can-openclaw-help-with-lead-gen-outreach-ads-and-blogs-for-a-saas)
  - [What are the advantages vs Claude Code for web development?](#what-are-the-advantages-vs-claude-code-for-web-development)
- [Skills and automation](#skills-and-automation)
  - [How do I customize skills without keeping the repo dirty?](#how-do-i-customize-skills-without-keeping-the-repo-dirty)
  - [Can I load skills from a custom folder?](#can-i-load-skills-from-a-custom-folder)
  - [How can I use different models for different tasks?](#how-can-i-use-different-models-for-different-tasks)
  - [The bot freezes while doing heavy work. How do I offload that?](#the-bot-freezes-while-doing-heavy-work-how-do-i-offload-that)
  - [Cron or reminders do not fire. What should I check?](#cron-or-reminders-do-not-fire-what-should-i-check)
  - [How do I install skills on Linux?](#how-do-i-install-skills-on-linux)
  - [Can OpenClaw run tasks on a schedule or continuously in the background?](#can-openclaw-run-tasks-on-a-schedule-or-continuously-in-the-background)
  - [Can I run Apple macOS-only skills from Linux?](#can-i-run-apple-macos-only-skills-from-linux)
  - [Do you have a Notion or HeyGen integration?](#do-you-have-a-notion-or-heygen-integration)
  - [How do I install the Chrome extension for browser takeover?](#how-do-i-install-the-chrome-extension-for-browser-takeover)
- [Sandboxing and memory](#sandboxing-and-memory)
  - [Is there a dedicated sandboxing doc?](#is-there-a-dedicated-sandboxing-doc)
  - [How do I bind a host folder into the sandbox?](#how-do-i-bind-a-host-folder-into-the-sandbox)
  - [How does memory work?](#how-does-memory-work)
  - [Memory keeps forgetting things. How do I make it stick?](#memory-keeps-forgetting-things-how-do-i-make-it-stick)
  - [Does memory persist forever? What are the limits?](#does-memory-persist-forever-what-are-the-limits)
  - [Does semantic memory search require an OpenAI API key?](#does-semantic-memory-search-require-an-openai-api-key)
- [Where things live on disk](#where-things-live-on-disk)
  - [Is all data used with OpenClaw saved locally?](#is-all-data-used-with-openclaw-saved-locally)
  - [Where does OpenClaw store its data?](#where-does-openclaw-store-its-data)
  - [Where should AGENTS.md / SOUL.md / USER.md / MEMORY.md live?](#where-should-agentsmd-soulmd-usermd-memorymd-live)
  - [What's the recommended backup strategy?](#whats-the-recommended-backup-strategy)
  - [How do I completely uninstall OpenClaw?](#how-do-i-completely-uninstall-openclaw)
  - [Can agents work outside the workspace?](#can-agents-work-outside-the-workspace)
  - [I'm in remote mode - where is the session store?](#im-in-remote-mode-where-is-the-session-store)
- [Config basics](#config-basics)
  - [What format is the config? Where is it?](#what-format-is-the-config-where-is-it)
  - [I set `gateway.bind: "lan"` (or `"tailnet"`) and now nothing listens / the UI says unauthorized](#i-set-gatewaybind-lan-or-tailnet-and-now-nothing-listens-the-ui-says-unauthorized)
  - [Why do I need a token on localhost now?](#why-do-i-need-a-token-on-localhost-now)
  - [Do I have to restart after changing config?](#do-i-have-to-restart-after-changing-config)
  - [How do I enable web search (and web fetch)?](#how-do-i-enable-web-search-and-web-fetch)
  - [config.apply wiped my config. How do I recover and avoid this?](#configapply-wiped-my-config-how-do-i-recover-and-avoid-this)
  - [如何在多设备上运行一个中心 Gateway 并配合专用的 workers？](#how-do-i-run-a-central-gateway-with-specialized-workers-across-devices)
  - [OpenClaw 浏览器可以以无头模式运行吗？](#can-the-openclaw-browser-run-headless)
  - [如何使用 Brave 进行浏览器控制？](#how-do-i-use-brave-for-browser-control)
- [远程 Gateway 和节点](#remote-gateways-and-nodes)
  - [命令如何在 Telegram、Gateway 和节点之间传播？](#how-do-commands-propagate-between-telegram-the-gateway-and-nodes)
  - [如果 Gateway 托管在远程，我的 agent 如何访问我的电脑？](#how-can-my-agent-access-my-computer-if-the-gateway-is-hosted-remotely)
  - Tailscale 已连接，但我没有收到任何回复。
    8. 现在该怎么办？ [两个 OpenClaw 实例可以互相通信吗（本地 + VPS）？](#can-two-openclaw-instances-talk-to-each-other-local-vps)
  - [Can two OpenClaw instances talk to each other (local + VPS)?](#can-two-openclaw-instances-talk-to-each-other-local-vps)
  - [与从 VPS 通过 SSH 相比，在个人笔记本上使用节点有什么好处吗？](#is-there-a-benefit-to-using-a-node-on-my-personal-laptop-instead-of-ssh-from-a-vps)
  - [节点是否运行 Gateway 服务？](#do-nodes-run-a-gateway-service)
  - [是否有 API / RPC 方式来应用配置？](#is-there-an-api-rpc-way-to-apply-config)
  - [首次安装的最小“合理”配置是什么？](#whats-a-minimal-sane-config-for-a-first-install)
  - [如何在 VPS 上设置 Tailscale 并从我的 Mac 连接？](#how-do-i-set-up-tailscale-on-a-vps-and-connect-from-my-mac)
  - [如何将 Mac 节点连接到远程 Gateway（Tailscale Serve）？](#how-do-i-connect-a-mac-node-to-a-remote-gateway-tailscale-serve)
  - [我应该在第二台笔记本上安装，还是只添加一个节点？](#should-i-install-on-a-second-laptop-or-just-add-a-node)
  - [Should I install on a second laptop or just add a node?](#should-i-install-on-a-second-laptop-or-just-add-a-node)
- [OpenClaw 如何加载环境变量？](#how-does-openclaw-load-environment-variables)
  - “我通过服务启动了 Gateway，结果环境变量消失了。”
    21. 现在该怎么办？
  - 我设置了  [会话和多重聊天](#sessions-and-multiple-chats)
  - [如何开始一个全新的对话？](#how-do-i-start-a-fresh-conversation) [如果我从不发送 `/new`，会话会自动重置吗？](#do-sessions-reset-automatically-if-i-never-send-new)
- [是否可以让一组 OpenClaw 实例组成一个 CEO 和多个 agent 的团队](#is-there-a-way-to-make-a-team-of-openclaw-instances-one-ceo-and-many-agents)
  - 为什么上下文在任务中途被截断？
    29. 我该如何防止？
  - [Do sessions reset automatically if I never send `/new`?](#do-sessions-reset-automatically-if-i-never-send-new)
  - [我遇到了“context too large”错误——如何重置或压缩？](#im-getting-context-too-large-errors-how-do-i-reset-or-compact)
  - [为什么我会看到“LLM request rejected: messages.N.content.X.tool_use.input: Field required”？](#why-am-i-seeing-llm-request-rejected-messagesncontentxtooluseinput-field-required) [为什么我每 30 分钟会收到一次心跳消息？](#why-am-i-getting-heartbeat-messages-every-30-minutes)
  - [我需要把一个“机器人账号”加入 WhatsApp 群组吗？](#do-i-need-to-add-a-bot-account-to-a-whatsapp-group)
  - [如何获取 WhatsApp 群组的 JID？](#how-do-i-get-the-jid-of-a-whatsapp-group)
  - [为什么 OpenClaw 在群组中不回复？](#why-doesnt-openclaw-reply-in-a-group)
  - [群组/线程是否与私信共享上下文？](#do-groupsthreads-share-context-with-dms)
  - [我可以创建多少个工作区和 agent？](#how-many-workspaces-and-agents-can-i-create)
  - [我可以同时运行多个机器人或聊天（Slack）吗？以及应该如何设置？](#can-i-run-multiple-bots-or-chats-at-the-same-time-slack-and-how-should-i-set-that-up)
  - [模型：默认值、选择、别名、切换](#models-defaults-selection-aliases-switching)
  - [什么是“默认模型”？](#what-is-the-default-model)
  - [你推荐使用哪个模型？](#what-model-do-you-recommend)
  - [如何在不清空配置的情况下切换模型？](#how-do-i-switch-models-without-wiping-my-config)
- [Models: defaults, selection, aliases, switching](#models-defaults-selection-aliases-switching)
  - [OpenClaw、Flawd 和 Krill 使用什么模型？](#what-do-openclaw-flawd-and-krill-use-for-models)
  - [如何在不重启的情况下即时切换模型？](#how-do-i-switch-models-on-the-fly-without-restarting)
  - [我可以用 GPT 5.2 处理日常任务，用 Codex 5.3 进行编程吗](#can-i-use-gpt-52-for-daily-tasks-and-codex-53-for-coding)
  - [Can I use self-hosted models (llama.cpp, vLLM, Ollama)?](#can-i-use-selfhosted-models-llamacpp-vllm-ollama)
  - [为什么我会看到“Unknown model: minimax/MiniMax-M2.1”？](#why-do-i-see-unknown-model-minimaxminimaxm21)
  - [How do I switch models on the fly (without restarting)?](#how-do-i-switch-models-on-the-fly-without-restarting)
  - [Can I use GPT 5.2 for daily tasks and Codex 5.3 for coding](#can-i-use-gpt-52-for-daily-tasks-and-codex-53-for-coding)
  - [Why do I see "Model … is not allowed" and then no reply?](#why-do-i-see-model-is-not-allowed-and-then-no-reply)
  - [Why do I see "Unknown model: minimax/MiniMax-M2.1"?](#why-do-i-see-unknown-model-minimaxminimaxm21)
  - [Can I use MiniMax as my default and OpenAI for complex tasks?](#can-i-use-minimax-as-my-default-and-openai-for-complex-tasks)
  - [Are opus / sonnet / gpt built-in shortcuts?](#are-opus-sonnet-gpt-builtin-shortcuts)
  - [How do I define/override model shortcuts (aliases)?](#how-do-i-defineoverride-model-shortcuts-aliases)
  - [How do I add models from other providers like OpenRouter or Z.AI?](#how-do-i-add-models-from-other-providers-like-openrouter-or-zai)
- [Model failover and "All models failed"](#model-failover-and-all-models-failed)
  - [How does failover work?](#how-does-failover-work)
  - [What does this error mean?](#what-does-this-error-mean)
  - [Fix checklist for `No credentials found for profile "anthropic:default"`](#fix-checklist-for-no-credentials-found-for-profile-anthropicdefault)
  - [Why did it also try Google Gemini and fail?](#why-did-it-also-try-google-gemini-and-fail)
- [Auth profiles: what they are and how to manage them](#auth-profiles-what-they-are-and-how-to-manage-them)
  - [What is an auth profile?](#what-is-an-auth-profile)
  - [What are typical profile IDs?](#what-are-typical-profile-ids)
  - [Can I control which auth profile is tried first?](#can-i-control-which-auth-profile-is-tried-first)
  - [OAuth vs API key: what's the difference?](#oauth-vs-api-key-whats-the-difference)
- [Gateway: ports, "already running", and remote mode](#gateway-ports-already-running-and-remote-mode)
  - [What port does the Gateway use?](#what-port-does-the-gateway-use)
  - [Why does `openclaw gateway status` say `Runtime: running` but `RPC probe: failed`?](#why-does-openclaw-gateway-status-say-runtime-running-but-rpc-probe-failed)
  - [Why does `openclaw gateway status` show `Config (cli)` and `Config (service)` different?](#why-does-openclaw-gateway-status-show-config-cli-and-config-service-different)
  - [What does "another gateway instance is already listening" mean?](#what-does-another-gateway-instance-is-already-listening-mean)
  - [How do I run OpenClaw in remote mode (client connects to a Gateway elsewhere)?](#how-do-i-run-openclaw-in-remote-mode-client-connects-to-a-gateway-elsewhere)
  - [The Control UI says "unauthorized" (or keeps reconnecting). What now?](#the-control-ui-says-unauthorized-or-keeps-reconnecting-what-now)
  - [I set `gateway.bind: "tailnet"` but it can't bind / nothing listens](#i-set-gatewaybind-tailnet-but-it-cant-bind-nothing-listens)
  - [Can I run multiple Gateways on the same host?](#can-i-run-multiple-gateways-on-the-same-host)
  - [What does "invalid handshake" / code 1008 mean?](#what-does-invalid-handshake-code-1008-mean)
- [Logging and debugging](#logging-and-debugging)
  - [Where are logs?](#where-are-logs)
  - [如何启动/停止/重启 Gateway 服务？](#how-do-i-startstoprestart-the-gateway-service)
  - [I closed my terminal on Windows - how do I restart OpenClaw?](#i-closed-my-terminal-on-windows-how-do-i-restart-openclaw)
  - [The Gateway is up but replies never arrive. What should I check?](#the-gateway-is-up-but-replies-never-arrive-what-should-i-check)
  - ["Disconnected from gateway: no reason" - what now?](#disconnected-from-gateway-no-reason-what-now)
  - [Telegram setMyCommands fails with network errors. What should I check?](#telegram-setmycommands-fails-with-network-errors-what-should-i-check)
  - [TUI shows no output. What should I check?](#tui-shows-no-output-what-should-i-check)
  - [How do I completely stop then start the Gateway?](#how-do-i-completely-stop-then-start-the-gateway)
  - [ELI5: `openclaw gateway restart` vs `openclaw gateway`](#eli5-openclaw-gateway-restart-vs-openclaw-gateway)
  - [What's the fastest way to get more details when something fails?](#whats-the-fastest-way-to-get-more-details-when-something-fails)
- [Media and attachments](#media-and-attachments)
  - [My skill generated an image/PDF, but nothing was sent](#my-skill-generated-an-imagepdf-but-nothing-was-sent)
- [Security and access control](#security-and-access-control)
  - [Is it safe to expose OpenClaw to inbound DMs?](#is-it-safe-to-expose-openclaw-to-inbound-dms)
  - [Is prompt injection only a concern for public bots?](#is-prompt-injection-only-a-concern-for-public-bots)
  - [Should my bot have its own email GitHub account or phone number](#should-my-bot-have-its-own-email-github-account-or-phone-number)
  - [Can I give it autonomy over my text messages and is that safe](#can-i-give-it-autonomy-over-my-text-messages-and-is-that-safe)
  - [Can I use cheaper models for personal assistant tasks?](#can-i-use-cheaper-models-for-personal-assistant-tasks)
  - [I ran `/start` in Telegram but didn't get a pairing code](#i-ran-start-in-telegram-but-didnt-get-a-pairing-code)
  - [WhatsApp: will it message my contacts? How does pairing work?](#whatsapp-will-it-message-my-contacts-how-does-pairing-work)
- [聊天命令、终止任务，以及“它停不下来”](#chat-commands-aborting-tasks-and-it-wont-stop)
  - [如何阻止内部系统消息显示在聊天中](#how-do-i-stop-internal-system-messages-from-showing-in-chat)
  - [如何停止/取消正在运行的任务？](#how-do-i-stopcancel-a-running-task)
  - [我如何从 Telegram 发送 Discord 消息？ (“跨上下文消息被拒绝”)](#how-do-i-send-a-discord-message-from-telegram-crosscontext-messaging-denied)
  - [为什么感觉机器人会“忽略”连续快速发送的消息？](#why-does-it-feel-like-the-bot-ignores-rapidfire-messages)

## 如果出现问题，前 60 秒该做什么

1. **快速状态（首次检查）**

   ```bash
   openclaw 状态
   ```

   快速本地汇总：操作系统 + 更新、网关/服务可达性、代理/会话、提供方配置 + 运行时问题（当网关可达时）。

2. **可粘贴报告（可安全分享）**

   ```bash
   openclaw status --all
   ```

   只读诊断并跟随日志末尾（令牌已脱敏）。

3. **守护进程 + 端口状态**

   ```bash
   openclaw gateway status
   ```

   显示监督器运行时与 RPC 可达性、探测目标 URL，以及服务可能使用的配置。

4. **深度探测**

   ```bash
   openclaw status --deep
   ```

   运行 Gateway 健康检查 + 提供方探测（需要可达的 Gateway）。 参见 [Health](/gateway/health)。

5. **尾随最新日志**

   ```bash
   openclaw logs --follow
   ```

   如果 RPC 不可用，则回退到：

   ```bash
   tail -f "$(ls -t /tmp/openclaw/openclaw-*.log | head -1)"
   ```

   文件日志与服务日志是分开的；参见 [Logging](/logging) 和 [Troubleshooting](/gateway/troubleshooting)。

6. **运行 doctor（修复）**

   ```bash
   openclaw doctor
   ```

   修复/迁移配置/状态并运行健康检查。 参见 [Doctor](/gateway/doctor)。

7. **网关快照**

   ```bash
   openclaw health --json
   openclaw health --verbose   # 在出错时显示目标 URL + 配置路径
   ```

   向正在运行的网关请求完整快照（仅 WS）。 参见 [Health](/gateway/health)。

## 快速开始与首次运行设置

### 我卡住了，最快脱困的方法是什么

使用一个能**看到你的机器**的本地 AI 代理。 这比在 Discord 里提问要有效得多，因为大多数“我卡住了”的情况都是**本地配置或环境问题**，远程帮助者无法检查。

- **Claude Code**: [https://www.anthropic.com/claude-code/](https://www.anthropic.com/claude-code/)
- **OpenAI Codex**: [https://openai.com/codex/](https://openai.com/codex/)

这些工具可以读取仓库、运行命令、检查日志，并帮助修复你机器级别的设置（PATH、服务、权限、认证文件）。 通过可黑客化的（git）安装方式向它们提供**完整源码检出**：

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git
```

这会**从 git 检出**安装 OpenClaw，因此代理可以读取代码和文档，并推理你正在运行的确切版本。 你始终可以在之后通过不带 `--install-method git` 重新运行安装器切换回稳定版。

提示：让代理**规划并监督**修复过程（逐步），然后只执行必要的命令。 这样可以让改动更小、更易审计。

如果你发现了真实的 bug 或修复，请提交 GitHub issue 或发送 PR：
[https://github.com/openclaw/openclaw/issues](https://github.com/openclaw/openclaw/issues)
[https://github.com/openclaw/openclaw/pulls](https://github.com/openclaw/openclaw/pulls)

从这些命令开始（在寻求帮助时分享输出）：

```bash
openclaw status
openclaw models status
openclaw doctor
```

它们的作用：

- `openclaw status`：快速查看网关/代理的健康状态 + 基本配置。
- `openclaw models status`：检查提供商认证 + 模型可用性。
- `openclaw doctor`：验证并修复常见的配置/状态问题。

其他有用的 CLI 检查：`openclaw status --all`、`openclaw logs --follow`，
`openclaw gateway status`、`openclaw health --verbose`。

快速调试循环：[出问题时的前 60 秒](#first-60-seconds-if-somethings-broken)。
Install docs: [Install](/install), [Installer flags](/install/installer), [Updating](/install/updating).

### 推荐的 OpenClaw 安装和设置方式是什么

仓库建议从源码运行并使用入门向导：

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw onboard --install-daemon
```

向导还可以自动构建 UI 资源。 完成入门后，通常会在端口 **18789** 上运行 Gateway。

从源码（贡献者/开发者）：

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm build
pnpm ui:build # auto-installs UI deps on first run
openclaw onboard
```

如果你还没有全局安装，可以通过 `pnpm openclaw onboard` 运行。

### 入门完成后如何打开仪表板

向导会在入门完成后立即用一个干净的（未令牌化）仪表板 URL 打开你的浏览器，并在总结中打印该链接。 保持该标签页打开；如果没有自动启动，请在同一台机器上复制/粘贴打印的 URL。

### 如何在 localhost 与远程环境下进行仪表板令牌认证

**Localhost（同一台机器）：**

- 打开 `http://127.0.0.1:18789/`。
- 如果提示需要认证，将 `gateway.auth.token`（或 `OPENCLAW_GATEWAY_TOKEN`）中的令牌粘贴到 Control UI 设置中。
- 在网关主机上获取：`openclaw config get gateway.auth.token`（或生成一个：`openclaw doctor --generate-gateway-token`）。

**不在 localhost：**

- **Tailscale Serve**（推荐）：保持绑定回环地址，运行 `openclaw gateway --tailscale serve`，打开 `https://<magicdns>/`。 如果 `gateway.auth.allowTailscale` 为 `true`，身份头即可满足认证（无需令牌）。
- **Tailnet 绑定**：运行 `openclaw gateway --bind tailnet --token "<token>"`，打开 `http://<tailscale-ip>:18789/`，在仪表板设置中粘贴令牌。
- **SSH 隧道**：`ssh -N -L 18789:127.0.0.1:18789 user@host`，然后打开 `http://127.0.0.1:18789/` 并在 Control UI 设置中粘贴令牌。

有关绑定模式和认证细节，请参阅 [Dashboard](/web/dashboard) 和 [Web surfaces](/web)。

### 需要什么运行时

需要 Node **>= 22**。 推荐使用 `pnpm`。 Gateway **不推荐** 使用 Bun。

### 能在 Raspberry Pi 上运行吗

可以。 Gateway 很轻量——文档列出 **512MB–1GB RAM**、**1 核**，以及约 **500MB** 磁盘即可满足个人使用，并指出 **Raspberry Pi 4 可以运行**。

如果需要更多余量（日志、媒体、其他服务），**推荐 2GB**，但这不是硬性最低要求。

提示：一台小型 Pi/VPS 就能托管 Gateway，你可以在笔记本/手机上配对 **节点**，用于本地屏幕/摄像头/画布或命令执行。 参见 [Nodes](/nodes)。

### Raspberry Pi 安装有什么建议吗

简短回答：能用，但要预期会有一些坑。

- 使用 **64 位** 操作系统，并保持 Node >= 22。
- 优先选择 **可折腾的（git）安装**，这样你可以查看日志并快速更新。
- 先不要启用 channels/skills，然后逐个添加。
- 如果遇到奇怪的二进制问题，通常是 **ARM 兼容性** 问题。

文档：[Linux](/platforms/linux)、[Install](/install)。

### 它卡在唤醒界面，我的朋友，入门向导不会孵化。现在怎么办？

该界面依赖 Gateway 可达且已通过认证。 TUI 也会在首次孵化时自动发送
“Wake up, my friend!”。 如果你看到这行文字却 **没有回复**，并且令牌始终为 0，说明代理从未运行。

1. 重启 Gateway：

```bash
1. openclaw 网关重启
```

2. 2. 检查状态 + 认证：

```bash
3. openclaw status
openclaw models status
openclaw logs --follow
```

3. 4. 如果仍然卡住，请运行：

```bash
5. openclaw doctor
```

6. 如果 Gateway 是远程的，请确保隧道/Tailscale 连接正常，并且 UI 指向正确的 Gateway。 7. 参见 [远程访问](/gateway/remote)。

### 8. 我可以在不重新进行引导的情况下，将我的设置迁移到一台新的 Mac mini 吗

9. 可以。 10. 复制 **state 目录** 和 **workspace**，然后运行一次 Doctor。 11. 只要你复制了 **这两个** 位置，这就能让你的机器人“**完全保持一致**”（内存、会话历史、认证以及通道状态）：

1. 12. 在新机器上安装 OpenClaw。
2. 13. 从旧机器复制 `$OPENCLAW_STATE_DIR`（默认：`~/.openclaw`）。
3. 14. 复制你的 workspace（默认：`~/.openclaw/workspace`）。
4. 15. 运行 `openclaw doctor` 并重启 Gateway 服务。

16) 这样可以保留配置、认证配置文件、WhatsApp 凭据、会话以及内存。 17. 如果你处于远程模式，请记住 gateway 主机拥有会话存储和 workspace。

18. **重要：** 如果你只是将 workspace 提交/推送到 GitHub，你备份的是 **内存 + 引导文件**，但 **不包括** 会话历史或认证信息。 19. 这些数据位于 `~/.openclaw/` 下（例如 `~/.openclaw/agents/<agentId>/sessions/`）。

20. 相关内容：[迁移](/install/migrating)、[磁盘上的数据位置](/help/faq#where-does-openclaw-store-its-data)、
    [Agent workspace](/concepts/agent-workspace)、[Doctor](/gateway/doctor)、
    [远程模式](/gateway/remote)。

### 21. 我在哪里可以看到最新版本的新内容

22. 查看 GitHub 更新日志：
    [https://github.com/openclaw/openclaw/blob/main/CHANGELOG.md](https://github.com/openclaw/openclaw/blob/main/CHANGELOG.md)

23. 最新条目位于顶部。 24. 如果顶部部分标记为 **Unreleased**，则下一个带日期的部分就是最近发布的版本。 25. 条目按 **Highlights**、**Changes** 和 **Fixes** 分组（必要时还包括文档/其他部分）。

### 26. 我无法访问 docs.openclaw.ai，出现 SSL 错误，该怎么办

27. 一些 Comcast/Xfinity 连接会通过 Xfinity Advanced Security 错误地阻止 `docs.openclaw.ai`。 28. 禁用该功能或将 `docs.openclaw.ai` 加入允许列表，然后重试。 29. 更多细节：[故障排除](/help/troubleshooting#docsopenclawai-shows-an-ssl-error-comcastxfinity)。
28. 请在此报告以帮助我们解除阻止：[https://spa.xfinity.com/check_url_status](https://spa.xfinity.com/check_url_status)。

31. 如果你仍然无法访问该站点，文档在 GitHub 上有镜像：
    [https://github.com/openclaw/openclaw/tree/main/docs](https://github.com/openclaw/openclaw/tree/main/docs)

### 32. stable 和 beta 之间有什么区别

33. **Stable** 和 **beta** 是 **npm dist-tag**，而不是独立的代码分支：

- 34. `latest` = 稳定版
- 35. `beta` = 用于测试的早期构建

36. 我们会将构建发布到 **beta**，进行测试，一旦某个构建足够稳定，就会 **将同一版本提升为 `latest`**。 37. 这就是为什么 beta 和 stable 可能指向 **同一个版本**。

38. 查看变更内容：
    [https://github.com/openclaw/openclaw/blob/main/CHANGELOG.md](https://github.com/openclaw/openclaw/blob/main/CHANGELOG.md)

### 39. 如何安装 beta 版本，以及 beta 和 dev 有什么区别

40. **Beta** 是 npm dist-tag `beta`（可能与 `latest` 相同）。
41. **Dev** 是 `main` 分支的持续最新版本（git）；发布时使用 npm dist-tag `dev`。

42. 一行命令（macOS/Linux）：

```bash
43. curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --beta
```

```bash
44. curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --install-method git
```

45. Windows 安装器（PowerShell）：
    [https://openclaw.ai/install.ps1](https://openclaw.ai/install.ps1)

46. 更多细节：[开发渠道](/install/development-channels) 和 [安装器参数](/install/installer)。

### 47. 安装和引导通常需要多长时间

48. 大致参考：

- 49. **安装：** 2–5 分钟
- 50. **引导：** 5–15 分钟，取决于你配置了多少通道/模型

If it hangs, use [Installer stuck](/help/faq#installer-stuck-how-do-i-get-more-feedback)
and the fast debug loop in [Im stuck](/help/faq#im-stuck--whats-the-fastest-way-to-get-unstuck).

### How do I try the latest bits

Two options:

1. **开发通道（git checkout）：**

```bash
openclaw update --channel dev
```

This switches to the `main` branch and updates from source.

2. **可黑客化安装（来自安装器站点）：**

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git
```

That gives you a local repo you can edit, then update via git.

If you prefer a clean clone manually, use:

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm build
```

Docs: [Update](/cli/update), [Development channels](/install/development-channels),
[Install](/install).

### 安装器卡住了——如何获得更多反馈

Re-run the installer with **verbose output**:

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --verbose
```

Beta install with verbose:

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --beta --verbose
```

For a hackable (git) install:

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git --verbose
```

More options: [Installer flags](/install/installer).

### Windows install says git not found or openclaw not recognized

Two common Windows issues:

**1) npm error spawn git / git not found**

- Install **Git for Windows** and make sure `git` is on your PATH.
- Close and reopen PowerShell, then re-run the installer.

**2) openclaw is not recognized after install**

- Your npm global bin folder is not on PATH.

- Check the path:

  ```powershell
  npm config get prefix
  ```

- Ensure `<prefix>\\bin` is on PATH (on most systems it is `%AppData%\\npm`).

- Close and reopen PowerShell after updating PATH.

If you want the smoothest Windows setup, use **WSL2** instead of native Windows.
文档：[Windows](/platforms/windows)。

### 文档没有回答我的问题，如何得到更好的答案

使用 **可黑客化（git）安装**，这样你就能在本地拥有完整源码和文档，然后在该文件夹 _内_ 询问你的机器人（或 Claude/Codex），让它读取仓库并给出精确答案。

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git
```

More detail: [Install](/install) and [Installer flags](/install/installer).

### How do I install OpenClaw on Linux

Short answer: follow the Linux guide, then run the onboarding wizard.

- Linux quick path + service install: [Linux](/platforms/linux).
- Full walkthrough: [Getting Started](/start/getting-started).
- Installer + updates: [Install & updates](/install/updating).

### How do I install OpenClaw on a VPS

Any Linux VPS works. Install on the server, then use SSH/Tailscale to reach the Gateway.

Guides: [exe.dev](/install/exe-dev), [Hetzner](/install/hetzner), [Fly.io](/install/fly).
Remote access: [Gateway remote](/gateway/remote).

### Where are the cloudVPS install guides

We keep a **hosting hub** with the common providers. Pick one and follow the guide:

- [VPS 托管](/vps)（所有提供商集中在一处）
- [Fly.io](/install/fly)
- [Hetzner](/install/hetzner)
- [exe.dev](/install/exe-dev)

云端的工作方式：**Gateway 运行在服务器上**，你通过控制 UI（或 Tailscale/SSH）从笔记本电脑/手机访问它。 你的状态 + 工作区
存放在服务器上，因此应将主机视为唯一事实来源并进行备份。

你可以将 **节点**（Mac/iOS/Android/无头）配对到该云端 Gateway，以访问本地屏幕/摄像头/画布，或在保持 Gateway 在云端的同时，在你的笔记本电脑上运行命令。

Hub：[Platforms](/platforms)。 远程访问：[Gateway remote](/gateway/remote)。
节点：[Nodes](/nodes)，[Nodes CLI](/cli/nodes)。

### 我可以让 OpenClaw 自行更新吗

简短回答：**可以，但不推荐**。 更新流程可能会重启 Gateway（这会断开当前会话），可能需要一次干净的 git 检出，并且可能会要求确认。 更安全的方式：由操作员在 shell 中运行更新。

使用 CLI：

```bash
openclaw update
openclaw update status
openclaw update --channel stable|beta|dev
openclaw update --tag <dist-tag|version>
openclaw update --no-restart
```

如果你必须从代理进行自动化：

```bash
openclaw update --yes --no-restart
openclaw gateway restart
```

文档：[Update](/cli/update)，[Updating](/install/updating)。

### 入门向导实际上做了什么

`openclaw onboard` 是推荐的设置路径。 在 **本地模式** 下，它会引导你完成：

- **模型/认证设置**（推荐用于 Claude 订阅的 Anthropic **setup-token**，支持 OpenAI Codex OAuth，可选 API key，支持 LM Studio 本地模型）
- **工作区** 位置 + 引导文件
- **Gateway 设置**（绑定/端口/认证/tailscale）
- **提供商**（WhatsApp、Telegram、Discord、Mattermost（插件）、Signal、iMessage）
- **守护进程安装**（macOS 上的 LaunchAgent；Linux/WSL2 上的 systemd 用户单元）
- **健康检查** 和 **技能** 选择

如果你配置的模型未知或缺少认证，它也会发出警告。

### 运行这个需要 Claude 或 OpenAI 订阅吗

不需要。 你可以使用 **API key**（Anthropic/OpenAI/其他）运行 OpenClaw，或使用 **仅本地模型**，这样你的数据会保留在你的设备上。 订阅（Claude Pro/Max 或 OpenAI Codex）是用于认证这些提供商的可选方式。

文档：[Anthropic](/providers/anthropic)，[OpenAI](/providers/openai)，
[Local models](/gateway/local-models)，[Models](/concepts/models)。

### 我可以在没有 API key 的情况下使用 Claude Max 订阅吗

可以。 你可以使用 **setup-token** 而不是 API key 进行认证。 这是订阅路径。

Claude Pro/Max 订阅 **不包含 API key**，因此这是订阅账户的正确做法。 重要：你必须向 Anthropic 核实此用法是否符合其订阅政策和条款。
如果你想要最明确、受支持的路径，请使用 Anthropic API key。

### Anthropic setuptoken 认证是如何工作的

`claude setup-token` 通过 Claude Code CLI 生成一个 **令牌字符串**（在网页控制台中不可用）。 你可以在 **任何机器** 上运行它。 在向导中选择 **Anthropic token（粘贴 setup-token）**，或使用 `openclaw models auth paste-token --provider anthropic` 粘贴。 该令牌会作为 **anthropic** 提供商的认证配置文件存储，并像 API key 一样使用（不会自动刷新）。 更多细节：[OAuth](/concepts/oauth)。

### 我在哪里可以找到 Anthropic 的 setuptoken

它 **不在** Anthropic Console 中。 setup-token 由 **Claude Code CLI** 在 **任何机器** 上生成：

```bash
claude setup-token
```

Copy the token it prints, then choose **Anthropic token (paste setup-token)** in the wizard. If you want to run it on the gateway host, use `openclaw models auth setup-token --provider anthropic`. If you ran `claude setup-token` elsewhere, paste it on the gateway host with `openclaw models auth paste-token --provider anthropic`. See [Anthropic](/providers/anthropic).

### Do you support Claude subscription auth (Claude Pro or Max)

Yes - via **setup-token**. OpenClaw no longer reuses Claude Code CLI OAuth tokens; use a setup-token or an Anthropic API key. 在任何地方生成令牌，然后粘贴到 Gateway 主机上。 参见 [Anthropic](/providers/anthropic) 和 [OAuth](/concepts/oauth)。

Note: Claude subscription access is governed by Anthropic's terms. For production or multi-user workloads, API keys are usually the safer choice.

### Why am I seeing HTTP 429 ratelimiterror from Anthropic

That means your **Anthropic quota/rate limit** is exhausted for the current window. If you
use a **Claude subscription** (setup-token or Claude Code OAuth), wait for the window to
reset or upgrade your plan. If you use an **Anthropic API key**, check the Anthropic Console
for usage/billing and raise limits as needed.

Tip: set a **fallback model** so OpenClaw can keep replying while a provider is rate-limited.
See [Models](/cli/models) and [OAuth](/concepts/oauth).

### Is AWS Bedrock supported

Yes - via pi-ai's **Amazon Bedrock (Converse)** provider with **manual config**. You must supply AWS credentials/region on the gateway host and add a Bedrock provider entry in your models config. See [Amazon Bedrock](/providers/bedrock) and [Model providers](/providers/models). If you prefer a managed key flow, an OpenAI-compatible proxy in front of Bedrock is still a valid option.

### How does Codex auth work

OpenClaw supports **OpenAI Code (Codex)** via OAuth (ChatGPT sign-in). The wizard can run the OAuth flow and will set the default model to `openai-codex/gpt-5.3-codex` when appropriate. See [Model providers](/concepts/model-providers) and [Wizard](/start/wizard).

### Do you support OpenAI subscription auth Codex OAuth

Yes. OpenClaw fully supports **OpenAI Code (Codex) subscription OAuth**. The onboarding wizard
can run the OAuth flow for you.

See [OAuth](/concepts/oauth), [Model providers](/concepts/model-providers), and [Wizard](/start/wizard).

### How do I set up Gemini CLI OAuth

Gemini CLI uses a **plugin auth flow**, not a client id or secret in `openclaw.json`.

Steps:

1. Enable the plugin: `openclaw plugins enable google-gemini-cli-auth`
2. Login: `openclaw models auth login --provider google-gemini-cli --set-default`

This stores OAuth tokens in auth profiles on the gateway host. Details: [Model providers](/concepts/model-providers).

### Is a local model OK for casual chats

Usually no. OpenClaw needs large context + strong safety; small cards truncate and leak. If you must, run the **largest** MiniMax M2.1 build you can locally (LM Studio) and see [/gateway/local-models](/gateway/local-models). Smaller/quantized models increase prompt-injection risk - see [Security](/gateway/security).

### How do I keep hosted model traffic in a specific region

Pick region-pinned endpoints. OpenRouter exposes US-hosted options for MiniMax, Kimi, and GLM; choose the US-hosted variant to keep data in-region. You can still list Anthropic/OpenAI alongside these by using `models.mode: "merge"` so fallbacks stay available while respecting the regioned provider you select.

### Do I have to buy a Mac Mini to install this

No. OpenClaw runs on macOS or Linux (Windows via WSL2). A Mac mini is optional - some people
buy one as an always-on host, but a small VPS, home server, or Raspberry Pi-class box works too.

You only need a Mac **for macOS-only tools**. For iMessage, use [BlueBubbles](/channels/bluebubbles) (recommended) - the BlueBubbles server runs on any Mac, and the Gateway can run on Linux or elsewhere. If you want other macOS-only tools, run the Gateway on a Mac or pair a macOS node.

Docs: [BlueBubbles](/channels/bluebubbles), [Nodes](/nodes), [Mac remote mode](/platforms/mac/remote).

### Do I need a Mac mini for iMessage support

You need **some macOS device** signed into Messages. **不** 一定要是 Mac mini —— 任何 Mac 都可以。 **Use [BlueBubbles](/channels/bluebubbles)** (recommended) for iMessage - the BlueBubbles server runs on macOS, while the Gateway can run on Linux or elsewhere.

Common setups:

- Run the Gateway on Linux/VPS, and run the BlueBubbles server on any Mac signed into Messages.
- Run everything on the Mac if you want the simplest single‑machine setup.

文档：[BlueBubbles](/channels/bluebubbles)，[Nodes](/nodes)，
[Mac 远程模式](/platforms/mac/remote)。

### If I buy a Mac mini to run OpenClaw can I connect it to my MacBook Pro

Yes. The **Mac mini can run the Gateway**, and your MacBook Pro can connect as a
**node** (companion device). Nodes don't run the Gateway - they provide extra
capabilities like screen/camera/canvas and `system.run` on that device.

Common pattern:

- Gateway on the Mac mini (always-on).
- MacBook Pro runs the macOS app or a node host and pairs to the Gateway.
- Use `openclaw nodes status` / `openclaw nodes list` to see it.

Docs: [Nodes](/nodes), [Nodes CLI](/cli/nodes).

### Can I use Bun

Bun is **not recommended**. We see runtime bugs, especially with WhatsApp and Telegram.
Use **Node** for stable gateways.

If you still want to experiment with Bun, do it on a non-production gateway
without WhatsApp/Telegram.

### Telegram what goes in allowFrom

`channels.telegram.allowFrom` is **the human sender's Telegram user ID** (numeric, recommended) or `@username`. It is not the bot username.

Safer (no third-party bot):

- DM your bot, then run `openclaw logs --follow` and read `from.id`.

Official Bot API:

- DM your bot, then call `https://api.telegram.org/bot<bot_token>/getUpdates` and read `message.from.id`.

Third-party (less private):

- DM `@userinfobot` or `@getidsbot`.

See [/channels/telegram](/channels/telegram#access-control-dms--groups).

### Can multiple people use one WhatsApp number with different OpenClaw instances

Yes, via **multi-agent routing**. 将每个发送者的 WhatsApp **DM**（peer `kind: "direct"`，发送者 E.164 如 `+15551234567`）绑定到不同的 `agentId`，这样每个人都有自己独立的工作区和会话存储。 Replies still come from the **same WhatsApp account**, and DM access control (`channels.whatsapp.dmPolicy` / `channels.whatsapp.allowFrom`) is global per WhatsApp account. See [Multi-Agent Routing](/concepts/multi-agent) and [WhatsApp](/channels/whatsapp).

### Can I run a fast chat agent and an Opus for coding agent

Yes. Use multi-agent routing: give each agent its own default model, then bind inbound routes (provider account or specific peers) to each agent. Example config lives in [Multi-Agent Routing](/concepts/multi-agent). See also [Models](/concepts/models) and [Configuration](/gateway/configuration).

### Does Homebrew work on Linux

Yes. Homebrew supports Linux (Linuxbrew). Quick setup:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.profile
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
brew install <formula>
```

If you run OpenClaw via systemd, ensure the service PATH includes `/home/linuxbrew/.linuxbrew/bin` (or your brew prefix) so `brew`-installed tools resolve in non-login shells.
Recent builds also prepend common user bin dirs on Linux systemd services (for example `~/.local/bin`, `~/.npm-global/bin`, `~/.local/share/pnpm`, `~/.bun/bin`) and honor `PNPM_HOME`, `NPM_CONFIG_PREFIX`, `BUN_INSTALL`, `VOLTA_HOME`, `ASDF_DATA_DIR`, `NVM_DIR`, and `FNM_DIR` when set.

### What's the difference between the hackable git install and npm install

- **Hackable (git) install:** full source checkout, editable, best for contributors.
  You run builds locally and can patch code/docs.
- **npm install:** global CLI install, no repo, best for "just run it."
  Updates come from npm dist-tags.

Docs: [Getting started](/start/getting-started), [Updating](/install/updating).

### Can I switch between npm and git installs later

Yes. Install the other flavor, then run Doctor so the gateway service points at the new entrypoint.
这 **不会删除你的数据** —— 只会更改 OpenClaw 代码的安装方式。 你的状态目录
(`~/.openclaw`) 和工作区 (`~/.openclaw/workspace`) 都保持不变。

From npm → git:

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm build
openclaw doctor
openclaw gateway restart
```

From git → npm:

```bash
npm install -g openclaw@latest
openclaw doctor
openclaw gateway restart
```

Doctor detects a gateway service entrypoint mismatch and offers to rewrite the service config to match the current install (use `--repair` in automation).

Backup tips: see [Backup strategy](/help/faq#whats-the-recommended-backup-strategy).

### Should I run the Gateway on my laptop or a VPS

Short answer: **if you want 24/7 reliability, use a VPS**. If you want the
lowest friction and you're okay with sleep/restarts, run it locally.

**Laptop (local Gateway)**

- **Pros:** no server cost, direct access to local files, live browser window.
- **Cons:** sleep/network drops = disconnects, OS updates/reboots interrupt, must stay awake.

**VPS / cloud**

- **Pros:** always-on, stable network, no laptop sleep issues, easier to keep running.
- **Cons:** often run headless (use screenshots), remote file access only, you must SSH for updates.

**OpenClaw-specific note:** WhatsApp/Telegram/Slack/Mattermost (plugin)/Discord all work fine from a VPS. The only real trade-off is **headless browser** vs a visible window. See [Browser](/tools/browser).

**Recommended default:** VPS if you had gateway disconnects before. Local is great when you're actively using the Mac and want local file access or UI automation with a visible browser.

### How important is it to run OpenClaw on a dedicated machine

Not required, but **recommended for reliability and isolation**.

- **Dedicated host (VPS/Mac mini/Pi):** always-on, fewer sleep/reboot interruptions, cleaner permissions, easier to keep running.
- **Shared laptop/desktop:** totally fine for testing and active use, but expect pauses when the machine sleeps or updates.

If you want the best of both worlds, keep the Gateway on a dedicated host and pair your laptop as a **node** for local screen/camera/exec tools. See [Nodes](/nodes).
For security guidance, read [Security](/gateway/security).

### What are the minimum VPS requirements and recommended OS

OpenClaw is lightweight. For a basic Gateway + one chat channel:

- **Absolute minimum:** 1 vCPU, 1GB RAM, ~500MB disk.
- **Recommended:** 1-2 vCPU, 2GB RAM or more for headroom (logs, media, multiple channels). Node tools and browser automation can be resource hungry.

OS: use **Ubuntu LTS** (or any modern Debian/Ubuntu). The Linux install path is best tested there.

Docs: [Linux](/platforms/linux), [VPS hosting](/vps).

### Can I run OpenClaw in a VM and what are the requirements

Yes. Treat a VM the same as a VPS: it needs to be always on, reachable, and have enough
RAM for the Gateway and any channels you enable.

Baseline guidance:

- **Absolute minimum:** 1 vCPU, 1GB RAM.
- **Recommended:** 2GB RAM or more if you run multiple channels, browser automation, or media tools.
- **OS:** Ubuntu LTS or another modern Debian/Ubuntu.

If you are on Windows, **WSL2 is the easiest VM style setup** and has the best tooling
compatibility. 参见 [Windows](/platforms/windows)，[VPS 托管](/vps)。
如果你在 VM 中运行 macOS，参见 [macOS VM](/install/macos-vm)。

## What is OpenClaw?

### What is OpenClaw in one paragraph

OpenClaw is a personal AI assistant you run on your own devices. It replies on the messaging surfaces you already use (WhatsApp, Telegram, Slack, Mattermost (plugin), Discord, Google Chat, Signal, iMessage, WebChat) and can also do voice + a live Canvas on supported platforms. The **Gateway** is the always-on control plane; the assistant is the product.

### What's the value proposition

OpenClaw is not "just a Claude wrapper." 这是一个 **本地优先的控制平面**，让你在 **自己的硬件** 上运行一个强大的助手，可从你已在使用的聊天应用访问，具备有状态会话、记忆和工具——无需把你的工作流控制权交给托管的 SaaS。

Highlights:

- **Your devices, your data:** run the Gateway wherever you want (Mac, Linux, VPS) and keep the
  workspace + session history local.
- **Real channels, not a web sandbox:** WhatsApp/Telegram/Slack/Discord/Signal/iMessage/etc,
  plus mobile voice and Canvas on supported platforms.
- **Model-agnostic:** use Anthropic, OpenAI, MiniMax, OpenRouter, etc., with per-agent routing
  and failover.
- **Local-only option:** run local models so **all data can stay on your device** if you want.
- **多智能体路由：** 按通道、账号或任务分离不同智能体，每个都有自己的工作区和默认设置。
- **Open source and hackable:** inspect, extend, and self-host without vendor lock-in.

Docs: [Gateway](/gateway), [Channels](/channels), [Multi-agent](/concepts/multi-agent),
[Memory](/concepts/memory).

### I just set it up what should I do first

Good first projects:

- Build a website (WordPress, Shopify, or a simple static site).
- Prototype a mobile app (outline, screens, API plan).
- Organize files and folders (cleanup, naming, tagging).
- Connect Gmail and automate summaries or follow ups.

It can handle large tasks, but it works best when you split them into phases and
use sub agents for parallel work.

### What are the top five everyday use cases for OpenClaw

Everyday wins usually look like:

- **Personal briefings:** summaries of inbox, calendar, and news you care about.
- **Research and drafting:** quick research, summaries, and first drafts for emails or docs.
- **Reminders and follow ups:** cron or heartbeat driven nudges and checklists.
- **Browser automation:** filling forms, collecting data, and repeating web tasks.
- **Cross device coordination:** send a task from your phone, let the Gateway run it on a server, and get the result back in chat.

### Can OpenClaw help with lead gen outreach ads and blogs for a SaaS

Yes for **research, qualification, and drafting**. It can scan sites, build shortlists,
summarize prospects, and write outreach or ad copy drafts.

For **outreach or ad runs**, keep a human in the loop. Avoid spam, follow local laws and
platform policies, and review anything before it is sent. The safest pattern is to let
OpenClaw draft and you approve.

Docs: [Security](/gateway/security).

### What are the advantages vs Claude Code for web development

OpenClaw is a **personal assistant** and coordination layer, not an IDE replacement. Use
Claude Code or Codex for the fastest direct coding loop inside a repo. Use OpenClaw when you
want durable memory, cross-device access, and tool orchestration.

Advantages:

- **Persistent memory + workspace** across sessions
- **Multi-platform access** (WhatsApp, Telegram, TUI, WebChat)
- **Tool orchestration** (browser, files, scheduling, hooks)
- **Always-on Gateway** (run on a VPS, interact from anywhere)
- **Nodes** for local browser/screen/camera/exec

Showcase: [https://openclaw.ai/showcase](https://openclaw.ai/showcase)

## Skills and automation

### How do I customize skills without keeping the repo dirty

Use managed overrides instead of editing the repo copy. Put your changes in `~/.openclaw/skills/<name>/SKILL.md` (or add a folder via `skills.load.extraDirs` in `~/.openclaw/openclaw.json`). Precedence is `<workspace>/skills` > `~/.openclaw/skills` > bundled, so managed overrides win without touching git. Only upstream-worthy edits should live in the repo and go out as PRs.

### Can I load skills from a custom folder

Yes. Add extra directories via `skills.load.extraDirs` in `~/.openclaw/openclaw.json` (lowest precedence). Default precedence remains: `<workspace>/skills` → `~/.openclaw/skills` → bundled → `skills.load.extraDirs`. `clawhub` installs into `./skills` by default, which OpenClaw treats as `<workspace>/skills`.

### How can I use different models for different tasks

Today the supported patterns are:

- **Cron jobs**: isolated jobs can set a `model` override per job.
- **Sub-agents**: route tasks to separate agents with different default models.
- **On-demand switch**: use `/model` to switch the current session model at any time.

See [Cron jobs](/automation/cron-jobs), [Multi-Agent Routing](/concepts/multi-agent), and [Slash commands](/tools/slash-commands).

### The bot freezes while doing heavy work How do I offload that

Use **sub-agents** for long or parallel tasks. Sub-agents run in their own session,
return a summary, and keep your main chat responsive.

Ask your bot to "spawn a sub-agent for this task" or use `/subagents`.
Use `/status` in chat to see what the Gateway is doing right now (and whether it is busy).

Token tip: long tasks and sub-agents both consume tokens. If cost is a concern, set a
cheaper model for sub-agents via `agents.defaults.subagents.model`.

Docs: [Sub-agents](/tools/subagents).

### Cron or reminders do not fire What should I check

Cron runs inside the Gateway process. If the Gateway is not running continuously,
scheduled jobs will not run.

Checklist:

- Confirm cron is enabled (`cron.enabled`) and `OPENCLAW_SKIP_CRON` is not set.
- Check the Gateway is running 24/7 (no sleep/restarts).
- Verify timezone settings for the job (`--tz` vs host timezone).

Debug:

```bash
openclaw cron run <jobId> --force
openclaw cron runs --id <jobId> --limit 50
```

Docs: [Cron jobs](/automation/cron-jobs), [Cron vs Heartbeat](/automation/cron-vs-heartbeat).

### How do I install skills on Linux

Use **ClawHub** (CLI) or drop skills into your workspace. The macOS Skills UI isn't available on Linux.
Browse skills at [https://clawhub.com](https://clawhub.com).

Install the ClawHub CLI (pick one package manager):

```bash
npm i -g clawhub
```

```bash
pnpm add -g clawhub
```

### Can OpenClaw run tasks on a schedule or continuously in the background

Yes. Use the Gateway scheduler:

- **Cron jobs** for scheduled or recurring tasks (persist across restarts).
- **Heartbeat** for "main session" periodic checks.
- **Isolated jobs** for autonomous agents that post summaries or deliver to chats.

Docs: [Cron jobs](/automation/cron-jobs), [Cron vs Heartbeat](/automation/cron-vs-heartbeat),
[Heartbeat](/gateway/heartbeat).

### Can I run Apple macOS-only skills from Linux?

Not directly. macOS skills are gated by `metadata.openclaw.os` plus required binaries, and skills only appear in the system prompt when they are eligible on the **Gateway host**. On Linux, `darwin`-only skills (like `apple-notes`, `apple-reminders`, `things-mac`) will not load unless you override the gating.

You have three supported patterns:

**Option A - run the Gateway on a Mac (simplest).**
Run the Gateway where the macOS binaries exist, then connect from Linux in [remote mode](#how-do-i-run-openclaw-in-remote-mode-client-connects-to-a-gateway-elsewhere) or over Tailscale. The skills load normally because the Gateway host is macOS.

**Option B - use a macOS node (no SSH).**
Run the Gateway on Linux, pair a macOS node (menubar app), and set **Node Run Commands** to "Always Ask" or "Always Allow" on the Mac. OpenClaw can treat macOS-only skills as eligible when the required binaries exist on the node. The agent runs those skills via the `nodes` tool. If you choose "Always Ask", approving "Always Allow" in the prompt adds that command to the allowlist.

**Option C - proxy macOS binaries over SSH (advanced).**
Keep the Gateway on Linux, but make the required CLI binaries resolve to SSH wrappers that run on a Mac. Then override the skill to allow Linux so it stays eligible.

1. Create an SSH wrapper for the binary (example: `memo` for Apple Notes):

   ```bash
   #!/usr/bin/env bash
   set -euo pipefail
   exec ssh -T user@mac-host /opt/homebrew/bin/memo "$@"
   ```

2. Put the wrapper on `PATH` on the Linux host (for example `~/bin/memo`).

3. Override the skill metadata (workspace or `~/.openclaw/skills`) to allow Linux:

   ```markdown
   ---
   name: apple-notes
   description: Manage Apple Notes via the memo CLI on macOS.
   metadata: { "openclaw": { "os": ["darwin", "linux"], "requires": { "bins": ["memo"] } } }
   ---
   ```

4. Start a new session so the skills snapshot refreshes.

### Do you have a Notion or HeyGen integration

Not built-in today.

Options:

- **Custom skill / plugin:** best for reliable API access (Notion/HeyGen both have APIs).
- **Browser automation:** works without code but is slower and more fragile.

If you want to keep context per client (agency workflows), a simple pattern is:

- One Notion page per client (context + preferences + active work).
- Ask the agent to fetch that page at the start of a session.

If you want a native integration, open a feature request or build a skill
targeting those APIs.

Install skills:

```bash
clawhub install <skill-slug>
clawhub update --all
```

ClawHub installs into `./skills` under your current directory (or falls back to your configured OpenClaw workspace); OpenClaw treats that as `<workspace>/skills` on the next session. For shared skills across agents, place them in `~/.openclaw/skills/<name>/SKILL.md`. Some skills expect binaries installed via Homebrew; on Linux that means Linuxbrew (see the Homebrew Linux FAQ entry above). See [Skills](/tools/skills) and [ClawHub](/tools/clawhub).

### How do I install the Chrome extension for browser takeover

Use the built-in installer, then load the unpacked extension in Chrome:

```bash
openclaw browser extension install
openclaw browser extension path
```

Then Chrome → `chrome://extensions` → enable "Developer mode" → "Load unpacked" → pick that folder.

Full guide (including remote Gateway + security notes): [Chrome extension](/tools/chrome-extension)

If the Gateway runs on the same machine as Chrome (default setup), you usually **do not** need anything extra.
If the Gateway runs elsewhere, run a node host on the browser machine so the Gateway can proxy browser actions.
You still need to click the extension button on the tab you want to control (it doesn't auto-attach).

## Sandboxing and memory

### Is there a dedicated sandboxing doc

Yes. See [Sandboxing](/gateway/sandboxing). For Docker-specific setup (full gateway in Docker or sandbox images), see [Docker](/install/docker).

### Docker feels limited How do I enable full features

The default image is security-first and runs as the `node` user, so it does not
include system packages, Homebrew, or bundled browsers. For a fuller setup:

- Persist `/home/node` with `OPENCLAW_HOME_VOLUME` so caches survive.
- Bake system deps into the image with `OPENCLAW_DOCKER_APT_PACKAGES`.
- Install Playwright browsers via the bundled CLI:
  `node /app/node_modules/playwright-core/cli.js install chromium`
- Set `PLAYWRIGHT_BROWSERS_PATH` and ensure the path is persisted.

Docs: [Docker](/install/docker), [Browser](/tools/browser).

**Can I keep DMs personal but make groups public sandboxed with one agent**

Yes - if your private traffic is **DMs** and your public traffic is **groups**.

Use `agents.defaults.sandbox.mode: "non-main"` so group/channel sessions (non-main keys) run in Docker, while the main DM session stays on-host. Then restrict what tools are available in sandboxed sessions via `tools.sandbox.tools`.

设置演练 + 示例配置：[分组：个人私信 + 公共群组](/channels/groups#pattern-personal-dms-public-groups-single-agent)

Key config reference: [Gateway configuration](/gateway/configuration#agentsdefaultssandbox)

### How do I bind a host folder into the sandbox

Set `agents.defaults.sandbox.docker.binds` to `["host:path:mode"]` (e.g., `"/home/user/src:/src:ro"`). Global + per-agent binds merge; per-agent binds are ignored when `scope: "shared"`. Use `:ro` for anything sensitive and remember binds bypass the sandbox filesystem walls. See [Sandboxing](/gateway/sandboxing#custom-bind-mounts) and [Sandbox vs Tool Policy vs Elevated](/gateway/sandbox-vs-tool-policy-vs-elevated#bind-mounts-security-quick-check) for examples and safety notes.

### How does memory work

OpenClaw memory is just Markdown files in the agent workspace:

- Daily notes in `memory/YYYY-MM-DD.md`
- Curated long-term notes in `MEMORY.md` (main/private sessions only)

OpenClaw also runs a **silent pre-compaction memory flush** to remind the model
to write durable notes before auto-compaction. This only runs when the workspace
is writable (read-only sandboxes skip it). See [Memory](/concepts/memory).

### Memory keeps forgetting things How do I make it stick

Ask the bot to **write the fact to memory**. Long-term notes belong in `MEMORY.md`,
short-term context goes into `memory/YYYY-MM-DD.md`.

This is still an area we are improving. It helps to remind the model to store memories;
it will know what to do. If it keeps forgetting, verify the Gateway is using the same
workspace on every run.

Docs: [Memory](/concepts/memory), [Agent workspace](/concepts/agent-workspace).

### Does semantic memory search require an OpenAI API key

Only if you use **OpenAI embeddings**. Codex OAuth covers chat/completions and
does **not** grant embeddings access, so **signing in with Codex (OAuth or the
Codex CLI login)** does not help for semantic memory search. OpenAI embeddings
still need a real API key (`OPENAI_API_KEY` or `models.providers.openai.apiKey`).

If you don't set a provider explicitly, OpenClaw auto-selects a provider when it
can resolve an API key (auth profiles, `models.providers.*.apiKey`, or env vars).
It prefers OpenAI if an OpenAI key resolves, otherwise Gemini if a Gemini key
resolves. If neither key is available, memory search stays disabled until you
configure it. If you have a local model path configured and present, OpenClaw
prefers `local`.

If you'd rather stay local, set `memorySearch.provider = "local"` (and optionally
`memorySearch.fallback = "none"`). If you want Gemini embeddings, set
`memorySearch.provider = "gemini"` and provide `GEMINI_API_KEY` (or
`memorySearch.remote.apiKey`). We support **OpenAI, Gemini, or local** embedding
models - see [Memory](/concepts/memory) for the setup details.

### Does memory persist forever What are the limits

1. 记忆文件存放在磁盘上，直到你删除它们之前都会一直存在。 2. 限制来自你的
   存储空间，而不是模型。 3. **会话上下文** 仍然受模型
   上下文窗口的限制，因此较长的对话可能会被压缩或截断。 4. 这就是为什么
   存在记忆搜索 —— 它只会将相关的部分拉回到上下文中。

5. 文档：[Memory](/concepts/memory)，[Context](/concepts/context)。

## 6. 数据在磁盘上的存放位置

### 7. 使用 OpenClaw 的所有数据都会保存在本地吗

8. 不会 —— **OpenClaw 的状态是本地的**，但**外部服务仍然可以看到你发送给它们的内容**。

- 9. **默认本地：** 会话、记忆文件、配置和工作区都位于 Gateway 主机上
     (`~/.openclaw` + 你的工作区目录)。
- 10. **因需要而远程：** 你发送给模型提供商（Anthropic/OpenAI 等）的消息 前往
      它们的 API，以及聊天平台（WhatsApp/Telegram/Slack 等）。 12. 会将消息数据存储在它们的
      服务器上。
- 13. **你控制数据足迹：** 使用本地模型可以让提示词留在你的机器上，但通道
      流量仍然会经过该通道的服务器。

14. 相关内容：[Agent workspace](/concepts/agent-workspace)，[Memory](/concepts/memory)。

### 15. OpenClaw 将数据存储在哪里

16. 所有内容都位于 `$OPENCLAW_STATE_DIR` 下（默认：`~/.openclaw`）：

| 17. 路径                                                              | 18. 用途                                          |
| ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| 19. `$OPENCLAW_STATE_DIR/openclaw.json`                             | 20. 主配置（JSON5）                                  |
| `$OPENCLAW_STATE_DIR/credentials/oauth.json`                                               | 22. 旧版 OAuth 导入（首次使用时复制到认证配置文件中）                |
| 23. `$OPENCLAW_STATE_DIR/agents/<agentId>/agent/auth-profiles.json` | 24. 认证配置（OAuth + API 密钥）                        |
| 25. `$OPENCLAW_STATE_DIR/agents/<agentId>/agent/auth.json`          | 26. 运行时认证缓存（自动管理）                               |
| 27. `$OPENCLAW_STATE_DIR/credentials/`                              | 28. 提供商状态（例如 `whatsapp/<accountId>/creds.json`） |
| 29. `$OPENCLAW_STATE_DIR/agents/`                                   | 30. 每个代理的状态（agentDir + 会话）                      |
| 31. `$OPENCLAW_STATE_DIR/agents/<agentId>/sessions/`                | 32. 对话历史和状态（按代理）                                |
| 33. `$OPENCLAW_STATE_DIR/agents/<agentId>/sessions/sessions.json`   | 34. 会话元数据（按代理）                                  |

35. 旧版单代理路径：`~/.openclaw/agent/*`（由 `openclaw doctor` 迁移）。

36. 你的 **工作区**（AGENTS.md、记忆文件、技能等） 37. 是独立的，并通过 `agents.defaults.workspace` 配置（默认：`~/.openclaw/workspace`）。

### 38. AGENTSmd、SOULmd、USERmd、MEMORYmd 应该放在哪里

39. 这些文件位于 **代理工作区** 中，而不是 `~/.openclaw`。

- **工作区（每个智能体）**：`AGENTS.md`、`SOUL.md`、`IDENTITY.md`、`USER.md`、
  `MEMORY.md`（或 `memory.md`）、`memory/YYYY-MM-DD.md`，可选 `HEARTBEAT.md`。
- 41. **状态目录（`~/.openclaw`）**：配置、凭据、认证配置、会话、日志，
      以及共享技能（`~/.openclaw/skills`）。

42. 默认工作区是 `~/.openclaw/workspace`，可通过以下方式配置：

```json5
43. {
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
}
```

44. 如果机器人在重启后“忘记”了内容，请确认 Gateway 在每次启动时都使用同一个
    工作区（并且请记住：远程模式使用的是 **Gateway 主机的**
    工作区，而不是你本地笔记本的）。

45. 提示：如果你希望某个行为或偏好是持久的，请让机器人 **将其写入
    AGENTS.md 或 MEMORY.md**，而不是依赖聊天记录。

46. 参见 [Agent workspace](/concepts/agent-workspace) 和 [Memory](/concepts/memory)。

### 47. 推荐的备份策略是什么

48. 将你的 **代理工作区** 放入一个 **私有** 的 git 仓库中，并备份到某个私有位置
    （例如 GitHub 私有仓库）。 49. 这样可以捕获记忆 + AGENTS/SOUL/USER
    文件，并让你以后能够恢复助手的“心智”。

50. **不要** 提交 `~/.openclaw` 下的任何内容（凭据、会话、令牌）。
    If you need a full restore, back up both the workspace and the state directory
    separately (see the migration question above).

Docs: [Agent workspace](/concepts/agent-workspace).

### How do I completely uninstall OpenClaw

See the dedicated guide: [Uninstall](/install/uninstall).

### Can agents work outside the workspace

Yes. The workspace is the **default cwd** and memory anchor, not a hard sandbox.
Relative paths resolve inside the workspace, but absolute paths can access other
host locations unless sandboxing is enabled. If you need isolation, use
[`agents.defaults.sandbox`](/gateway/sandboxing) or per-agent sandbox settings. If you
want a repo to be the default working directory, point that agent's
`workspace` to the repo root. The OpenClaw repo is just source code; keep the
workspace separate unless you intentionally want the agent to work inside it.

示例（仓库作为默认 cwd）：

```json5
{
  agents: {
    defaults: {
      workspace: "~/Projects/my-repo",
    },
  },
}
```

### Im in remote mode where is the session store

Session state is owned by the **gateway host**. If you're in remote mode, the session store you care about is on the remote machine, not your local laptop. 参见 [会话管理](/concepts/session)。

## Config basics

### What format is the config Where is it

OpenClaw reads an optional **JSON5** config from `$OPENCLAW_CONFIG_PATH` (default: `~/.openclaw/openclaw.json`):

```
$OPENCLAW_CONFIG_PATH
```

如果文件缺失，将使用相对安全的默认值（包括默认工作区 `~/.openclaw/workspace`）。

### I set gatewaybind lan or tailnet and now nothing listens the UI says unauthorized

Non-loopback binds **require auth**. 配置 `gateway.auth.mode` + `gateway.auth.token`（或使用 `OPENCLAW_GATEWAY_TOKEN`）。

```json5
{
  gateway: {
    bind: "lan",
    auth: {
      mode: "token",
      token: "replace-me",
    },
  },
}
```

Notes:

- `gateway.remote.token` is for **remote CLI calls** only; it does not enable local gateway auth.
- The Control UI authenticates via `connect.params.auth.token` (stored in app/UI settings). Avoid putting tokens in URLs.

### Why do I need a token on localhost now

The wizard generates a gateway token by default (even on loopback) so **local WS clients must authenticate**. This blocks other local processes from calling the Gateway. Paste the token into the Control UI settings (or your client config) to connect.

If you **really** want open loopback, remove `gateway.auth` from your config. Doctor can generate a token for you any time: `openclaw doctor --generate-gateway-token`.

### Do I have to restart after changing config

The Gateway watches the config and supports hot-reload:

- `gateway.reload.mode: "hybrid"` (default): hot-apply safe changes, restart for critical ones
- 也支持 `hot`、`restart`、`off`

### How do I enable web search and web fetch

`web_fetch` works without an API key. `web_search` requires a Brave Search API
key. **Recommended:** run `openclaw configure --section web` to store it in
`tools.web.search.apiKey`. Environment alternative: set `BRAVE_API_KEY` for the
Gateway process.

```json5
{
  tools: {
    web: {
      search: {
        enabled: true,
        apiKey: "BRAVE_API_KEY_HERE",
        maxResults: 5,
      },
      fetch: {
        enabled: true,
      },
    },
  },
}
```

Notes:

- If you use allowlists, add `web_search`/`web_fetch` or `group:web`.
- `web_fetch` is enabled by default (unless explicitly disabled).
- Daemons read env vars from `~/.openclaw/.env` (or the service environment).

Docs: [Web tools](/tools/web).

### How do I run a central Gateway with specialized workers across devices

The common pattern is **one Gateway** (e.g. Raspberry Pi) plus **nodes** and **agents**:

- **Gateway (central):** owns channels (Signal/WhatsApp), routing, and sessions.
- **Nodes (devices):** Macs/iOS/Android connect as peripherals and expose local tools (`system.run`, `canvas`, `camera`).
- **Agents (workers):** separate brains/workspaces for special roles (e.g. "Hetzner ops", "Personal data").
- **Sub-agents:** spawn background work from a main agent when you want parallelism.
- **TUI:** connect to the Gateway and switch agents/sessions.

Docs: [Nodes](/nodes), [Remote access](/gateway/remote), [Multi-Agent Routing](/concepts/multi-agent), [Sub-agents](/tools/subagents), [TUI](/web/tui).

### Can the OpenClaw browser run headless

Yes. It's a config option:

```json5
{
  browser: { headless: true },
  agents: {
    defaults: {
      sandbox: { browser: { headless: true } },
    },
  },
}
```

Default is `false` (headful). Headless is more likely to trigger anti-bot checks on some sites. See [Browser](/tools/browser).

Headless uses the **same Chromium engine** and works for most automation (forms, clicks, scraping, logins). 主要区别：

- 没有可见的浏览器窗口（如需视觉内容请使用截图）。
- Some sites are stricter about automation in headless mode (CAPTCHAs, anti-bot).
  For example, X/Twitter often blocks headless sessions.

### How do I use Brave for browser control

Set `browser.executablePath` to your Brave binary (or any Chromium-based browser) and restart the Gateway.
在 [Browser](/tools/browser#use-brave-or-another-chromium-based-browser) 中查看完整配置示例。

## Remote gateways and nodes

### How do commands propagate between Telegram the gateway and nodes

Telegram messages are handled by the **gateway**. The gateway runs the agent and
only then calls nodes over the **Gateway WebSocket** when a node tool is needed:

Telegram → Gateway → Agent → `node.*` → Node → Gateway → Telegram

Nodes don't see inbound provider traffic; they only receive node RPC calls.

### How can my agent access my computer if the Gateway is hosted remotely

Short answer: **pair your computer as a node**. The Gateway runs elsewhere, but it can
call `node.*` tools (screen, camera, system) on your local machine over the Gateway WebSocket.

Typical setup:

1. Run the Gateway on the always-on host (VPS/home server).
2. Put the Gateway host + your computer on the same tailnet.
3. Ensure the Gateway WS is reachable (tailnet bind or SSH tunnel).
4. Open the macOS app locally and connect in **Remote over SSH** mode (or direct tailnet)
   so it can register as a node.
5. Approve the node on the Gateway:

   ```bash
   openclaw nodes pending
   openclaw nodes approve <requestId>
   ```

No separate TCP bridge is required; nodes connect over the Gateway WebSocket.

Security reminder: pairing a macOS node allows `system.run` on that machine. Only
pair devices you trust, and review [Security](/gateway/security).

Docs: [Nodes](/nodes), [Gateway protocol](/gateway/protocol), [macOS remote mode](/platforms/mac/remote), [Security](/gateway/security).

### Tailscale is connected but I get no replies What now

Check the basics:

- Gateway is running: `openclaw gateway status`
- Gateway health: `openclaw status`
- Channel health: `openclaw channels status`

Then verify auth and routing:

- 1. 如果你使用 Tailscale Serve，请确保 `gateway.auth.allowTailscale` 设置正确。
- 2. 如果你通过 SSH 隧道连接，请确认本地隧道已建立并指向正确的端口。
- 3. 确认你的允许列表（私信或群组）包含你的账号。

4. 文档：[Tailscale](/gateway/tailscale)，[远程访问](/gateway/remote)，[频道](/channels)。

### 5. 两个 OpenClaw 实例可以在本地 VPS 上相互通信吗

6. 可以。 7. 没有内置的“bot-to-bot”桥接，但你可以通过几种可靠的方式自行搭建：

8. **最简单：** 使用两个机器人都能访问的普通聊天频道（Telegram/Slack/WhatsApp）。
9. 让 Bot A 向 Bot B 发送消息，然后让 Bot B 像往常一样回复。

10. **CLI 桥接（通用）：** 运行一个脚本，调用另一个 Gateway：
    `openclaw agent --message ... 11. --deliver`，目标是另一个机器人正在监听的聊天。 12. 如果其中一个机器人在远程 VPS 上，通过 SSH/Tailscale 将你的 CLI 指向该远程 Gateway（参见 [远程访问](/gateway/remote)）。

13. 示例模式（在一台可以访问目标 Gateway 的机器上运行）：

```bash
14. openclaw agent --message "Hello from local bot" --deliver --channel telegram --reply-to <chat-id>
```

15. 提示：添加防护措施，避免两个机器人无限循环（仅提及回复、频道允许列表，或“不要回复机器人消息”的规则）。

16. 文档：[远程访问](/gateway/remote)，[Agent CLI](/cli/agent)，[Agent 发送](/tools/agent-send)。

### 17. 我需要为多个 agent 使用单独的 VPS 吗

否。 19. 一个 Gateway 可以托管多个 agent，每个 agent 都有自己的工作区、模型默认值和路由。 20. 这是常规做法，比为每个 agent 运行一个 VPS 便宜且简单得多。

21. 只有在你需要强隔离（安全边界）或非常不同且不希望共享的配置时，才使用单独的 VPS。 22. 否则，保留一个 Gateway，使用多个 agent 或子 agent。

### 与从 VPS 通过 SSH 相比，在个人笔记本上使用节点是否有优势

24. 有——node 是从远程 Gateway 访问你笔记本的一级方式，而且解锁的不仅仅是 shell 访问。 25. Gateway 运行在 macOS/Linux（Windows 通过 WSL2），并且非常轻量（小型 VPS 或树莓派级别的设备即可；4 GB 内存就足够），因此常见的设置是一个始终在线的主机加上你的笔记本作为一个 node。

- 26. **无需入站 SSH。** Node 会主动连接到 Gateway 的 WebSocket，并使用设备配对。
- 27. **更安全的执行控制。** `system.run` 受该笔记本上的 node 允许列表/审批机制控制。
- 28. **更多设备工具。** 除了 `system.run`，node 还暴露 `canvas`、`camera` 和 `screen`。
- 29. **本地浏览器自动化。** 将 Gateway 放在 VPS 上，但在本地运行 Chrome，并通过 Chrome 扩展 + 笔记本上的 node host 中继控制。

30. SSH 适合临时的 shell 访问，但对于持续的 agent 工作流和设备自动化，node 更简单。

31. 文档：[Nodes](/nodes)，[Nodes CLI](/cli/nodes)，[Chrome 扩展](/tools/chrome-extension)。

### 32. 我应该在第二台笔记本上安装，还是只添加一个 node

33. 如果你只需要在第二台笔记本上使用 **本地工具**（screen/camera/exec），就把它添加为一个 **node**。 34. 这样可以保持单一 Gateway，并避免重复配置。 35. 本地 node 工具目前仅支持 macOS，但我们计划扩展到其他操作系统。

只有在需要 **硬隔离** 或两个完全独立的机器人时，才安装第二个 Gateway。

37. 文档：[Nodes](/nodes)，[Nodes CLI](/cli/nodes)，[多个 Gateway](/gateway/multiple-gateways)。

### 38. node 会运行一个 gateway 服务吗

39. 不会。 40. 除非你有意运行隔离的配置文件（参见 [多个 Gateway](/gateway/multiple-gateways)），否则每台主机只应运行 **一个 gateway**。 41. Node 是连接到 gateway 的外设（iOS/Android node，或 macOS 菜单栏应用中的“node 模式”）。 42. 对于无头 node 主机和 CLI 控制，参见 [Node host CLI](/cli/node)。

43. 对 `gateway`、`discovery` 和 `canvasHost` 的更改需要完整重启。

### 44. 是否有 API RPC 的方式来应用配置

是的。 46. `config.apply` 会校验并写入完整配置，并在操作过程中重启 Gateway。

### 47. configapply 把我的配置清空了，我该如何恢复并避免这种情况

`config.apply` 会替换 **整个配置**。 49. 如果你发送的是部分对象，其余所有内容都会被移除。

50. 恢复：

- Restore from backup (git or a copied `~/.openclaw/openclaw.json`).
- If you have no backup, re-run `openclaw doctor` and reconfigure channels/models.
- If this was unexpected, file a bug and include your last known config or any backup.
- A local coding agent can often reconstruct a working config from logs or history.

Avoid it:

- Use `openclaw config set` for small changes.
- Use `openclaw configure` for interactive edits.

Docs: [Config](/cli/config), [Configure](/cli/configure), [Doctor](/gateway/doctor).

### What's a minimal sane config for a first install

```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
  channels: { whatsapp: { allowFrom: ["+15555550123"] } },
}
```

This sets your workspace and restricts who can trigger the bot.

### How do I set up Tailscale on a VPS and connect from my Mac

Minimal steps:

1. **Install + login on the VPS**

   ```bash
   curl -fsSL https://tailscale.com/install.sh | sh
   sudo tailscale up
   ```

2. **在你的 Mac 上安装并登录**
   - Use the Tailscale app and sign in to the same tailnet.

3. **Enable MagicDNS (recommended)**
   - In the Tailscale admin console, enable MagicDNS so the VPS has a stable name.

4. **Use the tailnet hostname**
   - SSH: `ssh user@your-vps.tailnet-xxxx.ts.net`
   - Gateway WS: `ws://your-vps.tailnet-xxxx.ts.net:18789`

If you want the Control UI without SSH, use Tailscale Serve on the VPS:

```bash
openclaw gateway --tailscale serve
```

这会将网关绑定到回环地址，并通过 Tailscale 暴露 HTTPS。 See [Tailscale](/gateway/tailscale).

### How do I connect a Mac node to a remote Gateway Tailscale Serve

Serve exposes the **Gateway Control UI + WS**. Nodes connect over the same Gateway WS endpoint.

Recommended setup:

1. **Make sure the VPS + Mac are on the same tailnet**.
2. **Use the macOS app in Remote mode** (SSH target can be the tailnet hostname).
   The app will tunnel the Gateway port and connect as a node.
3. **在网关上批准该节点**：

   ```bash
   openclaw nodes pending
   openclaw nodes approve <requestId>
   ```

Docs: [Gateway protocol](/gateway/protocol), [Discovery](/gateway/discovery), [macOS remote mode](/platforms/mac/remote).

## Env vars and .env loading

### How does OpenClaw load environment variables

OpenClaw reads env vars from the parent process (shell, launchd/systemd, CI, etc.) and additionally loads:

- `.env` from the current working directory
- a global fallback `.env` from `~/.openclaw/.env` (aka `$OPENCLAW_STATE_DIR/.env`)

Neither `.env` file overrides existing env vars.

You can also define inline env vars in config (applied only if missing from the process env):

```json5
{
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: { GROQ_API_KEY: "gsk-..." },
  },
}
```

See [/environment](/help/environment) for full precedence and sources.

### I started the Gateway via the service and my env vars disappeared What now

Two common fixes:

1. Put the missing keys in `~/.openclaw/.env` so they're picked up even when the service doesn't inherit your shell env.
2. Enable shell import (opt-in convenience):

```json5
{
  env: {
    shellEnv: {
      enabled: true,
      timeoutMs: 15000,
    },
  },
}
```

This runs your login shell and imports only missing expected keys (never overrides). Env var equivalents:
`OPENCLAW_LOAD_SHELL_ENV=1`, `OPENCLAW_SHELL_ENV_TIMEOUT_MS=15000`.

### I set COPILOTGITHUBTOKEN but models status shows Shell env off Why

`openclaw models status` reports whether **shell env import** is enabled. "Shell env: off"
does **not** mean your env vars are missing - it just means OpenClaw won't load
your login shell automatically.

If the Gateway runs as a service (launchd/systemd), it won't inherit your shell
environment. Fix by doing one of these:

1. Put the token in `~/.openclaw/.env`:

   ```
   COPILOT_GITHUB_TOKEN=...
   ```

2. Or enable shell import (`env.shellEnv.enabled: true`).

3. Or add it to your config `env` block (applies only if missing).

Then restart the gateway and recheck:

```bash
openclaw models status
```

Copilot tokens are read from `COPILOT_GITHUB_TOKEN` (also `GH_TOKEN` / `GITHUB_TOKEN`).
See [/concepts/model-providers](/concepts/model-providers) and [/environment](/help/environment).

## Sessions and multiple chats

### 如何开始一段全新的对话

发送 `/new` 或 `/reset` 作为一条独立消息。 See [Session management](/concepts/session).

### 如果我从不发送 new，会话会自动重置吗

Yes. Sessions expire after `session.idleMinutes` (default **60**). The **next**
message starts a fresh session id for that chat key. This does not delete
transcripts - it just starts a new session.

```json5
{
  session: {
    idleMinutes: 240,
  },
}
```

### Is there a way to make a team of OpenClaw instances one CEO and many agents

Yes, via **multi-agent routing** and **sub-agents**. You can create one coordinator
agent and several worker agents with their own workspaces and models.

That said, this is best seen as a **fun experiment**. It is token heavy and often
less efficient than using one bot with separate sessions. The typical model we
envision is one bot you talk to, with different sessions for parallel work. That
bot can also spawn sub-agents when needed.

Docs: [Multi-agent routing](/concepts/multi-agent), [Sub-agents](/tools/subagents), [Agents CLI](/cli/agents).

### Why did context get truncated midtask How do I prevent it

Session context is limited by the model window. Long chats, large tool outputs, or many
files can trigger compaction or truncation.

What helps:

- Ask the bot to summarize the current state and write it to a file.
- Use `/compact` before long tasks, and `/new` when switching topics.
- Keep important context in the workspace and ask the bot to read it back.
- Use sub-agents for long or parallel work so the main chat stays smaller.
- Pick a model with a larger context window if this happens often.

### How do I completely reset OpenClaw but keep it installed

Use the reset command:

```bash
openclaw reset
```

Non-interactive full reset:

```bash
openclaw reset --scope full --yes --non-interactive
```

Then re-run onboarding:

```bash
openclaw onboard --install-daemon
```

Notes:

- The onboarding wizard also offers **Reset** if it sees an existing config. See [Wizard](/start/wizard).
- If you used profiles (`--profile` / `OPENCLAW_PROFILE`), reset each state dir (defaults are `~/.openclaw-<profile>`).
- 开发重置：`openclaw gateway --dev --reset`（仅限 dev；会清除 dev 配置 + 凭据 + 会话 + 工作区）。

### Im getting context too large errors how do I reset or compact

Use one of these:

- **Compact** (keeps the conversation but summarizes older turns):

  ```
  /compact
  ```

  or `/compact <instructions>` to guide the summary.

- **重置**（为同一聊天键生成新的会话 ID）：

  ```
  /new
  /reset
  ```

If it keeps happening:

- Enable or tune **session pruning** (`agents.defaults.contextPruning`) to trim old tool output.
- 使用具有更大上下文窗口的模型。

Docs: [Compaction](/concepts/compaction), [Session pruning](/concepts/session-pruning), [Session management](/concepts/session).

### Why am I seeing LLM request rejected messagesNcontentXtooluseinput Field required

This is a provider validation error: the model emitted a `tool_use` block without the required
`input`. It usually means the session history is stale or corrupted (often after long threads
or a tool/schema change).

Fix: start a fresh session with `/new` (standalone message).

### Why am I getting heartbeat messages every 30 minutes

Heartbeats run every **30m** by default. Tune or disable them:

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "2h", // or "0m" to disable
      },
    },
  },
}
```

If `HEARTBEAT.md` exists but is effectively empty (only blank lines and markdown
headers like `# Heading`), OpenClaw skips the heartbeat run to save API calls.
If the file is missing, the heartbeat still runs and the model decides what to do.

按智能体覆盖使用 `agents.list[].heartbeat`。文档：[心跳](/gateway/heartbeat)。 Docs: [Heartbeat](/gateway/heartbeat).

### Do I need to add a bot account to a WhatsApp group

No. OpenClaw runs on **your own account**, so if you're in the group, OpenClaw can see it.
By default, group replies are blocked until you allow senders (`groupPolicy: "allowlist"`).

If you want only **you** to be able to trigger group replies:

```json5
{
  channels: {
    whatsapp: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15551234567"],
    },
  },
}
```

### How do I get the JID of a WhatsApp group

Option 1 (fastest): tail logs and send a test message in the group:

```bash
openclaw logs --follow --json
```

Look for `chatId` (or `from`) ending in `@g.us`, like:
`1234567890-1234567890@g.us`.

Option 2 (if already configured/allowlisted): list groups from config:

```bash
openclaw directory groups list --channel whatsapp
```

Docs: [WhatsApp](/channels/whatsapp), [Directory](/cli/directory), [Logs](/cli/logs).

### Why doesnt OpenClaw reply in a group

Two common causes:

- Mention gating is on (default). You must @mention the bot (or match `mentionPatterns`).
- You configured `channels.whatsapp.groups` without `"*"` and the group isn't allowlisted.

See [Groups](/channels/groups) and [Group messages](/channels/group-messages).

### Do groupsthreads share context with DMs

Direct chats collapse to the main session by default. Groups/channels have their own session keys, and Telegram topics / Discord threads are separate sessions. 参见 [Groups](/channels/groups) 和 [Group messages](/channels/group-messages)。

### How many workspaces and agents can I create

No hard limits. Dozens (even hundreds) are fine, but watch for:

- **Disk growth:** sessions + transcripts live under `~/.openclaw/agents/<agentId>/sessions/`.
- **Token cost:** more agents means more concurrent model usage.
- **Ops overhead:** per-agent auth profiles, workspaces, and channel routing.

Tips:

- Keep one **active** workspace per agent (`agents.defaults.workspace`).
- Prune old sessions (delete JSONL or store entries) if disk grows.
- Use `openclaw doctor` to spot stray workspaces and profile mismatches.

### Can I run multiple bots or chats at the same time Slack and how should I set that up

Yes. Use **Multi-Agent Routing** to run multiple isolated agents and route inbound messages by
channel/account/peer. Slack 作为一个频道受支持，并且可以绑定到特定代理。

Browser access is powerful but not "do anything a human can" - anti-bot, CAPTCHAs, and MFA can
still block automation. For the most reliable browser control, use the Chrome extension relay
on the machine that runs the browser (and keep the Gateway anywhere).

Best-practice setup:

- Always-on Gateway host (VPS/Mac mini).
- One agent per role (bindings).
- Slack channel(s) bound to those agents.
- Local browser via extension relay (or a node) when needed.

Docs: [Multi-Agent Routing](/concepts/multi-agent), [Slack](/channels/slack),
[Browser](/tools/browser), [Chrome extension](/tools/chrome-extension), [Nodes](/nodes).

## Models: defaults, selection, aliases, switching

### What is the default model

OpenClaw 的默认模型是你在此处设置的：

```
agents.defaults.model.primary
```

Models are referenced as `provider/model` (example: `anthropic/claude-opus-4-6`). If you omit the provider, OpenClaw currently assumes `anthropic` as a temporary deprecation fallback - but you should still **explicitly** set `provider/model`.

### What model do you recommend

**Recommended default:** `anthropic/claude-opus-4-6`.
**Good alternative:** `anthropic/claude-sonnet-4-5`.
**Reliable (less character):** `openai/gpt-5.2` - nearly as good as Opus, just less personality.
**Budget:** `zai/glm-4.7`.

MiniMax M2.1 有其独立文档：[MiniMax](/providers/minimax) 以及
[Local models](/gateway/local-models)。

Rule of thumb: use the **best model you can afford** for high-stakes work, and a cheaper
model for routine chat or summaries. You can route models per agent and use sub-agents to
parallelize long tasks (each sub-agent consumes tokens). See [Models](/concepts/models) and
[Sub-agents](/tools/subagents).

Strong warning: weaker/over-quantized models are more vulnerable to prompt
injection and unsafe behavior. See [Security](/gateway/security).

More context: [Models](/concepts/models).

### Can I use selfhosted models llamacpp vLLM Ollama

Yes. If your local server exposes an OpenAI-compatible API, you can point a
custom provider at it. Ollama is supported directly and is the easiest path.

Security note: smaller or heavily quantized models are more vulnerable to prompt
injection. We strongly recommend **large models** for any bot that can use tools.
If you still want small models, enable sandboxing and strict tool allowlists.

Docs: [Ollama](/providers/ollama), [Local models](/gateway/local-models),
[Model providers](/concepts/model-providers), [Security](/gateway/security),
[Sandboxing](/gateway/sandboxing).

### How do I switch models without wiping my config

Use **model commands** or edit only the **model** fields. Avoid full config replaces.

Safe options:

- `/model` in chat (quick, per-session)
- `openclaw models set ...` (updates just model config)
- `openclaw configure --section model` (interactive)
- edit `agents.defaults.model` in `~/.openclaw/openclaw.json`

Avoid `config.apply` with a partial object unless you intend to replace the whole config.
If you did overwrite config, restore from backup or re-run `openclaw doctor` to repair.

Docs: [Models](/concepts/models), [Configure](/cli/configure), [Config](/cli/config), [Doctor](/gateway/doctor).

### What do OpenClaw, Flawd, and Krill use for models

- **OpenClaw + Flawd:** Anthropic Opus (`anthropic/claude-opus-4-6`) - see [Anthropic](/providers/anthropic).
- **Krill:** MiniMax M2.1 (`minimax/MiniMax-M2.1`) - see [MiniMax](/providers/minimax).

### How do I switch models on the fly without restarting

Use the `/model` command as a standalone message:

```
/model sonnet
/model haiku
/model opus
/model gpt
/model gpt-mini
/model gemini
/model gemini-flash
```

You can list available models with `/model`, `/model list`, or `/model status`.

`/model` (and `/model list`) shows a compact, numbered picker. Select by number:

```
/model 3
```

You can also force a specific auth profile for the provider (per session):

```
/model opus@anthropic:default
/model opus@anthropic:work
```

Tip: `/model status` shows which agent is active, which `auth-profiles.json` file is being used, and which auth profile will be tried next.
It also shows the configured provider endpoint (`baseUrl`) and API mode (`api`) when available.

**如何取消固定我用 profile 设置的配置**

重新运行 `/model`，**不要**带 `@profile` 后缀：

```
/model anthropic/claude-opus-4-6
```

If you want to return to the default, pick it from `/model` (or send `/model <default provider/model>`).
Use `/model status` to confirm which auth profile is active.

### Can I use GPT 5.2 for daily tasks and Codex 5.3 for coding

Yes. Set one as default and switch as needed:

- **Quick switch (per session):** `/model gpt-5.2` for daily tasks, `/model gpt-5.3-codex` for coding.
- **Default + switch:** set `agents.defaults.model.primary` to `openai/gpt-5.2`, then switch to `openai-codex/gpt-5.3-codex` when coding (or the other way around).
- **Sub-agents:** route coding tasks to sub-agents with a different default model.

See [Models](/concepts/models) and [Slash commands](/tools/slash-commands).

### Why do I see Model is not allowed and then no reply

If `agents.defaults.models` is set, it becomes the **allowlist** for `/model` and any
session overrides. Choosing a model that isn't in that list returns:

```
Model "provider/model" is not allowed. Use /model to list available models.
```

That error is returned **instead of** a normal reply. Fix: add the model to
`agents.defaults.models`, remove the allowlist, or pick a model from `/model list`.

### Why do I see Unknown model minimaxMiniMaxM21

This means the **provider isn't configured** (no MiniMax provider config or auth
profile was found), so the model can't be resolved. A fix for this detection is
in **2026.1.12** (unreleased at the time of writing).

Fix checklist:

1. Upgrade to **2026.1.12** (or run from source `main`), then restart the gateway.
2. Make sure MiniMax is configured (wizard or JSON), or that a MiniMax API key
   exists in env/auth profiles so the provider can be injected.
3. Use the exact model id (case-sensitive): `minimax/MiniMax-M2.1` or
   `minimax/MiniMax-M2.1-lightning`.
4. Run:

   ```bash
   openclaw models list
   ```

   and pick from the list (or `/model list` in chat).

See [MiniMax](/providers/minimax) and [Models](/concepts/models).

### Can I use MiniMax as my default and OpenAI for complex tasks

Yes. Use **MiniMax as the default** and switch models **per session** when needed.
Fallbacks are for **errors**, not "hard tasks," so use `/model` or a separate agent.

**Option A: switch per session**

```json5
{
  env: { MINIMAX_API_KEY: "sk-...", OPENAI_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "minimax/MiniMax-M2.1" },
      models: {
        "minimax/MiniMax-M2.1": { alias: "minimax" },
        "openai/gpt-5.2": { alias: "gpt" },
      },
    },
  },
}
```

Then:

```
/model gpt
```

**Option B: separate agents**

- 代理 A 默认：MiniMax
- Agent B default: OpenAI
- Route by agent or use `/agent` to switch

Docs: [Models](/concepts/models), [Multi-Agent Routing](/concepts/multi-agent), [MiniMax](/providers/minimax), [OpenAI](/providers/openai).

### Are opus sonnet gpt builtin shortcuts

Yes. OpenClaw ships a few default shorthands (only applied when the model exists in `agents.defaults.models`):

- `opus` → `anthropic/claude-opus-4-6`
- `sonnet` → `anthropic/claude-sonnet-4-5`
- `gpt` → `openai/gpt-5.2`
- `gpt-mini` → `openai/gpt-5-mini`
- `gemini` → `google/gemini-3-pro-preview`
- `gemini-flash` → `google/gemini-3-flash-preview`

If you set your own alias with the same name, your value wins.

### How do I defineoverride model shortcuts aliases

Aliases come from `agents.defaults.models.<modelId>.alias`. Example:

```json5
{
  agents: {
    defaults: {
      model: { primary: "anthropic/claude-opus-4-6" },
      models: {
        "anthropic/claude-opus-4-6": { alias: "opus" },
        "anthropic/claude-sonnet-4-5": { alias: "sonnet" },
        "anthropic/claude-haiku-4-5": { alias: "haiku" },
      },
    },
  },
}
```

Then `/model sonnet` (or `/<alias>` when supported) resolves to that model ID.

### How do I add models from other providers like OpenRouter or ZAI

OpenRouter (pay-per-token; many models):

```json5
{
  agents: {
    defaults: {
      model: { primary: "openrouter/anthropic/claude-sonnet-4-5" },
      models: { "openrouter/anthropic/claude-sonnet-4-5": {} },
    },
  },
  env: { OPENROUTER_API_KEY: "sk-or-..." },
}
```

Z.AI (GLM models):

```json5
{
  agents: {
    defaults: {
      model: { primary: "zai/glm-4.7" },
      models: { "zai/glm-4.7": {} },
    },
  },
  env: { ZAI_API_KEY: "..." },
}
```

If you reference a provider/model but the required provider key is missing, you'll get a runtime auth error (e.g. `No API key found for provider "zai"`).

**No API key found for provider after adding a new agent**

This usually means the **new agent** has an empty auth store. 认证是按代理划分的，并存储在：

```
~/.openclaw/agents/<agentId>/agent/auth-profiles.json
```

Fix options:

- Run `openclaw agents add <id>` and configure auth during the wizard.
- Or copy `auth-profiles.json` from the main agent's `agentDir` into the new agent's `agentDir`.

Do **not** reuse `agentDir` across agents; it causes auth/session collisions.

## Model failover and "All models failed"

### How does failover work

Failover happens in two stages:

1. **Auth profile rotation** within the same provider.
2. 1. **模型回退**到 `agents.defaults.model.fallbacks` 中的下一个模型。

2) 冷却时间适用于失败的配置（指数退避），因此即使某个提供方被限流或暂时失败，OpenClaw 也能继续响应。

### 3. 这个错误是什么意思

```
4. 未找到配置文件 "anthropic:default" 的凭据
```

5. 这表示系统尝试使用认证配置文件 ID `anthropic:default`，但在预期的认证存储中找不到它的凭据。

### 6. 解决“未找到配置文件 anthropicdefault 的凭据”的检查清单

- 7. **确认认证配置文件所在位置**（新路径 vs 旧路径）
  - 8. 当前：`~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
  - 旧版：`~/.openclaw/agent/*`（由 `openclaw doctor` 迁移）
- 10. **确认你的环境变量已被 Gateway 加载**
  - 11. 如果你在 shell 中设置了 `ANTHROPIC_API_KEY`，但通过 systemd/launchd 运行 Gateway，它可能无法继承该变量。 12. 将其放入 `~/.openclaw/.env`，或启用 `env.shellEnv`。
- **请确保你正在编辑的是正确的代理**
  - 14. 多 agent 设置意味着可能存在多个 `auth-profiles.json` 文件。
- 15. **对模型/认证状态进行健全性检查**
  - 16. 使用 `openclaw models status` 查看已配置的模型以及各提供方是否已通过认证。

17. 解决“未找到配置文件 anthropic 的凭据”的检查清单

18. 这意味着运行被固定到一个 Anthropic 认证配置文件，但 Gateway 在其认证存储中找不到它。

- 19. **使用 setup-token**
  - 20. 运行 `claude setup-token`，然后使用 `openclaw models auth setup-token --provider anthropic` 粘贴它。
  - 21. 如果该 token 是在另一台机器上创建的，请使用 `openclaw models auth paste-token --provider anthropic`。

- 22. **如果你想改用 API key**
  - 23. 在 **gateway 主机** 上将 `ANTHROPIC_API_KEY` 放入 `~/.openclaw/.env`。
  - 24. 清除任何强制使用缺失配置文件的固定顺序：

    ```bash
    openclaw models auth order clear --provider anthropic
    ```

- 26. **确认你是在 gateway 主机上运行命令**
  - 27. 在远程模式下，认证配置文件位于 gateway 机器上，而不是你的笔记本电脑。

### 28. 为什么它也尝试了 Google Gemini 并失败了

29. 如果你的模型配置将 Google Gemini 作为回退项（或者你切换到了 Gemini 的简写），OpenClaw 会在模型回退期间尝试它。 30. 如果你尚未配置 Google 凭据，你将看到 `No API key found for provider "google"`。

31. 修复方法：要么提供 Google 认证，要么在 `agents.defaults.model.fallbacks` / 别名中移除或避免使用 Google 模型，以免回退路由到那里。

32. **LLM request rejected message thinking signature required google antigravity**

33. 原因：会话历史包含**没有签名的 thinking 块**（通常来自中止/不完整的流）。 34. Google Antigravity 要求 thinking 块必须带有签名。

35. 修复：OpenClaw 现在会为 Google Antigravity Claude 移除未签名的 thinking 块。 36. 如果仍然出现，请开始一个**新会话**，或为该 agent 设置 `/thinking off`。

## 37. 认证配置文件：它们是什么以及如何管理

38. 相关：[ /concepts/oauth ](/concepts/oauth)（OAuth 流程、token 存储、多账户模式）

### 39. 什么是认证配置文件

40. 认证配置文件是一个与提供方绑定的、具名的凭据记录（OAuth 或 API key）。 41. 配置文件存放在：

```
~/.openclaw/agents/<agentId>/agent/auth-profiles.json
```

### 43. 常见的配置文件 ID 是什么

44. OpenClaw 使用带提供方前缀的 ID，例如：

- `anthropic:default`（在不存在邮箱身份时很常见）
- `anthropic:<email>` 用于 OAuth 身份
- 你选择的自定义 ID（例如 `anthropic:work`）

### 48. 我可以控制优先尝试哪个认证配置文件吗

49. 可以。 50. 配置支持为配置文件提供可选元数据，并为每个提供方设置顺序（`auth.order.<provider>`）\`). 这**不会**存储机密；它将 ID 映射到 provider/mode，并设置轮换顺序。

如果某个配置文件处于短暂的**冷却**状态（速率限制/超时/认证失败）或更长的**禁用**状态（计费/额度不足），OpenClaw 可能会临时跳过该配置文件。 要检查这一点，请运行 `openclaw models status --json` 并查看 `auth.unusableProfiles`。 调优：`auth.cooldowns.billingBackoffHours*`。

你也可以通过 CLI 设置**按代理**的顺序覆盖（存储在该代理的 `auth-profiles.json` 中）：

```bash
# Defaults to the configured default agent (omit --agent)
openclaw models auth order get --provider anthropic

# Lock rotation to a single profile (only try this one)
openclaw models auth order set --provider anthropic anthropic:default

# Or set an explicit order (fallback within provider)
openclaw models auth order set --provider anthropic anthropic:work anthropic:default

# Clear override (fall back to config auth.order / round-robin)
openclaw models auth order clear --provider anthropic
```

要指定特定代理：

```bash
openclaw models auth order set --provider anthropic --agent main anthropic:default
```

### OAuth 与 API key 有什么区别

OpenClaw 同时支持以下两种：

- **OAuth** 通常利用订阅访问（如适用）。
- **API keys** 使用按 token 计费。

向导明确支持 Anthropic 的 setup-token 和 OpenAI Codex OAuth，并可以为你存储 API 密钥。

## Gateway：端口、“already running”以及远程模式

### Gateway 使用哪个端口

`gateway.port` 控制用于 WebSocket + HTTP（控制 UI、hooks 等）的单一复用端口。

优先级：

```
--port > OPENCLAW_GATEWAY_PORT > gateway.port > 默认 18789
```

### 为什么 `openclaw gateway status` 显示 Runtime running 但 RPC probe failed

因为“running”是**监督器**的视角（launchd/systemd/schtasks）。 RPC 探测是 CLI 实际连接到 gateway WebSocket 并调用 `status`。

使用 `openclaw gateway status` 并相信这些行：

- `Probe target:`（探测实际使用的 URL）
- `Listening:`（端口上实际绑定的内容）
- `Last gateway error:`（当进程存活但端口未监听时的常见根因）

### 为什么 `openclaw gateway status` 显示 Config cli 和 Config service 不同

你在编辑一个配置文件，而服务正在运行另一个（通常是 `--profile` / `OPENCLAW_STATE_DIR` 不匹配）。

修复：

```bash
openclaw gateway install --force
```

从你希望服务使用的同一 `--profile` / 环境中运行该命令。

### “another gateway instance is already listening” 是什么意思

OpenClaw 通过在启动时立即绑定 WebSocket 监听器来强制执行运行时锁（默认 `ws://127.0.0.1:18789`）。 如果绑定因 `EADDRINUSE` 失败，它会抛出 `GatewayLockError`，表示已有另一个实例在监听。

修复：停止另一个实例、释放端口，或使用 `openclaw gateway --port <port>` 运行。

### 如何在远程模式下运行 OpenClaw，让客户端连接到其他地方的 Gateway

将 `gateway.mode: "remote"` 并指向远程 WebSocket URL，可选使用 token/password：

```json5
{
  gateway: {
    mode: "remote",
    remote: {
      url: "ws://gateway.tailnet:18789",
      token: "your-token",
      password: "your-password",
    },
  },
}
```

注意：

- 只有当 `gateway.mode` 为 `local`（或你传递了覆盖标志）时，`openclaw gateway` 才会启动。
- macOS 应用会监视配置文件，并在这些值更改时实时切换模式。

### 控制 UI 显示 unauthorized 或不断重连，现在怎么办

你的 gateway 以启用认证的方式运行（`gateway.auth.*`），但 UI 没有发送匹配的 token/password。

事实（来自代码）：

- 控制 UI 将 token 存储在浏览器 localStorage 的键 `openclaw.control.settings.v1` 中。

修复：

- 最快方式：`openclaw dashboard`（打印并复制仪表板 URL，尝试打开；若无界面则显示 SSH 提示）。
- 如果你还没有 token：`openclaw doctor --generate-gateway-token`。
- 如果是远程，先建立隧道：`ssh -N -L 18789:127.0.0.1:18789 user@host`，然后打开 `http://127.0.0.1:18789/`。
- 在 gateway 主机上设置 `gateway.auth.token`（或 `OPENCLAW_GATEWAY_TOKEN`）。
- In the Control UI settings, paste the same token.
- Still stuck? Run `openclaw status --all` and follow [Troubleshooting](/gateway/troubleshooting). See [Dashboard](/web/dashboard) for auth details.

### I set gatewaybind tailnet but it cant bind nothing listens

`tailnet` bind picks a Tailscale IP from your network interfaces (100.64.0.0/10). If the machine isn't on Tailscale (or the interface is down), there's nothing to bind to.

Fix:

- Start Tailscale on that host (so it has a 100.x address), or
- Switch to `gateway.bind: "loopback"` / `"lan"`.

Note: `tailnet` is explicit. `auto` prefers loopback; use `gateway.bind: "tailnet"` when you want a tailnet-only bind.

### Can I run multiple Gateways on the same host

Usually no - one Gateway can run multiple messaging channels and agents. Use multiple Gateways only when you need redundancy (ex: rescue bot) or hard isolation.

Yes, but you must isolate:

- `OPENCLAW_CONFIG_PATH` (per-instance config)
- `OPENCLAW_STATE_DIR` (per-instance state)
- `agents.defaults.workspace` (workspace isolation)
- `gateway.port` (unique ports)

Quick setup (recommended):

- 每个实例使用 `openclaw --profile <name> …`（会自动创建 `~/.openclaw-<name>`）。
- 在每个 profile 配置中设置唯一的 `gateway.port`（或在手动运行时传入 `--port`）。
- Install a per-profile service: `openclaw --profile <name> gateway install`.

Profiles also suffix service names (`bot.molt.<profile>`; legacy `com.openclaw.*`, `openclaw-gateway-<profile>.service`, `OpenClaw Gateway (<profile>)`).
完整指南：[Multiple gateways](/gateway/multiple-gateways)。

### What does invalid handshake code 1008 mean

The Gateway is a **WebSocket server**, and it expects the very first message to
be a `connect` frame. If it receives anything else, it closes the connection
with **code 1008** (policy violation).

Common causes:

- [安装和新手引导通常需要多长时间？](#how-long-does-install-and-onboarding-usually-take)
- You used the wrong port or path.
- A proxy or tunnel stripped auth headers or sent a non-Gateway request.

快速修复：

1. Use the WS URL: `ws://<host>:18789` (or `wss://...` if HTTPS).
2. Don't open the WS port in a normal browser tab.
3. If auth is on, include the token/password in the `connect` frame.

If you're using the CLI or TUI, the URL should look like:

```
openclaw tui --url ws://<host>:18789 --token <token>
```

Protocol details: [Gateway protocol](/gateway/protocol).

## Logging and debugging

### Where are logs

File logs (structured):

```
/tmp/openclaw/openclaw-YYYY-MM-DD.log
```

You can set a stable path via `logging.file`. File log level is controlled by `logging.level`. Console verbosity is controlled by `--verbose` and `logging.consoleLevel`.

Fastest log tail:

```bash
openclaw logs --follow
```

Service/supervisor logs (when the gateway runs via launchd/systemd):

- macOS: `$OPENCLAW_STATE_DIR/logs/gateway.log` and `gateway.err.log` (default: `~/.openclaw/logs/...`; profiles use `~/.openclaw-<profile>/logs/...`)
- Linux: `journalctl --user -u openclaw-gateway[-<profile>].service -n 200 --no-pager`
- Windows: `schtasks /Query /TN "OpenClaw Gateway (<profile>)" /V /FO LIST`

See [Troubleshooting](/gateway/troubleshooting#log-locations) for more.

### How do I startstoprestart the Gateway service

Use the gateway helpers:

```bash
openclaw gateway status
openclaw gateway restart
```

If you run the gateway manually, `openclaw gateway --force` can reclaim the port. See [Gateway](/gateway).

### I closed my terminal on Windows how do I restart OpenClaw

There are **two Windows install modes**:

**1) WSL2 (recommended):** the Gateway runs inside Linux.

打开 PowerShell，进入 WSL，然后重启：

```powershell
wsl
openclaw gateway status
openclaw gateway restart
```

If you never installed the service, start it in the foreground:

```bash
openclaw gateway run
```

**2) Native Windows (not recommended):** the Gateway runs directly in Windows.

Open PowerShell and run:

```powershell
openclaw gateway status
openclaw gateway restart
```

渠道配对/允许列表阻止回复（检查渠道配置 + 日志）。

```powershell
openclaw gateway run
```

Docs: [Windows (WSL2)](/platforms/windows), [Gateway service runbook](/gateway).

### The Gateway is up but replies never arrive What should I check

Start with a quick health sweep:

```bash
openclaw status
openclaw models status
openclaw channels status
openclaw logs --follow
```

Common causes:

- Model auth not loaded on the **gateway host** (check `models status`).
- Channel pairing/allowlist blocking replies (check channel config + logs).
- WebChat/Dashboard is open without the right token.

If you are remote, confirm the tunnel/Tailscale connection is up and that the
Gateway WebSocket is reachable.

Docs: [Channels](/channels), [Troubleshooting](/gateway/troubleshooting), [Remote access](/gateway/remote).

### Disconnected from gateway no reason what now

This usually means the UI lost the WebSocket connection. Check:

1. Is the Gateway running? `openclaw gateway status`
2. Is the Gateway healthy? `openclaw status`
3. Does the UI have the right token? `openclaw dashboard`
4. If remote, is the tunnel/Tailscale link up?

Then tail logs:

```bash
openclaw logs --follow
```

Docs: [Dashboard](/web/dashboard), [Remote access](/gateway/remote), [Troubleshooting](/gateway/troubleshooting).

### Telegram setMyCommands fails with network errors What should I check

Start with logs and channel status:

```bash
openclaw channels status
openclaw channels logs --channel telegram
```

If you are on a VPS or behind a proxy, confirm outbound HTTPS is allowed and DNS works.
If the Gateway is remote, make sure you are looking at logs on the Gateway host.

文档：[Telegram](/channels/telegram)，[Channel troubleshooting](/channels/troubleshooting)。

### TUI shows no output What should I check

First confirm the Gateway is reachable and the agent can run:

```bash
openclaw status
openclaw models status
openclaw logs --follow
```

In the TUI, use `/status` to see the current state. If you expect replies in a chat
channel, make sure delivery is enabled (`/deliver on`).

Docs: [TUI](/web/tui), [Slash commands](/tools/slash-commands).

### How do I completely stop then start the Gateway

If you installed the service:

```bash
openclaw gateway stop
openclaw gateway start
```

This stops/starts the **supervised service** (launchd on macOS, systemd on Linux).
Use this when the Gateway runs in the background as a daemon.

If you're running in the foreground, stop with Ctrl-C, then:

```bash
openclaw gateway run
```

Docs: [Gateway service runbook](/gateway).

### ELI5 openclaw gateway restart vs openclaw gateway

- `openclaw gateway restart`: restarts the **background service** (launchd/systemd).
- `openclaw gateway`: runs the gateway **in the foreground** for this terminal session.

If you installed the service, use the gateway commands. Use `openclaw gateway` when
you want a one-off, foreground run.

### 当某些东西失败时，获取更多细节的最快方式是什么

Start the Gateway with `--verbose` to get more console detail. 然后检查日志文件中的频道认证、模型路由和 RPC 错误。

## Media and attachments

### My skill generated an imagePDF but nothing was sent

Outbound attachments from the agent must include a `MEDIA:<path-or-url>` line (on its own line). See [OpenClaw assistant setup](/start/openclaw) and [Agent send](/tools/agent-send).

CLI 发送：

```bash
openclaw message send --target +15555550123 --message "Here you go" --media /path/to/file.png
```

Also check:

- The target channel supports outbound media and isn't blocked by allowlists.
- The file is within the provider's size limits (images are resized to max 2048px).

See [Images](/nodes/images).

## Security and access control

### Is it safe to expose OpenClaw to inbound DMs

Treat inbound DMs as untrusted input. Defaults are designed to reduce risk:

- Default behavior on DM-capable channels is **pairing**:
  - Unknown senders receive a pairing code; the bot does not process their message.
  - Approve with: `openclaw pairing approve <channel> <code>`
  - Pending requests are capped at **3 per channel**; check `openclaw pairing list <channel>` if a code didn't arrive.
- Opening DMs publicly requires explicit opt-in (`dmPolicy: "open"` and allowlist `"*"`).

Run `openclaw doctor` to surface risky DM policies.

### Is prompt injection only a concern for public bots

No. Prompt injection is about **untrusted content**, not just who can DM the bot.
If your assistant reads external content (web search/fetch, browser pages, emails,
docs, attachments, pasted logs), that content can include instructions that try
to hijack the model. This can happen even if **you are the only sender**.

The biggest risk is when tools are enabled: the model can be tricked into
exfiltrating context or calling tools on your behalf. Reduce the blast radius by:

- using a read-only or tool-disabled "reader" agent to summarize untrusted content
- keeping `web_search` / `web_fetch` / `browser` off for tool-enabled agents
- sandboxing and strict tool allowlists

Details: [Security](/gateway/security).

### Should my bot have its own email GitHub account or phone number

Yes, for most setups. Isolating the bot with separate accounts and phone numbers
reduces the blast radius if something goes wrong. This also makes it easier to rotate
credentials or revoke access without impacting your personal accounts.

Start small. Give access only to the tools and accounts you actually need, and expand
later if required.

Docs: [Security](/gateway/security), [Pairing](/channels/pairing).

### Can I give it autonomy over my text messages and is that safe

We do **not** recommend full autonomy over your personal messages. The safest pattern is:

- Keep DMs in **pairing mode** or a tight allowlist.
- Use a **separate number or account** if you want it to message on your behalf.
- Let it draft, then **approve before sending**.

If you want to experiment, do it on a dedicated account and keep it isolated. See
[Security](/gateway/security).

### Can I use cheaper models for personal assistant tasks

Yes, **if** the agent is chat-only and the input is trusted. Smaller tiers are
more susceptible to instruction hijacking, so avoid them for tool-enabled agents
or when reading untrusted content. 如果你必须使用较小的模型，请限制工具并在沙箱中运行。 See [Security](/gateway/security).

### I ran start in Telegram but didnt get a pairing code

Pairing codes are sent **only** when an unknown sender messages the bot and
`dmPolicy: "pairing"` is enabled. `/start` by itself doesn't generate a code.

Check pending requests:

```bash
openclaw pairing list telegram
```

If you want immediate access, allowlist your sender id or set `dmPolicy: "open"`
for that account.

### WhatsApp will it message my contacts How does pairing work

No. WhatsApp 私聊的默认策略是**配对**。 Unknown senders only get a pairing code and their message is **not processed**. OpenClaw only replies to chats it receives or to explicit sends you trigger.

Approve pairing with:

```bash
openclaw pairing approve whatsapp <code>
```

列出待处理请求：

```bash
openclaw pairing list whatsapp
```

Wizard phone number prompt: it's used to set your **allowlist/owner** so your own DMs are permitted. It's not used for auto-sending. If you run on your personal WhatsApp number, use that number and enable `channels.whatsapp.selfChatMode`.

## Chat commands, aborting tasks, and "it won't stop"

### How do I stop internal system messages from showing in chat

Most internal or tool messages only appear when **verbose** or **reasoning** is enabled
for that session.

Fix in the chat where you see it:

```
/verbose off
/reasoning off
```

If it is still noisy, check the session settings in the Control UI and set verbose
to **inherit**. Also confirm you are not using a bot profile with `verboseDefault` set
to `on` in config.

Docs: [Thinking and verbose](/tools/thinking), [Security](/gateway/security#reasoning--verbose-output-in-groups).

### How do I stopcancel a running task

Send any of these **as a standalone message** (no slash):

```
stop
abort
esc
wait
exit
interrupt
```

These are abort triggers (not slash commands).

For background processes (from the exec tool), you can ask the agent to run:

```
process action:kill sessionId:XXX
```

斜杠命令概览：参见 [Slash commands](/tools/slash-commands)。

Most commands must be sent as a **standalone** message that starts with `/`, but a few shortcuts (like `/status`) also work inline for allowlisted senders.

### How do I send a Discord message from Telegram Crosscontext messaging denied

OpenClaw blocks **cross-provider** messaging by default. If a tool call is bound
to Telegram, it won't send to Discord unless you explicitly allow it.

Enable cross-provider messaging for the agent:

```json5
{
  agents: {
    defaults: {
      tools: {
        message: {
          crossContext: {
            allowAcrossProviders: true,
            marker: { enabled: true, prefix: "[from {channel}] " },
          },
        },
      },
    },
  },
}
```

Restart the gateway after editing config. If you only want this for a single
agent, set it under `agents.list[].tools.message` instead.

### Why does it feel like the bot ignores rapidfire messages

队列模式控制新消息如何与正在进行的运行交互。 Use `/queue` to change modes:

- `steer` - new messages redirect the current task
- `followup` - run messages one at a time
- `collect` - batch messages and reply once (default)
- `steer-backlog` - steer now, then process backlog
- `interrupt` - 中止当前运行并重新开始

You can add options like `debounce:2s cap:25 drop:summarize` for followup modes.

## 准确回答截图/聊天记录中的具体问题

**Q: "What's the default model for Anthropic with an API key?"**

**A:** In OpenClaw, credentials and model selection are separate. 设置 `ANTHROPIC_API_KEY`（或在认证配置中存储 Anthropic API 密钥）可以启用认证，但实际的默认模型取决于你在 `agents.defaults.model.primary` 中的配置（例如 `anthropic/claude-sonnet-4-5` 或 `anthropic/claude-opus-4-6`）。 If you see `No credentials found for profile "anthropic:default"`, it means the Gateway couldn't find Anthropic credentials in the expected `auth-profiles.json` for the agent that's running.

---

Still stuck? Ask in [Discord](https://discord.com/invite/clawd) or open a [GitHub discussion](https://github.com/openclaw/openclaw/discussions).
