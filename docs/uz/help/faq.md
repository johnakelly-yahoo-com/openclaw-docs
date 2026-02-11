---
summary: "OpenClaw sozlash, konfiguratsiya va foydalanish bo‘yicha tez-tez beriladigan savollar"
title: "FAQ"
---

# FAQ

Haqiqiy muhitlar uchun tezkor javoblar va chuqurroq nosozliklarni bartaraf etish (lokal dev, VPS, multi-agent, OAuth/API kalitlari, model failover). Ish vaqtida diagnostika uchun [Troubleshooting](/gateway/troubleshooting) ga qarang. To‘liq konfiguratsiya ma’lumotnomasi uchun [Configuration](/gateway/configuration) ga qarang.

## 1. Mundarija

- 2. [Tezkor boshlash va birinchi ishga tushirish sozlamalari]
  - 3. [Qotib qoldim — tezda qanday chiqib ketish mumkin?](#im-stuck-whats-the-fastest-way-to-get-unstuck)
  - 4. [OpenClaw’ni o‘rnatish va sozlashning tavsiya etilgan usuli qanday?](#whats-the-recommended-way-to-install-and-set-up-openclaw)
  - 5. [Onboardingdan keyin boshqaruv panelini qanday ochaman?](#how-do-i-open-the-dashboard-after-onboarding)
  - 6. [Boshqaruv panelini (token) localhost va masofaviy muhitda qanday autentifikatsiya qilaman?](#how-do-i-authenticate-the-dashboard-token-on-localhost-vs-remote)
  - 7. [Qaysi runtime kerak?](#what-runtime-do-i-need)
  - 8. [Raspberry Pi’da ishlaydimi?](#does-it-run-on-raspberry-pi)
  - 9. [Raspberry Pi o‘rnatishlari uchun maslahatlar bormi?](#any-tips-for-raspberry-pi-installs)
  - 10. ["wake up my friend"da qotib qolgan / onboarding ishga tushmayapti.
    11. Endi nima qilaman?](#it-is-stuck-on-wake-up-my-friend-onboarding-will-not-hatch-what-now) 12. [Onboardingni qayta qilmasdan sozlamamni yangi mashinaga (Mac mini) ko‘chira olamanmi?](#can-i-migrate-my-setup-to-a-new-machine-mac-mini-without-redoing-onboarding)
  - 13. [So‘nggi versiyada nimalar yangilanganini qayerdan ko‘raman?](#where-do-i-see-what-is-new-in-the-latest-version)
  - 14. [docs.openclaw.ai’ga kira olmayapman (SSL xatosi).
    15. Endi nima?](#i-cant-access-docsopenclawai-ssl-error-what-now)
  - 16. [Stable va beta o‘rtasidagi farq nima?](#whats-the-difference-between-stable-and-beta) 17. [Beta versiyani qanday o‘rnataman va beta bilan dev o‘rtasidagi farq nima?](#how-do-i-install-the-beta-version-and-whats-the-difference-between-beta-and-dev)
  - 18. [Eng so‘nggi yangiliklarni qanday sinab ko‘raman?](#how-do-i-try-the-latest-bits)
  - 19. [O‘rnatish va onboarding odatda qancha vaqt oladi?](#how-long-does-install-and-onboarding-usually-take)
  - 20. [O‘rnatgich qotib qoldimi?
    21. Qanday qilib ko‘proq ma’lumot olaman?](#installer-stuck-how-do-i-get-more-feedback)
  - 22. [Windows o‘rnatishda git topilmadi yoki openclaw tan olinmadi deb chiqyapti](#windows-install-says-git-not-found-or-openclaw-not-recognized)
  - 23. [Hujjatlar savolimga javob bermadi — yaxshiroq javobni qanday olaman?](#the-docs-didnt-answer-my-question-how-do-i-get-a-better-answer) 24. [OpenClaw’ni Linux’da qanday o‘rnataman?](#how-do-i-install-openclaw-on-linux)
  - 25. [OpenClaw’ni VPS’da qanday o‘rnataman?](#how-do-i-install-openclaw-on-a-vps)
  - 26. [Bulut/VPS o‘rnatish qo‘llanmalari qayerda?](#where-are-the-cloudvps-install-guides)
  - 27. [OpenClaw’dan o‘zini yangilashni so‘rasa bo‘ladimi?](#can-i-ask-openclaw-to-update-itself)
  - 28. [Onboarding ustasi aslida nima qiladi?](#what-does-the-onboarding-wizard-actually-do)
  - 29. [Buni ishga tushirish uchun Claude yoki OpenAI obunasi kerakmi?](#do-i-need-a-claude-or-openai-subscription-to-run-this)
  - 30. [API kalitisiz Claude Max obunasidan foydalana olamanmi](#can-i-use-claude-max-subscription-without-an-api-key)
  - 31. [Anthropic "setup-token" autentifikatsiyasi qanday ishlaydi?](#how-does-anthropic-setuptoken-auth-work)
  - 32. [Anthropic setup-token’ni qayerdan topaman?](#where-do-i-find-an-anthropic-setuptoken)
  - 33. [Claude obuna autentifikatsiyasini (Claude Pro yoki Max) qo‘llab-quvvatlaysizmi?](#do-you-support-claude-subscription-auth-claude-pro-or-max)
  - 34. [Nega Anthropic’dan `HTTP 429: rate_limit_error` ko‘ryapman?](#why-am-i-seeing-http-429-ratelimiterror-from-anthropic)
  - 35. [AWS Bedrock qo‘llab-quvvatlanadimi?](#is-aws-bedrock-supported)
  - 36. [Codex autentifikatsiyasi qanday ishlaydi?](#how-does-codex-auth-work)
  - 37. [OpenAI obuna autentifikatsiyasini (Codex OAuth) qo‘llab-quvvatlaysizmi?](#do-you-support-openai-subscription-auth-codex-oauth)
  - 38. [Gemini CLI OAuth’ni qanday sozlayman](#how-do-i-set-up-gemini-cli-oauth)
  - 39. [Oddiy suhbatlar uchun lokal model yetarlimi?](#is-a-local-model-ok-for-casual-chats)
  - 40. [Xostlangan model trafikini ma’lum bir hududda qanday saqlayman?](#how-do-i-keep-hosted-model-traffic-in-a-specific-region)
  - 41. [Buni o‘rnatish uchun Mac Mini sotib olishim shartmi?](#do-i-have-to-buy-a-mac-mini-to-install-this)
  - 42. [iMessage qo‘llab-quvvatlashi uchun Mac mini kerakmi?](#do-i-need-a-mac-mini-for-imessage-support)
  - 43. [Agar OpenClaw’ni ishga tushirish uchun Mac mini olsam, uni MacBook Pro’ga ulay olamanmi?](#if-i-buy-a-mac-mini-to-run-openclaw-can-i-connect-it-to-my-macbook-pro)
  - 44. [Bun’dan foydalansam bo‘ladimi?](#can-i-use-bun)
  - 45. [Telegram: `allowFrom`ga nima yoziladi?](#telegram-what-goes-in-allowfrom)
  - 46. [Bir nechta odam bitta WhatsApp raqamini turli OpenClaw instansiyalari bilan ishlata oladimi?](#can-multiple-people-use-one-whatsapp-number-with-different-openclaw-instances)
  - 47. ["tezkor chat" agenti va "kodlash uchun Opus" agentini bir vaqtda ishga tushira olamanmi?](#can-i-run-a-fast-chat-agent-and-an-opus-for-coding-agent)
  - 48. [Homebrew Linux’da ishlaydimi?](#does-homebrew-work-on-linux)
  - 49. [Hacklanadigan (git) o‘rnatish bilan npm o‘rnatish o‘rtasidagi farq nima?](#whats-the-difference-between-the-hackable-git-install-and-npm-install)
  - 50. [Keyinroq npm va git o‘rnatishlari o‘rtasida almasha olamanmi?](#can-i-switch-between-npm-and-git-installs-later)
  - [Does Homebrew work on Linux?](#does-homebrew-work-on-linux)
  - [What's the difference between the hackable (git) install and npm install?](#whats-the-difference-between-the-hackable-git-install-and-npm-install)
  - [Can I switch between npm and git installs later?](#can-i-switch-between-npm-and-git-installs-later)
  - [Gateway’ni noutbukimda yoki VPS’da ishga tushirishim kerakmi?](#should-i-run-the-gateway-on-my-laptop-or-a-vps)
  - [OpenClaw’ni alohida ajratilgan mashinada ishga tushirish qanchalik muhim?](#how-important-is-it-to-run-openclaw-on-a-dedicated-machine)
  - [VPS uchun minimal talablar va tavsiya etilgan OS qaysilar?](#what-are-the-minimum-vps-requirements-and-recommended-os)
  - [OpenClaw’ni VM’da ishga tushira olamanmi va talablar qanday?](#can-i-run-openclaw-in-a-vm-and-what-are-the-requirements)
- [OpenClaw nima?](#what-is-openclaw)
  - [Bir paragrafda OpenClaw nima?](#what-is-openclaw-in-one-paragraph)
  - [Qiymat taklifi nimadan iborat?](#whats-the-value-proposition)
  - [Endi sozlab bo‘ldim, avval nima qilishim kerak?](#i-just-set-it-up-what-should-i-do-first)
  - [OpenClaw’ning kundalik eng yaxshi besh foydalanish holati qaysilar?](#what-are-the-top-five-everyday-use-cases-for-openclaw)
  - [OpenClaw SaaS uchun lead gen, outreach, reklama va bloglar bilan yordam bera oladimi?](#can-openclaw-help-with-lead-gen-outreach-ads-and-blogs-for-a-saas)
  - [Veb-dasturlashda Claude Code bilan solishtirganda qanday afzalliklari bor?](#what-are-the-advantages-vs-claude-code-for-web-development)
- [Ko‘nikmalar va avtomatlashtirish](#skills-and-automation)
  - [Repo’ni iflos qilmasdan ko‘nikmalarni qanday sozlayman?](#how-do-i-customize-skills-without-keeping-the-repo-dirty)
  - [Ko‘nikmalarni maxsus papkadan yuklay olamanmi?](#can-i-load-skills-from-a-custom-folder)
  - [Turli vazifalar uchun turli modellardan qanday foydalanaman?](#how-can-i-use-different-models-for-different-tasks)
  - Bot og‘ir ishlarni bajarayotganda qotib qoladi.
    Qanday qilib buni offload qilaman? Cron yoki eslatmalar ishga tushmayapti.
    Nimani tekshirishim kerak?
  - [Linux’da ko‘nikmalarni qanday o‘rnataman?](#how-do-i-install-skills-on-linux) [OpenClaw vazifalarni jadval asosida yoki fon rejimida uzluksiz bajara oladimi?](#can-openclaw-run-tasks-on-a-schedule-or-continuously-in-the-background)
  - [Linux’dan Apple macOS’ga xos ko‘nikmalarni ishga tushira olamanmi?](#can-i-run-apple-macos-only-skills-from-linux)
  - [Notion yoki HeyGen integratsiyangiz bormi?](#do-you-have-a-notion-or-heygen-integration)
  - [Brauzerni egallash (browser takeover) uchun Chrome kengaytmasini qanday o‘rnataman?](#how-do-i-install-the-chrome-extension-for-browser-takeover)
  - [Sandboxing va xotira](#sandboxing-and-memory)
  - [Sandboxing bo‘yicha alohida hujjat bormi?](#is-there-a-dedicated-sandboxing-doc)
- [Xost papkasini sandbox ichiga qanday bog‘layman?](#how-do-i-bind-a-host-folder-into-the-sandbox)
  - [Xotira qanday ishlaydi?](#how-does-memory-work)
  - Xotira narsalarni unutib yuboryapti.
    Buni qanday qilib mustahkamlayman?
  - Xotira abadiy saqlanadimi?
    Cheklovlar qanday?
  - [Semantik xotira qidiruvi uchun OpenAI API kaliti kerakmi?](#does-semantic-memory-search-require-an-openai-api-key) [Diskda narsalar qayerda joylashadi](#where-things-live-on-disk)
  - [OpenClaw bilan ishlatiladigan barcha ma’lumotlar lokalda saqlanadimi?](#is-all-data-used-with-openclaw-saved-locally) [OpenClaw o‘z ma’lumotlarini qayerda saqlaydi?](#where-does-openclaw-store-its-data)
  - [AGENTS.md / SOUL.md / USER.md / MEMORY.md qayerda joylashishi kerak?](#where-should-agentsmd-soulmd-usermd-memorymd-live)
- [Tavsiya etilgan zaxira nusxa (backup) strategiyasi qanday?](#whats-the-recommended-backup-strategy)
  - [OpenClaw’ni to‘liq qanday o‘chirib tashlayman?](#how-do-i-completely-uninstall-openclaw)
  - [Agentlar workspace’dan tashqarida ishlay oladimi?](#can-agents-work-outside-the-workspace)
  - [Remote rejimdaman — sessiya saqlovi qayerda?](#im-in-remote-mode-where-is-the-session-store)
  - [Konfiguratsiya asoslari](#config-basics)
  - Konfiguratsiya qaysi formatda?
    Qayerda joylashgan?
  - [Men `gateway.bind: "lan"` (yoki `"tailnet"`) ni o‘rnatdim va endi hech narsa tinglamayapti / UI "unauthorized" deydi](#i-set-gatewaybind-lan-or-tailnet-and-now-nothing-listens-the-ui-says-unauthorized)
  - [Nega endi localhost’da token kerak?](#why-do-i-need-a-token-on-localhost-now)
- [Konfiguratsiyani o‘zgartirgandan keyin qayta ishga tushirishim shartmi?](#do-i-have-to-restart-after-changing-config)
  - [Veb qidiruvni (va web fetch’ni) qanday yoqaman?](#how-do-i-enable-web-search-and-web-fetch) config.apply mening konfiguratsiyamni o‘chirib yubordi.
    Qanday tiklayman va buni qanday oldini olaman?
  - [I set `gateway.bind: "lan"` (or `"tailnet"`) and now nothing listens / the UI says unauthorized](#i-set-gatewaybind-lan-or-tailnet-and-now-nothing-listens-the-ui-says-unauthorized)
  - [Why do I need a token on localhost now?](#why-do-i-need-a-token-on-localhost-now)
  - [Do I have to restart after changing config?](#do-i-have-to-restart-after-changing-config)
  - [How do I enable web search (and web fetch)?](#how-do-i-enable-web-search-and-web-fetch)
  - [config.apply wiped my config. How do I recover and avoid this?](#configapply-wiped-my-config-how-do-i-recover-and-avoid-this)
  - [Qanday qilib markaziy Gateway’ni qurilmalar bo‘ylab ixtisoslashgan worker’lar bilan ishga tushiraman?](#how-do-i-run-a-central-gateway-with-specialized-workers-across-devices)
  - [OpenClaw brauzeri headless rejimda ishlay oladimi?](#can-the-openclaw-browser-run-headless)
  - [Brauzerni boshqarish uchun Brave’dan qanday foydalanaman?](#how-do-i-use-brave-for-browser-control)
- [Masofaviy gateway’lar va node’lar](#remote-gateways-and-nodes)
  - [Buyruqlar Telegram, gateway va node’lar o‘rtasida qanday uzatiladi?](#how-do-commands-propagate-between-telegram-the-gateway-and-nodes)
  - [Agar Gateway masofada joylashtirilgan bo‘lsa, agentim kompyuterimga qanday kira oladi?](#how-can-my-agent-access-my-computer-if-the-gateway-is-hosted-remotely)
  - Tailscale ulangan, lekin javoblar yo‘q.
    8. Endi nima qilaman? [Ikki OpenClaw instansiyasi (local + VPS) o‘zaro gaplasha oladimi?](#can-two-openclaw-instances-talk-to-each-other-local-vps)
  - [Bir nechta agentlar uchun alohida VPS’lar kerakmi?](#do-i-need-separate-vpses-for-multiple-agents)
  - [Shaxsiy noutbukimda node ishlatishning VPS’dan SSH orqali ulanishga nisbatan foydasi bormi?](#is-there-a-benefit-to-using-a-node-on-my-personal-laptop-instead-of-ssh-from-a-vps)
  - [Node’lar gateway servisni ishga tushiradimi?](#do-nodes-run-a-gateway-service)
  - [Config’ni qo‘llash uchun API / RPC usuli bormi?](#is-there-an-api-rpc-way-to-apply-config)
  - [Birinchi o‘rnatish uchun minimal “sog‘lom” config qanday bo‘lishi kerak?](#whats-a-minimal-sane-config-for-a-first-install)
  - [VPS’da Tailscale’ni qanday sozlayman va Mac’dan qanday ulanaman?](#how-do-i-set-up-tailscale-on-a-vps-and-connect-from-my-mac)
  - [Mac node’ni masofaviy Gateway’ga qanday ulayman (Tailscale Serve)?](#how-do-i-connect-a-mac-node-to-a-remote-gateway-tailscale-serve)
  - [Ikkinchi noutbukga o‘rnataymi yoki shunchaki node qo‘shaymi?](#should-i-install-on-a-second-laptop-or-just-add-a-node)
  - [Env o‘zgaruvchilari va .env yuklanishi](#env-vars-and-env-loading)
- [OpenClaw muhit o‘zgaruvchilarini qanday yuklaydi?](#how-does-openclaw-load-environment-variables)
  - “Gateway’ni servis orqali ishga tushirdim va env o‘zgaruvchilarim yo‘qolib qoldi.”
    21. Endi nima?
  - COPILOT_GITHUB_TOKEN [Sessiyalar va bir nechta chatlar](#sessions-and-multiple-chats)
  - [Yangi suhbatni qanday boshlayman?](#how-do-i-start-a-fresh-conversation) [Agar hech qachon `/new` yubormasam, sessiyalar avtomatik tarzda reset bo‘ladimi?](#do-sessions-reset-automatically-if-i-never-send-new)
- [Bir CEO va ko‘plab agentlardan iborat OpenClaw instansiyalari jamoasini yaratishning yo‘li bormi?](#is-there-a-way-to-make-a-team-of-openclaw-instances-one-ceo-and-many-agents)
  - Nega kontekst vazifa o‘rtasida qisqartirildi?
    29. Buni qanday oldini olaman?
  - [OpenClaw’ni to‘liq reset qilib, lekin o‘rnatilgan holda qanday qoldiraman?](#how-do-i-completely-reset-openclaw-but-keep-it-installed)
  - [“Context too large” xatolarini olyapman — qanday reset yoki ixchamlashtiraman?](#im-getting-context-too-large-errors-how-do-i-reset-or-compact)
  - [Nega “LLM request rejected: messages.N.content.X.tool_use.input: Field required” xabarini ko‘ryapman?](#why-am-i-seeing-llm-request-rejected-messagesncontentxtooluseinput-field-required) [Nega har 30 daqiqada heartbeat xabarlari olyapman?](#why-am-i-getting-heartbeat-messages-every-30-minutes)
  - [WhatsApp guruhiga “bot account” qo‘shishim kerakmi?](#do-i-need-to-add-a-bot-account-to-a-whatsapp-group)
  - [WhatsApp guruhi JID’sini qanday olaman?](#how-do-i-get-the-jid-of-a-whatsapp-group)
  - [Nega OpenClaw guruhda javob bermayapti?](#why-doesnt-openclaw-reply-in-a-group)
  - [Guruhlar/threads’lar DM’lar bilan kontekstni bo‘lishadimi?](#do-groupsthreads-share-context-with-dms)
  - [Qancha workspace va agent yaratishim mumkin?](#how-many-workspaces-and-agents-can-i-create)
  - [Bir vaqtning o‘zida bir nechta bot yoki chatlarni (Slack) ishga tushira olamanmi va buni qanday sozlash kerak?](#can-i-run-multiple-bots-or-chats-at-the-same-time-slack-and-how-should-i-set-that-up)
  - [Modellar: standartlar, tanlash, aliaslar, almashtirish](#models-defaults-selection-aliases-switching)
  - [“Default model” nima?](#what-is-the-default-model)
  - [Qaysi modelni tavsiya qilasiz?](#what-model-do-you-recommend)
  - [Config’ni o‘chirib yubormasdan modellerni qanday almashtiraman?](#how-do-i-switch-models-without-wiping-my-config)
- [O‘zim joylashtirgan modellarni (llama.cpp, vLLM, Ollama) ishlata olamanmi?](#can-i-use-selfhosted-models-llamacpp-vllm-ollama)
  - [OpenClaw, Flawd va Krill qaysi modellarni ishlatadi?](#what-do-openclaw-flawd-and-krill-use-for-models)
  - [Restart qilmasdan modellarni real vaqtda qanday almashtiraman?](#how-do-i-switch-models-on-the-fly-without-restarting)
  - [Kundalik vazifalar uchun GPT 5.2 va kod yozish uchun Codex 5.3 dan foydalana olamanmi?](#can-i-use-gpt-52-for-daily-tasks-and-codex-53-for-coding)
  - Nega “Model …
    49. ruxsat etilmagan” degan xabarni ko‘raman va keyin javob bo‘lmaydi?
  - [Nega “Unknown model: minimax/MiniMax-M2.1” degan xabarni ko‘ryapman?](#why-do-i-see-unknown-model-minimaxminimaxm21)
  - [How do I switch models on the fly (without restarting)?](#how-do-i-switch-models-on-the-fly-without-restarting)
  - [Can I use GPT 5.2 for daily tasks and Codex 5.3 for coding](#can-i-use-gpt-52-for-daily-tasks-and-codex-53-for-coding)
  - [Why do I see "Model … is not allowed" and then no reply?](#why-do-i-see-model-is-not-allowed-and-then-no-reply)
  - [Why do I see "Unknown model: minimax/MiniMax-M2.1"?](#why-do-i-see-unknown-model-minimaxminimaxm21)
  - [MiniMax’ni asosiy model sifatida, murakkab vazifalar uchun esa OpenAI’dan foydalana olamanmi?](#can-i-use-minimax-as-my-default-and-openai-for-complex-tasks)
  - [opus / sonnet / gpt ichki yorliqlarmi?](#are-opus-sonnet-gpt-builtin-shortcuts)
  - [Model yorliqlarini (aliaslarni) qanday aniqlash yoki bekor qilish mumkin?](#how-do-i-defineoverride-model-shortcuts-aliases)
  - [OpenRouter yoki Z.AI kabi boshqa provayderlardan modellarni qanday qo‘shaman?](#how-do-i-add-models-from-other-providers-like-openrouter-or-zai)
- [Model failover’i va "Barcha modellar muvaffaqiyatsiz tugadi"](#model-failover-and-all-models-failed)
  - [Failover qanday ishlaydi?](#how-does-failover-work)
  - [Bu xato nimani anglatadi?](#what-does-this-error-mean)
  - [`No credentials found for profile "anthropic:default"` xatosi uchun tuzatish ro‘yxati](#fix-checklist-for-no-credentials-found-for-profile-anthropicdefault)
  - [Nega u Google Gemini’ni ham sinab ko‘rdi va muvaffaqiyatsiz bo‘ldi?](#why-did-it-also-try-google-gemini-and-fail)
- [Auth profillar: ular nima va qanday boshqariladi](#auth-profiles-what-they-are-and-how-to-manage-them)
  - [Auth profil nima?](#what-is-an-auth-profile)
  - [Odatdagi profil ID’lari qaysilar?](#what-are-typical-profile-ids)
  - [Qaysi auth profil birinchi bo‘lib sinab ko‘rilishini boshqara olamanmi?](#can-i-control-which-auth-profile-is-tried-first)
  - [OAuth va API kaliti: farqi nimada?](#oauth-vs-api-key-whats-the-difference)
- [Gateway: portlar, "allaqachon ishlayapti" va masofaviy rejim](#gateway-ports-already-running-and-remote-mode)
  - [Gateway qaysi portdan foydalanadi?](#what-port-does-the-gateway-use)
  - [Nega `openclaw gateway status` `Runtime: running` deb ko‘rsatadi, lekin `RPC probe: failed`?](#why-does-openclaw-gateway-status-say-runtime-running-but-rpc-probe-failed)
  - [Nega `openclaw gateway status` da `Config (cli)` va `Config (service)` har xil ko‘rsatiladi?](#why-does-openclaw-gateway-status-show-config-cli-and-config-service-different)
  - ["another gateway instance is already listening" nimani anglatadi?](#what-does-another-gateway-instance-is-already-listening-mean)
  - [OpenClaw’ni masofaviy rejimda qanday ishga tushiraman (mijoz boshqa joydagi Gateway’ga ulanadi)?](#how-do-i-run-openclaw-in-remote-mode-client-connects-to-a-gateway-elsewhere)
  - Control UI’da "unauthorized" chiqyapti (yoki qayta-qayta ulanmoqda).
    22. Endi nima qilish kerak? [`gateway.bind: "tailnet"` qilib sozladim, lekin u bog‘lana olmayapti / hech narsa tinglamayapti](#i-set-gatewaybind-tailnet-but-it-cant-bind-nothing-listens)
  - [Bir xostda bir nechta Gateway’ni ishga tushira olamanmi?](#can-i-run-multiple-gateways-on-the-same-host)
  - ["invalid handshake" / 1008 kodi nimani anglatadi?](#what-does-invalid-handshake-code-1008-mean)
  - [Loglar va nosozliklarni tuzatish](#logging-and-debugging)
- [Loglar qayerda?](#where-are-logs)
  - [Gateway xizmatini qanday ishga tushirish/to‘xtatish/qayta ishga tushirish mumkin?](#how-do-i-startstoprestart-the-gateway-service)
  - [Windows’da terminalni yopib yubordim — OpenClaw’ni qanday qayta ishga tushiraman?](#i-closed-my-terminal-on-windows-how-do-i-restart-openclaw)
  - Gateway ishlayapti, lekin javoblar kelmayapti.
    31. Nimalarni tekshirishim kerak?
  - ["Disconnected from gateway: no reason" — endi nima?](#disconnected-from-gateway-no-reason-what-now) Telegram’da setMyCommands tarmoq xatolari bilan muvaffaqiyatsiz tugayapti.
    34. Nimalarni tekshirishim kerak?
  - TUI hech qanday chiqish ko‘rsatmayapti.
    36. Nimalarni tekshirishim kerak?
  - [Gateway’ni to‘liq to‘xtatib, keyin qayta qanday ishga tushiraman?](#how-do-i-completely-stop-then-start-the-gateway) [ELI5: `openclaw gateway restart` va `openclaw gateway` o‘rtasidagi farq](#eli5-openclaw-gateway-restart-vs-openclaw-gateway)
  - [Biror narsa ishlamay qolsa, eng tezkor tarzda qanday qilib ko‘proq tafsilot olish mumkin?](#whats-the-fastest-way-to-get-more-details-when-something-fails) [Media va ilovalar](#media-and-attachments)
  - [Mening ko‘nikmam rasm/PDF yaratdi, lekin hech narsa yuborilmadi](#my-skill-generated-an-imagepdf-but-nothing-was-sent)
  - [Xavfsizlik va kirishni boshqarish](#security-and-access-control)
  - [OpenClaw’ni kiruvchi DM’lar uchun ochish xavfsizmi?](#is-it-safe-to-expose-openclaw-to-inbound-dms)
- [Prompt injection faqat ommaviy botlar uchun muammomi?](#is-prompt-injection-only-a-concern-for-public-bots)
  - [Botimning o‘z emaili, GitHub akkaunti yoki telefon raqami bo‘lishi kerakmi?](#should-my-bot-have-its-own-email-github-account-or-phone-number)
- 16. [Xavfsizlik va kirish nazorati](#security-and-access-control)
  - 17. [OpenClaw’ni kiruvchi DMlar uchun ochish xavfsizmi?](#is-it-safe-to-expose-openclaw-to-inbound-dms)
  - [Telegram’da `/start` ni ishga tushirdim, lekin juftlash kodi kelmadi](#i-ran-start-in-telegram-but-didnt-get-a-pairing-code)
  - WhatsApp: u mening kontaktlarimga xabar yuboradimi?
    50. Juftlash qanday ishlaydi?
  - [Can I give it autonomy over my text messages and is that safe](#can-i-give-it-autonomy-over-my-text-messages-and-is-that-safe)
  - [Can I use cheaper models for personal assistant tasks?](#can-i-use-cheaper-models-for-personal-assistant-tasks)
  - [I ran `/start` in Telegram but didn't get a pairing code](#i-ran-start-in-telegram-but-didnt-get-a-pairing-code)
  - [WhatsApp: will it message my contacts? How does pairing work?](#whatsapp-will-it-message-my-contacts-how-does-pairing-work)
- [Chat buyruqlari, vazifalarni bekor qilish va "u to‘xtamayapti"](#chat-commands-aborting-tasks-and-it-wont-stop)
  - [Chatda ichki tizim xabarlari ko‘rinishini qanday to‘xtataman](#how-do-i-stop-internal-system-messages-from-showing-in-chat)
  - [Ishlayotgan vazifani qanday to‘xtataman/bekor qilaman?](#how-do-i-stopcancel-a-running-task)
  - [Telegramdan Discord xabarini qanday yuboraman? ("Kontekstlararo xabar yuborish rad etildi")](#how-do-i-send-a-discord-message-from-telegram-crosscontext-messaging-denied)
  - [Nega bot tez-tez yuborilgan xabarlarni "e’tiborsiz qoldirgandek" tuyuladi?](#why-does-it-feel-like-the-bot-ignores-rapidfire-messages)

## Agar nimadir buzilgan bo‘lsa, dastlabki 60 soniya

1. **Tezkor holat (birinchi tekshiruv)**

   ```bash
   openclaw holati
   ```

   Tezkor lokal xulosa: OS + yangilanish, gateway/xizmatga ulanish imkoniyati, agentlar/sessiyalar, provayder sozlamalari + ish vaqtidagi muammolar (gateway mavjud bo‘lsa).

2. 18. **Yopishtirish mumkin bo‘lgan hisobot (ulashish uchun xavfsiz)**

   ```bash
   openclaw status --all
   ```

   Faqat o‘qish uchun diagnostika va logning oxiri (tokenlar yashirilgan).

3. **Demon + port holati**

   ```bash
   openclaw gateway status
   ```

   Supervisor ish vaqti va RPC ulanishi, tekshiruv nishon URL manzili hamda xizmat qaysi konfiguratsiyadan foydalanganini ko‘rsatadi.

4. **Chuqur tekshiruvlar**

   ```bash
   19. openclaw status --deep
   ```

   20. Gateway sog‘liq tekshiruvlari + provayder probelarini ishga tushiradi (erishiladigan gateway talab qilinadi). 21. [Health](/gateway/health)ga qarang.

5. **So‘nggi logni kuzatish**

   ```bash
   openclaw logs --follow
   ```

   Agar RPC ishlamayotgan bo‘lsa, quyidagiga o‘ting:

   ```bash
   tail -f "$(ls -t /tmp/openclaw/openclaw-*.log | head -1)"
   ```

   Fayl loglari xizmat loglaridan alohida; [Logging](/logging) va [Troubleshooting](/gateway/troubleshooting) bo‘limlariga qarang.

6. **Doktorni ishga tushirish (ta’mirlash)**

   ```bash
   openclaw doctor
   ```

   Konfiguratsiya/holatni ta’mirlaydi yoki ko‘chiradi + sog‘liq tekshiruvlarini bajaradi. Qarang: [Doctor](/gateway/doctor).

7. **Gateway suratga olish**

   ```bash
   openclaw health --json
   openclaw health --verbose   # xatolar bo‘lganda nishon URL + konfiguratsiya yo‘lini ko‘rsatadi
   ```

   Ishlayotgan gateway’dan to‘liq suratni so‘raydi (faqat WS). Qarang: [Health](/gateway/health).

## Tezkor boshlash va birinchi ishga tushirish sozlamalari

### Men qotib qoldim — bundan chiqishning eng tez yo‘li qaysi?

Kompyuteringizni **ko‘ra oladigan** lokal AI agentdan foydalaning. Bu Discord’da so‘rashdan ancha samaraliroq,
chunki ko‘p "qotib qoldim" holatlari **lokal konfiguratsiya yoki muhit muammolari** bo‘lib,
masofaviy yordamchilar buni tekshira olmaydi.

- **Claude Code**: [https://www.anthropic.com/claude-code/](https://www.anthropic.com/claude-code/)
- **OpenAI Codex**: [https://openai.com/codex/](https://openai.com/codex/)

Bu vositalar repozitoriyani o‘qishi, buyruqlarni ishga tushirishi, loglarni tekshirishi va
mashina darajasidagi sozlamalarni (PATH, xizmatlar, ruxsatlar, avtorizatsiya fayllari) tuzatishga yordam berishi mumkin. Ularga **to‘liq manba kodini** quyidagi
xakerga mos (git) o‘rnatish orqali bering:

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git
```

Bu OpenClaw’ni **git checkout’dan** o‘rnatadi, shunda agent kod + hujjatlarni o‘qib,
siz ishlatayotgan aniq versiya haqida mulohaza yurita oladi. Keyinroq har doim barqaror versiyaga qaytishingiz mumkin,
`--install-method git` holda o‘rnatuvchini qayta ishga tushirish orqali.

Maslahat: agentdan tuzatishni **rejalashtirish va nazorat qilishni** (bosqichma-bosqich) so‘rang, so‘ng
faqat zarur buyruqlarni bajaring. Bu o‘zgarishlarni kichik va tekshirishni oson qiladi.

Agar haqiqiy xato yoki tuzatish topsangiz, iltimos GitHub’da issue oching yoki PR yuboring:
[https://github.com/openclaw/openclaw/issues](https://github.com/openclaw/openclaw/issues)
[https://github.com/openclaw/openclaw/pulls](https://github.com/openclaw/openclaw/pulls)

Yordam so‘rashni boshlashda ushbu buyruqlardan foydalaning (chiqishlarni ulashing):

```bash
openclaw status
openclaw models status
openclaw doctor
```

Ular nima qiladi:

- `openclaw status`: quick snapshot of gateway/agent health + basic config.
- `openclaw models status`: checks provider auth + model availability.
- `openclaw doctor`: validates and repairs common config/state issues.

Other useful CLI checks: `openclaw status --all`, `openclaw logs --follow`,
`openclaw gateway status`, `openclaw health --verbose`.

Quick debug loop: [First 60 seconds if something's broken](#first-60-seconds-if-somethings-broken).
Install docs: [Install](/install), [Installer flags](/install/installer), [Updating](/install/updating).

### What's the recommended way to install and set up OpenClaw

The repo recommends running from source and using the onboarding wizard:

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw onboard --install-daemon
```

The wizard can also build UI assets automatically. After onboarding, you typically run the Gateway on port **18789**.

From source (contributors/dev):

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm build
pnpm ui:build # auto-installs UI deps on first run
openclaw onboard
```

If you don't have a global install yet, run it via `pnpm openclaw onboard`.

### How do I open the dashboard after onboarding

The wizard opens your browser with a clean (non-tokenized) dashboard URL right after onboarding and also prints the link in the summary. Keep that tab open; if it didn't launch, copy/paste the printed URL on the same machine.

### How do I authenticate the dashboard token on localhost vs remote

**Localhost (same machine):**

- Open `http://127.0.0.1:18789/`.
- If it asks for auth, paste the token from `gateway.auth.token` (or `OPENCLAW_GATEWAY_TOKEN`) into Control UI settings.
- Retrieve it from the gateway host: `openclaw config get gateway.auth.token` (or generate one: `openclaw doctor --generate-gateway-token`).

**Not on localhost:**

- **Tailscale Serve** (recommended): keep bind loopback, run `openclaw gateway --tailscale serve`, open `https://<magicdns>/`. If `gateway.auth.allowTailscale` is `true`, identity headers satisfy auth (no token).
- **Tailnet bind**: run `openclaw gateway --bind tailnet --token "<token>"`, open `http://<tailscale-ip>:18789/`, paste token in dashboard settings.
- **SSH tunnel**: `ssh -N -L 18789:127.0.0.1:18789 user@host` then open `http://127.0.0.1:18789/` and paste the token in Control UI settings.

See [Dashboard](/web/dashboard) and [Web surfaces](/web) for bind modes and auth details.

### What runtime do I need

Node **>= 22** is required. `pnpm` is recommended. Bun is **not recommended** for the Gateway.

### Does it run on Raspberry Pi

Yes. The Gateway is lightweight - docs list **512MB-1GB RAM**, **1 core**, and about **500MB**
disk as enough for personal use, and note that a **Raspberry Pi 4 can run it**.

If you want extra headroom (logs, media, other services), **2GB is recommended**, but it's
not a hard minimum.

Tip: a small Pi/VPS can host the Gateway, and you can pair **nodes** on your laptop/phone for
local screen/camera/canvas or command execution. See [Nodes](/nodes).

### Any tips for Raspberry Pi installs

Short version: it works, but expect rough edges.

- Use a **64-bit** OS and keep Node >= 22.
- Prefer the **hackable (git) install** so you can see logs and update fast.
- Start without channels/skills, then add them one by one.
- If you hit weird binary issues, it is usually an **ARM compatibility** problem.

Docs: [Linux](/platforms/linux), [Install](/install).

### It is stuck on wake up my friend onboarding will not hatch What now

That screen depends on the Gateway being reachable and authenticated. The TUI also sends
"Wake up, my friend!" automatically on first hatch. If you see that line with **no reply**
and tokens stay at 0, the agent never ran.

1. Restart the Gateway:

```bash
openclaw gateway restart
```

2. Check status + auth:

```bash
openclaw status
openclaw models status
openclaw logs --follow
```

3. If it still hangs, run:

```bash
openclaw doctor
```

If the Gateway is remote, ensure the tunnel/Tailscale connection is up and that the UI
is pointed at the right Gateway. 22. [Remote access](/gateway/remote)ga qarang.

### 23. Onboarding’ni qayta qilmasdan sozlamamni yangi Mac mini mashinasiga ko‘chira olamanmi

Yes. Copy the **state directory** and **workspace**, then run Doctor once. This
keeps your bot "exactly the same" (memory, session history, auth, and channel
state) as long as you copy **both** locations:

1. Install OpenClaw on the new machine.
2. Copy `$OPENCLAW_STATE_DIR` (default: `~/.openclaw`) from the old machine.
3. Copy your workspace (default: `~/.openclaw/workspace`).
4. Run `openclaw doctor` and restart the Gateway service.

That preserves config, auth profiles, WhatsApp creds, sessions, and memory. If you're in
remote mode, remember the gateway host owns the session store and workspace.

**Important:** if you only commit/push your workspace to GitHub, you're backing
up **memory + bootstrap files**, but **not** session history or auth. Those live
under `~/.openclaw/` (for example `~/.openclaw/agents/<agentId>/sessions/`).

Related: [Migrating](/install/migrating), [Where things live on disk](/help/faq#where-does-openclaw-store-its-data),
[Agent workspace](/concepts/agent-workspace), [Doctor](/gateway/doctor),
[Remote mode](/gateway/remote).

### Where do I see what is new in the latest version

Check the GitHub changelog:
[https://github.com/openclaw/openclaw/blob/main/CHANGELOG.md](https://github.com/openclaw/openclaw/blob/main/CHANGELOG.md)

Newest entries are at the top. If the top section is marked **Unreleased**, the next dated
section is the latest shipped version. Entries are grouped by **Highlights**, **Changes**, and
**Fixes** (plus docs/other sections when needed).

### I cant access docs.openclaw.ai SSL error What now

Some Comcast/Xfinity connections incorrectly block `docs.openclaw.ai` via Xfinity
Advanced Security. Disable it or allowlist `docs.openclaw.ai`, then retry. More
detail: [Troubleshooting](/help/troubleshooting#docsopenclawai-shows-an-ssl-error-comcastxfinity).
Please help us unblock it by reporting here: [https://spa.xfinity.com/check_url_status](https://spa.xfinity.com/check_url_status).

If you still can't reach the site, the docs are mirrored on GitHub:
[https://github.com/openclaw/openclaw/tree/main/docs](https://github.com/openclaw/openclaw/tree/main/docs)

### What's the difference between stable and beta

**Stable** and **beta** are **npm dist-tags**, not separate code lines:

- `latest` = stable
- `beta` = early build for testing

We ship builds to **beta**, test them, and once a build is solid we **promote
that same version to `latest`**. That's why beta and stable can point at the
**same version**.

See what changed:
[https://github.com/openclaw/openclaw/blob/main/CHANGELOG.md](https://github.com/openclaw/openclaw/blob/main/CHANGELOG.md)

### How do I install the beta version and whats the difference between beta and dev

**Beta** is the npm dist-tag `beta` (may match `latest`).
**Dev** is the moving head of `main` (git); when published, it uses the npm dist-tag `dev`.

One-liners (macOS/Linux):

```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --beta
```

```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --install-method git
```

Windows installer (PowerShell):
[https://openclaw.ai/install.ps1](https://openclaw.ai/install.ps1)

More detail: [Development channels](/install/development-channels) and [Installer flags](/install/installer).

### How long does install and onboarding usually take

Rough guide:

- **Install:** 2-5 minutes
- **Onboarding:** 5-15 minutes depending on how many channels/models you configure

1. Agar u osilib qolsa, [Installer stuck](/help/faq#installer-stuck-how-do-i-get-more-feedback)
   va [Im stuck](/help/faq#im-stuck--whats-the-fastest-way-to-get-unstuck) dagi tezkor debug siklidan foydalaning.

### 2. Eng so‘nggi versiyalarni qanday sinab ko‘raman

3. Ikki variant:

1. 4. **Dev kanal (git checkout):**

```bash
5. openclaw update --channel dev
```

6. Bu `main` branchga o‘tadi va manbadan yangilaydi.

2. 7. **Hackable o‘rnatish (installer saytidan):**

```bash
8. curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git
```

9. Bu sizga tahrirlash mumkin bo‘lgan lokal repo beradi, keyin git orqali yangilaysiz.

10. Agar toza klonni qo‘lda xohlasangiz, quyidagidan foydalaning:

```bash
11. git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm build
```

12. Hujjatlar: [Update](/cli/update), [Development channels](/install/development-channels),
    [Install](/install).

### 13. Installer stuck — Qanday qilib ko‘proq fikr-mulohaza olaman

14. Installer’ni **verbose chiqish** bilan qayta ishga tushiring:

```bash
15. curl -fsSL https://openclaw.ai/install.sh | bash -s -- --verbose
```

16. Verbose bilan beta o‘rnatish:

```bash
17. curl -fsSL https://openclaw.ai/install.sh | bash -s -- --beta --verbose
```

18. Hackable (git) o‘rnatish uchun:

```bash
19. curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git --verbose
```

20. Ko‘proq variantlar: [Installer flags](/install/installer).

### 21. Windows o‘rnatishda git topilmadi yoki openclaw tanilmadi

22. Windows’dagi ikki keng tarqalgan muammo:

23. **1) npm xatosi spawn git / git not found**

- 24. **Git for Windows** ni o‘rnating va `git` PATH’da ekanligiga ishonch hosil qiling.
- 25. PowerShell’ni yoping va qayta oching, so‘ng installer’ni yana ishga tushiring.

26. **2) o‘rnatilgandan keyin openclaw tanilmadi**

- 27. npm global bin papkangiz PATH’da emas.

- 28. Yo‘lni tekshiring:

  ```powershell
  29. npm config get prefix
  ```

- 30. `<prefix>\\bin` PATH’da ekanligiga ishonch hosil qiling (ko‘p tizimlarda bu `%AppData%\\npm`).

- 31. PATH’ni yangilagandan so‘ng PowerShell’ni yoping va qayta oching.

32. Agar Windows’da eng silliq sozlamani xohlasangiz, native Windows o‘rniga **WSL2** dan foydalaning.
33. Hujjatlar: [Windows](/platforms/windows).

### 34. Hujjatlar savolimga javob bermadi, qanday qilib yaxshiroq javob olaman

35. **Hackable (git) o‘rnatish** dan foydalaning, shunda to‘liq manba va hujjatlar lokal bo‘ladi, keyin
    botingizdan (yoki Claude/Codex’dan) _shu papkadan_ so‘rang — u repo’ni o‘qib, aniq javob bera oladi.

```bash
36. curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git
```

37. Batafsil: [Install](/install) va [Installer flags](/install/installer).

### 38. OpenClaw’ni Linux’da qanday o‘rnataman

39. Qisqa javob: Linux qo‘llanmasiga amal qiling, so‘ng onboarding wizard’ni ishga tushiring.

- 40. Linux tezkor yo‘li + servis o‘rnatish: [Linux](/platforms/linux).
- 41. To‘liq qo‘llanma: [Getting Started](/start/getting-started).
- 42. Installer + yangilanishlar: [Install & updates](/install/updating).

### 43. OpenClaw’ni VPS’da qanday o‘rnataman

44. Istalgan Linux VPS mos keladi. 45. Serverga o‘rnating, keyin Gateway’ga ulanish uchun SSH/Tailscale’dan foydalaning.

46. Qo‘llanmalar: [exe.dev](/install/exe-dev), [Hetzner](/install/hetzner), [Fly.io](/install/fly).
47. Masofaviy kirish: [Gateway remote](/gateway/remote).

### 48. Cloud VPS o‘rnatish qo‘llanmalari qayerda

49. Biz umumiy provayderlar uchun **hosting hub** ni saqlaymiz. 50. Birini tanlang va qo‘llanmaga amal qiling:

- [VPS hosting](/vps) (barcha provayderlar bir joyda)
- [Fly.io](/install/fly)
- [Hetzner](/install/hetzner)
- [exe.dev](/install/exe-dev)

Bulutda qanday ishlaydi: **Gateway serverda ishlaydi**, va siz unga noutbuk/telefoningizdan Control UI (yoki Tailscale/SSH) orqali kirasiz. Sizning holatingiz + ish joyingiz
serverda saqlanadi, shuning uchun xostni asosiy manba sifatida qabul qiling va uni zaxiralang.

Siz **node**larni (Mac/iOS/Android/headless) shu bulut Gateway’iga ulab, mahalliy ekran/kamera/canvas’ga kirish yoki Gateway bulutda qolgan holda noutbukingizda buyruqlarni ishga tushirishingiz mumkin.

Hub: [Platforms](/platforms). 24. Masofaviy kirish: [Gateway remote](/gateway/remote).
Node’lar: [Nodes](/nodes), [Nodes CLI](/cli/nodes).

### OpenClaw’dan o‘zini yangilashni so‘rashim mumkinmi

Qisqa javob: **mumkin, lekin tavsiya etilmaydi**. Yangilash jarayoni
Gateway’ni qayta ishga tushirishi (bu faol sessiyani uzadi), toza git checkout talab qilishi va tasdiqlashni so‘rashi mumkin. Xavfsizroq yo‘l: yangilashlarni operator sifatida shell’dan ishga tushiring.

CLI’dan foydalaning:

```bash
openclaw update
openclaw update status
openclaw update --channel stable|beta|dev
openclaw update --tag <dist-tag|version>
openclaw update --no-restart
```

Agar agent orqali avtomatlashtirishga majbur bo‘lsangiz:

```bash
openclaw update --yes --no-restart
openclaw gateway restart
```

Hujjatlar: [Update](/cli/update), [Updating](/install/updating).

### Onboarding ustasi aslida nima qiladi

`openclaw onboard` — tavsiya etilgan sozlash yo‘li. **Local mode**da u sizni quyidagilar bo‘yicha bosqichma-bosqich olib boradi:

- **Model/auth sozlamalari** (Claude obunalari uchun Anthropic **setup-token** tavsiya etiladi, OpenAI Codex OAuth qo‘llab-quvvatlanadi, API kalitlar ixtiyoriy, LM Studio lokal modellari qo‘llab-quvvatlanadi)
- **Workspace** joylashuvi + boshlang‘ich fayllar
- **Gateway sozlamalari** (bind/port/auth/tailscale)
- **Provayderlar** (WhatsApp, Telegram, Discord, Mattermost (plagin), Signal, iMessage)
- **Daemon o‘rnatish** (macOS’da LaunchAgent; Linux/WSL2’da systemd user unit)
- **Health checks** va **skills** tanlovi

Shuningdek, sozlangan modelingiz noma’lum bo‘lsa yoki autentifikatsiya yetishmasa, ogohlantiradi.

### Buni ishga tushirish uchun Claude yoki OpenAI obunasi kerakmi

Yo‘q. 25. Siz OpenClaw’ni **API kalitlari** (Anthropic/OpenAI/boshqalar) bilan yoki **faqat lokal modellar** bilan ishga tushirishingiz mumkin, shunda ma’lumotlaringiz qurilmangizda qoladi. Obunalar (Claude
Pro/Max yoki OpenAI Codex) — bu provayderlarda autentifikatsiya qilishning ixtiyoriy usullari.

Hujjatlar: [Anthropic](/providers/anthropic), [OpenAI](/providers/openai),
[Local models](/gateway/local-models), [Models](/concepts/models).

### API kalitisiz Claude Max obunasidan foydalansam bo‘ladimi

Ha. Siz API kalit o‘rniga **setup-token** bilan autentifikatsiya qilishingiz mumkin. Bu obuna orqali autentifikatsiya yo‘lidir.

Claude Pro/Max obunalari **API kalitni o‘z ichiga olmaydi**, shuning uchun obuna akkauntlari uchun to‘g‘ri yondashuv shu. Muhim: bu foydalanish Anthropic’ning obuna siyosati va shartlariga muvofiq ekanini ular bilan tasdiqlashingiz kerak.
Agar eng aniq va qo‘llab-quvvatlanadigan yo‘lni xohlasangiz, Anthropic API kalitidan foydalaning.

### Anthropic setup-token autentifikatsiyasi qanday ishlaydi

`claude setup-token` Claude Code CLI orqali **token satrini** yaratadi (u veb-konsolda mavjud emas). Uni **istalgan kompyuterda** ishga tushirishingiz mumkin. Ustada **Anthropic token (setup-token’ni joylashtiring)** ni tanlang yoki `openclaw models auth paste-token --provider anthropic` bilan joylashtiring. Token **anthropic** provayderi uchun autentifikatsiya profili sifatida saqlanadi va API kalit kabi ishlatiladi (avto-yangilanishsiz). Batafsil: [OAuth](/concepts/oauth).

### Anthropic setup-token’ni qayerdan topaman

U Anthropic Console’da **mavjud emas**. Setup-token **Claude Code CLI** tomonidan **istalgan kompyuterda** yaratiladi:

```bash
claude setup-token
```

Copy the token it prints, then choose **Anthropic token (paste setup-token)** in the wizard. If you want to run it on the gateway host, use `openclaw models auth setup-token --provider anthropic`. If you ran `claude setup-token` elsewhere, paste it on the gateway host with `openclaw models auth paste-token --provider anthropic`. See [Anthropic](/providers/anthropic).

### Do you support Claude subscription auth (Claude Pro or Max)

Yes - via **setup-token**. OpenClaw no longer reuses Claude Code CLI OAuth tokens; use a setup-token or an Anthropic API key. Generate the token anywhere and paste it on the gateway host. See [Anthropic](/providers/anthropic) and [OAuth](/concepts/oauth).

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

You need **some macOS device** signed into Messages. It does **not** have to be a Mac mini -
any Mac works. **Use [BlueBubbles](/channels/bluebubbles)** (recommended) for iMessage - the BlueBubbles server runs on macOS, while the Gateway can run on Linux or elsewhere.

Common setups:

- Run the Gateway on Linux/VPS, and run the BlueBubbles server on any Mac signed into Messages.
- Run everything on the Mac if you want the simplest single‑machine setup.

Docs: [BlueBubbles](/channels/bluebubbles), [Nodes](/nodes),
[Mac remote mode](/platforms/mac/remote).

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

Yes, via **multi-agent routing**. Har bir jo‘natuvchining WhatsApp **DM** ini (peer `kind: "direct"`, jo‘natuvchi E.164 masalan `+15551234567`) alohida `agentId` ga bog‘lang, shunda har bir odam o‘z ish maydoni va sessiya xotirasiga ega bo‘ladi. Replies still come from the **same WhatsApp account**, and DM access control (`channels.whatsapp.dmPolicy` / `channels.whatsapp.allowFrom`) is global per WhatsApp account. See [Multi-Agent Routing](/concepts/multi-agent) and [WhatsApp](/channels/whatsapp).

### Can I run a fast chat agent and an Opus for coding agent

Yes. Use multi-agent routing: give each agent its own default model, then bind inbound routes (provider account or specific peers) to each agent. Example config lives in [Multi-Agent Routing](/concepts/multi-agent). 26. Shuningdek qarang: [Models](/concepts/models) va [Configuration](/gateway/configuration).

### 27. Homebrew Linux’da ishlaydimi

28. Ha. Homebrew supports Linux (Linuxbrew). 1. Tezkor sozlash:

```bash
2. /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.profile
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
brew install <formula>
```

3. Agar OpenClaw’ni systemd orqali ishga tushirsangiz, xizmat PATH’iga `/home/linuxbrew/.linuxbrew/bin` (yoki brew prefiksingiz) kiritilganiga ishonch hosil qiling, shunda `brew` orqali o‘rnatilgan vositalar login bo‘lmagan shelllarda ham topiladi.
4. So‘nggi buildlar Linux’dagi systemd xizmatlarida keng tarqalgan foydalanuvchi bin kataloglarini ham oldindan qo‘shadi (masalan `~/.local/bin`, `~/.npm-global/bin`, `~/.local/share/pnpm`, `~/.bun/bin`) va `PNPM_HOME`, `NPM_CONFIG_PREFIX`, `BUN_INSTALL`, `VOLTA_HOME`, `ASDF_DATA_DIR`, `NVM_DIR` hamda `FNM_DIR` o‘rnatilgan bo‘lsa, ularni inobatga oladi.

### 5. Hackable git o‘rnatish bilan npm o‘rnatish o‘rtasidagi farq nimada

- 6. **Hackable (git) o‘rnatish:** to‘liq manba kodi checkout’i, tahrirlash mumkin, hissa qo‘shuvchilar uchun eng yaxshi.
  7. Buildlarni lokalda ishga tushirasiz va kod/hujjatlarni patch qilishingiz mumkin.
- 8. **npm o‘rnatish:** global CLI o‘rnatish, repo yo‘q, “shunchaki ishga tushirish” uchun eng qulay.
  9. Yangilanishlar npm dist-tag’laridan keladi.

10. Hujjatlar: [Boshlash](/start/getting-started), [Yangilash](/install/updating).

### 11. Keyinroq npm va git o‘rnatishlari o‘rtasida almashsam bo‘ladimi

12. Ha. 13. Boshqa variantni o‘rnating, so‘ng gateway xizmati yangi entrypoint’ga ishora qilishi uchun Doctor’ni ishga tushiring.
13. Bu **ma’lumotlaringizni o‘chirmaydi** — faqat OpenClaw kod o‘rnatilishini almashtiradi. 15. Sizning holatingiz
    (`~/.openclaw`) va ish maydoni (`~/.openclaw/workspace`) o‘zgarmay qoladi.

16. npm → git:

```bash
17. git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm build
openclaw doctor
openclaw gateway restart
```

18. git → npm:

```bash
19. npm install -g openclaw@latest
openclaw doctor
openclaw gateway restart
```

20. Doctor gateway xizmati entrypoint’ida mos kelmaslikni aniqlaydi va xizmat konfiguratsiyasini joriy o‘rnatishga moslab qayta yozishni taklif qiladi (avtomatlashtirishda `--repair` dan foydalaning).

21. Zaxiralash bo‘yicha maslahatlar: [Backup strategy](/help/faq#whats-the-recommended-backup-strategy) ga qarang.

### 22. Gateway’ni noutbukda yoki VPS’da ishga tushirishim kerakmi

23. Qisqa javob: **agar 24/7 ishonchlilik xohlasangiz, VPS’dan foydalaning**. 24. Agar
    eng kam ishqalanishni xohlasangiz va uyqu/qayta ishga tushirishlarga rozi bo‘lsangiz, lokalda ishga tushiring.

25. **Noutbuk (lokal Gateway)**

- 26. **Afzalliklar:** server xarajati yo‘q, lokal fayllarga to‘g‘ridan-to‘g‘ri kirish, jonli brauzer oynasi.
- 27. **Kamchiliklar:** uyqu/tarmoq uzilishlari = uzilishlar, OS yangilanishlari/qayta yuklashlar to‘xtatadi, doim uyg‘oq turishi kerak.

28. **VPS / bulut**

- 29. **Afzalliklar:** doim yoqilgan, barqaror tarmoq, noutbuk uyqu muammolari yo‘q, ishlatib turish oson.
- 30. **Kamchiliklar:** ko‘pincha headless (skrinshotlardan foydalaniladi), faqat masofaviy faylga kirish, yangilash uchun SSH kerak.

31. **OpenClaw’ga xos eslatma:** WhatsApp/Telegram/Slack/Mattermost (plagin)/Discord’ning barchasi VPS’dan yaxshi ishlaydi. 32. Asosiy yagona murosa — **headless brauzer** va ko‘rinadigan oyna o‘rtasidagi tanlov. 33. [Brauzer](/tools/browser) ga qarang.

34. **Tavsiya etilgan standart:** agar ilgari gateway uzilishlari bo‘lgan bo‘lsa, VPS. 35. Lokal variant Mac’dan faol foydalanayotganingizda va lokal fayllarga kirish yoki ko‘rinadigan brauzer bilan UI avtomatlashtirishni xohlaganingizda juda qulay.

### 36. OpenClaw’ni alohida (dedicated) mashinada ishga tushirish qanchalik muhim

37. Majburiy emas, lekin **ishonchlilik va izolyatsiya uchun tavsiya etiladi**.

- 38. **Alohida host (VPS/Mac mini/Pi):** doim yoqilgan, uyqu/qayta yuklashlar kamroq, ruxsatlar toza, ishlatib turish osonroq.
- 39. **Ulashilgan noutbuk/desktop:** test va faol foydalanish uchun mutlaqo mos, ammo qurilma uxlaganda yoki yangilanganda pauzalar bo‘lishini kuting.

40. Eng yaxshi ikkala variantni xohlasangiz, Gateway’ni alohida host’da qoldiring va noutbukni lokal ekran/kamera/exec vositalari uchun **node** sifatida ulang. 41. [Node’lar](/nodes) ga qarang.
41. Xavfsizlik bo‘yicha ko‘rsatmalar uchun [Xavfsizlik](/gateway/security) ni o‘qing.

### 43. VPS uchun minimal talablar va tavsiya etilgan OS qanday

44. OpenClaw yengil. 45. Asosiy Gateway + bitta chat kanali uchun:

- 46. **Mutlaq minimum:** 1 vCPU, 1GB RAM, ~500MB disk.
- 47. **Tavsiya etiladi:** 1–2 vCPU, 2GB RAM yoki ko‘proq (loglar, media, bir nechta kanallar uchun zaxira). 48. Node vositalari va brauzer avtomatlashtirishi resurs talabchan bo‘lishi mumkin.

49. OS: **Ubuntu LTS** (yoki har qanday zamonaviy Debian/Ubuntu) dan foydalaning. 50. Linux o‘rnatish yo‘li shu yerda eng yaxshi sinovdan o‘tgan.

Hujjatlar: [Linux](/platforms/linux), [VPS hosting](/vps).

### OpenClaw’ni VM’da ishga tushira olamanmi va talablar qanday?

Ha. VM’ni VPS kabi ko‘ring: u doim yoqilgan bo‘lishi, tarmoq orqali mavjud bo‘lishi va Gateway hamda yoqadigan barcha kanallar uchun yetarli RAM’ga ega bo‘lishi kerak.

Boshlang‘ich tavsiyalar:

- **Mutlaq minimum:** 1 vCPU, 1GB RAM.
- **Tavsiya etiladi:** bir nechta kanal, brauzer avtomatlashtiruvi yoki media vositalarini ishlatsangiz 2GB RAM yoki undan ko‘p.
- **OS:** Ubuntu LTS yoki boshqa zamonaviy Debian/Ubuntu.

Agar Windows’da bo‘lsangiz, **WSL2 eng oson VM uslubidagi sozlama** va eng yaxshi vositalar mosligiga ega. Qarang: [Windows](/platforms/windows), [VPS hosting](/vps).
Agar macOS’ni VM’da ishga tushirayotgan bo‘lsangiz, [macOS VM](/install/macos-vm) sahifasiga qarang.

## OpenClaw nima?

### OpenClaw haqida bir paragrafda

OpenClaw — bu o‘zingizga tegishli qurilmalarda ishga tushiradigan shaxsiy AI yordamchi. U siz allaqachon ishlatadigan xabar almashish platformalarida (WhatsApp, Telegram, Slack, Mattermost (plugin), Discord, Google Chat, Signal, iMessage, WebChat) javob beradi va qo‘llab-quvvatlanadigan platformalarda ovoz hamda jonli Canvas’ni ham taqdim etadi. **Gateway** — doim yoqilgan boshqaruv qatlami; yordamchining o‘zi esa mahsulotdir.

### Qiymat taklifi nimada?

OpenClaw "shunchaki Claude o‘rami" emas. Bu **local-first boshqaruv qatlami** bo‘lib, **o‘zingizga tegishli apparatda** kuchli yordamchini ishga tushirish imkonini beradi; siz allaqachon ishlatadigan chat ilovalari orqali ulanadi, holatli sessiyalar, xotira va vositalarga ega — ish jarayonlaringiz nazoratini hosted SaaS’ga topshirmasdan.

Asosiy jihatlar:

- **Sizning qurilmalaringiz, sizning ma’lumotlaringiz:** Gateway’ni xohlagan joyda (Mac, Linux, VPS) ishga tushiring va ish maydoni hamda sessiya tarixini lokal saqlang.
- **Veb-sandbox emas, haqiqiy kanallar:** WhatsApp/Telegram/Slack/Discord/Signal/iMessage va boshqalar, shuningdek qo‘llab-quvvatlanadigan platformalarda mobil ovoz va Canvas.
- **Modeldan mustaqil:** Anthropic, OpenAI, MiniMax, OpenRouter va boshqalardan foydalaning, agentlar bo‘yicha marshrutlash va nosozlikka chidamlilik bilan.
- **Faqat lokal variant:** agar xohlasangiz lokal modellarni ishga tushiring, shunda **barcha ma’lumotlar qurilmangizda qoladi**.
- **Ko‘p agentli marshrutlash:** kanal, akkaunt yoki vazifa bo‘yicha alohida agentlar, har biri o‘z ish maydoni va standart sozlamalariga ega.
- **Ochiq manbali va sozlanadigan:** tekshiring, kengaytiring va vendor lock-in’siz o‘zingiz joylashtiring.

Hujjatlar: [Gateway](/gateway), [Channels](/channels), [Multi-agent](/concepts/multi-agent),
[Memory](/concepts/memory).

### Endi sozladim, birinchi nima qilay?

Yaxshi boshlang‘ich loyihalar:

- Veb-sayt yarating (WordPress, Shopify yoki oddiy statik sayt).
- Mobil ilova prototipini yarating (kontur, ekranlar, API reja).
- Fayl va papkalarni tartibga soling (tozalash, nomlash, teglar).
- Gmail’ni ulang va xulosalar yoki follow-up’larni avtomatlashtiring.

U katta vazifalarni ham bajara oladi, ammo ularni bosqichlarga bo‘lib, parallel ish uchun sub-agentlardan foydalansangiz eng samarali bo‘ladi.

### OpenClaw’ning kundalik eng yaxshi besh qo‘llanilish holati qaysilar?

Kundalik yutuqlar odatda quyidagicha ko‘rinadi:

- **Shaxsiy brifinglar:** kiruvchi xatlar, taqvim va siz qiziqadigan yangiliklar bo‘yicha xulosalar.
- **Tadqiqot va qoralama:** tezkor tadqiqot, xulosalar va email yoki hujjatlar uchun dastlabki qoralamalar.
- **Eslatmalar va follow-up’lar:** cron yoki heartbeat asosidagi eslatmalar va chek-listlar.
- **Brauzer avtomatlashtiruvi:** formalarni to‘ldirish, ma’lumot yig‘ish va takroriy veb vazifalar.
- **Qurilmalararo muvofiqlashtirish:** vazifani telefoningizdan yuboring, Gateway uni serverda bajarsin va natijani chatda qaytarsin.

### OpenClaw SaaS uchun lead gen, outreach, reklama va bloglarda yordam bera oladimi?

**Tadqiqot, saralash va qoralama** uchun — ha. U saytlarni ko‘zdan kechirishi, qisqa ro‘yxatlar tuzishi, potensial mijozlarni umumlashtirishi va outreach yoki reklama matnlari qoralamalarini yozishi mumkin.

**Outreach yoki reklama kampaniyalari** uchun odamni jarayonda qoldiring. Spamdan qoching, mahalliy qonunlar va platforma siyosatlariga rioya qiling va yuborishdan oldin hammasini ko‘rib chiqing. Eng xavfsiz yondashuv — OpenClaw qoralama tayyorlaydi, siz esa tasdiqlaysiz.

Hujjatlar: [Security](/gateway/security).

### Veb-ishlab chiqishda Claude Code bilan solishtirganda afzalliklari nimada?

OpenClaw — bu **shaxsiy yordamchi** va muvofiqlashtirish qatlami, IDE o‘rnini bosuvchi emas. 1. Repo ichida eng tezkor to‘g‘ridan-to‘g‘ri kod yozish sikli uchun Claude Code yoki Codex’dan foydalaning. 2. Barqaror xotira, qurilmalararo kirish va vositalarni orkestratsiya qilish kerak bo‘lganda OpenClaw’dan foydalaning.

3. Afzalliklar:

- 4. Sessiyalar davomida **doimiy xotira + ish maydoni**
- 5. **Ko‘p platformali kirish** (WhatsApp, Telegram, TUI, WebChat)
- 29. **Asboblarni orkestratsiya qilish** (brauzer, fayllar, rejalashtirish, hook’lar)
- 7. **Doimiy ishlaydigan Gateway** (VPS’da ishga tushiring, istalgan joydan muloqot qiling)
- 8. Mahalliy brauzer/ekran/kamera/exec uchun **Node’lar**

9. Namoyish: [https://openclaw.ai/showcase](https://openclaw.ai/showcase)

## 10. Ko‘nikmalar va avtomatlashtirish

### 11. Repo’ni iflos qilmasdan ko‘nikmalarni qanday sozlayman

12. Repo nusxasini tahrirlash o‘rniga boshqariladigan override’lardan foydalaning. 13. O‘zgartirishlaringizni `~/.openclaw/skills/<name>/SKILL.md` ga joylashtiring (yoki `~/.openclaw/openclaw.json` ichida `skills.load.extraDirs` orqali papka qo‘shing). 14. Ustuvorlik tartibi `<workspace>/skills` > `~/.openclaw/skills` > bundled, shuning uchun boshqariladigan override’lar git’ga tegmasdan yutadi. 15. Faqat upstream’ga munosib tahrirlar repo’da bo‘lishi va PR sifatida yuborilishi kerak.

### 16. Ko‘nikmalarni maxsus papkadan yuklay olamanmi

17. Ha. 18. `~/.openclaw/openclaw.json` ichida `skills.load.extraDirs` orqali qo‘shimcha kataloglar qo‘shing (eng past ustuvorlik). 19. Standart ustuvorlik saqlanadi: `<workspace>/skills` → `~/.openclaw/skills` → bundled → `skills.load.extraDirs`. 20. `clawhub` odatda `./skills` ichiga o‘rnatadi, OpenClaw esa buni `<workspace>/skills` sifatida ko‘radi.

### 21. Turli vazifalar uchun turli modellarni qanday ishlatsam bo‘ladi

22. Hozirda qo‘llab-quvvatlanadigan andozalar:

- 23. **Cron ishlar**: ajratilgan ishlar har bir ish uchun `model` override’ini belgilashi mumkin.
- 24. **Sub-agentlar**: vazifalarni turli standart modellarga ega alohida agentlarga yo‘naltiring.
- 25. **Talab bo‘yicha almashtirish**: joriy sessiya modelini istalgan vaqtda almashtirish uchun `/model` dan foydalaning.

30. [Cron jobs](/automation/cron-jobs), [Multi-Agent Routing](/concepts/multi-agent) va [Slash commands](/tools/slash-commands)ga qarang.

### 27. Og‘ir ish paytida bot qotib qoladi Buni qanday offload qilaman

28. Uzoq yoki parallel vazifalar uchun **sub-agentlar**dan foydalaning. 29. Sub-agentlar o‘z sessiyasida ishlaydi, xulosa qaytaradi va asosiy chat’ingizni responsiv saqlaydi.

30. Bot’ingizdan "bu vazifa uchun sub-agent yarat" deb so‘rang yoki `/subagents` dan foydalaning.
31. Chat’da `/status` dan foydalanib Gateway hozir nima qilayotganini (va band yoki yo‘qligini) ko‘ring.

32. Token maslahati: uzoq vazifalar ham, sub-agentlar ham token sarflaydi. 33. Agar xarajat muhim bo‘lsa, `agents.defaults.subagents.model` orqali sub-agentlar uchun arzonroq modelni belgilang.

34. Hujjatlar: [Sub-agents](/tools/subagents).

### 35. Cron yoki eslatmalar ishga tushmayapti Nimalarni tekshirishim kerak

36. Cron Gateway jarayoni ichida ishlaydi. 37. Agar Gateway uzluksiz ishlamayotgan bo‘lsa, rejalashtirilgan ishlar bajarilmaydi.

38. Tekshiruv ro‘yxati:

- 39. Cron yoqilganini (`cron.enabled`) va `OPENCLAW_SKIP_CRON` o‘rnatilmaganini tasdiqlang.
- 40. Gateway 24/7 ishlayotganini tekshiring (uyqu/restartlar yo‘q).
- 41. Ish uchun vaqt mintaqasi sozlamalarini tekshiring (`--tz` va xost vaqt mintaqasi).

42. Nosozliklarni aniqlash:

```bash
43. openclaw cron run <jobId> --force
openclaw cron runs --id <jobId> --limit 50
```

44. Hujjatlar: [Cron jobs](/automation/cron-jobs), [Cron vs Heartbeat](/automation/cron-vs-heartbeat).

### 45. Linux’da ko‘nikmalarni qanday o‘rnataman

46. **ClawHub** (CLI) dan foydalaning yoki ko‘nikmalarni ish maydoningizga joylashtiring. 47. macOS’dagi Skills UI Linux’da mavjud emas.
47. Ko‘nikmalarni [https://clawhub.com](https://clawhub.com) da ko‘rib chiqing.

49. ClawHub CLI’ni o‘rnating (paket menejerlaridan birini tanlang):

```bash
50. npm i -g clawhub
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

4. 31. Ko‘nikmalar snapshot’i yangilanishi uchun yangi sessiyani boshlang.

### 32) Sizda Notion yoki HeyGen integratsiyasi bormi

33. Hozircha built-in emas.

Options:

- **Custom skill / plugin:** best for reliable API access (Notion/HeyGen both have APIs).
- **Browser automation:** works without code but is slower and more fragile.

If you want to keep context per client (agency workflows), a simple pattern is:

- 34. Har bir mijoz uchun bitta Notion sahifasi (kontekst + afzalliklar + faol ish).
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

## 1. Sandboxlash va xotira

### 2. Sandboxlash bo‘yicha alohida hujjat bormi

3. Ha. 4. [Sandboxing](/gateway/sandboxing) sahifasiga qarang. 5. Docker’ga xos sozlamalar uchun (Docker’da to‘liq gateway yoki sandbox imijlar), [Docker](/install/docker) sahifasiga qarang.

### 6. Docker cheklangandek tuyuladi. To‘liq funksiyalarni qanday yoqaman

7. Standart imij xavfsizlikni birinchi o‘ringa qo‘yadi va `node` foydalanuvchisi sifatida ishlaydi, shuning uchun unda tizim paketlari, Homebrew yoki biriktirilgan brauzerlar mavjud emas. 35. To‘liqroq sozlama uchun:

- 9. Keshlar saqlanib qolishi uchun `/home/node` ni `OPENCLAW_HOME_VOLUME` bilan persist qiling.
- 10. Tizim bog‘liqliklarini imij ichiga `OPENCLAW_DOCKER_APT_PACKAGES` orqali qo‘shing.
- 11. Playwright brauzerlarini biriktirilgan CLI orqali o‘rnating:
      `node /app/node_modules/playwright-core/cli.js install chromium`
- 12. `PLAYWRIGHT_BROWSERS_PATH` ni o‘rnating va yo‘l persist qilinishini ta’minlang.

13. Hujjatlar: [Docker](/install/docker), [Browser](/tools/browser).

14. **DM’larni shaxsiy qoldirib, guruhlarni bitta agent bilan ommaviy sandboxlangan qilishim mumkinmi**

15. Ha — agar shaxsiy trafik **DM’lar**, ommaviy trafik esa **guruhlar** bo‘lsa.

16. `agents.defaults.sandbox.mode: "non-main"` dan foydalaning, shunda guruh/kanal sessiyalari (non-main kalitlar) Docker’da ishlaydi, asosiy DM sessiyasi esa host’da qoladi. 17. So‘ng sandboxlangan sessiyalarda mavjud bo‘ladigan asboblarni `tools.sandbox.tools` orqali cheklang.

18. Sozlash bo‘yicha qo‘llanma + misol konfiguratsiya: [Groups: personal DMs + public groups](/channels/groups#pattern-personal-dms-public-groups-single-agent)

19. Asosiy konfiguratsiya havolasi: [Gateway configuration](/gateway/configuration#agentsdefaultssandbox)

### 36. Xost papkasini sandbox’ga qanday bog‘layman

21. `agents.defaults.sandbox.docker.binds` ni `["host:path:mode"]` ga o‘rnating (masalan, `"/home/user/src:/src:ro"`). 22. Global va har bir agent uchun binds birlashtiriladi; `scope: "shared"` bo‘lsa, agentga xos binds e’tiborga olinmaydi. 23. Sezgir narsalar uchun `:ro` dan foydalaning va binds sandbox fayl tizimi devorlarini chetlab o‘tishini yodda tuting. 24. Misollar va xavfsizlik bo‘yicha eslatmalar uchun [Sandboxing](/gateway/sandboxing#custom-bind-mounts) va [Sandbox vs Tool Policy vs Elevated](/gateway/sandbox-vs-tool-policy-vs-elevated#bind-mounts-security-quick-check) sahifalariga qarang.

### 25. Xotira qanday ishlaydi

26. OpenClaw xotirasi agent ish maydonidagi oddiy Markdown fayllaridan iborat:

- 27. Kundalik qaydlar `memory/YYYY-MM-DD.md` da
- 28. Tanlab olingan uzoq muddatli qaydlar `MEMORY.md` da (faqat asosiy/shaxsiy sessiyalar)

29. OpenClaw, shuningdek, **jim pre-kompaktlash xotira flush** jarayonini ishga tushiradi, bu modelga avtomatik kompaktlashdan oldin barqaror qaydlar yozishni eslatadi. 30. Bu faqat ish maydoni yozish mumkin bo‘lganda ishlaydi (faqat o‘qish mumkin bo‘lgan sandboxlar buni o‘tkazib yuboradi). 31. [Memory](/concepts/memory) sahifasiga qarang.

### 32. Xotira doim unutib qo‘yyapti. Qanday qilib uni saqlab qolaman

33. Botdan **faktni xotiraga yozishni** so‘rang. 34. Uzoq muddatli qaydlar `MEMORY.md` ga, qisqa muddatli kontekst esa `memory/YYYY-MM-DD.md` ga tegishli.

35. Bu hali ham takomillashtirilayotgan soha. 36. Modelga xotiralarni saqlashni eslatish foydali; u nima qilishni biladi. 37. Agar u baribir unutaversa, Gateway har bir ishga tushishda bir xil ish maydonidan foydalanayotganini tekshiring.

38. Hujjatlar: [Memory](/concepts/memory), [Agent workspace](/concepts/agent-workspace).

### 39. Semantik xotira qidiruvi uchun OpenAI API kaliti kerakmi

40. Faqat **OpenAI embeddings** dan foydalansangiz. 41. Codex OAuth chat/completions ni qamrab oladi va embeddings’ga ruxsat bermaydi, shuning uchun **Codex orqali tizimga kirish (OAuth yoki Codex CLI login)** semantik xotira qidiruvi uchun yordam bermaydi. 42. OpenAI embeddings baribir haqiqiy API kalitini talab qiladi (`OPENAI_API_KEY` yoki `models.providers.openai.apiKey`).

43. Agar provayderni aniq ko‘rsatmasangiz, OpenClaw API kalitini aniqlay olganda provayderni avtomatik tanlaydi (auth profillari, `models.providers.*.apiKey` yoki muhit o‘zgaruvchilari).
44. Agar OpenAI kaliti topilsa, OpenAI’ni afzal ko‘radi, aks holda Gemini kaliti topilsa — Gemini’ni. 45. Agar hech bir kalit mavjud bo‘lmasa, xotira qidiruvi uni sozlamaguncha o‘chirilgan holatda qoladi. 46. Agar lokal model yo‘li sozlangan va mavjud bo‘lsa, OpenClaw `local` ni afzal ko‘radi.

47. Agar lokal holatda qolmoqchi bo‘lsangiz, `memorySearch.provider = "local"` ni (va ixtiyoriy ravishda `memorySearch.fallback = "none"`) o‘rnating. 48. Agar Gemini embeddings xohlasangiz, `memorySearch.provider = "gemini"` ni o‘rnating va `GEMINI_API_KEY` (yoki `memorySearch.remote.apiKey`) ni taqdim eting. 49. Biz **OpenAI, Gemini yoki local** embedding modellarini qo‘llab-quvvatlaymiz — sozlash tafsilotlari uchun [Memory](/concepts/memory) ga qarang.

### 50. Xotira abadiy saqlanadimi? Cheklovlar qanday

Xotira fayllari diskda saqlanadi va siz ularni o‘chirmaguningizcha saqlanib qoladi. Cheklov modelga emas, balki sizning saqlash joyingizga bog‘liq. **Sessiya konteksti** hali ham modelning kontekst oynasi bilan cheklangan, shuning uchun uzoq suhbatlar siqilishi yoki qisqartirilishi mumkin. Shu sababli xotira qidiruvi mavjud — u faqat tegishli qismlarni qayta kontekstga olib kiradi.

Hujjatlar: [Memory](/concepts/memory), [Context](/concepts/context).

## Ma’lumotlar diskda qayerda joylashadi

### OpenClaw bilan ishlatiladigan barcha ma’lumotlar lokalda saqlanadimi

Yo‘q — **OpenClaw holati lokal**, ammo **tashqi xizmatlar ularga yuborgan narsalaringizni baribir ko‘radi**.

- **Standart bo‘yicha lokal:** sessiyalar, xotira fayllari, konfiguratsiya va ish maydoni Gateway xostida joylashadi
  (`~/.openclaw` + sizning ish maydoni katalogingiz).
- **Zaruratga ko‘ra masofaviy:** model provayderlariga (Anthropic/OpenAI/etc.) yuborgan xabarlaringiz ularning API’lariga, shuningdek chat platformalari (WhatsApp/Telegram/Slack/etc.) xabar ma’lumotlarini o‘z serverlarida saqlaydi.
- **Izni siz boshqarasiz:** lokal modellarni ishlatish promptlarni kompyuteringizda qoldiradi, ammo kanal trafigi baribir kanal serverlari orqali o‘tadi.

Bog‘liq: [Agent workspace](/concepts/agent-workspace), [Memory](/concepts/memory).

### OpenClaw o‘z ma’lumotlarini qayerda saqlaydi

Hammasi `$OPENCLAW_STATE_DIR` ostida joylashgan (standart: `~/.openclaw`):

| Yo‘l                                                            | Maqsad                                                                                       |
| --------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `$OPENCLAW_STATE_DIR/openclaw.json`                             | Asosiy konfiguratsiya (JSON5)                                             |
| `$OPENCLAW_STATE_DIR/credentials/oauth.json`                    | Eski OAuth importi (birinchi foydalanishda auth profillarga ko‘chiriladi) |
| `$OPENCLAW_STATE_DIR/agents/<agentId>/agent/auth-profiles.json` | Auth profillar (OAuth + API kalitlar)                                     |
| `$OPENCLAW_STATE_DIR/agents/<agentId>/agent/auth.json`          | Ish vaqtidagi auth kesh (avtomatik boshqariladi)                          |
| `$OPENCLAW_STATE_DIR/credentials/`                              | Provayder holati (masalan `whatsapp/<accountId>/creds.json`)              |
| `$OPENCLAW_STATE_DIR/agents/`                                   | Har bir agent uchun holat (agentDir + sessiyalar)                         |
| `$OPENCLAW_STATE_DIR/agents/<agentId>/sessions/`                | Suhbat tarixi va holati (har bir agent uchun)                             |
| `$OPENCLAW_STATE_DIR/agents/<agentId>/sessions/sessions.json`   | Sessiya metama’lumotlari (har bir agent uchun)                            |

Eski bitta-agent yo‘li: `~/.openclaw/agent/*` (`openclaw doctor` tomonidan migratsiya qilinadi).

Sizning **ish maydoningiz** (AGENTS.md, xotira fayllari, ko‘nikmalar va h.k.) `agents.defaults.workspace` orqali alohida sozlanadi (standart: `~/.openclaw/workspace`).

### AGENTSmd SOULmd USERmd MEMORYmd qayerda bo‘lishi kerak

Bu fayllar `~/.openclaw` da emas, **agent ish maydoni**da joylashadi.

- **Ish maydoni (har bir agent uchun)**: `AGENTS.md`, `SOUL.md`, `IDENTITY.md`, `USER.md`,
  `MEMORY.md` (yoki `memory.md`), `memory/YYYY-MM-DD.md`, ixtiyoriy `HEARTBEAT.md`.
- **Holat katalogi (`~/.openclaw`)**: konfiguratsiya, credentiallar, auth profillar, sessiyalar, loglar,
  va umumiy ko‘nikmalar (`~/.openclaw/skills`).

Standart ish maydoni `~/.openclaw/workspace`, quyidagicha sozlanadi:

```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
}
```

Agar bot qayta ishga tushgandan keyin "unutsa", Gateway har safar ishga tushirilganda bir xil ish maydonidan foydalanayotganini tekshiring (va esda tuting: masofaviy rejim **gateway xosti**ning ish maydonidan foydalanadi, lokal noutbukingiznikidan emas).

Maslahat: agar uzoq muddatli xulq-atvor yoki afzallikni xohlasangiz, chat tarixiga tayanish o‘rniga botdan **uni AGENTS.md yoki MEMORY.md ga yozishni** so‘rang.

[Agent workspace](/concepts/agent-workspace) va [Memory](/concepts/memory) ga qarang.

### Tavsiya etilgan zaxiralash strategiyasi qanday

**Agent ish maydoningizni** **xususiy** git repozitoriyga joylashtiring va uni shaxsiy joyda zaxiralang (masalan, GitHub private). Bu xotira + AGENTS/SOUL/USER fayllarini qamrab oladi va yordamchining "ongini" keyinroq tiklash imkonini beradi.

`~/.openclaw` ostidagi hech narsani commit qilmang (credentiallar, sessiyalar, tokenlar).1) Agar sizga to‘liq tiklash kerak bo‘lsa, ish maydoni (workspace) va holat katalogini
   alohida-alohida zaxiralang (yuqoridagi migratsiya savoliga qarang).

2. Hujjatlar: [Agent workspace](/concepts/agent-workspace).

### 3. OpenClaw’ni qanday qilib to‘liq o‘chirib tashlayman

4. Maxsus qo‘llanmaga qarang: [Uninstall](/install/uninstall).

### 5. Agentlar ish maydonidan tashqarida ishlay oladimi

6. Ha. 7. Ish maydoni — bu **standart cwd** va xotira tayanchi, qat’iy sandbox emas.
7. Nisbiy yo‘llar ish maydoni ichida aniqlanadi, ammo mutlaq yo‘llar sandbox yoqilmagan bo‘lsa, boshqa xost joylariga kira oladi. 9. Agar izolyatsiya kerak bo‘lsa,
   [`agents.defaults.sandbox`](/gateway/sandboxing) yoki har bir agent uchun sandbox sozlamalaridan foydalaning. 10. Agar repozitoriy standart ishchi katalog bo‘lishini xohlasangiz, o‘sha agentning
   `workspace` ni repo ildiziga yo‘naltiring. 37. OpenClaw repozitoriyasi faqat manba kodidan iborat; agent ataylab uning ichida ishlashini xohlamasangiz, ish maydonini alohida saqlang.

12. Misol (repo standart cwd sifatida):

```json5
13. {
  agents: {
    defaults: {
      workspace: "~/Projects/my-repo",
    },
  },
}
```

### 14. Men remote rejimdaman, sessiya ombori qayerda

15. Sessiya holati **gateway xosti**ga tegishli. 16. Agar siz remote rejimda bo‘lsangiz, siz uchun muhim sessiya ombori lokal noutbukingizda emas, balki masofaviy mashinada joylashgan. 17. [Session management](/concepts/session) ga qarang.

## 38. Konfiguratsiya asoslari

### 19. Konfiguratsiya qaysi formatda va u qayerda

20. OpenClaw `$OPENCLAW_CONFIG_PATH` dan ixtiyoriy **JSON5** konfiguratsiyani o‘qiydi (standart: `~/.openclaw/openclaw.json`):

```
21. $OPENCLAW_CONFIG_PATH
```

22. Agar fayl mavjud bo‘lmasa, u xavfsizga yaqin standart sozlamalardan foydalanadi (jumladan `~/.openclaw/workspace` standart ish maydoni sifatida).

### 23. Gateway bind’ni lan yoki tailnet ga o‘rnatdim va endi hech narsa tinglamayapti, UI esa unauthorized deydi

24. Loopback bo‘lmagan bind’lar **autentifikatsiyani talab qiladi**. 25. `gateway.auth.mode` + `gateway.auth.token` ni sozlang (yoki `OPENCLAW_GATEWAY_TOKEN` dan foydalaning).

```json5
26. {
  gateway: {
    bind: "lan",
    auth: {
      mode: "token",
      token: "replace-me",
    },
  },
}
```

27. Eslatmalar:

- 28. `gateway.remote.token` faqat **remote CLI chaqiruvlari** uchun; u lokal gateway autentifikatsiyasini yoqmaydi.
- 29. Control UI `connect.params.auth.token` orqali autentifikatsiya qiladi (ilova/UI sozlamalarida saqlanadi). 30. Tokenlarni URL ichiga qo‘ymaslikka harakat qiling.

### 31. Nega endi localhost’da token kerak

32. Usta (wizard) standart holatda gateway tokenini yaratadi (hatto loopback’da ham), shuning uchun **lokal WS klientlari autentifikatsiyadan o‘tishi shart**. 33. Bu boshqa lokal jarayonlarning Gateway’ni chaqirishini bloklaydi. 34. Ulanish uchun tokenni Control UI sozlamalariga (yoki klient konfiguratsiyasiga) joylashtiring.

35. Agar siz **haqiqatan ham** ochiq loopback xohlasangiz, konfiguratsiyadan `gateway.auth` ni olib tashlang. 36. Doctor istalgan vaqtda siz uchun token yaratishi mumkin: `openclaw doctor --generate-gateway-token`.

### 37. Konfiguratsiyani o‘zgartirgandan keyin qayta ishga tushirishim kerakmi

38. Gateway konfiguratsiyani kuzatadi va hot-reload’ni qo‘llab-quvvatlaydi:

- 39. `gateway.reload.mode: "hybrid"` (standart): xavfsiz o‘zgarishlarni darhol qo‘llaydi, muhimlari uchun qayta ishga tushiradi
- 40. `hot`, `restart`, `off` ham qo‘llab-quvvatlanadi

### 41. Web search va web fetch’ni qanday yoqaman

42. `web_fetch` API kalitsiz ham ishlaydi. 43. `web_search` Brave Search API kalitini talab qiladi. 44. **Tavsiya etiladi:** uni `tools.web.search.apiKey` ga saqlash uchun `openclaw configure --section web` ni ishga tushiring. 45. Muhit varianti: Gateway jarayoni uchun `BRAVE_API_KEY` ni o‘rnating.

```json5
46. {
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

47. Eslatmalar:

- 48. Agar allowlist’lardan foydalansangiz, `web_search`/`web_fetch` yoki `group:web` ni qo‘shing.
- 49. `web_fetch` standart holatda yoqilgan (agar aniq o‘chirib qo‘yilmagan bo‘lsa).
- 50. Demonlar env o‘zgaruvchilarini `~/.openclaw/.env` dan (yoki servis muhiti) o‘qiydi.

Hujjatlar: [Web tools](/tools/web).

### Qanday qilib markaziy Gateway’ni turli qurilmalardagi ixtisoslashgan ishchilar bilan ishga tushiraman

Odatdagi naqsh — **bitta Gateway** (masalan, Raspberry Pi) va unga qo‘shilgan **node**lar hamda **agent**lar:

- 39. **Gateway (markaziy):** kanallarga (Signal/WhatsApp), marshrutlash va sessiyalarga egalik qiladi.
- **Node’lar (qurilmalar):** Mac/iOS/Android qurilmalari periferiyalar sifatida ulanadi va mahalliy vositalarni (`system.run`, `canvas`, `camera`) taqdim etadi.
- **Agentlar (ishchilar):** maxsus rollar uchun alohida miyalar/ish joylari (masalan, "Hetzner ops", "Shaxsiy ma’lumotlar").
- **Sub-agentlar:** parallellik kerak bo‘lganda asosiy agentdan fon ishlarini ishga tushiradi.
- **TUI:** Gateway’ga ulanib agentlar/sessiyalarni almashtirish.

Hujjatlar: [Nodes](/nodes), [Remote access](/gateway/remote), [Multi-Agent Routing](/concepts/multi-agent), [Sub-agents](/tools/subagents), [TUI](/web/tui).

### OpenClaw brauzeri headless rejimda ishlay oladimi

Ha. Bu konfiguratsiya opsiyasi:

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

Standart qiymat — `false` (oynali/headful). Headless rejim ayrim saytlarida anti-bot tekshiruvlarini ko‘proq qo‘zg‘atishi mumkin. Qarang: [Browser](/tools/browser).

Headless **xuddi shu Chromium dvigateli**dan foydalanadi va ko‘pchilik avtomatlashtirishlar (formalar, bosishlar, scraping, loginlar) uchun ishlaydi. Asosiy farqlar:

- Ko‘rinadigan brauzer oynasi yo‘q (vizual kerak bo‘lsa, skrinshotlardan foydalaning).
- Ba’zi saytlar headless rejimda avtomatlashtirishga nisbatan qattiqroq (CAPTCHA, anti-bot).
  Masalan, X/Twitter ko‘pincha headless sessiyalarni bloklaydi.

### Brauzer boshqaruvi uchun Brave’dan qanday foydalanaman

`browser.executablePath` ni Brave binaringizga (yoki istalgan Chromium-asosli brauzerga) sozlang va Gateway’ni qayta ishga tushiring.
To‘liq konfiguratsiya misollarini [Browser](/tools/browser#use-brave-or-another-chromium-based-browser) da ko‘ring.

## Masofaviy gateway’lar va node’lar

### Telegram, gateway va node’lar o‘rtasida buyruqlar qanday uzatiladi

Telegram xabarlari **gateway** tomonidan qayta ishlanadi. Gateway agentni ishga tushiradi va
faqat node vositasi kerak bo‘lgandagina **Gateway WebSocket** orqali node’larga murojaat qiladi:

Telegram → Gateway → Agent → `node.*` → Node → Gateway → Telegram

Node’lar kiruvchi provayder trafigini ko‘rmaydi; ular faqat node RPC chaqiruvlarini qabul qiladi.

### Gateway masofada joylashgan bo‘lsa, agentim kompyuterimga qanday kira oladi

Qisqa javob: **kompyuteringizni node sifatida juftlang**. Gateway boshqa joyda ishlaydi, lekin
Gateway WebSocket orqali mahalliy mashinangizdagi `node.*` vositalarini (ekran, kamera, tizim) chaqira oladi.

Odatdagi sozlama:

1. Gateway’ni doimiy yoqilgan xostda ishga tushiring (VPS/uy serveri).
2. Gateway xosti va kompyuteringizni bir xil tailnet’ga qo‘ying.
3. Gateway WS’ga ulanish mumkinligini ta’minlang (tailnet bind yoki SSH tunnel).
4. macOS ilovasini mahalliy ishga tushiring va **Remote over SSH** rejimida (yoki to‘g‘ridan-to‘g‘ri tailnet orqali) ulang,
   shunda u node sifatida ro‘yxatdan o‘ta oladi.
5. Gateway’da node’ni tasdiqlang:

   ```bash
   openclaw nodes pending
   openclaw nodes approve <requestId>
   ```

Alohida TCP bridge talab qilinmaydi; node’lar Gateway WebSocket orqali ulanadi.

Xavfsizlik eslatmasi: macOS node’ni juftlash ushbu mashinada `system.run` ga ruxsat beradi. Faqat
ishonchli qurilmalarni juftlang va [Security](/gateway/security) ni ko‘rib chiqing.

Hujjatlar: [Nodes](/nodes), [Gateway protocol](/gateway/protocol), [macOS remote mode](/platforms/mac/remote), [Security](/gateway/security).

### Tailscale ulangan, lekin javoblar yo‘q. Endi nima qilaman

Asosiylarini tekshiring:

- Gateway ishlayapti: `openclaw gateway status`
- Gateway holati: `openclaw status`
- Kanal holati: `openclaw channels status`

So‘ng autentifikatsiya va marshrutlashni tekshiring:

- If you use Tailscale Serve, make sure `gateway.auth.allowTailscale` is set correctly.
- If you connect via SSH tunnel, confirm the local tunnel is up and points at the right port.
- Confirm your allowlists (DM or group) include your account.

Docs: [Tailscale](/gateway/tailscale), [Remote access](/gateway/remote), [Channels](/channels).

### Can two OpenClaw instances talk to each other local VPS

Yes. There is no built-in "bot-to-bot" bridge, but you can wire it up in a few
reliable ways:

**Simplest:** use a normal chat channel both bots can access (Telegram/Slack/WhatsApp).
Have Bot A send a message to Bot B, then let Bot B reply as usual.

**CLI bridge (generic):** run a script that calls the other Gateway with
`openclaw agent --message ... --deliver`, targeting a chat where the other bot
listens. If one bot is on a remote VPS, point your CLI at that remote Gateway
via SSH/Tailscale (see [Remote access](/gateway/remote)).

Example pattern (run from a machine that can reach the target Gateway):

```bash
openclaw agent --message "Hello from local bot" --deliver --channel telegram --reply-to <chat-id>
```

Tip: add a guardrail so the two bots do not loop endlessly (mention-only, channel
allowlists, or a "do not reply to bot messages" rule).

Docs: [Remote access](/gateway/remote), [Agent CLI](/cli/agent), [Agent send](/tools/agent-send).

### Do I need separate VPSes for multiple agents

No. One Gateway can host multiple agents, each with its own workspace, model defaults,
and routing. That is the normal setup and it is much cheaper and simpler than running
one VPS per agent.

Use separate VPSes only when you need hard isolation (security boundaries) or very
different configs that you do not want to share. Otherwise, keep one Gateway and
use multiple agents or sub-agents.

### Is there a benefit to using a node on my personal laptop instead of SSH from a VPS

Yes - nodes are the first-class way to reach your laptop from a remote Gateway, and they
unlock more than shell access. The Gateway runs on macOS/Linux (Windows via WSL2) and is
lightweight (a small VPS or Raspberry Pi-class box is fine; 4 GB RAM is plenty), so a common
setup is an always-on host plus your laptop as a node.

- **No inbound SSH required.** Nodes connect out to the Gateway WebSocket and use device pairing.
- **Safer execution controls.** `system.run` is gated by node allowlists/approvals on that laptop.
- **More device tools.** Nodes expose `canvas`, `camera`, and `screen` in addition to `system.run`.
- **Local browser automation.** Keep the Gateway on a VPS, but run Chrome locally and relay control
  with the Chrome extension + a node host on the laptop.

SSH is fine for ad-hoc shell access, but nodes are simpler for ongoing agent workflows and
device automation.

Docs: [Nodes](/nodes), [Nodes CLI](/cli/nodes), [Chrome extension](/tools/chrome-extension).

### Should I install on a second laptop or just add a node

If you only need **local tools** (screen/camera/exec) on the second laptop, add it as a
**node**. That keeps a single Gateway and avoids duplicated config. Local node tools are
currently macOS-only, but we plan to extend them to other OSes.

Install a second Gateway only when you need **hard isolation** or two fully separate bots.

Docs: [Nodes](/nodes), [Nodes CLI](/cli/nodes), [Multiple gateways](/gateway/multiple-gateways).

### Do nodes run a gateway service

No. Only **one gateway** should run per host unless you intentionally run isolated profiles (see [Multiple gateways](/gateway/multiple-gateways)). Nodes are peripherals that connect
to the gateway (iOS/Android nodes, or macOS "node mode" in the menubar app). For headless node
hosts and CLI control, see [Node host CLI](/cli/node).

A full restart is required for `gateway`, `discovery`, and `canvasHost` changes.

### Is there an API RPC way to apply config

Yes. `config.apply` validates + writes the full config and restarts the Gateway as part of the operation.

### configapply wiped my config How do I recover and avoid this

`config.apply` replaces the **entire config**. If you send a partial object, everything
else is removed.

Recover:

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

2. **Install + login on your Mac**
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

This keeps the gateway bound to loopback and exposes HTTPS via Tailscale. See [Tailscale](/gateway/tailscale).

### How do I connect a Mac node to a remote Gateway Tailscale Serve

Serve exposes the **Gateway Control UI + WS**. Nodes connect over the same Gateway WS endpoint.

Recommended setup:

1. **Make sure the VPS + Mac are on the same tailnet**.
2. **Use the macOS app in Remote mode** (SSH target can be the tailnet hostname).
   40. Ilova Gateway portini tunnel qiladi va tugun sifatida ulanadi.
3. **Approve the node** on the gateway:

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

Bu login shell’ingizni ishga tushiradi va faqat yetishmayotgan kutilgan kalitlarni import qiladi (hech qachon ustiga yozmaydi). Env o‘zgaruvchilari ekvivalentlari:
`OPENCLAW_LOAD_SHELL_ENV=1`, `OPENCLAW_SHELL_ENV_TIMEOUT_MS=15000`.

### Men COPILOTGITHUBTOKEN ni o‘rnatdim, lekin modellar holatida Shell env o‘chiq ko‘rsatilmoqda. Nega?

`openclaw models status` **shell env import** yoqilgan-yo‘qligini bildiradi. "Shell env: off"
— bu env o‘zgaruvchilaringiz yo‘q degani **emas** — faqat OpenClaw login shell’ingizni avtomatik yuklamasligini anglatadi.

Agar Gateway servis sifatida (launchd/systemd) ishlayotgan bo‘lsa, u shell muhitini meros qilib olmaydi. Quyidagilardan birini qilib tuzating:

1. Tokenni `~/.openclaw/.env` ga qo‘ying:

   ```
   COPILOT_GITHUB_TOKEN=...
   ```

2. Yoki shell import’ni yoqing (`env.shellEnv.enabled: true`).

3. Yoki uni konfiguratsiyangizdagi `env` blokiga qo‘shing (faqat yo‘q bo‘lsa qo‘llanadi).

So‘ng gateway’ni qayta ishga tushiring va qayta tekshiring:

```bash
openclaw models status
```

Copilot tokenlari `COPILOT_GITHUB_TOKEN` dan o‘qiladi (shuningdek `GH_TOKEN` / `GITHUB_TOKEN`).
Qarang: [/concepts/model-providers](/concepts/model-providers) va [/environment](/help/environment).

## Sessiyalar va bir nechta chatlar

### Qanday qilib yangi suhbatni boshlayman

Alohida xabar sifatida `/new` yoki `/reset` yuboring. Qarang: [Session management](/concepts/session).

### Agar men hech qachon new yubormasam, sessiyalar avtomatik reset bo‘ladimi

Ha. Sessiyalar `session.idleMinutes` dan so‘ng muddati tugaydi (standart **60**). **Keyingi** xabar o‘sha chat kaliti uchun yangi sessiya ID’sini boshlaydi. Bu transkriptlarni o‘chirmaydi — faqat yangi sessiyani boshlaydi.

```json5
{
  session: {
    idleMinutes: 240,
  },
}
```

### OpenClaw instansiyalaridan iborat, bitta CEO va ko‘plab agentlardan tashkil topgan jamoa qilishning yo‘li bormi

Ha, **multi-agent routing** va **sub-agentlar** orqali. Siz bitta koordinatsiya qiluvchi agent va o‘z ish joylari hamda modellari bo‘lgan bir nechta ishchi agentlarni yaratishingiz mumkin.

Shuni aytish kerakki, bu ko‘proq **qiziqarli tajriba** sifatida qaraladi. Bu ko‘p token talab qiladi va ko‘pincha alohida sessiyalarga ega bitta botdan kamroq samarali bo‘ladi. Biz tasavvur qiladigan odatiy model — siz gaplashadigan bitta bot va parallel ishlar uchun turli sessiyalar. Zarur bo‘lganda u bot sub-agentlarni ham ishga tushirishi mumkin.

Hujjatlar: [Multi-agent routing](/concepts/multi-agent), [Sub-agents](/tools/subagents), [Agents CLI](/cli/agents).

### Nega kontekst vazifa o‘rtasida kesilib ketdi va buni qanday oldini olaman

Sessiya konteksti model oynasi bilan cheklangan. Uzoq chatlar, katta tool chiqishlari yoki ko‘p fayllar kompaktlash yoki kesib tashlashni keltirib chiqarishi mumkin.

Nima yordam beradi:

- Botdan joriy holatni qisqacha bayon qilib, uni faylga yozishni so‘rang.
- Uzoq vazifalardan oldin `/compact` dan foydalaning va mavzuni almashtirganda `/new` qiling.
- Muhim kontekstni workspace’da saqlang va botdan uni qayta o‘qib chiqishni so‘rang.
- Uzoq yoki parallel ishlar uchun sub-agentlardan foydalaning, shunda asosiy chat kichikroq bo‘lib qoladi.
- Agar bu tez-tez sodir bo‘lsa, kattaroq kontekst oynasiga ega modelni tanlang.

### OpenClaw’ni butunlay reset qilib, lekin o‘rnatilgan holda qoldirishim mumkinmi

Reset buyrug‘idan foydalaning:

```bash
openclaw reset
```

Interaktiv bo‘lmagan to‘liq reset:

```bash
openclaw reset --scope full --yes --non-interactive
```

So‘ng onboarding’ni qayta ishga tushiring:

```bash
openclaw onboard --install-daemon
```

Notes:

- The onboarding wizard also offers **Reset** if it sees an existing config. See [Wizard](/start/wizard).
- If you used profiles (`--profile` / `OPENCLAW_PROFILE`), reset each state dir (defaults are `~/.openclaw-<profile>`).
- Dev reset: `openclaw gateway --dev --reset` (dev-only; wipes dev config + credentials + sessions + workspace).

### Im getting context too large errors how do I reset or compact

Use one of these:

- **Compact** (keeps the conversation but summarizes older turns):

  ```
  /compact
  ```

  or `/compact <instructions>` to guide the summary.

- **Reset** (fresh session ID for the same chat key):

  ```
  /new
  /reset
  ```

If it keeps happening:

- Enable or tune **session pruning** (`agents.defaults.contextPruning`) to trim old tool output.
- Use a model with a larger context window.

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

Per-agent overrides use `agents.list[].heartbeat`. Docs: [Heartbeat](/gateway/heartbeat).

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

Direct chats collapse to the main session by default. Groups/channels have their own session keys, and Telegram topics / Discord threads are separate sessions. See [Groups](/channels/groups) and [Group messages](/channels/group-messages).

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
channel/account/peer. Slack is supported as a channel and can be bound to specific agents.

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

OpenClaw's default model is whatever you set as:

```
agents.defaults.model.primary
```

Models are referenced as `provider/model` (example: `anthropic/claude-opus-4-6`). If you omit the provider, OpenClaw currently assumes `anthropic` as a temporary deprecation fallback - but you should still **explicitly** set `provider/model`.

### What model do you recommend

**Recommended default:** `anthropic/claude-opus-4-6`.
**Good alternative:** `anthropic/claude-sonnet-4-5`.
**Reliable (less character):** `openai/gpt-5.2` - nearly as good as Opus, just less personality.
**Budget:** `zai/glm-4.7`.

MiniMax M2.1 has its own docs: [MiniMax](/providers/minimax) and
[Local models](/gateway/local-models).

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

**How do I unpin a profile I set with profile**

Re-run `/model` **without** the `@profile` suffix:

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

- Agent A default: MiniMax
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

This usually means the **new agent** has an empty auth store. Auth is per-agent and
stored in:

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
2. **Model fallback** `agents.defaults.model.fallbacks` dagi keyingi modelga o‘tadi.

Cooldownlar muvaffaqiyatsiz profillarga qo‘llanadi (eksponensial backoff), shuning uchun OpenClaw provayder tezlik chekloviga tushgan yoki vaqtincha ishlamayotgan bo‘lsa ham javob berishda davom eta oladi.

### Bu xato nimani anglatadi

```
"anthropic:default" profili uchun hech qanday credentials topilmadi
```

Bu tizim `anthropic:default` auth profili ID’sidan foydalanishga uringanini, ammo kutilgan auth omborida unga mos credentials topa olmaganini anglatadi.

### anthropicdefault profili uchun No credentials found xatosini tuzatish bo‘yicha chek-list

- **Auth profillari qayerda joylashganini tasdiqlang** (yangi va eski yo‘llar)
  - Joriy: `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
  - Eski: `~/.openclaw/agent/*` (`openclaw doctor` tomonidan ko‘chiriladi)
- **Gateway tomonidan env var yuklanayotganini tasdiqlang**
  - Agar `ANTHROPIC_API_KEY` ni shell’da sozlab, Gateway’ni systemd/launchd orqali ishga tushirsangiz, u uni meros qilib olmasligi mumkin. Uni `~/.openclaw/.env` ga joylashtiring yoki `env.shellEnv` ni yoqing.
- **To‘g‘ri agentni tahrirlayotganingizga ishonch hosil qiling**
  - Multi-agent sozlamalarda bir nechta `auth-profiles.json` fayllari bo‘lishi mumkin.
- **Model/auth holatini tekshirib ko‘ring**
  - Sozlangan modellar va provayderlar autentifikatsiyadan o‘tgan-o‘tmaganini ko‘rish uchun `openclaw models status` dan foydalaning.

anthropic profili uchun No credentials found xatosini tuzatish bo‘yicha chek-list

Bu ishga tushirish Anthropic auth profiliga qattiq bog‘langanini, ammo Gateway uni o‘z auth omborida topa olmayotganini anglatadi.

- **Setup-token’dan foydalaning**
  - `claude setup-token` ni ishga tushiring, so‘ng uni `openclaw models auth setup-token --provider anthropic` bilan joylashtiring.
  - Agar token boshqa mashinada yaratilgan bo‘lsa, `openclaw models auth paste-token --provider anthropic` dan foydalaning.

- **Agar API key’dan foydalanmoqchi bo‘lsangiz**
  - `ANTHROPIC_API_KEY` ni **gateway host** dagi `~/.openclaw/.env` ga joylashtiring.
  - Mavjud bo‘lmagan profilni majburlovchi har qanday pinlangan tartibni tozalang:

    ```bash
    openclaw models auth order clear --provider anthropic
    ```

- **Buyruqlarni gateway host’da ishga tushirayotganingizni tasdiqlang**
  - Remote rejimda auth profillari noutbukingizda emas, gateway mashinasida joylashadi.

### Nega u Google Gemini’ni ham sinab ko‘rib, muvaffaqiyatsiz bo‘ldi

Agar model konfiguratsiyangizda Google Gemini fallback sifatida kiritilgan bo‘lsa (yoki siz Gemini shorthand’iga o‘tgansangiz), OpenClaw model fallback jarayonida uni sinab ko‘radi. Agar Google credentials sozlanmagan bo‘lsa, `No API key found for provider "google"` xabarini ko‘rasiz.

Tuzatish: Google auth’ni taqdim eting yoki fallback u yerga yo‘naltirilmasligi uchun `agents.defaults.model.fallbacks` / aliaslardan Google modellarini olib tashlang yoki ishlatmang.

**LLM request rejected message thinking signature required google antigravity**

Sabab: sessiya tarixida **imzosiz thinking bloklari** mavjud (ko‘pincha bekor qilingan/qisman stream natijasida). Google Antigravity thinking bloklari uchun imzolarni talab qiladi.

Tuzatish: OpenClaw endi Google Antigravity Claude uchun imzosiz thinking bloklarini olib tashlaydi. Agar baribir chiqsa, **yangi sessiya** boshlang yoki ushbu agent uchun `/thinking off` ni o‘rnating.

## Auth profillari: ular nima va ularni qanday boshqarish

Bog‘liq: [/concepts/oauth](/concepts/oauth) (OAuth jarayonlari, token saqlash, multi-account andozalari)

### Auth profili nima

Auth profili — bu provayderga bog‘langan, nomlangan credentials yozuvi (OAuth yoki API key). Profillar quyida joylashadi:

```
~/.openclaw/agents/<agentId>/agent/auth-profiles.json
```

### Odatdagi profil ID’lari qanday

OpenClaw provayder-prefiksli ID’lardan foydalanadi, masalan:

- `anthropic:default` (email identifikatori mavjud bo‘lmaganda keng tarqalgan)
- `anthropic:<email>` OAuth identifikatorlari uchun
- 41. Siz tanlaydigan maxsus ID’lar (masalan, `anthropic:work`)

### Qaysi auth profili birinchi bo‘lib sinab ko‘rilishini boshqara olamanmi

Ha. Konfiguratsiya profillar uchun ixtiyoriy metadata va har bir provayder bo‘yicha tartibni qo‘llab-quvvatlaydi (`auth.order.<provider>`)\`). This does **not** store secrets; it maps IDs to provider/mode and sets rotation order.

OpenClaw may temporarily skip a profile if it's in a short **cooldown** (rate limits/timeouts/auth failures) or a longer **disabled** state (billing/insufficient credits). To inspect this, run `openclaw models status --json` and check `auth.unusableProfiles`. Tuning: `auth.cooldowns.billingBackoffHours*`.

You can also set a **per-agent** order override (stored in that agent's `auth-profiles.json`) via the CLI:

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

To target a specific agent:

```bash
openclaw models auth order set --provider anthropic --agent main anthropic:default
```

### OAuth vs API key whats the difference

OpenClaw supports both:

- **OAuth** often leverages subscription access (where applicable).
- **API keys** use pay-per-token billing.

The wizard explicitly supports Anthropic setup-token and OpenAI Codex OAuth and can store API keys for you.

## Gateway: ports, "already running", and remote mode

### What port does the Gateway use

`gateway.port` controls the single multiplexed port for WebSocket + HTTP (Control UI, hooks, etc.).

Precedence:

```
--port > OPENCLAW_GATEWAY_PORT > gateway.port > default 18789
```

### Why does openclaw gateway status say Runtime running but RPC probe failed

Because "running" is the **supervisor's** view (launchd/systemd/schtasks). The RPC probe is the CLI actually connecting to the gateway WebSocket and calling `status`.

Use `openclaw gateway status` and trust these lines:

- `Probe target:` (the URL the probe actually used)
- `Listening:` (what's actually bound on the port)
- `Last gateway error:` (common root cause when the process is alive but the port isn't listening)

### Why does openclaw gateway status show Config cli and Config service different

You're editing one config file while the service is running another (often a `--profile` / `OPENCLAW_STATE_DIR` mismatch).

Fix:

```bash
openclaw gateway install --force
```

Run that from the same `--profile` / environment you want the service to use.

### What does another gateway instance is already listening mean

OpenClaw enforces a runtime lock by binding the WebSocket listener immediately on startup (default `ws://127.0.0.1:18789`). If the bind fails with `EADDRINUSE`, it throws `GatewayLockError` indicating another instance is already listening.

Fix: stop the other instance, free the port, or run with `openclaw gateway --port <port>`.

### How do I run OpenClaw in remote mode client connects to a Gateway elsewhere

Set `gateway.mode: "remote"` and point to a remote WebSocket URL, optionally with a token/password:

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

Notes:

- `openclaw gateway` only starts when `gateway.mode` is `local` (or you pass the override flag).
- The macOS app watches the config file and switches modes live when these values change.

### The Control UI says unauthorized or keeps reconnecting What now

Your gateway is running with auth enabled (`gateway.auth.*`), but the UI is not sending the matching token/password.

Facts (from code):

- The Control UI stores the token in browser localStorage key `openclaw.control.settings.v1`.

Fix:

- Fastest: `openclaw dashboard` (prints + copies the dashboard URL, tries to open; shows SSH hint if headless).
- If you don't have a token yet: `openclaw doctor --generate-gateway-token`.
- If remote, tunnel first: `ssh -N -L 18789:127.0.0.1:18789 user@host` then open `http://127.0.0.1:18789/`.
- Set `gateway.auth.token` (or `OPENCLAW_GATEWAY_TOKEN`) on the gateway host.
- 1. Control UI sozlamalarida xuddi shu tokenni joylashtiring.
- 2. Hali ham muammo bormi? 3. `openclaw status --all` ni ishga tushiring va [Troubleshooting](/gateway/troubleshooting) bo‘yicha ko‘rsatmalarga amal qiling. 4. Avtorizatsiya tafsilotlari uchun [Dashboard](/web/dashboard) ni ko‘ring.

### 5. Men gatewaybind tailnet ni sozladim, lekin u bog‘lana olmayapti, hech narsa tinglamayapti.

6. `tailnet` bind tarmoq interfeyslaringizdan Tailscale IP ni tanlaydi (100.64.0.0/10). 7. Agar mashina Tailscale’da bo‘lmasa (yoki interfeys o‘chiq bo‘lsa), bog‘lanish uchun hech narsa yo‘q.

8. Tuzatish:

- 9. O‘sha xostda Tailscale’ni ishga tushiring (shunda u 100.x manzilga ega bo‘ladi), yoki
- 10. `gateway.bind: "loopback"` / `"lan"` ga o‘ting.

11. Eslatma: `tailnet` aniq ko‘rsatilgan. 12. `auto` loopback’ni afzal ko‘radi; faqat tailnet uchun bind kerak bo‘lsa `gateway.bind: "tailnet"` dan foydalaning.

### 13. Bir xil xostda bir nechta Gateway ishga tushira olamanmi

14. Odatda yo‘q — bitta Gateway bir nechta xabar almashish kanallari va agentlarni yurita oladi. 15. Bir nechta Gateway’dan faqat redundansiya (masalan: qutqaruv boti) yoki qat’iy izolyatsiya kerak bo‘lganda foydalaning.

16. Ha, lekin izolyatsiya qilishingiz kerak:

- 17. `OPENCLAW_CONFIG_PATH` (har bir instansiya uchun konfiguratsiya)
- 18. `OPENCLAW_STATE_DIR` (har bir instansiya uchun holat)
- 19. `agents.defaults.workspace` (ish joyini izolyatsiya qilish)
- 20. `gateway.port` (noyob portlar)

21. Tezkor sozlash (tavsiya etiladi):

- 22. Har bir instansiya uchun `openclaw --profile <name> …` dan foydalaning (`~/.openclaw-<name>` avtomatik yaratiladi).
- 23. Har bir profil konfiguratsiyasida noyob `gateway.port` ni belgilang (yoki qo‘lda ishga tushirish uchun `--port` ni bering).
- 24. Har bir profil uchun servis o‘rnating: `openclaw --profile <name> gateway install`.

25. Profil nomlari servis nomlariga ham qo‘shimcha sifatida qo‘shiladi (`bot.molt.<profile>`26. `; legacy `com.openclaw.\*`, `openclaw-gateway-<profile>.service`, `OpenClaw Gateway (<profile>)\`).
26. To‘liq qo‘llanma: [Multiple gateways](/gateway/multiple-gateways).

### 28. invalid handshake code 1008 nimani anglatadi

29. Gateway — bu **WebSocket server**, va u birinchi xabar sifatida 30. `connect` freymi kelishini kutadi.

31. Agar u boshqa biror narsa olsa, ulanishni

- 42. Siz WS klienti o‘rniga brauzerda **HTTP** URL’ni (`http://...`) ochgansiz.
- 33. Keng tarqalgan sabablar:
- 34. Siz WS mijoz o‘rniga brauzerda **HTTP** URL’ni (`http://...`) ochgansiz.

35. Noto‘g‘ri port yoki yo‘ldan foydalangansiz.

1. 36. Proksi yoki tunnel avtorizatsiya sarlavhalarini olib tashlagan yoki Gateway’ga aloqasi bo‘lmagan so‘rov yuborgan.
2. 37. Tezkor yechimlar:
3. 43. Agar autentifikatsiya yoqilgan bo‘lsa, `connect` freymiga token/parolni kiriting.

39) WS portini oddiy brauzer yorlig‘ida ochmang.

```
40. Agar avtorizatsiya yoqilgan bo‘lsa, `connect` freymiga token/parolni kiriting.
```

41. Agar CLI yoki TUI’dan foydalansangiz, URL quyidagicha bo‘lishi kerak:

## 42. openclaw tui --url ws://<host>:18789 --token <token>

### 43. Protokol tafsilotlari: [Gateway protocol](/gateway/protocol).

44. Loglash va nosozliklarni aniqlash

```
45. Loglar qayerda
```

46. Fayl loglari (strukturali): 47. /tmp/openclaw/openclaw-YYYY-MM-DD.log 48. Barqaror yo‘lni `logging.file` orqali sozlashingiz mumkin.

49. Fayl log darajasi `logging.level` bilan boshqariladi.

```bash
50. Konsol tafsilot darajasi `--verbose` va `logging.consoleLevel` bilan boshqariladi.
```

1. Xizmat/supervisor loglari (gateway launchd/systemd orqali ishga tushganda):

- 2. macOS: `$OPENCLAW_STATE_DIR/logs/gateway.log` va `gateway.err.log` (standart: `~/.openclaw/logs/...`; profillar `~/.openclaw-<profile>/logs/...` dan foydalanadi)
- 3. Linux: `journalctl --user -u openclaw-gateway[-<profile>].service -n 200 --no-pager`
- 4. Windows: `schtasks /Query /TN "OpenClaw Gateway (<profile>)" /V /FO LIST`

5. Batafsil maʼlumot uchun [Troubleshooting](/gateway/troubleshooting#log-locations) bo‘limiga qarang.

### 6. Gateway xizmatini qanday start/stop/restart qilaman

7. Gateway yordamchi buyruqlaridan foydalaning:

```bash
openclaw gateway status
openclaw gateway restart
```

9. Agar gateway’ni qo‘lda ishga tushirayotgan bo‘lsangiz, `openclaw gateway --force` portni qayta egallashi mumkin. 10. [Gateway](/gateway) bo‘limiga qarang.

### 11. Windows’da terminalni yopib qo‘ydim, OpenClaw’ni qanday qayta ishga tushiraman

12. **Windows’da ikki xil o‘rnatish rejimi mavjud**:

13. **1) WSL2 (tavsiya etiladi):** Gateway Linux ichida ishlaydi.

14. PowerShell’ni oching, WSL’ga kiring, so‘ng qayta ishga tushiring:

```powershell
wsl
openclaw gateway status
openclaw gateway restart
```

16. Agar xizmatni hech qachon o‘rnatmagan bo‘lsangiz, uni oldingi rejimda ishga tushiring:

```bash
openclaw gateway run
```

18. **2) Native Windows (tavsiya etilmaydi):** Gateway bevosita Windows’da ishlaydi.

19. PowerShell’ni ochib, quyidagilarni bajaring:

```powershell
openclaw gateway status
openclaw gateway restart
```

21. Agar uni qo‘lda ishga tushirayotgan bo‘lsangiz (xizmatsiz), quyidagidan foydalaning:

```powershell
openclaw gateway run
```

23. Hujjatlar: [Windows (WSL2)](/platforms/windows), [Gateway service runbook](/gateway).

### 24. Gateway ishlayapti, lekin javoblar kelmayapti. Nimani tekshirishim kerak

25. Tezkor sog‘liq tekshiruvidan boshlang:

```bash
openclaw status
openclaw models status
openclaw channels status
openclaw logs --follow
```

27. Keng tarqalgan sabablar:

- 28. **Gateway host**’da model autentifikatsiyasi yuklanmagan ( `models status` ni tekshiring).
- 29. Kanal juftlashuvi/allowlist javoblarni bloklayapti (kanal konfiguratsiyasi va loglarni tekshiring).
- 30. WebChat/Dashboard noto‘g‘ri token bilan ochilgan.

31. Agar masofadan ulangan bo‘lsangiz, tunnel/Tailscale ulanishi faol ekanini va Gateway WebSocket’iga ulanib bo‘lishini tasdiqlang.

44. Hujjatlar: [Channels](/channels), [Troubleshooting](/gateway/troubleshooting), [Remote access](/gateway/remote).

### 33. Gateway’dan hech qanday sababsiz uzildim, endi nima qilaman

45. Bu odatda UI WebSocket ulanishini yo‘qotganini anglatadi. 46. Tekshiring:

1. 36. Gateway ishlayaptimi? `openclaw gateway status`
2. 38. Gateway sog‘lom holatdami? `openclaw status`
3. 40. UI’da to‘g‘ri token bormi? `openclaw dashboard`
4. 42. Agar masofadan bo‘lsa, tunnel/Tailscale ulanishi faolmi?

43) So‘ng loglarni kuzating:

```bash
openclaw logs --follow
```

45. Hujjatlar: [Dashboard](/web/dashboard), [Remote access](/gateway/remote), [Troubleshooting](/gateway/troubleshooting).

### 46. Telegram setMyCommands tarmoq xatolari bilan ishlamayapti. Nimani tekshirishim kerak

47. Loglar va kanal holatidan boshlang:

```bash
openclaw channels status
openclaw channels logs --channel telegram
```

49. Agar VPS’da yoki proxy ortida bo‘lsangiz, chiqish HTTPS ruxsat etilganini va DNS ishlayotganini tasdiqlang.
50. Agar Gateway masofada bo‘lsa, Gateway xostidagi loglarga qarayotganingizga ishonch hosil qiling.

Hujjatlar: [Telegram](/channels/telegram), [Kanal muammolarini bartaraf etish](/channels/troubleshooting).

### TUI hech qanday chiqish ko‘rsatmayapti. Nimani tekshirishim kerak?

Avval Gateway mavjudligini va agent ishga tusha olishini tasdiqlang:

```bash
openclaw status
openclaw models status
openclaw logs --follow
```

TUI’da joriy holatni ko‘rish uchun `/status` dan foydalaning. Agar chat kanalida javoblar kutayotgan bo‘lsangiz, yetkazib berish yoqilganligiga ishonch hosil qiling (`/deliver on`).

Hujjatlar: [TUI](/web/tui), [Slash buyruqlar](/tools/slash-commands).

### Gateway’ni to‘liq to‘xtatib, keyin qayta ishga tushirishning yo‘li qanday?

Agar xizmatni o‘rnatgan bo‘lsangiz:

```bash
openclaw gateway stop
openclaw gateway start
```

Bu **nazorat qilinadigan xizmat**ni to‘xtatadi/ishga tushiradi (macOS’da launchd, Linux’da systemd).
48. Gateway fon rejimida daemon sifatida ishlaganda buni qo‘llang.

Agar oldingi rejimda ishlayotgan bo‘lsangiz, Ctrl-C bilan to‘xtating, so‘ng:

```bash
openclaw gateway run
```

Hujjatlar: [Gateway service runbook](/gateway).

### ELI5: openclaw gateway restart va openclaw gateway o‘rtasidagi farq

- `openclaw gateway restart`: **fon xizmati**ni (launchd/systemd) qayta ishga tushiradi.
- `openclaw gateway`: gateway’ni ushbu terminal sessiyasi uchun **oldingi rejimda** ishga tushiradi.

Agar xizmatni o‘rnatgan bo‘lsangiz, gateway buyruqlaridan foydalaning. Bir martalik, oldingi rejimda ishga tushirishni xohlasangiz `openclaw gateway` dan foydalaning.

### Biror narsa muvaffaqiyatsiz bo‘lganda ko‘proq tafsilotlarni olishning eng tez yo‘li qanday?

Ko‘proq konsol tafsilotlari uchun Gateway’ni `--verbose` bilan ishga tushiring. So‘ng kanal autentifikatsiyasi, model marshrutlash va RPC xatolari uchun log faylini tekshiring.

## Media va biriktirmalar

### Mening ko‘nikmam rasm/PDF yaratdi, ammo hech narsa yuborilmadi

Agentdan yuboriladigan tashqi biriktirmalar albatta `MEDIA:<path-or-url>` qatorini (alohida qatorda) o‘z ichiga olishi kerak. [OpenClaw assistant setup](/start/openclaw) va [Agent send](/tools/agent-send) ga qarang.

49. CLI yuborishi:

```bash
openclaw message send --target +15555550123 --message "Here you go" --media /path/to/file.png
```

50. Shuningdek tekshiring:

- Maqsad kanal chiqish media-ni qo‘llab-quvvatlaydi va ruxsat ro‘yxatlari (allowlist) tomonidan bloklanmagan.
- Fayl provayderning hajm cheklovlari doirasida ekanligini (rasmlar maksimal 2048px gacha o‘lchami o‘zgartiriladi).

[Images](/nodes/images) ga qarang.

## Xavfsizlik va kirish nazorati

### OpenClaw’ni kiruvchi DM’larga ochish xavfsizmi

Kiruvchi DM’larni ishonchsiz kiritma sifatida ko‘ring. Standart sozlamalar xavfni kamaytirish uchun mo‘ljallangan:

- DM’ga qodir kanallarda standart xatti-harakat — **juftlash**:
  - Noma’lum jo‘natuvchilar juftlash kodi oladi; bot ularning xabarini qayta ishlamaydi.
  - Tasdiqlash: `openclaw pairing approve <channel> <code>`
  - Kutilayotgan so‘rovlar **har bir kanal uchun 3 ta** bilan cheklangan; agar kod kelmagan bo‘lsa `openclaw pairing list <channel>` ni tekshiring.
- DM’larni ommaviy ochish aniq rozilikni talab qiladi (`dmPolicy: "open"` va allowlist `"*"`).

Xavfli DM siyosatlarini aniqlash uchun `openclaw doctor` ni ishga tushiring.

### Prompt injection faqat ommaviy botlar uchun muammomi?

Yo‘q. Prompt injection — bu faqat kim botga DM yubora olishi haqida emas, balki **ishonchsiz kontent** haqidadir.
Agar yordamchingiz tashqi kontentni o‘qisa (veb qidiruv/yuklash, brauzer sahifalari, elektron pochta,
hujjatlar, biriktirmalar, qo‘lda qo‘shilgan loglar), u kontent modelni egallab olishga urinadigan ko‘rsatmalarni o‘z ichiga olishi mumkin. Bu **faqat siz jo‘natuvchi bo‘lsangiz ham** sodir bo‘lishi mumkin.

Eng katta xavf vositalar yoqilganda yuzaga keladi: model kontekstni tashqariga chiqarishga yoki siz nomingizdan vositalarni chaqirishga aldanishi mumkin. Ta’sir doirasini kamaytirish yo‘llari:

- ishonchsiz kontentni qisqacha bayon qilish uchun faqat o‘qish yoki vositalari o‘chirilgan "reader" agentidan foydalanish
- vositalar yoqilgan agentlar uchun `web_search` / `web_fetch` / `browser` ni o‘chiq holda saqlash
- sandboxlash va qat’iy ruxsat etilgan vositalar ro‘yxati

Tafsilotlar: [Security](/gateway/security).

### Botim uchun alohida email, GitHub akkaunti yoki telefon raqami bo‘lishi kerakmi

Ha, aksariyat sozlamalar uchun. Botni alohida akkauntlar va telefon raqamlari bilan izolyatsiya qilish
agar nimadir noto‘g‘ri ketsa, zararning ta’sir doirasini kamaytiradi. Bu shuningdek shaxsiy akkauntlaringizga ta’sir qilmasdan
hisob ma’lumotlarini almashtirish yoki kirishni bekor qilishni osonlashtiradi.

Kichikdan boshlang. Faqat haqiqatan kerak bo‘lgan vositalar va akkauntlargagina ruxsat bering, va zarur bo‘lsa
keyinroq kengaytiring.

Hujjatlar: [Security](/gateway/security), [Pairing](/channels/pairing).

### Matnli xabarlarim ustidan unga avtonomiya bera olamanmi va bu xavfsizmi

Biz shaxsiy xabarlaringiz ustidan to‘liq avtonomiyani **tavsiya etmaymiz**. Eng xavfsiz andoza:

- DMlarni **pairing mode**da yoki qat’iy ruxsat ro‘yxati bilan saqlang.
- Agar u siz nomingizdan xabar yuborishini xohlasangiz, **alohida raqam yoki akkaunt**dan foydalaning.
- Unga qoralama yozdiring, so‘ng **yuborishdan oldin tasdiqlang**.

Agar tajriba qilmoqchi bo‘lsangiz, buni maxsus akkauntda qiling va uni izolyatsiyada saqlang. Qarang
[Security](/gateway/security).

### Shaxsiy yordamchi vazifalar uchun arzonroq modellardan foydalansam bo‘ladimi

Ha, **agar** agent faqat chat uchun bo‘lsa va kirish ma’lumotlari ishonchli bo‘lsa. Kichikroq darajalar
ko‘rsatmalarni egallab olishga ko‘proq moyil, shuning uchun ularni vositalari yoqilgan agentlar uchun
yoki ishonchsiz kontentni o‘qishda ishlatmang. Agar kichikroq modeldan foydalanishingiz kerak bo‘lsa, asboblarni (tools) qat’iy cheklang va sandbox ichida ishga tushiring. Qarang [Security](/gateway/security).

### Telegramda startni ishga tushirdim, lekin pairing kodi kelmadi

Pairing kodlari **faqat** noma’lum yuboruvchi botga xabar yuborganda va
`dmPolicy: "pairing"` yoqilgan bo‘lsa yuboriladi. `/start`ning o‘zi kod yaratmaydi.

Kutilayotgan so‘rovlarni tekshiring:

```bash
openclaw pairing list telegram
```

Agar darhol kirish kerak bo‘lsa, yuboruvchi IDingizni allowlistga qo‘shing yoki
shu akkaunt uchun `dmPolicy: "open"`ni o‘rnating.

### WhatsApp: u kontaktlarimga xabar yuboradimi? Pairing qanday ishlaydi

Yo‘q. WhatsApp uchun standart DM siyosati — **pairing**. Noma’lum yuboruvchilar faqat pairing kodini oladi va ularning xabari **qayta ishlanmaydi**. OpenClaw faqat o‘zi qabul qilgan chatlarga yoki siz qo‘zg‘atgan aniq yuborishlarga javob beradi.

Pairingni tasdiqlang:

```bash
openclaw pairing approve whatsapp <code>
```

Kutilayotgan so‘rovlar ro‘yxati:

```bash
openclaw pairing list whatsapp
```

Wizard’dagi telefon raqami so‘rovi: u **allowlist/owner**ni o‘rnatish uchun ishlatiladi, shunda o‘zingizning DMlaringizga ruxsat beriladi. U avtomatik yuborish uchun ishlatilmaydi. Agar shaxsiy WhatsApp raqamingizda ishga tushirsangiz, o‘sha raqamni kiriting va `channels.whatsapp.selfChatMode`ni yoqing.

## Chat buyruqlari, vazifalarni to‘xtatish va "u to‘xtamayapti"

### Chatda ichki tizim xabarlarining ko‘rinishini qanday to‘xtataman

Ko‘pchilik ichki yoki vosita xabarlari faqat shu sessiya uchun **verbose** yoki **reasoning** yoqilganda ko‘rinadi
.

U ko‘rinayotgan chatning o‘zida tuzating:

```
/verbose off
/reasoning off
```

Agar hanuz shovqin bo‘lsa, Control UI’dagi sessiya sozlamalarini tekshiring va verbose’ni **inherit**ga o‘rnating. Shuningdek, konfiguratsiyada `verboseDefault` `on` qilib o‘rnatilgan bot profilidan foydalanmayotganingizni tasdiqlang.

Hujjatlar: [Thinking and verbose](/tools/thinking), [Security](/gateway/security#reasoning--verbose-output-in-groups).

### Qanday qilib ishlayotgan vazifani to‘xtatishbekor qilish mumkin

Quyidagilardan istalganini **alohida xabar sifatida** yuboring (slashsiz):

```
stop
abort
esc
wait
exit
interrupt
```

Bular bekor qilish triggerlari (slash buyruqlar emas).

Fon jarayonlari uchun (exec asbobidan), agentdan quyidagini ishga tushirishni so‘rashingiz mumkin:

```
process action:kill sessionId:XXX
```

Slash buyruqlar sharhi: qarang [Slash commands](/tools/slash-commands).

Ko‘pchilik buyruqlar `/` bilan boshlanadigan **alohida** xabar sifatida yuborilishi kerak, ammo ayrim qisqa yo‘llar (masalan, `/status`) ruxsat berilgan jo‘natuvchilar uchun inline ham ishlaydi.

### Telegram’dan Discord xabarini qanday yuboraman Crosscontext xabar almashinuvi rad etildi

OpenClaw sukut bo‘yicha **provayderlararo** xabar almashuvni bloklaydi. Agar vosita chaqiruvi
Telegramga bog‘langan bo‘lsa, siz aniq ruxsat bermaguningizcha u Discordga yubormaydi.

Agent uchun kross-provayder xabarlashuvni yoqing:

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

Konfiguratsiyani tahrirlagandan so‘ng gateway’ni qayta ishga tushiring. Agar buni faqat bitta agent uchun xohlasangiz, uni `agents.list[].tools.message` ostida sozlang.

### Nega bot tez-tez yuborilgan xabarlarni e’tiborsiz qoldirgandek tuyuladi

Queue rejimi yangi xabarlar davom etayotgan ish bilan qanday o‘zaro ta’sirlashishini boshqaradi. Rejimlarni o‘zgartirish uchun `/queue` dan foydalaning:

- `steer` - yangi xabarlar joriy vazifani yo‘naltiradi
- `followup` - xabarlarni birma-bir bajaradi
- `collect` - xabarlarni to‘plab, bir marta javob beradi (standart)
- `steer-backlog` - hozir yo‘naltiradi, so‘ng backlog’ni qayta ishlaydi
- `interrupt` - joriy ishni bekor qiladi va yangidan boshlaydi

Followup rejimlari uchun `debounce:2s cap:25 drop:summarize` kabi opsiyalarni qo‘shishingiz mumkin.

## Skrinshot/chat jurnalidagi aniq savolga javob bering

**Q: "Anthropic uchun API kaliti bilan standart model qaysi?"**

**A:** OpenClaw’da credential’lar va model tanlash alohida. `ANTHROPIC_API_KEY` ni sozlash (yoki auth profillarda Anthropic API kalitini saqlash) autentifikatsiyani yoqadi, ammo haqiqiy standart model `agents.defaults.model.primary` da sozlaganingiz bo‘ladi (masalan, `anthropic/claude-sonnet-4-5` yoki `anthropic/claude-opus-4-6`). Agar `No credentials found for profile "anthropic:default"` ni ko‘rsangiz, bu Gateway ishlayotgan agent uchun kutilgan `auth-profiles.json` da Anthropic credential’larini topa olmaganini anglatadi.

---

Hali ham qotib qoldingizmi? [Discord](https://discord.com/invite/clawd) da so‘rang yoki [GitHub discussion](https://github.com/openclaw/openclaw/discussions) oching.
