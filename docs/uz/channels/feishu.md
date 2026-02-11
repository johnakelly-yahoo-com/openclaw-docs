---
summary: "Feishu bot overview, features, and configuration"
read_when:
  - You want to connect a Feishu/Lark bot
  - You are configuring the Feishu channel
title: Feishu
---

# Feishu bot

Feishu (Lark) is a team chat platform used by companies for messaging and collaboration. This plugin connects OpenClaw to a Feishu/Lark bot using the platform’s WebSocket event subscription so messages can be received without exposing a public webhook URL.

---

## Plugin required

Install the Feishu plugin:

```bash
openclaw plugins install @openclaw/feishu
```

Local checkout (when running from a git repo):

```bash
openclaw plugins install ./extensions/feishu
```

---

## Quickstart

There are two ways to add the Feishu channel:

### Method 1: onboarding wizard (recommended)

If you just installed OpenClaw, run the wizard:

```bash
openclaw onboard
```

The wizard guides you through:

1. Creating a Feishu app and collecting credentials
2. Configuring app credentials in OpenClaw
3. Starting the gateway

✅ **After configuration**, check gateway status:

- `openclaw gateway status`
- `openclaw logs --follow`

### Method 2: CLI setup

If you already completed initial install, add the channel via CLI:

```bash
openclaw channels add
```

Choose **Feishu**, then enter the App ID and App Secret.

✅ **After configuration**, manage the gateway:

- `openclaw gateway status`
- `openclaw gateway restart`
- `openclaw logs --follow`

---

## Step 1: Create a Feishu app

### 1. Open Feishu Open Platform

Visit [Feishu Open Platform](https://open.feishu.cn/app) and sign in.

Lark (global) tenants should use [https://open.larksuite.com/app](https://open.larksuite.com/app) and set `domain: "lark"` in the Feishu config.

### 2. Create an app

1. Click **Create enterprise app**
2. Fill in the app name + description
3. Choose an app icon

![Create enterprise app](../images/feishu-step2-create-app.png)

### 3. Copy credentials

From **Credentials & Basic Info**, copy:

- **App ID** (format: `cli_xxx`)
- **App Secret**

❗ **Important:** keep the App Secret private.

![Get credentials](../images/feishu-step3-credentials.png)

### 4. Configure permissions

On **Permissions**, click **Batch import** and paste:

```json
{
  "scopes": {
    "tenant": [
      "aily:file:read",
      "aily:file:write",
      "application:application.app_message_stats.overview:readonly",
      "application:application:self_manage",
      "application:bot.menu:write",
      "contact:user.employee_id:readonly",
      "corehr:file:download",
      "event:ip_list",
      "im:chat.access_event.bot_p2p_chat:read",
      "im:chat.members:bot_access",
      "im:message",
      "im:message.group_at_msg:readonly",
      "im:message.p2p_msg:readonly",
      "im:message:readonly",
      "im:message:send_as_bot",
      "im:resource"
    ],
    "user": ["aily:file:read", "aily:file:write", "im:chat.access_event.bot_p2p_chat:read"]
  }
}
```

![Configure permissions](../images/feishu-step4-permissions.png)

### 5. Enable bot capability

In **App Capability** > **Bot**:

1. Enable bot capability
2. Set the bot name

![Enable bot capability](../images/feishu-step5-bot-capability.png)

### 6. Configure event subscription

⚠️ **Important:** before setting event subscription, make sure:

1. You already ran `openclaw channels add` for Feishu
2. The gateway is running (`openclaw gateway status`)

In **Event Subscription**:

1. Choose **Use long connection to receive events** (WebSocket)
2. Add the event: `im.message.receive_v1`

⚠️ If the gateway is not running, the long-connection setup may fail to save.

![Configure event subscription](../images/feishu-step6-event-subscription.png)

### 7. Publish the app

1. Create a version in **Version Management & Release**
2. Submit for review and publish
3. Wait for admin approval (enterprise apps usually auto-approve)

---

## Step 2: Configure OpenClaw

### Configure with the wizard (recommended)

```bash
openclaw channels add
```

Choose **Feishu** and paste your App ID + App Secret.

### Configure via config file

Edit `~/.openclaw/openclaw.json`:

```json5
{
  channels: {
    feishu: {
      enabled: true,
      dmPolicy: "pairing",
      accounts: {
        main: {
          appId: "cli_xxx",
          appSecret: "xxx",
          botName: "My AI assistant",
        },
      },
    },
  },
}
```

### Configure via environment variables

```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
```

### Lark (global) domain

If your tenant is on Lark (international), set the domain to `lark` (or a full domain string). 1. Siz uni `channels.feishu.domain` da yoki har bir hisob bo‘yicha (`channels.feishu.accounts.<id> 2. .domain`) sozlashingiz mumkin.3. {
channels: {
feishu: {
domain: "lark",
accounts: {
main: {
appId: "cli_xxx",
appSecret: "xxx",
},
},
},
},
}

```json5
4. 3-qadam: Ishga tushirish + sinov
```

---

## Step 3: Start + test

### 6. Gateway’ni ishga tushiring 7. openclaw gateway

```bash
8. 2.
```

### 9. Sinov xabarini yuboring 10. Feishu’da botingizni topib, unga xabar yuboring.

11. 3.

### 12. Juftlashni tasdiqlash 13. Odatiy holatda bot juftlash kodi bilan javob beradi.

14. Uni tasdiqlang: 15. openclaw pairing approve feishu <CODE>

```bash
16. Tasdiqlangandan so‘ng, odatdagidek chat qilishingiz mumkin.
```

After approval, you can chat normally.

---

## **Feishu bot kanali**: gateway tomonidan boshqariladigan Feishu boti

- **Deterministik marshrutlash**: javoblar har doim Feishu’ga qaytadi
- **Sessiyalarni ajratish**: shaxsiy xabarlar bitta asosiy sessiyani ulashadi; guruhlar esa ajratilgan
- **Session isolation**: DMs share a main session; groups are isolated
- 22. Kirish nazorati

---

## 23. Shaxsiy xabarlar

### **Standart**: `dmPolicy: "pairing"` (noma’lum foydalanuvchilar juftlash kodini oladi)

- **Juftlashni tasdiqlash**:

- **Approve pairing**:

  ```bash
  **Allowlist rejimi**: ruxsat etilgan Open ID’lar bilan `channels.feishu.allowFrom` ni sozlang
  ```

- 28. Guruh chatlari

### \*\*1.

30. Guruh siyosati\*\* (`channels.feishu.groupPolicy`): `"open"` = guruhlarda hammaga ruxsat (standart)

- `"allowlist"` = faqat `groupAllowFrom` ga ruxsat
- `"disabled"` = guruh xabarlarini o‘chirish
- \*\*2.

35. Eslatib o‘tish talabi\*\* (\`channels.feishu.groups.<chat_id>
36. .requireMention`): `true` = @mention talab qilinadi (standart)`false\` = eslatmasiz javob berish

- 39. Guruh sozlamalari misollari
- 40. Barcha guruhlarga ruxsat, @mention talab qilinadi (standart)

---

41. {
    channels: {
    feishu: {
    groupPolicy: "open",
    // Default requireMention: true
    },
    },
    }
-----

### 42. Barcha guruhlarga ruxsat, @mention talab qilinmaydi

```json5
43. {
  channels: {
    feishu: {
      groups: {
        oc_xxx: { requireMention: false },
      },
    },
  },
}
```

### 44. Faqat ma’lum foydalanuvchilarga guruhlarda ruxsat berish

```json5
45. {
  channels: {
    feishu: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["ou_xxx", "ou_yyy"],
    },
  },
}
```

### 46. Guruh/foydalanuvchi ID’larini olish

```json5
47. Guruh ID’lari (chat_id)
```

---

## 48. Guruh ID’lari `oc_xxx` ko‘rinishida bo‘ladi.

### **49. 1-usul (tavsiya etiladi)**

50. Gateway’ni ishga tushiring va guruhda botni @mention qiling

**Method 1 (recommended)**

1. Start the gateway and @mention the bot in the group
2. `openclaw logs --follow` ni ishga tushiring va `chat_id` ni qidiring

**2-usul**

Guruh chatlarini roʻyxatlash uchun Feishu API debuggeridan foydalaning.

### Foydalanuvchi IDlari (open_id)

Foydalanuvchi IDlari `ou_xxx` koʻrinishida boʻladi.

**1-usul (tavsiya etiladi)**

1. Gateway’ni ishga tushiring va botga shaxsiy xabar (DM) yuboring
2. `openclaw logs --follow` ni ishga tushiring va `open_id` ni qidiring

**2-usul**

Foydalanuvchi Open IDlari uchun pairing soʻrovlarini tekshiring:

```bash
openclaw pairing list feishu
```

---

## Umumiy buyruqlar

| Buyruq    | Tavsif                          |
| --------- | ------------------------------- |
| `/status` | Bot holatini ko‘rsatish         |
| `/reset`  | Sessiyani tiklash               |
| `/model`  | Modelni ko‘rsatish/almashtirish |

> Eslatma: Feishu hozircha mahalliy buyruqlar menyusini qo‘llab-quvvatlamaydi, shuning uchun buyruqlar matn ko‘rinishida yuborilishi kerak.

## Gateway boshqaruv buyruqlari

| Command                    | Tavsif                                      |
| -------------------------- | ------------------------------------------- |
| `openclaw gateway status`  | Gateway holatini ko‘rsatish                 |
| `openclaw gateway install` | Gateway xizmatini o‘rnatish/ishga tushirish |
| `openclaw gateway stop`    | Gateway xizmatini to‘xtatish                |
| `openclaw gateway restart` | Gateway xizmatini qayta ishga tushirish     |
| `openclaw logs --follow`   | Gateway loglarini real vaqtda ko‘rish       |

---

## Muammolarni bartaraf etish

### Bot guruh chatlarida javob bermaydi

1. Bot guruhga qo‘shilganini tekshiring
2. Botni @mention qilganingizga ishonch hosil qiling (standart xatti-harakat)
3. `groupPolicy` `"disabled"` ga o‘rnatilmaganini tekshiring
4. Loglarni tekshiring: `openclaw logs --follow`

### Bot xabarlarni qabul qilmayapti

1. Ilova nashr qilingan va tasdiqlanganini tekshiring
2. Hodisa obunasi `im.message.receive_v1` ni o‘z ichiga olganini tekshiring
3. **uzoq ulanish (long connection)** yoqilganini tekshiring
4. Ilova ruxsatlari to‘liq ekanini tekshiring
5. Ensure the gateway is running: `openclaw gateway status`
6. Loglarni tekshiring: `openclaw logs --follow`

### App Secret sizib chiqishi

1. Feishu Open Platform’da App Secret’ni qayta tiklang
2. Konfiguratsiyangizda App Secret’ni yangilang
3. Restart the gateway

### Message send failures

1. Ensure the app has `im:message:send_as_bot` permission
2. Ensure the app is published
3. Check logs for detailed errors

---

## Advanced configuration

### Multiple accounts

```json5
{
  channels: {
    feishu: {
      accounts: {
        main: {
          appId: "cli_xxx",
          appSecret: "xxx",
          botName: "Primary bot",
        },
        backup: {
          appId: "cli_yyy",
          appSecret: "yyy",
          botName: "Backup bot",
          enabled: false,
        },
      },
    },
  },
}
```

### Message limits

- `textChunkLimit`: outbound text chunk size (default: 2000 chars)
- `mediaMaxMb`: media upload/download limit (default: 30MB)

### Streaming

Feishu supports streaming replies via interactive cards. When enabled, the bot updates a card as it generates text.

```json5
{
  channels: {
    feishu: {
      streaming: true, // enable streaming card output (default true)
      blockStreaming: true, // enable block-level streaming (default true)
    },
  },
}
```

Set `streaming: false` to wait for the full reply before sending.

### Multi-agent routing

Use `bindings` to route Feishu DMs or groups to different agents.

```json5
10. `match.peer.kind`: `"direct"` yoki `"group"`
```

Routing fields:

- `match.channel`: `"feishu"`
- 11. %%{init: {
      'theme': 'base',
      'themeVariables': {
      'primaryColor': '#ffffff',
      'primaryTextColor': '#000000',
      'primaryBorderColor': '#000000',
      'lineColor': '#000000',
      'secondaryColor': '#f9f9fb',
      'tertiaryColor': '#ffffff',
      'clusterBkg': '#f9f9fb',
      'clusterBorder': '#000000',
      'nodeBorder': '#000000',
      'mainBkg': '#ffffff',
      'edgeLabelBackground': '#ffffff'
      }
      }}%%
      flowchart TB
      subgraph T[" "]
      subgraph Tailscale[" "]
      direction LR
      Gateway["<b>Gateway xosti (Linux/VM)<br></b><br>openclaw gateway<br>channels.imessage.cliPath"]
      Mac["<b>Messages + imsg o‘rnatilgan Mac<br></b><br>Messages tizimga kirgan<br>Remote Login yoqilgan"]
      end
      Gateway -- SSH (imsg rpc) --> Mac
      Mac -- SCP (biriktirmalar) --> Gateway
      direction BT
      User["user@gateway-host"] -- "Tailscale tailnet (hostname yoki 100.x.y.z)" --> Gateway
      end
- `match.peer.id`: user Open ID (`ou_xxx`) or group ID (`oc_xxx`)

See [Get group/user IDs](#get-groupuser-ids) for lookup tips.

---

## Configuration reference

Full configuration: [Gateway configuration](/gateway/configuration)

Key options:

| Setting                                           | Description                                                         | Default   |
| ------------------------------------------------- | ------------------------------------------------------------------- | --------- |
| `channels.feishu.enabled`                         | Enable/disable channel                                              | `true`    |
| `channels.feishu.domain`                          | API domain (`feishu` or `lark`)                  | `feishu`  |
| `channels.feishu.accounts.<id>.appId`             | App ID                                                              | -         |
| `channels.feishu.accounts.<id>.appSecret`         | App Secret                                                          | -         |
| `channels.feishu.accounts.<id>.domain`            | Per-account API domain override                                     | `feishu`  |
| `channels.feishu.dmPolicy`                        | DM policy                                                           | `pairing` |
| `channels.feishu.allowFrom`                       | DM allowlist (open_id list) | -         |
| `channels.feishu.groupPolicy`                     | Group policy                                                        | `open`    |
| `channels.feishu.groupAllowFrom`                  | Group allowlist                                                     | -         |
| `channels.feishu.groups.<chat_id>.requireMention` | Require @mention                                       | `true`    |
| `channels.feishu.groups.<chat_id>.enabled`        | Enable group                                                        | `true`    |
| `channels.feishu.textChunkLimit`                  | Message chunk size                                                  | `2000`    |
| `channels.feishu.mediaMaxMb`                      | Media size limit                                                    | `30`      |
| `channels.feishu.streaming`                       | Enable streaming card output                                        | `true`    |
| `channels.feishu.blockStreaming`                  | Enable block streaming                                              | `true`    |

---

## dmPolicy reference

| Value         | Behavior                                                                        |
| ------------- | ------------------------------------------------------------------------------- |
| `"pairing"`   | **Default.** Unknown users get a pairing code; must be approved |
| `"allowlist"` | Only users in `allowFrom` can chat                                              |
| `"open"`      | Allow all users (requires `"*"` in allowFrom)                |
| `"disabled"`  | Disable DMs                                                                     |

---

## Supported message types

### Receive

- ✅ Text
- ✅ Rich text (post)
- ✅ Images
- ✅ Files
- ✅ Audio
- ✅ Video
- ✅ Stickers

### Send

- ✅ Text
- ✅ Images
- ✅ Files
- ✅ Audio
- ⚠️ Rich text (partial support)
