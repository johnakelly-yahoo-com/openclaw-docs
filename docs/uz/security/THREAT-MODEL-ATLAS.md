# OpenClaw Threat Model v1.0

## MITRE ATLAS Framework

**Version:** 1.0-draft
**Last Updated:** 2026-02-04
**Methodology:** MITRE ATLAS + Data Flow Diagrams
**Framework:** [MITRE ATLAS](https://atlas.mitre.org/) (Adversarial Threat Landscape for AI Systems)

### Framework Attribution

This threat model is built on [MITRE ATLAS](https://atlas.mitre.org/), the industry-standard framework for documenting adversarial threats to AI/ML systems. ATLAS is maintained by [MITRE](https://www.mitre.org/) in collaboration with the AI security community.

**Key ATLAS Resources:**

- [ATLAS Techniques](https://atlas.mitre.org/techniques/)
- [ATLAS Tactics](https://atlas.mitre.org/tactics/)
- [ATLAS Case Studies](https://atlas.mitre.org/studies/)
- [ATLAS GitHub](https://github.com/mitre-atlas/atlas-data)
- [Contributing to ATLAS](https://atlas.mitre.org/resources/contribute)

### Contributing to This Threat Model

This is a living document maintained by the OpenClaw community. See [CONTRIBUTING-THREAT-MODEL.md](./CONTRIBUTING-THREAT-MODEL.md) for guidelines on contributing:

- Reporting new threats
- Updating existing threats
- Proposing attack chains
- Suggesting mitigations

---

## 1. Introduction

### 1.1 Purpose

This threat model documents adversarial threats to the OpenClaw AI agent platform and ClawHub skill marketplace, using the MITRE ATLAS framework designed specifically for AI/ML systems.

### 1.2 Scope

| Component                 | Included | Notes                                                                    |
| ------------------------- | -------- | ------------------------------------------------------------------------ |
| OpenClaw Agent Runtime    | Yes      | Core agent execution, tool calls, sessions                               |
| Gateway                   | Yes      | Autentifikatsiya, marshrutlash, kanal integratsiyasi                     |
| Kanal integratsiyalari    | Ha       | WhatsApp, Telegram, Discord, Signal, Slack va boshqalar. |
| ClawHub Marketplace       | Ha       | Ko‘nikmalarni nashr qilish, moderatsiya, tarqatish                       |
| MCP serverlari            | Ha       | Tashqi vosita provayderlari                                              |
| Foydalanuvchi qurilmalari | Qisman   | Mobil ilovalar, desktop mijozlar                                         |

### 1.3 Qo‘llanilmaydigan soha

Ushbu tahdid modeli uchun hech narsa aniq ravishda qo‘llanilmaydigan deb belgilanmagan.

---

## 2. Tizim arxitekturasi

### 2.1 Trust Boundaries

```
┌─────────────────────────────────────────────────────────────────┐
│                    ISHONCHSIZ ZONA                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  WhatsApp   │  │  Telegram   │  │   Discord   │  ...         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘              │
│         │                │                │                      │
└─────────┼────────────────┼────────────────┼──────────────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────┐
│                 ISHONCH CHEGARASI 1: Kanalga kirish              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                      SHLYUZ                              │   │
│  │  • Qurilma juftlash (30 soniyalik imtiyozli davr)         │   │
│  │  • AllowFrom / AllowList tekshiruvi                       │   │
│  │  • Token/Parol/Tailscale autentifikatsiyasi               │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 ISHONCH CHEGARASI 2: Sessiya izolyatsiyasi       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   AGENT SESSIYALARI                       │   │
│  │  • Sessiya kaliti = agent:kanal:peer                      │   │
│  │  • Har bir agent uchun vosita siyosatlari                 │   │
│  │  • Transkriptlarni jurnalga yozish                        │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 ISHONCH CHEGARASI 3: Vosita bajarilishi          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  BAJARISH SANDIQCHASI                     │   │
│  │  • Docker sandiqchasi YOKI Host (exec-tasdiqlar)          │   │
│  │  • Node masofaviy bajarish                                │   │
│  │  • SSRF himoyasi (DNS pinning + IP bloklash)              │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 ISHONCH CHEGARASI 4: Tashqi kontent              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │        YUKLAB OLINGAN URL’LAR / EMAIL’LAR / WEBHOOK’LAR    │   │
│  │  • Tashqi kontentni o‘rash (XML teglar)                   │   │
│  │  • Xavfsizlik ogohlantirishini kiritish                   │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 ISHONCH CHEGARASI 5: Ta’minot zanjiri            │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                      CLAWHUB                              │   │
│  │  • Ko‘nikmalarni nashr qilish (semver, SKILL.md majburiy) │   │
│  │  • Andozaga asoslangan moderatsiya flaglari               │   │
│  │  • VirusTotal skanerlash (tez orada)                      │   │
│  │  • GitHub akkaunti yoshini tekshirish                     │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Ma’lumotlar oqimlari

| Oqim                         | Manba                           | Manzil                          | Ma’lumot                                  | Himoya                                        |
| ---------------------------- | ------------------------------- | ------------------------------- | ----------------------------------------- | --------------------------------------------- |
| F1                           | Kanal                           | Shlyuz                          | Foydalanuvchi xabarlari                   | TLS, AllowFrom                                |
| F2                           | Shlyuz                          | Agent                           | Marshrutlangan xabarlar                   | Sessiya izolyatsiyasi                         |
| F3                           | Agent                           | Vositalar                       | Vosita chaqiruvlari                       | Siyosatni majburiy qo‘llash                   |
| F4                           | Agent                           | Tashqi                          | web_fetch so‘rovlari | SSRF bloklash                                 |
| F5                           | ClawHub                         | Agent                           | Ko‘nikma kodi                             | Moderatsiya, skanerlash                       |
| 1. F6 | 2. Agent | 3. Kanal | 4. Javoblar        | 5. Chiqishni filtrlash |

---

## 3. ATLAS taktikasi bo‘yicha tahdid tahlili

### 3.1 Razvedka (AML.TA0002)

#### Agent endpointlarini aniqlash

| Atribut                        | Qiymat                                                                                         |
| ------------------------------ | ---------------------------------------------------------------------------------------------- |
| **ATLAS ID**                   | AML.T0006 - Faol skanerlash                                                    |
| **Tavsif**                     | Hujumchi ochiq OpenClaw shlyuzi endpointlarini skanerlaydi                                     |
| **Hujum vektori**              | Tarmoqni skanerlash, Shodan so‘rovlari, DNS enumeratsiyasi                                     |
| **Ta’sirlangan komponentlar**  | Shlyuz, ochiq API endpointlari                                                                 |
| **Joriy kamaytirish choralar** | Tailscale autentifikatsiya opsiyasi, sukut bo‘yicha loopback’ga bog‘lash                       |
| **Qoldiq xavf**                | O‘rta — ommaviy shlyuzlar aniqlanishi mumkin                                                   |
| **Tavsiyalar**                 | Xavfsiz joylashtirishni hujjatlashtirish, aniqlash endpointlariga tezlikni cheklashni qo‘shish |

#### Kanal integratsiyalarini tekshirish

| Atribut                        | Qiymat                                                                                                      |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| **ATLAS ID**                   | AML.T0006 - Faol skanerlash                                                                 |
| **Tavsif**                     | Hujumchi AI tomonidan boshqariladigan akkauntlarni aniqlash uchun xabar almashish kanallarini sinab ko‘radi |
| **Hujum vektori**              | Sinov xabarlarini yuborish, javob naqshlarini kuzatish                                                      |
| **Ta’sirlangan komponentlar**  | Barcha kanal integratsiyalari                                                                               |
| **Joriy kamaytirish choralar** | Aniq choralar yo‘q                                                                                          |
| **Qoldiq xavf**                | Past — faqat aniqlashning o‘zi cheklangan qiymatga ega                                                      |
| **Tavsiyalar**                 | Javob vaqtini tasodifiylashtirishni ko‘rib chiqing                                                          |

---

### 3.2 Dastlabki kirish (AML.TA0004)

#### T-ACCESS-001: Juftlash kodi tutib olinishi

| Atribut                 | Qiymat                                                            |
| ----------------------- | ----------------------------------------------------------------- |
| **ATLAS ID**            | AML.T0040 - AI model inferensiyasi API’ga kirish  |
| **Tavsif**              | Hujumchi 30 soniyalik imtiyoz davrida juftlash kodini tutib oladi |
| **Attack Vector**       | Shoulder surfing, network sniffing, social engineering            |
| **Affected Components** | Device pairing system                                             |
| **Current Mitigations** | 30s expiry, codes sent via existing channel                       |
| **Residual Risk**       | Medium - Grace period exploitable                                 |
| **Recommendations**     | Reduce grace period, add confirmation step                        |

#### T-ACCESS-002: AllowFrom Spoofing

| Attribute               | Value                                                                          |
| ----------------------- | ------------------------------------------------------------------------------ |
| **ATLAS ID**            | AML.T0040 - AI Model Inference API Access                      |
| **Description**         | Attacker spoofs allowed sender identity in channel                             |
| **Attack Vector**       | Depends on channel - phone number spoofing, username impersonation             |
| **Affected Components** | AllowFrom validation per channel                                               |
| **Current Mitigations** | Channel-specific identity verification                                         |
| **Residual Risk**       | Medium - Some channels vulnerable to spoofing                                  |
| **Recommendations**     | Document channel-specific risks, add cryptographic verification where possible |

#### T-ACCESS-003: Token Theft

| Attribute               | Value                                                                    |
| ----------------------- | ------------------------------------------------------------------------ |
| **ATLAS ID**            | AML.T0040 - AI Model Inference API Access                |
| **Description**         | Attacker steals authentication tokens from config files                  |
| **Attack Vector**       | Malware, unauthorized device access, config backup exposure              |
| **Affected Components** | ~/.openclaw/credentials/, config storage |
| **Current Mitigations** | File permissions                                                         |
| **Residual Risk**       | High - Tokens stored in plaintext                                        |
| **Recommendations**     | Implement token encryption at rest, add token rotation                   |

---

### 3.3 Execution (AML.TA0005)

#### T-EXEC-001: Direct Prompt Injection

| Attribute               | Value                                                                                        |
| ----------------------- | -------------------------------------------------------------------------------------------- |
| **ATLAS ID**            | AML.T0051.000 - LLM Prompt Injection: Direct |
| **Description**         | Attacker sends crafted prompts to manipulate agent behavior                                  |
| **Attack Vector**       | Channel messages containing adversarial instructions                                         |
| **Affected Components** | Agent LLM, all input surfaces                                                                |
| **Current Mitigations** | Pattern detection, external content wrapping                                                 |
| **Residual Risk**       | Critical - Detection only, no blocking; sophisticated attacks bypass                         |
| **Recommendations**     | Implement multi-layer defense, output validation, user confirmation for sensitive actions    |

#### T-EXEC-002: Indirect Prompt Injection

| Attribute               | Value                                                                                          |
| ----------------------- | ---------------------------------------------------------------------------------------------- |
| **ATLAS ID**            | AML.T0051.001 - LLM Prompt Injection: Indirect |
| **Description**         | Attacker embeds malicious instructions in fetched content                                      |
| **Attack Vector**       | Malicious URLs, poisoned emails, compromised webhooks                                          |
| **Affected Components** | web_fetch, email ingestion, external data sources                         |
| **Current Mitigations** | Content wrapping with XML tags and security notice                                             |
| **Residual Risk**       | High - LLM may ignore wrapper instructions                                                     |
| **Recommendations**     | Implement content sanitization, separate execution contexts                                    |

#### T-EXEC-003: Tool Argument Injection

| Attribute               | Value                                                                                        |
| ----------------------- | -------------------------------------------------------------------------------------------- |
| **ATLAS ID**            | AML.T0051.000 - LLM Prompt Injection: Direct |
| **Description**         | Attacker manipulates tool arguments through prompt injection                                 |
| **Attack Vector**       | Crafted prompts that influence tool parameter values                                         |
| **Affected Components** | All tool invocations                                                                         |
| **Current Mitigations** | Exec approvals for dangerous commands                                                        |
| **Residual Risk**       | High - Relies on user judgment                                                               |
| **Recommendations**     | Implement argument validation, parameterized tool calls                                      |

#### T-EXEC-004: Exec Approval Bypass

| Attribute               | Value                                                      |
| ----------------------- | ---------------------------------------------------------- |
| **ATLAS ID**            | AML.T0043 - Craft Adversarial Data         |
| **Description**         | Attacker crafts commands that bypass approval allowlist    |
| **Attack Vector**       | Command obfuscation, alias exploitation, path manipulation |
| **Affected Components** | exec-approvals.ts, command allowlist       |
| **Current Mitigations** | Allowlist + ask mode                                       |
| **Residual Risk**       | High - No command sanitization                             |
| **Recommendations**     | Implement command normalization, expand blocklist          |

---

### 3.4 Persistence (AML.TA0006)

#### T-PERSIST-001: Malicious Skill Installation

| Attribute               | Value                                                                                                |
| ----------------------- | ---------------------------------------------------------------------------------------------------- |
| **ATLAS ID**            | AML.T0010.001 - Supply Chain Compromise: AI Software |
| **Description**         | Attacker publishes malicious skill to ClawHub                                                        |
| **Attack Vector**       | Create account, publish skill with hidden malicious code                                             |
| **Affected Components** | ClawHub, skill loading, agent execution                                                              |
| **Current Mitigations** | GitHub account age verification, pattern-based moderation flags                                      |
| **Residual Risk**       | Critical - No sandboxing, limited review                                                             |
| **Recommendations**     | VirusTotal integration (in progress), skill sandboxing, community review          |

#### T-PERSIST-002: Skill Update Poisoning

| Attribute               | Value                                                                                                |
| ----------------------- | ---------------------------------------------------------------------------------------------------- |
| **ATLAS ID**            | AML.T0010.001 - Supply Chain Compromise: AI Software |
| **Description**         | Attacker compromises popular skill and pushes malicious update                                       |
| **Attack Vector**       | Account compromise, social engineering of skill owner                                                |
| **Affected Components** | ClawHub versioning, auto-update flows                                                                |
| **Current Mitigations** | Version fingerprinting                                                                               |
| **Residual Risk**       | High - Auto-updates may pull malicious versions                                                      |
| **Recommendations**     | Implement update signing, rollback capability, version pinning                                       |

#### T-PERSIST-003: Agent Configuration Tampering

| Attribute                                                | 1. Qiymat                                                                                                |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| 2. **ATLAS ID**                   | 3. AML.T0010.002 - Ta’minot zanjiriga hujum: Ma’lumotlar |
| 4. **Tavsif**                     | 5. Hujumchi doimiy kirishni saqlab qolish uchun agent konfiguratsiyasini o‘zgartiradi                    |
| 6. **Hujum vektori**              | 7. Konfiguratsiya faylini o‘zgartirish, sozlamalarni kiritish                                            |
| 8. **Ta’sirlangan komponentlar**  | 9. Agent konfiguratsiyasi, vosita siyosatlari                                                            |
| 10. **Joriy yumshatish choralar** | 11. Fayl ruxsatlari                                                                                      |
| 12. **Qolgan xavf**               | 13. O‘rta - Mahalliy kirishni talab qiladi                                                               |
| 14. **Tavsiyalar**                | 15. Konfiguratsiya yaxlitligini tekshirish, konfiguratsiya o‘zgarishlari uchun audit jurnallari          |

---

### 16. 3.5 Himoyadan chetlab o‘tish (AML.TA0007)

#### T-EVADE-001: Moderation Pattern Bypass

| 18. Atribut                       | 19. Qiymat                                                                                                 |
| -------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| 20. **ATLAS ID**                  | 21. AML.T0043 - Qarama-qarshi ma’lumotlarni yaratish                                       |
| 22. **Tavsif**                    | 23. Hujumchi moderatsiya andozalaridan qochish uchun ko‘nikma mazmunini yaratadi                           |
| 24. **Hujum vektori**             | 25. Unicode gomogliflari, kodlash hiylalari, dinamik yuklash                                               |
| 26. **Ta’sirlangan komponentlar** | 27. ClawHub moderation.ts                                                                  |
| 28. **Joriy yumshatish choralar** | 29. Andozaga asoslangan FLAG_RULES                                                    |
| 30. **Qolgan xavf**               | 31. Yuqori - Oddiy regex osonlikcha chetlab o‘tiladi                                                       |
| 32. **Tavsiyalar**                | 33. Xulq-atvor tahlilini qo‘shish (VirusTotal Code Insight), AST-ga asoslangan aniqlash |

#### 34. T-EVADE-002: Kontent o‘ramidan chiqib ketish

| 35. Atribut                       | 36. Qiymat                                                                                 |
| -------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| 37. **ATLAS ID**                  | 38. AML.T0043 - Qarama-qarshi ma’lumotlarni yaratish                       |
| 39. **Tavsif**                    | 40. Hujumchi XML o‘rami kontekstidan chiqib ketadigan kontentni yaratadi                   |
| 41. **Hujum vektori**             | 42. Teglarni manipulyatsiya qilish, kontekstni chalkashtirish, ko‘rsatmalarni bekor qilish |
| 43. **Ta’sirlangan komponentlar** | 44. Tashqi kontentni o‘rash                                                                |
| 45. **Joriy yumshatish choralar** | 46. XML teglari + xavfsizlik eslatmasi                                                     |
| 47. **Qolgan xavf**               | 48. O‘rta - Yangi chetlab o‘tish usullari muntazam ravishda aniqlanadi                     |
| 49. **Tavsiyalar**                | 50. Bir nechta o‘ram qatlamlari, chiqish tomonida tekshirish                               |

---

### 3.6 Discovery (AML.TA0008)

#### T-DISC-001: Tool Enumeration

| Attribute               | Value                                                     |
| ----------------------- | --------------------------------------------------------- |
| **ATLAS ID**            | AML.T0040 - AI Model Inference API Access |
| **Description**         | Attacker enumerates available tools through prompting     |
| **Attack Vector**       | "What tools do you have?" style queries                   |
| **Affected Components** | Agent tool registry                                       |
| **Current Mitigations** | None specific                                             |
| **Residual Risk**       | Low - Tools generally documented                          |
| **Recommendations**     | Consider tool visibility controls                         |

#### T-DISC-002: Session Data Extraction

| Attribute               | Value                                                     |
| ----------------------- | --------------------------------------------------------- |
| **ATLAS ID**            | AML.T0040 - AI Model Inference API Access |
| **Description**         | Attacker extracts sensitive data from session context     |
| **Attack Vector**       | "What did we discuss?" queries, context probing           |
| **Affected Components** | Session transcripts, context window                       |
| **Current Mitigations** | Session isolation per sender                              |
| **Residual Risk**       | Medium - Within-session data accessible                   |
| **Recommendations**     | Implement sensitive data redaction in context             |

---

### 3.7 Collection & Exfiltration (AML.TA0009, AML.TA0010)

#### T-EXFIL-001: Data Theft via web_fetch

| Attribute               | Value                                                                  |
| ----------------------- | ---------------------------------------------------------------------- |
| **ATLAS ID**            | AML.T0009 - Collection                                 |
| **Description**         | Attacker exfiltrates data by instructing agent to send to external URL |
| **Attack Vector**       | Prompt injection causing agent to POST data to attacker server         |
| **Affected Components** | web_fetch tool                                    |
| **Current Mitigations** | SSRF blocking for internal networks                                    |
| **Residual Risk**       | High - External URLs permitted                                         |
| **Recommendations**     | Implement URL allowlisting, data classification awareness              |

#### T-EXFIL-002: Unauthorized Message Sending

| Attribute               | Value                                                            |
| ----------------------- | ---------------------------------------------------------------- |
| **ATLAS ID**            | AML.T0009 - Collection                           |
| **Description**         | Attacker causes agent to send messages containing sensitive data |
| **Attack Vector**       | Prompt injection causing agent to message attacker               |
| **Affected Components** | Message tool, channel integrations                               |
| **Current Mitigations** | Outbound messaging gating                                        |
| **Residual Risk**       | Medium - Gating may be bypassed                                  |
| **Recommendations**     | Require explicit confirmation for new recipients                 |

#### T-EXFIL-003: Credential Harvesting

| Attribute               | Value                                                   |
| ----------------------- | ------------------------------------------------------- |
| **ATLAS ID**            | AML.T0009 - Collection                  |
| **Description**         | Malicious skill harvests credentials from agent context |
| **Attack Vector**       | Skill code reads environment variables, config files    |
| **Affected Components** | Skill execution environment                             |
| **Current Mitigations** | None specific to skills                                 |
| **Residual Risk**       | Critical - Skills run with agent privileges             |
| **Recommendations**     | Skill sandboxing, credential isolation                  |

---

### 3.8 Impact (AML.TA0011)

#### T-IMPACT-001: Unauthorized Command Execution

| Attribute               | Value                                                |
| ----------------------- | ---------------------------------------------------- |
| **ATLAS ID**            | AML.T0031 - Erode AI Model Integrity |
| **Description**         | Attacker executes arbitrary commands on user system  |
| **Attack Vector**       | Prompt injection combined with exec approval bypass  |
| **Affected Components** | Bash tool, command execution                         |
| **Current Mitigations** | Exec approvals, Docker sandbox option                |
| **Residual Risk**       | Critical - Host execution without sandbox            |
| **Recommendations**     | Default to sandbox, improve approval UX              |

#### T-IMPACT-002: Resource Exhaustion (DoS)

| Attribute               | Value                                                |
| ----------------------- | ---------------------------------------------------- |
| **ATLAS ID**            | AML.T0031 - Erode AI Model Integrity |
| **Description**         | Attacker exhausts API credits or compute resources   |
| **Attack Vector**       | Automated message flooding, expensive tool calls     |
| **Affected Components** | Gateway, agent sessions, API provider                |
| **Current Mitigations** | None                                                 |
| **Residual Risk**       | High - No rate limiting                              |
| **Recommendations**     | Implement per-sender rate limits, cost budgets       |

#### T-IMPACT-003: Reputation Damage

| Attribute               | Value                                                   |
| ----------------------- | ------------------------------------------------------- |
| **ATLAS ID**            | AML.T0031 - Erode AI Model Integrity    |
| **Description**         | Attacker causes agent to send harmful/offensive content |
| **Attack Vector**       | Prompt injection causing inappropriate responses        |
| **Affected Components** | Output generation, channel messaging                    |
| **Current Mitigations** | LLM provider content policies                           |
| **Residual Risk**       | Medium - Provider filters imperfect                     |
| **Recommendations**     | Output filtering layer, user controls                   |

---

## 4. ClawHub Supply Chain Analysis

### 4.1 Current Security Controls

| Control                           | Implementation                                                   | Effectiveness                                        |
| --------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------- |
| GitHub Account Age                | `requireGitHubAccountAge()`                                      | Medium - Raises bar for new attackers                |
| Path Sanitization                 | `sanitizePath()`                                                 | High - Prevents path traversal                       |
| File Type Validation              | `isTextFile()`                                                   | Medium - Only text files, but can still be malicious |
| Size Limits                       | 50MB total bundle                                                | High - Prevents resource exhaustion                  |
| Required SKILL.md | Mandatory readme                                                 | Low security value - Informational only              |
| Pattern Moderation                | FLAG_RULES in moderation.ts | Low - Easily bypassed                                |
| Moderation Status                 | `moderationStatus` field                                         | Medium - Manual review possible                      |

### 4.2 Moderation Flag Patterns

Current patterns in `moderation.ts`:

```javascript
// Known-bad identifiers
/(keepcold131\/ClawdAuthenticatorTool|ClawdAuthenticatorTool)/i

// Suspicious keywords
/(malware|stealer|phish|phishing|keylogger)/i
/(api[-_ ]?key|token|password|private key|secret)/i
/(wallet|seed phrase|mnemonic|crypto)/i
/(discord\.gg|webhook|hooks\.slack)/i
/(curl[^\n]+\|\s*(sh|bash))/i
/(bit\.ly|tinyurl\.com|t\.co|goo\.gl|is\.gd)/i
```

**Limitations:**

- Only checks slug, displayName, summary, frontmatter, metadata, file paths
- Does not analyze actual skill code content
- Simple regex easily bypassed with obfuscation
- No behavioral analysis

### 4.3 Planned Improvements

| Improvement            | Status                                                   | Impact                                                                |
| ---------------------- | -------------------------------------------------------- | --------------------------------------------------------------------- |
| VirusTotal Integration | In Progress                                              | High - Code Insight behavioral analysis                               |
| Community Reporting    | Partial (`skillReports` table exists) | Medium                                                                |
| Audit Logging          | Partial (`auditLogs` table exists)    | Medium                                                                |
| Badge System           | Implemented                                              | Medium - `highlighted`, `official`, `deprecated`, `redactionApproved` |

---

## 5. Risk Matrix

### 5.1 Likelihood vs Impact

| Threat ID                               | Likelihood                      | Impact                            | Risk Level                           | Priority                      |
| --------------------------------------- | ------------------------------- | --------------------------------- | ------------------------------------ | ----------------------------- |
| T-EXEC-001                              | High                            | Kritik                            | **Kritik**                           | P0                            |
| T-PERSIST-001                           | Yuqori                          | Kritik                            | **Kritik**                           | P0                            |
| T-EXFIL-003                             | O‘rta                           | Kritik                            | **Kritik**                           | P0                            |
| T-IMPACT-001                            | O‘rta                           | Kritik                            | **Yuqori**                           | P1                            |
| T-EXEC-002                              | Yuqori                          | Yuqori                            | **Yuqori**                           | P1                            |
| T-EXEC-004                              | O‘rta                           | Yuqori                            | **Yuqori**                           | P1                            |
| T-ACCESS-003                            | O‘rta                           | Yuqori                            | **Yuqori**                           | P1                            |
| T-EXFIL-001                             | O‘rta                           | Yuqori                            | **Yuqori**                           | P1                            |
| T-IMPACT-002                            | Yuqori                          | O‘rta                             | **Yuqori**                           | P1                            |
| T-EVADE-001                             | Yuqori                          | O‘rta                             | **O‘rta**                            | P2                            |
| T-ACCESS-001                            | Past                            | 1. Yuqori  | 2. **O‘rta**  | 3. P2  |
| 4. T-ACCESS-002  | 5. Past  | 6. Yuqori  | 7. **O‘rta**  | 8. P2  |
| 9. T-PERSIST-002 | 10. Past | 11. Yuqori | 12. **O‘rta** | 13. P2 |

### 14. 5.2 Muhim yo‘l hujum zanjirlari

15. **Hujum zanjiri 1: Ko‘nikmaga asoslangan ma’lumot o‘g‘irlash**

```
16. T-PERSIST-001 → T-EVADE-001 → T-EXFIL-003
(Zararli skillni e’lon qilish) → (Moderatsiyani chetlab o‘tish) → (Hisob ma’lumotlarini yig‘ish)
```

17. **Hujum zanjiri 2: Prompt Injection orqali RCE**

```
18. T-EXEC-001 → T-EXEC-004 → T-IMPACT-001
(Prompt kiritish) → (Ijroni tasdiqlashni chetlab o‘tish) → (Buyruqlarni bajarish)
```

19. **Hujum zanjiri 3: Olib kelingan kontent orqali bilvosita injection**

```
20. T-EXEC-002 → T-EXFIL-001 → Tashqi exfiltratsiya
(URL kontentini zaharlash) → (Agent kontentni olib ko‘rsatmalarga amal qiladi) → (Ma’lumotlar hujumchiga yuboriladi)
```

---

## 21. 6. 22. Tavsiyalar qisqacha mazmuni

### 23. 6.1 Zudlik bilan (P0)

| 24. ID    | 25. Tavsiya                                            | 26. Qamrab oladi               |
| -------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------- |
| 27. R-001 | 28. VirusTotal integratsiyasini to‘liq yakunlash       | 29. T-PERSIST-001, T-EVADE-001 |
| 30. R-002 | 31. Skill sandboxingni joriy etish                     | 32. T-PERSIST-001, T-EXFIL-003 |
| 33. R-003 | 34. Sezgir amallar uchun chiqish tekshiruvini qo‘shish | 35. T-EXEC-001, T-EXEC-002     |

### 36. 6.2 Qisqa muddatli (P1)

| 37. ID    | 38. Tavsiya                                                             | 39. Qamrab oladi |
| -------------------------------- | ---------------------------------------------------------------------------------------------- | --------------------------------------- |
| 40. R-004 | 41. Tezlikni cheklashni joriy etish                                     | 42. T-IMPACT-002 |
| 43. R-005 | 44. Tokenlarni saqlashda shifrlashni qo‘shish                           | 45. T-ACCESS-003 |
| 46. R-006 | 47. Ijro tasdiqlash UX va tekshiruvini yaxshilash                       | 48. T-EXEC-004   |
| 49. R-007 | 50. web_fetch uchun URL allowlistingni joriy etish | T-EXFIL-001                             |

### 6.3 O‘rta muddatli (P2)

| ID    | Tavsiya                                                      | Qamrab oladi  |
| ----- | ------------------------------------------------------------ | ------------- |
| R-008 | Imkon qadar kriptografik kanal tekshiruvini qo‘shing         | T-ACCESS-002  |
| R-009 | Konfiguratsiya yaxlitligini tekshirishni joriy eting         | T-PERSIST-003 |
| R-010 | Yangilanishlarni imzolash va versiyani mahkamlashni qo‘shing | T-PERSIST-002 |

---

## 7. Ilovalar

### 7.1 ATLAS texnikalarini moslashtirish

| ATLAS ID                                      | Texnika nomi                                               | OpenClaw tahdidlari                                              |
| --------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------------- |
| AML.T0006                     | Faol skanerlash                                            | T-RECON-001, T-RECON-002                                         |
| AML.T0009                     | Yig‘ish                                                    | T-EXFIL-001, T-EXFIL-002, T-EXFIL-003                            |
| AML.T0010.001 | Ta’minot zanjiri: AI dasturiy ta’minoti    | T-PERSIST-001, T-PERSIST-002                                     |
| AML.T0010.002 | Ta’minot zanjiri: Ma’lumotlar              | T-PERSIST-003                                                    |
| AML.T0031                     | AI modeli yaxlitligini yemirish                            | T-IMPACT-001, T-IMPACT-002, T-IMPACT-003                         |
| AML.T0040                     | AI modeli inferensiyasi API’iga kirish                     | T-ACCESS-001, T-ACCESS-002, T-ACCESS-003, T-DISC-001, T-DISC-002 |
| AML.T0043                     | Adversarial ma’lumotlarni yaratish                         | T-EXEC-004, T-EVADE-001, T-EVADE-002                             |
| AML.T0051.000 | LLM prompt in’eksiyasi: To‘g‘ridan-to‘g‘ri | T-EXEC-001, T-EXEC-003                                           |
| AML.T0051.001 | LLM prompt in’eksiyasi: Bilvosita          | T-EXEC-002                                                       |

### 7.2 Asosiy xavfsizlik fayllari

| Yo‘l                                | Maqsad                                | Xavf darajasi |
| ----------------------------------- | ------------------------------------- | ------------- |
| `src/infra/exec-approvals.ts`       | Buyruqlarni tasdiqlash mantiqi        | **Kritik**    |
| `src/gateway/auth.ts`               | Gateway autentifikatsiyasi            | **Kritik**    |
| `src/web/inbound/access-control.ts` | Kanalga kirishni nazorat qilish       | **Kritik**    |
| `src/infra/net/ssrf.ts`             | SSRF himoyasi                         | **Kritik**    |
| `src/security/external-content.ts`  | Prompt inʼektsiyasini yumshatish      | **Kritik**    |
| `src/agents/sandbox/tool-policy.ts` | Asboblar siyosatini majburiy qoʻllash | **Kritik**    |
| `convex/lib/moderation.ts`          | ClawHub moderatsiyasi                 | **Yuqori**    |
| `convex/lib/skillPublish.ts`        | Skillni nashr etish jarayoni          | **Yuqori**    |
| `src/routing/resolve-route.ts`      | Sessiyani izolyatsiya qilish          | **O‘rta**     |

### 7.3 Lugʻat

| Atama                | Taʼrif                                                            |
| -------------------- | ----------------------------------------------------------------- |
| **ATLAS**            | MITRE’ning AI tizimlari uchun Adversarial Tahdidlar Landshafti    |
| **ClawHub**          | OpenClaw’ning skilllar bozori                                     |
| **Gateway**          | OpenClaw’ning xabarlarni marshrutlash va autentifikatsiya qatlami |
| **MCP**              | Model Context Protocol — asbob provayderi interfeysi              |
| **Prompt Injection** | Zararli ko‘rsatmalar kiritma ichiga joylashtiriladigan hujum      |
| **Skill**            | OpenClaw agentlari uchun yuklab olinadigan kengaytma              |
| **SSRF**             | Server tomoni so‘rovini soxtalashtirish                           |

---

_Ushbu tahdid modeli doimiy ravishda yangilanib boriladigan hujjatdir._ Xavfsizlik muammolari haqida security@openclaw.ai manziliga xabar bering
