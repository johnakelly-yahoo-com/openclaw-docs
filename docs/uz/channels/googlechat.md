---
summary: "Google Chat app support status, capabilities, and configuration"
read_when:
  - Working on Google Chat channel features
title: "Google Chat"
---

# Google Chat (Chat API)

Status: ready for DMs + spaces via Google Chat API webhooks (HTTP only).

## Quick setup (beginner)

1. Create a Google Cloud project and enable the **Google Chat API**.
   - Go to: [Google Chat API Credentials](https://console.cloud.google.com/apis/api/chat.googleapis.com/credentials)
   - Enable the API if it is not already enabled.
2. Create a **Service Account**:
   - Press **Create Credentials** > **Service Account**.
   - Name it whatever you want (e.g., `openclaw-chat`).
   - Leave permissions blank (press **Continue**).
   - Leave principals with access blank (press **Done**).
3. Create and download the **JSON Key**:
   - In the list of service accounts, click on the one you just created.
   - Go to the **Keys** tab.
   - Click **Add Key** > **Create new key**.
   - Select **JSON** and press **Create**.
4. Store the downloaded JSON file on your gateway host (e.g., `~/.openclaw/googlechat-service-account.json`).
5. Create a Google Chat app in the [Google Cloud Console Chat Configuration](https://console.cloud.google.com/apis/api/chat.googleapis.com/hangouts-chat):
   - Fill in the **Application info**:
     - **App name**: (e.g. `OpenClaw`)
     - **Avatar URL**: (e.g. `https://openclaw.ai/logo.png`)
     - **Description**: (e.g. `Personal AI Assistant`)
   - Enable **Interactive features**.
   - Under **Functionality**, check **Join spaces and group conversations**.
   - Under **Connection settings**, select **HTTP endpoint URL**.
   - Under **Triggers**, select **Use a common HTTP endpoint URL for all triggers** and set it to your gateway's public URL followed by `/googlechat`.
     - _Tip: Run `openclaw status` to find your gateway's public URL._
   - Under **Visibility**, check **Make this Chat app available to specific people and groups in &lt;Your Domain&gt;**.
   - Enter your email address (e.g. `user@example.com`) in the text box.
   - Click **Save** at the bottom.
6. **Enable the app status**:
   - After saving, **refresh the page**.
   - Look for the **App status** section (usually near the top or bottom after saving).
   - Change the status to **Live - available to users**.
   - Click **Save** again.
7. Configure OpenClaw with the service account path + webhook audience:
   - Env: `GOOGLE_CHAT_SERVICE_ACCOUNT_FILE=/path/to/service-account.json`
   - Or config: `channels.googlechat.serviceAccountFile: "/path/to/service-account.json"`.
8. Set the webhook audience type + value (matches your Chat app config).
9. Start the gateway. Google Chat will POST to your webhook path.

## Add to Google Chat

Once the gateway is running and your email is added to the visibility list:

1. 1. [Google Chat](https://chat.google.com/) ga o‘ting.
2. 2. **Direct Messages** yonidagi **+** (plus) belgisini bosing.
3. 3. Qidiruv satrida (odatda odam qo‘shadigan joy), Google Cloud Console’da sozlagan **Ilova nomi**ni kiriting.
   - 4. **Eslatma**: Bot "Marketplace" ko‘rish ro‘yxatida _ko‘rinmaydi_, chunki u xususiy ilova. 5. Uni nomi bo‘yicha qidirishingiz kerak.
4. 6. Natijalardan botingizni tanlang.
5. 7. 1:1 suhbatni boshlash uchun **Add** yoki **Chat** tugmasini bosing.
6. 8. Yordamchini ishga tushirish uchun "Hello" yuboring!

## 9) Ommaviy URL (faqat Webhook)

10. Google Chat webhook’lari ommaviy HTTPS endpoint’ni talab qiladi. 11. Xavfsizlik uchun, **faqat `/googlechat` yo‘lini internetga oching**. 12. OpenClaw boshqaruv paneli va boshqa maxfiy endpoint’larni xususiy tarmog‘ingizda saqlang.

### 13. Variant A: Tailscale Funnel (Tavsiya etiladi)

14. Xususiy boshqaruv paneli uchun Tailscale Serve’dan, ommaviy webhook yo‘li uchun esa Funnel’dan foydalaning. 15. Bu `/` yo‘lini xususiy holda qoldirib, faqat `/googlechat` ni ochadi.

1. 16. **Gateway qaysi manzilga bog‘langanini tekshiring:**

   ```bash
   ss -tlnp | grep 18789
   ```

   18. IP manzilni qayd eting (masalan, `127.0.0.1`, `0.0.0.0` yoki `100.x.x.x` kabi Tailscale IP).

2. 19. **Boshqaruv panelini faqat tailnet ichida oching (8443-port):**

   ```bash
   # If bound to localhost (127.0.0.1 or 0.0.0.0):
   tailscale serve --bg --https 8443 http://127.0.0.1:18789

   # If bound to Tailscale IP only (e.g., 100.106.161.80):
   tailscale serve --bg --https 8443 http://100.106.161.80:18789
   ```

3. 21. **Faqat webhook yo‘lini ommaviy qilib oching:**

   ```bash
   # If bound to localhost (127.0.0.1 or 0.0.0.0):
   tailscale funnel --bg --set-path /googlechat http://127.0.0.1:18789/googlechat

   # If bound to Tailscale IP only (e.g., 100.106.161.80):
   tailscale funnel --bg --set-path /googlechat http://100.106.161.80:18789/googlechat
   ```

4. 23. **Funnel uchun tugunni avtorizatsiya qiling:**
       Agar so‘ralsa, chiqishda ko‘rsatilgan avtorizatsiya URL’iga o‘ting va tailnet siyosatingizda ushbu tugun uchun Funnel’ni yoqing.

5. 24. **Sozlamani tekshiring:**

   ```bash
   tailscale serve status
   tailscale funnel status
   ```

26) Ommaviy webhook URL’ingiz quyidagicha bo‘ladi:
    `https://<node-name>.<tailnet>`27. `.ts.net/googlechat`

28. Xususiy boshqaruv paneli faqat tailnet ichida qoladi:
    `https://<node-name>.<tailnet>`29. `.ts.net:8443/`

30. Google Chat ilovasi sozlamasida ( `:8443` siz) ommaviy URL’dan foydalaning.

> 31. Eslatma: Ushbu sozlama qayta yuklashlardan keyin ham saqlanib qoladi. 32. Keyinroq olib tashlash uchun `tailscale funnel reset` va `tailscale serve reset` buyruqlarini bajaring.

### 33. Variant B: Reverse Proxy (Caddy)

34. Agar Caddy kabi reverse proxy’dan foydalansangiz, faqat aniq yo‘lni proxy qiling:

```caddy
your-domain.com {
    reverse_proxy /googlechat* localhost:18789
}
```

36. Ushbu sozlama bilan `your-domain.com/` ga kelgan har qanday so‘rov e’tiborsiz qoldiriladi yoki 404 qaytariladi, `your-domain.com/googlechat` esa OpenClaw’ga xavfsiz yo‘naltiriladi.

### 37. Variant C: Cloudflare Tunnel

38. Tunnel’ingizning ingress qoidalarini faqat webhook yo‘lini marshrutlash uchun sozlang:

- 39. **Yo‘l**: `/googlechat` -> `http://localhost:18789/googlechat`
- 40. **Standart qoida**: HTTP 404 (Topilmadi)

## 41. Qanday ishlaydi

1. 42. Google Chat gateway’ga webhook POST’larini yuboradi. 43. Har bir so‘rov `Authorization: Bearer <token>` sarlavhasini o‘z ichiga oladi.
2. 44. OpenClaw tokenni sozlangan `audienceType` + `audience` ga qarshi tekshiradi:
   - 45. `audienceType: "app-url"` → audience bu sizning HTTPS webhook URL’ingiz.
   - 46. `audienceType: "project-number"` → audience bu Cloud loyiha raqami.
3. 47. Xabarlar space bo‘yicha yo‘naltiriladi:
   - 48. DM’lar `agent:<agentId>:googlechat:dm:<spaceId>` sessiya kalitidan foydalanadi.
   - 49. Space’lar `agent:<agentId>:googlechat:group:<spaceId>` sessiya kalitidan foydalanadi.
4. 50. DM’ga kirish sukut bo‘yicha pairing orqali amalga oshiriladi. Noma’lum jo‘natuvchilar juftlash kodi oladi; quyidagicha tasdiqlang:
   - `openclaw pairing approve googlechat <code>`
5. Guruh bo‘shliqlari sukut bo‘yicha @-eslatmani talab qiladi. Agar eslatmani aniqlash uchun ilovaning foydalanuvchi nomi kerak bo‘lsa, `botUser` dan foydalaning.

## Manzillar

Yetkazib berish va ruxsat ro‘yxatlari uchun ushbu identifikatorlardan foydalaning:

- To‘g‘ridan-to‘g‘ri xabarlar: `users/<userId>` yoki `users/<email>` (email manzillar qabul qilinadi).
- Bo‘shliqlar: `spaces/<spaceId>`.

## Konfiguratsiya asosiy jihatlari

```json5
{
  channels: {
    googlechat: {
      enabled: true,
      serviceAccountFile: "/path/to/service-account.json",
      audienceType: "app-url",
      audience: "https://gateway.example.com/googlechat",
      webhookPath: "/googlechat",
      botUser: "users/1234567890", // optional; helps mention detection
      dm: {
        policy: "pairing",
        allowFrom: ["users/1234567890", "name@example.com"],
      },
      groupPolicy: "allowlist",
      groups: {
        "spaces/AAAA": {
          allow: true,
          requireMention: true,
          users: ["users/1234567890"],
          systemPrompt: "Short answers only.",
        },
      },
      actions: { reactions: true },
      typingIndicator: "message",
      mediaMaxMb: 20,
    },
  },
}
```

Eslatmalar:

- Xizmat akkaunti hisob ma’lumotlarini `serviceAccount` orqali (JSON satri sifatida) ham ichma-ich uzatish mumkin.
- `webhookPath` o‘rnatilmagan bo‘lsa, sukut bo‘yicha webhook yo‘li `/googlechat`.
- `actions.reactions` yoqilganida, reaksiyalar `reactions` vositasi va `channels action` orqali mavjud bo‘ladi.
- `typingIndicator` `none`, `message` (sukut bo‘yicha) va `reaction` ni qo‘llab-quvvatlaydi (`reaction` foydalanuvchi OAuth’ni talab qiladi).
- Biriktirmalar Chat API orqali yuklab olinadi va media quvurida saqlanadi (hajmi `mediaMaxMb` bilan cheklanadi).

## Nosozliklarni bartaraf etish

### 405 Method Not Allowed

Agar Google Cloud Logs Explorer quyidagiga o‘xshash xatolarni ko‘rsatsa:

```
status code: 405, reason phrase: HTTP error response: HTTP/1.1 405 Method Not Allowed
```

Bu webhook ishlovchisi ro‘yxatdan o‘tkazilmaganini anglatadi. Keng tarqalgan sabablar:

1. **Kanal sozlanmagan**: konfiguratsiyangizda `channels.googlechat` bo‘limi yo‘q. Quyidagicha tekshiring:

   ```bash
   openclaw config get channels.googlechat
   ```

   Agar u "Config path not found" qaytarsa, konfiguratsiyani qo‘shing (qarang [Config highlights](#config-highlights)).

2. **Plagin yoqilmagan**: plagin holatini tekshiring:

   ```bash
   openclaw plugins list | grep googlechat
   ```

   Agar "disabled" ko‘rsatilsa, konfiguratsiyangizga `plugins.entries.googlechat.enabled: true` qo‘shing.

3. **Gateway qayta ishga tushirilmagan**: konfiguratsiyani qo‘shgandan so‘ng, gateway’ni qayta ishga tushiring:

   ```bash
   openclaw gateway restart
   ```

Kanal ishga tushganini tekshiring:

```bash
openclaw channels status
# Ko‘rsatishi kerak: Google Chat default: enabled, configured, ...
```

### Boshqa muammolar

- Avtorizatsiya xatolari yoki audience konfiguratsiyasi yetishmasligini tekshirish uchun `openclaw channels status --probe` dan foydalaning.
- Agar xabarlar kelmasa, Chat ilovasining webhook URL’i va hodisa obunalarini tasdiqlang.
- Agar eslatma cheklovi javoblarni bloklasa, `botUser` ni ilovaning foydalanuvchi resurs nomiga o‘rnating va `requireMention` ni tekshiring.
- Sinov xabarini yuborayotganda so‘rovlar gateway’ga yetib kelayotganini ko‘rish uchun `openclaw logs --follow` dan foydalaning.

Tegishli hujjatlar:

- [Gateway configuration](/gateway/configuration)
- [Security](/gateway/security)
- [Reactions](/tools/reactions)
