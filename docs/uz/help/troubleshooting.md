---
summary: "Symptom first troubleshooting hub for OpenClaw"
read_when:
  - OpenClaw is not working and you need the fastest path to a fix
  - You want a triage flow before diving into deep runbooks
title: "Troubleshooting"
---

# Troubleshooting

If you only have 2 minutes, use this page as a triage front door.

## First 60 seconds

1. Ushbu aniq ketma-ketlikni tartib bilan bajaring:

```bash
2. openclaw status
```

openclaw status --all

- openclaw gateway probe
- openclaw gateway status
- openclaw doctor
- openclaw channels status --probe
- openclaw logs --follow
- 3. Bir qatordagi yaxshi chiqish:
- 4. `openclaw status` → sozlangan kanallarni va aniq avtorizatsiya xatolarisiz holatni ko‘rsatadi.

## 5. `openclaw status --all` → to‘liq hisobot mavjud va ulashish mumkin.

```mermaid
6. `openclaw gateway probe` → kutilgan gateway manzili yetib boriladigan.
```

<AccordionGroup>
  <Accordion title="No replies">7. `openclaw gateway status` → `Runtime: running` va `RPC probe: ok`.<channel>8. `openclaw doctor` → bloklovchi konfiguratsiya/xizmat xatolari yo‘q.

    ```
    9. `openclaw channels status --probe` → kanallar `connected` yoki `ready` deb hisobot beradi.
    ```

  </Accordion>

  <Accordion title="Dashboard or Control UI will not connect">10. `openclaw logs --follow` → barqaror faollik, takrorlanuvchi jiddiy xatolar yo‘q.

    ```
    11. Qarorlar daraxti
    ```

  </Accordion>

  <Accordion title="Gateway will not start or service installed but not running">12. flowchart TD
  A[OpenClaw ishlamayapti] --> B{Qaysi joyda birinchi uziladi}
  B --> C[Javoblar yo‘q]
  B --> D[Dashboard yoki Control UI ulanmaydi]
  B --> E[Gateway ishga tushmaydi yoki xizmat ishlamayapti]
  B --> F[Kanal ulanadi, lekin xabarlar oqimi yo‘q]
  B --> G[Cron yoki heartbeat ishga tushmadi yoki yetkazilmadi]
  B --> H[Tugun ulangan, lekin kamera canvas screen exec muvaffaqiyatsiz]
  B --> I[Browser asbobi ishlamaydi]

  C --> C1[/Javoblar yo‘q bo‘limi/]
  D --> D1[/Control UI bo‘limi/]
  E --> E1[/Gateway bo‘limi/]
  F --> F1[/Kanal oqimi bo‘limi/]
  G --> G1[/Avtomatlashtirish bo‘limi/]
  H --> H1[/Tugun asboblari bo‘limi/]
  I --> I1[/Browser bo‘limi/]

    ```
    13. 
        ```bash
        openclaw status
        openclaw gateway status
        openclaw channels status --probe
        openclaw pairing list 
    ```

  </Accordion>

  <Accordion title="Channel connects but messages do not flow">14. 
    openclaw logs --follow
    ```

    ```
    15. Yaxshi chiqish quyidagicha ko‘rinadi:
    
    - `Runtime: running`
    - `RPC probe: ok`
    - `channels status --probe` da kanalingiz connected/ready ko‘rinadi
    - Yuboruvchi tasdiqlangan (yoki DM siyosati ochiq/allowlist)
    
    Keng tarqalgan log imzolari:
    
    - `drop guild message (mention required` → Discord’da mention cheklovi xabarni to‘sdi.
    - `pairing request` → yuboruvchi tasdiqlanmagan va DM pairing tasdig‘ini kutmoqda.
    - `blocked` / `allowlist` kanal loglarida → yuboruvchi, xona yoki guruh filtrlangan.
    
    Chuqur sahifalar:
    
    - [/gateway/troubleshooting#no-replies](/gateway/troubleshooting#no-replies)
    - [/channels/troubleshooting](/channels/troubleshooting)
    - [/channels/pairing](/channels/pairing)
    ```

  </Accordion>

  <Accordion title="Cron or heartbeat did not fire or did not deliver">16. 
    ```bash
    openclaw status
    openclaw gateway status
    openclaw logs --follow
    openclaw doctor
    openclaw channels status --probe
    ```<jobId>17. Yaxshi chiqish quyidagicha ko‘rinadi:

- `openclaw gateway status` da `Dashboard: http://...` ko‘rsatiladi
- `RPC probe: ok`
- Loglarda auth loop yo‘q

Keng tarqalgan log imzolari:

- `device identity required` → HTTP/xavfsiz bo‘lmagan kontekst qurilma auth’ini yakunlay olmaydi.
- `unauthorized` / qayta ulanish loop’i → noto‘g‘ri token/parol yoki auth rejimi nomuvofiqligi.
- `gateway connect failed:` → UI noto‘g‘ri URL/portni nishonga olgan yoki gateway yetib bo‘lmaydi.

Chuqur sahifalar:

- [/gateway/troubleshooting#dashboard-control-ui-connectivity](/gateway/troubleshooting#dashboard-control-ui-connectivity)
- [/web/control-ui](/web/control-ui)
- [/gateway/authentication](/gateway/authentication)

    ```
    18. 
        ```bash
        openclaw status
        openclaw gateway status
        openclaw logs --follow
        openclaw doctor
        openclaw channels status --probe
        ```
    ```

  </Accordion>

  <Accordion title="Node is paired but tool fails camera canvas screen exec">19. Yaxshi chiqish quyidagicha ko‘rinadi:

- `Service: ... (loaded)`
- `Runtime: running`
- `RPC probe: ok`

Keng tarqalgan log imzolari:

- `Gateway start blocked: set gateway.mode=local` → gateway rejimi o‘rnatilmagan/remote.
- `refusing to bind gateway ... without auth` → token/parolsiz non-loopback bind.
- `another gateway instance is already listening` yoki `EADDRINUSE` → port band.

Chuqur sahifalar:

- [/gateway/troubleshooting#gateway-service-not-running](/gateway/troubleshooting#gateway-service-not-running)
- [/gateway/background-process](/gateway/background-process)
- [/gateway/configuration](/gateway/configuration)<idOrNameOrIp>20. 
    ```bash
    openclaw status
    openclaw gateway status
    openclaw logs --follow
    openclaw doctor
    openclaw channels status --probe
    ```

    ```
    21. Yaxshi chiqish quyidagicha ko‘rinadi:
    
    - Kanal transporti ulangan.
    - Pairing/allowlist tekshiruvlari muvaffaqiyatli.
    - Kerak bo‘lganda mention’lar aniqlanadi.
    
    Keng tarqalgan log imzolari:
    
    - `mention required` → guruh mention cheklovi qayta ishlashni to‘sdi.
    - `pairing` / `pending` → DM yuboruvchi hali tasdiqlanmagan.
    - `not_in_channel`, `missing_scope`, `Forbidden`, `401/403` → kanal ruxsat tokeni muammosi.
    
    Chuqur sahifalar:
    
    - [/gateway/troubleshooting#channel-connected-messages-not-flowing](/gateway/troubleshooting#channel-connected-messages-not-flowing)
    - [/channels/troubleshooting](/channels/troubleshooting)
    ```

  </Accordion>

  <Accordion title="Browser tool fails">22. 
    ```bash
    openclaw status
    openclaw gateway status
    openclaw cron status
    openclaw cron list
    openclaw cron runs --id 

    ```
    23.  --limit 20
        openclaw logs --follow
        ```
    ```

  </Accordion>
</AccordionGroup>
