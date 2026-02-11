---
summary: "Gmail Pub/Sub push wired into OpenClaw webhooks via gogcli"
read_when:
  - Wiring Gmail inbox triggers to OpenClaw
  - Setting up Pub/Sub push for agent wake
title: "Gmail PubSub"
---

# Gmail Pub/Sub -> OpenClaw

Goal: Gmail watch -> Pub/Sub push -> `gog gmail watch serve` -> OpenClaw webhook.

## Prereqs

- `gcloud` installed and logged in ([install guide](https://docs.cloud.google.com/sdk/docs/install-sdk)).
- `gog` (gogcli) installed and authorized for the Gmail account ([gogcli.sh](https://gogcli.sh/)).
- OpenClaw hooks enabled (see [Webhooks](/automation/webhook)).
- `tailscale` logged in ([tailscale.com](https://tailscale.com/)). Supported setup uses Tailscale Funnel for the public HTTPS endpoint.
  Other tunnel services can work, but are DIY/unsupported and require manual wiring.
  Hozirda biz qo‘llab-quvvatlaydigan narsa — Tailscale.

Misol hook konfiguratsiyasi (Gmail preset mapping’ni yoqish):

```json5
{
  hooks: {
    enabled: true,
    token: "OPENCLAW_HOOK_TOKEN",
    path: "/hooks",
    presets: ["gmail"],
  },
}
```

Gmail xulosasini chat yuzasiga yetkazish uchun preset’ni `deliver` va ixtiyoriy `channel`/`to` ni o‘rnatadigan mapping bilan override qiling:

```json5
{
  hooks: {
    enabled: true,
    token: "OPENCLAW_HOOK_TOKEN",
    presets: ["gmail"],
    mappings: [
      {
        match: { path: "gmail" },
        action: "agent",
        wakeMode: "now",
        name: "Gmail",
        sessionKey: "hook:gmail:{{messages[0].id}}",
        messageTemplate: "New email from {{messages[0].from}}\nSubject: {{messages[0].subject}}\n{{messages[0].snippet}}\n{{messages[0].body}}",
        model: "openai/gpt-5.2-mini",
        deliver: true,
        channel: "last",
        // to: "+15551234567"
      },
    ],
  },
}
```

Agar sobit kanal kerak bo‘lsa, `channel` + `to` ni o‘rnating. Aks holda `channel: "last"`
oxirgi yetkazib berish marshrutidan foydalanadi (WhatsApp’ga qaytadi).

Gmail ishga tushirishlari uchun arzonroq modelni majburlash uchun mapping’da `model` ni o‘rnating
(`provider/model` yoki alias). Agar `agents.defaults.models` ni majburiy qilgan bo‘lsangiz, uni o‘sha yerga kiriting.

Gmail hook’lari uchun aniq standart model va thinking darajasini sozlash uchun konfiguratsiyaga
`hooks.gmail.model` / `hooks.gmail.thinking` ni qo‘shing:

```json5
{
  hooks: {
    gmail: {
      model: "openrouter/meta-llama/llama-3.3-70b-instruct:free",
      thinking: "off",
    },
  },
}
```

Eslatmalar:

- Mapping’dagi per-hook `model`/`thinking` baribir bu standartlarni override qiladi.
- Fallback tartibi: `hooks.gmail.model` → `agents.defaults.model.fallbacks` → asosiy (auth/rate-limit/timeouts).
- Agar `agents.defaults.models` o‘rnatilgan bo‘lsa, Gmail modeli allowlist’da bo‘lishi kerak.
- Gmail hook kontenti odatda tashqi-kontent xavfsizlik chegaralari bilan o‘raladi.
  O‘chirish uchun (xavfli), `hooks.gmail.allowUnsafeExternalContent: true` ni o‘rnating.

Payload ishlov berishni yanada moslashtirish uchun `hooks.mappings` yoki JS/TS transform modulini
`hooks.transformsDir` ostiga qo‘shing ([Webhooks](/automation/webhook) ga qarang).

## Wizard (tavsiya etiladi)

Hammasini birga ulash uchun OpenClaw helper’dan foydalaning (macOS’da brew orqali bog‘liqliklarni o‘rnatadi):

```bash
openclaw webhooks gmail setup \
  --account openclaw@gmail.com
```

Standartlar:

- Ommaviy push endpoint uchun Tailscale Funnel’dan foydalanadi.
- `openclaw webhooks gmail run` uchun `hooks.gmail` konfiguratsiyasini yozadi.
- Gmail hook preset’ini yoqadi (`hooks.presets: ["gmail"]`).

Yo‘l eslatmasi: `tailscale.mode` yoqilganida, OpenClaw avtomatik ravishda
`hooks.gmail.serve.path` ni `/` ga o‘rnatadi va ommaviy yo‘lni
`hooks.gmail.tailscale.path` (standart `/gmail-pubsub`) da saqlaydi, chunki Tailscale
proxy qilishdan oldin set-path prefiksini olib tashlaydi.
Agar backend prefiksli yo‘lni qabul qilishi kerak bo‘lsa,
`hooks.gmail.tailscale.target` (yoki `--tailscale-target`) ni
`http://127.0.0.1:8788/gmail-pubsub` kabi to‘liq URL’ga o‘rnating va `hooks.gmail.serve.path` bilan moslang.

Maxsus endpoint xohlaysizmi? `--push-endpoint <url>` dan foydalaning yoki `--tailscale off` qiling.

Platforma eslatmasi: macOS’da wizard `gcloud`, `gogcli` va `tailscale` ni
Homebrew orqali o‘rnatadi; Linux’da esa avval ularni qo‘lda o‘rnating.

Gateway’ni avtomatik ishga tushirish (tavsiya etiladi):

- `hooks.enabled=true` va `hooks.gmail.account` o‘rnatilganda, Gateway yuklanishda
  `gog gmail watch serve` ni ishga tushiradi va watch’ni avtomatik yangilaydi.
- Chiqib ketish uchun `OPENCLAW_SKIP_GMAIL_WATCHER=1` ni o‘rnating (daemon’ni o‘zingiz ishga tushirsangiz foydali).
- Qo‘lda ishga tushirilgan daemon’ni bir vaqtda ishlatmang, aks holda
  `listen tcp 127.0.0.1:8788: bind: address already in use` xatosiga duch kelasiz.

Qo‘lda daemon ( `gog gmail watch serve` + auto-renew’ni ishga tushiradi):

```bash
openclaw webhooks gmail run
```

## Bir martalik sozlash

1. `gog` ishlatadigan **OAuth client’ga egalik qiluvchi** GCP loyihasini tanlang.

```bash
gcloud auth login
gcloud config set project <project-id>
```

Eslatma: Gmail watch Pub/Sub mavzusi OAuth client bilan bir xil loyihada bo‘lishini talab qiladi.

2. API’larni yoqing:

```bash
gcloud services enable gmail.googleapis.com pubsub.googleapis.com
```

3. Mavzu yarating:

```bash
gcloud pubsub topics create gog-gmail-watch
```

4. Gmail push’ga nashr etishga ruxsat bering:

```bash
gcloud pubsub topics add-iam-policy-binding gog-gmail-watch \
  --member=serviceAccount:gmail-api-push@system.gserviceaccount.com \
  --role=roles/pubsub.publisher
```

## Watch’ni boshlang

```bash
gog gmail watch start \
  --account openclaw@gmail.com \
  --label INBOX \
  --topic projects/<project-id>/topics/gog-gmail-watch
```

Chiqarishdagi `history_id` ni saqlab qo‘ying (debug uchun).

## Push handler’ni ishga tushiring

1. Mahalliy misol (umumiy token autentifikatsiyasi):

```bash
2. gog gmail watch serve \
```

\--account openclaw@gmail.com \

- \--bind 127.0.0.1 \
- \--port 8788 \
- \--path /gmail-pubsub \

\--token <shared> \

## --hook-url http://127.0.0.1:18789/hooks/gmail \

\--hook-token OPENCLAW_HOOK_TOKEN \

```bash
  --include-body \
```

\--max-bytes 20000

```bash
3. Eslatmalar:
```

4. `--token` push endpointini himoya qiladi (`x-gog-token` yoki `?token=`).

```bash
5. `--hook-url` OpenClaw `/hooks/gmail` ga ishora qiladi (moslangan; izolyatsiyalangan ishga tushirish + asosiyga xulosa).
```

## 6. `--include-body` va `--max-bytes` OpenClaw’ga yuboriladigan body parchalarini boshqaradi.

7. Tavsiya etiladi: `openclaw webhooks gmail run` xuddi shu oqimni o‘rab beradi va watch’ni avtomatik yangilaydi.

```bash
8. Handler’ni ochiq qilish (ilg‘or, qo‘llab-quvvatlanmaydi)
```

9. Agar sizga Tailscale bo‘lmagan tunnel kerak bo‘lsa, uni qo‘lda ulang va push obunasida umumiy URL’dan foydalaning (qo‘llab-quvvatlanmaydi, himoya mexanizmlarisiz):

```bash
10. cloudflared tunnel --url http://127.0.0.1:8788 --no-autoupdate
```

## 11. Yaratilgan URL’ni push endpoint sifatida foydalaning:

- 12. gcloud pubsub subscriptions create gog-gmail-watch-push \
- \--topic gog-gmail-watch \
- \--push-endpoint "https://<public-url>/gmail-pubsub?token=<shared>"

## 13. Prodakshen: barqaror HTTPS endpointdan foydalaning va Pub/Sub OIDC JWT’ni sozlang, so‘ng ishga tushiring:

```bash
14. gog gmail watch serve --verify-oidc --oidc-email <svc@...>
```
