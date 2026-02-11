---
summary: "Agent bootstrapping ritual that seeds the workspace and identity files"
read_when:
  - Understanding what happens on the first agent run
  - Explaining where bootstrapping files live
  - Debugging onboarding identity setup
title: "Agent Bootstrapping"
sidebarTitle: "1. Bootstraplash"
---

# 2. Agentni bootstraplash

3. Bootstraplash — bu agent ish maydonini tayyorlaydigan va shaxsni aniqlash maʼlumotlarini yigʻadigan **birinchi ishga tushirish** marosimi. 4. Bu onboardingdan keyin, agent birinchi marta ishga tushirilganda sodir boʻladi.

## 5. Bootstraplash nima qiladi

6. Agent birinchi marta ishga tushirilganda, OpenClaw ish maydonini bootstraplaydi (standart: `~/.openclaw/workspace`):

- 7. `AGENTS.md`, `BOOTSTRAP.md`, `IDENTITY.md`, `USER.md` fayllarini yaratadi.
- Qisqa savol-javob marosimini bajaradi (bir vaqtning o‘zida bitta savol).
- 9. Shaxsiyat + afzalliklarni `IDENTITY.md`, `USER.md`, `SOUL.md` fayllariga yozadi.
- 10. Tugagach `BOOTSTRAP.md` ni olib tashlaydi, shunda u faqat bir marta ishlaydi.

## 11. Qayerda ishlaydi

12. Bootstraplash har doim **gateway xosti**da ishlaydi. 13. Agar macOS ilovasi masofaviy Gatewayʼga ulangan boʻlsa, ish maydoni va bootstraplash fayllari o‘sha masofaviy mashinada joylashadi.

<Note>14.
Gateway boshqa mashinada ishlayotgan bo‘lsa, ish maydoni fayllarini gateway xostida tahrirlang (masalan, `user@gateway-host:~/.openclaw/workspace`).</Note>

## 15. Tegishli hujjatlar

- 16. macOS ilovasini onboarding qilish: [Onboarding](/start/onboarding)
- 17. Ish maydoni tuzilishi: [Agent workspace](/concepts/agent-workspace)
