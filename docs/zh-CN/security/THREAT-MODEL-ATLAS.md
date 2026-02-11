# 4. OpenClaw 威胁模型 v1.0

## 5. MITRE ATLAS 框架

**Version:** 1.0-draft
**Last Updated:** 2026-02-04
**Methodology:** MITRE ATLAS + Data Flow Diagrams
**Framework:** [MITRE ATLAS](https://atlas.mitre.org/) (Adversarial Threat Landscape for AI Systems)

### 框架归属

该威胁模型基于 [MITRE ATLAS](https://atlas.mitre.org/)，这是用于记录 AI/ML 系统对抗性威胁的行业标准框架。 ATLAS 由 [MITRE](https://www.mitre.org/) 与 AI 安全社区合作维护。

**ATLAS 关键资源：**

- [ATLAS 技术](https://atlas.mitre.org/techniques/)
- [ATLAS 战术](https://atlas.mitre.org/tactics/)
- [ATLAS 案例研究](https://atlas.mitre.org/studies/)
- [ATLAS GitHub](https://github.com/mitre-atlas/atlas-data)
- [参与 ATLAS 贡献](https://atlas.mitre.org/resources/contribute)

### 为本威胁模型做出贡献

这是一个由 OpenClaw 社区维护的动态文档。 请参阅 [CONTRIBUTING-THREAT-MODEL.md](./CONTRIBUTING-THREAT-MODEL.md) 了解贡献指南：

- 报告新的威胁
- 更新现有威胁
- 提出攻击链
- 建议缓解措施

---

## 1. 引言

### 1.1 目的

本威胁模型使用专为 AI/ML 系统设计的 MITRE ATLAS 框架，记录针对 OpenClaw AI 代理平台和 ClawHub 技能市场的对抗性威胁。

### 1.2 范围

| 组件                   | 包含                           | 说明                                                               |
| -------------------- | ---------------------------- | ---------------------------------------------------------------- |
| OpenClaw 代理运行时       | 是                            | 核心代理执行、工具调用、会话                                                   |
| 网关                   | 是                            | Authentication, routing, channel integration                     |
| Channel Integrations | Yes                          | WhatsApp, Telegram, Discord, Signal, Slack, etc. |
| ClawHub Marketplace  | Yes                          | Skill publishing, moderation, distribution                       |
| MCP Servers          | Yes                          | External tool providers                                          |
| User Devices         | 7. 部分 | Mobile apps, desktop clients                                     |

### 1.3 Out of Scope

Nothing is explicitly out of scope for this threat model.

---

## 2. System Architecture

### 2.1 Trust Boundaries

```
┌─────────────────────────────────────────────────────────────────┐
│                    UNTRUSTED ZONE                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  WhatsApp   │  │  Telegram   │  │   Discord   │  ...         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘              │
│         │                │                │                      │
└─────────┼────────────────┼────────────────┼──────────────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────┐
│                 TRUST BOUNDARY 1: Channel Access                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                      GATEWAY                              │   │
│  │  • Device Pairing (30s grace period)                      │   │
│  │  • AllowFrom / AllowList validation                       │   │
│  │  • Token/Password/Tailscale auth                          │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 TRUST BOUNDARY 2: Session Isolation              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   AGENT SESSIONS                          │   │
│  │  • Session key = agent:channel:peer                       │   │
│  │  • Tool policies per agent                                │   │
│  │  • Transcript logging                                     │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 TRUST BOUNDARY 3: Tool Execution                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  EXECUTION SANDBOX                        │   │
│  │  • Docker sandbox OR Host (exec-approvals)                │   │
│  │  • Node remote execution                                  │   │
│  │  • SSRF protection (DNS pinning + IP blocking)            │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 TRUST BOUNDARY 4: External Content               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              FETCHED URLs / EMAILS / WEBHOOKS             │   │
│  │  • External content wrapping (XML tags)                   │   │
│  │  • Security notice injection                              │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 TRUST BOUNDARY 5: Supply Chain                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                      CLAWHUB                              │   │
│  │  • Skill publishing (semver, SKILL.md required)           │   │
│  │  • Pattern-based moderation flags                         │   │
│  │  • VirusTotal scanning (coming soon)                      │   │
│  │  • GitHub account age verification                        │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Data Flows

| Flow | Source                            | Destination                  | Data                                    | Protection                      |
| ---- | --------------------------------- | ---------------------------- | --------------------------------------- | ------------------------------- |
| F1   | Channel                           | Gateway                      | User messages                           | TLS, AllowFrom                  |
| F2   | Gateway                           | Agent                        | Routed messages                         | Session isolation               |
| F3   | Agent                             | Tools                        | Tool invocations                        | Policy enforcement              |
| F4   | Agent                             | External                     | web_fetch requests | SSRF blocking                   |
| F5   | 8. ClawHub | Agent                        | Skill code                              | Moderation, scanning            |
| F6   | Agent                             | 9. 通道 | Responses                               | 10. 输出过滤 |

---

## 3. Threat Analysis by ATLAS Tactic

### 3.1 Reconnaissance (AML.TA0002)

#### T-RECON-001: Agent Endpoint Discovery

| Attribute               | Value                                                                |
| ----------------------- | -------------------------------------------------------------------- |
| **ATLAS ID**            | AML.T0006 - Active Scanning                          |
| **Description**         | Attacker scans for exposed OpenClaw gateway endpoints                |
| **Attack Vector**       | Network scanning, shodan queries, DNS enumeration                    |
| **Affected Components** | Gateway, exposed API endpoints                                       |
| **Current Mitigations** | Tailscale auth option, bind to loopback by default                   |
| **Residual Risk**       | Medium - Public gateways discoverable                                |
| **Recommendations**     | Document secure deployment, add rate limiting on discovery endpoints |

#### T-RECON-002: Channel Integration Probing

| Attribute               | Value                                                              |
| ----------------------- | ------------------------------------------------------------------ |
| **ATLAS ID**            | AML.T0006 - Active Scanning                        |
| **Description**         | Attacker probes messaging channels to identify AI-managed accounts |
| **Attack Vector**       | Sending test messages, observing response patterns                 |
| **Affected Components** | All channel integrations                                           |
| **Current Mitigations** | None specific                                                      |
| **Residual Risk**       | Low - Limited value from discovery alone                           |
| **Recommendations**     | Consider response timing randomization                             |

---

### 3.2 Initial Access (AML.TA0004)

#### T-ACCESS-001: Pairing Code Interception

| Attribute               | Value                                                     |
| ----------------------- | --------------------------------------------------------- |
| **ATLAS ID**            | AML.T0040 - AI Model Inference API Access |
| **Description**         | Attacker intercepts pairing code during 30s grace period  |
| **Attack Vector**       | Shoulder surfing, network sniffing, social engineering    |
| **Affected Components** | 11. 设备配对系统                         |
| **Current Mitigations** | 30s expiry, codes sent via existing channel               |
| **Residual Risk**       | Medium - Grace period exploitable                         |
| **Recommendations**     | Reduce grace period, add confirmation step                |

#### T-ACCESS-002: AllowFrom Spoofing

| Attribute               | Value                                                              |
| ----------------------- | ------------------------------------------------------------------ |
| **ATLAS ID**            | AML.T0040 - AI Model Inference API Access          |
| **Description**         | Attacker spoofs allowed sender identity in channel                 |
| **Attack Vector**       | Depends on channel - phone number spoofing, username impersonation |
| **Affected Components** | AllowFrom validation per channel                                   |
| **Current Mitigations** | Channel-specific identity verification                             |
| **Residual Risk**       | Medium - Some channels vulnerable to spoofing                      |
| **Recommendations**     | 12. 记录特定通道的风险，并在可能的情况下添加加密验证                |

#### T-ACCESS-003: Token Theft

| Attribute                         | 13. 价值                                            |
| --------------------------------- | ------------------------------------------------------------------------ |
| **ATLAS ID**                      | AML.T0040 - AI Model Inference API Access                |
| 14. **描述** | Attacker steals authentication tokens from config files                  |
| **Attack Vector**                 | Malware, unauthorized device access, config backup exposure              |
| **Affected Components**           | ~/.openclaw/credentials/, config storage |
| **Current Mitigations**           | File permissions                                                         |
| **Residual Risk**                 | High - Tokens stored in plaintext                                        |
| **Recommendations**               | Implement token encryption at rest, add token rotation                   |

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
| **Attack Vector**       | 15. 恶意 URL、被投毒的电子邮件、被入侵的 Webhook                                        |
| **Affected Components** | web_fetch, email ingestion, external data sources                         |
| **Current Mitigations** | 16. 使用 XML 标签进行内容封装并添加安全提示                                              |
| **Residual Risk**       | High - LLM may ignore wrapper instructions                                                     |
| **Recommendations**     | Implement content sanitization, separate execution contexts                                    |

#### 17. T-EXEC-003：工具参数注入

| 18. 属性 | Value                                                                                        |
| ----------------------------- | -------------------------------------------------------------------------------------------- |
| **ATLAS ID**                  | AML.T0051.000 - LLM Prompt Injection: Direct |
| **Description**               | Attacker manipulates tool arguments through prompt injection                                 |
| **Attack Vector**             | Crafted prompts that influence tool parameter values                                         |
| **Affected Components**       | All tool invocations                                                                         |
| **Current Mitigations**       | Exec approvals for dangerous commands                                                        |
| **Residual Risk**             | High - Relies on user judgment                                                               |
| **Recommendations**           | Implement argument validation, parameterized tool calls                                      |

#### T-EXEC-004: Exec Approval Bypass

| Attribute    | Value                                                               |
| ------------ | ------------------------------------------------------------------- |
| **ATLAS ID** | AML.T0043 - 构造对抗性数据                                 |
| **描述**       | 攻击者构造绕过审批允许列表的命令                                                    |
| **攻击向量**     | 命令混淆、别名利用、路径操纵                                                      |
| **受影响组件**    | 19. exec-approvals.ts，命令允许列表 |
| **当前缓解措施**   | 允许列表 + 询问模式                                                         |
| **残余风险**     | 高 - 无命令净化                                                           |
| **建议**       | 实现命令规范化，扩展阻止列表                                                      |

---

### 20. 3.4 持久化（AML.TA0006）

#### T-PERSIST-001：恶意技能安装

| 属性           | 值                                                           |
| ------------ | ----------------------------------------------------------- |
| **ATLAS ID** | AML.T0010.001 - 供应链入侵：AI 软件 |
| **描述**       | 攻击者向 ClawHub 发布恶意技能                                         |
| **攻击向量**     | 创建账户，发布包含隐藏恶意代码的技能                                          |
| **受影响组件**    | ClawHub，技能加载，代理执行                                           |
| **当前缓解措施**   | 21. GitHub 账号年龄验证、基于模式的审核标记          |
| **残余风险**     | 严重 - 无沙箱，审查有限                                               |
| **建议**       | VirusTotal 集成（进行中），技能沙箱化，社区审查                               |

#### T-PERSIST-002：技能更新投毒

| 属性           | 值                                                           |
| ------------ | ----------------------------------------------------------- |
| **ATLAS ID** | AML.T0010.001 - 供应链入侵：AI 软件 |
| **描述**       | 攻击者入侵热门技能并推送恶意更新                                            |
| **攻击向量**     | 账户入侵，对技能所有者的社会工程                                            |
| **受影响组件**    | ClawHub 版本管理，自动更新流程                                         |
| **当前缓解措施**   | 版本指纹识别                                                      |
| **残余风险**     | 高 - 自动更新可能拉取恶意版本                                            |
| **建议**       | 实现更新签名、回滚能力、版本固定                                            |

#### T-PERSIST-003：代理配置篡改

| 属性                                    | Value                                                                                         |
| ------------------------------------- | --------------------------------------------------------------------------------------------- |
| **ATLAS ID**                          | AML.T0010.002 - Supply Chain Compromise: Data |
| **Description**                       | Attacker modifies agent configuration to persist access                                       |
| **Attack Vector**                     | Config file modification, settings injection                                                  |
| **Affected Components**               | Agent config, tool policies                                                                   |
| 22. **当前缓解措施** | File permissions                                                                              |
| **Residual Risk**                     | Medium - Requires local access                                                                |
| **Recommendations**                   | Config integrity verification, audit logging for config changes                               |

---

### 3.5 Defense Evasion (AML.TA0007)

#### T-EVADE-001: Moderation Pattern Bypass

| Attribute               | Value                                                                                     |
| ----------------------- | ----------------------------------------------------------------------------------------- |
| **ATLAS ID**            | AML.T0043 - Craft Adversarial Data                                        |
| **Description**         | Attacker crafts skill content to evade moderation patterns                                |
| **Attack Vector**       | Unicode homoglyphs, encoding tricks, dynamic loading                                      |
| **Affected Components** | ClawHub moderation.ts                                                     |
| **Current Mitigations** | Pattern-based FLAG_RULES                                             |
| **Residual Risk**       | High - Simple regex easily bypassed                                                       |
| **Recommendations**     | Add behavioral analysis (VirusTotal Code Insight), AST-based detection |

#### T-EVADE-002: Content Wrapper Escape

| Attribute               | Value                                                          |
| ----------------------- | -------------------------------------------------------------- |
| **ATLAS ID**            | 23. AML.T0043 - 构造对抗性数据 |
| **Description**         | Attacker crafts content that escapes XML wrapper context       |
| **Attack Vector**       | Tag manipulation, context confusion, instruction override      |
| **Affected Components** | External content wrapping                                      |
| **Current Mitigations** | XML tags + security notice                                     |
| **Residual Risk**       | Medium - Novel escapes discovered regularly                    |
| **Recommendations**     | Multiple wrapper layers, output-side validation                |

---

### 1. 3.6 发现（AML.TA0008）

#### 2. T-DISC-001：工具枚举

| 3. 属性           | 4. 值                                          |
| -------------------------------------- | -------------------------------------------------------------------- |
| 5. **ATLAS ID** | 6. AML.T0040 - AI 模型推理 API 访问 |
| 7. **描述**       | 8. 攻击者通过提示来枚举可用工具                             |
| 9. **攻击向量**     | 10. “你有哪些工具？”风格的查询                            |
| 11. **受影响的组件**  | 12. Agent 工具注册表                               |
| 13. **当前缓解措施**  | 14. 无特定措施                                     |
| 15. **剩余风险**    | 16. 低 - 工具通常已有文档说明                            |
| 17. **建议**      | 18. 考虑实施工具可见性控制                               |

#### 19. T-DISC-002：会话数据提取

| 20. 属性           | 21. 值                                          |
| --------------------------------------- | --------------------------------------------------------------------- |
| 22. **ATLAS ID** | 23. AML.T0040 - AI 模型推理 API 访问 |
| 24. **描述**       | 25. 攻击者从会话上下文中提取敏感数据                           |
| 26. **攻击向量**     | 27. “我们讨论了什么？”类查询，上下文探测                        |
| 28. **受影响的组件**   | 29. 会话记录、上下文窗口                                 |
| 30. **当前缓解措施**   | 31. 按发送方进行会话隔离                                 |
| 32. **剩余风险**     | 33. 中 - 会话内数据可被访问                              |
| 25. **建议**       | 35. 在上下文中实施敏感数据脱敏                              |

---

### 36. 3.7 收集与外泄（AML.TA0009, AML.TA0010）

#### 37. T-EXFIL-001：通过 web_fetch 进行数据窃取

| 38. 属性           | 39. 值                                 |
| --------------------------------------- | ------------------------------------------------------------ |
| 40. **ATLAS ID** | 41. AML.T0009 - 收集    |
| 42. **描述**       | 43. 攻击者指示 Agent 将数据发送到外部 URL 以实现外泄    |
| 44. **攻击向量**     | 26. 提示注入导致代理向攻击者服务器 POST 数据           |
| 46. **受影响的组件**   | 47. web_fetch 工具 |
| 48. **当前缓解措施**   | 49. 对内部网络的 SSRF 阻断                    |
| 50. **剩余风险**     | 高 - 允许外部 URL                                                 |
| **建议**                                  | 实施 URL 允许列表，数据分类意识                                           |

#### T-EXFIL-002：未授权消息发送

| 属性           | 值                                    |
| ------------ | ------------------------------------ |
| **ATLAS ID** | AML.T0009 - 收集       |
| **描述**       | 攻击者导致代理发送包含敏感数据的消息                   |
| **攻击向量**     | 提示注入导致代理向攻击者发送消息                     |
| **受影响组件**    | 27. 消息工具、通道集成 |
| **当前缓解措施**   | 28. 出站消息门控    |
| **残余风险**     | 中等 - 门控可能被绕过                         |
| **建议**       | 对新收件人要求明确确认                          |

#### T-EXFIL-003：凭据收集

| 属性           | 值                              |
| ------------ | ------------------------------ |
| **ATLAS ID** | AML.T0009 - 收集 |
| **描述**       | 恶意技能从代理上下文中收集凭据                |
| **攻击向量**     | 技能代码读取环境变量、配置文件                |
| **受影响组件**    | 技能执行环境                         |
| **当前缓解措施**   | 无针对技能的特定措施                     |
| **残余风险**     | 严重 - 技能以代理权限运行                 |
| **建议**       | 技能沙箱化，凭据隔离                     |

---

### 3.8 影响（AML.TA0011）

#### T-IMPACT-001：未授权命令执行

| 属性                  | 值                                         |
| ------------------- | ----------------------------------------- |
| **ATLAS ID**        | AML.T0031 - 侵蚀 AI 模型完整性   |
| **描述**              | 攻击者在用户系统上执行任意命令                           |
| **攻击向量**            | 提示注入与 exec 审批绕过相结合                        |
| **受影响组件**           | Bash 工具，命令执行                              |
| **当前缓解措施**          | Exec approvals, Docker sandbox option     |
| **Residual Risk**   | Critical - Host execution without sandbox |
| **Recommendations** | Default to sandbox, improve approval UX   |

#### T-IMPACT-002: Resource Exhaustion (DoS)

| Attribute               | Value                                                |
| ----------------------- | ---------------------------------------------------- |
| **ATLAS ID**            | AML.T0031 - Erode AI Model Integrity |
| **Description**         | Attacker exhausts API credits or compute resources   |
| **Attack Vector**       | Automated message flooding, expensive tool calls     |
| **Affected Components** | 29. 网关、代理会话、API 提供方           |
| **Current Mitigations** | None                                                 |
| **Residual Risk**       | High - No rate limiting                              |
| **Recommendations**     | Implement per-sender rate limits, cost budgets       |

#### T-IMPACT-003: Reputation Damage

| Attribute               | Value                                                              |
| ----------------------- | ------------------------------------------------------------------ |
| **ATLAS ID**            | 30. AML.T0031 - 侵蚀 AI 模型完整性 |
| **Description**         | Attacker causes agent to send harmful/offensive content            |
| **Attack Vector**       | Prompt injection causing inappropriate responses                   |
| **Affected Components** | Output generation, channel messaging                               |
| **Current Mitigations** | LLM provider content policies                                      |
| **Residual Risk**       | Medium - Provider filters imperfect                                |
| **Recommendations**     | Output filtering layer, user controls                              |

---

## 4. ClawHub Supply Chain Analysis

### 4.1 Current Security Controls

| Control                           | Implementation                                                                              | Effectiveness                                        |
| --------------------------------- | ------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| GitHub Account Age                | `requireGitHubAccountAge()`                                                                 | Medium - Raises bar for new attackers                |
| Path Sanitization                 | `sanitizePath()`                                                                            | High - Prevents path traversal                       |
| File Type Validation              | 31. `isTextFile()`                                                   | Medium - Only text files, but can still be malicious |
| Size Limits                       | 50MB total bundle                                                                           | 32. 高 - 防止资源耗尽                |
| Required SKILL.md | Mandatory readme                                                                            | 33. 低安全价值 - 仅供信息参考            |
| 34. 模式审核   | 35. moderation.ts 中的 FLAG_RULES | 36. 低 - 容易被绕过                 |
| Moderation Status                 | `moderationStatus` field                                                                    | Medium - Manual review possible                      |

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

37. **限制：**

- Only checks slug, displayName, summary, frontmatter, metadata, file paths
- Does not analyze actual skill code content
- Simple regex easily bypassed with obfuscation
- No behavioral analysis

### 4.3 Planned Improvements

| Improvement                     | Status                                                   | Impact                                                                |
| ------------------------------- | -------------------------------------------------------- | --------------------------------------------------------------------- |
| VirusTotal Integration          | In Progress                                              | High - Code Insight behavioral analysis                               |
| Community Reporting             | Partial (`skillReports` table exists) | Medium                                                                |
| 38. 审计日志 | Partial (`auditLogs` table exists)    | Medium                                                                |
| Badge System                    | Implemented                                              | Medium - `highlighted`, `official`, `deprecated`, `redactionApproved` |

---

## 5. Risk Matrix

### 5.1 Likelihood vs Impact

| Threat ID     | Likelihood | Impact                        | Risk Level   | Priority |
| ------------- | ---------- | ----------------------------- | ------------ | -------- |
| T-EXEC-001    | High       | 39. 严重 | **Critical** | P0       |
| T-PERSIST-001 | High       | Critical                      | **Critical** | P0       |
| T-EXFIL-003   | Medium     | Critical                      | **Critical** | P0       |
| T-IMPACT-001  | Medium     | Critical                      | **High**     | P1       |
| T-EXEC-002    | High       | 40. 高  | **High**     | P1       |
| T-EXEC-004    | Medium     | High                          | **High**     | P1       |
| T-ACCESS-003  | Medium     | High                          | **High**     | P1       |
| T-EXFIL-001   | Medium     | High                          | **High**     | P1       |
| T-IMPACT-002  | High       | Medium                        | **High**     | P1       |
| T-EVADE-001   | High       | Medium                        | **Medium**   | P2       |
| T-ACCESS-001  | Low        | High                          | **Medium**   | P2       |
| T-ACCESS-002  | Low        | High                          | **Medium**   | P2       |
| T-PERSIST-002 | Low        | High                          | **Medium**   | P2       |

### 5.2 Critical Path Attack Chains

**Attack Chain 1: Skill-Based Data Theft**

```
T-PERSIST-001 → T-EVADE-001 → T-EXFIL-003
(Publish malicious skill) → (Evade moderation) → (Harvest credentials)
```

**Attack Chain 2: Prompt Injection to RCE**

```
T-EXEC-001 → T-EXEC-004 → T-IMPACT-001
(Inject prompt) → (Bypass exec approval) → (Execute commands)
```

**Attack Chain 3: Indirect Injection via Fetched Content**

```
T-EXEC-002 → T-EXFIL-001 → External exfiltration
(Poison URL content) → (Agent fetches & follows instructions) → (Data sent to attacker)
```

---

## 6. Recommendations Summary

### 6.1 Immediate (P0)

| ID    | Recommendation                              | Addresses                  |
| ----- | ------------------------------------------- | -------------------------- |
| R-001 | Complete VirusTotal integration             | T-PERSIST-001, T-EVADE-001 |
| R-002 | Implement skill sandboxing                  | T-PERSIST-001, T-EXFIL-003 |
| R-003 | Add output validation for sensitive actions | T-EXEC-001, T-EXEC-002     |

### 6.2 Short-term (P1)

| ID    | Recommendation                                                | Addresses    |
| ----- | ------------------------------------------------------------- | ------------ |
| R-004 | Implement rate limiting                                       | T-IMPACT-002 |
| R-005 | Add token encryption at rest                                  | T-ACCESS-003 |
| R-006 | Improve exec approval UX and validation                       | T-EXEC-004   |
| R-007 | Implement URL allowlisting for web_fetch | T-EXFIL-001  |

### 6.3 Medium-term (P2)

| ID    | Recommendation                                        | Addresses     |
| ----- | ----------------------------------------------------- | ------------- |
| R-008 | Add cryptographic channel verification where possible | T-ACCESS-002  |
| R-009 | Implement config integrity verification               | T-PERSIST-003 |
| R-010 | Add update signing and version pinning                | T-PERSIST-002 |

---

## 7. Appendices

### 7.1 ATLAS Technique Mapping

| ATLAS ID                                      | Technique Name                                 | OpenClaw Threats                                                 |
| --------------------------------------------- | ---------------------------------------------- | ---------------------------------------------------------------- |
| AML.T0006                     | Active Scanning                                | T-RECON-001, T-RECON-002                                         |
| AML.T0009                     | Collection                                     | T-EXFIL-001, T-EXFIL-002, T-EXFIL-003                            |
| AML.T0010.001 | Supply Chain: AI Software      | T-PERSIST-001, T-PERSIST-002                                     |
| AML.T0010.002 | Supply Chain: Data             | T-PERSIST-003                                                    |
| AML.T0031                     | Erode AI Model Integrity                       | T-IMPACT-001, T-IMPACT-002, T-IMPACT-003                         |
| AML.T0040                     | AI Model Inference API Access                  | T-ACCESS-001, T-ACCESS-002, T-ACCESS-003, T-DISC-001, T-DISC-002 |
| AML.T0043                     | Craft Adversarial Data                         | T-EXEC-004, T-EVADE-001, T-EVADE-002                             |
| AML.T0051.000 | LLM Prompt Injection: Direct   | T-EXEC-001, T-EXEC-003                                           |
| AML.T0051.001 | LLM Prompt Injection: Indirect | T-EXEC-002                                                       |

### 7.2 Key Security Files

| Path                                | Purpose                     | Risk Level   |
| ----------------------------------- | --------------------------- | ------------ |
| `src/infra/exec-approvals.ts`       | Command approval logic      | **Critical** |
| `src/gateway/auth.ts`               | Gateway authentication      | **Critical** |
| `src/web/inbound/access-control.ts` | Channel access control      | **Critical** |
| `src/infra/net/ssrf.ts`             | SSRF protection             | **Critical** |
| `src/security/external-content.ts`  | Prompt injection mitigation | **Critical** |
| `src/agents/sandbox/tool-policy.ts` | Tool policy enforcement     | **Critical** |
| `convex/lib/moderation.ts`          | ClawHub moderation          | **High**     |
| `convex/lib/skillPublish.ts`        | Skill publishing flow       | **High**     |
| `src/routing/resolve-route.ts`      | Session isolation           | **Medium**   |

### 7.3 Glossary

| Term                 | Definition                                                |
| -------------------- | --------------------------------------------------------- |
| **ATLAS**            | MITRE's Adversarial Threat Landscape for AI Systems       |
| **ClawHub**          | OpenClaw's skill marketplace                              |
| **Gateway**          | OpenClaw's message routing and authentication layer       |
| **MCP**              | Model Context Protocol - tool provider interface          |
| **Prompt Injection** | Attack where malicious instructions are embedded in input |
| **Skill**            | Downloadable extension for OpenClaw agents                |
| **SSRF**             | Server-Side Request Forgery                               |

---

_This threat model is a living document. Report security issues to security@openclaw.ai_
