# OpenClaw Tahdidlar Modeliga hissa qo‘shish

OpenClaw’ni yanada xavfsiz qilishga yordam berganingiz uchun rahmat. Ushbu tahdidlar modeli doimiy ravishda yangilanib boriladigan hujjat bo‘lib, biz hammaning hissasini mamnuniyat bilan qabul qilamiz — xavfsizlik bo‘yicha mutaxassis bo‘lish shart emas.

## Hissa qo‘shish usullari

### Tahdid qo‘shing

Biz qamrab olmagan hujum vektori yoki xavfni payqadingizmi? [openclaw/trust](https://github.com/openclaw/trust/issues) da issue oching va uni o‘z so‘zlaringiz bilan tasvirlab bering. Hech qanday freymvorklarni bilishingiz yoki har bir maydonni to‘ldirishingiz shart emas — faqat ssenariyni tasvirlab bering.

**Qo‘shish foydali (lekin majburiy emas):**

- Hujum ssenariysi va undan qanday foydalanish mumkinligi
- OpenClaw’ning qaysi qismlari ta’sirlangan (CLI, gateway, kanallar, ClawHub, MCP serverlari va hokazo)
- Qanchalik jiddiy deb o‘ylaysiz (past / o‘rta / yuqori / kritik)
- Tegishli tadqiqotlar, CVElar yoki real hayotdagi misollarga havolalar

We'll handle the ATLAS mapping, threat IDs, and risk assessment during review. If you want to include those details, great - but it's not expected.

> **This is for adding to the threat model, not reporting live vulnerabilities.** If you've found an exploitable vulnerability, see our [Trust page](https://trust.openclaw.ai) for responsible disclosure instructions.

### Suggest a Mitigation

Have an idea for how to address an existing threat? Open an issue or PR referencing the threat. Useful mitigations are specific and actionable - for example, "per-sender rate limiting of 10 messages/minute at the gateway" is better than "implement rate limiting."

### Propose an Attack Chain

Attack chains show how multiple threats combine into a realistic attack scenario. If you see a dangerous combination, describe the steps and how an attacker would chain them together. A short narrative of how the attack unfolds in practice is more valuable than a formal template.

### Fix or Improve Existing Content

Typos, clarifications, outdated info, better examples - PRs welcome, no issue needed.

## What We Use

### MITRE ATLAS

This threat model is built on [MITRE ATLAS](https://atlas.mitre.org/) (Adversarial Threat Landscape for AI Systems), a framework designed specifically for AI/ML threats like prompt injection, tool misuse, and agent exploitation. You don't need to know ATLAS to contribute - we map submissions to the framework during review.

### Threat IDs

Each threat gets an ID like `T-EXEC-003`. The categories are:

| Code    | Category                                   |
| ------- | ------------------------------------------ |
| RECON   | Reconnaissance - information gathering     |
| ACCESS  | Initial access - gaining entry             |
| EXEC    | Execution - running malicious actions      |
| PERSIST | Persistence - maintaining access           |
| EVADE   | Defense evasion - avoiding detection       |
| DISC    | Discovery - learning about the environment |
| EXFIL   | Exfiltration - stealing data               |
| IMPACT  | Impact - damage or disruption              |

IDs are assigned by maintainers during review. You don't need to pick one.

### Risk Levels

| Level        | Meaning                                                           |
| ------------ | ----------------------------------------------------------------- |
| **Critical** | Full system compromise, or high likelihood + critical impact      |
| **High**     | Significant damage likely, or medium likelihood + critical impact |
| **Medium**   | Moderate risk, or low likelihood + high impact                    |
| **Low**      | Unlikely and limited impact                                       |

If you're unsure about the risk level, just describe the impact and we'll assess it.

## Review Process

1. **Triage** - We review new submissions within 48 hours
2. **Assessment** - We verify feasibility, assign ATLAS mapping and threat ID, validate risk level
3. **Documentation** - We ensure everything is formatted and complete
4. **Merge** - Added to the threat model and visualization

## Resources

- [ATLAS Website](https://atlas.mitre.org/)
- [ATLAS Techniques](https://atlas.mitre.org/techniques/)
- [ATLAS Case Studies](https://atlas.mitre.org/studies/)
- [OpenClaw Threat Model](./THREAT-MODEL-ATLAS.md)

## Contact

- **Security vulnerabilities:** See our [Trust page](https://trust.openclaw.ai) for reporting instructions
- **Threat model questions:** Open an issue on [openclaw/trust](https://github.com/openclaw/trust/issues)
- **General chat:** Discord #security channel

## Recognition

Contributors to the threat model are recognized in the threat model acknowledgments, release notes, and the OpenClaw security hall of fame for significant contributions.
