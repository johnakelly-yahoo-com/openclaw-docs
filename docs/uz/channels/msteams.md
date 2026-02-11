---
summary: "33. Microsoft Teams botini qo‘llab-quvvatlash holati, imkoniyatlari va konfiguratsiyasi"
read_when:
  - 34. MS Teams kanal funksiyalari ustida ish olib borilmoqda
title: "35. Microsoft Teams"
---

# 36. Microsoft Teams (plagin)

> 37. "Bu yerga kirgan barcha umidlaringni tashla."

Updated: 2026-01-21

39. Holat: matn + DM biriktirmalari qo‘llab-quvvatlanadi; kanal/guruhga fayl yuborish uchun `sharePointSiteId` va Graph ruxsatlari talab etiladi (qarang: [Sending files in group chats](#sending-files-in-group-chats)). 40. So‘rovnomalar Adaptive Cards orqali yuboriladi.

## 41. Plagin talab qilinadi

42. Microsoft Teams plagin sifatida yetkaziladi va asosiy o‘rnatmaga kiritilmagan.

**Breaking change (2026.1.15):** MS Teams moved out of core. 44. Agar undan foydalansangiz, plaginni o‘rnatishingiz kerak.

45. Tushuntirish: bu yadro o‘rnatmalarini yengillashtiradi va MS Teams bog‘liqliklarini mustaqil yangilashga imkon beradi.

46. CLI orqali o‘rnatish (npm registri):

```bash
47. openclaw plugins install @openclaw/msteams
```

48. Mahalliy checkout (git repozitoriydan ishga tushirilganda):

```bash
49. openclaw plugins install ./extensions/msteams
```

50. Agar sozlash/onboarding vaqtida Teams’ni tanlasangiz va git checkout aniqlansa,
    OpenClaw mahalliy o‘rnatish yo‘lini avtomatik taklif qiladi.

Details: [Plugins](/tools/plugin)

## Quick setup (beginner)

1. 3. Microsoft Teams plaginini o‘rnating.
2. Create an **Azure Bot** (App ID + client secret + tenant ID).
3. 5. OpenClaw’ni ushbu hisob ma’lumotlari bilan sozlang.
4. 6. `/api/messages` (standart bo‘yicha 3978-port) ni ommaviy URL yoki tunnel orqali oching.
5. 7. Teams ilova paketini o‘rnating va gateway’ni ishga tushiring.

8) Minimal sozlama:

```json5
9. {
  channels: {
    msteams: {
      enabled: true,
      appId: "<APP_ID>",
      appPassword: "<APP_PASSWORD>",
      tenantId: "<TENANT_ID>",
      webhook: { port: 3978, path: "/api/messages" },
    },
  },
}
```

10. Eslatma: guruh chatlari standart bo‘yicha bloklangan (`channels.msteams.groupPolicy: "allowlist"`). 11. Guruh javoblariga ruxsat berish uchun `channels.msteams.groupAllowFrom` ni sozlang (yoki `groupPolicy: "open"` dan foydalaning — istalgan a’zo, mention orqali).

## 12. Maqsadlar

- 13. Teams DM’lari, guruh chatlari yoki kanallar orqali OpenClaw bilan muloqot qilish.
- 14. Marshrutlashni deterministik saqlash: javoblar har doim kelgan kanaliga qaytadi.
- Default to safe channel behavior (mentions required unless configured otherwise).

## 16. Konfiguratsiya yozuvlari

17. Standart bo‘yicha Microsoft Teams `/config set|unset` orqali ishga tushirilgan konfiguratsiya yangilanishlarini yozishga ruxsat etiladi (`commands.config: true` talab etiladi).

18. O‘chirish:

```json5
19. {
  channels: { msteams: { configWrites: false } },
}
```

## 20. Kirish nazorati (DM’lar + guruhlar)

21. **DM kirish**

- 22. Standart: `channels.msteams.dmPolicy = "pairing"`. 23. Noma’lum jo‘natuvchilar tasdiqlanmaguncha e’tiborsiz qoldiriladi.
- 24. `channels.msteams.allowFrom` AAD obyekt ID’lari, UPN’lar yoki ko‘rinadigan nomlarni qabul qiladi. 25. Usta (wizard) ruxsatlar mavjud bo‘lsa, Microsoft Graph orqali nomlarni ID’larga moslaydi.

**Group access**

- 27. Standart: `channels.msteams.groupPolicy = "allowlist"` (`groupAllowFrom` qo‘shilmaguncha bloklangan). 28. Sozlanmagan holatda standartni bekor qilish uchun `channels.defaults.groupPolicy` dan foydalaning.
- 29. `channels.msteams.groupAllowFrom` guruh chatlari/kanallarida qaysi jo‘natuvchilar ishga tushira olishini boshqaradi (`channels.msteams.allowFrom` ga qaytadi).
- Set `groupPolicy: "open"` to allow any member (still mention‑gated by default).
- 31. **Hech qanday kanalga** ruxsat bermaslik uchun `channels.msteams.groupPolicy: "disabled"` ni o‘rnating.

32. Misol:

```json5
33. {
  channels: {
    msteams: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["user@org.com"],
    },
  },
}
```

34. **Teams + kanal allowlist**

- 35. `channels.msteams.teams` ostida jamoalar va kanallarni sanab, guruh/kanal javoblarini cheklang.
- 36. Kalitlar jamoa ID’lari yoki nomlari bo‘lishi mumkin; kanal kalitlari esa suhbat ID’lari yoki nomlari bo‘lishi mumkin.
- 37. `groupPolicy="allowlist"` va jamoalar allowlist’i mavjud bo‘lsa, faqat ko‘rsatilgan jamoalar/kanallar qabul qilinadi (mention talab qilinadi).
- 38. Sozlash ustasi `Team/Channel` yozuvlarini qabul qiladi va ularni siz uchun saqlaydi.
- 39. Ishga tushishda OpenClaw jamoa/kanal va foydalanuvchi allowlist nomlarini ID’larga moslaydi (Graph ruxsatlari mavjud bo‘lsa)
      va moslikni jurnalga yozadi; moslanmagan yozuvlar kiritilgandek saqlanadi.

40. Misol:

```json5
41. {
  channels: {
    msteams: {
      groupPolicy: "allowlist",
      teams: {
        "My Team": {
          channels: {
            General: { requireMention: true },
          },
        },
      },
    },
  },
}
```

## 42. Qanday ishlaydi

1. 43. Microsoft Teams plaginini o‘rnating.
2. 44. **Azure Bot** yarating (App ID + secret + tenant ID).
3. 45. Botga ishora qiladigan va quyidagi RSC ruxsatlarini o‘z ichiga olgan **Teams ilova paketi** ni yarating.
4. 46. Teams ilovasini jamoaga yuklab/o‘rnating (yoki DM’lar uchun shaxsiy doira).
5. 47. `~/.openclaw/openclaw.json` da (yoki muhit o‘zgaruvchilari orqali) `msteams` ni sozlang va gateway’ni ishga tushiring.
6. 48. Gateway standart bo‘yicha `/api/messages` da Bot Framework webhook trafikini tinglaydi.

## 49) Azure Bot sozlamasi (Talablar)

50. OpenClaw’ni sozlashdan oldin Azure Bot resursini yaratishingiz kerak.

### 1. 1-qadam: Azure Bot yaratish

1. 2. [Create Azure Bot](https://portal.azure.com/#create/Microsoft.AzureBot) sahifasiga o‘ting
2. 3. **Basics** (Asosiy) yorlig‘ini to‘ldiring:

   | 4. Maydon              | 5. Qiymat                                                                              |
   | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
   | 6. **Bot handle**      | 7. Bot nomingiz, masalan, `openclaw-msteams` (noyob bo‘lishi kerak) |
   | 8. **Subscription**    | 9. Azure obunangizni tanlang                                                           |
   | 10. **Resource group** | 11. Yangisini yarating yoki mavjudidan foydalaning                                     |
   | 12. **Pricing tier**   | 13. Dasturlash/sinov uchun **Free**                                                    |
   | 14. **Type of App**    | 15. **Single Tenant** (tavsiya etiladi — quyidagi eslatmaga qarang) |
   | 16. **Creation type**  | 17. **Create new Microsoft App ID**                                                    |

> 18) **Bekor qilish haqida xabarnoma:** Yangi multi-tenant botlarni yaratish 2025-07-31 dan keyin bekor qilingan. 19. Yangi botlar uchun **Single Tenant** dan foydalaning.

3. 20. **Review + create** → **Create** tugmasini bosing (taxminan 1–2 daqiqa kuting)

### 21) 2-qadam: Hisob ma’lumotlarini olish

1. 22. Azure Bot resursingizga o‘ting → **Configuration**
2. 23. **Microsoft App ID** ni nusxalang → bu sizning `appId`
3. 24. **Manage Password** ni bosing → App Registration sahifasiga o‘ting
4. Under **Certificates & secrets** → **New client secret** → copy the **Value** → this is your `appPassword`
5. 26. **Overview** bo‘limiga o‘ting → **Directory (tenant) ID** ni nusxalang → bu sizning `tenantId`

### 27) 3-qadam: Xabar almashish endpointini sozlash

1. 28. Azure Bot → **Configuration**
2. 29. **Messaging endpoint** ni webhook URL’ingizga o‘rnating:
   - 30. Production: `https://your-domain.com/api/messages`
   - 31. Local dev: Tunnel’dan foydalaning (quyida [Local Development](#local-development-tunneling) bo‘limiga qarang)

### 32) 4-qadam: Teams kanalini yoqish

1. 33. Azure Bot → **Channels**
2. 34. **Microsoft Teams** ni bosing → Configure → Save
3. 35. Xizmat ko‘rsatish shartlarini qabul qiling

## 36) Local Development (Tunneling)

37. Teams `localhost` ga ulana olmaydi. 38. Lokal dasturlash uchun tunnel’dan foydalaning:

39. **Option A: ngrok**

```bash
40. ngrok http 3978
```

# https URL’ni nusxalang, masalan, https://abc123.ngrok.io

```bash
# Xabar almashish endpointini quyidagiga o‘rnating: https://abc123.ngrok.io/api/messages
```

## 41. **Option B: Tailscale Funnel**

42. tailscale funnel 3978

1. # Messaging endpoint sifatida Tailscale funnel URL’ingizdan foydalaning
2. 43. Teams Developer Portal (Muqobil usul)
3. 44. Manifest ZIP faylini qo‘lda yaratish o‘rniga, [Teams Developer Portal](https://dev.teams.microsoft.com/apps) dan foydalanishingiz mumkin:
4. 45. **+ New app** ni bosing
5. 46. Asosiy ma’lumotlarni to‘ldiring (nomi, tavsifi, ishlab chiquvchi ma’lumotlari)
6. 47. **App features** → **Bot** bo‘limiga o‘ting
7. 1. Teams ichida: **Apps** → **Manage your apps** → **Upload a custom app** → ZIP faylni tanlang

2) Bu ko‘pincha JSON manifestlarini qo‘lda tahrirlashdan osonroq.

## 3. Botni sinovdan o‘tkazish

4. **Variant A: Azure Web Chat (avval webhook’ni tekshiring)**

1. In Azure Portal → your Azure Bot resource → **Test in Web Chat**
2. 6. Xabar yuboring — javobni ko‘rishingiz kerak
3. 7. Bu Teams sozlamasidan oldin webhook endpoint’ingiz ishlayotganini tasdiqlaydi

8) **Variant B: Teams (ilova o‘rnatilgandan keyin)**

1. 9. Teams ilovasini o‘rnating (sideload yoki tashkilot katalogi orqali)
2. 10. Teams’da botni toping va DM yuboring
3. 11. Kiruvchi faoliyat uchun gateway loglarini tekshiring

## Setup (minimal text-only)

1. 13. **Microsoft Teams plaginini o‘rnating**
   - 14. npm’dan: `openclaw plugins install @openclaw/msteams`
   - 15. Lokal checkout’dan: `openclaw plugins install ./extensions/msteams`

2. **Bot registration**
   - 17. Azure Bot yarating (yuqoriga qarang) va quyidagilarni qayd eting:
     - 18. App ID
     - 19. Client secret (App parol)
     - Tenant ID (single-tenant)

3. 21. **Teams ilova manifesti**
   - 22. `botId = <App ID>` bo‘lgan `bot` yozuvini kiriting.
   - 23. Scope’lar: `personal`, `team`, `groupChat`.
   - 24. `supportsFiles: true` (personal scope’da fayllar bilan ishlash uchun talab qilinadi).
   - 25. RSC ruxsatlarini qo‘shing (quyida).
   - 26. Ikonkalar yarating: `outline.png` (32x32) va `color.png` (192x192).
   - 27. Uchala faylni birga zip qiling: `manifest.json`, `outline.png`, `color.png`.

4. 28. **OpenClaw’ni sozlash**

   ```json
   29. {
     "msteams": {
       "enabled": true,
       "appId": "<APP_ID>",
       "appPassword": "<APP_PASSWORD>",
       "tenantId": "<TENANT_ID>",
       "webhook": { "port": 3978, "path": "/api/messages" }
     }
   }
   ```

   30. Config kalitlari o‘rniga muhit o‘zgaruvchilaridan ham foydalanishingiz mumkin:

   - 31. `MSTEAMS_APP_ID`
   - 32. `MSTEAMS_APP_PASSWORD`
   - 33. `MSTEAMS_TENANT_ID`

5. 34. **Bot endpoint’i**
   - 35. Azure Bot Messaging Endpoint’ini quyidagiga o‘rnating:
     - 36. `https://<host>:3978/api/messages` (yoki tanlangan path/port).

6. 37. **Gateway’ni ishga tushirish**
   - 38. Plagin o‘rnatilganda va `msteams` konfiguratsiyasi credential’lar bilan mavjud bo‘lsa, Teams kanali avtomatik ishga tushadi.

## 39) Tarix konteksti

- 40. `channels.msteams.historyLimit` so‘nggi nechta kanal/guruh xabarlari prompt’ga o‘ralishini boshqaradi.
- 41. `messages.groupChat.historyLimit` ga fallback qiladi. 42. O‘chirish uchun `0` ga o‘rnating (standart 50).
- 43. DM tarixi `channels.msteams.dmHistoryLimit` bilan cheklanishi mumkin (foydalanuvchi aylanishlari). Per-user overrides: `channels.msteams.dms["<user_id>"].historyLimit`.

## 45. Joriy Teams RSC ruxsatlari (Manifest)

46. Bular Teams ilova manifestimizdagi **mavjud resourceSpecific ruxsatlar**. 47. Ular faqat ilova o‘rnatilgan team/chat ichida amal qiladi.

48. **Kanallar uchun (team scope):**

- 49. `ChannelMessage.Read.Group` (Application) — @mention bo‘lmasdan barcha kanal xabarlarini qabul qilish
- 50. `ChannelMessage.Send.Group` (Application)
- `Member.Read.Group` (Application)
- `Owner.Read.Group` (Application)
- `ChannelSettings.Read.Group` (Application)
- `TeamMember.Read.Group` (Application)
- `TeamSettings.Read.Group` (Application)

**For group chats:**

- `ChatMessage.Read.Chat` (Application) - receive all group chat messages without @mention

## Teams manifestiga misol (tahrirlangan)

Kerakli maydonlarni o‘z ichiga olgan minimal, yaroqli misol. ID va URL’larni almashtiring.

```json
{
  "$schema": "https://developer.microsoft.com/en-us/json-schemas/teams/v1.23/MicrosoftTeams.schema.json",
  "manifestVersion": "1.23",
  "version": "1.0.0",
  "id": "00000000-0000-0000-0000-000000000000",
  "name": { "short": "OpenClaw" },
  "developer": {
    "name": "Your Org",
    "websiteUrl": "https://example.com",
    "privacyUrl": "https://example.com/privacy",
    "termsOfUseUrl": "https://example.com/terms"
  },
  "description": { "short": "OpenClaw in Teams", "full": "OpenClaw in Teams" },
  "icons": { "outline": "outline.png", "color": "color.png" },
  "accentColor": "#5B6DEF",
  "bots": [
    {
      "botId": "11111111-1111-1111-1111-111111111111",
      "scopes": ["personal", "team", "groupChat"],
      "isNotificationOnly": false,
      "supportsCalling": false,
      "supportsVideo": false,
      "supportsFiles": true
    }
  ],
  "webApplicationInfo": {
    "id": "11111111-1111-1111-1111-111111111111"
  },
  "authorization": {
    "permissions": {
      "resourceSpecific": [
        { "name": "ChannelMessage.Read.Group", "type": "Application" },
        { "name": "ChannelMessage.Send.Group", "type": "Application" },
        { "name": "Member.Read.Group", "type": "Application" },
        { "name": "Owner.Read.Group", "type": "Application" },
        { "name": "ChannelSettings.Read.Group", "type": "Application" },
        { "name": "TeamMember.Read.Group", "type": "Application" },
        { "name": "TeamSettings.Read.Group", "type": "Application" },
        { "name": "ChatMessage.Read.Chat", "type": "Application" }
      ]
    }
  }
}
```

### Manifest caveats (must-have fields)

- `bots[].botId` **albatta** Azure Bot App ID bilan mos bo‘lishi kerak.
- `webApplicationInfo.id` **albatta** Azure Bot App ID bilan mos bo‘lishi kerak.
- `bots[].scopes` siz foydalanishni rejalashtirgan yuzalarni o‘z ichiga olishi kerak (`personal`, `team`, `groupChat`).
- `bots[].supportsFiles: true` is required for file handling in personal scope.
- `authorization.permissions.resourceSpecific` must include channel read/send if you want channel traffic.

### Updating an existing app

Allaqachon o‘rnatilgan Teams ilovasini yangilash uchun (masalan, RSC ruxsatlarini qo‘shish):

1. Yangi sozlamalar bilan `manifest.json` faylini yangilang
2. **`version` maydonini oshiring** (masalan, `1.0.0` → `1.1.0`)
3. **Re-zip** the manifest with icons (`manifest.json`, `outline.png`, `color.png`)
4. Yangi zip faylni yuklang:
   - **Variant A (Teams Admin Center):** Teams Admin Center → Teams apps → Manage apps → ilovangizni toping → Upload new version
   - **Variant B (Sideload):** Teams ichida → Apps → Manage your apps → Upload a custom app
5. **Jamoa kanallari uchun:** yangi ruxsatlar kuchga kirishi uchun har bir jamoada ilovani qayta o‘rnating
6. Keshlangan ilova metama’lumotlarini tozalash uchun **Teams’dan to‘liq chiqing va qayta ishga tushiring** (faqat oynani yopish yetarli emas)

## Imkoniyatlar: faqat RSC vs Graph

### **Faqat Teams RSC bilan** (ilova o‘rnatilgan, Graph API ruxsatlarisiz)

Ishlaydi:

- Kanal xabarlarining **matn** tarkibini o‘qish.
- Kanal xabarlarining **matn** tarkibini yuborish.
- **Shaxsiy (DM)** fayl biriktirmalarini qabul qilish.

Ishlamaydi:

- Kanal/guruh **rasm yoki fayl tarkibi** (payload faqat HTML stubni o‘z ichiga oladi).
- SharePoint/OneDrive’da saqlangan biriktirmalarni yuklab olish.
- Xabarlar tarixini o‘qish (jonli webhook hodisasidan tashqari).

### **Teams RSC + Microsoft Graph Application ruxsatlari bilan**

Qo‘shadi:

- Joylashtirilgan kontentni yuklab olish (xabarlarga joylangan rasmlar).
- SharePoint/OneDrive’da saqlangan fayl biriktirmalarini yuklab olish.
- Graph orqali kanal/chat xabarlar tarixini o‘qish.

### RSC va Graph API taqqoslanishi

| Imkoniyat                    | RSC ruxsatlari                                            | Graph API                                           |
| ---------------------------- | --------------------------------------------------------- | --------------------------------------------------- |
| **Real vaqt xabarlari**      | Ha (webhook orqali)                    | Yo‘q (faqat polling)             |
| **Tarixiy xabarlar**         | Yo‘q                                                      | Ha (tarixni so‘rashi mumkin)     |
| **O‘rnatish murakkabligi**   | Faqat ilova manifesti                                     | Administrator roziligi + token oqimi talab qilinadi |
| **Offline rejimda ishlaydi** | Yo‘q (doim ishlayotgan bo‘lishi kerak) | Yes (query anytime)              |

**Xulosa:** RSC real vaqtli tinglash uchun; Graph API esa tarixiy ma’lumotlarga kirish uchun. Offline bo‘lgan paytda o‘tkazib yuborilgan xabarlarni olish uchun sizga `ChannelMessage.Read.All` (administrator roziligi talab qilinadi) bilan Graph API kerak.

## Graph orqali media + tarix (kanallar uchun majburiy)

**Kanallarda** rasmlar/fayllar kerak bo‘lsa yoki **xabarlar tarixini** olishni xohlasangiz, Microsoft Graph ruxsatlarini yoqib, administrator roziligini berishingiz kerak.

1. Entra ID (Azure AD) **App Registration** ichida Microsoft Graph **Application permissions** qo‘shing:
   - `ChannelMessage.Read.All` (kanal biriktirmalari + tarix)
   - `Chat.Read.All` yoki `ChatMessage.Read.All` (guruh chatlari)
2. **Grant admin consent** for the tenant.
3. Teams ilovasi **manifest versiyasini** oshiring, qayta yuklang va **ilovani Teams’da qayta o‘rnating**.
4. Keshlangan ilova metama’lumotlarini tozalash uchun **Teams’ni to‘liq yopib, qayta ishga tushiring**.

## Ma’lum cheklovlar

### Webhook timeoutlari

Teams xabarlarni HTTP webhook orqali yetkazadi. Agar qayta ishlash juda uzoq davom etsa (masalan, sekin LLM javoblari), quyidagilar yuz berishi mumkin:

- Gateway timeoutlari
- Teams xabarni qayta yuborishi (takrorlanishiga olib keladi)
- Yo‘qolib ketgan javoblar

OpenClaw buni tezda javob qaytarib va javoblarni proaktiv yuborish orqali hal qiladi, ammo juda sekin javoblar baribir muammo keltirib chiqarishi mumkin.

### Formatlash

Teams markdown’i Slack yoki Discord’ga qaraganda cheklanganroq:

- Basic formatting works: **bold**, _italic_, `code`, links
- Murakkab markdown (jadval, ichma-ich ro‘yxatlar) to‘g‘ri ko‘rinmasligi mumkin
- Adaptive Cards so‘rovnomalar va ixtiyoriy kartalarni yuborish uchun qo‘llab-quvvatlanadi (quyiga qarang)

## Konfiguratsiya

Asosiy sozlamalar (umumiy kanal andozalari uchun `/gateway/configuration` ga qarang):

- `channels.msteams.enabled`: enable/disable the channel.
- `channels.msteams.appId`, `channels.msteams.appPassword`, `channels.msteams.tenantId`: bot hisob ma’lumotlari.
- `channels.msteams.webhook.port` (standart `3978`)
- `channels.msteams.webhook.path` (standart `/api/messages`)
- `channels.msteams.dmPolicy`: `pairing | allowlist | open | disabled` (standart: pairing)
- `channels.msteams.allowFrom`: DM’lar uchun ruxsat ro‘yxati (AAD obyekt ID’lari, UPN’lar yoki ko‘rinadigan nomlar). Graph’ga kirish mavjud bo‘lsa, ustoz (wizard) sozlash vaqtida nomlarni ID’larga aylantiradi.
- `channels.msteams.textChunkLimit`: chiqish matn bo‘laklari o‘lchami.
- `channels.msteams.chunkMode`: `length` (standart) yoki `newline` — bo‘sh satrlar (paragraf chegaralari) bo‘yicha bo‘lish, so‘ng uzunlikka ko‘ra bo‘lish.
- `channels.msteams.mediaAllowHosts`: kiruvchi biriktirmalar uchun ruxsat etilgan hostlar ro‘yxati (standart — Microsoft/Teams domenlari).
- `channels.msteams.mediaAuthAllowHosts`: media qayta urinishlarida Authorization sarlavhalarini biriktirish uchun ruxsat etilgan hostlar (standart — Graph + Bot Framework hostlari).
- `channels.msteams.requireMention`: require @mention in channels/groups (default true).
- `channels.msteams.replyStyle`: `thread | top-level` (qarang [Reply Style](#reply-style-threads-vs-posts)).
- `channels.msteams.teams.<teamId>
  .replyStyle`: har bir jamoa uchun alohida sozlama.`channels.msteams.teams.<teamId>
  .requireMention`: har bir jamoa uchun alohida sozlama.
- `channels.msteams.teams.<teamId>.requireMention`: per-team override.
- `channels.msteams.teams.<teamId>.tools`: default per-team tool policy overrides (`allow`/`deny`/`alsoAllow`) used when a channel override is missing.
- `channels.msteams.teams.<teamId>.toolsBySender`: default per-team per-sender tool policy overrides (`"*"` wildcard supported).
- `channels.msteams.teams.<teamId>.channels.<conversationId>.replyStyle`: per-channel override.
- `channels.msteams.teams.<teamId>.channels.<conversationId>.requireMention`: per-channel override.
- `channels.msteams.teams.<teamId>.channels.<conversationId>.tools`: per-channel tool policy overrides (`allow`/`deny`/`alsoAllow`).
- `channels.msteams.teams.<teamId>.channels.<conversationId>.toolsBySender`: per-channel per-sender tool policy overrides (`"*"` wildcard supported).
- `channels.msteams.sharePointSiteId`: SharePoint site ID for file uploads in group chats/channels (see [Sending files in group chats](#sending-files-in-group-chats)).

## Routing & Sessions

- Session keys follow the standard agent format (see [/concepts/session](/concepts/session)):
  - Direct messages share the main session (`agent:<agentId>:<mainKey>`).
  - Channel/group messages use conversation id:
    - `agent:<agentId>:msteams:channel:<conversationId>`
    - `agent:<agentId>:msteams:group:<conversationId>`

## Reply Style: Threads vs Posts

Teams recently introduced two channel UI styles over the same underlying data model:

| Style                                       | Description                                               | Recommended `replyStyle`              |
| ------------------------------------------- | --------------------------------------------------------- | ------------------------------------- |
| **Posts** (classic)      | Messages appear as cards with threaded replies underneath | `thread` (default) |
| **Threads** (Slack-like) | Messages flow linearly, more like Slack                   | `top-level`                           |

**The problem:** The Teams API does not expose which UI style a channel uses. If you use the wrong `replyStyle`:

- `thread` in a Threads-style channel → replies appear nested awkwardly
- `top-level` in a Posts-style channel → replies appear as separate top-level posts instead of in-thread

**Solution:** Configure `replyStyle` per-channel based on how the channel is set up:

```json
{
  "msteams": {
    "replyStyle": "thread",
    "teams": {
      "19:abc...@thread.tacv2": {
        "channels": {
          "19:xyz...@thread.tacv2": {
            "replyStyle": "top-level"
          }
        }
      }
    }
  }
}
```

## Attachments & Images

**Current limitations:**

- **DMs:** Images and file attachments work via Teams bot file APIs.
- **Channels/groups:** Attachments live in M365 storage (SharePoint/OneDrive). The webhook payload only includes an HTML stub, not the actual file bytes. **Graph API permissions are required** to download channel attachments.

Without Graph permissions, channel messages with images will be received as text-only (the image content is not accessible to the bot).
By default, OpenClaw only downloads media from Microsoft/Teams hostnames. Override with `channels.msteams.mediaAllowHosts` (use `["*"]` to allow any host).
Authorization headers are only attached for hosts in `channels.msteams.mediaAuthAllowHosts` (defaults to Graph + Bot Framework hosts). 1. Ushbu roʻyxatni qatʼiy saqlang (multi-tenant qoʻshimchalaridan qoching).

## 2. Guruh chatlarida fayllarni yuborish

3. Botlar DMlarda FileConsentCard oqimi (o‘rnatilgan) orqali fayllarni yuborishi mumkin. 4. Biroq, **guruh chatlari/kanallarda fayllarni yuborish** qo‘shimcha sozlamalarni talab qiladi:

| 5. Kontekst                                              | 6. Fayllar qanday yuboriladi                                   | 7. Kerakli sozlamalar                                    |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| 8. **DMlar**                                             | 9. FileConsentCard → foydalanuvchi qabul qiladi → bot yuklaydi | 10. Qutidan chiqqan holda ishlaydi                       |
| 11. **Guruh chatlari/kanallar**                          | 12. SharePoint’ga yuklash → ulashish havolasini yuborish       | 13. `sharePointSiteId` + Graph ruxsatlari talab qilinadi |
| 14. **Rasmlar (har qanday kontekst)** | 15. Base64-kodlangan inline                                    | 16. Qutidan chiqqan holda ishlaydi                       |

### 17. Nima uchun guruh chatlari SharePoint’ni talab qiladi

18. Botlarda shaxsiy OneDrive diski yo‘q ( `/me/drive` Graph API endpoint’i ilova identifikatorlari uchun ishlamaydi). 19. Guruh chatlari/kanallarda fayllarni yuborish uchun bot **SharePoint saytiga** yuklaydi va ulashish havolasini yaratadi.

### 20. Sozlash

1. 21. Entra ID (Azure AD) → App Registration’da **Graph API ruxsatlarini qo‘shing**:
   - 22. `Sites.ReadWrite.All` (Application) — SharePoint’ga fayllarni yuklash
   - 23. `Chat.Read.All` (Application) — ixtiyoriy, foydalanuvchiga xos ulashish havolalarini yoqadi

2. **Grant admin consent** for the tenant.

3. 25. **SharePoint sayt ID’ingizni oling:**

   ```bash
   26. # Graph Explorer yoki amal qiluvchi token bilan curl orqali:
   ```

4. curl -H "Authorization: Bearer $TOKEN" \
   "https://graph.microsoft.com/v1.0/sites/{hostname}:/{site-path}"

   ```json5
   # Example: for a site at "contoso.sharepoint.com/sites/BotFiles"
   ```

### curl -H "Authorization: Bearer $TOKEN" \&#xA;"https://graph.microsoft.com/v1.0/sites/contoso.sharepoint.com:/sites/BotFiles"

| # Response includes: "id": "contoso.sharepoint.com,guid1,guid2"                                                                                                                                                                                                                         | Sharing behavior                          |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| 28. {&#xA;channels: {&#xA;msteams: {&#xA;// ... other config ...&#xA;sharePointSiteId: "contoso.sharepoint.com,guid1,guid2",&#xA;},&#xA;},&#xA;} | 29. Ulashish xulqi |
| 30. Ruxsat                                                                                                                                                                                                                                                                                                                       | 31. Ulashish xulqi |

32. Faqat `Sites.ReadWrite.All` 33. Tashkilot bo‘ylab ulashish havolasi (tashkilotdagi hamma kira oladi)

### 34. `Sites.ReadWrite.All` + `Chat.Read.All`

| 35. Foydalanuvchiga xos ulashish havolasi (faqat chat a’zolari kira oladi)       | 36. Foydalanuvchiga xos ulashish xavfsizroq, chunki faylga faqat chat ishtirokchilari kira oladi. |
| -------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| 37. Agar `Chat.Read.All` ruxsati bo‘lmasa, bot tashkilot bo‘ylab ulashishga o‘tadi. | 38. Zaxira (fallback) xulq                                                                     |
| 39. Ssenariy                                                                                        | 40. Natija                                                                                                        |
| 41. Guruh chat + fayl + `sharePointSiteId` sozlangan                                                | 42. SharePoint’ga yuklash, ulashish havolasini yuborish                                                           |
| 43. Guruh chat + fayl + `sharePointSiteId` yo‘q                                                     | 44. OneDrive’ga yuklashga urinish (muvaffaqiyatsiz bo‘lishi mumkin), faqat matn yuboriladi     |

### 45. Shaxsiy chat + fayl

46. FileConsentCard oqimi (SharePoint’siz ham ishlaydi)

## So‘rovnomalar (Adaptive Cards)

OpenClaw Teams so‘rovnomalarini Adaptive Cards orqali yuboradi (Teams’da mahalliy so‘rovnoma API yo‘q).

- CLI: `openclaw message poll --channel msteams --target conversation:<id> ...`
- Ovozlar gateway tomonidan `~/.openclaw/msteams-polls.json` faylida saqlanadi.
- The gateway must stay online to record votes.
- Polls do not auto-post result summaries yet (inspect the store file if needed).

## Adaptive Cards (ixtiyoriy)

`message` vositasi yoki CLI yordamida Teams foydalanuvchilari yoki suhbatlariga istalgan Adaptive Card JSON yuboring.

`card` parametri Adaptive Card JSON obyektini qabul qiladi. `card` berilganda, xabar matni ixtiyoriy bo‘ladi.

**Agent vositasi:**

```json
{
  "action": "send",
  "channel": "msteams",
  "target": "user:<id>",
  "card": {
    "type": "AdaptiveCard",
    "version": "1.5",
    "body": [{ "type": "TextBlock", "text": "Hello!" }]
  }
}
```

**CLI:**

```bash
openclaw message send --channel msteams \
  --target "conversation:19:abc...@thread.tacv2" \
  --card '{"type":"AdaptiveCard","version":"1.5","body":[{"type":"TextBlock","text":"Hello!"}]}'
```

Karta sxemasi va misollar uchun [Adaptive Cards hujjatlari](https://adaptivecards.io/) ga qarang. Target formati tafsilotlari uchun quyidagi [Target formatlari](#target-formats) bo‘limiga qarang.

## Target formatlari

MSTeams targetlari foydalanuvchilar va suhbatlarni farqlash uchun prefikslardan foydalanadi:

| Target turi                                     | Format                           | Misol                                                                    |
| ----------------------------------------------- | -------------------------------- | ------------------------------------------------------------------------ |
| Foydalanuvchi (ID bo‘yicha)  | `user:<aad-object-id>`           | `user:40a1a0ed-4ff2-4164-a219-55518990c197`                              |
| Foydalanuvchi (ism bo‘yicha) | `user:<display-name>`            | `user:John Smith` (Graph API talab etiladi)           |
| Guruh/kanal                                     | `conversation:<conversation-id>` | `conversation:19:abc123...@thread.tacv2`                                 |
| Guruh/kanal (xom)            | `<conversation-id>`              | `19:abc123...@thread.tacv2` (`@thread` mavjud bo‘lsa) |

**CLI misollari:**

```bash
# ID bo‘yicha foydalanuvchiga yuborish
openclaw message send --channel msteams --target "user:40a1a0ed-..." --message "Hello"

# Ko‘rsatiladigan nom bo‘yicha foydalanuvchiga yuborish (Graph API qidiruvini ishga tushiradi)
openclaw message send --channel msteams --target "user:John Smith" --message "Hello"

# Guruh chatiga yoki kanalga yuborish
openclaw message send --channel msteams --target "conversation:19:abc...@thread.tacv2" --message "Hello"

# Suhbatga Adaptive Card yuborish
openclaw message send --channel msteams --target "conversation:19:abc...@thread.tacv2" \
  --card '{"type":"AdaptiveCard","version":"1.5","body":[{"type":"TextBlock","text":"Hello"}]}'
```

**Agent vositasi misollari:**

```json
{
  "action": "send",
  "channel": "msteams",
  "target": "user:John Smith",
  "message": "Hello!"
}
```

```json
{
  "action": "send",
  "channel": "msteams",
  "target": "conversation:19:abc...@thread.tacv2",
  "card": {
    "type": "AdaptiveCard",
    "version": "1.5",
    "body": [{ "type": "TextBlock", "text": "Hello" }]
  }
}
```

Eslatma: `user:` prefiksi bo‘lmasa, nomlar sukut bo‘yicha guruh/jamoa sifatida aniqlanadi. Ko‘rsatiladigan nom bo‘yicha odamlarni nishonga olishda har doim `user:` dan foydalaning.

## Proaktiv xabar yuborish

- Proaktiv xabarlar faqat foydalanuvchi **muloqot qilgandan keyin** mumkin, chunki biz shu paytda suhbat havolalarini saqlaymiz.
- `dmPolicy` va allowlist cheklovlari uchun `/gateway/configuration` ga qarang.

## Jamoa va Kanal IDlari (Keng tarqalgan xato)

Teams URLlaridagi `groupId` so‘rov parametri konfiguratsiya uchun ishlatiladigan jamoa IDsi **EMAS**. Buning o‘rniga IDlarni URL yo‘lidan ajrating:

**Jamoa URLi:**

```
https://teams.microsoft.com/l/team/19%3ABk4j...%40thread.tacv2/conversations?groupId=...
                                    └────────────────────────────┘
                                    Jamoa IDsi (buni URL-dekod qiling)
```

**Kanal URLi:**

```
https://teams.microsoft.com/l/channel/19%3A15bc...%40thread.tacv2/ChannelName?groupId=...
                                      └─────────────────────────┘
                                      Kanal IDsi (buni URL-dekod qiling)
```

**Konfiguratsiya uchun:**

- Team ID = `/team/` dan keyingi yo‘l segmenti (URL-dekodlangan, masalan, `19:Bk4j...@thread.tacv2`)
- Channel ID = `/channel/` dan keyingi yo‘l segmenti (URL-dekodlangan)
- `groupId` so‘rov parametrini **e’tiborsiz qoldiring**

## Yopiq (Private) kanallar

Botlar yopiq kanallarda cheklangan qo‘llab-quvvatlashga ega:

| Funksiya                                        | Standart kanallar | Private Channels                        |
| ----------------------------------------------- | ----------------- | --------------------------------------- |
| Botni o‘rnatish                                 | Ha                | Cheklangan                              |
| Real-time messages (webhook) | Yes               | Ishlamasligi mumkin                     |
| RSC ruxsatlari                                  | Ha                | Boshqacha ishlashi mumkin               |
| @mentionlar                        | Ha                | Agar botga kirish mumkin bo‘lsa         |
| Graph API tarixi                                | Ha                | Ha (ruxsatlar bilan) |

**Agar yopiq kanallar ishlamasa, yechimlar:**

1. Bot bilan o‘zaro aloqalar uchun standart kanallardan foydalaning
2. DMlardan foydalaning — foydalanuvchilar har doim botga to‘g‘ridan-to‘g‘ri xabar yubora oladi
3. Tarixiy ma’lumotlarga kirish uchun Graph API’dan foydalaning (`ChannelMessage.Read.All` talab etiladi)

## Nosozliklarni bartaraf etish

### Keng tarqalgan muammolar

- **Kanallarda rasmlar ko‘rinmayapti:** Graph ruxsatlari yoki administrator roziligi yetishmayapti. Teams ilovasini qayta o‘rnating va Teams’ni to‘liq yopib qayta oching.
- **Kanалда javoblar yo‘q:** odatda @mention talab qilinadi; `channels.msteams.requireMention=false` qilib sozlang yoki jamoa/kanal bo‘yicha alohida sozlang.
- **Versiya nomuvofiqligi (Teams eski manifestni ko‘rsatmoqda):** ilovani olib tashlab qayta qo‘shing va Teams’ni to‘liq yoping — yangilanish uchun.
- **Webhook’dan 401 Unauthorized:** Azure JWTsiz qo‘lda sinov qilganda kutiladi — endpoint yetib borilishini bildiradi, ammo autentifikatsiya muvaffaqiyatsiz. To‘g‘ri sinash uchun Azure Web Chat’dan foydalaning.

### Manifest yuklash xatolari

- **"Icon file cannot be empty":** Manifest 0 baytli ikon fayllarga ishora qilmoqda. `outline.png` uchun 32x32, `color.png` uchun 192x192 o‘lchamdagi yaroqli PNG ikonlarni yarating.
- **"webApplicationInfo.Id already in use":** Ilova boshqa jamoa/chatda hali ham o‘rnatilgan. Avval topib olib o‘chiring yoki tarqalish uchun 5–10 daqiqa kuting.
- **Yuklashda "Something went wrong":** Buning o‘rniga [https://admin.teams.microsoft.com](https://admin.teams.microsoft.com) orqali yuklang, brauzer DevTools (F12) → Network bo‘limini oching va haqiqiy xato uchun response body’ni tekshiring.
- **Sideload ishlamayapti:** "Upload a custom app" o‘rniga "Upload an app to your org's app catalog"ni sinab ko‘ring — bu ko‘pincha sideload cheklovlarini chetlab o‘tadi.

### RSC ruxsatlari ishlamayapti

1. `webApplicationInfo.id` botingizning App ID’si bilan aynan mos kelishini tekshiring
2. Ilovani qayta yuklang va jamoa/chatga qayta o‘rnating
3. Tashkilot administratori RSC ruxsatlarini bloklamaganini tekshiring
4. To‘g‘ri scope’dan foydalanayotganingizni tasdiqlang: jamoalar uchun `ChannelMessage.Read.Group`, guruh chatlari uchun `ChatMessage.Read.Chat`

## References

- [Create Azure Bot](https://learn.microsoft.com/en-us/azure/bot-service/bot-service-quickstart-registration) — Azure Bot’ni sozlash qo‘llanmasi
- [Teams Developer Portal](https://dev.teams.microsoft.com/apps) — Teams ilovalarini yaratish/boshqarish
- [Teams ilova manifest sxemasi](https://learn.microsoft.com/en-us/microsoftteams/platform/resources/schema/manifest-schema)
- [RSC orqali kanal xabarlarini qabul qilish](https://learn.microsoft.com/en-us/microsoftteams/platform/bots/how-to/conversations/channel-messages-with-rsc)
- [RSC ruxsatnomalari ma’lumotnomasi](https://learn.microsoft.com/en-us/microsoftteams/platform/graph-api/rsc/resource-specific-consent)
- [Teams bot fayllar bilan ishlashi](https://learn.microsoft.com/en-us/microsoftteams/platform/bots/how-to/bots-filesv4) (kanal/guruh uchun Graph talab qilinadi)
- [Proaktiv xabar yuborish](https://learn.microsoft.com/en-us/microsoftteams/platform/bots/how-to/conversations/send-proactive-messages)
